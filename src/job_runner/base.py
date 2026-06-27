"""
MemoryQwen — BaseJob 接口
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from src.job_runner.models import JobResult


class JobContext:
    """job 执行上下文"""
    def __init__(self, task_id: str, task_runtime, metadata: dict | None = None):
        self.task_id = task_id
        self.task_runtime = task_runtime
        self.metadata = metadata or {}


class BaseJob(ABC):
    job_type: str = "custom"

    def estimate_total(self) -> int | None:
        return None

    @abstractmethod
    def run(self, context: JobContext) -> JobResult:
        ...


def get_task_status(context: JobContext) -> str:
    task = context.task_runtime.get_task(context.task_id)
    return task.status if task else "unknown"


def should_stop(context: JobContext) -> bool:
    status = get_task_status(context)
    return status in ("paused", "cancelled")


def checkpoint(context: JobContext, current: int, total: int = 0, message: str = "") -> str:
    """更新进度并返回当前状态。如果是 paused/cancelled，调用方应停止。"""
    context.task_runtime.update_progress(context.task_id, current, total, message)
    return get_task_status(context)
