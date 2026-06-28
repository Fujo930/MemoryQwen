from src.ace.schema import ACEDecision, ContextPlan, ModelPlan, ReviewPlan

class TestACESchema:
    def test_defaults(self):
        d = ACEDecision()
        assert d.route == "shallow"
        assert not d.context_plan.use_capability_registry
        assert not d.model_plan.deep_suggested
        assert not d.review_plan.manual_review_required

    def test_serializable(self):
        d = ACEDecision(route="test", reasons=["a", "b"])
        data = {"route": d.route, "reasons": d.reasons}
        assert data["route"] == "test"

    def test_context_plan_defaults(self):
        cp = ContextPlan()
        assert not cp.use_capability_registry
        assert cp.use_guard is True

    def test_model_plan_defaults(self):
        mp = ModelPlan()
        assert mp.selected_model_role == "daily"
        assert not mp.auto_escalated

    def test_review_plan_defaults(self):
        rp = ReviewPlan()
        assert not rp.judge_review_recommended
