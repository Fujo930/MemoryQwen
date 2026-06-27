"""
MemoryQwen — Eval Judge
Supports manual / heuristic / llm judging modes.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import json, logging

logger = logging.getLogger(__name__)

JudgeMode = "manual"  # acceptable values: manual, heuristic, llm


@dataclass
class JudgeResult:
    correctness: str = "unjudged"  # correct / partial / wrong / unjudged
    confidence: float = 0.0
    failure_type: str = ""
    notes: str = ""
    judge_mode: str = "heuristic"
    evidence: dict = field(default_factory=dict)
    manual_override: bool = False


# ─── Rubric ──────────────────────────────────────────

CORRECT_RULES = [
    "事实正确，无严重遗漏",
    "没有把未实现/未来计划说成已实现",
    "没有编造 CLI/tool/功能",
    "对 yes/no 边界题给出明确判断",
    "没有 overclaim",
]
PARTIAL_RULES = [
    "大方向正确但遗漏关键限定",
    "引用不足或表达模糊",
    "没有完整覆盖 expected_answer",
]
WRONG_RULES = [
    "把未实现/未来计划说成已实现",
    "编造 CLI/tool/功能",
    "把 wrong_answer 当事实",
    "答非所问",
    "与 expected_answer 核心结论相反",
    "严重 source_misread",
]

NEGATION_SIGNALS = [
    "不是", "没有", "不支持", "未实现", "不包含", "无法",
    "不能", "不可", "不会", "不做",
]


def heuristic_judge(question_text: str, expected_answer: str,
                    actual_answer: str, expected_sources: list[str],
                    guard_triggered: bool) -> JudgeResult:
    """Heuristic v2 judge — multi-dimensional, not just keyword match."""
    if not expected_answer or len(expected_answer) < 10:
        return JudgeResult(correctness="unjudged", confidence=0.0,
                           notes="expected_answer too short for heuristic judge")

    ans = actual_answer.lower()
    exp = expected_answer.lower()

    # 1. Extract key concepts from expected answer (verbs + nouns)
    concept_hits = 0
    concept_total = 0
    concepts = _extract_concepts(exp)
    for c in concepts:
        concept_total += 1
        if c in ans:
            concept_hits += 1

    # 2. Negation check: if expected says "没有/不支持" and answer also says "没有/不支持"
    exp_negative = any(w in exp for w in NEGATION_SIGNALS)
    ans_negative = any(w in ans for w in NEGATION_SIGNALS)
    negation_match = exp_negative == ans_negative if exp_negative else True

    # 3. Overclaim check
    overclaim = False
    overclaim_patterns = [
        ("web ui", "不支持"),
        ("pdf", "不支持"),
        ("daemon", "不是"),
        ("cli webui", "没有"),
        ("crawler", "不支持"),
        ("embedding", "不支持"),
        ("lora", "不支持"),
    ]
    for feat, should_say in overclaim_patterns:
        if feat in ans and should_say not in ans and "不支持" not in ans and "没有" not in ans and "未实现" not in ans:
            # only flag if feature appears positively
            positive = True
            for neg in NEGATION_SIGNALS:
                if neg in ans[ans.find(feat)-20:ans.find(feat)+len(feat)+20]:
                    positive = False
                    break
            if positive:
                overclaim = True

    # 4. "不能确定/资料不足" as valid answer
    uncertainty_signals = ["不能确定", "无法确定", "资料不足", "资料中没有", "未提及", "不确定"]
    ans_uncertain = any(s in ans for s in uncertainty_signals)

    # Decision
    concept_ratio = concept_hits / concept_total if concept_total else 0

    if overclaim:
        return JudgeResult(correctness="wrong", confidence=0.9,
                           failure_type="capability_overclaim",
                           notes="Overclaim detected: positive statement about unsupported feature",
                           evidence={"concept_ratio": concept_ratio, "overclaim": True})

    if concept_ratio >= 0.6 and negation_match and not overclaim:
        return JudgeResult(correctness="correct_candidate", confidence=concept_ratio,
                           notes=f"Heuristic: {concept_hits}/{concept_total} concepts matched",
                           evidence={"concept_ratio": concept_ratio, "negation_match": negation_match})

    if concept_ratio >= 0.3:
        return JudgeResult(correctness="partial_candidate", confidence=concept_ratio,
                           notes=f"Heuristic: {concept_hits}/{concept_total} concepts — partial",
                           evidence={"concept_ratio": concept_ratio})

    if ans_uncertain:
        return JudgeResult(correctness="partial_candidate", confidence=0.5,
                           notes="Model expressed uncertainty — may be valid anti-hallucination",
                           evidence={"uncertain": True})

    return JudgeResult(correctness="unjudged", confidence=0.0,
                       notes="Insufficient confidence for auto-judge",
                       evidence={"concept_ratio": concept_ratio})


def _extract_concepts(text: str) -> list[str]:
    """Extract meaningful concept tokens from mixed EN+ZH text."""
    import re
    concepts = []
    # Extract CJK sequences as separate tokens
    cjk_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
    for match in cjk_pattern.finditer(text):
        w = match.group()
        if len(w) > 1:
            # Split long CJK sequences into bigrams
            for i in range(len(w)-1):
                concepts.append(w[i:i+2])
            if len(w) <= 4:
                concepts.append(w)
    # Extract space-separated English/ASCII words
    stop = {"the","a","an","is","are","was","were","be","been","being","have","has","had",
            "do","does","did","will","would","shall","should","may","might","must","can","could",
            "and","or","but","if","then","else","when","where","how","what","which","who",
            "to","of","in","for","on","with","at","by","from","as","into","through","about",
            "this","that","these","those","it","its","they","them","their","we","our","you","your",
            "not","no","none","nor","only","just","also","very","too","so","than","more","most",
            "v0","v0.1","v0.2","是","的","了","在","有","和","就","不","人","都","去","也",
            "很","到","说","要","吗","吧","呢","啊","哦","嗯","啦","呀"}
    en_pattern = re.compile(r'[a-z0-9._-]+')
    for match in en_pattern.finditer(text.lower()):
        w = match.group()
        if len(w) > 2 and w not in stop:
            concepts.append(w)
    # Deduplicate preserving order, limit to 20
    seen = set()
    result = []
    for c in concepts:
        if c not in seen:
            seen.add(c)
            result.append(c)
            if len(result) >= 20:
                break
    return result


# ─── LLM-as-Judge ────────────────────────────────────

LLM_JUDGE_PROMPT = """You are an evaluation judge for MemoryQwen.

Review the following:

Question: {question}
Expected Answer: {expected}
Model Answer: {actual}

Rubric:
- correct: Factually correct, no overclaim, clearly states unsupported features as unsupported.
- partial: Generally correct but missing key details, vague, or incomplete.
- wrong: Claims unsupported features are supported, fabricates CLI/tools, uses wrong_answer as fact, or contradicts expected answer.

Return ONLY a JSON object:
{{"correctness": "correct|partial|wrong", "confidence": 0.0-1.0, "failure_type": "hallucination|source_misread|capability_overclaim|source_miss|...", "notes": "brief", "reason": "brief"}}"""


async def llm_judge(question_text: str, expected_answer: str,
                    actual_answer: str, model_client) -> JudgeResult:
    """Use an LLM to judge the answer."""
    prompt = LLM_JUDGE_PROMPT.format(
        question=question_text[:500],
        expected=expected_answer[:500],
        actual=actual_answer[:800],
    )
    try:
        resp = await model_client.chat(messages=[
            {"role": "user", "content": prompt}
        ])
        raw = resp.content.strip()
        # Extract JSON
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(raw[start:end])
        else:
            raise ValueError("No JSON found in response")
        return JudgeResult(
            correctness=data.get("correctness", "unjudged"),
            confidence=float(data.get("confidence", 0.0)),
            failure_type=data.get("failure_type", ""),
            notes=data.get("reason", data.get("notes", "")),
            judge_mode="llm",
            evidence={"raw": raw[:200]},
        )
    except Exception as e:
        logger.warning(f"LLM judge failed: {e}")
        return JudgeResult(correctness="unjudged", confidence=0.0,
                           notes=f"LLM judge error: {e}", judge_mode="llm")
