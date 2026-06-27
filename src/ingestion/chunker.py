"""
MemoryQwen — DocumentChunker 语义切片器
支持 markdown 标题分割、段落分割、固定 token 分割
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from typing import Any

from src.ingestion.parser import Document

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """文档切片"""
    doc_id: str
    content: str
    token_count: int
    chunk_index: int
    metadata: dict = field(default_factory=dict)


class DocumentChunker:
    """文档切片器"""

    def __init__(self, config: Any | None = None):
        self.config = config
        self.max_tokens = getattr(config.memory.chunking, "max_tokens", 512) if config else 512
        self.overlap = getattr(config.memory.chunking, "overlap_tokens", 32) if config else 32
        self.strategy = getattr(config.memory.chunking, "strategy", "semantic") if config else "semantic"

    def chunk(self, document: Document) -> list[Chunk]:
        """将文档切片"""
        if self.strategy == "semantic":
            return self._semantic_chunk(document)
        elif self.strategy == "heading":
            return self._heading_chunk(document)
        else:
            return self._fixed_chunk(document)

    def _semantic_chunk(self, document: Document) -> list[Chunk]:
        """语义切片：按标题/段落分层"""
        content = document.content
        file_type = document.file_type

        if file_type == "md":
            sections = self._split_by_markdown_headings(content)
        else:
            sections = self._split_by_paragraphs(content)

        chunks = []
        current_section = ""
        current_tokens = 0
        chunk_idx = 0

        for section in sections:
            section_tokens = self._count_tokens(section)

            # 如果当前块 + 新段落不超过 max_tokens，合并
            if current_tokens + section_tokens <= self.max_tokens:
                if current_section:
                    current_section += "\n\n" + section
                else:
                    current_section = section
                current_tokens += section_tokens
            else:
                # 保存当前块
                if current_section.strip():
                    chunks.append(self._make_chunk(
                        document, current_section, current_tokens, chunk_idx
                    ))
                    chunk_idx += 1

                # 如果段落本身超过 max_tokens，需要拆分
                if section_tokens > self.max_tokens:
                    sub_chunks = self._split_long_section(section, document, chunk_idx)
                    chunks.extend(sub_chunks)
                    chunk_idx += len(sub_chunks)
                    current_section = ""
                    current_tokens = 0
                else:
                    current_section = section
                    current_tokens = section_tokens

        # 最后一段
        if current_section.strip():
            chunks.append(self._make_chunk(
                document, current_section, current_tokens, chunk_idx
            ))

        logger.debug("Chunked into %d chunks (strategy=%s)", len(chunks), self.strategy)
        return chunks

    def _heading_chunk(self, document: Document) -> list[Chunk]:
        """按文档前 N 个字符扁平切分"""
        return self._fixed_chunk(document)

    def _fixed_chunk(self, document: Document) -> list[Chunk]:
        """固定 token 切分"""
        text = document.content
        chunks = []
        chunk_idx = 0

        while text:
            # 取前 max_tokens 个 token 的文本
            chunk_text = self._take_tokens(text, self.max_tokens)
            taken_len = len(chunk_text)
            token_count = self._count_tokens(chunk_text)

            chunks.append(self._make_chunk(document, chunk_text, token_count, chunk_idx))
            chunk_idx += 1

            # 重叠切分
            overlap_chars = int(len(chunk_text) * (self.overlap / self.max_tokens))
            text = text[taken_len - overlap_chars:]

        return chunks

    @staticmethod
    def _split_by_markdown_headings(content: str) -> list[str]:
        """按 markdown 标题分割"""
        # 在标题前分割
        sections = re.split(r'(?=^#{1,6}\s)', content, flags=re.MULTILINE)
        # 过滤空字符串
        return [s.strip() for s in sections if s.strip()]

    @staticmethod
    def _split_by_paragraphs(content: str) -> list[str]:
        """按段落（空行）分割"""
        paragraphs = re.split(r'\n\s*\n', content)
        result = []
        for p in paragraphs:
            p = p.strip()
            if p:
                # 如果段落太长，进一步按句号分割
                if len(p) > 2000:
                    sentences = re.split(r'(?<=[。！？.!?])', p)
                    result.extend(s for s in sentences if s.strip())
                else:
                    result.append(p)
        return result if result else [content]

    def _split_long_section(self, section: str, document: Document, start_idx: int) -> list[Chunk]:
        """拆分超长段落"""
        chunks = []
        while section:
            chunk_text = self._take_tokens(section, self.max_tokens)
            taken_len = len(chunk_text)
            token_count = self._count_tokens(chunk_text)
            chunks.append(self._make_chunk(document, chunk_text, token_count, start_idx + len(chunks)))
            section = section[taken_len:]
        return chunks

    def _make_chunk(self, document: Document, content: str, token_count: int, index: int) -> Chunk:
        """创建 Chunk 对象"""
        return Chunk(
            doc_id=document.file_path,
            content=content,
            token_count=token_count,
            chunk_index=index,
            metadata={
                "source_path": document.file_path,
                "source_type": document.file_type,
                "doc_title": document.title,
                "chunk_index": index,
                "chunk_of": document.file_path,
            },
        )

    def _count_tokens(self, text: str) -> int:
        """估算 token 数"""
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except Exception:
            # fallback 估算
            chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
            other = len(text) - chinese
            return int(chinese * 1.5 + other / 4) + 10

    def _take_tokens(self, text: str, max_tokens: int) -> str:
        """截取不超过 max_tokens 的文本"""
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            tokens = enc.encode(text)
            if len(tokens) <= max_tokens:
                return text
            truncated = tokens[:max_tokens]
            return enc.decode(truncated)
        except Exception:
            # fallback: 按字符估算
            ratio = max_tokens / max(self._count_tokens(text), 1)
            cutoff = int(len(text) * ratio)
            return text[:cutoff]
