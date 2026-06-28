"""Tests for web search providers."""
import pytest
from src.web.search_provider import MockWebSearchProvider, create_search_provider
from src.web.models import WebSearchResult


class TestMockWebSearchProvider:
    def setup_method(self):
        self.provider = MockWebSearchProvider()

    def test_search_returns_results(self):
        results = self.provider.search("memoryqwen")
        assert len(results) > 0
        assert isinstance(results[0], WebSearchResult)

    def test_search_python(self):
        results = self.provider.search("python")
        assert len(results) >= 1

    def test_search_max_results(self):
        results = self.provider.search("python", max_results=2)
        assert len(results) <= 2

    def test_search_unknown_query(self):
        results = self.provider.search("xyzabc123nonexistent")
        assert len(results) >= 1  # generic fallback
        assert "xyzabc123nonexistent" in results[0].title.lower() or                "xyzabc123nonexistent" in results[0].snippet.lower()

    def test_empty_query(self):
        results = self.provider.search("")
        assert len(results) == 0

    def test_results_have_url(self):
        results = self.provider.search("memoryqwen")
        for r in results:
            assert r.url, f"Result {r.title} has no URL"

    def test_results_are_ranked(self):
        results = self.provider.search("python", max_results=3)
        ranks = [r.rank for r in results]
        assert ranks == sorted(ranks)


class TestCreateSearchProvider:
    def test_default_mock(self):
        from types import SimpleNamespace
        cfg = SimpleNamespace(web=SimpleNamespace(provider="mock"))
        p = create_search_provider(cfg)
        assert isinstance(p, MockWebSearchProvider)

    def test_explicit_mock(self):
        from types import SimpleNamespace
        cfg = SimpleNamespace(web=SimpleNamespace(provider="mock"))
        p = create_search_provider(cfg)
        assert isinstance(p, MockWebSearchProvider)

    def test_unknown_provider_raises(self):
        from types import SimpleNamespace
        cfg = SimpleNamespace(web=SimpleNamespace(provider="nonexistent"))
        with pytest.raises(ValueError, match="Unknown web search provider"):
            create_search_provider(cfg)

    def test_no_web_config_defaults_to_mock(self):
        from types import SimpleNamespace
        cfg = SimpleNamespace()  # no web attr
        p = create_search_provider(cfg)
        assert isinstance(p, MockWebSearchProvider)
