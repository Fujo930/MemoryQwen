# SDGI Phase 3 — Backend Feasibility Report

**Date:** 2026-06-28
**Status:** COMPLETE (research analysis — no code changes to production)

## Executive Summary

Phase 3 investigated whether current inference backends can support per-token variable depth computation. The answer is **no — not without significant engineering work.** However, two viable paths forward were identified: a low-risk system-level path (draft-verify ACE-v2) and a medium-risk research path (Transformers offline layer truncation).

## Key Findings

### 1. Ollama Cannot Support Per-Token Depth

- Ollama API provides no layer-level control
- Only exposes: temperature, top_p, num_ctx, num_gpu
- Fine-grained depth control requires going below Ollama to llama.cpp

### 2. llama.cpp Fork Is Required for Internal Depth Control

- llama.cpp has internal layer loop but no per-token depth API
- KV cache assumes uniform depth across all tokens
- Fork would require: depth hooks + KV cache discontinuity handling
- **Estimated effort: 2-4 weeks of C++ development for prototype**

### 3. HuggingFace Transformers Can Do Offline Depth Ablation

- Layer truncation is trivial: `model.model.layers = model.model.layers[:N]`
- Can test same prompt at 4, 8, 16, 28 layers
- Limitation: FP16 memory (~16GB) and no GGUF quantization
- **Best path for quick depth-quality experiments without C++ fork**

### 4. KV Cache Discontinuity Is THE Core Blocker

The fundamental problem: if token A exits at layer 8 but token B continues to layer 32, layers 9-32 have no KV vectors for token A. Six strategies were evaluated (see kv_cache_strategy.md).

### 5. Draft-Verify Is Production-Ready Now

Phase 2B validated 7B draft → 14B verify on 3 cases (0 false accepts). This approach:
- Bypasses KV cache issues entirely (two separate model calls)
- Already working at system level
- Can be integrated as ACE-v2 optional `--verify` mode
- **Low risk, immediate value**

## Feasibility Assessment Matrix

| Component | Supports depth control? | Production ready? |
|-----------|:----------------------:|:-----------------:|
| Ollama API | ❌ No | — |
| llama.cpp (stock) | ❌ No | — |
| llama.cpp (forked) | ⚠️ With C++ changes | ❌ Needs 2-4 weeks |
| Transformers/HF | ✅ Offline only | ❌ 16GB FP16, slow |
| Draft-Verify | ✅ System-level | ✅ Now |
| True per-token depth | ❌ Blocked by KV cache | ❌ Research only |

## Decision Matrix

| Route | Cost | Risk | Benefit | Recommendation |
|-------|:----:|:----:|:-------:|:--------------|
| Ollama depth control | Low | ❌ Blocked | None | **Rejected** |
| llama.cpp fork | High | Medium | High | **Deferred to post-Phase 4** |
| Transformers offline | Medium | Low | High | **Phase 4A — Recommended** |
| Draft-Verify ACE-v2 | Low | ✅ Validated | Medium | **Phase 4B — Implement now** |
| Per-token variable depth | Very High | ❌ Blocker | Very High | **Research — deferred** |

## Recommended Phase 4 Path

### Phase 4A: Transformers Offline Layer Truncation Prototype
**Priority: HIGH**
- Test Qwen2.5-7B at 4/8/16/28 layers on 50 SDGI questions
- Measure quality degradation per layer count
- Identify minimum layer count for each difficulty class
- Determine if llama.cpp fork is worth the investment

### Phase 4B: ACE-v2 Draft-Verify Optional Mode
**Priority: MEDIUM (immediate value)**
- Add `--verify` flag to CLI
- Integrate verifier prompt into ACE context
- Enable for deep_suggested, manual_review, judge_review routes
- Default: off (preserves current behavior)

## Answers to Phase 3 Core Questions

1. **Can llama.cpp/Ollama support layer truncation?** Not without a fork. Ollama is the wrong abstraction layer.

2. **Can Transformers do offline depth ablation?** Yes. Trivial to implement. Best for research.

3. **What is the core blocker for per-token depth?** KV cache discontinuity. All tokens must have KV at same dimensions for attention to work.

4. **Is KV cache a blocker?** Yes — for true per-token depth. No — for system-level draft-verify approach.

5. **Viable minimum prototype?** Two options: (a) Transformers offline layer truncation, (b) Draft-verify ACE-v2 mode.

6. **Should draft-verify be ACE-v2?** Yes, as optional `--verify` mode for specific routes.

7. **Is Phase 4 worth it?** Yes. Phase 4A establishes depth-quality baseline. Phase 4B adds immediate production value.

## Verdict

**Phase 3 identifies two viable Phase 4 paths and defers per-token variable depth to post-Phase 4 research.**

Backend reality: true per-token variable depth requires llama.cpp fork + KV cache solution = 4-8 weeks of engineering. The system-level draft-verify approach provides immediate value while the research path continues in parallel.

## Next Steps

- **Issue #41A:** Transformers Offline Layer Truncation Prototype
- **Issue #41B:** ACE-v2 Draft-Verify Optional Mode
