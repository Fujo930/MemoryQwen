# Real Eval Questions — 06_gpu_guardian_real_10

## Q001
topic: 06
question: GPU Guardian v0 有哪四种模式？
expected_answer: normal(正常), light_yield(轻度让路), game_mode(游戏模式), full_yield(完全让路)。
expected_sources: gpu_guardian
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q002
topic: 06
question: GPU Guardian 是 daemon 吗？
expected_answer: 不是。它只提供 guardian status 和 guardian json 命令用于检测 GPU 状态。v0.1 没有后台 daemon。
expected_sources: gpu_guardian
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q003
topic: 06
question: GPU Guardian 会 kill 进程吗？
expected_answer: 不会。v0.1 不 kill 任何进程。Guardian 只检测和建议。
expected_sources: gpu_guardian
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: 06
question: GPU Guardian 会卸载模型吗？
expected_answer: 不会。v0.1 的 GPU Guardian 只做检测和建议，不做自动模型卸载。
expected_sources: gpu_guardian
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q005
topic: 06
question: GPU Guardian 检测什么？
expected_answer: 通过 nvidia-smi 查询：GPU 名称、VRAM、利用率、温度、运行进程。
expected_sources: gpu_guardian
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q006
topic: 06
question: game_mode 什么时候触发？
expected_answer: 检测到游戏/创作进程或 GPU Util >= 70%。推荐暂停后台AI任务，用户优先。
expected_sources: gpu_guardian
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q007
topic: 06
question: full_yield 什么时候触发？
expected_answer: VRAM >= 85%。推荐暂停所有 AI 任务，完全让路。
expected_sources: gpu_guardian
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q008
topic: 06
question: GuardianTaskPolicy 是什么？
expected_answer: 根据 Guardian 推荐动作暂停 Task Runtime 中的对应任务。ingestion→暂停 ingestion, pause_all_ai_tasks→暂停除 error/strategy 外所有任务。
expected_sources: gpu_guardian
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q009
topic: 06
question: nvidia-smi 不可用时 Guardian 返回什么？
expected_answer: Guarding 系统不可用时返回 normal 模式，available=false，不报错。
expected_sources: gpu_guardian
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q010
topic: 06
question: GPU Guardian 和 Task Runtime 如何交互？
expected_answer: Guardian 检测 → 推荐动作 → GuardianTaskPolicy 决定 → TaskRuntimeService.pause_task。
expected_sources: gpu_guardian, task_runtime
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

