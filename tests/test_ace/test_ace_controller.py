from src.ace import ACEController

class TestACEController:
    def setup_method(self):
        self.ctrl = ACEController()

    def test_shallow(self):
        d = self.ctrl.decide("你好")
        assert d.route == "shallow"
        assert not d.context_plan.use_memory_retrieval
        assert not d.model_plan.deep_suggested

    def test_capability_registry(self):
        d = self.ctrl.decide("你可以联网吗")
        assert d.route == "capability_registry"
        assert d.context_plan.use_capability_registry
        assert d.context_plan.include_registry_context

    def test_memory(self):
        d = self.ctrl.decide("GPU Guardian 是什么")
        assert d.route in ("memory", "shallow")
        assert d.model_plan.selected_model_role == "daily"

    def test_web_with_web_disabled(self):
        d = self.ctrl.decide("最新的 AI 新闻", web_requested=False, web_enabled=False)
        assert d.route == "web"
        assert not d.context_plan.use_web_context

    def test_web_with_web_requested(self):
        d = self.ctrl.decide("最新的 AI 新闻", web_requested=True, web_enabled=False)
        assert d.context_plan.use_web_context

    def test_deep_suggested_no_auto_escalate(self):
        d = self.ctrl.decide("帮我规划架构", deep_requested=False)
        assert d.route == "deep_suggested"
        assert d.model_plan.deep_suggested
        assert not d.model_plan.auto_escalated
        assert d.model_plan.selected_model_role == "daily"

    def test_deep_requested_uses_deep_role(self):
        d = self.ctrl.decide("帮我规划架构", deep_requested=True)
        assert d.model_plan.selected_model_role == "deep"
        assert d.model_plan.requested_mode == "deep"

    def test_judge_review(self):
        d = self.ctrl.decide("wrong_answer 当事实用")
        assert d.route in ("judge_review", "capability_registry", "memory")
        if d.route == "judge_review":
            assert d.review_plan.judge_review_recommended

    def test_manual_review(self):
        d = self.ctrl.decide("冲突", has_source_conflict=True)
        assert d.route == "manual_review"
        assert d.review_plan.manual_review_required

    def test_registry_priority(self):
        d = self.ctrl.decide("支持 PDF 吗", capability_detected=True)
        assert d.context_plan.use_capability_registry

    def test_base_mode_uses_7b(self):
        d = self.ctrl.decide("你好")
        assert d.model_plan.selected_model == "qwen2.5:7b"

    def test_deep_mode_uses_14b(self):
        d = self.ctrl.decide("规划", deep_requested=True)
        assert d.model_plan.selected_model == "qwen2.5:14b"

    def test_metadata_present(self):
        d = self.ctrl.decide("你好")
        assert d.context_plan.use_guard is True
        assert d.model_plan.selected_model_role == "daily"

    def test_guard_always_enabled(self):
        for q in ["你好", "支持PDF吗", "规划"]:
            d = self.ctrl.decide(q)
            assert d.context_plan.use_guard is True
