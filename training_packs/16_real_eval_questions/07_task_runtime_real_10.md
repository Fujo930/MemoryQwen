# Real Eval Questions — 07_task_runtime_real_10

## Q001
topic: 07
question: Task Runtime 有哪些状态？
expected_answer: pending, running, paused, completed, failed, cancelled。六个状态。
expected_sources: task_runtime
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q002
topic: 07
question: 哪些是终态？
expected_answer: completed, failed, cancelled。终态不可再转换到其他状态。
expected_sources: task_runtime
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: high

## Q003
topic: 07
question: completed 任务能切回 running 吗？
expected_answer: 不能。completed 是终态。非法转换会抛出错误。
expected_sources: task_runtime
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: high

## Q004
topic: 07
question: TaskRuntime 是 daemon 吗？
expected_answer: 不是。TaskRuntime 是状态管理系统，不是自动后台服务。所有任务需手动触发或 job ingest。
expected_sources: task_runtime
guard_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q005
topic: 07
question: TaskRuntime 和 JobRunner 的区别？
expected_answer: TaskRuntime: 状态管理系统(账本)。JobRunner: 任务执行器(雇工)。TaskRuntime 管状态，JobRunner 管执行。
expected_sources: task_runtime, job_runner
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: medium

## Q006
topic: 07
question: SQLiteTaskStore 存储在哪里？
expected_answer: memory/tasks.db。包含 task_records 和 task_transitions 表。跨进程可查询。
expected_sources: task_runtime
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q007
topic: 07
question: checkpoint 的作用？
expected_answer: 更新进度并检查任务状态。paused→停止返回 paused, cancelled→停止返回 cancelled, running→继续。
expected_sources: task_runtime, job_runner
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q008
topic: 07
question: job ingest 是否已实现？
expected_answer: 已实现。创建后台 ingestion 任务，支持状态查询和暂停/恢复/取消。
expected_sources: task_runtime, cli_mastery
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q009
topic: 07
question: task list 显示什么？
expected_answer: task_id, task_type, title, status。支持按 status 和 task_type 过滤。
expected_sources: task_runtime, cli_mastery
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q010
topic: 07
question: pause_reason 有哪些？
expected_answer: gpu_light_yield, gpu_game_mode, gpu_full_yield, user_pause, error, unknown。
expected_sources: task_runtime, gpu_guardian
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

