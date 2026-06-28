## Q001
topic: mixed_trap
question: Retrieval Gate 在"你好"时检索吗？
expected_answer: 不会。casual_skip 规则下跳过检索。v0.1.2 新特性。
expected_sources: mixed_trap
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q002
topic: mixed_trap
question: Judge v3 把所有"不能确定"判 correct？
expected_answer: 不会。仅在无 overclaim 的高风险边界题。明确事实题仍需具体答案。
expected_sources: mixed_trap
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q003
topic: mixed_trap
question: 22K chunks 下每次聊天都全搜？
expected_answer: 不需要。v0.1.2 Smart Retrieval Gate 按需检索。
expected_sources: mixed_trap
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: mixed_trap
question: v0.1.2 的 smart retrieval gate 能否关闭？
expected_answer: 可以。配置 agent.use_retrieval_gate: false 即可关闭，恢复旧行为。
expected_sources: retrieval_gate
failure_type_if_wrong: source_miss
trap_level: medium

