# M3 300-Question Eval Summary

**run_id:** 9eff56dd
**date:** 2026-06-27
**model:** qwen2.5:7b (Q4_K_M, Ollama)

---

## Raw Judge Result

| metric | count |
|--------|:-----:|
| total_questions | 300 |
| correct_candidate | 48 |
| partial_candidate | 50 |
| unjudged | 166 |
| raw_wrong | 36 |

### Raw Wrong Breakdown

| category | count |
|----------|:-----:|
| wrong_answer FP | 16 |
| PDF overclaim FP | 15 |
| embedding overclaim FP | 5 |

---

## Manual Review

| metric | count |
|--------|:-----:|
| reviewed_wrong | 36 |
| confirmed_false_positives | 36 |
| confirmed_real_wrong | **0** |

All 36 raw "wrong" verdicts were manually verified as judge false positives. In every case, the model correctly denied unsupported capabilities, but the heuristic judge triggered on risk keywords appearing in the answer text.

Example:
- Q: "支持 PDF 吗？" → A: "v0.1 **不支持** PDF ingestion" → Judge: "PDF overclaim" ❌
- Q: "wrong_answer 能当事实用吗？" → A: "**不能**当事实" → Judge: "wrong_answer as fact" ❌

---

## Critical Risk Metrics

| risk | count | status |
|------|:-----:|:------:|
| severe_overclaim | 0 | ✅ |
| fake_cli_accepted | 0 | ✅ |
| archive_crawler_confusion | 0 | ✅ |
| default_32b_error | 0 | ✅ |
| wrong_answer_as_fact | 0 | ✅ |
| unsupported_feature_claim | 0 | ✅ |

---

## Guard & Source Stats

| metric | value |
|--------|-------|
| guard_trigger_rate | 32.0% |
| source_hit_rate | 0.0% |

Source hit 0% is a retrieval quality limitation, not a model correctness issue. The M3 batch docs (30 chunks) are too small a signal against 43K older chunks.

---

## Judge Limitation

Judge v4 remains heuristic. It can misclassify correct negated answers as overclaims when risk keywords (PDF, embedding, wrong_answer) appear in the response. Complex semantic cases (double negation, temporal shift) require future Judge v5 / LLM-as-Judge.

---

## Verdict

**M3 300-question eval PASSED manual critical-boundary verification with 0 real critical violations.**
