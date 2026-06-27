"""
MemoryQwen — ModelClient 工厂
根据配置 provider 创建对应客户端实例。
不绑定任何具体模型名称。
"""

from __future__ import annotations

import logging
from typing import Any

from src.model_client.base import ModelClient
from src.model_client.openai_compatible import OpenAICompatibleClient

logger = logging.getLogger(__name__)

_PROVIDER_MAP: dict[str, type[ModelClient]] = {
    "ollama": OpenAICompatibleClient,
    "lm_studio": OpenAICompatibleClient,
    "llamacpp": OpenAICompatibleClient,
    "openai": OpenAICompatibleClient,
}


def create_model_client(config: Any) -> ModelClient:
    """
    根据配置创建 ModelClient 实例。

    所有已知本地后端（Ollama / LM Studio / llama.cpp）都使用
    OpenAI-compatible 协议，因此统一用 OpenAICompatibleClient。

    后续可通过 _PROVIDER_MAP 扩展新的客户端实现。
    """
    provider = config.model_client.provider

    client_cls = _PROVIDER_MAP.get(provider)
    if client_cls is None:
        logger.warning(
            "Unknown model provider '%s', falling back to OpenAI-compatible. "
            "Supported: %s",
            provider, list(_PROVIDER_MAP.keys()),
        )
        client_cls = OpenAICompatibleClient

    logger.info("Creating ModelClient: provider=%s, class=%s", provider, client_cls.__name__)
    return client_cls(config)
