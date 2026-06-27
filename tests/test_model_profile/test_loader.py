"""
ModelProfile Loader 测试
"""

import json
import pytest
import tempfile
from pathlib import Path

from src.model_profile.loader import (
    load_profile, save_profile, validate_profile, ProfileLoadError,
)
from src.model_profile.models import ModelProfile


@pytest.fixture
def temp_dir():
    d = tempfile.mkdtemp()
    yield Path(d)
    import shutil
    shutil.rmtree(d, ignore_errors=True)


class TestYamlLoad:
    def test_load_valid_yaml(self, temp_dir):
        fp = temp_dir / "profile.yaml"
        fp.write_text("""
model_id: test_model
family: qwen
size_b: 7.0
backend: ollama
capabilities:
  reasoning: 0.7
  coding: 0.5
  tool_calling: 0.5
  json_stability: 0.5
  chinese: 0.8
  long_context: 0.5
limits:
  recommended_context: 8192
  max_context: 32768
  recommended_output_tokens: 1024
protocol:
  preferred_format: plain
roles:
  suitable_for:
    - main_chat
""")
        profile = load_profile(str(fp))
        assert profile.model_id == "test_model"
        assert profile.capabilities.reasoning == 0.7
        assert profile.capabilities.chinese == 0.8

    def test_load_invalid_yaml(self, temp_dir):
        fp = temp_dir / "bad.yaml"
        fp.write_text("{{invalid: yaml: [")
        with pytest.raises(ProfileLoadError, match="parse"):
            load_profile(str(fp))


class TestJsonLoad:
    def test_load_valid_json(self, temp_dir):
        fp = temp_dir / "profile.json"
        fp.write_text(json.dumps({
            "model_id": "json_test",
            "capabilities": {"reasoning": 0.6},
            "roles": {"suitable_for": ["main_chat"]},
        }))
        profile = load_profile(str(fp))
        assert profile.model_id == "json_test"


class TestSave:
    def test_save_and_reload(self, temp_dir):
        profile = ModelProfile(model_id="save_test")
        fp = temp_dir / "saved.yaml"
        save_profile(profile, str(fp))
        loaded = load_profile(str(fp))
        assert loaded.model_id == "save_test"


class TestValidate:
    def test_validate_pass(self):
        validate_profile({"model_id": "v", "roles": {"suitable_for": ["main_chat"]}})

    def test_validate_fail(self):
        with pytest.raises((ProfileLoadError, ValueError, TypeError)):
            validate_profile({"model_id": "v", "capabilities": {"reasoning": 999}})

    def test_validate_no_model_id(self):
        with pytest.raises((ProfileLoadError, ValueError)):
            validate_profile({})


class TestLoadErrors:
    def test_nonexistent_file(self):
        with pytest.raises(ProfileLoadError, match="not found"):
            load_profile("/nonexistent/profile.yaml")

    def test_invalid_extension(self, temp_dir):
        fp = temp_dir / "profile.txt"
        fp.write_text("{}")
        with pytest.raises(ProfileLoadError, match="Unsupported"):
            load_profile(str(fp))
