"""
MemoryQwen — ModelProfile Registry
"""

from __future__ import annotations

import logging

from src.model_profile.models import ModelProfile
from src.model_profile.defaults import get_builtin, get_all_builtins
from src.model_profile.loader import load_profile, ProfileLoadError

logger = logging.getLogger(__name__)


class ProfileRegistry:
    """ModelProfile 注册表"""

    def __init__(self):
        self._profiles: dict[str, ModelProfile] = {}
        # 预加载内置 profiles
        self._profiles.update(get_all_builtins())

    def register(self, profile: ModelProfile):
        """注册一个 profile"""
        self._profiles[profile.model_id] = profile

    def get(self, profile_id: str) -> ModelProfile | None:
        """获取 profile"""
        return self._profiles.get(profile_id)

    def load(self, path: str) -> ModelProfile:
        """从文件加载并注册"""
        profile = load_profile(path)
        self.register(profile)
        return profile

    def get_or_fallback(self, profile_id: str | None = None, path: str | None = None) -> ModelProfile:
        """加载指定 profile 或 fallback 到 generic"""
        # 先尝试从文件加载
        if path:
            try:
                return self.load(path)
            except ProfileLoadError as e:
                logger.warning("Profile load failed: %s, falling back", e)

        # 再尝试从注册表获取
        if profile_id:
            p = self.get(profile_id)
            if p:
                return p

        # fallback
        logger.info("Using fallback profile: generic_openai_compatible")
        return self.get("generic_openai_compatible")


_registry: ProfileRegistry | None = None


def get_registry() -> ProfileRegistry:
    global _registry
    if _registry is None:
        _registry = ProfileRegistry()
    return _registry
