# Real Eval Questions — 05_error_strategy_real_15

## Q001
topic: 05
question: error_store 的作用是？
expected_answer: 存储用户纠正的错误案例。每条含 wrong_answer(反例)和 correct_answer(正确回答)。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q002
topic: 05
question: wrong_answer 能不能当事实引用？
expected_answer: 绝对不能。wrong_answer 是反例。应用 correct_answer 和 strategy 指导回答。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: high

## Q003
topic: 05
question: strategy_store 的作用是？
expected_answer: 存储可复用的回答策略。通过纠错流程沉淀。遇到相似问题注入 prompt 指导。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q004
topic: 05
question: correct 命令写入什么？
expected_answer: 写入 error_store(错误案例)并自动生成 strategy_store(行为策略)。
expected_sources: error_strategy, cli_mastery
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q005
topic: 05
question: failure_type 有哪些常用类型？
expected_answer: hallucination, source_miss, source_misread, citation_error, strategy_ignored, capability_overclaim, tool_usage_error, small_model_confusion, format_error, reasoning_error。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q006
topic: 05
question: 如果模型看到 error_store 中的 wrong_answer 应该怎么做？
expected_answer: 不能复述 wrong_answer。应使用 correct_answer 和 strategy 中的指导。wrong_answer 只用于避免错误。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: high

## Q007
topic: 05
question: strategy_store 和 error_store 的关系？
expected_answer: error_store 创建修正记录 → StrategyLearningService 自动生成 strategy_store 策略。策略沉淀自错误。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: medium

## Q008
topic: 05
question: strategy 优先于模型直觉吗？
expected_answer: 是。如果策略和模型直觉冲突，按策略修正回答。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: strategy_ignored
trap_level: high

## Q009
topic: 05
question: correct 后 strategy_store 会自动更新吗？
expected_answer: 是。StrategyLearningService 会根据纠错内容自动生成/更新策略。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q010
topic: 05
question: 复测纠错的作用？
expected_answer: 验证 error/strategy 是否注入 prompt，确认模型不再重复相同错误。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q011
topic: 05
question: 策略的典型格式？
expected_answer: 适用场景 + 避免什么错误 + 应该怎么回答 + 使用什么验证方法。短、明确、可复用。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q012
topic: 05
question: error_store 存储什么字段？
expected_answer: task, session_id, wrong_answer, correct_answer, failure_type, strategy, metadata。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q013
topic: 05
question: 如果模型把 wrong_answer 当事实回答怎么办？
expected_answer: 立即 correct 纠错。failure_type: source_misread。strategy: wrong_answer 是反例不是事实。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: high

## Q014
topic: 05
question: strategy_store 中的 strategy 如何被检索？
expected_answer: BM25 keyword search → recent fallback。prompt 中显示为 [T1][T2]。
expected_sources: error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q015
topic: 05
question: 小模型是否容易把反例当事实？
expected_answer: 是。3B 容易把 error_store 中的 wrong_answer 当成权威信息。7B 表现更好。
expected_sources: error_strategy, model_hardware
guard_expected: true
failure_type_if_wrong: small_model_confusion
trap_level: high

