"""Tests for web context builder."""
import pytest
from src.web.web_context import (
    assign_source_ids, build_web_context, build_web_search_display,
    mark_web_untrusted
)
from src.web.models import WebSource


class TestAssignSourceIds:
    def test_assigns_W1_W2_W3(self):
        sources = [
            WebSource(title="A", url="https://a.com", text="a"),
            WebSource(title="B", url="https://b.com", text="b"),
            WebSource(title="C", url="https://c.com", text="c"),
        ]
        result = assign_source_ids(sources)
        assert result[0].source_id == "W1"
        assert result[1].source_id == "W2"
        assert result[2].source_id == "W3"

    def test_empty_list(self):
        assert assign_source_ids([]) == []


class TestBuildWebContext:
    def test_empty_sources(self):
        result = build_web_context([])
        assert result == ""

    def test_includes_W_id(self):
        sources = [WebSource(title="Test", url="https://t.com", text="content",
                              fetched_at="2026-01-01T00:00:00Z")]
        result = build_web_context(sources)
        assert "[W1]" in result

    def test_includes_url(self):
        sources = [WebSource(title="Test", url="https://example.com/page",
                              text="content", fetched_at="2026-01-01T00:00:00Z")]
        result = build_web_context(sources)
        assert "https://example.com/page" in result

    def test_includes_fetched_at(self):
        sources = [WebSource(title="Test", url="https://t.com", text="c",
                              fetched_at="2026-06-27T12:00:00Z")]
        result = build_web_context(sources)
        assert "2026-06-27T12:00:00Z" in result

    def test_marks_web_untrusted(self):
        sources = [WebSource(title="T", url="https://t.com", text="c",
                              fetched_at="2026-01-01T00:00:00Z")]
        result = build_web_context(sources)
        assert "untrusted" in result.lower()

    def test_truncates_long_content(self):
        sources = [WebSource(title="T", url="https://t.com", text="x" * 2000,
                              fetched_at="2026-01-01T00:00:00Z")]
        result = build_web_context(sources, max_per_source_chars=100)
        # Should contain "..." at truncation point
        assert "..." in result

    def test_includes_content_text(self):
        sources = [WebSource(title="T", url="https://t.com", text="hello unique text 12345",
                              fetched_at="2026-01-01T00:00:00Z")]
        result = build_web_context(sources)
        assert "hello unique text 12345" in result


class TestBuildWebSearchDisplay:
    def test_empty_results(self):
        result = build_web_search_display([])
        assert "No web results" in result or "no" in result.lower()

    def test_includes_urls(self):
        sources = [WebSource(title="Test", url="https://example.com", text="c",
                              snippet="A test result")]
        result = build_web_search_display(sources)
        assert "https://example.com" in result

    def test_includes_snippet(self):
        sources = [WebSource(title="T", url="https://t.com", snippet="my snippet", text="c")]
        result = build_web_search_display(sources)
        assert "my snippet" in result


class TestMarkWebUntrusted:
    def test_returns_notice(self):
        notice = mark_web_untrusted()
        assert "untrusted" in notice.lower()
        assert "[W1]" in notice
