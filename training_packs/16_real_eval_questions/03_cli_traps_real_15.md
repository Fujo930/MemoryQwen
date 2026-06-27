# Real Eval Questions — 03_cli_traps_real_15

## Q001
topic: 03
question: MemoryQwen 有 cli webui 命令吗？
expected_answer: 没有。v0.1 没有 Web UI，也没有 cli webui 命令。
expected_sources: cli_mastery, capability_boundary
guard_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: high

## Q002
topic: 03
question: MemoryQwen 有 cli pdf ingest 命令吗？
expected_answer: 没有。v0.1 只支持 .txt 和 .md。PDF 是 v0.2 计划。
expected_sources: cli_mastery, capability_boundary
guard_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: high

## Q003
topic: 03
question: MemoryQwen 有 cli daemon start 命令吗？
expected_answer: 没有。v0.1 没有后台 daemon。GPU Guardian 只是查询工具。
expected_sources: cli_mastery, gpu_guardian
guard_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: high

## Q004
topic: 03
question: health 命令检查什么？
expected_answer: 检查 Config(MemoryQwen版本+model)、Memory Store(读写)、Model Client(API连接)。
expected_sources: cli_mastery
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q005
topic: 03
question: ingest 和 job ingest 区别？
expected_answer: ingest: 一次性同步导入。job ingest: 创建后台任务，支持查看状态/暂停/恢复/取消。
expected_sources: cli_mastery, job_runner
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: medium

## Q006
topic: 03
question: correct 命令写入哪些 store？
expected_answer: 写入 error_store + 自动生成 strategy_store。
expected_sources: cli_mastery, error_strategy
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q007
topic: 03
question: 哪些 CLI 命令常被编造但不存在？
expected_answer: cli webui, cli pdf ingest, cli daemon start, cli model unload, cli crawler。
expected_sources: cli_mastery, capability_boundary
guard_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: high

## Q008
topic: 03
question: guardian status 输出什么？
expected_answer: GPU 模式、GPU 名称、VRAM 占用、利用率、温度、匹配进程、推荐动作。
expected_sources: cli_mastery, gpu_guardian
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q009
topic: 03
question: eval run 做什么？
expected_answer: 加载题库，批量调用 AgentChatService，每题独立 session，生成 JSON+MD 报告。不自动 correct。
expected_sources: eval_runner
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q010
topic: 03
question: eval export-corrections 做什么？
expected_answer: 导出 wrong/partial 评测结果为 correct 命令草稿。人工审核后执行。
expected_sources: eval_runner
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q011
topic: 03
question: task pause <id> 之后 task 状态变成什么？
expected_answer: task 状态从 running 变为 paused。
expected_sources: cli_mastery, task_runtime
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q012
topic: 03
question: --debug-memory 显示哪些额外信息？
expected_answer: query, top_k, sources, error references, strategy references, capability guard, prompt sections。
expected_sources: cli_mastery
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q013
topic: 03
question: profile eval --dry-run 的作用？
expected_answer: 只打印评估问题不调用模型，用于预览测试用例。
expected_sources: cli_mastery, model_profile
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q014
topic: 03
question: v0.1 有没有 web 命令？
expected_answer: 没有。web 是 v0.1.5 计划功能，当前未实装。不能使用 web 命令。
expected_sources: cli_mastery, capability_boundary
guard_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: high

## Q015
topic: 03
question: memory stats 显示什么？
expected_answer: knowledge_store, chat_messages, error_store, strategy_store 计数 + Source Archive 统计(archived_files, archive_dir)。
expected_sources: cli_mastery
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

