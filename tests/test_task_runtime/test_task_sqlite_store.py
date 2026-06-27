"""
SQLiteTaskStore 测试
"""

from __future__ import annotations

import json
import tempfile
import pytest
from pathlib import Path

from src.task_runtime.models import TaskRecord, TaskTransition
from src.task_runtime.sqlite_store import SQLiteTaskStore


@pytest.fixture
def store():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    s = SQLiteTaskStore(tmp.name)
    yield s
    s.close()
    Path(tmp.name).unlink(missing_ok=True)


class TestSQLiteStore:
    def test_add_and_get(self, store):
        t = TaskRecord(task_id="t1", task_type="ingestion", title="Test")
        store.add(t)
        t2 = store.get("t1")
        assert t2 is not None
        assert t2.title == "Test"
        assert t2.task_type == "ingestion"

    def test_get_nonexistent(self, store):
        assert store.get("nonexistent") is None

    def test_update(self, store):
        t = TaskRecord(task_id="t2", status="pending")
        store.add(t)
        store.update("t2", {"status": "running", "progress_current": 5})
        t2 = store.get("t2")
        assert t2.status == "running"
        assert t2.progress_current == 5

    def test_list_by_status(self, store):
        store.add(TaskRecord(task_id="a", status="running"))
        store.add(TaskRecord(task_id="b", status="paused"))
        assert len(store.list(status="running")) == 1
        assert len(store.list(status="paused")) == 1

    def test_list_by_type(self, store):
        store.add(TaskRecord(task_id="a", task_type="ingestion"))
        store.add(TaskRecord(task_id="b", task_type="custom"))
        assert len(store.list(task_type="ingestion")) == 1

    def test_delete(self, store):
        store.add(TaskRecord(task_id="d"))
        store.delete("d")
        assert store.get("d") is None

    def test_delete_nonexistent_no_crash(self, store):
        store.delete("zzz")

    def test_count(self, store):
        store.add(TaskRecord(task_id="1", status="running"))
        store.add(TaskRecord(task_id="2", status="running"))
        assert store.count(status="running") == 2

    def test_metadata_roundtrip(self, store):
        t = TaskRecord(task_id="meta", metadata={"key": "val", "num": 42})
        store.add(t)
        t2 = store.get("meta")
        assert t2.metadata == {"key": "val", "num": 42}

    def test_transition(self, store):
        tr = TaskTransition(task_id="t1", from_status="pending", to_status="running",
                            reason="start", timestamp="2024-01-01T00:00:00")
        store.add_transition(tr)
        transitions = store.list_transitions("t1")
        assert len(transitions) == 1
        assert transitions[0].to_status == "running"


class TestSQLiteStorePersistence:
    """跨连接持久化测试"""
    def test_data_persists(self, store):
        store.add(TaskRecord(task_id="p1", status="running"))
        # 通过 get 重读（同连接）
        t = store.get("p1")
        assert t.status == "running"

        # 新建另一个连接
        from src.task_runtime.sqlite_store import SQLiteTaskStore
        store2 = SQLiteTaskStore(store.db_path)
        t2 = store2.get("p1")
        assert t2 is not None
        assert t2.status == "running"
        store2.close()
