"""
MemoryQwen — 内置 Jobs
"""

from __future__ import annotations

from pathlib import Path

from src.job_runner.base import BaseJob, JobContext, checkpoint
from src.job_runner.models import JobResult


class FakeJob(BaseJob):
    """用于测试的可中断 job"""
    job_type = "custom"

    def __init__(self, steps: int = 10, fail_at: int = -1):
        self.steps = steps
        self.fail_at = fail_at

    def estimate_total(self) -> int:
        return self.steps

    def run(self, context: JobContext) -> JobResult:
        for i in range(1, self.steps + 1):
            if self.fail_at > 0 and i == self.fail_at:
                raise RuntimeError("FakeJob failed at step %d" % i)

            status = checkpoint(context, i, self.steps, f"step {i}/{self.steps}")
            if status == "paused":
                return JobResult(task_id=context.task_id, status="paused", processed=i - 1, total=self.steps)
            if status == "cancelled":
                return JobResult(task_id=context.task_id, status="cancelled", processed=i - 1, total=self.steps)
        return JobResult(task_id=context.task_id, status="completed", processed=self.steps, total=self.steps)


class IngestionDirectoryJob(BaseJob):
    """目录摄入 job — 通过 subprocess 调 CLI ingest"""
    job_type = "ingestion"

    def __init__(self, dir_path: str, supported_extensions: list[str] | None = None):
        self.dir_path = str(Path(dir_path).resolve())
        self.supported = supported_extensions or [".txt", ".md"]

    def estimate_total(self) -> int:
        return len(self._list_files())

    def _list_files(self) -> list[Path]:
        dp = Path(self.dir_path)
        if not dp.exists() or not dp.is_dir():
            return []
        files = []
        for ext in self.supported:
            for f in dp.glob(f"*{ext}"):
                files.append(f)
        return sorted(files)

    def run(self, context: JobContext) -> JobResult:
        import subprocess, sys

        files = self._list_files()
        total = len(files)
        checkpoint(context, 0, total, "starting")

        # 通过 subprocess 调 CLI ingest（避免 async/sync 嵌套）
        result = subprocess.run(
            [sys.executable, "-m", "src.cli", "ingest", self.dir_path],
            capture_output=True, text=True, timeout=120,
        )

        # 解析输出
        proc = 0
        for line in result.stdout.split("\n"):
            if "Files ingested:" in line:
                try:
                    proc = int(line.split(":")[-1].strip())
                except ValueError:
                    pass

        # 判断状态
        status = "completed"
        task_status = context.task_runtime.get_task(context.task_id)
        if task_status:
            status = task_status.status
        if status == "paused":
            return JobResult(task_id=context.task_id, status="paused", processed=proc, total=total)
        if status == "cancelled":
            return JobResult(task_id=context.task_id, status="cancelled", processed=proc, total=total)

        checkpoint(context, proc, total, "done")

        return JobResult(
            task_id=context.task_id, status="completed",
            processed=proc, total=total,
            message=result.stdout.strip()[:200],
            metadata={"files_processed": proc},
        )
