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


# ─── Compatibility: old heuristic_judge signature ────

def heuristic_judge(question_text: str, expected: str, answer: str,
                    expected_sources=None, guard_triggered=False,
                    metadata=None):
    """Compatibility wrapper for eval runner's old call signature."""
    from src.eval_runner.models import EvalQuestion, EvalAnswer
    q = EvalQuestion(
        question_id="auto", question=question_text,
        expected_answer=expected,
        expected_sources=expected_sources or [],
    )
    a = EvalAnswer(
        question_id="auto", answer=answer,
        guard_triggered=guard_triggered,
        metadata=metadata or {},
    )
    return judge_v3(q, a)


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


# ═══════════════════════════════════════════════════════
# Judge v4 — Negation-Aware Detection
# ═══════════════════════════════════════════════════════

NEGATION_ZH = [
    "不支持", "没有", "未实现", "尚未实现", "当前没有",
    "当前不支持", "不能使用", "不是当前功能", "不是 v0.1",
    "还没有加入", "只是未来计划", "不是默认",
    "不能作为", "不能当", "不存在", "没有实现",
    "资料中未提及已经实现", "不能确认已经实现",
    "不是", "不推荐", "不可以", "不能说",
]
NEGATION_EN = [
    "not supported", "not implemented", "not available",
    "does not include", "cannot use", "is not a current",
    "not part of v0.1", "future plan only",
    "not currently implemented", "no evidence that",
    "does not support", "not a default",
]

AFFIRMATION_ZH = [
    "已支持", "已经支持", "可以使用", "已实现", "已经实现",
    "内置", "默认", "会自动", "是默认", "可作为",
    "已加入", "当前已", "现在已", "已经可用",
    "当前支持", "现在支持", "支持了", "会做", "已可用",
]
AFFIRMATION_EN = [
    "already supports", "is implemented", "can use",
    "built in", "default", "automatically crawls",
    "is available", "now supports", "currently supports",
]

RISK_TERMS = [
    "Web UI", "FastAPI", "PDF", "DOCX", "Internet Query",
    "web search", "web ingest", "embedding", "vector DB",
    "crawler", "daemon", "tray", "LoRA", "fine-tuning",
    "model unload", "cli webui", "cli pdf ingest",
    "cli daemon start", "cli crawler", "32B",
    "wrong_answer", "source archive",
    "联网", "爬网页", "自动抓取",
]


def detect_negated_risk_claim(answer: str) -> dict:
    """Detect whether risk terms appear in negated context."""
    a_lower = answer.lower()

    risk_found = []
    for term in RISK_TERMS:
        if term.lower() in a_lower:
            risk_found.append(term)

    if not risk_found:
        return {
            "risk_keyword_detected": False,
            "risk_terms": [],
            "negation_detected": False,
            "negated_terms": [],
            "negation_scope_valid": False,
            "affirmation_override_detected": False,
        }

    # Check for affirmations (overclaim)
    affirmed = False
    for aff in AFFIRMATION_ZH + AFFIRMATION_EN:
        if aff in a_lower:
            affirmed = True
            break

    # Check for negations within a window of each risk term
    negated_terms = []
    for term in risk_found:
        idx = a_lower.find(term.lower())
        if idx < 0:
            continue
        # Check 30 chars before and after for negation
        start = max(0, idx - 30)
        end = min(len(a_lower), idx + len(term) + 30)
        context = a_lower[start:end]
        for neg in NEGATION_ZH + NEGATION_EN:
            if neg in context:
                negated_terms.append(term)
                break

    return {
        "risk_keyword_detected": True,
        "risk_terms": risk_found,
        "negation_detected": len(negated_terms) > 0,
        "negated_terms": negated_terms,
        "negation_scope_valid": len(negated_terms) == len(risk_found),
        "affirmation_override_detected": affirmed and len(negated_terms) < len(risk_found),
    }


def judge_v4(question, answer) -> "EvalJudgement":
    """Heuristic judge v4: negation-aware + cautious uncertainty + overclaim detection."""
    from src.eval_runner.models import EvalJudgement

    a = answer.answer.lower()
    expected = question.expected_answer.lower()

    judgement = EvalJudgement()
    neg_result = detect_negated_risk_claim(answer.answer)

    metadata = {
        "judge_version": "heuristic_v4",
        "risk_keyword_detected": neg_result["risk_keyword_detected"],
        "risk_terms": neg_result["risk_terms"],
        "negation_detected": neg_result["negation_detected"],
        "negated_terms": neg_result["negated_terms"],
        "negation_scope_valid": neg_result["negation_scope_valid"],
        "affirmation_override_detected": neg_result["affirmation_override_detected"],
        "cautious_uncertainty_detected": False,
        "overclaim_detected": False,
    }

    # ─── Affirmation override: risk term + affirmation but no negation → wrong ───
    if neg_result["affirmation_override_detected"]:
        judgement.correctness = "wrong"
        judgement.notes = f"Affirmed overclaim: {neg_result['risk_terms']}"
        judgement.failure_type = "capability_overclaim"
        metadata["overclaim_detected"] = True
        judgement.metadata = metadata
        return judgement

    # ─── Negated risk: all risk terms are in negated context → correct_candidate ───
    if neg_result["negation_scope_valid"] and neg_result["negated_terms"]:
        judgement.correctness = "correct_candidate"
        judgement.notes = f"Correct negation: {neg_result['negated_terms']}"
        judgement.metadata = metadata
        return judgement

    # ─── Partial negation: some terms negated but not all → partial ───
    if neg_result["negation_detected"] and not neg_result["negation_scope_valid"]:
        # Some risk terms are negated, others are not
        judgement.correctness = "partial_candidate"
        judgement.notes = f"Partial negation: {neg_result['negated_terms']} negated, {set(neg_result['risk_terms'])-set(neg_result['negated_terms'])} unchecked"
        judgement.metadata = metadata
        return judgement

    # ─── Fallback to judge_v3 for remaining cases ───
    # But first: check if any v3 regex match is actually negated
    j3 = judge_v3(question, answer)
    if j3.correctness == "wrong" and j3.metadata and j3.metadata.get("overclaim_detected"):
        # Check if the overclaim was actually a negated statement
        if neg_result["negation_scope_valid"] and neg_result["negated_terms"]:
            # The v3 regex caught a risk term but it's in a negated context
            judgement.correctness = "correct_candidate"
            judgement.notes = f"v3 overclaim override: negation detected for {neg_result['negated_terms']}"
            metadata["overclaim_detected"] = False
            metadata["negation_detected"] = True
            metadata["negated_terms"] = neg_result["negated_terms"]
            judgement.metadata = metadata
            return judgement
    return j3


# ─── Compatibility wrapper for eval runner ────────────

def heuristic_judge_v4(question_text: str, expected: str, answer: str,
                        expected_sources=None, guard_triggered=False,
                        metadata=None):
    """Compatibility wrapper for eval runner — uses judge_v4."""
    from src.eval_runner.models import EvalQuestion, EvalAnswer
    q = EvalQuestion(
        question_id="auto", question=question_text,
        expected_answer=expected,
        expected_sources=expected_sources or [],
    )
    a = EvalAnswer(
        question_id="auto", answer=answer,
        guard_triggered=guard_triggered,
        metadata=metadata or {},
    )
    return judge_v4(q, a)
