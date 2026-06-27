"""
PromptBuilder + ModelProfile 集成测试
"""

import pytest
from src.agent.prompt_builder import PromptBuilder
from src.model_profile.models import ModelProfile, Protocol

SYSTEM = "你是 MemoryQwen。"


class TestPromptBuilderWithProfile:
    def test_without_profile_unchanged(self):
        """无 profile 时行为不变"""
        builder = PromptBuilder(SYSTEM)  # model_profile=None
        msgs = builder.build("hello")
        system_content = msgs[0]["content"]
        assert system_content == SYSTEM
        assert "JSON" not in system_content
        assert "XML" not in system_content

    def test_plain_format_no_extra(self):
        profile = ModelProfile(model_id="test", protocol=Protocol(preferred_format="plain"))
        builder = PromptBuilder(SYSTEM, model_profile=profile)
        msgs = builder.build("hello")
        system_content = msgs[0]["content"]
        assert system_content == SYSTEM

    def test_json_format_injects_hint(self):
        profile = ModelProfile(model_id="test", protocol=Protocol(preferred_format="json"))
        builder = PromptBuilder(SYSTEM, model_profile=profile)
        msgs = builder.build("hello")
        system_content = msgs[0]["content"]
        assert "严格 JSON" in system_content

    def test_xml_format_injects_hint(self):
        profile = ModelProfile(model_id="test", protocol=Protocol(preferred_format="xml"))
        builder = PromptBuilder(SYSTEM, model_profile=profile)
        msgs = builder.build("hello")
        system_content = msgs[0]["content"]
        assert "XML" in system_content
