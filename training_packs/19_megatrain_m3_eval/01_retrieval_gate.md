# 01 Retrieval Gate
type: m3_eval
updated: 2026-06-27

## Q001
topic: retrieval_gate
question: 检索门控在"你好"时会检索吗？
expected_answer: 不会。casual_skip 规则下普通问候跳过检索。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q002
topic: retrieval_gate
question: "支持 PDF 吗？"会触发什么级别的检索？
expected_answer: high 级别。检索 knowledge+error+strategy 全部 store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: true

## Q003
topic: retrieval_gate
question: MemoryQwen 项目问题会检索哪些 store？
expected_answer: knowledge_store + strategy_store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q004
topic: retrieval_gate
question: 检索门控能关闭吗？
expected_answer: 可以。设置 agent.use_retrieval_gate: false。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q005
topic: retrieval_gate
question: 常见问候跳过检索有哪些？
expected_answer: 你好 hi hello 谢谢 好的 拜拜 等。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q006
topic: retrieval_gate
question: 检索门控在"你好"时会检索吗？
expected_answer: 不会。casual_skip 规则下普通问候跳过检索。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q007
topic: retrieval_gate
question: "支持 PDF 吗？"会触发什么级别的检索？
expected_answer: high 级别。检索 knowledge+error+strategy 全部 store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: true

## Q008
topic: retrieval_gate
question: MemoryQwen 项目问题会检索哪些 store？
expected_answer: knowledge_store + strategy_store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q009
topic: retrieval_gate
question: 检索门控能关闭吗？
expected_answer: 可以。设置 agent.use_retrieval_gate: false。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q010
topic: retrieval_gate
question: 常见问候跳过检索有哪些？
expected_answer: 你好 hi hello 谢谢 好的 拜拜 等。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q011
topic: retrieval_gate
question: 检索门控在"你好"时会检索吗？
expected_answer: 不会。casual_skip 规则下普通问候跳过检索。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q012
topic: retrieval_gate
question: "支持 PDF 吗？"会触发什么级别的检索？
expected_answer: high 级别。检索 knowledge+error+strategy 全部 store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: true

## Q013
topic: retrieval_gate
question: MemoryQwen 项目问题会检索哪些 store？
expected_answer: knowledge_store + strategy_store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q014
topic: retrieval_gate
question: 检索门控能关闭吗？
expected_answer: 可以。设置 agent.use_retrieval_gate: false。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q015
topic: retrieval_gate
question: 常见问候跳过检索有哪些？
expected_answer: 你好 hi hello 谢谢 好的 拜拜 等。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q016
topic: retrieval_gate
question: 检索门控在"你好"时会检索吗？
expected_answer: 不会。casual_skip 规则下普通问候跳过检索。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q017
topic: retrieval_gate
question: "支持 PDF 吗？"会触发什么级别的检索？
expected_answer: high 级别。检索 knowledge+error+strategy 全部 store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: true

## Q018
topic: retrieval_gate
question: MemoryQwen 项目问题会检索哪些 store？
expected_answer: knowledge_store + strategy_store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q019
topic: retrieval_gate
question: 检索门控能关闭吗？
expected_answer: 可以。设置 agent.use_retrieval_gate: false。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q020
topic: retrieval_gate
question: 常见问候跳过检索有哪些？
expected_answer: 你好 hi hello 谢谢 好的 拜拜 等。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q021
topic: retrieval_gate
question: 检索门控在"你好"时会检索吗？
expected_answer: 不会。casual_skip 规则下普通问候跳过检索。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q022
topic: retrieval_gate
question: "支持 PDF 吗？"会触发什么级别的检索？
expected_answer: high 级别。检索 knowledge+error+strategy 全部 store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: true

## Q023
topic: retrieval_gate
question: MemoryQwen 项目问题会检索哪些 store？
expected_answer: knowledge_store + strategy_store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q024
topic: retrieval_gate
question: 检索门控能关闭吗？
expected_answer: 可以。设置 agent.use_retrieval_gate: false。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q025
topic: retrieval_gate
question: 常见问候跳过检索有哪些？
expected_answer: 你好 hi hello 谢谢 好的 拜拜 等。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q026
topic: retrieval_gate
question: 检索门控在"你好"时会检索吗？
expected_answer: 不会。casual_skip 规则下普通问候跳过检索。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q027
topic: retrieval_gate
question: "支持 PDF 吗？"会触发什么级别的检索？
expected_answer: high 级别。检索 knowledge+error+strategy 全部 store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: true

## Q028
topic: retrieval_gate
question: MemoryQwen 项目问题会检索哪些 store？
expected_answer: knowledge_store + strategy_store。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q029
topic: retrieval_gate
question: 检索门控能关闭吗？
expected_answer: 可以。设置 agent.use_retrieval_gate: false。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false

## Q030
topic: retrieval_gate
question: 常见问候跳过检索有哪些？
expected_answer: 你好 hi hello 谢谢 好的 拜拜 等。
expected_sources: retrieval_gate_edge_cases, batch_02
failure_type_if_wrong: capability_overclaim
trap_level: medium
guard_expected: false
