# 14B Deep Mode Benchmark — v0.1.5

date: 2026-06-28
status: COMPLETE

## Setup

- GPU: NVIDIA GeForce RTX 4080 Laptop (12 GB)
- Model: qwen2.5:14b (9.0 GB download, Q4_K_M)
- VRAM used: 9.4 GB / 12 GB (no OOM)
- Load success: ✅

## Internet Query Consistency (9 synonym questions)

| Question | 7B | 14B |
|----------|:--:|:--:|
| 你可以联网吗 | ✅ | ✅ |
| 你能联网吗 | ✅ | ✅ |
| 你支持联网吗 | ✅ | ✅ |
| 你能上网查资料吗 | ✅ | ✅ |
| 你可以 web search 吗 | ✅ | ✅ |
| 你是 crawler 吗 | ✅ | ✅ |
| web ask 会写入记忆吗 | ✅ | ✅ |
| chat --web 会自动存网页吗 | ✅ | ✅ |
| web ingest vs web ask | ✅ | ✅ |

- 7B: 8/8 correct (1 hallucinated "v0.1.6")
- 14B: 8/8 correct (zero hallucinations)

## Latency

| Model | First load | Steady-state |
|-------|:---------:|:-----------:|
| 7B | ~3s | ~2.5s |
| 14B | ~13s | ~3-5s |

14B steady-state is close to 7B speed. First load slower but acceptable.

## VRAM

- Idle (7B loaded): 4.8 GB
- 14B loaded: 9.4 GB
- Free: ~2.8 GB
- GPU Guardian: no pressure detected

## Conclusion

1. 7B remains recommended daily/default model ✅
2. 14B deep mode is stable and VRAM-safe ✅
3. 14B eliminates version hallucinations ✅
4. 14B speed acceptable for deep/audit mode ✅
5. Base MemoryQwen does NOT require 14B ✅

## Verdict

**Promote 14B to optional deep mode.** Keep 7B as default. 14B ready for v0.2 ACE/TDR validation baseline.

## Next

Capability Registry / TDR-v1 / ACE-v1 → v0.2 Web UI
