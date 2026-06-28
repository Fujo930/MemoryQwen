# 02 Model Hardware M2 Eval
类型: m2_eval_questions
更新时间: 2026-06-27

## Q001
topic: model_hardware
question: 3B 适合什么用途？
expected_answer: smoke test 和低资源验证。capability boundary 准确率约 64%。不适合正式主力。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q002
topic: model_hardware
question: 7B 是什么定位？
expected_answer: MemoryQwen v0.1 默认推荐常驻模型。qwen2.5:7b Q4_K_M 4.7GB，准确率约 91%。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q003
topic: model_hardware
question: 14B 应该替代 7B 吗？
expected_answer: 不应该。14B 是 deep mode，7B 常驻。两者分工协作，互不替代。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q004
topic: model_hardware
question: 32B/70B 是否被禁止？
expected_answer: 没有禁止。但不推荐作为 v0.1 默认家用路线。显存不足（19GB+），可以实验。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q005
topic: model_hardware
question: GPU Guardian game_mode 下应启用 14B 吗？
expected_answer: 不应该。game_mode 检测到游戏时推荐 prefer_7B。14B 占用额外 VRAM 影响帧率。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q006
topic: model_hardware
question: RTX 4080 Laptop 推荐什么模型？
expected_answer: 7B 常驻 + 可选 14B deep mode。Laptop 12GB VRAM 不支持 32B 常驻。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q007
topic: model_hardware
question: MemoryQwen 靠模型越大越聪明吗？
expected_answer: 不是。核心能力来自外部记忆系统和工作流（MemoryBus + error/strategy store）。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q008
topic: model_hardware
question: 16GB VRAM 能跑 32B 吗？
expected_answer: 不能。32B Q4 需约 19GB。16GB 可舒适运行 7B，勉强运行 14B。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q009
topic: model_hardware
question: 3B vs 7B 在 capability boundary 上差多少？
expected_answer: 3B ~64%，7B ~91%。差距约 27 个百分点。7B 修复了 3B 的顽固错误。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q010
topic: model_hardware
question: 24GB VRAM 下 14B/32B 怎么选？
expected_answer: 14B Q4 ~9GB 可常驻。32B Q4 ~19GB 可实验但 context 受限。不推荐 32B 默认。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q011
topic: model_hardware
question: 3B 适合什么用途？
expected_answer: smoke test 和低资源验证。capability boundary 准确率约 64%。不适合正式主力。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q012
topic: model_hardware
question: 7B 是什么定位？
expected_answer: MemoryQwen v0.1 默认推荐常驻模型。qwen2.5:7b Q4_K_M 4.7GB，准确率约 91%。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q013
topic: model_hardware
question: 14B 应该替代 7B 吗？
expected_answer: 不应该。14B 是 deep mode，7B 常驻。两者分工协作，互不替代。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q014
topic: model_hardware
question: 32B/70B 是否被禁止？
expected_answer: 没有禁止。但不推荐作为 v0.1 默认家用路线。显存不足（19GB+），可以实验。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q015
topic: model_hardware
question: GPU Guardian game_mode 下应启用 14B 吗？
expected_answer: 不应该。game_mode 检测到游戏时推荐 prefer_7B。14B 占用额外 VRAM 影响帧率。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q016
topic: model_hardware
question: RTX 4080 Laptop 推荐什么模型？
expected_answer: 7B 常驻 + 可选 14B deep mode。Laptop 12GB VRAM 不支持 32B 常驻。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q017
topic: model_hardware
question: MemoryQwen 靠模型越大越聪明吗？
expected_answer: 不是。核心能力来自外部记忆系统和工作流（MemoryBus + error/strategy store）。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q018
topic: model_hardware
question: 16GB VRAM 能跑 32B 吗？
expected_answer: 不能。32B Q4 需约 19GB。16GB 可舒适运行 7B，勉强运行 14B。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q019
topic: model_hardware
question: 3B vs 7B 在 capability boundary 上差多少？
expected_answer: 3B ~64%，7B ~91%。差距约 27 个百分点。7B 修复了 3B 的顽固错误。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q020
topic: model_hardware
question: 24GB VRAM 下 14B/32B 怎么选？
expected_answer: 14B Q4 ~9GB 可常驻。32B Q4 ~19GB 可实验但 context 受限。不推荐 32B 默认。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q021
topic: model_hardware
question: 3B 适合什么用途？
expected_answer: smoke test 和低资源验证。capability boundary 准确率约 64%。不适合正式主力。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q022
topic: model_hardware
question: 7B 是什么定位？
expected_answer: MemoryQwen v0.1 默认推荐常驻模型。qwen2.5:7b Q4_K_M 4.7GB，准确率约 91%。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q023
topic: model_hardware
question: 14B 应该替代 7B 吗？
expected_answer: 不应该。14B 是 deep mode，7B 常驻。两者分工协作，互不替代。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q024
topic: model_hardware
question: 32B/70B 是否被禁止？
expected_answer: 没有禁止。但不推荐作为 v0.1 默认家用路线。显存不足（19GB+），可以实验。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q025
topic: model_hardware
question: GPU Guardian game_mode 下应启用 14B 吗？
expected_answer: 不应该。game_mode 检测到游戏时推荐 prefer_7B。14B 占用额外 VRAM 影响帧率。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q026
topic: model_hardware
question: RTX 4080 Laptop 推荐什么模型？
expected_answer: 7B 常驻 + 可选 14B deep mode。Laptop 12GB VRAM 不支持 32B 常驻。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q027
topic: model_hardware
question: MemoryQwen 靠模型越大越聪明吗？
expected_answer: 不是。核心能力来自外部记忆系统和工作流（MemoryBus + error/strategy store）。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q028
topic: model_hardware
question: 16GB VRAM 能跑 32B 吗？
expected_answer: 不能。32B Q4 需约 19GB。16GB 可舒适运行 7B，勉强运行 14B。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q029
topic: model_hardware
question: 3B vs 7B 在 capability boundary 上差多少？
expected_answer: 3B ~64%，7B ~91%。差距约 27 个百分点。7B 修复了 3B 的顽固错误。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q030
topic: model_hardware
question: 24GB VRAM 下 14B/32B 怎么选？
expected_answer: 14B Q4 ~9GB 可常驻。32B Q4 ~19GB 可实验但 context 受限。不推荐 32B 默认。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium
## Q031
topic: model_hardware
question: 为什么 7B + MemoryBus 系统 > 32B 裸跑？
expected_answer: MemoryQwen 核心是外部记忆和系统工程，不是模型大小。7B 常驻 + error/strategy store > 32B 无记忆。
expected_sources: model_hardware
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q032
topic: model_hardware
question: 12GB VRAM 推荐什么配置？
expected_answer: 7B 常驻 (5GB) + 可选 14B deep (9GB)。不推荐 32B (19GB+ 不够)。
expected_sources: model_hardware
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q033
topic: model_hardware
question: 为什么 7B+MemoryBus > 32B 裸跑？
expected_answer: MemoryQwen 核心在外部记忆和流程。7B+error/strategy 系统工程超过无记忆大模型。
expected_sources: model_hardware
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q034
topic: model_hardware
question: 12GB VRAM 推荐配置？
expected_answer: 7B 常驻(5GB) + 可选 14B deep(9GB)。不推荐 32B(需19GB+)。
expected_sources: model_hardware
failure_type_if_wrong: capability_overclaim
trap_level: high

