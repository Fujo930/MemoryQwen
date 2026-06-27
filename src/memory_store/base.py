"""
MemoryQwen — MemoryStore 抽象基类
定义统一的记忆存储接口，不绑定具体数据库。
"""

from __future__ import annotations

from abc import ABC, abstractmethod

TABLE_NAMES = (
    "knowledge_store",
    "knowledge_chunks",
    "chat_messages",
    "error_store",
    "error_experiences",
    "strategy_store",
    "strategies",
    "examples",
)


class MemoryStore(ABC):
    """记忆存储基类"""

    @abstractmethod
    async def init(self) -> None:
        """初始化存储（建表、migration）"""
        ...

    @abstractmethod
    async def add(self, table: str, record: dict) -> str:
        """添加记录，返回 record_id"""
        ...

    @abstractmethod
    async def get(self, table: str, record_id: str) -> dict | None:
        """获取单条记录"""
        ...

    @abstractmethod
    async def update(self, table: str, record_id: str, patch: dict) -> bool:
        """更新记录，返回是否成功"""
        ...

    @abstractmethod
    async def delete(self, table: str, record_id: str) -> bool:
        """删除记录，返回是否成功"""
        ...

    @abstractmethod
    async def list(
        self, table: str, limit: int = 20, offset: int = 0
    ) -> list[dict]:
        """分页列出记录"""
        ...

    @abstractmethod
    async def search_keyword(
        self, table: str, query: str, limit: int = 10
    ) -> list[dict]:
        """关键词搜索"""
        ...

    @abstractmethod
    async def count(self, table: str) -> int:
        """记录总数"""
        ...

    @abstractmethod
    async def close(self) -> None:
        """关闭连接"""
        ...

    @abstractmethod
    async def exists_by_metadata(
        self, store_type: str, filters: dict[str, str]
    ) -> bool:
        """通过 metadata 字段值检查记录是否存在（用于去重）"""
        ...

    @abstractmethod
    async def list_by_metadata(
        self,
        store_type: str,
        filters: dict[str, str],
        limit: int = 100,
        order_by: str = "created_at",
        descending: bool = False,
    ) -> list[dict]:
        """按 metadata 过滤并排序列出的记录"""
        ...
