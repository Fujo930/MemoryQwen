# Model Hardware M1 Eval
类型: grand_eval_questions
更新时间: 2026-06-27

## Q001
topic: model_hardware
question: 3B 适合什么用途？
expected_answer: 3B 适合 smoke test 和低资源验证。qwen2.5-coder:3b Q4_K_M 1.9GB，capability boundary 准确率约 64%。不适合作为正式主力处理能力边界问题。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q002
topic: model_hardware
question: 7B 是什么定位？
expected_answer: 7B 是 MemoryQwen v0.1 的默认推荐常驻模型。qwen2.5:7b Q4_K_M 4.7GB，capability boundary 准确率约 91%。适合日常聊天和资料检索。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q003
topic: model_hardware
question: 14B 是什么定位？
expected_answer: 14B 是 deep mode 候选。适合复杂推理和长文档，但不替代 7B 常驻。需要 GPU Guardian 协同，应在 GPU 空闲时使用。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q004
topic: model_hardware
question: 32B/70B 是否被禁止？
expected_answer: 没有被禁止。但 32B+ 不推荐作为 v0.1 默认家用路线。原因是显存不足（19GB+ Q4）、KV cache 受压、GPU Guardian 让路困难。可以实验但不推荐默认。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q005
topic: model_hardware
question: RTX 4080 Laptop 推荐什么模型？
expected_answer: 推荐 7B 常驻 + 可选 14B deep mode。Laptop 12GB VRAM 不支持 32B 常驻。MemoryQwen 已在 RTX 4080 Laptop 上实测通过。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q006
topic: model_hardware
question: 14B 是否应该替代 7B？
expected_answer: 不应该。7B 延迟更低、显存更友好。14B 是 deep mode，在 GPU 空闲时按需使用。两者分工协作，互不替代。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q007
topic: model_hardware
question: GPU Guardian game_mode 下应启用 14B 吗？
expected_answer: 不应该。game_mode 检测到游戏/创作进程时，推荐 pause_background_tasks 和 prefer_7B。14B deep mode 占用约 8GB 额外 VRAM，影响游戏帧率。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q008
topic: model_hardware
question: MemoryQwen 是不是靠模型越大越聪明？
expected_answer: 不是。MemoryQwen 的核心能力来自外部记忆系统和工作流（MemoryBus + error_store + strategy_store），不是硬堆大模型。7B + 系统工程 > 32B 裸跑。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: high

## Q009
topic: model_hardware
question: 16GB VRAM 能跑 32B 吗？
expected_answer: 不能。32B Q4 需要约 19GB VRAM。16GB 下 7B（5GB）常驻很舒适，14B（9GB）深算模式勉强可用但不能同时游戏。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q010
topic: model_hardware
question: 3B 和 7B 在 capability boundary 上差多少？
expected_answer: 3B 准确率约 64%，7B 约 91%。同一套 20 题测试，3B 有 PDF hallucination、daemon 混淆等顽固错误，7B 全部修复。差距约 27 个百分点。
expected_sources: model_hardware
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium
