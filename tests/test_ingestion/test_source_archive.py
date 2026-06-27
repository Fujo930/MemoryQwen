"""
Source Archive 测试 (≥10)
"""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

import pytest
import pytest_asyncio

from src.config import load_config
from src.ingestion.models import IngestionResult
from src.ingestion.pipeline import IngestionPipeline
from src.ingestion.parser import DocumentParser
from src.ingestion.chunker import DocumentChunker


@pytest_asyncio.fixture
async def pipeline_and_temp():
    """创建带有临时目录和独立数据库的 pipeline"""
    config = load_config()
    config.ingestion.archive_sources = True
    config.ingestion.source_archive_dir = str(Path(tempfile.mkdtemp()) / "memory/sources")
    inbox = Path(tempfile.mkdtemp())
    config.ingestion.inbox_path = str(inbox)
    # 使用独立临时数据库，避免污染真实 memory
    db_path = str(Path(tempfile.mkdtemp()) / "test.db")
    config.memory_store.database_path = db_path

    from src.memory_store.factory import create_memory_store
    store = create_memory_store(config)
    try:
        await store.init()
    except Exception:
        pass

    pipeline = IngestionPipeline(config, store, DocumentParser(config), DocumentChunker(config))
    yield pipeline, inbox, config
    await store.close()


def _write_file(parent: Path, name: str, content: str) -> Path:
    fp = parent / name
    fp.write_text(content, encoding="utf-8")
    return fp


class TestSourceArchive:
    @pytest.mark.asyncio
    async def test_archive_source_file_on_ingest(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        fp = _write_file(inbox, "test.md", "# Test\ncontent")
        result = await pipeline.ingest_file(str(fp))
        assert result.files_ingested == 1
        # 检查归档文件是否存在
        archive_dir = Path(config.ingestion.source_archive_dir)
        archived_files = list(archive_dir.rglob("test.md"))
        assert len(archived_files) >= 1

    @pytest.mark.asyncio
    async def test_archive_preserves_relative_path(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        sub = inbox / "subdir"
        sub.mkdir(exist_ok=True)
        fp = _write_file(sub, "nested.md", "# Nested")
        result = await pipeline.ingest_file(str(fp))
        assert result.files_ingested == 1
        archive_dir = Path(config.ingestion.source_archive_dir)
        nested = list(archive_dir.rglob("nested.md"))
        assert len(nested) >= 1
        assert "subdir" in str(nested[0])

    @pytest.mark.asyncio
    async def test_archive_path_written_to_metadata(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        fp = _write_file(inbox, "meta.md", "# Meta test")
        await pipeline.ingest_file(str(fp))
        # Get first chunk from store
        store = pipeline.store
        results = await store.search_keyword("knowledge_store", "Meta", limit=1)
        assert len(results) > 0
        meta = results[0].get("metadata", {})
        if isinstance(meta, str):
            import json; meta = json.loads(meta)
        assert "archive_path" in meta
        assert meta.get("archived") is True

    @pytest.mark.asyncio
    async def test_source_hash_written_to_metadata(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        fp = _write_file(inbox, "hash.md", "# Hash test\nunique content here")
        await pipeline.ingest_file(str(fp))
        store = pipeline.store
        results = await store.search_keyword("knowledge_store", "Hash test", limit=1)
        assert len(results) > 0
        meta = results[0].get("metadata", {})
        if isinstance(meta, str):
            import json; meta = json.loads(meta)
        assert "source_hash" in meta
        # source_hash is a 64-char hex string
        assert len(meta["source_hash"]) == 64

    @pytest.mark.asyncio
    async def test_archive_duplicate_same_hash_not_copied_twice(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        fp = _write_file(inbox, "dup.md", "# Duplicate")
        await pipeline.ingest_file(str(fp))
        await pipeline.ingest_file(str(fp))  # second ingest
        archive_dir = Path(config.ingestion.source_archive_dir)
        # 应该只有一个文件（第二次不重复复制）
        archived = list(archive_dir.rglob("dup.md"))
        assert len(archived) == 1

    @pytest.mark.asyncio
    async def test_archive_filename_conflict_different_hash(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        fp = _write_file(inbox, "conflict.md", "# Version A")
        await pipeline.ingest_file(str(fp))
        # 修改文件内容
        fp.write_text("# Version B - different content")
        await pipeline.ingest_file(str(fp))
        archive_dir = Path(config.ingestion.source_archive_dir)
        archived = list(archive_dir.rglob("conflict*"))
        # 应该有两个文件（第二个加 hash 后缀）
        assert len(archived) >= 2

    @pytest.mark.asyncio
    async def test_archive_disabled(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        config.ingestion.archive_sources = False
        fp = _write_file(inbox, "noarchive.md", "# No archive")
        await pipeline.ingest_file(str(fp))
        archive_dir = Path(config.ingestion.source_archive_dir)
        archived = list(archive_dir.rglob("noarchive.md"))
        assert len(archived) == 0

    @pytest.mark.asyncio
    async def test_ingest_result_metadata_has_archived(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        fp = _write_file(inbox, "meta_out.md", "# Meta output")
        result = await pipeline.ingest_file(str(fp))
        assert result.metadata.get("archived_sources", 0) >= 0

    @pytest.mark.asyncio
    async def test_directory_ingest_archives(self, pipeline_and_temp):
        pipeline, inbox, config = pipeline_and_temp
        _write_file(inbox, "a.md", "# A")
        _write_file(inbox, "b.md", "# B")
        result = await pipeline.ingest_directory(str(inbox))
        assert result.metadata.get("archived_sources", 0) >= 2
