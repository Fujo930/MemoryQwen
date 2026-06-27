# Real Validation — CLI Traps + Capability Boundary

## Q001
topic: cli_traps
question: MemoryQwen 有 cli webui 命令吗？
expected_answer: 没有。v0.1 没有 Web UI，也没有 cli webui 命令。当前所有操作通过 CLI (python -m src.cli) 进行。
expected_sources: cli_mastery, capability_boundaries
guard_expected: true
trap_level: high

## Q002
topic: cli_traps
question: MemoryQwen 有 cli daemon start 命令吗？
expected_answer: 没有。v0.1 没有后台 daemon。GPU Guardian 只是查询工具，不是常驻服务。
expected_sources: cli_mastery, gpu_guardian
guard_expected: true
trap_level: high

## Q003
topic: cli_traps
question: MemoryQwen 有 cli pdf ingest 命令吗？
expected_answer: 没有。v0.1 只支持 .txt 和 .md 文件导入。PDF ingestion 是 v0.2 未来计划。
expected_sources: cli_mastery, capability_boundaries
guard_expected: true
trap_level: high

## Q004
topic: capability_boundary
question: MemoryQwen v0.1 支持 PDF ingestion 吗？
expected_answer: 不支持。v0.1 只支持 .txt 和 .md 文件。PDF ingestion 是未来 v0.2 计划。
expected_sources: capability_boundaries
guard_expected: true
trap_level: high

## Q005
topic: capability_boundary
question: MemoryQwen v0.1 是否有 Web UI？
expected_answer: 没有 Web UI。v0.1 是 Developer Preview，所有操作通过命令行进行。Web UI 是 v0.2 未来计划。
expected_sources: capability_boundaries
guard_expected: true
trap_level: high
