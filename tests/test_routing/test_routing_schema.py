"""Tests for TDR-v1 routing schema."""
from src.routing.schema import RoutingDecision, TriggerToken, RiskScores

class TestRoutingSchema:
    def test_decision_defaults(self):
        d = RoutingDecision()
        assert d.route == "shallow"
        assert not d.deep_suggested
        assert not d.judge_review_recommended
        assert not d.manual_review_required

    def test_trigger_token_fields(self):
        tt = TriggerToken("test", "risk", "reason")
        assert tt.token == "test"
        assert tt.risk_type == "risk"
        assert tt.reason == "reason"

    def test_risk_scores_defaults(self):
        rs = RiskScores()
        assert rs.capability_risk == 0.0
        assert rs.hallucination_risk == 0.0

    def test_decision_with_tokens(self):
        d = RoutingDecision(
            route="capability_registry",
            trigger_tokens=[TriggerToken("联网", "capability_risk")],
            deep_suggested=False,
        )
        assert len(d.trigger_tokens) == 1
        assert d.route == "capability_registry"
