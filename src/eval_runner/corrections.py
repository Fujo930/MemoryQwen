"""
MemoryQwen — Eval Correction Export
Exports correction draft commands from eval reports.
"""
import shlex
from dataclasses import dataclass, field
from pathlib import Path

from src.eval_runner.report import load_json
from src.eval_runner.models import EvalReport


@dataclass
class CorrectionExportResult:
    exported_count: int = 0
    skipped_count: int = 0
    output_path: str = ""
    warnings: list[str] = field(default_factory=list)


def export_correction_drafts(
    report_path: str | Path,
    output_path: str | Path,
    include_partial: bool = False,
    output_format: str = "markdown",
    failure_type_default: str = "hallucination",
) -> CorrectionExportResult:
    """Export correction drafts for wrong/partial results."""
    report = load_json(report_path)
    if not report:
        return CorrectionExportResult(
            warnings=["Report not found: {}".format(report_path)]
        )

    result = CorrectionExportResult()
    items = []

    for r in report.results:
        c = r.judgement.correctness
        if c == "correct" or c == "unjudged":
            continue
        if c == "partial" and not include_partial:
            continue

        wrong_text = r.answer.answer.strip()
        correct_text = r.question.expected_answer.strip()

        if not correct_text:
            result.skipped_count += 1
            result.warnings.append(f"Skipped {r.question.question_id}: missing expected_answer")
            continue
        if not wrong_text:
            result.skipped_count += 1
            result.warnings.append(f"Skipped {r.question.question_id}: missing actual_answer")
            continue

        failure_type = (r.judgement.failure_type or
                        r.question.failure_type_if_wrong or
                        failure_type_default)
        # Ensure empty strings don't override
        if not failure_type or failure_type.strip() == "":
            failure_type = failure_type_default

        items.append({
            "question_id": r.question.question_id,
            "topic": r.question.topic,
            "question": r.question.question,
            "expected_answer": correct_text,
            "actual_answer": wrong_text[:500],
            "full_actual_answer": wrong_text,
            "failure_type": failure_type,
            "notes": r.judgement.notes,
        })
        result.exported_count += 1

    # Write output
    out = Path(output_path)
    if output_format == "bash":
        _write_bash(out, items)
    else:
        _write_markdown(out, report.run_id, items)

    result.output_path = str(out)
    return result


def _write_markdown(path: Path, run_id: str, items: list[dict]):
    md = f"# Eval Correction Drafts\n\nrun_id: {run_id}\ngenerated_at: auto\nitems: {len(items)}\n\n"
    for it in items:
        md += f"## {it['question_id']}\n\n"
        md += f"topic: {it['topic']}\n"
        md += f"question: {it['question']}\n"
        md += f"expected_answer: {it['expected_answer']}\n"
        md += f"actual_answer: {it['actual_answer']}\n"
        md += f"failure_type: {it['failure_type']}\n"
        md += f"notes: {it['notes']}\n\n"
        md += "**Suggested command:**\n\n"
        w = shlex.quote(it["full_actual_answer"][:300])
        c = shlex.quote(it["expected_answer"][:300])
        md += f"```bash\npython -m src.cli correct --wrong {w} --correct {c} --failure-type {it['failure_type']}\n```\n\n"
    path.write_text(md, encoding="utf-8")


def _write_bash(path: Path, items: list[dict]):
    lines = ["# Eval Correction Drafts — Review before running.", ""]
    for it in items:
        w = shlex.quote(it["full_actual_answer"][:300])
        c = shlex.quote(it["expected_answer"][:300])
        lines.append(f"python -m src.cli correct --wrong {w} --correct {c} --failure-type {it['failure_type']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
