"""
MemoryQwen — ModelAdapter 模块测试
"""

import pytest
from unittest.mock import AsyncMock, patch

from src.model_adapter.base import BaseModelAdapter, ChatResult, EmbeddingResult
from src.model_adapter.openai_compat import OpenAICompatAdapter


class MockConfig:
    """Mock 配置"""
    class Model:
        default_provider = "ollama"
        default_light_model = "qwen2.5:7b"
        default_deep_model = "qwen2.5:14b"
        embedding_model = "test-embedding"
        embedding_device = "cpu"
        embedding_dimension = 512
        class Providers:
            ollama = type('obj', (object,), {'base_url': 'http://localhost:11434', 'api_key': ''})
        providers = {'ollama': Providers.ollama}
    model = Model()


class TestBaseModelAdapter:
    """基类接口测试"""

    def test_get_token_count_estimate(self):
        """测试 token 估算"""
        adapter = MockAdapter(MockConfig())
        # 中文
        count = adapter.get_token_count("你好世界")
        assert count > 0
        # 英文
        count = adapter.get_token_count("hello world")
        assert count > 0
        # 混合
        count = adapter.get_token_count("你好 hello world 测试")
        assert count > 0


class MockAdapter(BaseModelAdapter):
    """测试用 Mock 适配器"""

    async def chat(self, messages, model="default", temperature=0.7,
                   max_tokens=4096, tools=None, stream=False):
        return ChatResult(
            content="测试回复",
            token_usage={"prompt": 10, "completion": 5, "total": 15},
            model="test-model",
            latency_ms=100.0,
        )

    async def embed(self, texts, model="default"):
        return EmbeddingResult(
            embeddings=[[0.1, 0.2, 0.3] for _ in texts],
            model="test-embedding",
            token_usage=10,
            latency_ms=50.0,
        )
