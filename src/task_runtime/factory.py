"""
MemoryQwen — TaskRuntime 工厂
"""

from src.task_runtime.store import InMemoryTaskStore
from src.task_runtime.service import TaskRuntimeService


def create_task_runtime(config):
    store_type = getattr(config.task_runtime, "store", "memory")
    if store_type == "sqlite":
        from src.task_runtime.sqlite_store import SQLiteTaskStore
        db_path = getattr(config.task_runtime, "database_path", "memory/tasks.db")
        store = SQLiteTaskStore(db_path)
    else:
        store = InMemoryTaskStore()
    return TaskRuntimeService(config, store)
