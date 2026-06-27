"""
MemoryQwen — ModelClient 抽象基类
定义统一的模型调用接口，不绑定任何具体模型名称。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import AsyncIterator


@dataclass
class ChatMessage:
    """聊天消息"""
    role: str          # "system" | "user" | "assistant" | "tool"
    content: str
    name: str | None = None


@dataclass
class ChatResponse:
    """聊天响应"""
    content: str
    model: str
    usage: dict = field(default_factory=lambda: {
        "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0,
    })
    finish_reason: str = "stop"


@dataclass
class CompleteResponse:
    """补全响应"""
    content: str
    model: str
    usage: dict = field(default_factory=lambda: {
        "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0,
    })
    finish_reason: str = "stop"


class ChatStreamEvent:
    """流式事件"""
    def __init__(self, text: str = "", finish_reason: str | None = None):
        self.text = text
        self.finish_reason = finish_reason


class ModelClientError(Exception):
    """模型调用通用异常"""
    def __init__(self, message: str, status_code: int | None = None,
                 response_body: str | None = None):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class ConnectionError(ModelClientError):
    """连接失败"""
    pass


class TimeoutError(ModelClientError):
    """请求超时"""
    pass


class AuthenticationError(ModelClientError):
    """认证失败（API key 错误）"""
    pass


class ModelNotFoundError(ModelClientError):
    """模型不存在"""
    pass


class RateLimitError(ModelClientError):
    """频率限制"""
    pass


class ModelClient(ABC):
    """模型客户端基类——所有 provider 的统一接口"""

    def __init__(self, config):
        self.config = config

    @abstractmethod
    async def chat(
        self,
        messages: list[dict] | list[ChatMessage],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
    ) -> ChatResponse | AsyncIterator[ChatStreamEvent]:
        """
        聊天补全。

        stream=False: 返回 ChatResponse
        stream=True:  返回 AsyncIterator[ChatStreamEvent]
        """
        ...

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
    ) -> CompleteResponse | AsyncIterator[ChatStreamEvent]:
        """
        文本补全（用于简单生成场景）。

        stream=False: 返回 CompleteResponse
        stream=True:  返回 AsyncIterator[ChatStreamEvent]
        """
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """检查后端服务是否可用"""
        ...

    @abstractmethod
    async def list_models(self) -> list[str]:
        """列出后端可用模型"""
        ...
