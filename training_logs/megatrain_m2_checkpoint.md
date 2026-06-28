# MegaTrain M2 Checkpoint

冻结时间：2026-06-27

## M2 Overview

M2 was the second phase of MegaTrain, targeting 5M tokens and 5K knowledge chunks.

## M2 Final Metrics

| Metric | M1 End | M2 End | Multiplier |
|--------|--------|--------|------------|
| estimated_tokens | 1.64M | **5.12M** | 3.1x |
| knowledge_store | 2,309 | **22,211** | 9.6x |
| archived_files | 1,131 | **4,000+** | 3.5x |
| total source docs | 555 | **4,200+** | 7.6x |
| pytest | 429 | **463** | +34 |
| 10M progress | 16.38% | **51.22%** | — |

## M2 Batches (12)

- 8 main batches (agent workflows, task/GPU, eval/judge, memory, model, assistant, strategy, integrated)
- 4 massive top-up batches (reliability expansion)
- Total: ~3,650 source docs generated

## v0.1.2 Smart Retrieval Gate

Integrated during M2. Casual chat now skips retrieval. High-risk questions still retrieve. 463/463 tests.

## Heuristic Judge v3

- Cautious uncertainty recognized as correct_candidate
- Known limitation: regex false positives in negated contexts (~5-9/200)
- 19 judge tests passing

## Issue #24: M2 200-Question Eval

- 200 questions across 9 topics
- 192 verified (excl. block headers)
- 0 real critical violations
- Fake CLI: 0, Archive=crawler: 0, 32B default: 0
- Judge v3 regex FPs documented as known limitation

## Recommendation

Proceed to M3 or v0.1.5 (Internet Query, Judge v4, targeted training).
