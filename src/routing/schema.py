"""MemoryQwen — TDR-v1 routing schema."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TriggerToken:
    token: str
    risk_type: str
    reason: str = ""


@dataclass
class RiskScores:
    capability_risk: float = 0.0
    version_conflict_risk: float = 0.0
    web_need: float = 0.0
    source_conflict_risk: float = 0.0
    planning_depth: float = 0.0
    model_upgrade_need: float = 0.0
    hallucination_risk: float = 0.0


@dataclass
class RoutingDecision:
    route: str = "shallow"
    trigger_tokens: list[TriggerToken] = field(default_factory=list)
    risk_scores: RiskScores = field(default_factory=RiskScores)
    deep_suggested: bool = False
    judge_review_recommended: bool = False
    manual_review_required: bool = False
    reason: str = ""


VALID_ROUTES = frozenset({
    "shallow",
    "capability_registry",
    "memory",
    "web",
    "deep_suggested",
    "judge_review",
    "manual_review",
})
