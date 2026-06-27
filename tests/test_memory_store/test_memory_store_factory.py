"""
MemoryStore 工厂测试
"""

import pytest
from src.memory_store.factory import create_memory_store
from src.memory_store.sqlite_store import SQLiteStore


class MockMSConfig:
    backend = "sqlite"
    database_path = ":memory:"

class MockConfig:
    memory_store = MockMSConfig()


class TestFactory:
    def test_sqlite(self):
        store = create_memory_store(MockConfig())
        assert isinstance(store, SQLiteStore)

    def test_unknown_backend_fallback(self):
        config = MockConfig()
        config.memory_store.backend = "unknown_db"
        store = create_memory_store(config)
        assert isinstance(store, SQLiteStore)
