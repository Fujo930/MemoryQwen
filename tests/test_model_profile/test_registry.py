"""
ProfileRegistry 测试
"""

from src.model_profile.registry import ProfileRegistry
from src.model_profile.models import ModelProfile


class TestRegistry:
    def test_register_and_get(self):
        reg = ProfileRegistry()
        p = ModelProfile(model_id="reg_test")
        reg.register(p)
        assert reg.get("reg_test") is p

    def test_get_nonexistent(self):
        reg = ProfileRegistry()
        assert reg.get("nope") is None

    def test_builtins_loaded(self):
        """内置 profile 预加载"""
        reg = ProfileRegistry()
        assert reg.get("qwen_7b_default") is not None
        assert reg.get("generic_openai_compatible") is not None

    def test_get_or_fallback_builtin(self):
        reg = ProfileRegistry()
        p = reg.get_or_fallback(profile_id="qwen_7b_default")
        assert p.model_id == "qwen_7b_default"

    def test_get_or_fallback_unknown(self):
        """未知 profile_id fallback 到 generic"""
        reg = ProfileRegistry()
        p = reg.get_or_fallback(profile_id="nonexistent")
        assert p.model_id == "generic_openai_compatible"
