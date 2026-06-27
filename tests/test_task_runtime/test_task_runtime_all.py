"""
TaskRuntime 测试 (≥25)
"""

from __future__ import annotations

import pytest
from src.task_runtime.models import (
    TaskRecord, TaskTransition, ALLOWED_TRANSITIONS, VALID_STATUSES, VALID_TYPES, now_iso,
)
from src.task_runtime.store import InMemoryTaskStore
from src.task_runtime.service import TaskRuntimeService, InvalidTransitionError
from src.task_runtime.policy import GuardianTaskPolicy
from src.gpu_guardian.models import GuardianState


# ─── Mock Config ───────────────────────────────────────

class MockTaskConfig:
    enabled = True
    store = "memory"
    auto_resume_on_normal = False


class MockConfig:
    task_runtime = MockTaskConfig()


# ─── Models Tests ──────────────────────────────────────

class TestTaskRecord:
    def test_defaults(self):
        t = TaskRecord()
        assert t.status == "pending"
        assert t.task_type == "custom"
        assert t.task_id == ""

    def test_status_values(self):
        assert "pending" in VALID_STATUSES
        assert "running" in VALID_STATUSES
        assert "paused" in VALID_STATUSES
        assert "cancelled" in VALID_STATUSES
        assert len(VALID_STATUSES) == 6

    def test_type_values(self):
        assert "ingestion" in VALID_TYPES
        assert "embedding" in VALID_TYPES
        assert "custom" in VALID_TYPES

    def test_now_iso(self):
        ts = now_iso()
        assert "T" in ts  # ISO format


# ─── Store Tests ───────────────────────────────────────

class TestInMemoryStore:
    def test_add_and_get(self):
        store = InMemoryTaskStore()
        t = TaskRecord(task_id="1", title="Task 1")
        store.add(t)
        assert store.get("1") is t

    def test_update(self):
        store = InMemoryTaskStore()
        t = TaskRecord(task_id="1", status="pending")
        store.add(t)
        store.update("1", {"status": "running"})
        assert store.get("1").status == "running"

    def test_list_by_status(self):
        store = InMemoryTaskStore()
        store.add(TaskRecord(task_id="1", status="running"))
        store.add(TaskRecord(task_id="2", status="paused"))
        assert len(store.list(status="running")) == 1

    def test_list_by_type(self):
        store = InMemoryTaskStore()
        store.add(TaskRecord(task_id="1", task_type="ingestion"))
        store.add(TaskRecord(task_id="2", task_type="custom"))
        assert len(store.list(task_type="ingestion")) == 1

    def test_delete(self):
        store = InMemoryTaskStore()
        store.add(TaskRecord(task_id="1"))
        store.delete("1")
        assert store.get("1") is None


# ─── Service Tests ─────────────────────────────────────

@pytest.fixture
def svc():
    return TaskRuntimeService(MockConfig())


class TestServiceLifecycle:
    def test_create_task_pending(self, svc):
        t = svc.create_task("ingestion", "Test")
        assert t.status == "pending"
        assert t.task_type == "ingestion"
        assert t.task_id

    def test_start_task(self, svc):
        t = svc.create_task("custom", "X")
        svc.start_task(t.task_id)
        t2 = svc.get_task(t.task_id)
        assert t2.status == "running"
        assert t2.started_at

    def test_update_progress(self, svc):
        t = svc.create_task("custom", "X")
        svc.start_task(t.task_id)
        svc.update_progress(t.task_id, 5, 10, "half done")
        t2 = svc.get_task(t.task_id)
        assert t2.progress_current == 5
        assert t2.progress_total == 10
        assert t2.progress_message == "half done"

    def test_pause_running_task(self, svc):
        t = svc.create_task("ingestion", "X")
        svc.start_task(t.task_id)
        svc.pause_task(t.task_id, "user_pause")
        t2 = svc.get_task(t.task_id)
        assert t2.status == "paused"
        assert t2.pause_reason == "user_pause"

    def test_resume_paused_task(self, svc):
        t = svc.create_task("ingestion", "X")
        svc.start_task(t.task_id)
        svc.pause_task(t.task_id, "user_pause")
        svc.resume_task(t.task_id)
        t2 = svc.get_task(t.task_id)
        assert t2.status == "running"

    def test_complete_running_task(self, svc):
        t = svc.create_task("custom", "X")
        svc.start_task(t.task_id)
        svc.complete_task(t.task_id)
        t2 = svc.get_task(t.task_id)
        assert t2.status == "completed"
        assert t2.completed_at

    def test_fail_running_task(self, svc):
        t = svc.create_task("custom", "X")
        svc.start_task(t.task_id)
        svc.fail_task(t.task_id, "error msg")
        t2 = svc.get_task(t.task_id)
        assert t2.status == "failed"
        assert t2.error_message == "error msg"

    def test_cancel_pending_task(self, svc):
        t = svc.create_task("custom", "X")
        svc.cancel_task(t.task_id)
        t2 = svc.get_task(t.task_id)
        assert t2.status == "cancelled"

    def test_cancel_running_task(self, svc):
        t = svc.create_task("custom", "X")
        svc.start_task(t.task_id)
        svc.cancel_task(t.task_id)
        t2 = svc.get_task(t.task_id)
        assert t2.status == "cancelled"


class TestServiceInvalidTransitions:
    def test_completed_to_running(self, svc):
        t = svc.create_task("custom", "X")
        svc.start_task(t.task_id)
        svc.complete_task(t.task_id)
        with pytest.raises(InvalidTransitionError):
            svc.start_task(t.task_id)

    def test_failed_to_running(self, svc):
        t = svc.create_task("custom", "X")
        svc.start_task(t.task_id)
        svc.fail_task(t.task_id, "e")
        with pytest.raises(InvalidTransitionError):
            svc.start_task(t.task_id)

    def test_cancelled_to_running(self, svc):
        t = svc.create_task("custom", "X")
        svc.cancel_task(t.task_id)
        with pytest.raises(InvalidTransitionError):
            svc.start_task(t.task_id)

    def test_pause_completed_invalid(self, svc):
        t = svc.create_task("custom", "X")
        svc.start_task(t.task_id)
        svc.complete_task(t.task_id)
        with pytest.raises(InvalidTransitionError):
            svc.pause_task(t.task_id, "user_pause")


# ─── Policy Tests ──────────────────────────────────────

def _make_task(tid, ttype):
    return TaskRecord(task_id=tid, task_type=ttype, status="running")

GP = GuardianTaskPolicy()


class TestGuardianTaskPolicy:
    def test_pause_background_ingestion(self):
        tasks = [_make_task("1", "ingestion"), _make_task("2", "custom")]
        paused = GP.evaluate(["pause_background_ingestion"], tasks)
        assert paused == ["1"]

    def test_pause_index_refresh(self):
        tasks = [_make_task("1", "index_refresh")]
        paused = GP.evaluate(["pause_index_refresh"], tasks)
        assert paused == ["1"]

    def test_pause_background_tasks(self):
        tasks = [_make_task("1", "ingestion"), _make_task("2", "embedding"), _make_task("3", "custom")]
        paused = GP.evaluate(["pause_background_tasks"], tasks)
        assert "1" in paused
        assert "2" in paused
        assert "3" not in paused

    def test_pause_all_ai_tasks(self):
        tasks = [
            _make_task("1", "ingestion"),
            _make_task("2", "model_chat"),
            _make_task("3", "error_learning"),
        ]
        paused = GP.evaluate(["pause_all_ai_tasks"], tasks)
        assert "1" in paused
        assert "2" in paused
        # error_learning should NOT be paused
        assert "3" not in paused

    def test_policy_normal_no_auto_resume(self):
        tasks = [_make_task("1", "ingestion")]
        paused = GP.evaluate(["allow_14b", "allow_background_ingestion"], tasks)
        assert paused == []


# ─── Guardian Integration Tests ────────────────────────

class TestGuardianIntegration:
    def test_apply_guardian_state_pauses_tasks(self):
        svc = TaskRuntimeService(MockConfig())
        t1 = svc.create_task("ingestion", "Import")
        t2 = svc.create_task("custom", "Other")
        svc.start_task(t1.task_id)
        svc.start_task(t2.task_id)

        state = GuardianState(recommended_actions=["pause_background_ingestion"])
        paused = svc.apply_guardian_state(state)
        assert t1.task_id in paused
        assert svc.get_task(t1.task_id).status == "paused"
        # custom task should NOT be paused
        assert svc.get_task(t2.task_id).status == "running"

    def test_apply_guardian_state_returns_paused_ids(self):
        svc = TaskRuntimeService(MockConfig())
        t1 = svc.create_task("ingestion", "X")
        svc.start_task(t1.task_id)
        state = GuardianState(recommended_actions=["pause_background_tasks"])
        paused = svc.apply_guardian_state(state)
        assert paused == [t1.task_id]
