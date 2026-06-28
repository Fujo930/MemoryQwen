# SDGI Phase 3 — Backend Feasibility Analysis

**Date:** 2026-06-28
**Status:** Research Notes

## Current Inference Backend

MemoryQwen uses Ollama → llama.cpp → GGUF for inference. The backend chain is:

```
MemoryQwen CLI → Ollama API (localhost:11434) → llama.cpp → GGUF model → GPU
```

## Can We Control Layer Depth?

### Ollama Layer

Ollama provides a high-level API for chat/generate. It does NOT expose layer-level control. Options:
- `num_predict`: max tokens
- `temperature`, `top_p`, `top_k`: sampling
- `num_ctx`: context window size
- `num_gpu`: GPU layers (offloading)

**None of these control which specific layers are computed during inference.**

### llama.cpp Layer

llama.cpp (the underlying C++ engine) has more internal hooks:
- `n_gpu_layers`: offloads first N layers to GPU, rest to CPU
- Internal layer loop: iterates through all transformer layers
- Could theoretically be modified to stop at layer N
- But: KV cache assumes uniform depth across all tokens

**llama.cpp does NOT support per-token layer depth out of the box. A fork would be required.**

### GGUF Model Format

GGUF stores model weights in a serialized format. The layer weights are stored but not individually addressable at inference time without modifying the loader.

## Feasibility Assessment

| Component | Fine-grained depth control? | Effort |
|-----------|:---------------------------:|:------:|
| Ollama API | ❌ No | — |
| llama.cpp | ⚠️ Possible with fork | High (C++ changes) |
| GGUF loader | ⚠️ Possible | Medium |
| Transformers/HF | ✅ Yes (offline) | Medium (Python) |
| PyTorch direct | ✅ Yes | High (reimplement inference) |

## Recommended Path for Phase 4

**Path B: HuggingFace Transformers offline layer truncation prototype.**

Rationale:
1. Python-based — can be done without C++ fork
2. Qwen2.5 model available on HuggingFace
3. Can manually truncate layers: `model.model.layers = model.model.layers[:N]`
4. Can test same prompt at different depths
5. Does NOT require modifying production inference code
6. Results can inform whether a llama.cpp fork is worthwhile

## What We CAN Test with Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B")
# Truncate to first 8 layers
model.model.layers = model.model.layers[:8]
# Run inference at reduced depth
```

Limitations:
- Slow (no GGUF quantization)
- High memory (~16GB for 7B in FP16)
- Not suitable for production
- Excellent for depth ablation experiments
