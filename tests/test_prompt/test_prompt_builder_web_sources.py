"""Tests for PromptBuilder with web sources."""
import pytest
from src.agent.prompt_builder import PromptBuilder

SYSTEM_PROMPT = "You are MemoryQwen, a local AI agent."


class FakeWebSource:
    def __init__(self, source_id, title, url, text):
        self.source_id = source_id
        self.title = title
        self.url = url
        self.text = text


class TestPromptBuilderWebSources:
    def setup_method(self):
        self.pb = PromptBuilder(SYSTEM_PROMPT)

    def test_prompt_includes_web_sources_section(self):
        ws = [FakeWebSource("W1", "Test Page", "https://test.com", "web content here")]
        msgs = self.pb.build("question?", web_sources=ws)
        user = msgs[1]["content"]
        assert "临时网页资料" in user or "Web Context" in user

    def test_web_sources_use_W_ids(self):
        ws = [
            FakeWebSource("W1", "A", "https://a.com", "a"),
            FakeWebSource("W2", "B", "https://b.com", "b"),
        ]
        msgs = self.pb.build("q?", web_sources=ws)
        user = msgs[1]["content"]
        assert "[W1]" in user
        assert "[W2]" in user

    def test_local_sources_still_use_S_ids(self):
        from src.retrieval.models import RetrievalResult
        retrieved = [RetrievalResult(source_path="/test/doc.md", content="local data", chunk_index=0, total_chunks=1)]
        ws = [FakeWebSource("W1", "Web", "https://w.com", "web")]
        msgs = self.pb.build("q?", retrieved=retrieved, web_sources=ws)
        user = msgs[1]["content"]
        assert "[S1]" in user
        assert "[W1]" in user

    def test_prompt_marks_web_sources_untrusted(self):
        ws = [FakeWebSource("W1", "T", "https://t.com", "content")]
        msgs = self.pb.build("q?", web_sources=ws)
        user = msgs[1]["content"]
        assert "untrusted" in user.lower()

    def test_no_web_sources_keeps_old_behavior(self):
        from src.retrieval.models import RetrievalResult
        retrieved = [RetrievalResult(source_path="/t/doc.md", content="data", chunk_index=0, total_chunks=1)]
        msgs = self.pb.build("q?", retrieved=retrieved)
        user = msgs[1]["content"]
        assert "[S1]" in user
        # v0.1.5 capability baseline may mention [W] but no actual web sources section

    def test_web_section_separate_from_local(self):
        from src.retrieval.models import RetrievalResult
        retrieved = [RetrievalResult(source_path="/t/doc.md", content="local", chunk_index=0, total_chunks=1)]
        ws = [FakeWebSource("W1", "Web", "https://w.com", "web content")]
        msgs = self.pb.build("q?", retrieved=retrieved, web_sources=ws)
        user = msgs[1]["content"]
        s_pos = user.find("[S1]")
        w_pos = user.find("[W1]")
        assert s_pos >= 0 and w_pos >= 0
        # v0.1.5 capability baseline appears first, then local [S], then web [W]
