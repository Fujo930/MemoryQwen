"""
KeywordRetriever 测试
"""

from __future__ import annotations

import json
import pytest
import pytest_asyncio
import tempfile
from pathlib import Path

from src.retrieval.keyword import KeywordRetriever
from src.retrieval.models import RetrievalQuery, RetrievalResult
from src.memory_store.sqlite_store import SQLiteStore
KNOWLEDGE_STORE = "knowledge_store"
DOCUMENT_CHUNK = "document_chunk"


# ─── Mock 配置 ───────────────────────────────────────

class MockKWConfig:
    enabled: bool = True
    default_top_k: int = 5
    min_score: float = 0.0
    tokenizer: str = "simple"


class MockConfig:
    class Memory:
        retrieval_keyword = MockKWConfig()
        class Retrieval:
            top_k = 5
        retrieval = Retrieval()
    memory = Memory()
    memory_store = type('obj', (), {'database_path': ':memory:'})()


# ─── Fixtures ─────────────────────────────────────────

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
async def retriever(store):
    r = KeywordRetriever(MockConfig(), store)
    return r


async def _add_chunk(store, title, content, **extra_meta):
    """添加一条 document_chunk 记录"""
    meta = {
        "record_kind": DOCUMENT_CHUNK,
        "source_path": extra_meta.pop("source_path", "/docs/test.md"),
        "source_name": "test.md",
        "source_extension": extra_meta.pop("source_extension", "md"),
        "document_title": title,
        "chunk_index": extra_meta.pop("chunk_index", 0),
        "total_chunks": extra_meta.pop("total_chunks", 1),
        "content_hash": extra_meta.pop("content_hash", "abc123"),
    }
    meta.update(extra_meta)
    await store.add(KNOWLEDGE_STORE, {
        "source_path": meta["source_path"],
        "title": title,
        "content": content,
        "metadata": meta,
    })


# ─── 检索测试 ────────────────────────────────────────

class TestSearchEnglish:
    @pytest.mark.asyncio
    async def test_english_hit(self, retriever, store):
        await _add_chunk(store, "Python Guide", "Python is a programming language for data science.")
        await retriever.refresh_index()

        results = await retriever.search("Python programming")
        assert len(results) > 0
        assert "Python" in results[0].content

    @pytest.mark.asyncio
    async def test_case_insensitive(self, retriever, store):
        await _add_chunk(store, "Test", "Hello World data Science")
        await retriever.refresh_index()

        results = await retriever.search("HELLO SCIENCE")
        assert len(results) > 0


class TestSearchChinese:
    @pytest.mark.asyncio
    async def test_chinese_hit(self, retriever, store):
        await _add_chunk(store, "Python 介绍", "Python 是一种编程语言，广泛用于数据分析。")
        await retriever.refresh_index()

        results = await retriever.search("编程语言")
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_chinese_bigram_match(self, retriever, store):
        await _add_chunk(store, "深度学习", "深度学习是机器学习的一个分支。")
        await retriever.refresh_index()

        results = await retriever.search("深度")
        assert len(results) > 0


class TestSearchResults:
    @pytest.mark.asyncio
    async def test_score_descending(self, retriever, store):
        await _add_chunk(store, "A", "machine learning deep learning neural network")
        await _add_chunk(store, "B", "python for machine learning beginners")
        await retriever.refresh_index()

        results = await retriever.search("deep learning machine")
        assert len(results) >= 2
        for i in range(len(results) - 1):
            assert results[i].score >= results[i + 1].score

    @pytest.mark.asyncio
    async def test_top_k(self, retriever, store):
        for i in range(10):
            await _add_chunk(store, f"Chunk {i}", f"test data content {i}")
        await retriever.refresh_index()

        results = await retriever.search("test", top_k=3)
        assert len(results) <= 3

    @pytest.mark.asyncio
    async def test_empty_query(self, retriever, store):
        await _add_chunk(store, "X", "some content")
        await retriever.refresh_index()

        results = await retriever.search("")
        assert results == []

    @pytest.mark.asyncio
    async def test_no_match(self, retriever, store):
        await _add_chunk(store, "Y", "abcdef ghi jkl")
        await retriever.refresh_index()

        results = await retriever.search("xyzunknown")
        assert results == []

    @pytest.mark.asyncio
    async def test_result_fields(self, retriever, store):
        await _add_chunk(store, "Field Test", "content for result fields", source_path="/a/b.md", chunk_index=2, total_chunks=5)
        await retriever.refresh_index()

        results = await retriever.search("content")
        assert len(results) > 0
        r = results[0]
        assert isinstance(r, RetrievalResult)
        assert r.record_id != ""
        assert r.store_type == KNOWLEDGE_STORE
        assert r.source_path == "/a/b.md"
        assert r.chunk_index == 2
        assert r.total_chunks == 5
        assert r.score > 0

    @pytest.mark.asyncio
    async def test_filter_by_source_extension(self, retriever, store):
        await _add_chunk(store, "MD", "content one", source_extension="md")
        await _add_chunk(store, "TXT", "content two", source_extension="txt")
        await retriever.refresh_index()

        results = await retriever.search("content", filters={"source_extension": "md"})
        assert len(results) > 0
        for r in results:
            assert r.metadata.get("source_extension") == "md"

    @pytest.mark.asyncio
    async def test_only_document_chunks(self, retriever, store):
        # 添加 document_chunk
        await _add_chunk(store, "Doc", "relevant content")
        # 添加 non-document_chunk (不同 record_kind)
        await store.add(KNOWLEDGE_STORE, {
            "source_path": "/x",
            "title": "Not Doc",
            "content": "irrelevant content",
            "metadata": {"record_kind": "other_kind"},
        })
        await retriever.refresh_index()

        results = await retriever.search("content")
        # 只返回 record_kind=document_chunk 的
        for r in results:
            assert r.metadata.get("record_kind") == DOCUMENT_CHUNK

    @pytest.mark.asyncio
    async def test_refresh_index(self, retriever, store):
        await retriever.refresh_index()

        # 初始索引为空
        results = await retriever.search("test")
        assert results == []

        # 添加数据后 refresh
        await _add_chunk(store, "New", "new test content here")
        await retriever.refresh_index()

        results = await retriever.search("test content")
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_search_structured(self, retriever, store):
        await _add_chunk(store, "S", "structured search test")
        await retriever.refresh_index()

        req = RetrievalQuery(query="structured", top_k=2)
        results = await retriever.search_structured(req)
        assert len(results) <= 2

    @pytest.mark.asyncio
    async def test_min_score_filter(self, retriever, store):
        """min_score > 0 时过滤低分结果"""
        # 设置较高 min_score
        retriever.config.memory.retrieval_keyword.min_score = 99.0
        await _add_chunk(store, "Low", "barely matching")
        await retriever.refresh_index()

        results = await retriever.search("barely")
        assert results == []
