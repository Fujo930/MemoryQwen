"""
MemoryQwen — Retrieval 数据模型
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RetrievalQuery:
    """检索请求"""
    query: str
    store_types: list[str] = field(default_factory=lambda: ["knowledge_store"])
    top_k: int = 5
    filters: dict | None = None


@dataclass
class RetrievalResult:
    """检索结果"""
    record_id: str = ""
    store_type: str = ""
    title: str = ""
    content: str = ""
    metadata: dict = field(default_factory=dict)
    score: float = 0.0
    source_path: str = ""
    chunk_index: int = 0
    total_chunks: int = 0
