"""
MemoryQwen — Eval Report Writer
"""

from __future__ import annotations
import json, os
from pathlib import Path
from collections import defaultdict
from src.eval_runner.models import EvalReport, EvalResult


def write_json(report: EvalReport, output_dir: str | Path) -> str:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    fp = out / f"{report.run_id}.json"
    data = _report_to_dict(report)
    fp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(fp)


def write_markdown(report: EvalReport, output_dir: str | Path) -> str:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    fp = out / f"{report.run_id}.md"
    md = _report_to_md(report)
    fp.write_text(md, encoding="utf-8")
    return str(fp)


def load_json(file_path: str | Path) -> EvalReport | None:
    try:
        data = json.loads(Path(file_path).read_text(encoding="utf-8"))
        return _dict_to_report(data)
    except Exception:
        return None


def mark_result(report: EvalReport, question_id: str, correctness: str,
                failure_type: str = "", notes: str = "") -> EvalReport:
    """Update a single result's judgement."""
    for r in report.results:
        if r.question.question_id == question_id:
            r.judgement.correctness = correctness
            r.judgement.failure_type = failure_type
            r.judgement.notes = notes
            r.judgement.correction_needed = correctness in ("wrong", "partial")
    # Re-compute
    report.correct = sum(1 for r in report.results if r.judgement.correctness == "correct")
    report.partial = sum(1 for r in report.results if r.judgement.correctness == "partial")
    report.wrong = sum(1 for r in report.results if r.judgement.correctness == "wrong")
    report.unjudged = report.total_questions - report.correct - report.partial - report.wrong
    return report


def _report_to_dict(r: EvalReport) -> dict:
    return {
        "run_id": r.run_id,
        "started_at": r.started_at,
        "completed_at": r.completed_at,
        "total_questions": r.total_questions,
        "correct": r.correct, "partial": r.partial, "wrong": r.wrong, "unjudged": r.unjudged,
        "source_hit_rate": r.source_hit_rate,
        "guard_trigger_rate": r.guard_trigger_rate,
        "metadata": r.metadata,
        "results": [
            {
                "question_id": x.question.question_id,
                "topic": x.question.topic,
                "question": x.question.question,
                "expected_answer": x.question.expected_answer,
                "expected_sources": x.question.expected_sources,
                "failure_type_if_wrong": x.question.failure_type_if_wrong,
                "guard_expected": x.question.guard_expected,
                "answer": x.answer.answer,
                "sources": x.answer.sources,
                "source_hit": x.answer.source_hit,
                "guard_triggered": x.answer.guard_triggered,
                "metadata": x.answer.metadata,
                "judgement": {
                    "correctness": x.judgement.correctness,
                    "notes": x.judgement.notes,
                    "failure_type": x.judgement.failure_type,
                    "correction_needed": x.judgement.correction_needed,
                }
            }
            for x in r.results
        ]
    }


def _dict_to_report(d: dict) -> EvalReport:
    from src.eval_runner.models import EvalQuestion, EvalAnswer, EvalJudgement, EvalResult
    results = []
    for rd in d.get("results", []):
        q = EvalQuestion(
            question_id=rd["question_id"], topic=rd.get("topic",""),
            question=rd["question"], expected_answer=rd.get("expected_answer",""),
            expected_sources=rd.get("expected_sources", []),
            failure_type_if_wrong=rd.get("failure_type_if_wrong", ""),
            guard_expected=rd.get("guard_expected"),
        )
        a = EvalAnswer(
            question_id=rd["question_id"], answer=rd["answer"], sources=rd.get("sources",[]),
            metadata=rd.get("metadata",{}), source_hit=rd.get("source_hit",False),
            guard_triggered=rd.get("guard_triggered",False),
        )
        jd = rd.get("judgement", {})
        j = EvalJudgement(
            correctness=jd.get("correctness","unjudged"),
            notes=jd.get("notes",""), failure_type=jd.get("failure_type",""),
            correction_needed=jd.get("correction_needed", False),
        )
        results.append(EvalResult(question=q, answer=a, judgement=j))
    return EvalReport(
        run_id=d["run_id"], started_at=d.get("started_at",""), completed_at=d.get("completed_at",""),
        total_questions=d["total_questions"],
        correct=d.get("correct",0), partial=d.get("partial",0), wrong=d.get("wrong",0),
        unjudged=d.get("unjudged",0), source_hit_rate=d.get("source_hit_rate",0),
        guard_trigger_rate=d.get("guard_trigger_rate",0), results=results,
    )


def _report_to_md(r: EvalReport) -> str:
    md = f"""# Eval Run Report

## Summary
- run_id: {r.run_id}
- total_questions: {r.total_questions}
- correct: {r.correct}
- partial: {r.partial}
- wrong: {r.wrong}
- unjudged: {r.unjudged}
- source_hit_rate: {r.source_hit_rate:.1%}
- guard_trigger_rate: {r.guard_trigger_rate:.1%}

## Topic Breakdown

| topic | total | correct | partial | wrong | unjudged |
|-------|-------|---------|---------|-------|----------|
"""
    by_topic = defaultdict(lambda: {"total":0,"correct":0,"partial":0,"wrong":0,"unjudged":0})
    for x in r.results:
        t = x.question.topic or "unknown"
        by_topic[t]["total"] += 1
        c = x.judgement.correctness
        if c == "correct": by_topic[t]["correct"] += 1
        elif c == "partial": by_topic[t]["partial"] += 1
        elif c == "wrong": by_topic[t]["wrong"] += 1
        else: by_topic[t]["unjudged"] += 1

    for t, s in by_topic.items():
        md += f"| {t} | {s['total']} | {s['correct']} | {s['partial']} | {s['wrong']} | {s['unjudged']} |\n"

    md += "\n## Results\n\n"
    for x in r.results:
        md += f"### {x.question.question_id} ({x.question.topic})\n"
        md += f"- question: {x.question.question}\n"
        md += f"- expected: {x.question.expected_answer}\n"
        md += f"- answer: {x.answer.answer[:300]}\n"
        md += f"- sources: {', '.join(x.answer.sources[:5])}\n"
        md += f"- source_hit: {x.answer.source_hit}\n"
        md += f"- guard_triggered: {x.answer.guard_triggered}\n"
        md += f"- judgement: {x.judgement.correctness}"
        if x.judgement.notes:
            md += f" ({x.judgement.notes})"
        md += "\n\n"
    return md
