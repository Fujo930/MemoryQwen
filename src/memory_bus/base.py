"""
MemoryQwen — MemoryBus 基类
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryEntry:
    """记忆条目基类"""
    id: str = ""
    content: str = ""
    metadata: dict = field(default_factory=dict)
    score: float = 0.0


@dataclass
class ScoredEntry(MemoryEntry):
    """带分值的检索结果"""
    pass


class BaseMemoryStore(ABC):
    """记忆存储基类"""

    def __init__(self, config: Any):
        self.config = config

    @abstractmethod
    async def add(self, entry: MemoryEntry) -> str:
        """添加记忆条目，返回 ID"""
        ...

    @abstractmethod
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[ScoredEntry]:
        """检索相关记忆"""
        ...

    @abstractmethod
    async def delete(self, entry_id: str) -> bool:
        """删除记忆"""
        ...

    @abstractmethod
    async def update(self, entry: MemoryEntry) -> bool:
        """更新记忆"""
        ...

    @abstractmethod
    async def count(self) -> int:
        """条目总数"""
        ...
