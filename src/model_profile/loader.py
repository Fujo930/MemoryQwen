"""
MemoryQwen — ModelProfile Loader
从 YAML/JSON 加载、保存、验证 profile。
"""

from __future__ import annotations

import json
import yaml
from pathlib import Path

from src.model_profile.models import ModelProfile


class ProfileLoadError(Exception):
    """Profile 加载错误"""
    pass


def load_profile(path: str) -> ModelProfile:
    """从 YAML 或 JSON 文件加载 ModelProfile"""
    p = Path(path)
    if not p.exists():
        raise ProfileLoadError(f"Profile file not found: {path}")

    raw_text = p.read_text(encoding="utf-8")
    ext = p.suffix.lower()

    try:
        if ext in (".yaml", ".yml"):
            raw = yaml.safe_load(raw_text)
        elif ext == ".json":
            raw = json.loads(raw_text)
        else:
            raise ProfileLoadError(f"Unsupported profile format: {ext}")
    except yaml.YAMLError as e:
        raise ProfileLoadError(f"YAML parse error: {e}")
    except json.JSONDecodeError as e:
        raise ProfileLoadError(f"JSON parse error: {e}")

    if not isinstance(raw, dict):
        raise ProfileLoadError("Profile must be a dictionary")

    try:
        # 展平嵌套结构
        profile = _dict_to_profile(raw)
        profile.validate()
        return profile
    except (TypeError, ValueError) as e:
        raise ProfileLoadError(f"Invalid profile: {e}")


def save_profile(profile: ModelProfile, path: str):
    """保存 ModelProfile 到 YAML 文件"""
    raw = _profile_to_dict(profile)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        yaml.dump(raw, f, default_flow_style=False, allow_unicode=True)


def validate_profile(raw: dict) -> None:
    """验证 raw dict 是否为合法 profile，不合法时抛错"""
    profile = _dict_to_profile(raw)
    profile.validate()


def _dict_to_profile(raw: dict) -> ModelProfile:
    """将 dict 转为 ModelProfile"""
    from src.model_profile.models import Capabilities, Limits, Protocol, Runtime, Roles
    return ModelProfile(
        model_id=raw.get("model_id", ""),
        family=raw.get("family"),
        size_b=raw.get("size_b"),
        backend=raw.get("backend"),
        capabilities=Capabilities(**_dict_to_caps(raw.get("capabilities", {}))),
        limits=Limits(**_dict_to_limits(raw.get("limits", {}))),
        protocol=Protocol(**_dict_to_protocol(raw.get("protocol", {}))),
        runtime=Runtime(**_dict_to_runtime(raw.get("runtime", {}))),
        roles=Roles(**_dict_to_roles(raw.get("roles", {}))),
    )


def _dict_to_caps(d: dict) -> dict:
    return {
        "reasoning": float(d.get("reasoning", 0.5)),
        "coding": float(d.get("coding", 0.5)),
        "tool_calling": float(d.get("tool_calling", 0.5)),
        "json_stability": float(d.get("json_stability", 0.5)),
        "chinese": float(d.get("chinese", 0.5)),
        "long_context": float(d.get("long_context", 0.5)),
    }


def _dict_to_limits(d: dict) -> dict:
    return {
        "recommended_context": int(d.get("recommended_context", 8192)),
        "max_context": int(d.get("max_context", 32768)),
        "recommended_output_tokens": int(d.get("recommended_output_tokens", 1024)),
    }


def _dict_to_protocol(d: dict) -> dict:
    return {
        "preferred_format": str(d.get("preferred_format", "plain")),
        "supports_memory_query": bool(d.get("supports_memory_query", False)),
        "supports_tool_call": bool(d.get("supports_tool_call", False)),
        "needs_strict_json_prompt": bool(d.get("needs_strict_json_prompt", True)),
    }


def _dict_to_runtime(d: dict) -> dict:
    return {
        "default_temperature": float(d.get("default_temperature", 0.4)),
        "reasoning_temperature": float(d.get("reasoning_temperature", 0.6)),
        "json_temperature": float(d.get("json_temperature", 0.1)),
        "max_retries": int(d.get("max_retries", 2)),
    }


def _dict_to_roles(d: dict) -> dict:
    return {
        "suitable_for": list(d.get("suitable_for", ["main_chat"])),
    }


def _profile_to_dict(profile: ModelProfile) -> dict:
    """将 ModelProfile 转为可序列化 dict"""
    caps = profile.capabilities
    limits = profile.limits
    protocol = profile.protocol
    runtime = profile.runtime
    return {
        "model_id": profile.model_id,
        "family": profile.family,
        "size_b": profile.size_b,
        "backend": profile.backend,
        "capabilities": {
            "reasoning": caps.reasoning,
            "coding": caps.coding,
            "tool_calling": caps.tool_calling,
            "json_stability": caps.json_stability,
            "chinese": caps.chinese,
            "long_context": caps.long_context,
        },
        "limits": {
            "recommended_context": limits.recommended_context,
            "max_context": limits.max_context,
            "recommended_output_tokens": limits.recommended_output_tokens,
        },
        "protocol": {
            "preferred_format": protocol.preferred_format,
            "supports_memory_query": protocol.supports_memory_query,
            "supports_tool_call": protocol.supports_tool_call,
            "needs_strict_json_prompt": protocol.needs_strict_json_prompt,
        },
        "runtime": {
            "default_temperature": runtime.default_temperature,
            "reasoning_temperature": runtime.reasoning_temperature,
            "json_temperature": runtime.json_temperature,
            "max_retries": runtime.max_retries,
        },
        "roles": {
            "suitable_for": profile.roles.suitable_for,
        },
    }
