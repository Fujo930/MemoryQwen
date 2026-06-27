"""
ModelProfile 数据模型测试
"""

import pytest
from src.model_profile.models import (
    ModelProfile, Capabilities, Limits, Protocol, Runtime, Roles,
    VALID_FORMATS, VALID_ROLES,
)


class TestCapabilities:
    def test_defaults(self):
        caps = Capabilities()
        assert caps.reasoning == 0.5
        assert caps.chinese == 0.5

    def test_validate_range(self):
        caps = Capabilities(reasoning=0.8, coding=0.0)
        caps.validate()  # 不抛异常

    def test_validate_out_of_range(self):
        caps = Capabilities(reasoning=1.5)
        with pytest.raises(ValueError, match="reasoning"):
            caps.validate()

    def test_validate_negative(self):
        caps = Capabilities(reasoning=-0.1)
        with pytest.raises(ValueError, match="reasoning"):
            caps.validate()


class TestLimits:
    def test_validate_positive(self):
        limits = Limits(recommended_context=0)
        with pytest.raises(ValueError, match="recommended_context"):
            limits.validate()


class TestProtocol:
    def test_invalid_format(self):
        p = Protocol(preferred_format="invalid")
        with pytest.raises(ValueError, match="preferred_format"):
            p.validate()

    def test_valid_formats(self):
        for fmt in VALID_FORMATS:
            p = Protocol(preferred_format=fmt)
            p.validate()  # 不抛异常


class TestRoles:
    def test_invalid_role(self):
        r = Roles(suitable_for=["invalid_role"])
        with pytest.raises(ValueError, match="invalid role"):
            r.validate()

    def test_valid_roles(self):
        r = Roles(suitable_for=["main_chat", "coder"])
        r.validate()


class TestModelProfile:
    def test_default_profile(self):
        p = ModelProfile(model_id="test")
        assert p.model_id == "test"
        assert p.capabilities.reasoning == 0.5

    def test_no_shared_mutable_defaults(self):
        """确保两个 profile 不共享可变默认值"""
        p1 = ModelProfile(model_id="a")
        p2 = ModelProfile(model_id="b")
        p1.capabilities.reasoning = 0.9
        assert p2.capabilities.reasoning == 0.5  # 不受影响
        p1.roles.suitable_for.append("coder")
        assert "coder" not in p2.roles.suitable_for
