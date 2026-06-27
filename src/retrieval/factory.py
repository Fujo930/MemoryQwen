"""
MemoryQwen — Retriever 工厂
"""

from __future__ import annotations

import logging
from typing import Any

from src.retrieval.base import BaseRetriever
from src.retrieval.keyword import KeywordRetriever

logger = logging.getLogger(__name__)


def create_keyword_retriever(config: Any, store) -> KeywordRetriever:
    """创建 KeywordRetriever 实例"""
    logger.info("Creating KeywordRetriever")
    return KeywordRetriever(config, store)
