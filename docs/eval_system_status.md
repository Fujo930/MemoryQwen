# Eval System Status

**updated:** 2026-06-27

## Eval Packs

| pack | questions | status |
|------|:---------:|:------:|
| 14_validation_questions_expanded | 460 | COMPLETE |
| 15_strategy_seed_pack | — | COMPLETE |
| 16_real_eval_questions | 130 | COMPLETE |
| 17_megatrain_m1_grand_eval | — | COMPLETE |
| 18_megatrain_m2_200_eval | 200 | COMPLETE |
| **19_megatrain_m3_eval** | **312** | **COMPLETE** |

## M3 Eval Results

- Full 300 executed (run 9eff56dd)
- Raw heuristic wrong: 36
- Manual verified false positives: 36
- Real critical violations: 0

## Judge Status

- Judge v4 (heuristic, negation-aware): active
- Known limitation: false positives on negated wrong_answer/PDF/embedding answers
- Next: Judge v5 (LLM-as-Judge) for complex semantic cases

## Eval Runner

- eval run: working
- eval mark: working
- eval corrections export: working
- heuristic judge: working (with known limitations)
- LLM judge: not yet implemented
