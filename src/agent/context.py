"""
MemoryQwen — Agent Context 上下文构建器
管理有限的上下文窗口，按优先级分层构建提示词
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from src.memory_bus import MemoryBus
from src.memory_bus.chat_memory import ChatMemory
from src.memory_bus.base import ScoredEntry

logger = logging.getLogger(__name__)


@dataclass
class AgentContext:
    """Agent 上下文"""
    system_prompt: str = ""
    memories: list[ScoredEntry] = field(default_factory=list)
    error_memories: list[ScoredEntry] = field(default_factory=list)
    chat_history: list[dict] = field(default_factory=list)
    current_message: str = ""
    session_summary: str = ""
    total_tokens: int = 0
    budget: dict = field(default_factory=dict)

    def to_messages(self) -> list[dict]:
        """将上下文转为模型消息列表"""
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]

        # 记忆注入
        memory_context = self._format_memories()
        if memory_context:
            messages.append({"role": "system", "content": memory_context})

        # 错误经验注入
        error_context = self._format_errors()
        if error_context:
            messages.append({"role": "system", "content": error_context})

        # 会话摘要
        if self.session_summary:
            messages.append({
                "role": "system",
                "content": f"[会话摘要]\n{self.session_summary}",
            })

        # 历史消息
        for msg in self.chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # 当前消息
        messages.append({"role": "user", "content": self.current_message})

        return messages

    def _format_memories(self) -> str:
        """格式化知识库记忆"""
        if not self.memories:
            return ""
        parts = ["[相关知识]"]
        for i, m in enumerate(self.memories[:5], 1):
            source = m.metadata.get("source_path", "unknown") if hasattr(m, 'metadata') else "unknown"
            parts.append(f"{i}. [{source}] {m.content[:300]}")
        return "\n".join(parts)

    def _format_errors(self) -> str:
        """格式化错误经验"""
        if not self.error_memories:
            return ""
        parts = ["[历史错误经验—请避免重犯]"]
        for i, m in enumerate(self.error_memories[:3], 1):
            parts.append(f"{i}. {m.content[:300]}")
        return "\n".join(parts)


class ContextBuilder:
    """上下文构建器——管理 token 预算"""

    def __init__(self, config: Any, chat_memory: ChatMemory, memory_bus: MemoryBus):
        self.config = config
        self.chat_memory = chat_memory
        self.memory_bus = memory_bus
        self.budget = config.agent.context_budget

    async def build(
        self,
        message: str,
        session_id: str,
        model_max_tokens: int = 8192,
    ) -> AgentContext:
        """构建 Agent 上下文"""
        context = AgentContext(current_message=message)
        context.budget = {
            "total": model_max_tokens,
            "reserved_response": self.budget.response_reserved,
            "available": model_max_tokens - self.budget.response_reserved,
        }

        # 1. 构建系统提示词
        session = await self.chat_memory.get_session(session_id)
        session_summary = session.get("summary", "") if session else ""

        context.system_prompt = self._build_system_prompt(session_summary)
        context.session_summary = session_summary

        # 2. 检索知识库记忆
        try:
            memories = await self.memory_bus.hybrid_search(
                message,
                stores=["knowledge"],
                top_k=self.config.memory.retrieval.top_k,
            )
            context.memories = memories
        except Exception as e:
            logger.warning("Memory retrieval failed: %s", e)

        # 3. 检索错误经验
        try:
            errors = await self.memory_bus.hybrid_search(
                message,
                stores=["errors"],
                top_k=3,
            )
            context.error_memories = errors
        except Exception as e:
            logger.warning("Error retrieval failed: %s", e)

        # 4. 加载聊天历史
        history = await self.chat_memory.get_history(
            session_id,
            limit=self.config.memory.chat.max_history,
        )
        context.chat_history = [
            {"role": m["role"], "content": m["content"]}
            for m in history[-20:]  # 最近 20 条
        ]

        # 5. 计算总 token
        messages = context.to_messages()
        context.total_tokens = self._estimate_tokens(messages)

        # 6. 如果超出预算，压缩
        if context.total_tokens > context.budget["available"]:
            context = await self._compress(context)

        return context

    def _build_system_prompt(self, session_summary: str) -> str:
        """构建系统提示词"""
        return f"""你是 MemoryQwen，一个运行在本地电脑上的 AI 助手。

【能力】
- 你擅长回答问题、分析资料、编写代码。
- 你可以检索本地知识库中的资料来回答用户问题。
- 你从历史错误中学习，避免重复犯错。

【规则】
- 回答中文问题时使用中文。
- 当引用知识库内容时，请注明来源（文件名）。
- 如果不知道答案，请直接说不知道，不要编造。
- 用户指出错误时，请承认并记住。

【格式】
- 使用 markdown 格式回复。
- 代码块标注语言。
- 列表清晰分段。"""

    def _estimate_tokens(self, messages: list[dict]) -> int:
        """估算消息列表的总 token 数"""
        total = 0
        for msg in messages:
            total += len(msg.get("content", "")) * 1.5  # 粗略估算
            total += 10  # 消息头开销
        return int(total) + 50  # 格式开销

    async def _compress(self, context: AgentContext) -> AgentContext:
        """压缩上下文以适配 budget"""
        # 优先压缩记忆
        while (context.total_tokens > context.budget["available"]
               and len(context.memories) > 1):
            context.memories.pop()
            context.total_tokens = self._estimate_tokens(context.to_messages())

        # 然后压缩聊天历史
        while (context.total_tokens > context.budget["available"]
               and len(context.chat_history) > 4):
            context.chat_history.pop(0)  # 移除最早消息
            context.total_tokens = self._estimate_tokens(context.to_messages())

        if context.total_tokens > context.budget["available"]:
            logger.warning("Context still over budget: %d > %d",
                           context.total_tokens, context.budget["available"])

        return context
