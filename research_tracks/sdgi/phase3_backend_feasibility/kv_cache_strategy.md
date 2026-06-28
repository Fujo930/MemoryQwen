# SDGI Phase 3 — KV Cache Strategy for Variable Depth Inference

## The Core Problem

Transformer attention requires all tokens to have KV vectors at the SAME dimension for each layer.

If token A exits at layer 8 and token B continues to layer 32:
- Layer 9-32 attention: token B needs KV from token A, but token A has no KV for layers 9-32
- This is the **KV cache discontinuity problem**

## Visualization

```
Layer:  1  2  3  4  5  6  7  8  9 10 ... 32
Token1: K1 K2 K3 K4 K5 K6 K7 K8  -  - ...  -   (shallow exit at L8)
Token2: K1 K2 K3 K4 K5 K6 K7 K8 K9 K10... K32  (full depth)
                                        ↑
                          Token2 needs Token1 KV at L9-L32
                          But Token1 has NO KV at L9-L32!
```

## Candidate Strategies

### Strategy A: Per-Sequence Uniform Depth
All tokens use same depth. No discontinuity. Simplest.
- ✅ No KV cache issues
- ❌ No per-token benefit
- **Recommendation: Good baseline for Phase 4**

### Strategy B: Per-Block / Per-Segment Depth
Group tokens into blocks. Each block uses uniform depth.
- ✅ KV cache consistent within block
- ⚠️ Block boundaries need transition logic
- **Recommendation: Viable intermediate step**

### Strategy C: Projected KV Filler
For shallow tokens at deep layers: project last KV to required dimensionality.
- ⚠️ Needs per-layer projection matrices (trainable or static)
- ❌ Adds compute overhead
- **Recommendation: Research only, not prototype-ready**

### Strategy D: Attention Mask / Skip
Deep tokens simply don't attend to shallow tokens at layers beyond exit point.
- ⚠️ May lose important context
- ✅ Simple implementation
- **Recommendation: Worth testing in Phase 4**

### Strategy E: Shallow Draft + Deep Verify (SDGI Phase 2B)
Two-pass: shallow generates draft, deep verifies. No KV sharing between passes.
- ✅ No KV cache issues at all
- ✅ Already validated in Phase 2B pilot
- ❌ Two model calls = higher latency
- **Recommendation: Ready for ACE-v2 integration now**

### Strategy F: Full-Depth Fallback
All tokens run full depth if any token in sequence needs it.
- ✅ Conservative, safe
- ❌ No efficiency gain
- **Recommendation: Fallback only, not primary strategy**

## Assessment

| Strategy | KV Issue | Implementability | Efficiency Gain | Priority |
|----------|:--------:|:----------------:|:--------------:|:--------:|
| A: Uniform depth | ✅ None | Easy | Low (per sequence) | Phase 4 baseline |
| B: Block depth | ⚠️ Minor | Medium | Medium | Phase 4 candidate |
| C: Projected KV | ❌ Complex | Hard | High (theoretical) | Research only |
| D: Attention skip | ⚠️ Medium | Medium | Medium | Phase 4 test |
| E: Draft-verify | ✅ None | Already done | Medium (per question) | ACE-v2 ready |
| F: Full fallback | ✅ None | Trivial | None | Safety net |

## Recommended Phase 4 Path

1. **Immediate:** Draft-Verify as ACE-v2 optional mode (Strategy E)
2. **Phase 4 prototype:** Uniform depth ablation via Transformers (Strategy A)
3. **Phase 4 experiment:** Attention-skip test on block-level depth (Strategy D)
4. **Deferred:** Projected KV (Strategy C) — needs more research
