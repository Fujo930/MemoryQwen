"""
MemoryQwen — Web module data models.

Defines the core types for Internet Query: search results, fetched
documents, web sources, and query results.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WebSearchResult:
    """A single search result from a web search provider."""
    title: str
    url: str
    snippet: str | None = None
    source: str | None = None    # provider name (e.g. "mock", "duckduckgo")
    rank: int = 0


@dataclass
class WebFetchedDocument:
    """A fetched and sanitized web document."""
    url: str
    title: str | None = None
    text: str = ""
    fetched_at: str = ""
    content_type: str | None = None
    status_code: int | None = None
    word_count: int = 0
    truncated: bool = False
    error: str | None = None


@dataclass
class WebSource:
    """A web source ready for prompt context, assigned a [W] citation ID."""
    source_id: str = ""           # W1, W2, W3, ...
    title: str = ""
    url: str = ""
    snippet: str | None = None
    text: str = ""
    fetched_at: str = ""
    rank: int = 0
    trusted: bool = False         # always False for web content


@dataclass
class WebQueryResult:
    """Result of a web query (search + optional fetch)."""
    query: str
    sources: list[WebSource] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    elapsed_ms: int = 0
    error: str | None = None
