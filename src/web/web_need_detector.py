"""
MemoryQwen — Web Need Detector.

Heuristic: detects whether a user question likely needs web access
based on keyword signals and question category.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ── Web signal keywords ─────────────────────────────────────
_WEB_SIGNAL_KEYWORDS: list[str] = [
    "最新", "今天", "现在", "最近",
    "current", "latest", "news", "today",
    "price", "stock", "weather", "release",
    "after 2025",
    "官网", "查一下", "搜索", "联网", "网上",
    "internet", "web",
    "breaking", "trending",
    "what's new", "what is new",
]

# ── Local-only question patterns (override web signal) ──────
_LOCAL_ONLY_INDICATORS: list[str] = [
    "memoryqwen", "capability", "guardian", "gpu",
    "task runtime", "job runner", "ingest",
    "source archive", "error store", "strategy store",
    "pytest", "training", "eval", "embedding",
]


@dataclass
class WebNeedDecision:
    """Result of web-need detection."""
    should_query_web: bool = False
    reason: str = ""
    confidence: float = 0.0


class WebNeedDetector:
    """Detect whether a user question needs web access.

    Rules:
      - web_enabled=False: never query web
      - web_enabled=True:
        - local project questions → no web
        - explicit latest/news/search signals → query web
        - otherwise → no web (conservative)
    """

    def should_use_web(self, user_message: str, web_enabled: bool) -> WebNeedDecision:
        # Rule 1: web disabled → never
        if not web_enabled:
            return WebNeedDecision(
                should_query_web=False,
                reason="web_not_enabled",
                confidence=1.0,
            )

        msg_lower = user_message.lower().strip()

        # Rule 2: local project questions → skip web
        local_count = sum(1 for kw in _LOCAL_ONLY_INDICATORS if kw in msg_lower)
        if local_count >= 1:
            # But if explicit search request, override
            if any(kw in msg_lower for kw in ["搜索", "查一下", "联网", "search", "web", "internet"]):
                return WebNeedDecision(
                    should_query_web=True,
                    reason="explicit_web_search_request",
                    confidence=0.9,
                )
            return WebNeedDecision(
                should_query_web=False,
                reason="local_project_question",
                confidence=0.85,
            )

        # Rule 3: explicit latest/news/search signals → query web
        signal_hits = [kw for kw in _WEB_SIGNAL_KEYWORDS if kw in msg_lower]
        if signal_hits:
            return WebNeedDecision(
                should_query_web=True,
                reason=f"web_signal_detected: {','.join(signal_hits[:3])}",
                confidence=min(0.5 + 0.1 * len(signal_hits), 1.0),
            )

        # Rule 4: default — don't query, user explicitly passed --web but no signal
        return WebNeedDecision(
            should_query_web=False,
            reason="no_web_signal_detected_in_query",
            confidence=0.7,
        )
