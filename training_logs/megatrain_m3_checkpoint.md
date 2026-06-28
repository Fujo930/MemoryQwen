# MegaTrain M3 Checkpoint

**Issue #27-28: M3 MegaTrain 5.12M → 10M+**

date: 2026-06-27
status: **COMPLETE**

---

## Summary

M3 expanded MemoryQwen beyond 10M estimated training tokens and 43K knowledge chunks. The 312-question eval pack was created and a 300-question full eval was executed. After manual review, 0 real critical violations were found. All 36 raw "wrong" verdicts were confirmed as judge v4 false positives.

---

## Assets

| metric | M2 baseline | M3 actual |
|--------|:-----------:|:---------:|
| estimated_tokens | 5.12M | **11,274,562** |
| knowledge_store chunks | 22,211 | **43,645** |
| archived source docs | 4,200+ | **28,339** |
| training_packs | 18 | **19** |
| M3 batch source docs | 0 | **8** |
| M3 eval pack questions | 0 | **312** |

---

## Eval

| run | questions | raw wrong | real violations |
|-----|:---------:|:---------:|:---------------:|
| pilot 50 | 50 | 8 | 0 |
| 150 | 150 | 17 | 0 |
| full 300 | 300 | 36 | 0 |

- M3 eval pack: 312 questions total (300 executed)
- Raw heuristic wrong: 36
- Manual verified false positives: 36
- Real critical violations: 0

### False Positive Breakdown

| category | count | root cause |
|----------|:-----:|------------|
| wrong_answer FP | 16 | model says "wrong_answer cannot be used as fact" → judge flags keyword |
| PDF overclaim FP | 15 | model says "v0.1 does not support PDF" → judge flags keyword |
| embedding overclaim FP | 5 | model says "v0.1 does not support embedding" → judge flags keyword |

These are NOT model errors. They are Judge v4 heuristic false positives triggered by risk keywords appearing in correct negated answers.

---

## Risk Metrics

| risk | count |
|------|:-----:|
| severe overclaim | 0 |
| fake CLI accepted | 0 |
| source archive = crawler | 0 |
| 32B/70B default recommendation | 0 |
| wrong_answer treated as fact | 0 |
| unsupported PDF/embedding claims | 0 |

---

## Performance

30-question latency + accuracy smoke (qwen2.5:7b, RTX 4080 Laptop):

| category | questions | avg | fastest | slowest |
|----------|:---------:|:---:|:-------:|:-------:|
| casual | 5 | 1.9s | 1.2s | 4.0s |
| error | 5 | 3.1s | 1.8s | 4.8s |
| boundary | 5 | 3.5s | 3.4s | 3.6s |
| task | 5 | 4.3s | 3.8s | 5.0s |
| project | 5 | 4.4s | 3.6s | 5.2s |
| hardware | 5 | 4.5s | 4.0s | 5.6s |
| **overall** | **30** | **3.6s** | 1.2s | 5.6s |

Accuracy spot check: 5/5 critical boundary questions answered correctly. Smart Retrieval Gate remains effective.

---

## Known Limitations

- **Source hit 0%** on M3 eval runs: 30 new M3 batch chunks drowned by 43K older chunks. Retrieval Quality v2 needed before M4.
- **Judge v4 false positives**: Heuristic judge over-triggers on risk keywords in correct negated answers. Needs Judge v5 (LLM-as-Judge) for complex semantic cases.
- **Retrieval quality**: BM25 cannot prioritize authoritative M3 docs over generic training content.
- **Internet Query**: not implemented (v0.1.5 planned).
- **Web UI**: not implemented (v0.2 planned).

---

## Checks

| check | status |
|-------|:------:|
| pytest | 496/496 |
| safety | 0 blocked patterns |
| release safety | PASS (1 known: M2 devpack zip) |
| eval quality | 312/321 with question field |

---

## Verdict

**M3 COMPLETE.** All numeric targets exceeded. 0 real critical violations after manual review. Judge v4 limitations documented. Runtime performance remains usable at 10M+ token scale.

---

## Next Recommendation

**v0.1.5 Internet Query.** M3 training assets provide sufficient knowledge base coverage for safe web-augmented retrieval.

---

## Changelog

- 2026-06-27 21:54: M3 300-full-eval completed (run 9eff56dd)
- 2026-06-27 21:43: M3 150-eval completed (run a0a1c9a7)
- 2026-06-27 21:16: M3 pilot-50 completed (run cb52e8bc)
- 2026-06-27: M3 batch source docs (8 files) created and ingested
- 2026-06-27: M3 eval pack guard_expected + expected_sources fields added
