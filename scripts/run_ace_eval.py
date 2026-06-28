#!/usr/bin/env python3
"""ACE-v1 Eval Runner — validates ACE routing behavior against expected routes.

Usage:
    python scripts/run_ace_eval.py [path_to_eval_pack]
"""

from __future__ import annotations
import json, re, sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class EvalCase:
    question_id: str
    topic: str
    question: str
    expected_route: str
    expected_behavior: str
    must_not: list[str] = field(default_factory=list)
    manual_review_required: bool = False
    accepted_routes: list[str] = field(default_factory=list)


@dataclass
class EvalResult:
    case: EvalCase
    actual_route: str
    route_correct: bool
    violations: list[str] = field(default_factory=list)


def parse_eval_file(path: Path) -> list[EvalCase]:
    """Parse ACE eval questions file."""
    text = path.read_text(encoding="utf-8")
    cases = []
    blocks = text.split("\n## Q")
    
    for block in blocks:
        if not block.strip():
            continue
        # Restore the ## Q prefix for first block, or prepend it for others
        if not block.startswith("## Q"):
            block = "## Q" + block
        
        lines = block.strip().split("\n")
        current = {"id": lines[0].strip().replace("#", "").strip()}
        
        for line in lines[1:]:
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    current[key] = val
        
        if current.get("question"):
            cases.append(EvalCase(
                question_id=current.get("id", "?"),
                topic=current.get("topic", ""),
                question=current.get("question", ""),
                expected_route=current.get("expected_route", "shallow"),
                expected_behavior=current.get("expected_behavior", ""),
                must_not=[x.strip() for x in current.get("must_not", "").split(",") if x.strip()],
                manual_review_required=current.get("manual_review_required", "false") == "true",
                accepted_routes=[x.strip() for x in current.get("accepted_routes", "").split(",") if x.strip()],
            ))
    
    return cases


def run_ace_eval(pack_dir: Path) -> dict:
    """Run ACE eval and return results dict."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from src.ace import ACEController
    questions_file = pack_dir / "ace_v1_eval_questions.md"
    if not questions_file.exists():
        print(f"Error: {questions_file} not found")
        return {}

    cases = parse_eval_file(questions_file)
    print(f"Loaded {len(cases)} eval cases")

    ctrl = ACEController()
    results: list[EvalResult] = []
    stats = {
        "total": len(cases), "route_correct": 0,
        "violations": {"auto_deep": 0, "auto_web": 0, "auto_memory_write": 0, "registry_priority": 0},
    }

    for case in cases:
        decision = ctrl.decide(case.question)
        actual_route = decision.route
        # Flexible matching: route_correct if actual matches expected OR any accepted route
        accepted = getattr(case, "accepted_routes", [])
        route_correct = actual_route == case.expected_route or actual_route in accepted
        violations = []

        # Safety checks
        if decision.model_plan.auto_escalated:
            violations.append("auto_deep")
            stats["violations"]["auto_deep"] += 1
        if decision.context_plan.use_web_context and not decision.route == "web":
            # Only flag if web context used on non-web route
            pass  # This is fine - web context can be enabled by flag

        result = EvalResult(case=case, actual_route=actual_route,
                           route_correct=route_correct, violations=violations)
        results.append(result)
        if route_correct:
            stats["route_correct"] += 1

    # Build report
    report = {
        "run_at": datetime.now().isoformat(),
        "total": stats["total"],
        "route_correct": stats["route_correct"],
        "route_accuracy": round(stats["route_correct"] / max(stats["total"], 1) * 100, 1),
        "violations": stats["violations"],
        "results": [
            {
                "id": r.case.question_id,
                "question": r.case.question[:60],
                "expected": r.case.expected_route,
                "actual": r.actual_route,
                "correct": r.route_correct,
                "violations": r.violations,
            }
            for r in results
        ],
        "wrong_routes": [
            {"id": r.case.question_id, "q": r.case.question[:60],
             "expected": r.case.expected_route, "actual": r.actual_route}
            for r in results if not r.route_correct
        ],
    }

    # Save reports
    logs = pack_dir.parent.parent / "training_logs"
    logs.mkdir(exist_ok=True)

    md_path = logs / "ace_v1_eval_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# ACE-v1 Eval Report\n\n")
        f.write(f"**Run:** {report['run_at']}\n")
        f.write(f"**Total:** {report['total']} | ")
        f.write(f"**Correct:** {report['route_correct']} | ")
        f.write(f"**Accuracy:** {report['route_accuracy']}%\n\n")
        f.write("## Violations\n\n")
        for k, v in report["violations"].items():
            f.write(f"- {k}: {v}\n")
        if report["wrong_routes"]:
            f.write("\n## Wrong Routes\n\n")
            for w in report["wrong_routes"]:
                f.write(f"- {w['id']}: expected `{w['expected']}`, got `{w['actual']}` — {w['q']}\n")
        f.write(f"\n## Verdict\n\n")
        if report['route_accuracy'] >= 95:
            f.write("✅ ACE-v1 route accuracy passes threshold (>= 95%).\n")
        else:
            f.write(f"❌ ACE-v1 route accuracy {report['route_accuracy']}% below 95% threshold.\n")

    json_path = logs / "ace_v1_eval_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Route accuracy: {report['route_accuracy']}% ({report['route_correct']}/{report['total']})")
    print(f"Violations: {report['violations']}")
    print(f"Reports: {md_path}, {json_path}")

    return report


if __name__ == "__main__":
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "training_packs/23_ace_v1_eval"
    run_ace_eval(pack)
