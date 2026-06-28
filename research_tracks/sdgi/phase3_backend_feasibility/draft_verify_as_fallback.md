# Draft-Verify as ACE-v2 Optional Mode

Based on SDGI Phase 2B pilot (Issue #39).

## Integration Proposal

Add to ACE-v2 as optional verification mode:

```yaml
ace:
  draft_verify:
    enabled: false  # default off
    routes:
      - deep_suggested     # planning questions
      - manual_review      # source conflict
      - judge_review       # high hallucination risk
    auto_enabled: false    # never auto-trigger
```

## CLI

```bash
python -m src.cli chat "帮我规划 v0.3 路线" --verify
```

## Behavior

1. ACE routes to deep_suggested
2. 7B generates draft answer (with ACE context)
3. 14B verifies draft against checklist:
   - Version hallucination?
   - Capability overclaim?
   - Registry conflict?
   - Planning gaps?
4. If ACCEPT → return draft
5. If REVISE → return draft with corrections
6. If REJECT → 14B generates fresh answer

## Recommended Routes

| Route | Draft-Verify? | Reason |
|-------|:------------:|--------|
| shallow | ❌ No | 7B raw sufficient |
| capability_registry | ❌ No | Registry is authoritative |
| memory | ❌ No | Retrieval handles this |
| web | ❌ No | Web context provides evidence |
| deep_suggested | ✅ Yes | Planning needs verification |
| judge_review | ✅ Yes | Hallucination risk needs check |
| manual_review | ✅ Yes | Source conflict needs audit |

## Safety Constraints

- Never auto-enabled — requires explicit `--verify` flag
- Never replaces Guard or Registry
- Never writes to memory
- Never auto-escalates to 14B without verification
- 14B verify only — never uses 14B for full generation unless REJECT verdict
