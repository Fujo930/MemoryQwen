"""ACE-v1 security contract tests."""

from src.ace import ACEController


class TestACESecurity:
    def setup_method(self):
        self.ctrl = ACEController()

    def test_never_auto_web(self):
        d = self.ctrl.decide("latest news", web_requested=False, web_enabled=False)
        assert not d.context_plan.use_web_context

    def test_never_auto_deep(self):
        d = self.ctrl.decide("规划架构", deep_requested=False)
        assert d.model_plan.deep_suggested
        assert not d.model_plan.auto_escalated
        assert d.model_plan.selected_model_role == "daily"

    def test_never_auto_escalate_14b(self):
        for q in ["规划", "架构", "算法", "设计"]:
            d = self.ctrl.decide(q, deep_requested=False)
            assert d.model_plan.selected_model_role == "daily"
            assert not d.model_plan.auto_escalated

    def test_registry_not_overridden_by_old_docs(self):
        d = self.ctrl.decide("支持 PDF 吗", capability_detected=True)
        assert d.context_plan.use_capability_registry

    def test_registry_not_overridden_by_web(self):
        d = self.ctrl.decide("支持 Web UI 吗", capability_detected=True)
        assert d.context_plan.use_capability_registry
        assert not d.context_plan.use_web_context

    def test_guard_always_enabled_all_routes(self):
        """Guard must be enabled regardless of route."""
        for q in ["你好", "支持PDF吗", "规划算法", "最新的新闻", "fake CLI"]:
            d = self.ctrl.decide(q)
            assert d.context_plan.use_guard is True, f"Guard disabled for: {q}"

    def test_routing_in_decision(self):
        d = self.ctrl.decide("你好")
        assert "route" in d.routing

    def test_ace_decision_reasons_captured(self):
        d = self.ctrl.decide("规划架构")
        assert len(d.reasons) > 0

    def test_invalid_input_not_crash(self):
        d = self.ctrl.decide("")
        assert d.route == "shallow"
