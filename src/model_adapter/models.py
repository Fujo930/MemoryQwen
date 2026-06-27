"""
MemoryQwen — AutoModelAdapter 数据模型
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EvalCase:
    """评估用例"""
    case_id: str
    category: str                      # json_stability | chinese | tool_calling | reasoning | long_context
    messages: list[dict]               # [{"role":..., "content":...}]
    temperature: float = 0.1
    max_tokens: int = 256
    metadata: dict = field(default_factory=dict)


@dataclass
class EvalCaseResult:
    """单条评估结果"""
    case_id: str = ""
    category: str = ""
    passed: bool = False
    score: float = 0.0
    raw_output: str = ""
    reason: str | None = None


@dataclass
class EvalReport:
    """完整评估报告"""
    model_id: str = ""
    results: list[EvalCaseResult] = field(default_factory=list)
    capability_scores: dict[str, float] = field(default_factory=dict)
    recommended_roles: list[str] = field(default_factory=list)
    preferred_format: str = "plain"
    metadata: dict = field(default_factory=dict)
