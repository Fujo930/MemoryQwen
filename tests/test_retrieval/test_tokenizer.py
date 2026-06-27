"""
SimpleTokenizer 测试
"""

import pytest
from src.retrieval.tokenizer import SimpleTokenizer


@pytest.fixture
def tok():
    return SimpleTokenizer()


class TestEnglish:
    def test_basic_words(self, tok):
        tokens = tok.tokenize("hello world test")
        assert "hello" in tokens
        assert "world" in tokens
        assert "test" in tokens

    def test_lowercase(self, tok):
        tokens = tok.tokenize("Hello WORLD")
        assert "hello" in tokens
        assert "world" in tokens

    def test_filter_single_char(self, tok):
        tokens = tok.tokenize("a test")
        assert "a" not in tokens
        assert "test" in tokens

    def test_filter_numbers(self, tok):
        tokens = tok.tokenize("123 4567 test")
        assert "123" not in tokens
        assert "4567" not in tokens
        assert "test" in tokens

    def test_punctuation_removed(self, tok):
        tokens = tok.tokenize("hello, world! test.")
        assert "hello" in tokens
        assert "world" in tokens
        assert "test" in tokens
        assert "," not in tokens


class TestChinese:
    def test_unigram(self, tok):
        tokens = tok.tokenize("检索")
        # unigram: "检", "索"; bigram: "检索"
        assert "检" in tokens
        assert "索" in tokens
        assert "检索" in tokens

    def test_unigram_and_bigram(self, tok):
        tokens = tok.tokenize("检索测试")
        assert "检" in tokens
        assert "索" in tokens
        assert "测" in tokens
        assert "试" in tokens
        assert "检索" in tokens
        assert "测试" in tokens

    def test_chinese_no_filter_single(self, tok):
        """中文单字不过滤"""
        tokens = tok.tokenize("你好")
        assert "你" in tokens
        assert "好" in tokens


class TestMixed:
    def test_mixed_zh_en(self, tok):
        tokens = tok.tokenize("Python 是一种编程语言")
        assert "python" in tokens
        assert "编" in tokens
        assert "编程" in tokens

    def test_empty(self, tok):
        assert tok.tokenize("") == []

    def test_whitespace_only(self, tok):
        assert tok.tokenize("   ") == []


class TestDedup:
    def test_unique_tokens(self, tok):
        tokens = tok.tokenize("hello hello world")
        assert tokens.count("hello") == 1
        assert tokens.count("world") == 1
