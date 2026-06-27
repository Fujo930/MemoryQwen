"""
SQLiteStore 完整测试
CRUD / 搜索 / 重复初始化 / JSON round-trip / 5 种 store type
"""

from __future__ import annotations

import json
import pytest
import pytest_asyncio
import tempfile
from pathlib import Path

from src.memory_store.sqlite_store import SQLiteStore
from src.memory_store.base import TABLE_NAMES


# ─── Mock 配置 ────────────────────────────────────────

class MockConfig:
    class MemoryStore:
        backend = "sqlite"
        database_path = ":memory:"  # 默认内存，各测试可覆盖
    memory_store = MemoryStore()


# ─── Fixture ──────────────────────────────────────────

@pytest_asyncio.fixture
async def store():
    """创建使用临时文件的 store"""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    config = MockConfig()
    config.memory_store.database_path = tmp.name
    s = SQLiteStore(config)
    await s.init()
    yield s
    await s.close()
    Path(tmp.name).unlink(missing_ok=True)


# ─── 基础 CRUD ────────────────────────────────────────

class TestAdd:
    """add 测试"""

    @pytest.mark.asyncio
    async def test_add_knowledge(self, store):
        rid = await store.add("knowledge_chunks", {
            "source_path": "/docs/readme.md",
            "title": "README",
            "content": "# 项目介绍\n内容是...",
            "metadata": {"author": "test", "version": 1},
        })
        assert rid is not None
        record = await store.get("knowledge_chunks", rid)
        assert record["title"] == "README"
        assert record["source_path"] == "/docs/readme.md"
        assert "内容是" in record["content"]
        assert record["metadata"]["author"] == "test"
        assert record["metadata"]["version"] == 1

    @pytest.mark.asyncio
    async def test_add_chat(self, store):
        rid = await store.add("chat_messages", {
            "session_id": "sess-001",
            "role": "user",
            "content": "你好，请问 Python 是什么？",
            "metadata": {"client": "web"},
        })
        assert rid is not None
        record = await store.get("chat_messages", rid)
        assert record["session_id"] == "sess-001"
        assert record["role"] == "user"
        assert "Python" in record["content"]
        assert record["metadata"]["client"] == "web"

    @pytest.mark.asyncio
    async def test_add_error(self, store):
        rid = await store.add("error_experiences", {
            "task": "计算 1+1",
            "wrong_answer": "3",
            "correct_answer": "2",
            "failure_type": "math_error",
            "strategy": "使用计算器验证",
            "metadata": {"severity": "low"},
        })
        assert rid is not None
        record = await store.get("error_experiences", rid)
        assert record["task"] == "计算 1+1"
        assert record["wrong_answer"] == "3"
        assert record["correct_answer"] == "2"
        assert record["failure_type"] == "math_error"
        assert record["strategy"] == "使用计算器验证"

    @pytest.mark.asyncio
    async def test_add_strategy(self, store):
        rid = await store.add("strategies", {
            "title": "数学问题验证策略",
            "content": "遇到数学问题时，先写 Python 代码验证",
            "tags": ["math", "verification", "python"],
            "success_count": 5,
        })
        assert rid is not None
        record = await store.get("strategies", rid)
        assert record["title"] == "数学问题验证策略"
        assert "Python 代码验证" in record["content"]
        assert "math" in record["tags"]

    @pytest.mark.asyncio
    async def test_add_example(self, store):
        rid = await store.add("examples", {
            "task": "生成 Fibonacci 数列",
            "answer": "def fib(n): return ...",
            "reasoning_pattern": "递归+记忆化",
            "tags": ["code", "recursion"],
            "metadata": {"language": "python"},
        })
        assert rid is not None
        record = await store.get("examples", rid)
        assert record["task"] == "生成 Fibonacci 数列"
        assert "def fib" in record["answer"]
        assert record["reasoning_pattern"] == "递归+记忆化"

    @pytest.mark.asyncio
    async def test_add_with_custom_id(self, store):
        rid = await store.add("knowledge_chunks", {
            "id": "custom-id-001",
            "source_path": "/x.txt",
            "title": "X",
            "content": "xxx",
        })
        assert rid == "custom-id-001"

    @pytest.mark.asyncio
    async def test_add_invalid_table(self, store):
        with pytest.raises(ValueError, match="Unknown table"):
            await store.add("nonexistent_table", {"content": "x"})


class TestGet:
    """get 测试"""

    @pytest.mark.asyncio
    async def test_get_by_id(self, store):
        rid = await store.add("knowledge_chunks", {
            "source_path": "/a.md", "title": "A", "content": "body",
        })
        record = await store.get("knowledge_chunks", rid)
        assert record["id"] == rid
        assert record["title"] == "A"

    @pytest.mark.asyncio
    async def test_get_nonexistent(self, store):
        record = await store.get("knowledge_chunks", "no-such-id")
        assert record is None


class TestUpdate:
    """update 测试"""

    @pytest.mark.asyncio
    async def test_update_content(self, store):
        rid = await store.add("knowledge_chunks", {
            "source_path": "/b.md", "title": "B", "content": "old",
        })
        ok = await store.update("knowledge_chunks", rid, {"content": "new content"})
        assert ok is True
        record = await store.get("knowledge_chunks", rid)
        assert record["content"] == "new content"

    @pytest.mark.asyncio
    async def test_update_metadata(self, store):
        rid = await store.add("error_experiences", {
            "task": "test", "wrong_answer": "w", "correct_answer": "c",
            "metadata": {"severity": "low"},
        })
        ok = await store.update("error_experiences", rid, {
            "metadata": {"severity": "critical", "reviewed": True},
        })
        assert ok is True
        record = await store.get("error_experiences", rid)
        assert record["metadata"]["severity"] == "critical"
        assert record["metadata"]["reviewed"] is True

    @pytest.mark.asyncio
    async def test_update_nonexistent(self, store):
        ok = await store.update("knowledge_chunks", "no-id", {"content": "x"})
        assert ok is False


class TestDelete:
    """delete 测试"""

    @pytest.mark.asyncio
    async def test_delete_removes_record(self, store):
        rid = await store.add("knowledge_chunks", {
            "source_path": "/d.md", "title": "D", "content": "del",
        })
        before = await store.count("knowledge_chunks")
        ok = await store.delete("knowledge_chunks", rid)
        assert ok is True
        after = await store.count("knowledge_chunks")
        assert after == before - 1
        assert await store.get("knowledge_chunks", rid) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, store):
        ok = await store.delete("knowledge_chunks", "no-id")
        assert ok is False


class TestList:
    """list 测试"""

    @pytest.mark.asyncio
    async def test_list_default(self, store):
        for i in range(5):
            await store.add("knowledge_chunks", {
                "source_path": f"/d{i}.md", "title": f"D{i}", "content": f"body{i}",
            })
        records = await store.list("knowledge_chunks")
        assert len(records) == 5

    @pytest.mark.asyncio
    async def test_list_pagination(self, store):
        for i in range(10):
            await store.add("knowledge_chunks", {
                "source_path": f"/e{i}.md", "title": f"E{i}", "content": f"body{i}",
            })
        page1 = await store.list("knowledge_chunks", limit=3, offset=0)
        page2 = await store.list("knowledge_chunks", limit=3, offset=3)
        assert len(page1) == 3
        assert len(page2) == 3
        assert page1[0]["id"] != page2[0]["id"]


class TestCount:
    """count 测试"""

    @pytest.mark.asyncio
    async def test_count_zero(self, store):
        assert await store.count("strategies") == 0

    @pytest.mark.asyncio
    async def test_count_increments(self, store):
        await store.add("strategies", {"title": "S1", "content": "c1"})
        await store.add("strategies", {"title": "S2", "content": "c2"})
        assert await store.count("strategies") == 2


class TestSearch:
    """关键词搜索测试"""

    @pytest.mark.asyncio
    async def test_search_by_title(self, store):
        await store.add("knowledge_chunks", {
            "source_path": "/a.md", "title": "Python 入门指南", "content": "Python 是...",
        })
        await store.add("knowledge_chunks", {
            "source_path": "/b.md", "title": "Java 入门", "content": "Java 是...",
        })
        results = await store.search_keyword("knowledge_chunks", "Python")
        assert len(results) >= 1
        assert any("Python" in r["title"] for r in results)

    @pytest.mark.asyncio
    async def test_search_by_content(self, store):
        await store.add("knowledge_chunks", {
            "source_path": "/x.md", "title": "测试", "content": "关于异步编程 asyncio 的内容",
        })
        results = await store.search_keyword("knowledge_chunks", "asyncio")
        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_search_no_match(self, store):
        await store.add("knowledge_chunks", {
            "source_path": "/z.md", "title": "Z", "content": "abc",
        })
        results = await store.search_keyword("knowledge_chunks", "不存在的关键词 xyz123")
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_search_error_by_task(self, store):
        await store.add("error_experiences", {
            "task": "递归溢出问题",
            "wrong_answer": "...",
            "correct_answer": "...",
            "failure_type": "recursion",
        })
        results = await store.search_keyword("error_experiences", "递归")
        assert len(results) >= 1
        assert "递归" in results[0]["task"]


class TestMetadataRoundtrip:
    """JSON metadata round-trip"""

    @pytest.mark.asyncio
    async def test_metadata_roundtrip(self, store):
        meta = {"nested": {"key": "value"}, "list": [1, 2, 3], "bool": True}
        rid = await store.add("knowledge_chunks", {
            "source_path": "/meta.md",
            "title": "Meta Test",
            "content": "test",
            "metadata": meta,
        })
        record = await store.get("knowledge_chunks", rid)
        assert record["metadata"] == meta

    @pytest.mark.asyncio
    async def test_tags_roundtrip(self, store):
        rid = await store.add("strategies", {
            "title": "T1", "content": "c", "tags": ["tag-a", "tag-b", "中文标签"],
        })
        record = await store.get("strategies", rid)
        assert record["tags"] == ["tag-a", "tag-b", "中文标签"]

    @pytest.mark.asyncio
    async def test_empty_metadata_defaults_to_dict(self, store):
        rid = await store.add("knowledge_chunks", {
            "source_path": "/empty.md", "title": "Empty", "content": "test",
        })
        record = await store.get("knowledge_chunks", rid)
        assert isinstance(record["metadata"], dict)


class TestRepeatInit:
    """重复初始化测试"""

    @pytest.mark.asyncio
    async def test_repeat_init_preserves_data(self, store):
        rid = await store.add("knowledge_chunks", {
            "source_path": "/persist.md", "title": "Persist", "content": "data",
        })
        # 再次 init
        await store.init()
        record = await store.get("knowledge_chunks", rid)
        assert record is not None
        assert record["title"] == "Persist"


class TestAllStoreTypes:
    """所有 5 种 table 均可读写"""

    @pytest.mark.asyncio
    async def test_all_tables_writable(self, store):
        records = {
            "knowledge_store": {
                "source_path": "/test.md", "title": "T", "content": "c",
            },
            "knowledge_chunks": {
                "source_path": "/test.md", "title": "T", "content": "c",
            },
            "chat_messages": {
                "session_id": "s1", "role": "user", "content": "hello",
            },
            "error_store": {
                "task": "test", "wrong_answer": "w", "correct_answer": "c",
            },
            "error_experiences": {
                "task": "test", "wrong_answer": "w", "correct_answer": "c",
            },
            "strategy_store": {
                "title": "S", "content": "c",
            },
            "strategies": {
                "title": "S", "content": "c",
            },
            "examples": {
                "task": "t", "answer": "a",
            },
        }
        for table_name in TABLE_NAMES:
            rid = await store.add(table_name, records[table_name])
            fetched = await store.get(table_name, rid)
            assert fetched is not None, f"Failed for table: {table_name}"
            assert fetched["id"] == rid


class TestClose:
    """关闭连接"""

    @pytest.mark.asyncio
    async def test_close(self, store):
        await store.close()
        assert store._conn is None
        assert store._initialized is False
