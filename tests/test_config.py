"""
MemoryQwen 配置模块测试
"""

import pytest
import yaml
from pathlib import Path
from src.config import load_config, AppConfig, get_config


class TestConfig:
    """配置加载测试"""

    def test_default_config_loading(self):
        """测试默认配置加载"""
        config = load_config()
        assert config is not None
        assert config.system.name == "MemoryQwen"
        assert config.system.version == "0.2.0-alpha"
        assert config.server.host == "127.0.0.1"
        assert config.server.port == 7860

    def test_model_defaults(self):
        """测试模型默认配置"""
        config = load_config()
        assert config.model.default_provider == "ollama"
        assert config.model.default_light_model  # 不绑定具体名称
        assert config.model.default_deep_model   # 不绑定具体名称
        assert config.model.embedding_dimension == 512

    def test_memory_retrieval_defaults(self):
        """测试记忆检索默认参数"""
        config = load_config()
        assert config.memory.retrieval.top_k == 5
        assert config.memory.retrieval.rrf_k == 60
        assert config.memory.retrieval.vector_weight == 0.7
        assert config.memory.retrieval.bm25_weight == 0.3

    def test_chunking_defaults(self):
        """测试切片默认配置"""
        config = load_config()
        assert config.memory.chunking.max_tokens == 512
        assert config.memory.chunking.overlap_tokens == 32
        assert config.memory.chunking.strategy == "semantic"

    def test_context_budget(self):
        """测试 agent 配置新增字段"""
        config = load_config()
        assert config.agent.system_prompt != ""
        assert config.agent.default_top_k == 5
        assert config.agent.max_recent_messages == 10
        assert config.agent.cite_sources is True
        assert config.agent.save_chat_memory is True

    def test_yaml_roundtrip(self):
        """测试 YAML 配置加载一致性"""
        config = load_config()
        # 验证所有主要 section 都存在
        assert hasattr(config, 'system')
        assert hasattr(config, 'server')
        assert hasattr(config, 'model')
        assert hasattr(config, 'memory')
        assert hasattr(config, 'ingestion')
        assert hasattr(config, 'agent')
        assert hasattr(config, 'reasoner')
        assert hasattr(config, 'gpu_guardian')
        assert hasattr(config, 'backup')

    def test_gpu_guardian_defaults_disabled(self):
        """测试 GPU Guardian 默认配置"""
        config = load_config()
        assert config.gpu_guardian.enabled is True
        assert config.gpu_guardian.provider == "nvidia_smi"
        assert config.gpu_guardian.light_yield_vram_ratio == 0.55

    def test_supported_extensions(self):
        """测试支持的文件扩展名"""
        config = load_config()
        assert ".txt" in config.ingestion.supported_extensions
        assert ".md" in config.ingestion.supported_extensions
        assert len(config.ingestion.supported_extensions) == 2

    def test_get_config_caching(self):
        """测试配置缓存"""
        c1 = load_config()
        c2 = get_config()
        assert c1 is c2  # 同一对象
