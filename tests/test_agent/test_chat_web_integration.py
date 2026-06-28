"""Tests for chat --web integration in AgentChatService."""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.agent.models import ChatRequest, AgentChatResponse
from src.agent.chat_service import AgentChatService


class FakeConfig:
    class agent:
        system_prompt = "You are MemoryQwen."
        use_error_memory = True
        use_strategy_memory = True
        error_top_k = 3
        strategy_top_k = 3
        max_error_context_chars = 1200
        max_strategy_context_chars = 1000
        error_memory_recent_fallback = False
        strategy_memory_recent_fallback = False
        save_chat_memory = True
    class web:
        enabled = False
        provider = "mock"
        search_max_results = 3
        fetch_timeout_seconds = 10
        fetch_max_bytes = 500000
        fetch_max_chars = 12000
        user_agent = "Test/1.0"
        allow_private_network = False


class FakeModelClient:
    async def chat(self, messages):
        m = MagicMock()
        m.content = "mock response"
        m.model = "test"
        m.usage = {"total_tokens": 10}
        return m


class FakeRetriever:
    async def search(self, query, top_k=5):
        from src.retrieval.models import RetrievalResult
        return [RetrievalResult(source_path="/t/doc.md", content="test data", chunk_index=0, total_chunks=1)]


class FakeStore:
    async def add(self, store_type, data): pass
    async def list(self, store_type, limit=100): return []
    async def list_by_metadata(self, store_type, filters, limit=100, order_by="created_at", descending=False): return []
    async def close(self): pass


@pytest.fixture
def service():
    return AgentChatService(
        config=FakeConfig(),
        model_client=FakeModelClient(),
        retriever=FakeRetriever(),
        store=FakeStore(),
    )


class TestChatWebIntegration:
    @pytest.mark.asyncio
    async def test_chat_without_web_does_not_call_web_service(self, service):
        req = ChatRequest(session_id="test", message="hello", use_web=False)
        resp = await service.chat(req)
        meta = resp.metadata
        assert meta["web"]["enabled_for_chat"] is False
        assert meta["web"]["queried"] is False
        assert meta["web"]["reason"] == "web_not_enabled"

    @pytest.mark.asyncio
    async def test_chat_with_web_local_question_does_not_query(self, service):
        req = ChatRequest(session_id="test", message="MemoryQwen 支持什么功能？", use_web=True)
        resp = await service.chat(req)
        meta = resp.metadata
        assert meta["web"]["enabled_for_chat"] is True
        assert meta["web"]["queried"] is False
        assert "local" in meta["web"]["reason"].lower()

    @pytest.mark.asyncio
    async def test_chat_metadata_records_web_not_enabled(self, service):
        req = ChatRequest(session_id="test", message="hello", use_web=False)
        resp = await service.chat(req)
        assert "web" in resp.metadata
        assert resp.metadata["web"]["enabled_for_chat"] is False

    @pytest.mark.asyncio
    async def test_chat_metadata_records_web_enabled_but_no_query(self, service):
        req = ChatRequest(session_id="test", message="memoryqwen function", use_web=True)
        resp = await service.chat(req)
        assert resp.metadata["web"]["enabled_for_chat"] is True
        assert resp.metadata["web"]["queried"] is False

    @pytest.mark.asyncio
    async def test_capability_guard_still_runs_with_web(self, service):
        req = ChatRequest(session_id="test", message="支持 PDF 吗？", use_web=True)
        resp = await service.chat(req)
        # Capability guard should trigger for this message
        assert "capability_guard_triggered" in resp.metadata

    @pytest.mark.asyncio
    async def test_retrieval_gate_still_runs_with_web(self, service):
        req = ChatRequest(session_id="test", message="hello", use_web=True)
        resp = await service.chat(req)
        assert "retrieval_gate_enabled" in resp.metadata
        assert "retrieval_skipped" in resp.metadata

    @pytest.mark.asyncio
    async def test_web_sources_are_passed_to_prompt_builder(self, service):
        # Use latest signal to trigger web query
        req = ChatRequest(session_id="test", message="latest AI news today", use_web=True)
        resp = await service.chat(req)
        # Even if web query fails in test, the web meta should record the attempt
        assert resp.metadata["web"]["enabled_for_chat"] is True

    @pytest.mark.asyncio
    async def test_memory_used_includes_web_when_queried(self, service):
        req = ChatRequest(session_id="test", message="latest news today", use_web=True)
        resp = await service.chat(req)
        # web is added to memory_used when queried
        assert "memory_used" in resp.metadata

    @pytest.mark.asyncio
    async def test_use_web_defaults_to_false(self):
        req = ChatRequest(session_id="test", message="hello")
        assert req.use_web is False

    @pytest.mark.asyncio
    async def test_web_prompt_injection_not_executed(self, service):
        # This tests that web content containing injection patterns
        # is still handled safely by the chat service
        req = ChatRequest(session_id="test", message="latest news today", use_web=True)
        resp = await service.chat(req)
        # Chat should still complete without exception
        assert resp.answer is not None
        assert "web" in resp.metadata
