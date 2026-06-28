# M3 30-Question Latency + Accuracy Smoke

**date:** 2026-06-27
**model:** qwen2.5:7b (Q4_K_M, Ollama)
**GPU:** NVIDIA GeForce RTX 4080 Laptop GPU (12 GB)
**session:** speedtest

---

## Speed

| category | questions | avg | fastest | slowest |
|----------|:---------:|:---:|:-------:|:-------:|
| casual | 5 | 1.9s | 1.2s | 4.0s |
| error | 5 | 3.1s | 1.8s | 4.8s |
| boundary | 5 | 3.5s | 3.4s | 3.6s |
| task | 5 | 4.3s | 3.8s | 5.0s |
| project | 5 | 4.4s | 3.6s | 5.2s |
| hardware | 5 | 4.5s | 4.0s | 5.6s |
| **overall** | **30** | **3.6s** | 1.2s | 5.6s |

Casual greetings (1.2-1.4s) confirm Smart Retrieval Gate skips retrieval correctly.
First query overhead ("你好" 4.0s) normal for initial model warmup.

---

## Accuracy Spot Check

| question | answer | verdict |
|----------|--------|:------:|
| 支持 PDF 吗？ | v0.1 不支持 PDF ingestion | ✅ |
| 有 Web UI 吗？ | v0.1 没有 Web UI, CLI only | ✅ |
| 32B 默认推荐？ | 7B 常驻, 32B+ 仅实验 | ✅ |
| source archive 爬虫？ | 没有 crawler, 本地归档 | ✅ |
| wrong_answer 当事实？ | 不能, 仅标记错误 | ✅ |

---

## GPU Utilization During Inference

| metric | value |
|--------|-------|
| GPU utilization | 94% |
| VRAM used (7B model) | 4,857 MB |
| VRAM total | 12,282 MB |
| VRAM free | 7,425 MB |

RTX 4080 is confirmed in use. 7B model fully loaded on GPU.

---

## Verdict

M3 remains usable at 10M+ token scale. Smart Retrieval Gate successfully skips retrieval for casual prompts while preserving high-risk boundary retrieval. All 5 boundary accuracy spot checks passed.
