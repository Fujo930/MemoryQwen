"""
MemoryQwen — Web fetcher: fetch and download web pages with safety constraints.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from urllib.parse import urlparse

from src.web.models import WebFetchedDocument
from src.web.safety import validate_url, detect_prompt_injection


class WebFetcher:
    """Fetch web pages with safety constraints.

    - Only http/https
    - Blocks private IPs by default
    - Enforces timeout, max bytes, max chars
    - Only accepts text content types
    """

    def __init__(
        self,
        timeout: int = 10,
        max_bytes: int = 500_000,
        max_chars: int = 12_000,
        user_agent: str = "MemoryQwen/0.1.5",
        allow_private: bool = False,
    ):
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.max_chars = max_chars
        self.user_agent = user_agent
        self.allow_private = allow_private

    # ── URL validation ───────────────────────────────────────

    def _check_url(self, url: str) -> str | None:
        """Validate URL. Returns error string or None."""
        is_safe, error = validate_url(url, allow_private=self.allow_private)
        if not is_safe:
            return error or "URL rejected"
        return None

    def _check_content_type(self, content_type: str | None) -> str | None:
        """Validate content type. Returns error string or None."""
        if not content_type:
            return None  # no content-type header — allow, might be text
        ct = content_type.lower().split(";")[0].strip()
        allowed = {"text/html", "text/plain", "application/json",
                    "text/markdown", "text/csv", "application/xml", "text/xml"}
        if ct not in allowed:
            return f"content type '{ct}' not allowed (text only)"
        return None

    # ── Main fetch ───────────────────────────────────────────

    def fetch(self, url: str) -> WebFetchedDocument:
        """Fetch a URL and return a sanitized document.

        On error, returns a WebFetchedDocument with error set (never raises).
        """
        start = time.monotonic()

        # Safety: validate URL
        url_error = self._check_url(url)
        if url_error:
            return WebFetchedDocument(
                url=url,
                error=url_error,
                fetched_at=datetime.now(timezone.utc).isoformat(),
            )

        # Attempt HTTP fetch
        try:
            import urllib.request

            req = urllib.request.Request(url)
            req.add_header("User-Agent", self.user_agent)
            req.add_header("Accept", "text/html, text/plain, application/json, text/*")

            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status_code = resp.getcode()
                content_type = resp.headers.get("Content-Type", "")

                # Check content type
                ct_error = self._check_content_type(content_type)
                if ct_error:
                    return WebFetchedDocument(
                        url=url,
                        content_type=content_type,
                        status_code=status_code,
                        error=ct_error,
                        fetched_at=datetime.now(timezone.utc).isoformat(),
                    )

                # Read with max_bytes limit
                raw = resp.read(self.max_bytes)
                truncated_raw = len(raw) >= self.max_bytes

                # Decode
                charset = "utf-8"
                if "charset=" in content_type.lower():
                    try:
                        charset = content_type.lower().split("charset=")[-1].split(";")[0].strip()
                    except Exception:
                        charset = "utf-8"

                try:
                    text = raw.decode(charset, errors="replace")
                except Exception:
                    text = raw.decode("utf-8", errors="replace")

                # Sanitize HTML → text
                from src.web.sanitizer import html_to_text, extract_title

                title = extract_title(text, url)
                clean_text = html_to_text(text)

                # Truncate to max chars
                truncated = truncated_raw or len(clean_text) > self.max_chars
                if len(clean_text) > self.max_chars:
                    clean_text = clean_text[:self.max_chars]

                word_count = len(clean_text.split())

                # Check for prompt injection patterns
                injection_hits = detect_prompt_injection(clean_text)

                return WebFetchedDocument(
                    url=url,
                    title=title,
                    text=clean_text,
                    fetched_at=datetime.now(timezone.utc).isoformat(),
                    content_type=content_type,
                    status_code=status_code,
                    word_count=word_count,
                    truncated=truncated,
                    error=(
                        f"prompt_injection_detected: {', '.join(injection_hits)}"
                        if injection_hits and not truncated else None
                    ),
                )

        except urllib.error.URLError as e:
            return WebFetchedDocument(
                url=url,
                error=f"URL error: {e.reason}",
                fetched_at=datetime.now(timezone.utc).isoformat(),
            )
        except urllib.error.HTTPError as e:
            return WebFetchedDocument(
                url=url,
                status_code=e.code,
                error=f"HTTP {e.code}: {e.reason}",
                fetched_at=datetime.now(timezone.utc).isoformat(),
            )
        except TimeoutError:
            return WebFetchedDocument(
                url=url,
                error="timeout",
                fetched_at=datetime.now(timezone.utc).isoformat(),
            )
        except Exception as e:
            return WebFetchedDocument(
                url=url,
                error=f"fetch error: {e}",
                fetched_at=datetime.now(timezone.utc).isoformat(),
            )
