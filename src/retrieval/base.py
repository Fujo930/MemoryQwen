"""
MemoryQwen — BaseRetriever 抽象基类
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.retrieval.models import RetrievalQuery, RetrievalResult


class BaseRetriever(ABC):
    """检索器基类"""

    @abstractmethod
    async def refresh_index(self) -> None:
        """重建索引"""
        ...

    @abstractmethod
    async def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict | None = None,
    ) -> list[RetrievalResult]:
        """检索"""
        ...

    @abstractmethod
    async def search_structured(
        self,
        request: RetrievalQuery,
    ) -> list[RetrievalResult]:
        """结构化检索"""
        ...
