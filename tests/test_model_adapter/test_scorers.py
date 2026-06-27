"""
Scorer 测试
"""

from src.model_adapter.scorers import (
    score_json_validity,
    score_chinese_response,
    score_citation_format,
    score_tool_call_json,
    score_simple_reasoning,
    score_context_recall,
)


class TestJsonScorer:
    def test_valid_json(self):
        assert score_json_validity('{"answer": "ok", "confidence": 0.8}') == 1.0

    def test_invalid_json(self):
        assert score_json_validity("not json at all") == 0.0

    def test_json_in_codeblock(self):
        out = '''好的：\n```json\n{"answer": "ok", "confidence": 0.8}\n```'''
        assert score_json_validity(out) == 1.0

    def test_json_embedded(self):
        out = '结果是 {"answer": "ok", "confidence": 0.9}，确认成功。'
        assert score_json_validity(out) == 1.0

    def test_json_no_answer_field(self):
        assert score_json_validity('{"other": 1}') == 0.5


class TestChineseScorer:
    def test_high_chinese(self):
        out = "机器学习是人工智能的一个重要分支，通过对大量数据的学习使计算机具备预测和决策能力。"
        assert score_chinese_response(out) > 0.5

    def test_low_chinese(self):
        out = "hello world"
        assert score_chinese_response(out) < 0.3


class TestCitationScorer:
    def test_hit(self):
        assert score_citation_format("根据[S1]的说明，答案是...") == 1.0

    def test_miss(self):
        assert score_citation_format("答案是地球") == 0.0


class TestToolScorer:
    def test_valid_tool(self):
        out = '{"tool": "search_memory", "arguments": {"query": "test"}}'
        assert score_tool_call_json(out) == 1.0

    def test_partial_tool(self):
        out = '{"tool": "search_memory"}'
        assert score_tool_call_json(out) == 0.3

    def test_codeblock_tool(self):
        out = '```json\n{"tool": "search_memory", "arguments": {"query": "test"}}\n```'
        assert score_tool_call_json(out) == 1.0


class TestReasoningScorer:
    def test_correct_4(self):
        assert score_simple_reasoning("4") == 1.0

    def test_correct_text(self):
        assert score_simple_reasoning("答案是 4 个苹果") == 1.0

    def test_wrong_5(self):
        assert score_simple_reasoning("5") == 0.0

    def test_negated(self):
        assert score_simple_reasoning("答案是 3，不是 4") == 0.0

    def test_not_4(self):
        assert score_simple_reasoning("不是4") == 0.0

    def test_four_chinese(self):
        assert score_simple_reasoning("四个") == 1.0


class TestContextScorer:
    def test_hit(self):
        assert score_context_recall("代号是 BLUE-RABBIT") == 1.0

    def test_miss(self):
        assert score_context_recall("不知道") == 0.0
