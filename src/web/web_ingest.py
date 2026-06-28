"""
MemoryQwen — Web Ingest Pipeline.

The ONLY path for web content to enter long-term memory.
Requires explicit `web ingest` command. Not automatic.
"""

from __future__ import annotations

import hashlib
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from src.web.fetcher import WebFetcher
from src.web.safety import validate_url
from src.web.sanitizer import html_to_text, extract_title


# ── Sensitive query parameters to redact ────────────────────
_SENSITIVE_PARAMS = {
    "token", "api_key", "apikey", "key", "secret",
    "password", "passwd", "session", "auth", "access_token",
    "refresh_token", "client_secret", "private_key",
}


@dataclass
class WebIngestResult:
    """Result of a web ingest operation."""
    url: str
    url_safe: str = ""           # URL with sensitive params redacted
    saved_path: str = ""         # relative path under memory/sources/web/
    title: str | None = None
    source_hash: str = ""
    chunks_added: int = 0
    duplicated: bool = False
    truncated: bool = False
    warnings: list[str] = field(default_factory=list)
    error: str | None = None


def _redact_url(url: str) -> str:
    """Remove sensitive query parameters from a URL for logging."""
    parsed = urlparse(url)
    if not parsed.query:
        return url
    params = parsed.query.split("&")
    safe_params = []
    for p in params:
        if "=" in p:
            k = p.split("=")[0].lower()
            if k in _SENSITIVE_PARAMS:
                safe_params.append(f"{k}=[REDACTED]")
            else:
                safe_params.append(p)
        else:
            safe_params.append(p)
    safe_query = "&".join(safe_params)
    return urlunparse(parsed._replace(query=safe_query))


def _safe_slug(url: str, title: str | None = None) -> str:
    """Generate a safe filename slug from a URL and optional title."""
    # Use title if available, otherwise hostname+path
    if title:
        slug = re.sub(r"[^a-zA-Z0-9一-鿿_\- ]", "", title.lower())[:60].strip()
        slug = re.sub(r"\s+", "-", slug)
        if slug:
            return slug

    parsed = urlparse(url)
    slug = f"{parsed.hostname or 'web'}-{parsed.path.strip('/')}"
    slug = re.sub(r"[^a-zA-Z0-9_\-]", "-", slug)[:80].strip("-")
    return slug or "web-page"


def _compute_source_hash(content: str, url: str) -> str:
    """SHA-256 hash of content + canonical URL."""
    return hashlib.sha256(
        (content.strip() + "|" + url.strip()).encode("utf-8")
    ).hexdigest()


class WebIngestService:
    """Service for ingesting web pages into long-term memory.

    Writes to: memory/sources/web/<YYYYMMDD>/<slug>.md
    Only path that adds web content to knowledge_store.
    """

    def __init__(self, config=None):
        self.config = config
        timeout = getattr(getattr(config, "web", None), "fetch_timeout_seconds", 10) if config else 10
        max_bytes = getattr(getattr(config, "web", None), "fetch_max_bytes", 500_000) if config else 500_000
        max_chars = getattr(getattr(config, "web", None), "fetch_max_chars", 12_000) if config else 12_000
        ua = getattr(getattr(config, "web", None), "user_agent", "MemoryQwen/0.1.5") if config else "MemoryQwen/0.1.5"
        allow_priv = getattr(getattr(config, "web", None), "allow_private_network", False) if config else False

        self.fetcher = WebFetcher(
            timeout=timeout, max_bytes=max_bytes, max_chars=max_chars,
            user_agent=ua, allow_private=allow_priv,
        )

    def ingest_url(self, url: str) -> WebIngestResult:
        """Fetch a URL, save to memory/sources/web/, return result."""
        start = time.monotonic()
        warnings: list[str] = []
        url_safe = _redact_url(url)

        # 1. URL safety check
        is_safe, err = validate_url(url)
        if not is_safe:
            return WebIngestResult(
                url=url, url_safe=url_safe,
                error=err or "URL rejected by safety check",
            )

        # 2. Fetch
        doc = self.fetcher.fetch(url)
        if doc.error:
            return WebIngestResult(
                url=url, url_safe=url_safe,
                error=doc.error,
            )

        # 3. Sanitize
        text = doc.text
        title = doc.title or extract_title(text, url)
        truncated = doc.truncated

        # 4. Build body and compute hash for dedup
        body = f"# {title}\n\n{text}"
        source_hash = _compute_source_hash(body, url)

        # 5. Build frontmatter markdown
        fm = "\n".join([
            "---",
            f"source_type: web",
            f"url: {url_safe}",
            f"fetched_at: {doc.fetched_at}",
            f"title: {title}",
            f"content_type: {doc.content_type or 'text/html'}",
            f"status_code: {doc.status_code or 0}",
            f"source_hash: {source_hash}",
            f"truncated: {str(truncated).lower()}",
            "---",
            "",
            body,
            "",
        ])

        # 5. Save to memory/sources/web/
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
        dest_dir = Path("memory/sources/web") / today
        dest_dir.mkdir(parents=True, exist_ok=True)

        slug = _safe_slug(url, title) + ".md"
        dest = dest_dir / slug

        # Dedup: check if existing file has same hash
        duplicated = False
        if dest.exists():
            existing = dest.read_text(encoding="utf-8", errors="replace")
            existing_hash = _compute_source_hash(
                re.sub(r"^---.*?---\n", "", existing, flags=re.DOTALL).strip(),
                url
            )
            if existing_hash == source_hash:
                return WebIngestResult(
                    url=url, url_safe=url_safe,
                    saved_path=str(dest.relative_to(Path.cwd())) if dest.is_relative_to(Path.cwd()) else str(dest),
                    title=title, source_hash=source_hash,
                    duplicated=True, truncated=truncated,
                    warnings=["Source already archived with identical hash"],
                )
            # Hash differs — add suffix
            base_name = slug.replace(".md", "")
            suffix = 1
            while dest.exists():
                dest = dest_dir / f"{base_name}__{suffix}.md"
                suffix += 1

        dest.write_text(fm, encoding="utf-8")

        saved_path = str(dest.relative_to(Path.cwd())) if dest.is_relative_to(Path.cwd()) else str(dest)

        # 6. Try to run ingestion pipeline (if available)
        chunks_added = 0
        try:
            from src.ingestion.pipeline import IngestionPipeline
            from src.config import load_config
            cfg = self.config if self.config else load_config()
            pipeline = IngestionPipeline(cfg)
            result = pipeline.ingest_file(dest)
            chunks_added = getattr(result, "chunks_stored", 0)
        except Exception as e:
            warnings.append(f"Ingestion pipeline skipped: {e}")
            chunks_added = 0

        return WebIngestResult(
            url=url, url_safe=url_safe,
            saved_path=saved_path,
            title=title, source_hash=source_hash,
            chunks_added=chunks_added,
            duplicated=False, truncated=truncated,
            warnings=warnings,
        )
