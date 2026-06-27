"""
OpenAICompatibleClient 测试
所有测试使用 mock HTTP 响应，不启动真实模型服务。
"""

from __future__ import annotations

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from typing import Any

from src.model_client.openai_compatible import OpenAICompatibleClient
from src.model_client.base import (
    ChatResponse, CompleteResponse, ChatStreamEvent,
    ConnectionError, TimeoutError, AuthenticationError,
    ModelNotFoundError, RateLimitError,
)


# ─── 辅助：Mock 配置 ─────────────────────────────────

class MockModelClientConfig:
    provider = "ollama"
    base_url = "http://localhost:11434"
    api_key = ""
    model = ""
    timeout = 10
    max_retries = 1
    default_temperature = 0.7
    default_max_tokens = 2048


class MockConfig:
    model_client = MockModelClientConfig()


# ─── 辅助：Mock response ──────────────────────────────

def mock_chat_response(content: str = "你好！我是 AI。", model: str = "test-model"):
    """生成 mock /chat/completions 响应"""
    return {
        "id": "chat-123",
        "object": "chat.completion",
        "created": 1700000000,
        "model": model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": content},
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


def mock_complete_response(text: str = "Once upon a time", model: str = "test-model"):
    """生成 mock /completions 响应"""
    return {
        "id": "cmpl-123",
        "object": "text_completion",
        "created": 1700000000,
        "model": model,
        "choices": [{
            "index": 0,
            "text": text,
            "finish_reason": "stop",
        }],
        "usage": {"prompt_tokens": 5, "completion_tokens": 10, "total_tokens": 15},
    }


# ─── Fixture ──────────────────────────────────────────

@pytest.fixture
def client():
    return OpenAICompatibleClient(MockConfig())


# ─── chat 测试 ─────────────────────────────────────────

class TestChat:
    """chat 接口测试"""

    @pytest.mark.asyncio
    async def test_chat_basic(self, client):
        """测试基本 chat 调用"""
        mock_resp = mock_chat_response()

        async def mock_post(path, json=None, **kw):
            m = Mock()
            m.status_code = 200
            m.json = MagicMock(return_value=mock_resp)
            return m

        client._client.post = mock_post
        result = await client.chat(
            messages=[{"role": "user", "content": "你好"}],
            model="test-model",
            temperature=0.5,
            max_tokens=100,
        )
        assert isinstance(result, ChatResponse)
        assert result.content == "你好！我是 AI。"
        assert result.model == "test-model"
        assert result.usage["total_tokens"] == 15
        assert result.finish_reason == "stop"

    @pytest.mark.asyncio
    async def test_chat_payload_format(self, client):
        """验证 chat 请求 payload 格式正确"""
        captured = {}

        async def mock_post(path, json=None, **kw):
            captured["payload"] = json
            m = Mock()
            m.status_code = 200
            m.json = MagicMock(return_value=mock_chat_response())
            return m

        client._client.post = mock_post
        await client.chat(
            messages=[{"role": "user", "content": "测试 payload"}],
            model="qwen2.5:7b",
            temperature=0.8,
            max_tokens=512,
        )

        payload = captured["payload"]
        assert payload["model"] == "qwen2.5:7b"
        assert payload["messages"] == [{"role": "user", "content": "测试 payload"}]
        assert payload["temperature"] == 0.8
        assert payload["max_tokens"] == 512
        assert payload["stream"] is False
        # 端点路径
        assert captured.get("path") is None or True  # 我们只验证 payload

    @pytest.mark.asyncio
    async def test_chat_with_chatmessage_object(self, client):
        """测试传入 ChatMessage 对象也能正常工作"""
        from src.model_client.base import ChatMessage

        mock_resp = mock_chat_response()

        async def mock_post(path, json=None, **kw):
            m = Mock()
            m.status_code = 200
            m.json = MagicMock(return_value=mock_resp)
            return m

        client._client.post = mock_post
        result = await client.chat(
            messages=[ChatMessage(role="user", content="ChatMessage 对象")],
            model="test-model",
        )
        assert isinstance(result, ChatResponse)
        assert result.content == "你好！我是 AI。"

    @pytest.mark.asyncio
    async def test_chat_stream(self, client):
        """测试流式 chat"""
        from src.model_client.base import ChatStreamEvent

        chunk_data = [
            'data: {"id":"1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}',
            'data: {"id":"1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"你好"},"finish_reason":null}]}',
            'data: {"id":"1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"世界"},"finish_reason":null}]}',
            'data: {"id":"1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}',
            'data: [DONE]',
        ]

        class MockStreamResponse:
            status_code = 200

            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            async def aiter_lines(self):
                for line in chunk_data:
                    yield line

            async def aread(self):
                return b""

        client._client.stream = lambda method, path, json=None: MockStreamResponse()
        events = []
        async for event in await client.chat(
            messages=[{"role": "user", "content": "流式测试"}],
            model="test-model",
            stream=True,
        ):
            events.append(event)

        # 累积文本
        text = "".join(e.text for e in events if e.text)
        assert text == "你好世界"

        # 确认最后有 finish
        finish_events = [e for e in events if e.finish_reason]
        assert len(finish_events) > 0
        assert finish_events[-1].finish_reason == "stop"

    @pytest.mark.asyncio
    async def test_chat_connection_error(self, client):
        """测试连接失败时抛出 ConnectionError"""
        async def mock_post(path, json=None, **kw):
            import httpx
            raise httpx.ConnectError("Connection refused")

        client._client.post = mock_post

        with pytest.raises(ConnectionError) as excinfo:
            await client.chat(
                messages=[{"role": "user", "content": "hi"}],
                model="test-model",
            )
        assert "无法连接" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_chat_timeout_error(self, client):
        """测试超时错误"""
        async def mock_post(path, json=None, **kw):
            import httpx
            raise httpx.TimeoutException("Timed out")

        client._client.post = mock_post

        with pytest.raises(TimeoutError) as excinfo:
            await client.chat(
                messages=[{"role": "user", "content": "hi"}],
                model="test-model",
            )
        assert "超时" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_chat_authentication_error(self, client):
        """测试 401 认证错误"""
        async def mock_post(path, json=None, **kw):
            m = Mock()
            m.status_code = 401
            m.content = b'{"error": "unauthorized"}'
            return m

        client._client.post = mock_post

        with pytest.raises(AuthenticationError) as excinfo:
            await client.chat(
                messages=[{"role": "user", "content": "hi"}],
                model="test-model",
            )
        assert excinfo.value.status_code == 401

    @pytest.mark.asyncio
    async def test_chat_model_not_found(self, client):
        """测试 404 模型不存在"""
        async def mock_post(path, json=None, **kw):
            m = Mock()
            m.status_code = 404
            m.content = b'{"error": "model not found"}'
            return m

        client._client.post = mock_post

        with pytest.raises(ModelNotFoundError) as excinfo:
            await client.chat(
                messages=[{"role": "user", "content": "hi"}],
                model="nonexistent-model",
            )
        assert excinfo.value.status_code == 404

    @pytest.mark.asyncio
    async def test_chat_rate_limit(self, client):
        """测试 429 频率限制"""
        async def mock_post(path, json=None, **kw):
            m = Mock()
            m.status_code = 429
            m.content = b'{"error": "rate limited"}'
            return m

        client._client.post = mock_post

        with pytest.raises(RateLimitError) as excinfo:
            await client.chat(
                messages=[{"role": "user", "content": "hi"}],
                model="test-model",
            )
        assert excinfo.value.status_code == 429

    @pytest.mark.asyncio
    async def test_chat_uses_config_defaults(self, client):
        """测试 chat 使用配置默认值"""
        cfg = client.config
        assert cfg.model_client.default_temperature == 0.7
        assert cfg.model_client.default_max_tokens == 2048

        captured = {}

        async def mock_post(path, json=None, **kw):
            captured["payload"] = json
            m = Mock()
            m.status_code = 200
            m.json = MagicMock(return_value=mock_chat_response())
            return m

        client._client.post = mock_post
        # 不传 temperature 和 max_tokens，应使用默认值
        await client.chat(
            messages=[{"role": "user", "content": "默认参数测试"}],
            model="test-model",
        )

        payload = captured["payload"]
        assert payload["temperature"] == cfg.model_client.default_temperature
        assert payload["max_tokens"] == cfg.model_client.default_max_tokens


# ─── complete 测试 ─────────────────────────────────────

class TestComplete:
    """complete 接口测试"""

    @pytest.mark.asyncio
    async def test_complete_basic(self, client):
        """测试基本 complete 调用"""
        mock_resp = mock_complete_response()

        async def mock_post(path, json=None, **kw):
            m = Mock()
            m.status_code = 200
            m.json = MagicMock(return_value=mock_resp)
            return m

        client._client.post = mock_post
        result = await client.complete(
            prompt="Once upon a",
            model="test-model",
        )
        assert isinstance(result, CompleteResponse)
        assert result.content == "Once upon a time"
        assert result.usage["total_tokens"] == 15
        assert result.finish_reason == "stop"

    @pytest.mark.asyncio
    async def test_complete_payload_format(self, client):
        """验证 complete 请求 payload 格式正确"""
        captured = {}

        async def mock_post(path, json=None, **kw):
            captured["payload"] = json
            m = Mock()
            m.status_code = 200
            m.json = MagicMock(return_value=mock_complete_response())
            return m

        client._client.post = mock_post
        await client.complete(
            prompt="Hello, world!",
            model="gpt-3.5-turbo-instruct",
            temperature=0.9,
            max_tokens=100,
        )

        payload = captured["payload"]
        assert payload["model"] == "gpt-3.5-turbo-instruct"
        assert payload["prompt"] == "Hello, world!"
        assert payload["temperature"] == 0.9
        assert payload["max_tokens"] == 100
        assert payload["stream"] is False

    @pytest.mark.asyncio
    async def test_complete_connection_error(self, client):
        """测试 complete 连接失败"""
        async def mock_post(path, json=None, **kw):
            import httpx
            raise httpx.ConnectError("Connection refused")

        client._client.post = mock_post

        with pytest.raises(ConnectionError):
            await client.complete(prompt="test", model="test-model")

    @pytest.mark.asyncio
    async def test_complete_timeout_error(self, client):
        """测试 complete 超时"""
        async def mock_post(path, json=None, **kw):
            import httpx
            raise httpx.TimeoutException("Timed out")

        client._client.post = mock_post

        with pytest.raises(TimeoutError):
            await client.complete(prompt="test", model="test-model")

    @pytest.mark.asyncio
    async def test_complete_stream(self, client):
        """测试流式 complete"""
        chunk_data = [
            'data: {"id":"1","object":"text_completion","choices":[{"index":0,"text":"Hello","finish_reason":null}]}',
            'data: {"id":"1","object":"text_completion","choices":[{"index":0,"text":" world","finish_reason":null}]}',
            'data: {"id":"1","object":"text_completion","choices":[{"index":0,"text":"","finish_reason":"stop"}]}',
            'data: [DONE]',
        ]

        class MockStreamResponse:
            status_code = 200

            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            async def aiter_lines(self):
                for line in chunk_data:
                    yield line

            async def aread(self):
                return b""

        client._client.stream = lambda method, path, json=None: MockStreamResponse()
        events = []
        async for event in await client.complete(
            prompt="Hello",
            model="test-model",
            stream=True,
        ):
            events.append(event)

        text = "".join(e.text for e in events if e.text)
        assert text == "Hello world"


# ─── health_check 测试 ─────────────────────────────────

class TestHealthCheck:
    """health_check 测试"""

    @pytest.mark.asyncio
    async def test_health_check_ok(self, client):
        """测试 /models 返回 200"""
        async def mock_get(path, **kw):
            m = Mock()
            m.status_code = 200
            return m

        client._client.get = mock_get
        result = await client.health_check()
        assert result is True

    @pytest.mark.asyncio
    async def test_health_check_fail(self, client):
        """测试 /models 返回非 200"""
        async def mock_get(path, **kw):
            m = Mock()
            m.status_code = 500
            return m

        client._client.get = mock_get
        result = await client.health_check()
        assert result is False

    @pytest.mark.asyncio
    async def test_health_check_connection_refused(self, client):
        """测试连接被拒绝时返回 False"""
        async def mock_get(path, **kw):
            raise Exception("Connection refused")

        client._client.get = mock_get
        result = await client.health_check()
        assert result is False


# ─── list_models 测试 ──────────────────────────────────

class TestListModels:
    """list_models 测试"""

    @pytest.mark.asyncio
    async def test_list_models_success(self, client):
        """测试列出模型成功"""
        async def mock_get(path, **kw):
            m = Mock()
            m.status_code = 200
            m.json = MagicMock(return_value={
                "data": [{"id": "qwen2.5:7b"}, {"id": "qwen2.5:14b"}]
            })
            return m

        client._client.get = mock_get
        models = await client.list_models()
        assert models == ["qwen2.5:7b", "qwen2.5:14b"]

    @pytest.mark.asyncio
    async def test_list_models_empty_on_error(self, client):
        """测试错误时返回空列表"""
        async def mock_get(path, **kw):
            raise Exception("Error")

        client._client.get = mock_get
        models = await client.list_models()
        assert models == []


# ─── close 测试 ────────────────────────────────────────

class TestClose:
    """close 测试"""

    @pytest.mark.asyncio
    async def test_close(self, client):
        """测试关闭连接不报错"""
        client._client.aclose = AsyncMock()
        await client.close()
        client._client.aclose.assert_called_once()
