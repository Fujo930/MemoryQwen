# 08 Local Project Assistant
type: m2_eval_completion
updated: 2026-06-27

## Q001
topic: project
question: v0.1 当前完成了多少个 Issue？
expected_answer: #0 到 #24。最近：#23 Judge v3, #24 M2 200Q eval。
expected_sources: project
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q002
topic: project
question: MegaTrain M1 包含多少个 batch？
expected_answer: 7 batches + 1 top-up。覆盖 archive/hardware/CLI/capability/anti-hallucination。
expected_sources: project
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q003
topic: project
question: v0.1.2 Smart Retrieval Gate 解决什么问题？
expected_answer: 每次 chat 不再无差别检索全部 store。闲聊跳过，高风险必须检索。
expected_sources: project
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: project
question: v0.1.2 已发布到哪？
expected_answer: GitHub release v0.1.2。包含 release notes 和变更说明。
expected_sources: project
failure_type_if_wrong: capability_overclaim
trap_level: high
