"""
MemoryQwen — JobRunner 工厂
"""

from src.job_runner.runner import BackgroundJobRunner


def create_job_runner(config, task_runtime, guardian_service=None) -> BackgroundJobRunner:
    return BackgroundJobRunner(config, task_runtime, guardian_service)
