"""
PromptBuilder 测试
"""

import pytest
from src.agent.prompt_builder import PromptBuilder
from src.retrieval.models import RetrievalResult

SYSTEM = "你是 MemoryQwen。"


@pytest.fixture
def builder():
    return PromptBuilder(SYSTEM)


class TestPromptStructure:
    def test_has_system_first(self, builder):
        msgs = builder.build("hello")
        assert msgs[0]["role"] == "system"
        assert msgs[0]["content"] == SYSTEM

    def test_has_user_message_last(self, builder):
        msgs = builder.build("hello")
        assert msgs[-1]["role"] == "user"
        content = msgs[-1]["content"]
        assert "用户问题" in content
        assert "hello" in content

    def test_no_sources_still_works(self, builder):
        msgs = builder.build("test", retrieved=[])
        assert len(msgs) == 2
        assert "本地资料" not in msgs[1]["content"]


class TestSourceCitation:
    def test_sources_numbered(self, builder):
        retrieved = [
            RetrievalResult(
                record_id="a", title="DocA", content="Content A",
                source_path="/a.txt", chunk_index=0, total_chunks=1,
            ),
            RetrievalResult(
                record_id="b", title="DocB", content="Content B",
                source_path="/b.txt", chunk_index=1, total_chunks=3,
            ),
        ]
        msgs = builder.build("query", retrieved=retrieved)
        user_content = msgs[1]["content"]
        assert "[S1]" in user_content
        assert "[S2]" in user_content
        assert "Content A" in user_content
        assert "Content B" in user_content
        assert "/a.txt" in user_content or "a.txt" in user_content
        # 验证切片信息
        assert "2/3" in user_content or "1/3" in user_content

    def test_snippet_truncated(self, builder):
        long_text = "x" * 500
        retrieved = [RetrievalResult(record_id="a", content=long_text, source_path="/a.txt")]
        msgs = builder.build("q", retrieved=retrieved)
        user_content = msgs[1]["content"]
        # 截断符号出现
        assert "…" in user_content
        assert len([c for c in user_content if c == "x"]) < 500


class TestRecentChat:
    def test_recent_chat_in_prompt(self, builder):
        recent = [
            {"role": "user", "content": "之前的问题"},
            {"role": "assistant", "content": "之前的回答"},
        ]
        msgs = builder.build("新问题", recent_chat=recent)
        user_content = msgs[1]["content"]
        assert "最近对话" in user_content
        assert "之前的问题" in user_content
        assert "之前的回答" in user_content


class TestErrorContext:
    def test_error_section_present(self, builder):
        """注入 error cases"""
        error_cases = [{
            "failure_type": "math_error",
            "wrong_answer": "1+1=3",
            "correct_answer": "1+1=2",
            "strategy": "使用计算器验证",
        }]
        msgs = builder.build("query", error_cases=error_cases)
        user_content = msgs[1]["content"]
        assert "过去类似错误" in user_content
        assert "[E1]" in user_content
        assert "math_error" in user_content
        assert "1+1=3" in user_content
        assert "1+1=2" in user_content

    def test_no_error_section_when_empty(self, builder):
        """无 error cases 时不显示错误段"""
        msgs = builder.build("query", error_cases=[])
        user_content = msgs[1]["content"]
        assert "过去类似错误" not in user_content

    def test_error_truncation(self, builder):
        """错误片段截断"""
        error_cases = [{
            "failure_type": "test",
            "wrong_answer": "x" * 300,
            "correct_answer": "y" * 300,
            "strategy": "z" * 500,
        }]
        msgs = builder.build("query", error_cases=error_cases)
        user_content = msgs[1]["content"]
        # wrong/correct 截断到 200，strategy 截断到 300
        assert "…" in user_content


class TestStrategyContext:
    def test_strategy_section(self, builder):
        strategy_cases = [{
            "strategy": "使用计算器验证数学结果",
            "failure_type": "math_error",
            "avoid": "1+1=3",
            "prefer": "1+1=2",
        }]
        msgs = builder.build("query", strategy_cases=strategy_cases)
        user_content = msgs[1]["content"]
        assert "可复用策略" in user_content
        assert "[T1]" in user_content
        assert "math_error" in user_content
        assert "使用计算器验证" in user_content

    def test_no_strategy_when_empty(self, builder):
        msgs = builder.build("query", strategy_cases=[])
        user_content = msgs[1]["content"]
        assert "可复用策略" not in user_content

    def test_strategy_order(self, builder):
        """验证顺序：资料 → 错误 → 策略 → 对话 → 问题"""
        from src.retrieval.models import RetrievalResult
        retrieved = [RetrievalResult(record_id="a", content="资料内容")]
        error_cases = [{"failure_type": "e", "wrong_answer": "w", "correct_answer": "c", "strategy": "s"}]
        strategy_cases = [{"strategy": "策略", "failure_type": "t"}]
        recent = [{"role": "user", "content": "对话"}]
        msgs = builder.build("问题", retrieved=retrieved, error_cases=error_cases,
                              strategy_cases=strategy_cases, recent_chat=recent)
        content = msgs[1]["content"]
        # 最近对话 now comes right after capability baseline, before local sources
        assert content.index("最近对话") < content.index("本地资料") < content.index("过去类似错误") < content.index("可复用策略") < content.index("用户问题")