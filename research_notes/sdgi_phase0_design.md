# SDGI Research Track — Phase 0: Token Difficulty Signal Collection

## Goal

Verify the hypothesis: **Different tokens/phrases have stable, measurable differences in computational depth requirements.**

Phase 0 does NOT modify llama.cpp or Transformer internals.
It uses existing ACE/TDR infrastructure as an external observation layer.

## Core Question

Do tokens that TDR-v1 flags as "high difficulty" (deep_suggested, judge_review, manual_review)
actually correlate with:
1. 7B answer inconsistency (same question → different answers)
2. 7B/14B disagreement (14B correct, 7B wrong)
3. Response length / verbosity changes

## Data Points Per Question

For each test question, record:
- question text
- TDR route + trigger_tokens + risk_scores
- 7B answer text + latency
- 14B answer text + latency
- whether 7B answer is consistent across 3 runs
- whether 14B is more stable

## Test Set

Focus on the 7 conflict categories where 7B is known to oscillate:
1. Internet Query capability synonym questions (9 questions)
2. version conflict questions (old vs new data)
3. PDF/WebUI/embedding boundary questions
4. source archive vs crawler questions
5. deep_suggested planning questions
6. judge_review risk questions
7. 14B deep mode benchmark questions (80)

## Analysis Questions

1. Which trigger_tokens most strongly predict 7B inconsistency?
2. Is planning_depth score correlated with 7B/14B divergence?
3. Are there tokens where 14B consistently outperforms 7B?
4. Can we identify a "difficulty signature" (token → risk_score) that predicts when deep mode helps?

## Deliverables

- `scripts/collect_token_signals.py` — data collector
- `research_notes/sdgi_phase0_data.json` — raw data
- `research_notes/sdgi_phase0_report.md` — analysis report
- `research_notes/token_difficulty_signatures.md` — token signatures

## Hard Rules

- Does NOT modify llama.cpp
- Does NOT modify Transformer forward pass
- Does NOT auto-escalate to 14B
- 14B runs are explicit and optional
- All data is external observation
- Phase 0 proves/disproves hypothesis, does not implement
