"""
MemoryQwen — ModelAdapter 基类
定义统一的模型通信接口
"""

from __future__ import annotations

import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ChatResult:
    """模型聊天返回结果"""
    content: str
    token_usage: dict  # {"prompt": n, "completion": n, "total": n}
    model: str
    latency_ms: float
    finish_reason: str = "stop"
    tool_calls: list[dict] | None = None


@dataclass
class EmbeddingResult:
    """Embedding 返回结果"""
    embeddings: list[list[float]]
    model: str
    token_usage: int = 0
    latency_ms: float = 0.0


@dataclass
class ModelProfile:
    """模型能力画像"""
    name: str
    provider: str
    max_tokens: int = 8192
    supports_tools: bool = False
    supports_json: bool = False
    supports_streaming: bool = True
    json_stability: float = 0.0       # 0-1
    instruction_following: float = 0.0
    context_retention: float = 0.0
    embedding_dimensions: int = 512
    notes: list[str] = field(default_factory=list)


class BaseModelAdapter(ABC):
    """所有模型适配器的基类"""

    def __init__(self, config: Any):
        self.config = config

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: list[dict] | None = None,
        stream: bool = False,
    ) -> ChatResult:
        """统一聊天接口"""
        ...

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
        model: str = "default",
    ) -> EmbeddingResult:
        """统一 embedding 接口"""
        ...

    async def test_profile(self) -> ModelProfile:
        """测试模型能力，生成画像（默认实现）"""
        profile = ModelProfile(
            name="unknown",
            provider="unknown",
        )
        try:
            result = await self.chat(
                messages=[{"role": "user", "content": "你好，请回复'OK'"}],
                model="default",
                max_tokens=10,
            )
            profile.max_tokens = 8192  # 默认值，后续可细化
            profile.supports_streaming = True
            profile.notes.append("基础通信正常")
        except Exception as e:
            profile.notes.append(f"通信测试失败: {e}")

        return profile

    def get_token_count(self, text: str) -> int:
        """估算 token 数（可被子类覆盖）"""
        # 粗略估算：中文 1.5 token/字，英文 1 token/4字符
        import re
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        other_chars = len(text) - chinese_chars
        return int(chinese_chars * 1.5 + other_chars / 4) + 10
