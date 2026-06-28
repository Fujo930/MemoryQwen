"""Tests for CapabilityNeedDetector."""
import pytest
from src.agent.capability_need_detector import CapabilityNeedDetector


class TestCapabilityNeedDetector:
    def setup_method(self):
        self.detector = CapabilityNeedDetector()

    def test_capability_question_triggered(self):
        r = self.detector.detect("你可以联网吗")
        assert r.is_capability_question is True

    def test_web_ui_question(self):
        r = self.detector.detect("MemoryQwen 有 Web UI 吗")
        assert r.is_capability_question is True

    def test_pdf_question(self):
        r = self.detector.detect("支持PDF吗")
        assert r.is_capability_question is True

    def test_deep_mode_question(self):
        r = self.detector.detect("14B是默认模型吗")
        assert r.is_capability_question is True

    def test_short_capability_question_high_confidence(self):
        r = self.detector.detect("能联网吗")
        assert r.is_capability_question
        assert r.confidence >= 0.9

    def test_non_capability_question(self):
        r = self.detector.detect("hello")
        assert r.is_capability_question is False

    def test_greeting_not_capability(self):
        r = self.detector.detect("你好")
        assert r.is_capability_question is False

    def test_matched_keywords(self):
        r = self.detector.detect("可以联网吗？支持PDF吗？")
        assert "支持" in r.matched_keywords or "联网" in r.matched_keywords
        assert r.confidence > 0.5
