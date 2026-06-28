"""MemoryQwen — TDR-v1 Token-Difficulty Router.

External token-aware routing: identifies difficulty signals in user
messages and recommends a cognitive path. Does NOT modify the model.
"""

from __future__ import annotations

from .rules import (
    ROUTE_PRIORITY,
    CAPABILITY_TOKENS,
    WEB_TOKENS,
    DEEP_TOKENS,
    JUDGE_TOKENS,
    MANUAL_TOKENS,
)
from .schema import RoutingDecision, TriggerToken, RiskScores


class TokenDifficultyRouter:
    """Route user messages by difficulty signals."""

    def route(
        self,
        user_message: str,
        *,
        capability_detected: bool = False,
        web_need_detected: bool = False,
        has_source_conflict: bool = False,
        unknown_capability: bool = False,
    ) -> RoutingDecision:
        msg = user_message.lower()
        triggers: list[TriggerToken] = []
        scores = RiskScores()

        # 1. Capability tokens
        cap_hits = [t for t in CAPABILITY_TOKENS if t.lower() in msg]
        if cap_hits:
            scores.capability_risk = min(0.5 + 0.1 * len(cap_hits), 1.0)
            for t in cap_hits:
                triggers.append(TriggerToken(t, "capability_risk", f"capability token: {t}"))

        # 2. Web-need tokens
        web_hits = [t for t in WEB_TOKENS if t.lower() in msg]
        if web_hits:
            scores.web_need = min(0.6 + 0.1 * len(web_hits), 1.0)
            for t in web_hits:
                triggers.append(TriggerToken(t, "web_need", f"web signal: {t}"))

        # 3. Deep-suggested tokens
        deep_hits = [t for t in DEEP_TOKENS if t.lower() in msg]
        if deep_hits:
            scores.planning_depth = min(0.5 + 0.1 * len(deep_hits), 1.0)
            scores.model_upgrade_need = 0.5
            scores.version_conflict_risk = 0.4
            for t in deep_hits:
                triggers.append(TriggerToken(t, "planning_depth", f"deep signal: {t}"))

        # 4. Judge-review tokens
        judge_hits = [t for t in JUDGE_TOKENS if t.lower() in msg]
        if judge_hits:
            scores.hallucination_risk = min(0.5 + 0.1 * len(judge_hits), 1.0)
            for t in judge_hits:
                triggers.append(TriggerToken(t, "hallucination_risk", f"judge signal: {t}"))

        # 5. Manual-review tokens
        manual_hits = [t for t in MANUAL_TOKENS if t.lower() in msg]
        if manual_hits:
            scores.source_conflict_risk = min(0.6 + 0.1 * len(manual_hits), 1.0)
            for t in manual_hits:
                triggers.append(TriggerToken(t, "source_conflict_risk", f"conflict signal: {t}"))

        # 6. Input flags
        if capability_detected:
            scores.capability_risk = max(scores.capability_risk, 0.8)
        if web_need_detected:
            scores.web_need = max(scores.web_need, 0.8)
        if has_source_conflict:
            scores.source_conflict_risk = max(scores.source_conflict_risk, 0.8)
        if unknown_capability:
            scores.capability_risk = max(scores.capability_risk, 0.9)
            scores.version_conflict_risk = max(scores.version_conflict_risk, 0.8)

        # 7. Decide route by priority
        route = "shallow"
        reason = "no difficulty signals detected"
        deep_suggested = False
        judge_review = False
        manual_review = False

        # Determine route by highest-priority match
        if unknown_capability or has_source_conflict:
            route = "manual_review"
            manual_review = True
            reason = "unknown_capability" if unknown_capability else "source_conflict"
        elif scores.hallucination_risk >= 0.6:
            route = "judge_review"
            judge_review = True
            reason = f"hallucination_risk_{scores.hallucination_risk:.2f}"
        elif scores.capability_risk >= 0.5:
            route = "capability_registry"
            reason = f"capability_risk_{scores.capability_risk:.2f}"
        elif scores.web_need >= 0.6:
            route = "web"
            reason = f"web_need_{scores.web_need:.2f}"
        elif scores.planning_depth >= 0.5:
            route = "deep_suggested"
            deep_suggested = True
            reason = f"planning_depth_{scores.planning_depth:.2f}"
        elif triggers:
            route = "memory"
            reason = "low_risk_with_signals"

        return RoutingDecision(
            route=route,
            trigger_tokens=triggers,
            risk_scores=scores,
            deep_suggested=deep_suggested,
            judge_review_recommended=judge_review,
            manual_review_required=manual_review,
            reason=reason,
        )
