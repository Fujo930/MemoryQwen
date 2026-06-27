"""Eval Correction Export Tests (≥13)"""
import tempfile
from pathlib import Path

from src.eval_runner.models import (
    EvalQuestion, EvalAnswer, EvalJudgement, EvalResult, EvalReport,
)
from src.eval_runner.report import write_json
from src.eval_runner.corrections import export_correction_drafts, CorrectionExportResult


def _make_report(items: list[EvalResult]) -> str:
    d = tempfile.mkdtemp()
    r = EvalReport(run_id="test", total_questions=len(items), results=items)
    return write_json(r, d)


def _result(qid, correctness, expected="", answer="", failure_type="",
            question_failure=""):
    q = EvalQuestion(
        question_id=qid, topic="test", question="test question?",
        expected_answer=expected, failure_type_if_wrong=question_failure,
    )
    a = EvalAnswer(question_id=qid, answer=answer)
    j = EvalJudgement(correctness=correctness, failure_type=failure_type)
    return EvalResult(question=q, answer=a, judgement=j)


class TestExport:
    def test_wrong_items_only(self):
        fp = _make_report([
            _result("Q1", "wrong", expected="correct ans", answer="wrong ans", failure_type="hallucination"),
            _result("Q2", "correct", expected="yes", answer="yes"),
        ])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out)
        assert r.exported_count == 1

    def test_include_partial(self):
        fp = _make_report([
            _result("Q1", "wrong", expected="e", answer="w", failure_type="x"),
            _result("Q2", "partial", expected="e2", answer="w2"),
        ])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out, include_partial=True)
        assert r.exported_count == 2

    def test_does_not_export_correct(self):
        fp = _make_report([_result("Q1", "correct", expected="e", answer="y")])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out)
        assert r.exported_count == 0

    def test_does_not_export_unjudged(self):
        fp = _make_report([_result("Q1", "unjudged", expected="e", answer="y")])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out)
        assert r.exported_count == 0

    def test_skips_missing_expected_answer(self):
        fp = _make_report([_result("Q1", "wrong", expected="", answer="wrong")])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out)
        assert r.exported_count == 0
        assert r.skipped_count == 1

    def test_uses_judgement_failure_type(self):
        fp = _make_report([_result("Q1", "wrong", expected="e", answer="w",
                                    failure_type="custom_type", question_failure="qtype")])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out)
        content = Path(r.output_path).read_text(encoding="utf-8")
        assert "custom_type" in content

    def test_falls_back_to_question_failure_type(self):
        fp = _make_report([_result("Q1", "wrong", expected="e", answer="w",
                                    failure_type="", question_failure="question_fallback")])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out)
        content = Path(r.output_path).read_text(encoding="utf-8")
        assert "question_fallback" in content

    def test_falls_back_to_default_failure_type(self):
        fp = _make_report([_result("Q1", "wrong", expected="e", answer="w")])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out, failure_type_default="default_type")
        content = Path(r.output_path).read_text(encoding="utf-8")
        assert "default_type" in content

    def test_writes_markdown_export(self):
        fp = _make_report([_result("Q1", "wrong", expected="correct", answer="wrong")])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out, output_format="markdown")
        content = Path(r.output_path).read_text(encoding="utf-8")
        assert "## Q1" in content
        assert "Suggested command" in content
        assert "python -m src.cli correct" in content

    def test_writes_bash_export(self):
        fp = _make_report([_result("Q1", "wrong", expected="correct", answer="wrong")])
        out = tempfile.mktemp(suffix=".sh")
        r = export_correction_drafts(fp, out, output_format="bash")
        content = Path(r.output_path).read_text(encoding="utf-8")
        assert "python -m src.cli correct" in content
        assert "Review" in content

    def test_export_does_not_modify_report(self):
        fp = _make_report([_result("Q1", "wrong", expected="e", answer="w")])
        original = Path(fp).read_text(encoding="utf-8")
        out = tempfile.mktemp(suffix=".md")
        export_correction_drafts(fp, out)
        after = Path(fp).read_text(encoding="utf-8")
        assert original == after

    def test_shell_quotes_special_chars(self):
        fp = _make_report([_result("Q1", "wrong",
                                    expected="correct 'answer'",
                                    answer='wrong "answer" with $dollar')])
        out = tempfile.mktemp(suffix=".md")
        r = export_correction_drafts(fp, out)
        content = Path(r.output_path).read_text(encoding="utf-8")
        # Should contain shell-quoted strings
        assert "correct" in content
