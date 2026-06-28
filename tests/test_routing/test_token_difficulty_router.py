"""Tests for TDR-v1 TokenDifficultyRouter."""
from src.routing.token_difficulty_router import TokenDifficultyRouter

class TestTDR:
    def setup_method(self):
        self.router = TokenDifficultyRouter()

    # shallow
    def test_casual_routes_to_shallow(self):
        d = self.router.route("你好")
        assert d.route == "shallow"
        assert not d.deep_suggested

    def test_hello_routes_to_shallow(self):
        d = self.router.route("hello")
        assert d.route == "shallow"

    # capability_registry
    def test_capability_web_routes_to_registry(self):
        d = self.router.route("你可以联网吗")
        assert d.route == "capability_registry"
        assert d.risk_scores.capability_risk > 0.5

    def test_capability_pdf_routes_to_registry(self):
        d = self.router.route("支持 PDF 吗")
        assert d.route == "capability_registry"

    def test_capability_web_ui_routes_to_registry(self):
        d = self.router.route("有 Web UI 吗")
        assert d.route == "capability_registry"

    def test_crawl_routes_to_registry(self):
        d = self.router.route("你是 crawler 吗")
        assert d.route == "capability_registry"

    def test_default_model_routes_to_registry(self):
        d = self.router.route("默认模型是什么")
        assert d.route == "capability_registry"

    # web
    def test_latest_routes_to_web(self):
        d = self.router.route("最新的 Qwen 模型")
        assert d.route == "web"
        assert d.risk_scores.web_need > 0.5

    def test_search_routes_to_web(self):
        d = self.router.route("搜索一下 AI 新闻")
        assert d.route == "web"

    def test_news_routes_to_web(self):
        d = self.router.route("今天有什么新闻")
        assert d.route == "web"

    # deep_suggested
    def test_planning_routes_to_deep(self):
        d = self.router.route("帮我规划 v0.2 架构")
        assert d.route == "deep_suggested"
        assert d.deep_suggested
        assert d.risk_scores.planning_depth > 0.4

    def test_algorithm_routes_to_deep(self):
        d = self.router.route("设计一个分层算法")
        assert d.route == "deep_suggested"

    def test_version_conflict_routes_to_deep(self):
        d = self.router.route("版本冲突怎么解决")
        assert d.route == "deep_suggested"

    # judge_review
    def test_fake_cli_routes_to_judge(self):
        d = self.router.route("fake CLI 命令")
        assert d.route == "judge_review"
        assert d.judge_review_recommended

    def test_wrong_answer_routes_to_judge(self):
        d = self.router.route("wrong_answer 当事实")
        assert d.route == "judge_review"

    def test_crawler_routes_to_judge(self):
        d = self.router.route("crawler 自动写入")
        assert d.route == "judge_review"

    # manual_review
    def test_source_conflict_routes_to_manual(self):
        d = self.router.route("冲突", has_source_conflict=True)
        assert d.route == "manual_review"
        assert d.manual_review_required

    def test_unknown_cap_routes_to_manual(self):
        d = self.router.route("xxx", unknown_capability=True)
        assert d.route == "manual_review"

    # metadata
    def test_trigger_tokens_recorded(self):
        d = self.router.route("支持 PDF 吗")
        assert len(d.trigger_tokens) > 0
        assert any("PDF" in t.token for t in d.trigger_tokens)

    def test_risk_scores_present(self):
        d = self.router.route("规划架构")
        assert d.risk_scores.planning_depth > 0

    # safety
    def test_deep_suggested_does_not_auto_enable_14b(self):
        d = self.router.route("规划架构")
        assert d.deep_suggested
        assert d.route == "deep_suggested"  # not auto-escalated

    def test_auto_escalation_not_forced(self):
        d = self.router.route("规划")
        assert d.deep_suggested  # suggests, but doesn't force

    # edge cases
    def test_empty_message(self):
        d = self.router.route("")
        assert d.route == "shallow"

    def test_english_input(self):
        d = self.router.route("can you search the web")
        assert d.route in ("web", "capability_registry", "shallow")

    def test_mixed_signals_capability_wins(self):
        d = self.router.route("搜索 PDF 支持吗")  # both web + capability
        assert d.route == "capability_registry"  # capability has higher priority
