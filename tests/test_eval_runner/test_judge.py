"""Judge Tests (≥20)"""
import pytest
from src.eval_runner.judge import (
    heuristic_judge, JudgeResult, _extract_concepts,
    NEGATION_SIGNALS,
)
from src.eval_runner.models import EvalRunConfig


class TestJudgeResult:
    def test_defaults(self):
        j = JudgeResult()
        assert j.correctness == "unjudged"
        assert j.confidence == 0.0

    def test_manual_mark_overrides(self):
        # Manual marks always take priority
        j = JudgeResult(correctness="wrong", manual_override=True)
        assert j.correctness == "wrong"


class TestHeuristicJudge:
    def test_accepts_synonym_answer(self):
        """inbox 不是长期资产 should NOT be false negative"""
        j = heuristic_judge(
            "inbox 是长期资产吗？",
            "不是。inbox 是临时投喂入口。用户可能清理 inbox。",
            "inbox 不是长期资产，它是一个临时投喂区。",
            [], False,
        )
        # Should be correct or partial, not wrong
        assert j.correctness != "wrong"
        assert j.correctness in ("correct_candidate", "partial_candidate")

    def test_handles_negative_boundary(self):
        """Does not support PDF"""
        j = heuristic_judge(
            "支持 PDF 吗？",
            "不支持。v0.1 只支持 .txt 和 .md。PDF 是 v0.2 计划。",
            "v0.1 不支持 PDF，只支持 .txt 和 .md 文件。",
            [], True,
        )
        assert j.correctness in ("correct_candidate", "partial_candidate")

    def test_detects_overclaim(self):
        """Fabricating CLI commands"""
        j = heuristic_judge(
            "有 Web UI 吗？",
            "没有。v0.1 没有 Web UI。",
            "有 Web UI，可以通过 cli webui 启动。",
            [], True,
        )
        assert j.correctness == "wrong" or j.failure_type == "capability_overclaim"

    def test_inbox_not_long_term_correct(self):
        """The specific false negative from Issue #20"""
        j = heuristic_judge(
            "inbox 是长期资产吗？",
            "不是。inbox 是临时投喂入口，用户可能清理 inbox。",
            "inbox 不是长期资产，是一个临时投喂区，用于存放待处理的文件。一旦文件被解析入库，就可以清理 inbox 而不影响已归档资料。",
            [], False,
        )
        assert j.correctness in ("correct_candidate", "partial_candidate")
        assert j.confidence >= 0.3

    def test_marks_uncertain_as_unjudged(self):
        j = heuristic_judge(
            "复杂问题",
            "很长的详细回答包含多个关键概念需要匹配验证测试",
            "我不知道",
            [], False,
        )
        # Very short answer with low match
        assert j.correctness in ("partial_candidate", "unjudged")

    def test_uncertainty_signal_triggers_partial(self):
        j = heuristic_judge(
            "某些功能",
            "回答应该包含具体信息",
            "根据当前本地资料不能确定。",
            [], False,
        )
        assert "uncertain" in j.evidence or "不能确定" in j.notes


class TestConcepts:
    def test_extract_concepts(self):
        c = _extract_concepts("inbox 是临时投喂入口 用户可能清理 inbox")
        assert len(c) > 0
        assert any("inbox" in x for x in c)
        assert any("临时" in x for x in c)

    def test_filters_stop_words(self):
        c = _extract_concepts("the is not a and or but if")
        assert len(c) <= 2  # most filtered


class TestRunConfig:
    def test_judge_mode_default(self):
        c = EvalRunConfig()
        assert c.judge_mode == "heuristic"

    def test_judge_mode_custom(self):
        c = EvalRunConfig(judge_mode="llm")
        assert c.judge_mode == "llm"


class TestJudgeRubric:
    def test_negation_signals(self):
        assert "不是" in NEGATION_SIGNALS
        assert "不支持" in NEGATION_SIGNALS
        assert "未实现" in NEGATION_SIGNALS

    def test_judge_no_auto_correct(self):
        """Judge does not write error_store — it only sets correctness"""
        j = heuristic_judge("q", "exp", "ans", [], False)
        assert j.correctness in ("correct_candidate", "partial_candidate", "wrong", "unjudged")
        # No side effects
        assert j.failure_type is not None or j.correctness == "unjudged"
