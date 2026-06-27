"""
MemoryQwen — MemoryBus 统一入口
"""

from __future__ import annotations

import logging
from typing import Any

from src.memory_bus.knowledge_store import KnowledgeStore
from src.memory_bus.chat_memory import ChatMemory
from src.memory_bus.error_store import ErrorStore
from src.memory_bus.base import ScoredEntry

logger = logging.getLogger(__name__)


class MemoryBus:
    """MemoryBus 统一入口——组合所有存储模块"""

    def __init__(self, config: Any):
        self.config = config
        self.knowledge = KnowledgeStore(config)
        self.chat = ChatMemory(config)
        self.errors = ErrorStore(config)
        logger.info("MemoryBus initialized")

    async def hybrid_search(
        self,
        query: str,
        stores: list[str] | None = None,
        top_k: int = 5,
    ) -> list[ScoredEntry]:
        """跨存储混合检索"""
        if stores is None:
            stores = ["knowledge", "errors"]

        all_results: list[ScoredEntry] = []

        if "knowledge" in stores:
            try:
                results = await self.knowledge.hybrid_search(query, top_k=top_k)
                all_results.extend(results)
            except Exception as e:
                logger.warning("Knowledge search failed: %s", e)

        if "errors" in stores:
            try:
                results = await self.errors.search(query, top_k=top_k)
                all_results.extend(results)
            except Exception as e:
                logger.warning("Error search failed: %s", e)

        if "chat" in stores:
            try:
                results = await self.chat.search(query, top_k=top_k)
                all_results.extend(results)
            except Exception as e:
                logger.warning("Chat search failed: %s", e)

        # 去重 + 按分数排序
        seen_ids = set()
        deduped = []
        for entry in all_results:
            if entry.id not in seen_ids:
                seen_ids.add(entry.id)
                deduped.append(entry)

        deduped.sort(key=lambda x: x.score, reverse=True)
        return deduped[:top_k]
