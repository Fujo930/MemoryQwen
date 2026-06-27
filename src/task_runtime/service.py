"""
MemoryQwen — TaskRuntimeService
任务状态机 + 生命周期管理
"""

from __future__ import annotations

import uuid
from typing import Any

from src.task_runtime.models import (
    TaskRecord, TaskTransition, ALLOWED_TRANSITIONS,
    VALID_STATUSES, VALID_TYPES, VALID_PAUSE_REASONS, now_iso,
)
from src.task_runtime.store import InMemoryTaskStore


class InvalidTransitionError(Exception):
    pass


class TaskRuntimeService:
    """任务运行时服务"""

    def __init__(self, config: Any, store: InMemoryTaskStore | None = None):
        self.config = config
        self.store = store or InMemoryTaskStore()
        self.transitions: list[TaskTransition] = []

    # ─── CRUD ──────────────────────────────────────────

    def create_task(self, task_type: str, title: str, metadata: dict | None = None) -> TaskRecord:
        if task_type not in VALID_TYPES:
            raise ValueError(f"Invalid task_type: {task_type}")
        t = TaskRecord(
            task_id=str(uuid.uuid4()),
            task_type=task_type,
            title=title,
            status="pending",
            created_at=now_iso(),
            updated_at=now_iso(),
            metadata=metadata or {},
        )
        self.store.add(t)
        return t

    def list_tasks(self, status: str | None = None, task_type: str | None = None) -> list[TaskRecord]:
        return self.store.list(status=status, task_type=task_type)

    def get_task(self, task_id: str) -> TaskRecord | None:
        return self.store.get(task_id)

    # ─── 状态转换 ─────────────────────────────────────┐

    def start_task(self, task_id: str) -> TaskRecord:
        return self._transition(task_id, "running")

    def update_progress(self, task_id: str, current: int, total: int = 0, message: str = "") -> TaskRecord:
        t = self._get(task_id)
        t.progress_current = current
        if total > 0:
            t.progress_total = total
        if message:
            t.progress_message = message
        t.updated_at = now_iso()
        self.store.update(task_id, {k: getattr(t, k) for k in ("progress_current", "progress_total", "progress_message", "updated_at")})
        return t

    def pause_task(self, task_id: str, reason: str) -> TaskRecord:
        if reason not in VALID_PAUSE_REASONS:
            raise ValueError(f"Invalid pause_reason: {reason}")
        t = self._transition(task_id, "paused")
        t.paused_at = now_iso()
        t.pause_reason = reason
        self.store.update(task_id, {"paused_at": t.paused_at, "pause_reason": reason})
        return t

    def resume_task(self, task_id: str) -> TaskRecord:
        t = self._transition(task_id, "running")
        t.paused_at = ""
        t.pause_reason = ""
        self.store.update(task_id, {"paused_at": "", "pause_reason": ""})
        return t

    def complete_task(self, task_id: str) -> TaskRecord:
        t = self._transition(task_id, "completed")
        t.completed_at = now_iso()
        self.store.update(task_id, {"completed_at": t.completed_at})
        return t

    def fail_task(self, task_id: str, error_message: str) -> TaskRecord:
        t = self._transition(task_id, "failed")
        t.error_message = error_message
        t.completed_at = now_iso()
        self.store.update(task_id, {"error_message": error_message, "completed_at": t.completed_at})
        return t

    def cancel_task(self, task_id: str, reason: str = "user_cancel") -> TaskRecord:
        t = self._transition(task_id, "cancelled")
        t.completed_at = now_iso()
        self.store.update(task_id, {"completed_at": t.completed_at})
        return t

    # ─── Guardian 集成 ─────────────────────────────────

    def apply_guardian_state(self, guardian_state: Any) -> list[str]:
        """根据 GuardianState.recommended_actions 暂停 running tasks"""
        from src.task_runtime.policy import GuardianTaskPolicy
        policy = GuardianTaskPolicy()
        to_pause = policy.evaluate(
            guardian_state.recommended_actions,
            self.store.list(status="running"),
        )
        paused_ids = []
        for task_id in to_pause:
            try:
                self.pause_task(task_id, "gpu_game_mode")
                paused_ids.append(task_id)
            except InvalidTransitionError:
                pass
        return paused_ids

    # ─── 内部 ─────────────────────────────────────────┐

    def _get(self, task_id: str) -> TaskRecord:
        t = self.store.get(task_id)
        if t is None:
            raise KeyError(f"Task not found: {task_id}")
        return t

    def _transition(self, task_id: str, to_status: str) -> TaskRecord:
        t = self._get(task_id)
        allowed = ALLOWED_TRANSITIONS.get(t.status, set())
        if to_status not in allowed:
            raise InvalidTransitionError(
                f"Cannot transition task {task_id} from '{t.status}' to '{to_status}'"
            )
        self.transitions.append(TaskTransition(
            task_id=task_id, from_status=t.status, to_status=to_status,
            reason="", timestamp=now_iso(),
        ))
        t.status = to_status
        t.updated_at = now_iso()
        if to_status == "running" and not t.started_at:
            t.started_at = now_iso()
        self.store.update(task_id, {"status": to_status, "updated_at": t.updated_at, "started_at": t.started_at})
        return t
