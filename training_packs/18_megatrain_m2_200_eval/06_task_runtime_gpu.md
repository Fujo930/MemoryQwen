# 06 Task Runtime Gpu
type: m2_eval_completion
updated: 2026-06-27

## Q001
topic: task_runtime
question: task runtime 的终态有哪些？
expected_answer: completed、failed、cancelled。这三个状态不能再转换。paused 不是终态。
expected_sources: task_runtime
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q002
topic: gpu_guardian
question: GPU Guardian game_mode 下应暂停哪些任务？
expected_answer: background tasks。应用 pause_background_tasks 动作暂停 ingestion/index_refresh 等。
expected_sources: gpu_guardian
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q003
topic: task_runtime
question: job checkpoint 返回 paused 时 job 应怎么处理？
expected_answer: 停止处理，返回 paused 状态。不应强行继续执行。
expected_sources: task_runtime
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: gpu_guardian
question: GuardianTaskPolicy 根据什么暂停任务？
expected_answer: GuardianState 的 recommended_actions。pause_background_ingestion→暂停ingestion任务。
expected_sources: gpu_guardian
failure_type_if_wrong: capability_overclaim
trap_level: high
