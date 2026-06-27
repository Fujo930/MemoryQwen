"""
MemoryQwen — AgentChatService
编排 Agent 聊天管线：检索 → 构建 prompt → 调用模型 → 保存记录
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

from src.agent.models import (
    ChatRequest, SourceCitation, ErrorCitation, StrategyCitation,
    AgentChatResponse,
)
from src.agent.prompt_builder import PromptBuilder
from src.agent.capability_guard import CapabilityBoundaryGuard, CapabilityGuardResult
from src.agent.retrieval_gate import RetrievalGate, RetrievalDecision

logger = logging.getLogger(__name__)

CHAT_STORE = "chat_messages"
ERROR_STORE = "error_store"
STRATEGY_STORE = "strategy_store"
SNIPPET_MAX_CHARS = 240


class AgentChatService:
    """Agent 聊天服务"""

    def __init__(self, config: Any, model_client, retriever, store):
        self.config = config
        self.model_client = model_client
        self.retriever = retriever
        self.store = store
        self.prompt_builder = PromptBuilder(
            system_prompt=config.agent.system_prompt,
        )
        self.retrieval_gate = RetrievalGate(config)

    async def chat(self, request: ChatRequest) -> AgentChatResponse:
        if not request.message.strip():
            raise ValueError("消息不能为空")

        session_id = request.session_id or str(uuid.uuid4())

        # 1. 保存 user message
        await self.store.add(CHAT_STORE, {
            "session_id": session_id,
            "role": "user",
            "content": request.message,
            "metadata": {"session_id": session_id, "role": "user"},
        })

        # 2. 检索
        retrieved = []
        error_retrieved = []
        strategy_retrieved = []

        # 1.5 能力边界检测
        cap_guard_result = CapabilityGuardResult()
        memory_used = []
        try:
            guard = CapabilityBoundaryGuard()
            cap_guard_result = guard.detect(request.message)
        except Exception as e:
            logger.warning("Capability guard failed: %s", e)

        # 1.6 检索门控
        gate_decision = RetrievalDecision(should_retrieve=True,
            store_types=["knowledge_store", "error_store", "strategy_store"],
            top_k=5, reason="default")
        retrieval_skipped = False
        try:
            gate_decision = self.retrieval_gate.decide(request.message)
            retrieval_skipped = gate_decision.skipped_retrieval
        except Exception as e:
            logger.warning("Retrieval gate failed: %s", e)

        # 2. 检索知识、错误、策略（受 gate 控制）
        if "knowledge_store" in gate_decision.store_types:
            try:
                retrieved = await self.retriever.search(
                    query=request.message, top_k=request.top_k,
                )
                memory_used.append("knowledge_store")
            except Exception as e:
                logger.warning("Knowledge retrieval failed: %s", e)

        if self.config.agent.use_error_memory and "error_store" in gate_decision.store_types:
            try:
                error_retrieved = await self._search_errors(request.message)
                memory_used.append("error_store")
            except Exception as e:
                logger.warning("Error retrieval failed: %s", e)

        if self.config.agent.use_strategy_memory and "strategy_store" in gate_decision.store_types:
            try:
                strategy_retrieved = await self._search_strategies(request.message)
                memory_used.append("strategy_store")
            except Exception as e:
                logger.warning("Strategy retrieval failed: %s", e)

        # 3. 获取最近对话
        recent_chat = []
        if request.include_recent:
            try:
                recent_chat = await self._get_recent_chat(
                    session_id, request.max_recent_messages,
                )
            except Exception as e:
                logger.warning("Recent chat failed: %s", e)

        # 4. 构建 error/strategy cases
        error_cases = [
            {
                "failure_type": (e.get("metadata", {}) or {}).get("failure_type", "general"),
                "wrong_answer": self._extract_field(e.get("content", ""), "Wrong Answer"),
                "correct_answer": self._extract_field(e.get("content", ""), "Correct Answer"),
                "strategy": self._extract_field(e.get("content", ""), "Strategy"),
            }
            for e in error_retrieved
        ]

        strategy_cases = [
            {
                "strategy": (s.get("metadata", {}) or {}).get("strategy", 
                    self._extract_field(s.get("content", ""), "Strategy")),
                "failure_type": (s.get("metadata", {}) or {}).get("failure_type", "general"),
                "avoid": self._extract_field(s.get("content", ""), "Avoid"),
                "prefer": self._extract_field(s.get("content", ""), "Prefer"),
            }
            for s in strategy_retrieved
        ]

        # 5. 构建 prompt
        messages = self.prompt_builder.build(
            user_message=request.message,
            retrieved=retrieved,
            recent_chat=recent_chat,
            error_cases=error_cases,
            strategy_cases=strategy_cases,
            max_error_context_chars=self.config.agent.max_error_context_chars,
            max_strategy_context_chars=self.config.agent.max_strategy_context_chars,
            capability_guard_result=cap_guard_result if cap_guard_result.is_capability_question else None,
        )

        # 6. 调用模型
        try:
            model_response = await self.model_client.chat(messages=messages)
        except Exception as e:
            logger.error("Model call failed: %s", e)
            raise

        # 7. 构建 citations
        sources = self._build_sources(retrieved)
        error_sources = self._build_error_sources(error_retrieved)
        strategy_sources = self._build_strategy_sources(strategy_retrieved)

        # 8. 保存 assistant answer
        if self.config.agent.save_chat_memory:
            await self.store.add(CHAT_STORE, {
                "session_id": session_id,
                "role": "assistant",
                "content": model_response.content,
                "metadata": {
                    "session_id": session_id,
                    "role": "assistant",
                    "sources": [s.__dict__ for s in sources],
                },
            })

        # 9. 返回
        metadata = {
            "retrieval_count": len(retrieved),
            "error_count": len(error_sources),
            "strategy_count": len(strategy_sources),
            "error_memory_used": len(error_sources) > 0,
            "strategy_memory_used": len(strategy_sources) > 0,
            "memory_used": memory_used,
            "recent_messages_count": len(recent_chat),
            "capability_guard_triggered": cap_guard_result.is_capability_question,
            "capability_guard_terms": cap_guard_result.matched_terms,
            "capability_guard_risk_level": cap_guard_result.risk_level,
            "retrieval_gate_enabled": self.retrieval_gate.enabled,
            "retrieval_gate_should_retrieve": gate_decision.should_retrieve,
            "retrieval_gate_stores": gate_decision.store_types,
            "retrieval_gate_reason": gate_decision.reason,
            "retrieval_gate_confidence": gate_decision.confidence,
            "retrieval_gate_risk_level": gate_decision.risk_level,
            "retrieval_skipped": retrieval_skipped,
        }
        if cap_guard_result.is_capability_question:
            memory_used.append("capability_guard")

        return AgentChatResponse(
            answer=model_response.content,
            session_id=session_id,
            sources=sources,
            error_sources=error_sources,
            strategy_sources=strategy_sources,
            memory_used=memory_used,
            model=getattr(model_response, "model", ""),
            prompt_tokens_estimate=model_response.usage.get("total_tokens", 0),
            metadata=metadata,
        )

    async def _search_errors(self, query: str) -> list:
        try:
            results = await self.store.search_keyword(
                ERROR_STORE, query, limit=self.config.agent.error_top_k,
            )
            filtered = [
                r for r in results
                if r.get("metadata", {}).get("record_kind", "") == "error_case"
                 or "error_case" in str(r.get("title", ""))
            ]
            # Fallback: if no results and enabled, return recent errors
            if not filtered and self.config.agent.error_memory_recent_fallback:
                recent = await self.store.list(ERROR_STORE, limit=self.config.agent.error_top_k)
                for r in recent:
                    meta = r.get("metadata", {})
                    if isinstance(meta, str):
                        import json
                        try: meta = json.loads(meta)
                        except: meta = {}
                    if meta.get("record_kind") == "error_case":
                        r["metadata"] = {**meta, "retrieval_method": "recent_fallback"}
                        filtered.append(r)
            return filtered
        except Exception:
            return []

    async def _search_strategies(self, query: str) -> list:
        try:
            results = await self.store.search_keyword(
                STRATEGY_STORE, query, limit=self.config.agent.strategy_top_k,
            )
            filtered = [
                r for r in results
                if r.get("metadata", {}).get("record_kind", "") == "strategy"
                 or "strategy:" in str(r.get("title", ""))
            ]
            if not filtered and self.config.agent.strategy_memory_recent_fallback:
                recent = await self.store.list(STRATEGY_STORE, limit=self.config.agent.strategy_top_k)
                for r in recent:
                    meta = r.get("metadata", {})
                    if isinstance(meta, str):
                        import json
                        try: meta = json.loads(meta)
                        except: meta = {}
                    if meta.get("record_kind") == "strategy":
                        r["metadata"] = {**meta, "retrieval_method": "recent_fallback"}
                        filtered.append(r)
            return filtered
        except Exception:
            return []

    async def _get_recent_chat(self, session_id: str, limit: int) -> list[dict]:
        try:
            records = await self.store.list_by_metadata(
                store_type=CHAT_STORE,
                filters={"session_id": session_id},
                limit=limit,
                order_by="created_at",
                descending=True,
            )
            records.reverse()
            return [
                {"role": r.get("role", ""), "content": r.get("content", "")}
                for r in records
            ]
        except Exception:
            return []

    def _build_sources(self, retrieved: list) -> list[SourceCitation]:
        sources = []
        for r in retrieved:
            snippet = r.content[:SNIPPET_MAX_CHARS]
            if len(r.content) > SNIPPET_MAX_CHARS:
                snippet += "…"
            sources.append(SourceCitation(
                record_id=r.record_id, title=r.title,
                source_path=r.source_path, chunk_index=r.chunk_index,
                score=r.score, snippet=snippet,
            ))
        return sources

    def _build_error_sources(self, retrieved: list) -> list[ErrorCitation]:
        sources = []
        for e in retrieved:
            content = e.get("content", "") if isinstance(e, dict) else getattr(e, "content", "")
            meta = e.get("metadata", {}) if isinstance(e, dict) else getattr(e, "metadata", {})
            if isinstance(meta, str):
                try: meta = json.loads(meta)
                except: meta = {}
            rid = e.get("record_id", e.get("id", "")) if isinstance(e, dict) else getattr(e, "record_id", getattr(e, "id", ""))
            score = e.get("score", 0.0) if isinstance(e, dict) else getattr(e, "score", 0.0)
            snippet = content[:SNIPPET_MAX_CHARS]
            if len(content) > SNIPPET_MAX_CHARS:
                snippet += "…"
            sources.append(ErrorCitation(
                record_id=rid,
                task=meta.get("task", ""),
                failure_type=meta.get("failure_type", ""),
                strategy=meta.get("strategy", ""),
                score=score,
                snippet=snippet,
            ))
        return sources

    def _build_strategy_sources(self, retrieved: list) -> list[StrategyCitation]:
        sources = []
        for s in retrieved:
            content = s.get("content", "") if isinstance(s, dict) else getattr(s, "content", "")
            meta = s.get("metadata", {}) if isinstance(s, dict) else getattr(s, "metadata", {})
            if isinstance(meta, str):
                try: meta = json.loads(meta)
                except: meta = {}
            rid = s.get("record_id", s.get("id", "")) if isinstance(s, dict) else getattr(s, "record_id", getattr(s, "id", ""))
            score = s.get("score", 0.0) if isinstance(s, dict) else getattr(s, "score", 0.0)
            snippet = content[:SNIPPET_MAX_CHARS]
            if len(content) > SNIPPET_MAX_CHARS:
                snippet += "…"
            sources.append(StrategyCitation(
                record_id=rid,
                title=s.get("title", "") if isinstance(s, dict) else getattr(s, "title", ""),
                strategy=meta.get("strategy", "") or self._extract_field(content, "Strategy"),
                failure_type=meta.get("failure_type", "general"),
                score=score,
                snippet=snippet,
                source_error_ids=meta.get("source_error_ids", []),
            ))
        return sources

    @staticmethod
    def _extract_field(content: str, field_name: str) -> str:
        for line in content.split("\n"):
            if line.startswith(f"{field_name}: "):
                return line[len(field_name) + 2:]
        return ""
