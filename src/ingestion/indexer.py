"""
MemoryQwen — Indexer 索引 Pipeline
将 parse → chunk → embed → store 串联为完整 pipeline
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.ingestion.parser import DocumentParser, Document
from src.ingestion.chunker import DocumentChunker, Chunk
from src.memory_bus.knowledge_store import KnowledgeStore

logger = logging.getLogger(__name__)


@dataclass
class IndexResult:
    """索引结果"""
    doc_id: str
    file_path: str
    chunks_count: int
    total_tokens: int
    success: bool
    error: str | None = None


class Indexer:
    """索引 Pipeline：解析 → 切片 → 向量化 → 存储"""

    def __init__(
        self,
        parser: DocumentParser,
        chunker: DocumentChunker,
        knowledge_store: KnowledgeStore,
    ):
        self.parser = parser
        self.chunker = chunker
        self.knowledge_store = knowledge_store

    async def index_file(self, file_path: str) -> IndexResult:
        """索引单个文件"""
        path = Path(file_path)
        try:
            logger.info("Indexing: %s", file_path)

            # 1. 解析
            document = await self.parser.parse(file_path)

            # 2. 切片
            chunks = self.chunker.chunk(document)

            # 3. 构建 chunks 数据
            chunk_data = []
            for chunk in chunks:
                chunk_data.append({
                    "content": chunk.content,
                    "metadata": chunk.metadata,
                    "id": f"{document.file_path}#chunk-{chunk.chunk_index}",
                })

            # 4. 索引（embed + store）
            chunk_ids = await self.knowledge_store.add_chunks(chunk_data)

            # 5. 移动文件到已处理区域（可选）
            # processed_dir = Path(self.knowledge_store.config.ingestion.inbox_dir) / ".processed"
            # processed_dir.mkdir(exist_ok=True)

            total_tokens = sum(c.token_count for c in chunks)
            logger.info("Indexed %d chunks (%d tokens) from %s",
                        len(chunks), total_tokens, file_path)

            return IndexResult(
                doc_id=document.file_path,
                file_path=file_path,
                chunks_count=len(chunks),
                total_tokens=total_tokens,
                success=True,
            )

        except Exception as e:
            logger.error("Index failed for %s: %s", file_path, e)
            return IndexResult(
                doc_id=file_path,
                file_path=file_path,
                chunks_count=0,
                total_tokens=0,
                success=False,
                error=str(e),
            )

    async def index_files(self, file_paths: list[str]) -> list[IndexResult]:
        """批量索引文件"""
        results = []
        for fp in file_paths:
            result = await self.index_file(fp)
            results.append(result)
        return results

    async def remove_document(self, doc_id: str) -> bool:
        """从知识库移除文档"""
        return await self.knowledge_store.delete(doc_id)

    async def index_inbox(self, inbox_dir: str) -> list[IndexResult]:
        """索引 inbox 目录中所有支持的文件"""
        from src.ingestion.parser import UnsupportedFormatError

        inbox = Path(inbox_dir)
        if not inbox.exists():
            logger.warning("Inbox directory not found: %s", inbox_dir)
            return []

        file_paths = []
        for ext in self.parser.supported_extensions():
            for f in inbox.rglob(f"*{ext}"):
                if ".processed" not in str(f):
                    file_paths.append(str(f))

        logger.info("Found %d files in inbox", len(file_paths))
        return await self.index_files(file_paths)
