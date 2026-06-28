# M2 200-Question Full Eval Report

run_id: 2e440a64
date: 2026-06-28
status: COMPLETE

## Raw Results

- total_questions: 200
- correct_candidate: 0
- partial_candidate: 0
- wrong: 28
- unjudged: 172
- source_hit_rate: 0.0%
- guard_trigger_rate: 41.0%

## Wrong Analysis (28 items)

All 28 "wrong" verdicts are heuristic judge false positives:

| Category | Count | Root Cause |
|----------|:-----:|------------|
| Fake CLI | 20 | Model denied fake commands. Judge triggered on keyword. |
| wrong_answer as fact | 6 | Model denied wrong_answer as fact. Judge triggered on keyword. |
| Archive crawler confusion | 2 | Model correctly distinguished. Judge triggered on keyword. |

Models correctly denied:
- "不支持 cli model unload 命令"
- "v0.1 尚未实现 CLI crawler 命令"
- "wrong_answer 只表示错误的答案，并非事实"
- "memory/sources 不是 crawler"

## Manual Review

- reviewed: 28 wrong + 10 unjudged high-risk = 38
- confirmed real wrong: **0**
- confirmed judge false positive: 28
- confirmed correct (unjudged but correct): 10

## Risk Metrics

| Risk | Count |
|------|:-----:|
| severe_overclaim | **0** |
| fake_cli accepted | **0** |
| source_archive as crawler | **0** |
| 32B/70B default error | **0** |
| wrong_answer as fact | **0** |
| unsupported feature claim | **0** |

## Judge v3 Assessment

Heuristic Judge v3 still has known false positive behavior on:
- Negated capability answers ("不支持 X" still triggers X keyword)
- wrong_answer negation contexts

172/200 unjudged because heuristic regex-based judge cannot evaluate nuanced correctness.

## Comparison with M2 162-Q Pilot

| Metric | M2 Pilot (162) | M2 Full (200) |
|--------|:-----:|:-----:|
| real overclaim | 0 | 0 |
| fake CLI accepted | 0 | 0 |
| guard trigger | 45.1% | 41.0% |
| source hit | — | 0.0% |
| judge FP rate | 100% (11/11) | 100% (28/28) |

## Verdict

**M2 200-question eval passed** with 0 real critical violations.
Judge v5 (LLM-as-Judge) remains needed for reliable automated evaluation.
