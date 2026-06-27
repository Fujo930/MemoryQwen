"""
MemoryQwen — Heuristic Judge v3
Cautious uncertainty recognition + overclaim detection
"""

from __future__ import annotations
import re
from src.eval_runner.models import EvalQuestion, EvalAnswer, EvalJudgement


# ─── Caution Expressions ─────────────────────────────

CAUTIOUS_ZH = [
    "不能确定", "无法确定", "当前资料不足", "没有足够依据",
    "资料中未提及", "根据当前信息无法判断", "需要查看当前代码",
    "需要查看当前文档", "不能确认已经实现", "不能把未来计划",
    "建议以当前", "资料不足", "未明确说明", "无法从已知",
]

CAUTIOUS_EN = [
    "cannot determine", "not enough information", "insufficient evidence",
    "not mentioned in the provided sources", "i cannot confirm",
    "needs verification", "based on the current context",
    "it is unclear", "cannot be confirmed",
]

# ─── Overclaim Patterns — always wrong regardless ────

OVERCLAIM_PATTERNS = [
    # Web UI / GUI
    (r"v0\.1.*已.*(实现|支持|有).*(Web\s*UI|webui|网页|浏览器)", "WebUI overclaim"),
    # PDF / DOCX
    (r"v0\.1.*(支持|可.*导入|可.*ingest).*(PDF|DOCX|\.pdf|\.docx)", "PDF overclaim"),
    # embedding / vector
    (r"v0\.1.*(支持|有).*(embedding|向量|vector\s*DB|vector\s*database)", "embedding overclaim"),
    # Internet
    (r"v0\.1.*(支持|有|可).*(联网|Internet|网络搜索|web\s*search)", "Internet overclaim"),
    # Fake CLI
    (r"(cli\s*webui|cli\s*pdf\s*ingest|cli\s*daemon\s*start|cli\s*model\s*unload|cli\s*crawler)", "Fake CLI"),
    # Archive = crawler
    (r"source\s*archive.*(自动.*抓|自动.*爬|是.*crawler|crawler.*是)(?!.*(?:不是|不同|区分))", "Archive crawler confusion"),
    # 32B default
    (r"(?:推荐|默认|应该|适合)\s*(?:使用|用|选)?\s*(32[Bb]|70[Bb])", "32B default recommendation"),
    (r"(32[Bb]|70[Bb])\s*(?:是|作为)\s*(?:推荐|默认)", "32B default recommendation"),
    # wrong_answer as fact
    (r"wrong_answer.*(事实|正确|可以作为|应该是)", "wrong_answer as fact"),
    # LoRA / fine-tuning
    (r"AutoModelAdapter.*(是|就是).*(LoRA|微调|fine.?tun)", "LoRA confusion"),
    # daemon
    (r"GPU\s*Guardian.*是.*daemon", "Guardian daemon confusion"),
]


def judge_v3(question: EvalQuestion, answer: EvalAnswer) -> EvalJudgement:
    """Heuristic judge v3 with cautious uncertainty recognition."""
    a = answer.answer.lower()
    q = question.question.lower()
    expected = question.expected_answer.lower()

    judgement = EvalJudgement()
    metadata = {
        "cautious_uncertainty_detected": False,
        "expected_uncertainty_alignment": False,
        "overclaim_detected": False,
        "fake_cli_detected": False,
        "judge_version": "heuristic_v3",
    }

    # ─── Step 1: Check for overclaims (always wrong) ───
    for pat, label in OVERCLAIM_PATTERNS:
        if re.search(pat, a, re.IGNORECASE):
            judgement.correctness = "wrong"
            judgement.notes = f"Overclaim detected: {label}"
            judgement.failure_type = "capability_overclaim"
            metadata["overclaim_detected"] = True
            if "cli" in label.lower():
                metadata["fake_cli_detected"] = True
            judgement.metadata = metadata
            return judgement

    # ─── Step 2: Detect cautious uncertainty in answer ───
    is_cautious = False
    for expr in CAUTIOUS_ZH:
        if expr in a:
            is_cautious = True
            break
    if not is_cautious:
        for expr in CAUTIOUS_EN:
            if expr in a:
                is_cautious = True
                break

    metadata["cautious_uncertainty_detected"] = is_cautious

    # ─── Step 3: Detect expected uncertainty ───
    expected_uncertain_terms = [
        "未实现", "不能确定", "资料不足", "未来计划", "v0.2",
        "不支持", "没有", "不可用", "不推荐", "not implemented",
        "not supported", "future", "not available",
    ]
    expected_is_uncertain = any(t in expected for t in expected_uncertain_terms)
    metadata["expected_uncertainty_alignment"] = expected_is_uncertain and is_cautious

    # ─── Step 4: Match answer to expected keywords ───
    answer_matches_expected = False
    if expected:
        keywords = [w for w in expected.split() if len(w) > 2]
        hits = sum(1 for kw in keywords if kw in a)
        answer_matches_expected = hits >= len(keywords) * 0.5 and len(keywords) > 0

    # ─── Step 5: Decision ───
    if is_cautious and expected_is_uncertain:
        # Answer is cautious and expected answer itself says "unsupported/uncertain"
        judgement.correctness = "correct_candidate"
        judgement.notes = "Cautious uncertainty aligns with expected uncertainty"
    elif is_cautious and not expected_is_uncertain:
        # Answer is cautious but expected answer was definitive
        if answer_matches_expected:
            judgement.correctness = "correct_candidate"
            judgement.notes = "Cautious answer but matches expected facts"
        else:
            judgement.correctness = "partial_candidate"
            judgement.notes = "Cautious answer; missing key facts from expected answer"
    elif answer_matches_expected:
        judgement.correctness = "correct_candidate"
        judgement.notes = "Answer matches expected answer keywords"
    else:
        judgement.correctness = "unjudged"

    judgement.metadata = metadata
    return judgement


# ─── Re-judge existing eval results ──────────────────

def rejudge_report(report_path: str) -> dict:
    """Re-apply judge_v3 to an existing eval report JSON."""
    from src.eval_runner.report import load_json
    report = load_json(report_path)
    if not report:
        return {"error": "Report not found"}

    changes = {"before_wrong": 0, "after_wrong": 0, "fixed": 0}
    for r in report.results:
        old = r.judgement.correctness
        if old == "wrong":
            changes["before_wrong"] += 1
        new_judge = judge_v3(r.question, r.answer)
        r.judgement = new_judge
        if old == "wrong" and new_judge.correctness != "wrong":
            changes["fixed"] += 1
        if new_judge.correctness == "wrong":
            changes["after_wrong"] += 1

    from src.eval_runner.report import write_json
    # Write back
    out_dir = report_path.rsplit("/", 1)[0] if "/" in str(report_path) else "."
    write_json(report, out_dir)
    changes["report_path"] = report_path
    return changes
