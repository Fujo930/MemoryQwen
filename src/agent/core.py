"""
MemoryQwen — Agent Core 核心主循环
"""

from __future__ import annotations

import time
import logging
from typing import Any
from dataclasses import dataclass, field

from src.model_adapter.base import BaseModelAdapter, ChatResult
from src.memory_bus import MemoryBus
from src.agent.context import ContextBuilder, AgentContext

logger = logging.getLogger(__name__)


@dataclass
class SourceRef:
    """来源引用"""
    title: str = ""
    source: str = ""
    snippet: str = ""


@dataclass
class AgentResponse:
    """Agent 响应"""
    content: str
    sources: list[SourceRef] = field(default_factory=list)
    token_usage: dict = field(default_factory=dict)
    model_used: str = ""
    latency_ms: float = 0.0
    error: str | None = None


class Agent:
    """Agent 主循环"""

    def __init__(
        self,
        config: Any,
        model_adapter: BaseModelAdapter,
        memory_bus: MemoryBus,
    ):
        self.config = config
        self.adapter = model_adapter
        self.memory = memory_bus
        self.context_builder = ContextBuilder(config, memory_bus.chat, memory_bus)

    async def process_message(
        self,
        message: str,
        session_id: str,
        model_tier: str = "light",
    ) -> AgentResponse:
        """处理单条用户消息"""
        start = time.time()

        try:
            # 1. 构建上下文
            context = await self.context_builder.build(
                message=message,
                session_id=session_id,
            )

            # 2. 选择模型
            model = self._select_model(model_tier)

            # 3. 调用模型
            chat_messages = context.to_messages()
            result = await self.adapter.chat(
                messages=chat_messages,
                model=model,
                temperature=0.7,
                max_tokens=self._get_max_tokens(model_tier),
            )

            # 4. 提取来源
            sources = self._extract_sources(context)

            # 5. 保存聊天记录
            await self.memory.chat.add_message(
                session_id=session_id,
                role="user",
                content=message,
                tokens=result.token_usage.get("prompt", 0),
            )
            await self.memory.chat.add_message(
                session_id=session_id,
                role="assistant",
                content=result.content,
                sources=[s.__dict__ for s in sources],
                tokens=result.token_usage.get("completion", 0),
            )

            elapsed = (time.time() - start) * 1000

            return AgentResponse(
                content=result.content,
                sources=sources,
                token_usage=result.token_usage,
                model_used=result.model,
                latency_ms=round(elapsed, 2),
            )

        except Exception as e:
            elapsed = (time.time() - start) * 1000
            logger.error("Agent process_message failed: %s", e)
            return AgentResponse(
                content=f"抱歉，处理消息时出错: {str(e)}",
                model_used="",
                latency_ms=round(elapsed, 2),
                error=str(e),
            )

    async def process_message_stream(
        self,
        message: str,
        session_id: str,
    ):
        """流式处理（AsyncGenerator）"""
        # 简化：先收集完整结果，再逐字 yield
        response = await self.process_message(message, session_id)
        for char in response.content:
            yield char

    def _select_model(self, tier: str) -> str:
        """选择模型"""
        if tier == "deep":
            return self.config.model.default_deep_model
        return self.config.model.default_light_model

    def _get_max_tokens(self, tier: str) -> int:
        """获取模型最大输出 token"""
        if tier == "deep":
            return 8192
        return 4096

    def _extract_sources(self, context: AgentContext) -> list[SourceRef]:
        """从上下文中提取来源引用"""
        sources = []
        for mem in context.memories:
            path = mem.metadata.get("source_path", "") if hasattr(mem, 'metadata') else ""
            title = mem.metadata.get("doc_title", "") if hasattr(mem, 'metadata') else ""
            sources.append(SourceRef(
                title=title or path.split("/")[-1] if path else "unknown",
                source=path,
                snippet=mem.content[:150] if mem.content else "",
            ))
        return sources[:5]
