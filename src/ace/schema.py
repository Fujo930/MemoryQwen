"""ACE-v1 — Adaptive Cognitive Exoskeleton schema."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextPlan:
    use_capability_registry: bool = False
    use_memory_retrieval: bool = False
    use_web_context: bool = False
    use_guard: bool = True
    include_routing_metadata: bool = True
    include_registry_context: bool = False
    include_web_safety_context: bool = False
    include_deep_mode_hint: bool = False
    include_anaphora_skip: bool = False


@dataclass
class ModelPlan:
    requested_mode: str = "default"
    selected_model_role: str = "daily"
    selected_model: str | None = None
    deep_suggested: bool = False
    auto_escalated: bool = False
    fallback_used: bool = False


@dataclass
class ReviewPlan:
    judge_review_recommended: bool = False
    manual_review_required: bool = False
    reason: str = ""


@dataclass
class ACEDecision:
    route: str = "shallow"
    context_plan: ContextPlan = field(default_factory=ContextPlan)
    model_plan: ModelPlan = field(default_factory=ModelPlan)
    review_plan: ReviewPlan = field(default_factory=ReviewPlan)
    routing: dict[str, Any] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
