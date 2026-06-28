"""Tests for web module data models."""
import pytest
from src.web.models import WebSearchResult, WebFetchedDocument, WebSource, WebQueryResult


class TestWebSearchResult:
    def test_create_minimal(self):
        r = WebSearchResult(title="T", url="https://x.com")
        assert r.title == "T"
        assert r.url == "https://x.com"
        assert r.snippet is None
        assert r.rank == 0

    def test_create_full(self):
        r = WebSearchResult(title="T", url="https://x.com", snippet="s", source="mock", rank=3)
        assert r.snippet == "s"
        assert r.source == "mock"
        assert r.rank == 3


class TestWebFetchedDocument:
    def test_create_success(self):
        d = WebFetchedDocument(url="https://x.com", title="T", text="hello world",
                                fetched_at="2026-01-01T00:00:00Z",
                                content_type="text/html", status_code=200,
                                word_count=2, truncated=False)
        assert d.url == "https://x.com"
        assert d.title == "T"
        assert d.text == "hello world"
        assert d.word_count == 2
        assert d.truncated is False
        assert d.error is None

    def test_create_error(self):
        d = WebFetchedDocument(url="https://x.com", error="timeout")
        assert d.error == "timeout"
        assert d.text == ""


class TestWebSource:
    def test_assign_source_id(self):
        s = WebSource(source_id="W1", title="T", url="https://x.com", text="hello")
        assert s.source_id == "W1"
        assert s.trusted is False

    def test_trusted_default_false(self):
        s = WebSource(title="T", url="https://x.com", text="h")
        assert s.trusted is False


class TestWebQueryResult:
    def test_empty_result(self):
        r = WebQueryResult(query="test")
        assert r.query == "test"
        assert r.sources == []
        assert r.warnings == []
        assert r.elapsed_ms == 0

    def test_with_sources(self):
        s = WebSource(source_id="W1", title="T", url="https://x.com", text="h")
        r = WebQueryResult(query="test", sources=[s], elapsed_ms=150)
        assert len(r.sources) == 1
        assert r.elapsed_ms == 150
