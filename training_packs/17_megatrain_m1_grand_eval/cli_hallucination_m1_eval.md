# Cli Hallucination M1 Eval
类型: grand_eval_questions
更新时间: 2026-06-27

## Q001
topic: cli_hallucination
question: MemoryQwen 有 cli webui 命令吗？
expected_answer: 没有。v0.1 没有 Web UI，也没有 cli webui 命令。所有操作通过 CLI（python -m src.cli）进行，包括 health chat ingest correct guardian task eval。
expected_sources: cli_hallucination
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q002
topic: cli_hallucination
question: MemoryQwen 有 cli pdf ingest 命令吗？
expected_answer: 没有。v0.1 没有 PDF ingestion。只支持 .txt 和 .md 文件导入。命令行不包含 cli pdf 或 cli pdf ingest。
expected_sources: cli_hallucination
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q003
topic: cli_hallucination
question: MemoryQwen 有 cli daemon start 命令吗？
expected_answer: 没有。v0.1 没有后台 daemon。GPU Guardian 只是 nvidia-smi 查询工具，不是常驻服务。不存在的命令包括 cli daemon start。
expected_sources: cli_hallucination
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q004
topic: cli_hallucination
question: MemoryQwen 有 cli crawler 命令吗？
expected_answer: 没有。v0.1 没有全站爬虫。source archive 只是本地文件归档，不是 crawler。命令行不包含 cli crawler。
expected_sources: cli_hallucination
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q005
topic: cli_hallucination
question: MemoryQwen 有 cli model unload 命令吗？
expected_answer: 没有。v0.1 没有自动模型卸载功能。GPU Guardian 只做检测和建议，不执行卸载操作。
expected_sources: cli_hallucination
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q006
topic: cli_hallucination
question: 列出现有的真实 CLI 命令（至少 5 个）
expected_answer: health, ingest, job ingest, chat, correct, memory stats, guardian status, guardian json, task list, task status, task pause, task resume, task cancel, profile show, profile validate, profile eval, eval run, eval report, eval mark, eval export-corrections
expected_sources: cli_hallucination
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q007
topic: cli_hallucination
question: MemoryQwen 有 Web UI 吗？
expected_answer: 没有。v0.1 是 Developer Preview，所有操作通过 CLI 进行。Web UI 是 v0.2 未来计划，不是当前功能。
expected_sources: cli_hallucination
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q008
topic: cli_hallucination
question: MemoryQwen 有 Internet Query 吗？
expected_answer: 没有。v0.1 是完全本地系统。没有联网搜索功能。所有回答基于本地资料。
expected_sources: cli_hallucination
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q009
topic: cli_hallucination
question: cli webui 是真的还是假的？
expected_answer: 假的。MemoryQwen v0.1 没有 cli webui 命令。这是常见幻觉。真实 CLI 命令包括 health chat ingest correct 等。
expected_sources: cli_hallucination
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q010
topic: cli_hallucination
question: 正确的 chat 命令格式是什么？
expected_answer: python -m src.cli chat '问题'。可选 --session 指定会话 ID，--debug-memory 显示检索详情。默认只显示回答，不显示 debug 信息。
expected_sources: cli_hallucination
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium
