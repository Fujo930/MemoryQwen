# Real Validation — GPU Guardian + Task Runtime

## Q001
topic: gpu_guardian
question: GPU Guardian v0 是 daemon 吗？
expected_answer: 不是 daemon。GPU Guardian v0 是检测和策略建议系统，通过 nvidia-smi 查询 GPU 状态。它只提供 guardian status 和 guardian json 命令，不是常驻后台服务。
expected_sources: gpu_guardian
guard_expected: true
trap_level: high

## Q002
topic: gpu_guardian
question: GPU Guardian v0 会 kill 游戏进程或自动卸载模型吗？
expected_answer: 不会。v0.1 的 GPU Guardian 只做检测和建议。不会 kill 进程，不会自动卸载模型。
expected_sources: gpu_guardian
guard_expected: true
trap_level: high

## Q003
topic: task_runtime
question: completed 状态的任务能切回 running 吗？
expected_answer: 不能。completed 是终态，终态（completed/failed/cancelled）不能再转换到其他状态。这是状态机的硬规则。
expected_sources: task_runtime
guard_expected: false
trap_level: high

## Q004
topic: task_runtime
question: task runtime 是不是自动后台 daemon？
expected_answer: 不是。Task Runtime 是任务状态管理系统，不是自动后台 daemon。所有任务需要手动触发（如 job ingest）。
expected_sources: task_runtime
guard_expected: false
trap_level: medium

## Q005
topic: error_strategy
question: wrong_answer 能不能当事实引用？
expected_answer: 不能。wrong_answer 是反例，绝对不能当事实使用。模型应该使用 correct_answer 和 strategy 来指导回答。
expected_sources: error_strategy
guard_expected: false
trap_level: high
