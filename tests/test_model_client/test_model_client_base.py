"""
ModelClient 基类测试
"""

import pytest
from src.model_client.base import (
    ChatMessage, ChatResponse, CompleteResponse, ChatStreamEvent,
    ModelClientError, ConnectionError, TimeoutError,
    AuthenticationError, ModelNotFoundError, RateLimitError,
)


class TestChatMessage:
    """ChatMessage 数据结构测试"""

    def test_basic_creation(self):
        msg = ChatMessage(role="user", content="你好")
        assert msg.role == "user"
        assert msg.content == "你好"
        assert msg.name is None

    def test_with_name(self):
        msg = ChatMessage(role="assistant", content="回复", name="test")
        assert msg.name == "test"

    def test_dict_conversion(self):
        """验证能转为 dict"""
        msg = ChatMessage(role="system", content="设定")
        d = {"role": msg.role, "content": msg.content}
        assert d == {"role": "system", "content": "设定"}


class TestChatResponse:
    """ChatResponse 数据结构测试"""

    def test_default_usage(self):
        resp = ChatResponse(content="你好", model="test")
        assert resp.content == "你好"
        assert resp.model == "test"
        assert resp.usage["total_tokens"] == 0
        assert resp.finish_reason == "stop"

    def test_with_usage(self):
        resp = ChatResponse(
            content="回答",
            model="gpt-3.5",
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            finish_reason="length",
        )
        assert resp.usage["total_tokens"] == 30
        assert resp.finish_reason == "length"


class TestCompleteResponse:
    """CompleteResponse 数据结构测试"""

    def test_basic(self):
        resp = CompleteResponse(content="Hello", model="test")
        assert resp.content == "Hello"
        assert resp.usage["total_tokens"] == 0


class TestChatStreamEvent:
    """流式事件测试"""

    def test_text_event(self):
        event = ChatStreamEvent(text="Hello")
        assert event.text == "Hello"
        assert event.finish_reason is None

    def test_finish_event(self):
        event = ChatStreamEvent(finish_reason="stop")
        assert event.text == ""
        assert event.finish_reason == "stop"


class TestErrorHierarchy:
    """异常层次测试"""

    def test_inheritance(self):
        assert issubclass(ConnectionError, ModelClientError)
        assert issubclass(TimeoutError, ModelClientError)
        assert issubclass(AuthenticationError, ModelClientError)
        assert issubclass(ModelNotFoundError, ModelClientError)
        assert issubclass(RateLimitError, ModelClientError)

    def test_error_attributes(self):
        err = ModelClientError("出错了", status_code=500, response_body="内部错误")
        assert str(err) == "出错了"
        assert err.status_code == 500
        assert err.response_body == "内部错误"

    def test_error_without_details(self):
        err = ConnectionError("连接失败")
        assert err.status_code is None
        assert err.response_body is None
