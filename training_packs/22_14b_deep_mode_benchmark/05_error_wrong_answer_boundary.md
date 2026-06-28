# 05 Error Wrong Answer Boundary
## Q001
topic: error_boundary
question: wrong_answer 能当事实吗？
expected_answer: 不能。wrong_answer 是 counterexample，不是正确信息。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q002
topic: error_boundary
question: error_store 存什么？
expected_answer: 用户纠正过的错误案例（错误答案+正确答案+策略）。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q003
topic: error_boundary
question: strategy_store 存什么？
expected_answer: 从错误中提炼的可复用策略。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q004
topic: error_boundary
question: eval 会自动 correct 吗？
expected_answer: 不会。eval run 只生成报告，不自动纠正。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q005
topic: error_boundary
question: judge v4 可靠吗？
expected_answer: 有已知限制。会误判包含关键词的正确回答。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q006
topic: error_boundary
question: M3 eval 36 个 wrong 真实吗？
expected_answer: 不真实。100% 是 judge false positive。0 个真实违规。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q007
topic: error_boundary
question: 能自动把网页内容写成策略吗？
expected_answer: 不能。策略只能通过用户显式 correct/strategy 命令产生。
expected_sources: error_boundary, batch
guard_expected: true
deep_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q008
topic: error_boundary
question: 策略优先级高于模型直觉吗？
expected_answer: 是。strategy_store 的策略优先于模型自身的判断。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q009
topic: error_boundary
question: 纠正后的错误还会再犯吗？
expected_answer: 不会。correct 命令将错误存入 error_store，未来对话会被注入。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q010
topic: error_boundary
question: 怎么查看 error_store 内容？
expected_answer: memory stats 命令显示 error_store 计数。
expected_sources: error_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
