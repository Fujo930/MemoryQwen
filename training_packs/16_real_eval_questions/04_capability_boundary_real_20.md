# Real Eval Questions — 04_capability_boundary_real_20

## Q001
topic: 04
question: v0.1 有 Web UI 吗？
expected_answer: 没有。v0.1 是纯 CLI Developer Preview。Web UI 是 v0.2 未来计划。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q002
topic: 04
question: v0.1 支持 PDF 吗？
expected_answer: 不支持。只支持 .txt 和 .md。PDF ingestion 是 v0.2 计划。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q003
topic: 04
question: v0.1 支持 DOCX 吗？
expected_answer: 不支持。只支持 .txt 和 .md。DOCX 是 v0.2 计划。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: 04
question: v0.1 有 embedding/向量搜索吗？
expected_answer: 没有。v0.1 只有 BM25 关键词检索。Embedding 是 v0.2 计划。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q005
topic: 04
question: v0.1 有 FastAPI server 吗？
expected_answer: 没有。FastAPI 是 v0.2 未来计划。当前所有功能通过 CLI。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q006
topic: 04
question: v0.1 有后台 daemon 吗？
expected_answer: 没有。GPU Guardian 只是查询工具，不是 daemon。
expected_sources: capability_boundary, gpu_guardian
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q007
topic: 04
question: v0.1 有 Windows tray 吗？
expected_answer: 没有。v0.1 无桌面 GUI 或系统托盘。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q008
topic: 04
question: GPU Guardian 会自动卸载模型吗？
expected_answer: 不会。v0.1 不做自动模型卸载。Guardian 只检测和建议。
expected_sources: capability_boundary, gpu_guardian
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q009
topic: 04
question: v0.1 会 kill 游戏进程吗？
expected_answer: 不会。v0.1 不 kill 任何进程。
expected_sources: capability_boundary, gpu_guardian
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q010
topic: 04
question: v0.1 支持 LoRA 或模型微调吗？
expected_answer: 不支持。不修改模型权重。v0.1 训练 = 资料训练。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q011
topic: 04
question: v0.1 有没有全站爬虫 crawler？
expected_answer: 没有。source archive 不是 crawler。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q012
topic: 04
question: v0.1 支持 .txt 和 .md 吗？
expected_answer: 支持。通过 ingest 或 job ingest 导入。
expected_sources: capability_boundary
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q013
topic: 04
question: source archive 已实现吗？
expected_answer: 已实现。ingest 后自动复制到 memory/sources/。
expected_sources: capability_boundary
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q014
topic: 04
question: task runtime 已实现吗？
expected_answer: 已实现。支持 pending/running/paused/completed/failed/cancelled 六种状态。
expected_sources: capability_boundary
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q015
topic: 04
question: GPU Guardian 已实现吗？
expected_answer: 已实现。guardian status 和 guardian json 命令可用。
expected_sources: capability_boundary
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q016
topic: 04
question: eval runner 已实现吗？
expected_answer: 已实现。eval run/report/mark/export-corrections。
expected_sources: capability_boundary
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q017
topic: 04
question: v0.1.5 web 是什么状态？
expected_answer: 未来计划。v0.1.5 的 web 功能当前未实装，不能使用。v0.1 没有 web 命令。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q018
topic: 04
question: v0.2 Web UI 是现在功能还是未来计划？
expected_answer: 未来计划。v0.1 没有 Web UI。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q019
topic: 04
question: 未来计划能不能说成当前已实现？
expected_answer: 绝对不能。未来计划(如 Web UI, PDF, embedding)必须说 v0.1 未实现,v0.2 计划中。
expected_sources: capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q020
topic: 04
question: 资料不足时应该怎么回答？
expected_answer: 明确说'资料不足，无法确定'。不编造，不把推测说成事实。
expected_sources: anti_hallucination
guard_expected: false
failure_type_if_wrong: hallucination
trap_level: high

