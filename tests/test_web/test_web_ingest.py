"""Tests for Web Ingest Pipeline."""
import pytest
import tempfile, shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.web.web_ingest import (
    WebIngestService, WebIngestResult, _redact_url,
    _safe_slug, _compute_source_hash,
)


class TestRedactURL:
    def test_normal_url_unchanged(self):
        assert _redact_url("https://example.com/page") == "https://example.com/page"

    def test_token_redacted(self):
        result = _redact_url("https://api.com?token=abc123&user=john")
        assert "token=[REDACTED]" in result
        assert "abc123" not in result

    def test_api_key_redacted(self):
        result = _redact_url("https://api.com?api_key=secret123")
        assert "api_key=[REDACTED]" in result

    def test_multiple_sensitive_params(self):
        result = _redact_url("https://x.com?token=a&secret=b&name=c")
        assert "token=[REDACTED]" in result
        assert "secret=[REDACTED]" in result
        assert "name=c" in result


class TestSafeSlug:
    def test_from_title(self):
        slug = _safe_slug("https://example.com/long/path", "My Test Page!")
        assert "my-test-page" in slug.lower()

    def test_fallback_to_url(self):
        slug = _safe_slug("https://github.com/Fujo930/MemoryQwen", None)
        assert "github" in slug.lower() or "memoryqwen" in slug.lower()

    def test_no_special_chars(self):
        slug = _safe_slug("https://x.com", "Hello??? World!!!")
        assert "?" not in slug
        assert "!" not in slug


class TestSourceHash:
    def test_same_content_same_hash(self):
        h1 = _compute_source_hash("hello", "https://x.com")
        h2 = _compute_source_hash("hello", "https://x.com")
        assert h1 == h2

    def test_different_url_different_hash(self):
        h1 = _compute_source_hash("hello", "https://a.com")
        h2 = _compute_source_hash("hello", "https://b.com")
        assert h1 != h2


class TestWebIngestService:
    def setup_method(self):
        self.tmpdir = Path(tempfile.mkdtemp())
        self.orig_cwd = Path.cwd()
        # Run from tmpdir so memory/sources/web is created there
        import os
        os.chdir(str(self.tmpdir))
        self.svc = WebIngestService()

    def teardown_method(self):
        import os
        os.chdir(str(self.orig_cwd))
        shutil.rmtree(str(self.tmpdir), ignore_errors=True)

    def test_reject_file_url(self):
        result = self.svc.ingest_url("file:///etc/passwd")
        assert result.error is not None
        assert result.saved_path == ""

    def test_reject_localhost(self):
        result = self.svc.ingest_url("http://localhost/admin")
        assert result.error is not None

    def test_reject_private_ip(self):
        result = self.svc.ingest_url("http://192.168.1.1/admin")
        assert result.error is not None

    def test_successful_ingest_writes_markdown(self):
        html = "<html><head><title>Test Page</title></head><body><p>Hello world</p></body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html; charset=utf-8"}
        mock_resp.read.return_value = html.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = self.svc.ingest_url("https://example.com")
            assert result.error is None
            assert result.saved_path != ""
            assert "memory" in result.saved_path.replace("\\", "/")
            assert result.title == "Test Page"

    def test_ingest_frontmatter_contains_url(self):
        html = "<html><title>T</title><body>x</body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_resp.read.return_value = html.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = self.svc.ingest_url("https://example.com/page")
            assert result.error is None
            saved = Path(result.saved_path)
            content = saved.read_text(encoding="utf-8")
            assert "source_type: web" in content
            assert "url: https://example.com/page" in content

    def test_ingest_frontmatter_contains_fetched_at(self):
        html = "<html><title>T</title><body>x</body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_resp.read.return_value = html.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = self.svc.ingest_url("https://example.com")
            assert result.error is None
            saved = Path(result.saved_path)
            content = saved.read_text(encoding="utf-8")
            assert "fetched_at:" in content

    def test_ingest_records_source_hash(self):
        html = "<html><title>T</title><body>x</body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_resp.read.return_value = html.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = self.svc.ingest_url("https://example.com")
            assert len(result.source_hash) == 64  # SHA-256 hex

    def test_dedup_same_content(self):
        html = "<html><title>T</title><body>unique content 12345</body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_resp.read.return_value = html.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            r1 = self.svc.ingest_url("https://example.com")
            assert not r1.duplicated
            r2 = self.svc.ingest_url("https://example.com")
            assert r2.duplicated
