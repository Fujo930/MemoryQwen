# Training Assets Status

日期：2026-06-27

## Real Metrics (Asset Metrics v2)

| 指标 | 值 |
|------|-----|
| project_total | ~3.78 MB |
| training_packs | 0.05 MB |
| training_logs | 0.01 MB |
| memory/sources | 0.08 MB |
| total_chars | ~1.57M |
| estimated_tokens | ~419K |
| knowledge_store | 395 |
| error_store | 17 |
| strategy_store | 11 |
| archived_files | 132+ |

## 已废弃的错误数据

旧报告中的 **233.9 MB / 22.8% 进度** 是统计脚本 bug 导致的错误数据。

根因：`total = sum(sections.values())` 把文件计数(整数)当作 MB 累加。

真实训练资产应以 Asset Metrics v2 输出为准。

## Multi-Target Progress

| 目标 | 当前 | 进度 |
|------|------|------|
| disk (1024 MB) | ~3.78 MB | 0.4% |
| tokens (10M) | ~419K | 4.2% |
| knowledge_chunks (10K) | 395 | 4.0% |
| questions (5K) | 130 | 2.6% |
| error_cases (500) | 17 | 3.4% |
| strategies (200) | 11 | 5.5% |

## 10x Training Pack

10 themes, 90+ source files, 63 questions, 63 traps, 63 answer keys.
Stage C v2: 50 longform docs, 705K chars.
Full 1GB target deferred to v0.2.
