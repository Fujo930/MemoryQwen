# 14B Deep Mode Benchmark

date: 2026-06-28
status: COMPLETE

## Setup

- GPU: NVIDIA GeForce RTX 4080 Laptop (12 GB)
- Model: qwen2.5:14b (Q4_K_M, 9.0 GB)
- Ollama: localhost:11434

## VRAM

| state | usage |
|-------|:-----:|
| idle | 99 MB |
| 14B loaded | 9,363 MB (76%) |
| GPU utilization | 97% |
| Temperature | 58°C |

## Speed

| metric | 7B | 14B |
|--------|:--:|:---:|
| First query (warmup) | ~4s | ~11s |
| Steady state avg | 3.6s | 3.8s |
| Fastest | 1.2s | 3.7s |
| Slowest | 5.6s | 4.7s |

14B steady-state speed is nearly identical to 7B on RTX 4080.

## Internet Query Consistency

| question | 7B | 14B |
|----------|:--:|:---:|
| 你可以联网吗 | ✅ | ✅ (consistent wording) |
| 你能联网吗 | ✅ | ✅ (identical answer) |
| 你支持联网吗 | ✅ | ✅ (identical answer) |
| 你能上网查资料吗 | ✅ | ✅ (identical answer) |
| 你可以web search吗 | ✅ | ✅ (identical answer) |
| 你是crawler吗 | ⚠️ v0.1 | ✅ v0.1.5 |
| web ask会写入记忆吗 | ✅ | ✅ |
| chat --web存网页吗 | ✅ | ✅ |
| web ingest vs ask | ✅ | ✅ (more precise) |

**7B: 8/9 (89%) | 14B: 9/9 (100%)**

## Verdict

14B promoted to optional deep mode. 7B remains default daily model. 14B shows superior consistency with negligible speed penalty on RTX 4080.
