"""
MemoryQwen — SimpleTokenizer
英文按词切分 + 中文 unigram/bigram
"""

from __future__ import annotations

import re
import logging

logger = logging.getLogger(__name__)

# 中文字符范围
_CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')
# 英文单词
_ENGLISH_RE = re.compile(r'[a-zA-Z]{2,}')
# 标点/空白
_PUNCT_RE = re.compile(r'[^\w\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')


class SimpleTokenizer:
    """简单分词器 —— 无外部依赖"""

    def tokenize(self, text: str) -> list[str]:
        """对文本分词，返回 token 列表"""
        if not text:
            return []

        text = text.lower()
        tokens = []

        # 分离中文和非中文字符块
        segments = self._split_segments(text)

        for seg in segments:
            if self._is_chinese(seg[0]):
                # 中文：unigram + bigram
                tokens.extend(self._chinese_tokens(seg))
            else:
                # 英文/数字：按词切分
                tokens.extend(self._english_tokens(seg))

        # 去重不改变顺序的去重
        seen = set()
        unique = []
        for t in tokens:
            if t not in seen:
                seen.add(t)
                unique.append(t)
        return unique

    def _split_segments(self, text: str) -> list[str]:
        """将文本按中/英文块分离"""
        segments = []
        current = ""
        current_type = None  # 'zh' or 'en'

        for ch in text:
            if _CHINESE_RE.match(ch):
                if current_type == 'en':
                    segments.append(current)
                    current = ""
                current_type = 'zh'
                current += ch
            elif ch.isalpha() or ch.isdigit():
                if current_type == 'zh':
                    segments.append(current)
                    current = ""
                current_type = 'en'
                current += ch
            else:
                if current:
                    segments.append(current)
                    current = ""
                current_type = None
        if current:
            segments.append(current)
        return segments

    def _chinese_tokens(self, text: str) -> list[str]:
        """中文 unigram + bigram"""
        tokens = []
        chars = list(text)
        # unigram（不过滤单字）
        tokens.extend(chars)
        # bigram
        for i in range(len(chars) - 1):
            tokens.append(chars[i] + chars[i + 1])
        return tokens

    def _english_tokens(self, text: str) -> list[str]:
        """英文按词切分，过滤纯数字和单字符"""
        # 去标点
        cleaned = _PUNCT_RE.sub(' ', text)
        words = cleaned.split()
        tokens = []
        for w in words:
            if len(w) >= 2 and not w.isdigit():
                tokens.append(w)
        return tokens

    @staticmethod
    def _is_chinese(ch: str) -> bool:
        return bool(_CHINESE_RE.match(ch))
