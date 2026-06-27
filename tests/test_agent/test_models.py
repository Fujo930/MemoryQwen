"""
Agent 数据模型测试
"""

from src.agent.models import ChatRequest, SourceCitation, AgentChatResponse


class TestChatRequest:
    def test_defaults(self):
        req = ChatRequest(session_id="s1", message="hello")
        assert req.session_id == "s1"
        assert req.message == "hello"
        assert req.top_k == 5
        assert req.include_recent is True
        assert req.max_recent_messages == 10

    def test_custom(self):
        req = ChatRequest(session_id="s2", message="hi", top_k=3, include_recent=False)
        assert req.top_k == 3
        assert req.include_recent is False


class TestSourceCitation:
    def test_fields(self):
        sc = SourceCitation(
            record_id="r1", title="T", source_path="/a.md",
            chunk_index=2, score=0.85, snippet="snip..."
        )
        assert sc.record_id == "r1"
        assert sc.title == "T"
        assert sc.source_path == "/a.md"
        assert sc.chunk_index == 2
        assert sc.score == 0.85
        assert sc.snippet == "snip..."


class TestAgentChatResponse:
    def test_defaults(self):
        resp = AgentChatResponse()
        assert resp.answer == ""
        assert resp.sources == []
        assert resp.memory_used == []
        assert resp.metadata == {}

    def test_full(self):
        resp = AgentChatResponse(
            answer="Hello",
            session_id="s1",
            sources=[SourceCitation(record_id="r1")],
            memory_used=["knowledge_store"],
            model="test-model",
            metadata={"retrieval_count": 3},
        )
        assert resp.model == "test-model"
        assert resp.metadata["retrieval_count"] == 3
        assert len(resp.sources) == 1
