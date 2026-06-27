"""
MemoryQwen — Ingestion 模块测试
"""

import pytest
import tempfile
from pathlib import Path
from src.ingestion.parser import DocumentParser, UnsupportedFormatError


class TestDocumentParser:
    """文件解析器测试"""

    @pytest.fixture
    def parser(self):
        return DocumentParser()

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as d:
            yield Path(d)

    @pytest.mark.asyncio
    async def test_parse_txt(self, parser, temp_dir):
        """测试 txt 解析"""
        file_path = temp_dir / "test.txt"
        file_path.write_text("这是一个测试文件\n第二行内容", encoding="utf-8")

        doc = await parser.parse(str(file_path))
        assert doc.file_type == "txt"
        assert doc.title == "test"
        assert "测试文件" in doc.content
        assert doc.char_count > 0

    @pytest.mark.asyncio
    async def test_parse_md(self, parser, temp_dir):
        """测试 markdown 解析"""
        file_path = temp_dir / "test.md"
        file_path.write_text("# 标题\n\n这是正文内容\n\n- 列表项1\n- 列表项2", encoding="utf-8")

        doc = await parser.parse(str(file_path))
        assert doc.file_type == "md"
        assert "# 标题" in doc.content

    @pytest.mark.asyncio
    async def test_parse_code(self, parser, temp_dir):
        """测试代码文件解析"""
        file_path = temp_dir / "test.py"
        file_path.write_text("def hello():\n    print('Hello')\n", encoding="utf-8")

        doc = await parser.parse(str(file_path))
        assert doc.file_type == "py"
        assert "def hello" in doc.content

    @pytest.mark.asyncio
    async def test_unsupported_format(self, parser, temp_dir):
        """测试不支持格式"""
        file_path = temp_dir / "test.xyz"
        file_path.write_text("content", encoding="utf-8")

        with pytest.raises(UnsupportedFormatError):
            await parser.parse(str(file_path))

    def test_supported_extensions(self, parser):
        """测试支持的扩展名"""
        exts = parser.supported_extensions()
        assert ".txt" in exts
        assert ".md" in exts
        assert ".pdf" in exts
        assert ".docx" in exts
        assert ".py" in exts
        assert ".js" in exts

    def test_can_handle(self, parser):
        """测试 can_handle"""
        assert parser.can_handle("file.txt") is True
        assert parser.can_handle("file.md") is True
        assert parser.can_handle("file.py") is True
        assert parser.can_handle("file.xyz") is False


class TestDocumentChunker:
    """切片器测试"""

    @pytest.fixture
    def chunker(self):
        from src.ingestion.chunker import DocumentChunker
        return DocumentChunker()

    def test_chunk_short_document(self, chunker):
        """测试短文档"""
        from src.ingestion.parser import Document
        doc = Document(
            file_path="test.md",
            file_type="md",
            title="test",
            content="这是一篇短文档。",
            metadata={},
            char_count=8,
        )
        chunks = chunker.chunk(doc)
        assert len(chunks) == 1
        assert chunks[0].content == "这是一篇短文档。"
        assert chunks[0].token_count > 0

    def test_chunk_markdown_by_headings(self, chunker):
        """测试 markdown 按标题切片"""
        from src.ingestion.chunker import DocumentChunker
        from src.ingestion.parser import Document
        # 使用小 max_tokens 强制分块
        small_chunker = DocumentChunker()
        small_chunker.max_tokens = 30

        content = "# 第一章\n\n" + "第一章内容详情。\n" * 20 + \
                  "\n# 第二章\n\n" + "第二章内容详情。\n" * 20 + \
                  "\n# 第三章\n\n" + "第三章内容详情。\n" * 20
        doc = Document(
            file_path="test.md",
            file_type="md",
            title="test",
            content=content,
            metadata={},
            char_count=len(content),
        )
        chunks = small_chunker.chunk(doc)
        assert len(chunks) >= 3

    def test_chunk_metadata(self, chunker):
        """测试切片元数据"""
        from src.ingestion.parser import Document
        doc = Document(
            file_path="test.md",
            file_type="md",
            title="test",
            content="测试内容",
            metadata={"source_path": "test.md"},
            char_count=4,
        )
        chunks = chunker.chunk(doc)
        chunk = chunks[0]
        assert chunk.doc_id == "test.md"
        assert chunk.metadata["source_path"] == "test.md"
        assert chunk.metadata["chunk_index"] == 0
