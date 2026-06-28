"""Tests for WebNeedDetector."""
import pytest
from src.web.web_need_detector import WebNeedDetector, WebNeedDecision


class TestWebNeedDetector:
    def setup_method(self):
        self.detector = WebNeedDetector()

    def test_web_disabled_never_queries(self):
        d = self.detector.should_use_web("latest AI news", web_enabled=False)
        assert d.should_query_web is False
        assert d.reason == "web_not_enabled"

    def test_latest_with_web_enabled_queries(self):
        d = self.detector.should_use_web("what is the latest AI news?", web_enabled=True)
        assert d.should_query_web is True
        assert "web_signal" in d.reason

    def test_current_news_with_web_enabled_queries(self):
        d = self.detector.should_use_web("current stock price of Apple", web_enabled=True)
        assert d.should_query_web is True

    def test_explicit_search_queries(self):
        d = self.detector.should_use_web("搜索 Qwen2.5 最新 release", web_enabled=True)
        assert d.should_query_web is True

    def test_local_project_question_no_web(self):
        d = self.detector.should_use_web("MemoryQwen 支持什么功能？", web_enabled=True)
        assert d.should_query_web is False
        assert "local" in d.reason.lower()

    def test_capability_boundary_no_web_by_default(self):
        d = self.detector.should_use_web("支持 PDF 吗？", web_enabled=True)
        assert d.should_query_web is False

    def test_no_signal_no_web(self):
        d = self.detector.should_use_web("hello how are you", web_enabled=True)
        assert d.should_query_web is False
        assert "no_web_signal" in d.reason

    def test_web_keyword_queries(self):
        d = self.detector.should_use_web("联网查一下", web_enabled=True)
        assert d.should_query_web is True
