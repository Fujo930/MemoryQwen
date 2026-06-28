"""
MemoryQwen — Web module (v0.1.5 Internet Query).

Controlled web access: search, fetch, ask, ingest.
Not a crawler. Not automatic. Safety-first.
"""

from src.web.models import (
    WebSearchResult,
    WebFetchedDocument,
    WebSource,
    WebQueryResult,
)
from src.web.fetcher import WebFetcher
from src.web.sanitizer import html_to_text, extract_title
from src.web.search_provider import (
    WebSearchProvider,
    MockWebSearchProvider,
    create_search_provider,
)
from src.web.safety import validate_url, detect_prompt_injection
from src.web.web_context import (
    build_web_context,
    build_web_search_display,
    mark_web_untrusted,
    assign_source_ids,
)

__all__ = [
    "WebSearchResult",
    "WebFetchedDocument",
    "WebSource",
    "WebQueryResult",
    "WebFetcher",
    "html_to_text",
    "extract_title",
    "WebSearchProvider",
    "MockWebSearchProvider",
    "create_search_provider",
    "validate_url",
    "detect_prompt_injection",
    "build_web_context",
    "build_web_search_display",
    "mark_web_untrusted",
    "assign_source_ids",
]
