"""
MemoryQwen — Agent 工厂
"""

from __future__ import annotations

import logging
from typing import Any

from src.agent.chat_service import AgentChatService

logger = logging.getLogger(__name__)


def create_agent_chat_service(
    config: Any,
    model_client,
    retriever,
    store,
) -> AgentChatService:
    """创建 AgentChatService 实例"""
    logger.info("Creating AgentChatService")
    return AgentChatService(config, model_client, retriever, store)
