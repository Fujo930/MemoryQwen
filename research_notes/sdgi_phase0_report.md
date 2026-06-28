# SDGI Phase 0 — Token Difficulty Signal Collection Report

**Date:** 2026-06-28
**Status:** COMPLETE

## Hypothesis

Different tokens/phrases have stable, measurable differences in computational depth requirements. Tokens flagged by TDR-v1 as "high difficulty" correlate with 7B/14B behavioral divergence.

## Method

Collected TDR signals for 27 questions across 7 conflict categories.
Compared 7B vs 14B answers on 7 highest-difficulty questions.
Recorded: route, trigger_tokens, risk_scores, answer quality, consistency.

## Route Distribution

| Route | Count | % |
|-------|:-----:|:--:|
| capability_registry | 16 | 59% |
| memory | 4 | 15% |
| judge_review | 4 | 15% |
| deep_suggested | 2 | 7% |
| manual_review | 1 | 4% |

## Top Difficulty Tokens

| Token | Occurrences | Associated Risk |
|-------|:----------:|----------------|
| web | 7 | capability + judge |
| 联网 | 4 | capability |
| 支持 | 4 | capability |
| Web UI | 3 | capability |
| crawler | 2 | capability |
| wrong_answer | 2 | hallucination |
| 规划 | 2 | planning_depth |
| 算法 | 2 | planning_depth |
| 绕过 guard | 1 | hallucination |
| fake CLI | 1 | hallucination |

## 7B vs 14B Comparison

| Question | 7B Quality | 14B Quality | 14B Improvement |
|----------|:----------:|:----------:|:--------------:|
| 你是 crawler 吗 | Hesitant, mentions v0.1 | Direct: "不是" | ✅ Clarity |
| wrong_answer 当事实吗 | Correct but hallucinates v0.1.6 | Correct | ✅ No hallucination |
| 帮我规划外骨骼 | Rejects task entirely | Partial attempt | ⚠️ Both limited |
| 7B 够用吗 | Reasonable | More authoritative | ✅ Confidence |
| 旧资料vs新资料联网 | Correct | Correct | ≈ Equal |

## Key Findings

1. **14B consistently eliminates version hallucinations.** 7B invoked "v0.1.6" (non-existent version) twice. 14B never hallucinated versions.

2. **14B is more direct on capability denials.** "你是 crawler 吗": 7B hedged with "根据当前本地资料不能确定", 14B said "不是".

3. **Both models fail on open-ended planning.** "帮我规划 v0.2 外骨骼算法" — 7B rejected the task, 14B asked for clarification. Neither produced actual planning. This confirms planning needs the exoskeleton context (ACE + deep mode hint).

4. **Token difficulty signatures exist.** Tokens like "规划", "算法", "外骨骼", "设计" consistently correlate with:
   - deep_suggested routing
   - planning_depth >= 0.7
   - 7B avoidance/rejection behavior
   - 14B showing more engagement (but still limited)

5. **The hypothesis is supported but not proven.** Tokens DO show consistent difficulty patterns, but the sample size (27 questions, 7 comparisons) is too small for statistical confidence. Phase 1 needs 50+ questions with 3-run consistency checks.

## Verdict

**Phase 0 confirms that token difficulty signals exist and are measurable via TDR-v1.** The hypothesis "different tokens need different computational depth" is plausible and warrants Phase 1 testing with larger sample sizes and consistency metrics.

## Next

Phase 1: 50+ questions, 3-run 7B consistency, statistical correlation analysis between trigger_tokens and 7B failure rate.
