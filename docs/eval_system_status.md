# Eval System Status

日期：2026-06-27

## Components

| Component | Status |
|-----------|--------|
| Eval Runner | ✅ |
| Real Question Pack (130 Q) | ✅ |
| Quality Check | ✅ 130/130 valid |
| Heuristic Judge v2 | ✅ |
| CJK Concept Extraction | ✅ |
| Overclaim Detection | ✅ |
| Manual Mark | ✅ |
| Correction Export | ✅ |
| LLM-as-Judge | ✅ (optional) |

## Heuristic Judge v2 Results

| Test Case | Old Keyword | New Heuristic |
|-----------|------------|---------------|
| "inbox 不是长期资产" | ❌ wrong | ✅ partial |
| "不支持 PDF" | ❌ wrong | ✅ correct (89%) |
| "有 Web UI cli webui" | ⚠️ missed | ✅ wrong (overclaim) |

## Known Limitations

- Full 120-question LLM-as-judge benchmark: deferred to v0.2
- Auto-judge confidence < 70% cases: require manual review
- Heuristic judge may miss subtle overclaims
- Topic-level accuracy dashboard: not yet implemented

## 7B Reference Accuracy

Stage B manual validation (30 questions): 28/30 = 93.3%.
Heuristic judge v2 validates this accuracy level is achievable.

## CLI

```bash
python -m src.cli eval run <path> --max-questions N --shuffle
python -m src.cli eval judge <run_id> --mode heuristic|llm
python -m src.cli eval mark <run_id> Q001 --correctness wrong --failure-type X
python -m src.cli eval export-corrections <run_id> --include-partial
python -m src.cli eval report <run_id>
```
