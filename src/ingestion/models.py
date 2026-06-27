"""
MemoryQwen — Ingestion 数据模型
Document / DocumentChunk / IngestionResult / IngestionError
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """解析后的文档"""
    file_path: str
    file_type: str          # "txt" | "md"
    title: str
    content: str
    metadata: dict = field(default_factory=dict)
    char_count: int = 0


@dataclass
class DocumentChunk:
    """文档切片"""
    content: str
    content_hash: str                    # sha256 hexdigest
    chunk_index: int
    total_chunks: int
    metadata: dict = field(default_factory=dict)


@dataclass
class IngestionResult:
    """摄入结果统计"""
    files_seen: int = 0
    files_ingested: int = 0
    files_skipped: int = 0
    chunks_created: int = 0
    chunks_stored: int = 0
    duplicates_skipped: int = 0
    errors: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class IngestionError(Exception):
    """摄入错误"""
    def __init__(self, message: str, file_path: str = ""):
        self.file_path = file_path
        super().__init__(message)
