"""
StrategyLearningService 测试
"""

from __future__ import annotations

import json
import pytest
import pytest_asyncio
import tempfile
from pathlib import Path

from src.agent.models import CorrectionRequest
from src.agent.strategy_learning import StrategyLearningService, STRATEGY_STORE
from src.memory_store.sqlite_store import SQLiteStore


class MockConfig:
    class Agent:
        enable_strategy_learning = True
    agent = Agent()
    memory_store = type('obj', (), {'database_path': ':memory:'})()


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
def service(store):
    return StrategyLearningService(MockConfig(), store)


class TestUpsertStrategy:
    @pytest.mark.asyncio
    async def test_add_strategy(self, service, store):
        req = CorrectionRequest(
            user_message="test", wrong_answer="w", correct_answer="c",
            failure_type="math_error", strategy="使用计算器验证",
        )
        result = await service.upsert_strategy_from_correction(req, "err-1")
        assert result["created"] is True
        assert result["strategy_id"] != ""

        record = await store.get(STRATEGY_STORE, result["strategy_id"])
        assert record is not None
        assert "strategy:math_error:" in record.get("title", "")

    @pytest.mark.asyncio
    async def test_strategy_hash_dedup(self, service):
        req = CorrectionRequest(
            user_message="test", wrong_answer="w", correct_answer="c",
            failure_type="math", strategy="verify with calc",
        )
        r1 = await service.upsert_strategy_from_correction(req, "err-1")
        assert r1["created"] is True

        r2 = await service.upsert_strategy_from_correction(req, "err-2")
        assert r2.get("updated") is True or r2.get("created") is False

    @pytest.mark.asyncio
    async def test_updated_count_increments(self, service, store):
        req = CorrectionRequest(
            user_message="t", wrong_answer="w", correct_answer="c",
            failure_type="type1", strategy="unique strategy for counting",
        )
        r1 = await service.upsert_strategy_from_correction(req, "err-1")
        r2 = await service.upsert_strategy_from_correction(req, "err-2")

        record = await store.get(STRATEGY_STORE, r1.get("strategy_id") or r2.get("strategy_id"))
        meta = record.get("metadata", {})
        if isinstance(meta, str):
            meta = json.loads(meta)
        assert meta.get("updated_count", 0) >= 2

    @pytest.mark.asyncio
    async def test_source_error_ids_append(self, service, store):
        req = CorrectionRequest(
            user_message="t", wrong_answer="w", correct_answer="c",
            failure_type="type2", strategy="append ids test",
        )
        r1 = await service.upsert_strategy_from_correction(req, "err-a")
        r2 = await service.upsert_strategy_from_correction(req, "err-b")

        sid = r1.get("strategy_id") or r2.get("strategy_id")
        record = await store.get(STRATEGY_STORE, sid)
        meta = record.get("metadata", {})
        if isinstance(meta, str):
            meta = json.loads(meta)
        ids = meta.get("source_error_ids", [])
        assert "err-a" in ids or "err-b" in ids

    @pytest.mark.asyncio
    async def test_strategy_metadata(self, service, store):
        req = CorrectionRequest(
            user_message="meta test", wrong_answer="bad", correct_answer="good",
            failure_type="meta_type", strategy="meta strategy",
        )
        result = await service.upsert_strategy_from_correction(req, "err-99")
        record = await store.get(STRATEGY_STORE, result["strategy_id"])
        meta = record.get("metadata", {})
        if isinstance(meta, str):
            meta = json.loads(meta)
        assert meta.get("record_kind") == "strategy"
        assert "strategy_hash" in meta
        assert meta.get("created_by") == "correction"
        assert meta.get("last_used_at") is None

    @pytest.mark.asyncio
    async def test_last_used_at_none(self, service, store):
        req = CorrectionRequest(
            user_message="t", wrong_answer="w", correct_answer="c",
            strategy="last used test",
        )
        result = await service.upsert_strategy_from_correction(req, "err")
        record = await store.get(STRATEGY_STORE, result["strategy_id"])
        meta = record.get("metadata", {})
        if isinstance(meta, str):
            meta = json.loads(meta)
        assert meta.get("last_used_at") is None

    @pytest.mark.asyncio
    async def test_hash_normalized(self, service):
        req1 = CorrectionRequest(
            user_message="t", wrong_answer="w", correct_answer="c",
            failure_type="Math", strategy=" Use Calculator ",
        )
        r1 = await service.upsert_strategy_from_correction(req1, "err-1")

        req2 = CorrectionRequest(
            user_message="t2", wrong_answer="w2", correct_answer="c2",
            failure_type="math", strategy="use calculator",
        )
        r2 = await service.upsert_strategy_from_correction(req2, "err-2")
        # 应视为同一策略（normalized 后相同）
        assert r2.get("updated") is True or r2.get("created") is False
