"""
MemoryQwen — Web search provider abstraction.

Provides a Protocol for web search and a MockWebSearchProvider for testing.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.web.models import WebSearchResult


# ── Mock results database ────────────────────────────────────
_MOCK_SEARCH_DB: dict[str, list[WebSearchResult]] = {
    "memoryqwen": [
        WebSearchResult(
            title="MemoryQwen — Local AI Agent",
            url="https://github.com/Fujo930/MemoryQwen",
            snippet="MemoryQwen is a local AI agent system that runs entirely on your computer. "
                     "No cloud, all data stays local.",
            source="mock",
            rank=1,
        ),
        WebSearchResult(
            title="MemoryQwen v0.1 Release Notes",
            url="https://github.com/Fujo930/MemoryQwen/releases",
            snippet="v0.1 Developer Preview: CLI chat, BM25 retrieval, error learning, GPU guardian.",
            source="mock",
            rank=2,
        ),
    ],
    "python": [
        WebSearchResult(
            title="Welcome to Python.org",
            url="https://www.python.org/",
            snippet="The official home of the Python Programming Language.",
            source="mock",
            rank=1,
        ),
        WebSearchResult(
            title="Python 3.12 Documentation",
            url="https://docs.python.org/3.12/",
            snippet="Official Python 3.12 documentation.",
            source="mock",
            rank=2,
        ),
        WebSearchResult(
            title="Python Package Index",
            url="https://pypi.org/",
            snippet="Find, install and publish Python packages with the Python Package Index.",
            source="mock",
            rank=3,
        ),
    ],
}


@runtime_checkable
class WebSearchProvider(Protocol):
    """Protocol for web search providers.

    Implementations:
      - MockWebSearchProvider (testing)
      - ConfiguredHttpSearchProvider (real, requires config)
    """

    def search(self, query: str, max_results: int = 5) -> list[WebSearchResult]:
        """Search the web and return results."""
        ...


class MockWebSearchProvider:
    """Mock search provider for testing. Returns fake results from a static DB.

    Does NOT make real HTTP requests. Safe for pytest.
    """

    def search(self, query: str, max_results: int = 5) -> list[WebSearchResult]:
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        results: list[WebSearchResult] = []

        # Try exact match first, then substring
        for key, entries in _MOCK_SEARCH_DB.items():
            if key in query_lower or query_lower in key:
                results.extend(entries[:max_results])
                break

        # If no match, return a generic result
        if not results and query_lower:
            results.append(WebSearchResult(
                title=f"Search results for: {query}",
                url=f"https://example.com/search?q={query.replace(' ', '+')}",
                snippet=f"Mock search result for '{query}'. This is a test placeholder.",
                source="mock",
                rank=1,
            ))

        return results[:max_results]


class ConfiguredHttpSearchProvider:
    """Real HTTP search provider. Wired via config.

    Placeholder — actual implementation depends on chosen search API.
    Raises NotImplementedError until configured.
    """

    def search(self, query: str, max_results: int = 5) -> list[WebSearchResult]:
        raise NotImplementedError(
            "ConfiguredHttpSearchProvider not yet implemented. "
            "Set web.provider to a real search backend."
        )


def create_search_provider(config) -> WebSearchProvider:
    """Factory: create a search provider from config."""
    provider_name = getattr(config.web, "provider", "mock") if config and hasattr(config, "web") else "mock"

    if provider_name == "mock":
        return MockWebSearchProvider()

    if provider_name == "http":
        return ConfiguredHttpSearchProvider()

    raise ValueError(f"Unknown web search provider: {provider_name}")
