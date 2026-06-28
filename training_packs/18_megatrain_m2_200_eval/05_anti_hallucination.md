# 05 Anti Hallucination M2 Eval
类型: m2_eval_questions
更新时间: 2026-06-27

## Q001
topic: anti_hallucination
question: 资料不足时应怎么回答？
expected_answer: 明确说资料不足无法确定，不编造信息。如基于常识标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q002
topic: anti_hallucination
question: sources 没命中能编答案吗？
expected_answer: 不能。必须承认资料不足。基于常识的内容要标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q003
topic: anti_hallucination
question: error_store 的 wrong_answer 能当事实吗？
expected_answer: 绝对不能。wrong_answer 是反例，只能避免错误。用 correct_answer 和 strategy。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q004
topic: anti_hallucination
question: strategy 和模型直觉冲突时听谁的？
expected_answer: 听 strategy。strategy_store 策略优先于模型直觉。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q005
topic: anti_hallucination
question: 未来计划能说成当前已实现吗？
expected_answer: 不能。Web UI、FastAPI、PDF、embedding 都是 v0.2 计划。必须说 v0.1 未实现。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q006
topic: anti_hallucination
question: 资料不足时应怎么回答？
expected_answer: 明确说资料不足无法确定，不编造信息。如基于常识标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q007
topic: anti_hallucination
question: sources 没命中能编答案吗？
expected_answer: 不能。必须承认资料不足。基于常识的内容要标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q008
topic: anti_hallucination
question: error_store 的 wrong_answer 能当事实吗？
expected_answer: 绝对不能。wrong_answer 是反例，只能避免错误。用 correct_answer 和 strategy。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q009
topic: anti_hallucination
question: strategy 和模型直觉冲突时听谁的？
expected_answer: 听 strategy。strategy_store 策略优先于模型直觉。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q010
topic: anti_hallucination
question: 未来计划能说成当前已实现吗？
expected_answer: 不能。Web UI、FastAPI、PDF、embedding 都是 v0.2 计划。必须说 v0.1 未实现。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q011
topic: anti_hallucination
question: 资料不足时应怎么回答？
expected_answer: 明确说资料不足无法确定，不编造信息。如基于常识标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q012
topic: anti_hallucination
question: sources 没命中能编答案吗？
expected_answer: 不能。必须承认资料不足。基于常识的内容要标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q013
topic: anti_hallucination
question: error_store 的 wrong_answer 能当事实吗？
expected_answer: 绝对不能。wrong_answer 是反例，只能避免错误。用 correct_answer 和 strategy。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q014
topic: anti_hallucination
question: strategy 和模型直觉冲突时听谁的？
expected_answer: 听 strategy。strategy_store 策略优先于模型直觉。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q015
topic: anti_hallucination
question: 未来计划能说成当前已实现吗？
expected_answer: 不能。Web UI、FastAPI、PDF、embedding 都是 v0.2 计划。必须说 v0.1 未实现。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q016
topic: anti_hallucination
question: 资料不足时应怎么回答？
expected_answer: 明确说资料不足无法确定，不编造信息。如基于常识标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q017
topic: anti_hallucination
question: sources 没命中能编答案吗？
expected_answer: 不能。必须承认资料不足。基于常识的内容要标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q018
topic: anti_hallucination
question: error_store 的 wrong_answer 能当事实吗？
expected_answer: 绝对不能。wrong_answer 是反例，只能避免错误。用 correct_answer 和 strategy。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q019
topic: anti_hallucination
question: strategy 和模型直觉冲突时听谁的？
expected_answer: 听 strategy。strategy_store 策略优先于模型直觉。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q020
topic: anti_hallucination
question: 未来计划能说成当前已实现吗？
expected_answer: 不能。Web UI、FastAPI、PDF、embedding 都是 v0.2 计划。必须说 v0.1 未实现。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q021
topic: anti_hallucination
question: 资料不足时应怎么回答？
expected_answer: 明确说资料不足无法确定，不编造信息。如基于常识标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q022
topic: anti_hallucination
question: sources 没命中能编答案吗？
expected_answer: 不能。必须承认资料不足。基于常识的内容要标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q023
topic: anti_hallucination
question: error_store 的 wrong_answer 能当事实吗？
expected_answer: 绝对不能。wrong_answer 是反例，只能避免错误。用 correct_answer 和 strategy。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q024
topic: anti_hallucination
question: strategy 和模型直觉冲突时听谁的？
expected_answer: 听 strategy。strategy_store 策略优先于模型直觉。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q025
topic: anti_hallucination
question: 未来计划能说成当前已实现吗？
expected_answer: 不能。Web UI、FastAPI、PDF、embedding 都是 v0.2 计划。必须说 v0.1 未实现。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q026
topic: anti_hallucination
question: 资料不足时应怎么回答？
expected_answer: 明确说资料不足无法确定，不编造信息。如基于常识标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q027
topic: anti_hallucination
question: sources 没命中能编答案吗？
expected_answer: 不能。必须承认资料不足。基于常识的内容要标注推测。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q028
topic: anti_hallucination
question: error_store 的 wrong_answer 能当事实吗？
expected_answer: 绝对不能。wrong_answer 是反例，只能避免错误。用 correct_answer 和 strategy。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q029
topic: anti_hallucination
question: strategy 和模型直觉冲突时听谁的？
expected_answer: 听 strategy。strategy_store 策略优先于模型直觉。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q030
topic: anti_hallucination
question: 未来计划能说成当前已实现吗？
expected_answer: 不能。Web UI、FastAPI、PDF、embedding 都是 v0.2 计划。必须说 v0.1 未实现。
expected_sources: anti_hallucination
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium
## Q031
topic: anti_hallucination
question: 怎么区分 error_store 和 strategy_store？
expected_answer: error_store 是错误案例（反例库），strategy_store 是正确策略（行为指南库）。不能用 error_store 当事实。
expected_sources: anti_hallucination
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q032
topic: anti_hallucination
question: 如果 expected_answer 说“不能确定”，模型回答“不能确定”对不对？
expected_answer: 对。这是谨慎不确定性，Judge v3 判为 correct_candidate 而非 wrong。
expected_sources: anti_hallucination
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q033
topic: anti_hallucination
question: error_store 和 strategy_store 的区别？
expected_answer: error_store=反例库(wrong_answer)。strategy_store=策略库(行为指南)。不能混用。
expected_sources: anti_hallucination
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q034
topic: anti_hallucination
question: expected_answer=不能确定，模型答不能确定，对不对？
expected_answer: 对。Judge v3 判 correct_candidate。
expected_sources: anti_hallucination
failure_type_if_wrong: capability_overclaim
trap_level: high

