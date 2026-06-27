"""
MemoryQwen — Smart Retrieval Gate v0.1.2
Determines whether to retrieve long-term stores based on user message content.
Uses deterministic heuristic rules, not LLM calls.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class RetrievalDecision:
    should_retrieve: bool = False
    store_types: list[str] = field(default_factory=list)
    top_k: int = 0
    reason: str = "no_decision"
    confidence: float = 0.0
    risk_level: str = "low"
    use_recent_chat: bool = True
    skipped_retrieval: bool = False


# ─── Casual / skip phrases ────────────────────────────────

CASUAL_SKIP = {
    "你好", "hi", "hello", "hey", "谢谢", "thanks", "thank you",
    "好的", "ok", "okay", "收到", "继续", "可以", "晚安", "早",
    "测试一下", "你在吗", "are you there", "在吗", "在不在",
    "拜拜", "bye", "goodbye", "再见", "👋",
    # Extended casual patterns
    "天气不错", "今天天气", "吃了吗", "怎么样", "how are you",
    "周末愉快", "辛苦了", "加油", "不错", "很好",
}

EXPLICIT_NO_MEMORY = {
    "不用查资料", "不要查资料", "不要查 memory", "不用检索",
    "别查", "不要搜", "skip retrieval", "no retrieval",
    "don't search", "不用搜", "不用查",
}

# ─── High-risk capability boundary keywords ──────────────

HIGH_RISK_TERMS = {
    "PDF", "DOCX", "Web UI", "FastAPI", "Internet Query",
    "联网", "web search", "web ingest", "embedding",
    "vector DB", "向量", "crawler", "爬虫", "daemon",
    "tray", "托盘", "自动卸载", "kill 进程", "kill process",
    "LoRA", "微调", "fine-tuning", "fine tuning",
    "cli webui", "cli pdf ingest", "cli daemon start",
    "cli model unload", "cli crawler", "cli internet",
    "cli fastapi", "rebuild from sources", "cli tray",
    "model unload",
}

# ─── MemoryQwen project keywords ─────────────────────────

PROJECT_TERMS = {
    "memoryqwen", "v0.1", "v0.1.2", "v0.2", "issue",
    "megatrain", "m1", "m2", "checkpoint", "release",
    "devpack", "training_packs", "training_logs",
    "eval", "judge", "source archive", "memory/sources",
    "memoryqwen.db", "tasks.db", "gpu guardian",
    "task runtime", "background job runner",
    "capability guard", "capability boundary guard",
    "cli", "agentchatservice", "retrievalgate",
    "promptbuilder", "ingestionpipeline",
}

# ─── Error / Strategy keywords ───────────────────────────

ERROR_STRATEGY_TERMS = {
    "错题", "纠错", "上次错", "不要再", "wrong_answer",
    "correct_answer", "failure_type", "策略", "strategy",
    "反例", "避免", "幻觉", "overclaim", "false negative",
    "false positive", "error_store", "strategy_store",
    "correct命令", "correct 命令", "error learning",
    "strategy learning",
}

# ─── Model / Hardware keywords ───────────────────────────

MODEL_HARDWARE_TERMS = {
    "3b", "7b", "14b", "32b", "70b", "qwen",
    "模型推荐", "常驻", "deep mode", "深度模式",
    "rtx", "显存", "vram", "gpu", "4080", "3080", "3060",
    "q4", "q5", "q6", "量化", "num_ctx", "kv cache",
    "上下文长度", "模型选择", "选什么模型", "用什么模型",
}


class RetrievalGate:
    """Deterministic heuristic retrieval gate."""

    def __init__(self, config=None):
        self.enabled = getattr(
            getattr(config, "agent", None), "use_retrieval_gate", True
        ) if config else True
        self.default_retrieve = getattr(
            getattr(config, "agent", None), "retrieval_gate_default_retrieve", True
        ) if config else True
        self.min_confidence = getattr(
            getattr(config, "agent", None), "retrieval_gate_min_confidence", 0.4
        ) if config else 0.4
        self.max_top_k = getattr(
            getattr(config, "agent", None), "retrieval_gate_max_top_k", 5
        ) if config else 5

    def decide(self, user_message: str,
               chat_history: list | None = None) -> RetrievalDecision:
        """Determine whether and which stores to retrieve."""
        if not self.enabled:
            return RetrievalDecision(
                should_retrieve=True,
                store_types=["knowledge_store", "error_store", "strategy_store"],
                top_k=self.max_top_k,
                reason="gate_disabled",
                confidence=1.0,
                risk_level="medium",
            )

        msg = user_message.strip()
        msg_lower = msg.lower()

        # ─── Rule 1: Casual / skip ───
        if msg in CASUAL_SKIP or msg_lower in {s.lower() for s in CASUAL_SKIP}:
            return RetrievalDecision(
                should_retrieve=False,
                store_types=[],
                top_k=0,
                reason="casual_skip",
                confidence=0.9,
                risk_level="low",
                skipped_retrieval=True,
            )

        # Short casual messages (< 2 chars, not a query)
        if len(msg) <= 1:
            return RetrievalDecision(
                should_retrieve=False,
                store_types=[],
                top_k=0,
                reason="short_casual",
                confidence=0.7,
                risk_level="low",
                skipped_retrieval=True,
            )

        # ─── Rule 2: Explicit no-memory ───
        if any(kw in msg for kw in EXPLICIT_NO_MEMORY):
            return RetrievalDecision(
                should_retrieve=False,
                store_types=[],
                top_k=0,
                reason="explicit_no_memory",
                confidence=0.95,
                risk_level="low",
                skipped_retrieval=True,
            )

        # ─── Rule 3: High-risk capability boundary → retrieve all ───
        high_risk_hits = []
        for term in HIGH_RISK_TERMS:
            if term.lower() in msg_lower:
                high_risk_hits.append(term)
        if high_risk_hits:
            return RetrievalDecision(
                should_retrieve=True,
                store_types=["knowledge_store", "error_store", "strategy_store"],
                top_k=min(5, self.max_top_k),
                reason=f"capability_boundary_risk:{','.join(high_risk_hits[:3])}",
                confidence=0.95,
                risk_level="high",
            )

        # ─── Rule 4: Error/Strategy terms → error + strategy ───
        es_hits = [t for t in ERROR_STRATEGY_TERMS if t.lower() in msg_lower]
        if es_hits:
            stores = ["error_store", "strategy_store"]
            # Also add knowledge if project terms also hit
            proj_hits = [t for t in PROJECT_TERMS if t.lower() in msg_lower]
            if proj_hits:
                stores.append("knowledge_store")
            return RetrievalDecision(
                should_retrieve=True,
                store_types=stores,
                top_k=min(3, self.max_top_k),
                reason="error_strategy_question",
                confidence=0.9,
                risk_level="medium",
            )

        # ─── Rule 5: Project terms → knowledge + strategy ───
        proj_hits = [t for t in PROJECT_TERMS if t.lower() in msg_lower]
        if proj_hits:
            return RetrievalDecision(
                should_retrieve=True,
                store_types=["knowledge_store", "strategy_store"],
                top_k=min(5, self.max_top_k),
                reason="memoryqwen_project_question",
                confidence=0.85,
                risk_level="medium",
            )

        # ─── Rule 6: Model/Hardware terms → knowledge + strategy ───
        mh_hits = [t for t in MODEL_HARDWARE_TERMS if t.lower() in msg_lower]
        if mh_hits:
            return RetrievalDecision(
                should_retrieve=True,
                store_types=["knowledge_store", "strategy_store"],
                top_k=min(5, self.max_top_k),
                reason="model_hardware_question",
                confidence=0.85,
                risk_level="medium",
            )

        # ─── Rule 7: Default — low confidence, conservative retrieve ───
        if self.default_retrieve:
            return RetrievalDecision(
                should_retrieve=True,
                store_types=["knowledge_store"],
                top_k=min(3, self.max_top_k),
                reason="low_confidence_default_retrieve",
                confidence=self.min_confidence,
                risk_level="low",
            )
        else:
            return RetrievalDecision(
                should_retrieve=False,
                store_types=[],
                top_k=0,
                reason="low_confidence_default_skip",
                confidence=self.min_confidence,
                risk_level="low",
                skipped_retrieval=True,
            )
