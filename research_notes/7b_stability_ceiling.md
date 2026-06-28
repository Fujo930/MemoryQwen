# 7B Stability Ceiling

date: 2026-06-28

## Observation

qwen2.5:7b (Q4_K_M) successfully validated the 10M-token M3 training target with 0 real critical violations. However, in live testing with v0.1.5 Internet Query, the model shows instability when sources conflict.

## Specific Failure Mode

When the system prompt says "v0.1.5 supports web" but 43K training chunks say "v0.1 has no web", the model oscillates between answers:
- "v0.1.5 支持联网查询" — correct
- "v0.1 没有联网搜索功能" — incorrect (outdated)
- "资料不足，无法确定" — conservative hedge

Same question, three runs, three different answers.

## Root Cause

7B's parameter count is insufficient to resolve source authority conflicts. The model cannot reliably determine which source (system prompt vs training data) takes priority. This is a **parameter count limitation**, not a prompt engineering failure.

## Mitigation

1. System prompt v0.1.5 capability baseline injection
2. CapabilityBoundaryGuard forced instructions
3. Training data updates (09_capability_boundaries.md)

These reduce but do not eliminate the instability.

## Resolution Path

14B deep mode fully resolves this category of conflict (100% consistency vs 89% for 7B).

## Implications for v0.2

Token-Difficulty Routing (TDR) should route capability-conflict questions to 14B even without explicit --deep flag. A Capability Registry could serve as the authoritative source, eliminating the training data vs system prompt conflict entirely.
