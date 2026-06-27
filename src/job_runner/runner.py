"""
MemoryQwen — BackgroundJobRunner
"""

from __future__ import annotations

import logging
from typing import Any

from src.job_runner.base import BaseJob, JobContext, get_task_status
from src.job_runner.models import JobResult
from src.task_runtime.service import TaskRuntimeService, InvalidTransitionError

logger = logging.getLogger(__name__)


class BackgroundJobRunner:
    """后台 job 执行器"""

    def __init__(self, config: Any, task_runtime: TaskRuntimeService, guardian_service=None):
        self.config = config
        self.task_runtime = task_runtime
        self.guardian_service = guardian_service

    def run_job(self, job: BaseJob, task_type: str, title: str, metadata: dict | None = None) -> JobResult:
        """创建任务 → 执行 → 完成"""
        task = self.task_runtime.create_task(task_type, title, metadata)
        return self.run_existing_task(job, task.task_id)

    def run_existing_task(self, job: BaseJob, task_id: str) -> JobResult:
        """在已有 task 上执行 job"""
        try:
            self.task_runtime.start_task(task_id)
        except InvalidTransitionError:
            pass

        context = JobContext(task_id, self.task_runtime)

        try:
            result = job.run(context)
        except Exception as e:
            self._fail_task(task_id, str(e))
            return JobResult(task_id=task_id, status="failed", message=str(e))

        # 根据最终状态决定如何处理
        final_status = get_task_status(context)
        if final_status == "cancelled":
            return JobResult(task_id=task_id, status="cancelled", message="Task was cancelled")
        if final_status == "paused":
            return JobResult(task_id=task_id, status="paused", message="Task paused")
        if final_status == "running":
            try:
                self.task_runtime.complete_task(task_id)
            except InvalidTransitionError:
                pass
            return JobResult(task_id=task_id, status=result.status or "completed",
                             processed=result.processed, total=result.total, message=result.message, metadata=result.metadata)

        return result

    # ─── Guardian checkpoint ───────────────────────────

    def guardian_checkpoint(self, context: JobContext, current: int, total: int = 0, message: str = "") -> str:
        """checkpoint + Guardian 检查"""
        from src.job_runner.base import checkpoint
        status = checkpoint(context, current, total, message)

        if self.guardian_service and self._check_guardian_enabled():
            try:
                import asyncio
                state = asyncio.run(self.guardian_service.check_once())
                self.task_runtime.apply_guardian_state(state)
                status = get_task_status(context)
            except Exception as e:
                logger.warning("Guardian check failed: %s", e)

        return status

    def _check_guardian_enabled(self) -> bool:
        cfg = getattr(self.config, "job_runner", None)
        if cfg:
            return getattr(cfg, "check_guardian_on_checkpoint", True)
        return True

    def _fail_task(self, task_id: str, error_message: str):
        try:
            self.task_runtime.fail_task(task_id, error_message)
        except (InvalidTransitionError, KeyError):
            pass
