# Capability Boundary M1 Eval
类型: grand_eval_questions
更新时间: 2026-06-27

## Q001
topic: capability_boundary
question: MemoryQwen v0.1 支持 PDF ingestion 吗？
expected_answer: 不支持。v0.1 只支持 .txt 和 .md 文件导入。PDF ingestion 是 v0.2 未来计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q002
topic: capability_boundary
question: MemoryQwen v0.1 支持 embedding/vector DB 吗？
expected_answer: 不支持。v0.1 使用 BM25 关键词检索，没有 embedding 或向量数据库。embedding 是 v0.2 未来计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q003
topic: capability_boundary
question: MemoryQwen v0.1 有 FastAPI server 吗？
expected_answer: 没有。v0.1 当前没有 FastAPI server。FastAPI 是 v0.2 未来计划。当前所有功能通过 CLI 操作。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q004
topic: capability_boundary
question: MemoryQwen v0.1 有 daemon/tray 吗？
expected_answer: 没有。v0.1 没有后台 daemon，没有 Windows tray。GPU Guardian 只是查询工具。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q005
topic: capability_boundary
question: MemoryQwen v0.1 会 kill 进程吗？
expected_answer: 不会。v0.1 不会 kill 任何用户进程。GPU Guardian 只做检测和策略建议，不执行 kill 操作。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q006
topic: capability_boundary
question: MemoryQwen v0.1 支持 LoRA 或模型微调吗？
expected_answer: 不支持。v0.1 不修改模型权重。AutoModelAdapter 是轻量模型能力评估工具，不是 LoRA。v0.1 的训练是指资料训练而非权重训练。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q007
topic: capability_boundary
question: 列举 3 个 v0.1 已实现的功能
expected_answer: .txt/.md ingestion、chat、correct (纠错)、memory stats、guardian status、task management、eval runner、source archive。任选 3 个。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q008
topic: capability_boundary
question: 列举 3 个 v0.1 未实现的功能
expected_answer: Web UI、PDF ingestion、embedding/vector DB、daemon/tray、Internet Query、crawler、LoRA、FastAPI server。任选 3 个。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q009
topic: capability_boundary
question: Capability Boundary Guard 做什么？
expected_answer: 检测用户问题是否涉及 v0.1 能力边界。如果触发，在 prompt 中插入 10 条强制规则（high/medium/low 三级），防止模型 hallucinate 不支持的功能。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q010
topic: capability_boundary
question: AutoModelAdapter 是什么？
expected_answer: 轻量模型能力评估工具，用于 eval 模型 profile。不修改模型权重。不是 LoRA，不是微调。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium
