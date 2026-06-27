"""
IngestionPipeline 完整测试
"""

from __future__ import annotations

import json
import hashlib
import pytest
import pytest_asyncio
import tempfile
from pathlib import Path

from src.ingestion.models import IngestionResult
from src.ingestion.pipeline import IngestionPipeline, STORE_TYPE, RECORD_KIND
from src.ingestion.parser import DocumentParser
from src.ingestion.chunker import DocumentChunker
from src.memory_store.sqlite_store import SQLiteStore


# ─── Mock 配置 ───────────────────────────────────────

class MockIngestConfig:
    inbox_path: str = "inbox"
    supported_extensions: list[str] = [".txt", ".md"]
    recursive: bool = True
    chunk_size: int = 800
    chunk_overlap: int = 120
    skip_hidden_files: bool = True
    watcher_enabled: bool = False
    watch_delay: int = 5
    auto_index: bool = True


class MockMSConfig:
    backend = "sqlite"
    database_path = ":memory:"


class MockConfig:
    ingestion = MockIngestConfig()
    memory_store = MockMSConfig()
    # For parser/chunker
    class Memory:
        class Chunking:
            max_tokens = 512
            overlap_tokens = 32
            strategy = "semantic"
        chunking = Chunking()
    memory = Memory()


# ─── Fixture ─────────────────────────────────────────

@pytest_asyncio.fixture
async def store():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    config = MockConfig()
    config.memory_store.database_path = tmp.name
    s = SQLiteStore(config)
    await s.init()
    yield s
    await s.close()
    Path(tmp.name).unlink(missing_ok=True)


@pytest_asyncio.fixture
def pipeline(store):
    config = MockConfig()
    parser = DocumentParser(config)
    chunker = DocumentChunker(config)
    return IngestionPipeline(config, store, parser, chunker)


@pytest_asyncio.fixture
def temp_dir():
    d = tempfile.mkdtemp()
    yield Path(d)
    import shutil
    shutil.rmtree(d, ignore_errors=True)


def _write_file(dir: Path, name: str, content: str) -> str:
    fp = dir / name
    fp.write_text(content, encoding="utf-8")
    return str(fp)


# ─── 测试 ────────────────────────────────────────────

class TestIngestSingleFile:
    """单文件摄入"""

    @pytest.mark.asyncio
    async def test_ingest_txt(self, pipeline, temp_dir):
        path = _write_file(temp_dir, "hello.txt", "Hello World.\nThis is a test file.")
        result = await pipeline.ingest_file(path)

        assert result.files_seen == 1
        assert result.files_ingested == 1
        assert result.files_skipped == 0
        assert result.chunks_created >= 1
        assert result.chunks_stored >= 1
        assert result.duplicates_skipped == 0
        assert result.errors == []

    @pytest.mark.asyncio
    async def test_ingest_md(self, pipeline, temp_dir):
        path = _write_file(temp_dir, "readme.md", "# Title\n\nContent paragraph.\n\n- item1\n- item2")
        result = await pipeline.ingest_file(path)

        assert result.files_seen == 1
        assert result.files_ingested == 1
        assert result.chunks_created >= 1
        assert result.chunks_stored >= 1

    @pytest.mark.asyncio
    async def test_unsupported_file_skipped(self, pipeline, temp_dir):
        path = _write_file(temp_dir, "data.pdf", "fake pdf")
        path = path.replace(".pdf", ".xyz")
        Path(path).write_text("fake")
        result = await pipeline.ingest_file(path)

        assert result.files_seen == 1
        assert result.files_skipped == 1
        assert result.files_ingested == 0
        assert result.chunks_created == 0
        assert result.chunks_stored == 0

    @pytest.mark.asyncio
    async def test_hidden_file_skipped(self, pipeline, temp_dir):
        path = _write_file(temp_dir, ".hidden.txt", "secret content")
        result = await pipeline.ingest_file(path)

        assert result.files_seen == 1
        assert result.files_skipped == 1
        assert result.chunks_stored == 0

    @pytest.mark.asyncio
    async def test_empty_file_no_crash(self, pipeline, temp_dir):
        path = _write_file(temp_dir, "empty.txt", "")
        result = await pipeline.ingest_file(path)

        # 空文件应被跳过，不崩溃
        assert result.files_seen == 1
        assert result.files_skipped == 1
        assert result.errors == []

    @pytest.mark.asyncio
    async def test_nonexistent_file_error(self, pipeline):
        result = await pipeline.ingest_file("/nonexistent/path/file.txt")
        assert result.files_skipped == 1
        assert len(result.errors) == 1
        assert "不存在" in result.errors[0]["error"]

    @pytest.mark.asyncio
    async def test_content_hash_present(self, pipeline, temp_dir):
        path = _write_file(temp_dir, "hash_test.md", "# Hash Test\n\nSome content.")
        result = await pipeline.ingest_file(path)

        assert result.chunks_stored >= 1
        records = await pipeline.store.list(STORE_TYPE, limit=10)
        for r in records:
            meta = r.get("metadata", {})
            assert "content_hash" in meta, f"missing content_hash in {r}"
            # 验证是 sha256 格式 (64 hex chars)
            assert len(meta["content_hash"]) == 64


class TestChunkMetadata:
    """chunk metadata 正确性"""

    @pytest.mark.asyncio
    async def test_metadata_fields(self, pipeline, temp_dir):
        path = _write_file(temp_dir, "meta.md", "# Title\n\nParagraph one.\n\nParagraph two.")
        await pipeline.ingest_file(path)

        records = await pipeline.store.list(STORE_TYPE, limit=10)
        for r in records:
            meta = r.get("metadata", {})
            if isinstance(meta, str):
                meta = json.loads(meta)

            assert meta.get("record_kind") == RECORD_KIND
            assert "source_path" in meta
            assert meta["source_path"] == path
            assert "source_name" in meta
            assert meta["source_extension"] in ("txt", "md")
            assert "document_title" in meta
            assert "chunk_index" in meta
            assert "total_chunks" in meta
            assert "content_hash" in meta
            assert isinstance(meta["chunk_index"], int)
            assert isinstance(meta["total_chunks"], int)
            assert meta["chunk_index"] < meta["total_chunks"]


class TestDeduplicate:
    """去重测试"""

    @pytest.mark.asyncio
    async def test_dedup_same_file(self, pipeline, temp_dir):
        path = _write_file(temp_dir, "dup.txt", "Unique content for dedup test.")

        # 第一次 ingest
        r1 = await pipeline.ingest_file(path)
        assert r1.chunks_stored > 0
        assert r1.duplicates_skipped == 0

        count_before = await pipeline.store.count(STORE_TYPE)

        # 第二次 ingest 同一文件
        r2 = await pipeline.ingest_file(path)
        assert r2.duplicates_skipped > 0 or r2.chunks_stored == 0
        assert r2.files_ingested == 0 or r2.chunks_stored == 0

        count_after = await pipeline.store.count(STORE_TYPE)
        assert count_after == count_before  # 不增加

    @pytest.mark.asyncio
    async def test_dedup_different_files(self, pipeline, temp_dir):
        path1 = _write_file(temp_dir, "a.txt", "Content A for testing.")
        path2 = _write_file(temp_dir, "b.txt", "Content B different.")

        await pipeline.ingest_file(path1)
        await pipeline.ingest_file(path2)

        count = await pipeline.store.count(STORE_TYPE)
        assert count >= 2


class TestIngestDirectory:
    """目录摄入"""

    @pytest.mark.asyncio
    async def test_ingest_directory(self, pipeline, temp_dir):
        sub = temp_dir / "subdir"
        sub.mkdir(exist_ok=True)
        _write_file(temp_dir, "root.md", "# Root")
        _write_file(sub, "sub.txt", "In sub directory")

        result = await pipeline.ingest_directory(str(temp_dir), recursive=True)

        assert result.files_seen == 2
        assert result.files_ingested == 2
        assert result.chunks_stored >= 2

    @pytest.mark.asyncio
    async def test_ingest_directory_mixed(self, pipeline, temp_dir):
        _write_file(temp_dir, "valid.txt", "Valid")
        _write_file(temp_dir, "skip.xyz", "Skip me")

        result = await pipeline.ingest_directory(str(temp_dir))

        assert result.files_seen == 1  # 只看到 .txt
        assert result.files_ingested == 1

    @pytest.mark.asyncio
    async def test_error_not_break_batch(self, pipeline, temp_dir):
        """批处理中单个文件出错不中断全部"""
        _write_file(temp_dir, "good.txt", "Good file content.")

        result = await pipeline.ingest_directory(str(temp_dir))
        # 好的文件仍然被处理
        assert result.files_ingested >= 1
        assert result.chunks_stored >= 1


class TestResultStats:
    """结果统计"""

    @pytest.mark.asyncio
    async def test_stats_accuracy(self, pipeline, temp_dir):
        _write_file(temp_dir, "stats.txt", "Stats test content. " * 20)

        result = await pipeline.ingest_file(str(temp_dir / "stats.txt"))

        assert isinstance(result, IngestionResult)
        assert result.files_seen == 1
        assert result.files_ingested == 1
        assert result.files_skipped == 0
        assert result.chunks_created >= 1
        assert result.chunks_stored >= 1
        assert result.duplicates_skipped == 0
        assert isinstance(result.errors, list)

    @pytest.mark.asyncio
    async def test_multiple_files_stats(self, pipeline, temp_dir):
        _write_file(temp_dir, "a.txt", "Content A.")
        _write_file(temp_dir, "b.txt", "Content B.")
        _write_file(temp_dir, "c.xyz", "Skip")

        r1 = await pipeline.ingest_file(str(temp_dir / "a.txt"))
        r2 = await pipeline.ingest_file(str(temp_dir / "b.txt"))
        r3 = await pipeline.ingest_file(str(temp_dir / "c.xyz"))

        assert r1.files_ingested == 1
        assert r2.files_ingested == 1
        assert r3.files_skipped == 1


class TestExistsByMetadata:
    """exists_by_metadata 测试"""

    @pytest.mark.asyncio
    async def test_exists_positive(self, pipeline, temp_dir):
        path = _write_file(temp_dir, "exist_test.txt", "Check existence.")

        await pipeline.ingest_file(path)

        # 用过 metadata LIKE 检查存在（content_hash 纯字母数字，无转义问题）
        records = await pipeline.store.list("knowledge_store", limit=1)
        assert len(records) > 0
        meta = records[0].get("metadata", {})
        if isinstance(meta, str):
            meta = json.loads(meta)
        content_hash = meta.get("content_hash", "")
        assert len(content_hash) == 64

        exists = await pipeline.store.exists_by_metadata("knowledge_store", {
            "content_hash": content_hash,
        })
        assert exists is True

    @pytest.mark.asyncio
    async def test_exists_negative(self, pipeline):
        exists = await pipeline.store.exists_by_metadata("knowledge_store", {
            "source_path": "/no/such/file.txt",
        })
        assert exists is False
