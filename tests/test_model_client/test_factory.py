"""
ModelClient 工厂测试
验证 create_model_client 根据配置正确创建客户端。
"""

import pytest
from src.model_client.factory import create_model_client
from src.model_client.openai_compatible import OpenAICompatibleClient


# ─── Mock 配置 ─────────────────────────────────────────

class MockMCConfig:
    provider: str
    base_url: str = "http://localhost:11434"
    api_key: str = ""
    model: str = ""
    timeout: int = 60
    max_retries: int = 3
    default_temperature: float = 0.7
    default_max_tokens: int = 4096


class MockConfig:
    model_client: MockMCConfig = MockMCConfig()


def make_config(provider: str) -> MockConfig:
    cfg = MockConfig()
    cfg.model_client.provider = provider
    return cfg


class TestFactory:
    """工厂函数测试"""

    def test_ollama(self):
        """ollama → OpenAICompatibleClient"""
        config = make_config("ollama")
        client = create_model_client(config)
        assert isinstance(client, OpenAICompatibleClient)
        assert "11434" in client.base_url

    def test_lm_studio(self):
        """lm_studio → OpenAICompatibleClient"""
        config = make_config("lm_studio")
        client = create_model_client(config)
        assert isinstance(client, OpenAICompatibleClient)

    def test_llamacpp(self):
        """llamacpp → OpenAICompatibleClient"""
        config = make_config("llamacpp")
        client = create_model_client(config)
        assert isinstance(client, OpenAICompatibleClient)

    def test_openai(self):
        """openai → OpenAICompatibleClient"""
        config = make_config("openai")
        client = create_model_client(config)
        assert isinstance(client, OpenAICompatibleClient)

    def test_unknown_provider_fallback(self):
        """未知 provider 回退到 OpenAICompatibleClient"""
        config = make_config("unknown_provider_xyz")
        client = create_model_client(config)
        assert isinstance(client, OpenAICompatibleClient)

    def test_client_base_url_format(self):
        """验证 base_url 格式正确（追加 /v1）"""
        config = make_config("ollama")
        config.model_client.base_url = "http://localhost:11434"
        client = create_model_client(config)
        assert client.base_url.endswith("/v1")
        assert "11434" in client.base_url

    def test_client_inherits_timeout(self):
        """验证客户端继承了超时配置"""
        config = make_config("ollama")
        config.model_client.timeout = 120
        client = create_model_client(config)
        assert client._timeout == 120
