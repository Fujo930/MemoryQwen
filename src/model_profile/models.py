"""
MemoryQwen — ModelProfile 数据模型
"""

from __future__ import annotations

from dataclasses import dataclass, field

VALID_FORMATS = {"plain", "json", "xml"}
VALID_ROLES = {
    "main_chat", "reasoner", "coder", "verifier",
    "router", "summarizer", "low_vram_mode",
}


@dataclass
class Capabilities:
    reasoning: float = 0.5
    coding: float = 0.5
    tool_calling: float = 0.5
    json_stability: float = 0.5
    chinese: float = 0.5
    long_context: float = 0.5

    def validate(self):
        """验证所有分数在 0-1 范围内"""
        fields = ["reasoning", "coding", "tool_calling", "json_stability", "chinese", "long_context"]
        for f in fields:
            v = getattr(self, f)
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"capabilities.{f} must be 0.0-1.0, got {v}")


@dataclass
class Limits:
    recommended_context: int = 8192
    max_context: int = 32768
    recommended_output_tokens: int = 1024

    def validate(self):
        if self.recommended_context <= 0:
            raise ValueError("limits.recommended_context must be > 0")
        if self.max_context <= 0:
            raise ValueError("limits.max_context must be > 0")


@dataclass
class Protocol:
    preferred_format: str = "plain"
    supports_memory_query: bool = False
    supports_tool_call: bool = False
    needs_strict_json_prompt: bool = True

    def validate(self):
        if self.preferred_format not in VALID_FORMATS:
            raise ValueError(f"protocol.preferred_format must be one of {VALID_FORMATS}, got '{self.preferred_format}'")


@dataclass
class Runtime:
    default_temperature: float = 0.4
    reasoning_temperature: float = 0.6
    json_temperature: float = 0.1
    max_retries: int = 2


@dataclass
class Roles:
    suitable_for: list[str] = field(default_factory=lambda: ["main_chat"])

    def validate(self):
        for role in self.suitable_for:
            if role not in VALID_ROLES:
                raise ValueError(f"roles.suitable_for contains invalid role '{role}'. Valid: {VALID_ROLES}")


@dataclass
class ModelProfile:
    model_id: str = ""
    family: str | None = None
    size_b: float | None = None
    backend: str | None = None
    capabilities: Capabilities = field(default_factory=Capabilities)
    limits: Limits = field(default_factory=Limits)
    protocol: Protocol = field(default_factory=Protocol)
    runtime: Runtime = field(default_factory=Runtime)
    roles: Roles = field(default_factory=Roles)

    def validate(self):
        """验证所有嵌套字段"""
        if not self.model_id:
            raise ValueError("model_id is required")
        self.capabilities.validate()
        self.limits.validate()
        self.protocol.validate()
        self.roles.validate()
