"""ACE-v1 Controller — unified cognitive exoskeleton decision engine."""

from __future__ import annotations
from .schema import ContextPlan, ModelPlan, ReviewPlan, ACEDecision


class ACEController:
    """Central cognitive scheduler for MemoryQwen v0.2.

    Takes user message + system flags → produces a unified decision
    covering context plan, model plan, and review plan.
    """

    def __init__(self):
        self._default_model = "qwen2.5:7b"
        self._deep_model = "qwen2.5:14b"

    def decide(
        self,
        user_message: str,
        *,
        deep_requested: bool = False,
        web_requested: bool = False,
        web_enabled: bool = False,
        capability_detected: bool = False,
        web_need_detected: bool = False,
        has_source_conflict: bool = False,
        unknown_capability: bool = False,
    ) -> ACEDecision:
        # 1. Get TDR-v1 route
        from src.routing import TokenDifficultyRouter
        tdr = TokenDifficultyRouter()
        routing = tdr.route(
            user_message,
            capability_detected=capability_detected,
            web_need_detected=web_need_detected,
            has_source_conflict=has_source_conflict,
            unknown_capability=unknown_capability,
        )

        # 2. Build context plan from route
        cp = ContextPlan()
        reasons: list[str] = []

        if routing.route == "shallow":
            cp.use_capability_registry = False
            cp.use_memory_retrieval = False
            cp.use_web_context = False
            reasons.append("Shallow route: fast casual response, no retrieval needed.")

        elif routing.route == "capability_registry":
            cp.use_capability_registry = True
            cp.include_registry_context = True
            cp.use_memory_retrieval = False
            cp.use_web_context = False
            reasons.append("Capability route: query Registry as authority source.")

        elif routing.route == "memory":
            cp.use_memory_retrieval = True
            reasons.append("Memory route: retrieve from local knowledge store.")

        elif routing.route == "web":
            cp.use_web_context = web_requested or web_enabled
            cp.include_web_safety_context = cp.use_web_context
            if not cp.use_web_context:
                reasons.append("Web route detected but web is disabled. Marking web_needed_but_disabled.")
            else:
                reasons.append("Web route: use web evidence as temporary context.")

        elif routing.route == "deep_suggested":
            cp.include_deep_mode_hint = True
            cp.use_memory_retrieval = True
            reasons.append("Deep suggested: complex planning detected. Use --deep for better reasoning.")

        elif routing.route == "judge_review":
            cp.use_guard = True
            reasons.append("Judge review: high hallucination risk detected. Verify answer carefully.")

        elif routing.route == "manual_review":
            cp.use_capability_registry = True
            cp.include_registry_context = True
            reasons.append("Manual review: conflicting sources. Registry is authoritative.")

        # 3. Model plan
        mp = ModelPlan()
        mp.deep_suggested = routing.deep_suggested
        mp.requested_mode = "deep" if deep_requested else "default"
        mp.selected_model_role = "deep" if deep_requested else "daily"
        mp.selected_model = self._deep_model if deep_requested else self._default_model
        mp.auto_escalated = False  # Never auto-escalate

        # 4. Review plan
        rp = ReviewPlan()
        rp.judge_review_recommended = routing.judge_review_recommended
        rp.manual_review_required = routing.manual_review_required
        rp.reason = routing.reason

        return ACEDecision(
            route=routing.route,
            context_plan=cp,
            model_plan=mp,
            review_plan=rp,
            routing={
                "route": routing.route,
                "trigger_tokens": [{"token": t.token, "risk_type": t.risk_type} for t in routing.trigger_tokens],
                "risk_scores": {k: getattr(routing.risk_scores, k) for k in vars(routing.risk_scores)},
                "deep_suggested": routing.deep_suggested,
                "judge_review_recommended": routing.judge_review_recommended,
                "manual_review_required": routing.manual_review_required,
            },
            reasons=reasons,
        )
