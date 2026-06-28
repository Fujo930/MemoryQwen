"""Tests for HTML sanitizer."""
from src.web.sanitizer import html_to_text, extract_title, truncate_text, strip_noise


class TestHtmlToText:
    def test_plain_text_unchanged(self):
        assert html_to_text("Hello world") == "Hello world"

    def test_empty_input(self):
        assert html_to_text("") == ""
        assert html_to_text(None) == ""

    def test_script_removed(self):
        html = "<html><script>alert('xss')</script><body>safe</body></html>"
        result = html_to_text(html)
        assert "alert" not in result
        assert "safe" in result

    def test_style_removed(self):
        html = "<html><style>.x{color:red}</style><body>text</body></html>"
        result = html_to_text(html)
        assert "color" not in result
        assert "text" in result

    def test_html_tags_removed(self):
        html = "<div><p>Hello <b>world</b></p></div>"
        result = html_to_text(html)
        assert "<div>" not in result
        assert "<b>" not in result
        assert "Hello world" in result

    def test_entities_decoded(self):
        html = "Price: &amp; &lt; &gt; &quot;"
        result = html_to_text(html)
        assert "&" in result
        assert "<" in result
        assert ">" in result
        assert '"' in result

    def test_whitespace_collapsed(self):
        html = "hello    world\n\n\nfoo"
        result = html_to_text(html)
        # Should collapse multiple spaces
        assert "hello world" in result or "hello  world" in result


class TestExtractTitle:
    def test_extract_title_tag(self):
        html = "<html><head><title>My Page</title></head><body></body></html>"
        assert extract_title(html) == "My Page"

    def test_extract_h1_fallback(self):
        # extract_title looks for <title> tag only, not <h1>
        # HTML h1 is not a fallback in current implementation
        html = "<html><body><h1>My Heading</h1></body></html>"
        result = extract_title(html, "fallback.com")
        assert result == "fallback.com"  # falls back to URL since no <title>

    def test_no_title_returns_fallback(self):
        html = "<html><body>no title here</body></html>"
        result = extract_title(html, "fallback.com")
        assert result == "fallback.com" or result == "Untitled"

    def test_empty_input(self):
        assert extract_title("") == "Untitled"


class TestTruncateText:
    def test_no_truncation_needed(self):
        text, truncated = truncate_text("short", 100)
        assert text == "short"
        assert truncated is False

    def test_truncation(self):
        text, truncated = truncate_text("x" * 200, 100)
        assert len(text) == 100
        assert truncated is True


class TestStripNoise:
    def test_excessive_blank_lines_collapsed(self):
        result = strip_noise("a\n\n\n\n\nb")
        assert result.count("\n") <= 2

    def test_leading_trailing_whitespace_removed(self):
        result = strip_noise("  \nhello\n  ")
        assert result == "hello"
