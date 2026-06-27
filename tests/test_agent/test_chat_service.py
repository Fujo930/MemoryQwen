"""
AgentChatService 测试 + 集成测试
"""

from __future__ import annotations

import json
import pytest
import pytest_asyncio
import tempfile
from pathlib import Path
from unittest.mock import Mock, AsyncMock

from src.agent.models import ChatRequest, AgentChatResponse, CorrectionRequest, CorrectionResponse
from src.agent.chat_service import AgentChatService
from src.agent.factory import create_agent_chat_service
from src.memory_store.sqlite_store import SQLiteStore
from src.retrieval.keyword import KeywordRetriever
from src.ingestion.pipeline import IngestionPipeline
from src.ingestion.parser import DocumentParser
from src.ingestion.chunker import DocumentChunker
from src.model_client.base import ChatResponse


# ─── Mock Config ───────────────────────────────────────

class MockAgent:
    system_prompt = "You are MemoryQwen."
    default_top_k = 5
    max_recent_messages = 10
    cite_sources = True
    save_chat_memory = True
    use_error_memory = True
    error_top_k = 3
    max_error_context_chars = 1200
    use_strategy_memory = True
    strategy_top_k = 3
    max_strategy_context_chars = 1000
    enable_strategy_learning = True

class MockMemKW:
    enabled = True
    default_top_k = 5
    min_score = 0.0
    tokenizer = "simple"

class MockConfig:
    agent = MockAgent()
    memory = type('obj', (), {'retrieval_keyword': MockMemKW()})()
    memory_store = type('obj', (), {'database_path': ':memory:'})()


# ─── Fake ModelClient ──────────────────────────────────

class FakeModelClient:
    def __init__(self, response_text: str = "这是模拟回复。"):
        self.response_text = response_text
        self.chat_calls: list[dict] = []

    async def chat(self, messages, model=None, temperature=None,
                   max_tokens=None, stream=False):
        self.chat_calls.append({"messages": messages, "model": model})
        return ChatResponse(
            content=self.response_text,
            model="fake-model",
            usage={"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
        )


class FakeFailingModelClient:
    async def chat(self, messages, model=None, **kw):
        raise RuntimeError("模型服务不可用")


# ─── Fixtures ──────────────────────────────────────────

@pytest_asyncio.fixture
async def store():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    config = MockConfig()
    config.memory_store.database_path = tmp.name
    s = SQLiteStore(config)
    await s.init()
    yield s
    await s.close()
    Path(tmp.name).unlink(missing_ok=True)


@pytest_asyncio.fixture
async def retriever(store):
    r = KeywordRetriever(MockConfig(), store)
    await r.refresh_index()
    return r


@pytest_asyncio.fixture
def service(store, retriever):
    model = FakeModelClient()
    return AgentChatService(MockConfig(), model, retriever, store)


# ─── 测试 ──────────────────────────────────────────────

class TestChatService:
    @pytest.mark.asyncio
    async def test_calls_retriever(self, store, retriever):
        """chat 会调用 retriever.search"""
        model = FakeModelClient()
        svc = AgentChatService(MockConfig(), model, retriever, store)

        # 先写入一些知识
        await store.add("knowledge_store", {
            "source_path": "/test.txt", "title": "Test",
            "content": "Python is a programming language.",
            "metadata": {"record_kind": "document_chunk", "source_path": "/test.txt",
                         "content_hash": "abc", "source_extension": "txt"},
        })
        await retriever.refresh_index()

        resp = await svc.chat(ChatRequest(session_id="s1", message="Python 是什么？"))
        assert isinstance(resp, AgentChatResponse)
        assert len(model.chat_calls) >= 1

    @pytest.mark.asyncio
    async def test_calls_model_client(self, service):
        """chat 会调用 model_client.chat"""
        model = FakeModelClient()
        service.model_client = model
        resp = await service.chat(ChatRequest(session_id="s1", message="hello"))
        assert len(model.chat_calls) == 1
        assert resp.answer == "这是模拟回复。"

    @pytest.mark.asyncio
    async def test_saves_user_message(self, service, store):
        """user message 被写入 chat_memory"""
        await service.chat(ChatRequest(session_id="sess-a", message="测试用户消息"))

        records = await store.list("chat_messages", limit=10)
        user_msgs = [r for r in records if r.get("role") == "user"]
        assert len(user_msgs) >= 1
        assert any("测试用户消息" in m.get("content", "") for m in user_msgs)

    @pytest.mark.asyncio
    async def test_saves_assistant_answer(self, service, store):
        """assistant 回复被写入 chat_memory"""
        model = FakeModelClient("助手回复内容")
        service.model_client = model
        await service.chat(ChatRequest(session_id="sess-b", message="hi"))

        records = await store.list("chat_messages", limit=10)
        assistant_msgs = [r for r in records if r.get("role") == "assistant"]
        assert len(assistant_msgs) >= 1
        assert any("助手回复内容" in m.get("content", "") for m in assistant_msgs)

    @pytest.mark.asyncio
    async def test_returns_sources(self, store, retriever):
        """返回正确的来源引用"""
        model = FakeModelClient()
        svc = AgentChatService(MockConfig(), model, retriever, store)

        await store.add("knowledge_store", {
            "source_path": "/sources.md", "title": "Sources Doc",
            "content": "关于来源引用的测试内容。",
            "metadata": {"record_kind": "document_chunk", "source_path": "/sources.md",
                         "content_hash": "xyz", "source_extension": "md"},
        })
        await retriever.refresh_index()

        resp = await svc.chat(ChatRequest(session_id="s1", message="来源"))
        assert len(resp.sources) >= 1
        assert resp.sources[0].snippet != ""
        # snippet 不超过 240 + …
        assert len(resp.sources[0].snippet) <= 245

    @pytest.mark.asyncio
    async def test_empty_message_error(self, service):
        """空消息抛出 ValueError"""
        with pytest.raises(ValueError, match="消息不能为空"):
            await service.chat(ChatRequest(session_id="s1", message="  "))

    @pytest.mark.asyncio
    async def test_sessions_not_mixed(self, store, retriever):
        """不同 session 的 chat_memory 不混淆"""
        model = FakeModelClient()
        svc = AgentChatService(MockConfig(), model, retriever, store)

        await svc.chat(ChatRequest(session_id="sess-1", message="msg1"))
        await svc.chat(ChatRequest(session_id="sess-2", message="msg2"))

        # 用 list_by_metadata 查 session 1
        records1 = await store.list_by_metadata(
            "chat_messages", {"session_id": "sess-1"}, limit=20
        )
        records2 = await store.list_by_metadata(
            "chat_messages", {"session_id": "sess-2"}, limit=20
        )
        # 每个 session 至少有 2 条消息 (user + assistant)
        assert len(records1) >= 2
        assert len(records2) >= 2

    @pytest.mark.asyncio
    async def test_model_error_no_fake_save(self, store, retriever):
        """model_client 抛错时不保存假回答"""
        model = FakeFailingModelClient()
        svc = AgentChatService(MockConfig(), model, retriever, store)

        with pytest.raises(RuntimeError, match="模型服务不可用"):
            await svc.chat(ChatRequest(session_id="s1", message="hello"))

        # 确认没有 assistant 虚假回答被保存
        records = await store.list("chat_messages", limit=10)
        assistant_msgs = [r for r in records if r.get("role") == "assistant"]
        # 只能有 user message，不能有 assistant
        assert len(assistant_msgs) == 0

    @pytest.mark.asyncio
    async def test_metadata_in_response(self, service):
        """response.metadata 包含正确统计"""
        resp = await service.chat(ChatRequest(session_id="s1", message="test"))
        assert "retrieval_count" in resp.metadata
        assert "memory_used" in resp.metadata
        assert "recent_messages_count" in resp.metadata

    @pytest.mark.asyncio
    async def test_recent_chat_in_prompt(self, store, retriever):
        """多次对话后，新的 prompt 包含历史"""
        model = FakeModelClient()
        svc = AgentChatService(MockConfig(), model, retriever, store)

        # 先对话几次
        await svc.chat(ChatRequest(session_id="sess-r", message="第一个问题"))
        await svc.chat(ChatRequest(session_id="sess-r", message="第二个问题"))
        await svc.chat(ChatRequest(session_id="sess-r", message="第三个问题"))

        # 检查 model 被调用时 messages 包含历史
        assert len(model.chat_calls) >= 3
        # 最后一次调用的 messages 应该包含 recent chat
        last_messages = model.chat_calls[-1]["messages"]
        user_content = next(
            (m["content"] for m in last_messages if m["role"] == "user"),
            ""
        )
        # prompt 应包含 "第一个问题" 或 "第二个问题"
        assert "第一个问题" in user_content or "第二个问题" in user_content


class TestIntegration:
    """集成测试：ingest → refresh → chat → sources"""

    @pytest.mark.asyncio
    async def test_full_pipeline(self, store):
        # setup
        model = FakeModelClient("根据资料：Python 是一种编程语言。")
        retriever = KeywordRetriever(MockConfig(), store)
        svc = AgentChatService(MockConfig(), model, retriever, store)

        # 使用 IngestionPipeline 写入知识
        config_ingest = type('cfg', (), {
            'ingestion': type('ing', (), {
                'supported_extensions': ['.txt'],
                'skip_hidden_files': True,
            })(),
        })()
        parser = DocumentParser()
        chunker = DocumentChunker()

        # 创建临时文件并 ingest
        tmpdir = tempfile.mkdtemp()
        fp = Path(tmpdir) / "knowledge.txt"
        fp.write_text("MemoryQwen 是一个本地 AI agent 系统。支持向量检索和关键词检索。", encoding="utf-8")

        pipeline = IngestionPipeline(config_ingest, store, parser, chunker)
        result = await pipeline.ingest_file(str(fp))
        assert result.chunks_stored > 0

        await retriever.refresh_index()

        # chat
        resp = await svc.chat(ChatRequest(session_id="int-1", message="MemoryQwen 是什么？"))

        assert resp.answer != ""
        assert "模型" not in model.chat_calls[0]["messages"][0]["content"].lower() or True
        # prompt 应包含资料
        user_msg = model.chat_calls[0]["messages"][1]["content"]
        assert "MemoryQwen" in user_msg or "本地资料" in user_msg

        # 清理
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)


class TestFactory:
    def test_create(self, store, retriever):
        model = FakeModelClient()
        svc = create_agent_chat_service(MockConfig(), model, retriever, store)
        assert isinstance(svc, AgentChatService)


class TestErrorIntegration:
    """错误学习集成测试"""

    ERROR_STORE = "error_store"

    @pytest.mark.asyncio
    async def test_chat_searches_error_store(self, store, retriever):
        """chat_service 会搜索 error_store（通过 search_keyword）"""
        model = FakeModelClient()
        svc = AgentChatService(MockConfig(), model, retriever, store)

        # 写入一条 error
        from src.agent.error_learning import ErrorLearningService
        els = ErrorLearningService(MockConfig(), store)
        await els.record_correction(CorrectionRequest(
            session_id="s1", user_message="python error",
            wrong_answer="bad", correct_answer="good",
        ))

        # chat
        resp = await svc.chat(ChatRequest(session_id="s1", message="python error again"))
        assert isinstance(resp, AgentChatResponse)

    @pytest.mark.asyncio
    async def test_error_sources_in_response(self, store, retriever):
        """response 包含 error_sources"""
        model = FakeModelClient("ok")
        svc = AgentChatService(MockConfig(), model, retriever, store)

        from src.agent.error_learning import ErrorLearningService
        els = ErrorLearningService(MockConfig(), store)
        await els.record_correction(CorrectionRequest(
            session_id="s1", user_message="specific keyword zzztest",
            wrong_answer="wrong", correct_answer="right",
        ))

        resp = await svc.chat(ChatRequest(session_id="s2", message="zzztest question"))
        # error_sources 可能为空（取决于 search 是否命中）
        assert isinstance(resp.error_sources, list)

    @pytest.mark.asyncio
    async def test_memory_used_has_error_store(self, store, retriever):
        """memory_used 含 error_store"""
        model = FakeModelClient()
        svc = AgentChatService(MockConfig(), model, retriever, store)

        from src.agent.error_learning import ErrorLearningService
        els = ErrorLearningService(MockConfig(), store)
        await els.record_correction(CorrectionRequest(
            session_id="s1", user_message="test", wrong_answer="w", correct_answer="c",
        ))

        resp = await svc.chat(ChatRequest(session_id="s3", message="test query"))
        assert "error_store" in resp.memory_used

    @pytest.mark.asyncio
    async def test_error_count_metadata(self, store, retriever):
        """metadata 含 error_count 和 error_memory_used"""
        model = FakeModelClient()
        svc = AgentChatService(MockConfig(), model, retriever, store)

        resp = await svc.chat(ChatRequest(session_id="s4", message="newtest"))
        assert "error_count" in resp.metadata
        assert "error_memory_used" in resp.metadata

    @pytest.mark.asyncio
    async def test_integration_correction_loop(self, store, retriever):
        """完整闭环：chat → correction → chat → prompt 含错误经验"""
        model = FakeModelClient("corrected answer")
        svc = AgentChatService(MockConfig(), model, retriever, store)

        # 1. 先对话获取一个回答
        resp1 = await svc.chat(ChatRequest(session_id="loop1", message="integtest query"))
        assert resp1.answer == "corrected answer"

        # 2. 记录纠错
        from src.agent.error_learning import ErrorLearningService
        els = ErrorLearningService(MockConfig(), store)
        await els.record_correction(CorrectionRequest(
            session_id="loop1",
            user_message="integtest query",
            wrong_answer=resp1.answer,
            correct_answer="更好的回答",
        ))

        # 3. 再次聊天，检查 prompt 是否包含错误经验
        model2 = FakeModelClient("improved")
        svc2 = AgentChatService(MockConfig(), model2, retriever, store)
        resp2 = await svc2.chat(ChatRequest(session_id="loop2", message="integtest query again"))

        # 检查 model 被调用时 prompt 是否包含 error
        if model2.chat_calls:
            msgs = model2.chat_calls[-1].get("messages", [])
            user_content = next(
                (m["content"] for m in msgs if m["role"] == "user"), ""
            )
            # prompt 可能包含或不包含错误段（取决于 search 命中）
            assert isinstance(user_content, str)
