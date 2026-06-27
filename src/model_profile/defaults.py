"""
MemoryQwen — 内置默认 Profile
"""

from src.model_profile.models import (
    ModelProfile, Capabilities, Limits, Protocol, Runtime, Roles,
)

QWEN_7B_DEFAULT = ModelProfile(
    model_id="qwen_7b_default",
    family="qwen",
    size_b=7.0,
    backend="ollama",
    capabilities=Capabilities(
        reasoning=0.6, coding=0.5, tool_calling=0.4,
        json_stability=0.5, chinese=0.9, long_context=0.5,
    ),
    limits=Limits(recommended_context=8192, max_context=32768, recommended_output_tokens=1024),
    protocol=Protocol(preferred_format="plain", supports_memory_query=True, supports_tool_call=False),
    runtime=Runtime(default_temperature=0.4, reasoning_temperature=0.6, json_temperature=0.1),
    roles=Roles(suitable_for=["main_chat", "summarizer", "low_vram_mode"]),
)

QWEN_14B_DEFAULT = ModelProfile(
    model_id="qwen_14b_default",
    family="qwen",
    size_b=14.0,
    backend="ollama",
    capabilities=Capabilities(
        reasoning=0.7, coding=0.65, tool_calling=0.6,
        json_stability=0.6, chinese=0.9, long_context=0.7,
    ),
    limits=Limits(recommended_context=16384, max_context=131072, recommended_output_tokens=2048),
    protocol=Protocol(preferred_format="plain", supports_memory_query=True, supports_tool_call=True),
    runtime=Runtime(default_temperature=0.4, reasoning_temperature=0.5, json_temperature=0.1),
    roles=Roles(suitable_for=["main_chat", "reasoner", "coder", "router", "summarizer"]),
)

GENERIC_7B = ModelProfile(
    model_id="generic_7b",
    family="generic",
    size_b=7.0,
    backend="openai_compatible",
    capabilities=Capabilities(),
    limits=Limits(),
    protocol=Protocol(),
    runtime=Runtime(),
    roles=Roles(suitable_for=["main_chat", "low_vram_mode"]),
)

GENERIC_OPENAI_COMPATIBLE = ModelProfile(
    model_id="generic_openai_compatible",
    family="generic",
    backend="openai_compatible",
    roles=Roles(suitable_for=["main_chat"]),
)

_BUILTINS: dict[str, ModelProfile] = {
    p.model_id: p
    for p in [QWEN_7B_DEFAULT, QWEN_14B_DEFAULT, GENERIC_7B, GENERIC_OPENAI_COMPATIBLE]
}


def get_builtin(profile_id: str) -> ModelProfile | None:
    return _BUILTINS.get(profile_id)


def get_all_builtins() -> dict[str, ModelProfile]:
    return dict(_BUILTINS)
