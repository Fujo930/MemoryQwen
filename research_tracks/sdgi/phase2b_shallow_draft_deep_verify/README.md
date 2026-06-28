# SDGI Phase 2B — Shallow Draft + Deep Verify

Tests whether a 7B draft → 14B verification pipeline can reduce hallucinations
while preserving speed, as a system-level approximation of selective depth.

## Method
- 7B generates draft answer
- 14B verifies specific claims (not full rewrite)
- Verdict: accept / revise / reject / deep_rewrite_required

## Conditions
A: 7B direct
B: 7B + ACE direct  
C: 14B direct
D: 14B + ACE direct
E: 7B draft → 14B verify
