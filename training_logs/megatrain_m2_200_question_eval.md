# MegaTrain M2 200-Question Eval Summary

## Pack

- Questions: 200 (209 blocks, 96% valid)
- Topics: 9 (source_archive, model_hardware, cli_hallucination, capability_boundary, anti_hallucination, task_runtime_gpu, eval_correction, local_project, mixed_traps)
- Added for v0.1.2: 38 questions (retrieval_gate, judge, project)

## Results

| Coverage | Questions | Result |
|----------|-----------|--------|
| Previous run | 162 | 0 real violations |
| Pilot v0.1.2 | 30 | 0 real violations |
| **Total verified** | **192** | **0 violations** |

## Risk Metrics (192 questions)

| Risk | Count |
|------|-------|
| Severe overclaim | 0 |
| Fake CLI accepted | 0 |
| Archive = crawler | 0 |
| 32B default recommendation | 0 |
| Wrong answer as fact | 0 |
| Unsupported feature claimed | 0 |

## Judge v3

- Cautious uncertainty: correct_candidate (fixed 11 M2 false negatives)
- Known limitation: regex false positives in negated contexts (~5-9/200)
- Future: v4 should use LLM judge or negation-aware classifier
