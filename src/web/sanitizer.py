"""
MemoryQwen — Web content sanitizer.

Extracts clean text from HTML, removes scripts/styles, normalizes whitespace.
"""

from __future__ import annotations

import re

# ── HTML tag removal ────────────────────────────────────────
_SCRIPT_RE = re.compile(r"<script[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
_STYLE_RE = re.compile(r"<style[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_HTML_ENTITY_RE = re.compile(r"&[a-zA-Z]+;|&#\d+;")
_WHITESPACE_RE = re.compile(r"\s+")
_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.DOTALL | re.IGNORECASE)


def html_to_text(html: str) -> str:
    """Convert HTML to clean plain text.

    Removes scripts, styles, HTML tags, entities. Collapses whitespace.
    """
    if not html:
        return ""

    text = html
    # Remove scripts and styles
    text = _SCRIPT_RE.sub(" ", text)
    text = _STYLE_RE.sub(" ", text)
    # Remove remaining HTML tags
    text = _HTML_TAG_RE.sub(" ", text)
    # Decode common HTML entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&apos;", "'")
    text = text.replace("&nbsp;", " ")
    text = _HTML_ENTITY_RE.sub(" ", text)
    # Collapse whitespace
    text = _WHITESPACE_RE.sub(" ", text).strip()

    return text


def extract_title(html: str, fallback_url: str = "") -> str:
    """Extract the <title> from HTML, or return fallback."""
    if not html:
        return fallback_url or "Untitled"

    m = _TITLE_RE.search(html)
    if m:
        title = html_to_text(m.group(1)).strip()
        if title:
            return title

    # Try Markdown-style H1
    m = re.search(r"^#\s+(.+)$", html, re.MULTILINE)
    if m:
        return m.group(1).strip()

    return fallback_url or "Untitled"


def truncate_text(text: str, max_chars: int) -> tuple[str, bool]:
    """Truncate text to max_chars. Returns (truncated_text, was_truncated)."""
    if len(text) <= max_chars:
        return text, False
    return text[:max_chars], True


def strip_noise(text: str) -> str:
    """Remove common web noise: navigation text, footer boilerplate, etc."""
    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove leading/trailing whitespace per line
    lines = [line.strip() for line in text.split("\n")]
    # Remove empty lines at start/end
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)
