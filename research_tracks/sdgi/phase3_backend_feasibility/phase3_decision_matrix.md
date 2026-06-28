# SDGI Phase 3 — Decision Matrix

## Candidates for Phase 4

| # | Route | Description | Cost | Risk | Benefit | Rec |
|---|-------|-------------|:---:|:---:|:------:|:---:|
| A | Ollama direct depth | Control layers via Ollama | Low | ❌ Blocked | None | ❌ |
| B | llama.cpp fork | Modify C++ engine for depth hooks | **High** | ⚠️ Fork maintenance | **High** | Defer |
| C | Transformers offline | HF layer truncation experiments | Medium | ⚠️ Memory (16GB FP16) | **High** | ✅ Phase 4 |
| D | Segment-level depth | Block-level uniform depth routing | Low-Med | ⚠️ Block boundary | Medium | Defer |
| E | Draft-Verify ACE-v2 | 7B draft → 14B verify pipeline | **Low** | ✅ Already validated | **Medium** | ✅ Now |
| F | Per-token variable depth | True token-level layer skipping | **Very High** | ❌ KV cache blocker | **Very High** | Research |

## Recommended Phase 4

**Primary: Route C — Transformers Offline Layer Truncation Prototype**
- Verify depth sensitivity with real layer counts
- Test: 4/8/16/28 layers on Qwen2.5-7B
- Measure quality degradation by layer count
- Inform whether llama.cpp fork is worth the investment

**Secondary: Route E — Draft-Verify ACE-v2 Integration**
- Add optional `--verify` flag to chat
- Enable for version_conflict, source_conflict, deep_suggested routes
- Production-ready system-level approximation
- Low risk, immediate value

**Deferred: Route B — llama.cpp Fork**
- Only if Transformers experiments show strong depth-quality correlation
- Requires significant C++ development
- Must solve KV cache discontinuity before per-token depth

**Research only: Route F — Per-token variable depth**
- Blocked by KV cache discontinuity
- Requires projected KV or attention-skip solution
- PhD-level research problem
