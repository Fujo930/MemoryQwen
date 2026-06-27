"""
MemoryQwen — InMemoryTaskStore
"""

from __future__ import annotations

from src.task_runtime.models import TaskRecord


class InMemoryTaskStore:
    """内存任务存储（后续可换 SQLite）"""

    def __init__(self):
        self._tasks: dict[str, TaskRecord] = {}

    def add(self, task: TaskRecord):
        self._tasks[task.task_id] = task

    def get(self, task_id: str) -> TaskRecord | None:
        return self._tasks.get(task_id)

    def update(self, task_id: str, patch: dict):
        task = self._tasks.get(task_id)
        if not task:
            raise KeyError(f"Task not found: {task_id}")
        for k, v in patch.items():
            if hasattr(task, k):
                setattr(task, k, v)

    def list(self, status: str | None = None, task_type: str | None = None, limit: int = 100) -> list[TaskRecord]:
        result = list(self._tasks.values())
        if status:
            result = [t for t in result if t.status == status]
        if task_type:
            result = [t for t in result if t.task_type == task_type]
        return result[:limit]

    def delete(self, task_id: str):
        self._tasks.pop(task_id, None)

    def count(self, status: str | None = None, task_type: str | None = None) -> int:
        return len(self.list(status=status, task_type=task_type))
