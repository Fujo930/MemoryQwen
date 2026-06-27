"""
ErrorLearningService 测试
"""

from __future__ import annotations

import json
import pytest
import pytest_asyncio
import tempfile
from pathlib import Path

from src.agent.models import CorrectionRequest
from src.agent.error_learning import ErrorLearningService, ERROR_STORE
from src.memory_store.sqlite_store import SQLiteStore


class MockConfig:
    class Agent:
        use_error_memory = True
        error_top_k = 3
        max_error_context_chars = 1200
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
    return ErrorLearningService(MockConfig(), store)


class TestRecordCorrection:
    @pytest.mark.asyncio
    async def test_empty_wrong_answer(self, service):
        req = CorrectionRequest(wrong_answer="  ", correct_answer="c")
        with pytest.raises(ValueError, match="wrong_answer"):
            await service.record_correction(req)

    @pytest.mark.asyncio
    async def test_empty_correct_answer(self, service):
        req = CorrectionRequest(wrong_answer="w", correct_answer="")
        with pytest.raises(ValueError, match="correct_answer"):
            await service.record_correction(req)

    @pytest.mark.asyncio
    async def test_writes_to_error_store(self, service, store):
        req = CorrectionRequest(
            session_id="s1", user_message="1+1=?", wrong_answer="3", correct_answer="2",
        )
        resp = await service.record_correction(req)
        assert resp.saved is True
        assert resp.error_id != ""

        record = await store.get(ERROR_STORE, resp.error_id)
        assert record is not None
        assert "3" in record.get("wrong_answer", "")
        assert "2" in record.get("correct_answer", "")

    @pytest.mark.asyncio
    async def test_default_strategy(self, service, store):
        req = CorrectionRequest(
            wrong_answer="w", correct_answer="c", strategy="",
        )
        resp = await service.record_correction(req)
        assert resp.strategy != ""
        record = await store.get(ERROR_STORE, resp.error_id)
        assert "避免重复错误" in record.get("strategy", "")

    @pytest.mark.asyncio
    async def test_strategy_source_user(self, service, store):
        req = CorrectionRequest(
            wrong_answer="w", correct_answer="c", strategy="用户自定义策略",
        )
        resp = await service.record_correction(req)
        assert resp.metadata["strategy_source"] == "user"

    @pytest.mark.asyncio
    async def test_strategy_source_auto(self, service, store):
        req = CorrectionRequest(wrong_answer="w", correct_answer="c", strategy="")
        resp = await service.record_correction(req)
        assert resp.metadata["strategy_source"] == "auto"

    @pytest.mark.asyncio
    async def test_correction_hash_dedup(self, service, store):
        req = CorrectionRequest(
            session_id="s1", user_message="test", wrong_answer="w", correct_answer="c",
        )
        r1 = await service.record_correction(req)
        assert r1.saved is True

        r2 = await service.record_correction(req)
        assert r2.saved is False
        assert r2.metadata.get("reason") == "duplicate"

    @pytest.mark.asyncio
    async def test_error_metadata_fields(self, service, store):
        req = CorrectionRequest(
            session_id="s1", user_message="test", wrong_answer="w",
            correct_answer="c", failure_type="math_error",
        )
        resp = await service.record_correction(req)
        record = await store.get(ERROR_STORE, resp.error_id)
        meta = record.get("metadata", {})
        if isinstance(meta, str):
            meta = json.loads(meta)
        assert meta.get("record_kind") == "error_case"
        assert meta.get("failure_type") == "math_error"
        assert meta.get("has_strategy") is True
        assert meta.get("created_by") == "user_correction"
        assert "correction_hash" in meta

    @pytest.mark.asyncio
    async def test_structured_fields(self, service, store):
        req = CorrectionRequest(
            user_message="test task", wrong_answer="bad", correct_answer="good",
            failure_type="test_type", strategy="test_strategy",
        )
        resp = await service.record_correction(req)
        record = await store.get(ERROR_STORE, resp.error_id)
        assert record.get("task") == "test task"
        assert record.get("wrong_answer") == "bad"
        assert record.get("correct_answer") == "good"
