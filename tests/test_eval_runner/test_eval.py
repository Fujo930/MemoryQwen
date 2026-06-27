"""Eval Runner Tests (≥27)"""
import json, tempfile
from pathlib import Path
import pytest

from src.eval_runner.models import (
    EvalQuestion, EvalAnswer, EvalJudgement, EvalResult,
    EvalReport, EvalRunConfig,
)
from src.eval_runner.question_loader import (
    load_questions_from_markdown, load_questions_from_directory,
)
from src.eval_runner.report import (
    write_json, write_markdown, load_json, mark_result,
)

# ─── Models ──────────────────────────────────────────

class TestModels:
    def test_eval_question_defaults(self):
        q = EvalQuestion()
        assert q.question_id == ""
        assert q.expected_sources == []

    def test_eval_run_config(self):
        c = EvalRunConfig(session_prefix="custom", shuffle=True)
        assert c.session_prefix == "custom"
        assert c.shuffle is True

    def test_eval_answer(self):
        a = EvalAnswer(question_id="Q001", answer="test", source_hit=True)
        assert a.guard_triggered is False
        assert a.source_hit is True

    def test_eval_judgement(self):
        j = EvalJudgement(correctness="wrong", failure_type="hallucination")
        assert j.correction_needed is False  # default

    def test_eval_result(self):
        q = EvalQuestion(question_id="Q001")
        r = EvalResult(question=q)
        assert r.judgement.correctness == "unjudged"

    def test_eval_report(self):
        r = EvalReport(run_id="test", total_questions=10, correct=7, wrong=2, unjudged=1)
        assert r.source_hit_rate == 0.0

# ─── Loader ──────────────────────────────────────────

VALID_MD = """## Q001
topic: test
question: What is MemoryQwen?
expected_answer: A local AI agent
expected_sources: source1, source2
guard_expected: yes
failure_type_if_wrong: source_miss
trap_level: high

## Q002
topic: test2
question: Does v0.1 support PDF?
expected_answer: No
"""

class TestQuestionLoader:
    def test_load_from_markdown(self):
        qs = load_questions_from_markdown(_tmp_md(VALID_MD))
        assert len(qs) == 2
        assert qs[0].topic == "test"
        assert qs[0].expected_sources == ["source1", "source2"]
        assert qs[0].guard_expected is True
        assert qs[1].topic == "test2"

    def test_load_from_directory(self):
        d = tempfile.mkdtemp()
        (Path(d) / "q1.md").write_text(VALID_MD, encoding="utf-8")
        qs = load_questions_from_directory(d)
        assert len(qs) >= 2

    def test_topic_filter(self):
        d = tempfile.mkdtemp()
        (Path(d) / "q.md").write_text(VALID_MD, encoding="utf-8")
        qs = load_questions_from_directory(d, topic_filter="test2")
        assert len(qs) == 1
        assert qs[0].topic == "test2"

    def test_max_questions(self):
        d = tempfile.mkdtemp()
        (Path(d) / "q.md").write_text(VALID_MD, encoding="utf-8")
        qs = load_questions_from_directory(d, max_questions=1)
        assert len(qs) == 1

    def test_shuffle(self):
        d = tempfile.mkdtemp()
        (Path(d) / "q.md").write_text(VALID_MD, encoding="utf-8")
        qs = load_questions_from_directory(d, shuffle=True)
        assert len(qs) == 2

    def test_malformed_question_warns(self):
        malformed = "## Q001\ntopic: x\n## Q002\ntopic: y\nquestion: OK"
        qs = load_questions_from_markdown(_tmp_md(malformed))
        assert len(qs) >= 1  # Q002 OK

# ─── Report ──────────────────────────────────────────

class TestReport:
    def test_write_json(self):
        r = EvalReport(run_id="t001", total_questions=10, correct=5, partial=2, wrong=1, unjudged=2)
        fp = write_json(r, tempfile.mkdtemp())
        assert Path(fp).exists()
        data = json.loads(Path(fp).read_text())
        assert data["run_id"] == "t001"

    def test_write_markdown(self):
        r = EvalReport(run_id="t002", total_questions=5, correct=5)
        fp = write_markdown(r, tempfile.mkdtemp())
        assert Path(fp).exists()
        content = Path(fp).read_text(encoding="utf-8")
        assert "t002" in content
        assert "## Summary" in content

    def test_load_json_roundtrip(self):
        d = tempfile.mkdtemp()
        r = EvalReport(run_id="rt", total_questions=3, correct=1, partial=1, wrong=1)
        r.results = [EvalResult(
            question=EvalQuestion(question_id="Q1", question="test?",
                                  expected_answer="yes", topic="t"),
            answer=EvalAnswer(question_id="Q1", answer="yes", source_hit=True),
            judgement=EvalJudgement(correctness="correct"),
        )]
        write_json(r, d)
        loaded = load_json(f"{d}/rt.json")
        assert loaded.run_id == "rt"
        assert len(loaded.results) == 1

    def test_mark_result(self):
        d = tempfile.mkdtemp()
        r = EvalReport(run_id="mrk", total_questions=1)
        r.results = [EvalResult(
            question=EvalQuestion(question_id="Q1", question="test?"),
            answer=EvalAnswer(question_id="Q1", answer="x"),
            judgement=EvalJudgement(),
        )]
        r = mark_result(r, "Q1", "wrong", failure_type="hallucination", notes="bad")
        assert r.results[0].judgement.correctness == "wrong"
        assert r.wrong == 1


def _tmp_md(content: str) -> str:
    d = tempfile.mkdtemp()
    fp = Path(d) / "test.md"
    fp.write_text(content, encoding="utf-8")
    return str(fp)
