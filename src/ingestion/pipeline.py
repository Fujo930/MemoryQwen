"""
MemoryQwen — IngestionPipeline
文档摄入管道：parse → chunk → store (去重) → archive
"""

from __future__ import annotations

import hashlib
import logging
import shutil
from pathlib import Path
from typing import Any

from src.ingestion.models import Document, DocumentChunk, IngestionResult, IngestionError
from src.ingestion.parser import DocumentParser
from src.ingestion.chunker import DocumentChunker

logger = logging.getLogger(__name__)

STORE_TYPE = "knowledge_store"
RECORD_KIND = "document_chunk"


class IngestionPipeline:
    """文档摄入管道"""

    def __init__(self, config: Any, store, parser=None, chunker=None):
        self.config = config
        self.store = store
        self._parser = parser or DocumentParser(config)
        self._chunker = chunker or DocumentChunker(config)

    async def ingest_file(self, file_path: str) -> IngestionResult:
        """摄入单个文件"""
        result = IngestionResult(files_seen=1)

        path = Path(file_path)

        if not path.exists():
            result.errors.append({"file": file_path, "error": f"文件不存在: {file_path}"})
            result.files_skipped = 1
            return result

        ext = path.suffix.lower()
        if ext not in self.config.ingestion.supported_extensions:
            result.files_skipped = 1
            return result

        if self.config.ingestion.skip_hidden_files and path.name.startswith("."):
            result.files_skipped = 1
            return result

        if path.stat().st_size == 0:
            logger.info("Skipping empty file: %s", file_path)
            result.files_skipped = 1
            return result

        try:
            document = await self._parser.parse(file_path)
            if not document.content.strip():
                logger.info("Skipping file with empty content: %s", file_path)
                result.files_skipped = 1
                return result

            # 计算来源文件 hash
            source_hash = self._compute_source_hash(file_path)

            # 归档原文件
            archive_path = await self._archive_source(file_path, source_hash)

            # 切片
            chunks = self._chunker.chunk(document)
            chunk_results = await self._store_chunks(document, chunks, source_hash, archive_path)
            result.chunks_created = len(chunks)
            result.chunks_stored = chunk_results["stored"]
            result.duplicates_skipped = chunk_results["duplicates"]
            result.files_ingested = 1 if chunk_results["stored"] > 0 else 0

            if archive_path:
                result.metadata["archived_sources"] = result.metadata.get("archived_sources", 0) + 1

        except Exception as e:
            logger.error("Ingest failed for %s: %s", file_path, e)
            result.errors.append({"file": file_path, "error": str(e)})
            result.files_skipped = 1

        return result

    async def ingest_directory(self, directory: str, recursive: bool | None = None) -> IngestionResult:
        if recursive is None:
            recursive = self.config.ingestion.recursive

        path = Path(directory)
        if not path.exists():
            return IngestionResult(files_seen=0)

        supported_exts = self.config.ingestion.supported_extensions
        skip_hidden = self.config.ingestion.skip_hidden_files

        file_paths = []
        glob_pattern = "**/*" if recursive else "*"
        for ext in supported_exts:
            for f in path.glob(f"{glob_pattern}{ext}"):
                if skip_hidden and f.name.startswith("."):
                    continue
                file_paths.append(str(f))

        file_paths = list(set(file_paths))
        file_paths.sort()

        total = IngestionResult(files_seen=len(file_paths))
        archived_count = 0

        for fp in file_paths:
            file_result = await self.ingest_file(fp)
            total.files_ingested += file_result.files_ingested
            total.files_skipped += file_result.files_skipped
            total.chunks_created += file_result.chunks_created
            total.chunks_stored += file_result.chunks_stored
            total.duplicates_skipped += file_result.duplicates_skipped
            total.errors.extend(file_result.errors)
            archived_count += file_result.metadata.get("archived_sources", 0)

        total.metadata["archived_sources"] = archived_count

        return total

    # ─── 内部 ──────────────────────────────────────────

    def _compute_source_hash(self, file_path: str) -> str:
        """计算整个文件的 sha256"""
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    async def _archive_source(self, file_path: str, source_hash: str) -> str:
        """归档原始文件到 memory/sources/。返回归档路径或空字符串"""
        cfg = getattr(self.config.ingestion, "archive_sources", False)
        if not cfg:
            return ""

        archive_dir = getattr(self.config.ingestion, "source_archive_dir", "memory/sources")
        src_path = Path(file_path)
        archive_root = Path(archive_dir)

        # 保留相对目录结构（从 inbox 到 archive）
        # 例如 inbox/training/01.md → memory/sources/training/01.md
        try:
            rel = src_path.relative_to(Path(self.config.ingestion.inbox_path))
            dest_parent = archive_root / rel.parent
            dest_name = rel.name
        except ValueError:
            # 不在 inbox 下，直接扁平归档
            dest_parent = archive_root
            dest_name = src_path.name

        dest_parent.mkdir(parents=True, exist_ok=True)
        dest = dest_parent / dest_name

        # 如果目标已存在且 hash 相同 → 不重复复制
        if dest.exists():
            existing_hash = self._compute_source_hash(str(dest))
            if existing_hash == source_hash:
                logger.debug("Source already archived (same hash): %s", dest)
                return str(dest)
            # hash 不同 → 加短 hash 后缀
            short = source_hash[:8]
            stem = dest.stem
            dest = dest_parent / f"{stem}__{short}{dest.suffix}"

        try:
            shutil.copy2(file_path, str(dest))
            logger.info("Archived: %s -> %s", file_path, dest)
            return str(dest)
        except Exception as e:
            logger.warning("Archive failed for %s: %s", file_path, e)
            return ""

    async def _store_chunks(self, document: Document, chunks: list, source_hash: str, archive_path: str) -> dict:
        stored = 0
        duplicates = 0
        total = len(chunks)

        for i, chunk in enumerate(chunks):
            content = chunk.content
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

            exists = await self._chunk_exists(document.file_path, content_hash)
            if exists:
                duplicates += 1
                continue

            metadata = {
                "record_kind": RECORD_KIND,
                "source_path": document.file_path,
                "source_name": Path(document.file_path).name,
                "source_extension": document.file_type,
                "document_title": document.title,
                "chunk_index": i,
                "total_chunks": total,
                "content_hash": content_hash,
                "source_hash": source_hash,
                "archive_path": archive_path,
                "archived": bool(archive_path),
                "ingest_time": "",
            }

            await self.store.add(STORE_TYPE, {
                "source_path": document.file_path,
                "title": f"{document.title}#chunk-{i}#{content_hash}",
                "content": content,
                "metadata": metadata,
            })
            stored += 1

        return {"stored": stored, "duplicates": duplicates}

    async def _chunk_exists(self, source_path: str, content_hash: str) -> bool:
        try:
            exists = await self.store.exists_by_metadata(STORE_TYPE, {
                "content_hash": content_hash,
            })
            return exists
        except Exception:
            return False
