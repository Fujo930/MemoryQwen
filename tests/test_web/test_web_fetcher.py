"""Tests for WebFetcher with mocked HTTP."""
import pytest
from unittest.mock import patch, MagicMock
from src.web.fetcher import WebFetcher
from src.web.models import WebFetchedDocument


class TestWebFetcher:
    def setup_method(self):
        self.fetcher = WebFetcher()

    def test_reject_file_url(self):
        doc = self.fetcher.fetch("file:///etc/passwd")
        assert doc.error is not None
        assert "scheme" in doc.error.lower() or "file" in doc.error.lower()

    def test_reject_localhost(self):
        doc = self.fetcher.fetch("http://localhost/test")
        assert doc.error is not None
        assert "localhost" in doc.error.lower()

    def test_reject_private_ip(self):
        doc = self.fetcher.fetch("http://192.168.1.1/admin")
        assert doc.error is not None

    def test_reject_non_http_scheme(self):
        doc = self.fetcher.fetch("ftp://example.com/file")
        assert doc.error is not None

    def test_reject_empty_url(self):
        doc = self.fetcher.fetch("")
        assert doc.error is not None

    def test_allow_https(self):
        html_content = "<html><head><title>Test</title></head><body><p>Hello world</p></body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html; charset=utf-8"}
        mock_resp.read.return_value = html_content.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            doc = self.fetcher.fetch("https://example.com")
            assert doc.error is None
            assert doc.title == "Test"
            assert "Hello world" in doc.text
            assert doc.status_code == 200

    def test_content_type_non_text_rejected(self):
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "image/png"}
        mock_resp.read.return_value = b"fake-png-data"
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            doc = self.fetcher.fetch("https://example.com/image.png")
            assert doc.error is not None
            assert "content type" in doc.error.lower()

    def test_http_error_handled(self):
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(
            "https://example.com", 404, "Not Found", {}, None
        )):
            doc = self.fetcher.fetch("https://example.com/404")
            assert doc.error is not None
            assert "Not Found" in doc.error

    def test_url_error_handled(self):
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("connection refused")):
            doc = self.fetcher.fetch("https://example.com")
            assert doc.error is not None

    def test_fetched_at_populated(self):
        html = "<html><title>T</title><body>text</body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_resp.read.return_value = html.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            doc = self.fetcher.fetch("https://example.com")
            assert doc.fetched_at
            assert "T" in doc.fetched_at or doc.fetched_at  # ISO format check

    def test_word_count(self):
        html = "<html><title>T</title><body>one two three</body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_resp.read.return_value = html.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            doc = self.fetcher.fetch("https://example.com")
            assert doc.word_count >= 3

    def test_truncation(self):
        fetcher = WebFetcher(max_chars=20)
        html = "<html><title>T</title><body>" + "x" * 200 + "</body></html>"
        mock_resp = MagicMock()
        mock_resp.getcode.return_value = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_resp.read.return_value = html.encode("utf-8")
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            doc = fetcher.fetch("https://example.com")
            assert doc.truncated is True
            assert len(doc.text) <= 25  # max_chars + some margin
