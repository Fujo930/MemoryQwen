# 14B as Deep Brain

date: 2026-06-28

## Test Results

14B (qwen2.5:14b Q4_K_M) was tested as a deep mode option on RTX 4080 Laptop.

### Performance
- VRAM: 9.4 GB / 12 GB (76%)
- Speed: 3.7-4.7s steady state (comparable to 7B's 3.6s)
- First load: ~11s

### Consistency
- Internet Query capability: 9/9 (100%) vs 7B's 8/9 (89%)
- Answers are more precise and consistent in wording
- Correctly distinguishes v0.1.5 from v0.1

### Verdict
14B is viable as optional deep mode. It should NOT replace 7B as default — speed is comparable but VRAM doubles. Users with <12GB VRAM cannot run both models simultaneously.

## Recommended Usage

| Scenario | Model |
|----------|:-----:|
| Casual chat | 7B |
| Project questions | 7B |
| Web queries | 7B |
| Capability conflicts | 14B (--deep) |
| Version-aware answers | 14B (--deep) |
| Audit/verification | 14B (--deep) |
| Complex planning | 14B (--deep) |

## Future: TDR-v1

Token-Difficulty Routing should auto-escalate capability-conflict questions to 14B without requiring the user to know about --deep. This requires a Difficulty Estimator that can detect:
- Source conflict signals
- Version-specific questions
- Capability boundary questions
