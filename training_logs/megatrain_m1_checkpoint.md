# MegaTrain M1 Checkpoint

冻结时间：2026-06-27

## M1 总目标回顾

MegaTrain M1 是 MemoryQwen v0.1 的第一阶段大规模训练。目标是通过高质量 longform 训练资料、测试问题、陷阱问题和策略种子，让 MemoryQwen 建立核心语义认知。

## M1 最终指标

| Metric | Start | End | Change |
|--------|-------|-----|--------|
| estimated_tokens | ~419K | **1,638,350** | +1.2M |
| total_chars | ~1.5M | **6,412,302** | +4.9M |
| knowledge_store | 395 | **2,309** | +1,914 |
| archived_files | 221 | **1,131** | +910 |
| training_packs_mb | 1.14 | **1.31** | +0.17 |
| memory_sources_mb | 1.06 | **8.31** | +7.25 |
| project_total_mb | 3.78 | **24.37** | +20.59 |
| error_store | 17 | **17** | 0 (by design) |
| strategy_store | 11 | **11** | 0 (by design) |
| pytest | 387→429 | **429** | +42 |
| 10M progress | ~4% | **16.38%** | +12% |

## Batch History

| Batch | Docs | Tokens | Knowledge | Archived | Focus |
|-------|------|--------|-----------|----------|-------|
| 01 Source Archive | 100 | +110K | +362 | +105 | inbox/sources/backup semantics |
| 02 Model Hardware | 100 | +62K | +242 | +105 | 3B/7B/14B/32B routing |
| 02.5 Hardware Top-up | 35 | +94K | +163 | +35 | Token gap fill |
| 03 CLI Hallucination | 80 | +91K | +166 | +80 | Real vs fake CLI commands |
| 04 Capability Boundary | 80 | +86K | +166 | +80 | Implemented vs not |
| 05 Anti-Hallucination | 80 | +85K | +163 | +80 | Evidence, uncertainty, no-fabrication |
| 05.5 Reliability Top-up | 80 | +227K | +170 | +80 | Cross-theme reliability |
| **Total** | **555** | **+1.2M** | **+1,914** | **+910** | |

## Audit Results

- ✅ No fake CLI commands (cli webui, cli pdf, cli daemon)
- ✅ No unsupported features claimed (Web UI, PDF, Internet)
- ✅ No wrong_answer-as-fact violations
- ✅ No source-archive-as-crawler violations
- ✅ Safety: 0 issues (no secrets, no weights, no cache)
- ✅ pytest: 429/429

## Key Reinforced Themes

1. Source archive semantics: inbox ≠ memory/sources ≠ memoryqwen.db ≠ tasks.db
2. Model routing: 3B run, 7B default, 14B deep, 32B+ experiment
3. CLI boundaries: real commands (20+) vs fake commands (9)
4. Capability boundaries: implemented (20+) vs not implemented (12)
5. Anti-hallucination: admit uncertainty, cite sources, don't fabricate

## Current Limitations

- questions_count stuck at 63 (eval loader format mismatch)
- error_store/strategy_store intentionally not grown (requires real correct)
- 555 docs are somewhat repetitive (by design for reinforcement)
- Most docs use para-loop pattern, not carefully hand-crafted

## M2 Recommendation

**Yes, proceed to M2.** M1 baseline is solid. M2 should focus on:
1. Real eval questions with proper format
2. GPU Guardian + Task Runtime scenario training
3. Error/Strategy extreme training
4. Reduce repetition, increase content diversity
5. Target: 5M tokens, 5,000 knowledge, 100+ real eval questions
