"""
MemoryQwen — MemoryStore 工厂
根据配置 backend 创建对应实例。
"""

from __future__ import annotations

import logging
from typing import Any

from src.memory_store.base import MemoryStore
from src.memory_store.sqlite_store import SQLiteStore

logger = logging.getLogger(__name__)

BACKEND_MAP: dict[str, type[MemoryStore]] = {
    "sqlite": SQLiteStore,
}


def create_memory_store(config: Any) -> MemoryStore:
    """根据配置创建 MemoryStore 实例"""
    backend = config.memory_store.backend

    store_cls = BACKEND_MAP.get(backend)
    if store_cls is None:
        logger.warning(
            "Unknown memory store backend '%s', falling back to sqlite. "
            "Supported: %s",
            backend, list(BACKEND_MAP.keys()),
        )
        store_cls = SQLiteStore

    logger.info("Creating MemoryStore: backend=%s, class=%s", backend, store_cls.__name__)
    return store_cls(config)
