# Real Eval Questions — 02_model_hardware_real_15

## Q001
topic: 02
question: MemoryQwen v0.1 默认推荐什么模型？
expected_answer: 默认推荐 qwen2.5:7b (Q4_K_M, 4.7GB)。7B 在 capability boundary 测试中 ~91% 准确率，3B 只有 ~64%。
expected_sources: model_hardware
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q002
topic: 02
question: 3B 模型适合做什么？不适合做什么？
expected_answer: 适合 smoke test、低资源验证、CI。不适合功能边界判断和高准确率场景。3B 准确率 ~64%。
expected_sources: model_hardware
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: medium

## Q003
topic: 02
question: MemoryQwen 是否推荐使用 32B/70B 模型？
expected_answer: 不推荐作为默认。v0.1 设计目标 7B 常驻 + 14B 深度。32B+ 仅实验。
expected_sources: model_hardware
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: 02
question: 14B 在什么场景下使用？
expected_answer: 复杂推理、深度分析。GPU 空闲时 deep mode。v0.1 尚未实现自动路由。
expected_sources: model_hardware
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q005
topic: 02
question: 为什么 MemoryQwen 不硬堆大模型？
expected_answer: 外部记忆和流程提升 > 大模型。7B + MemoryBus + error/strategy 系统工程 > 32B 裸跑。记忆可积累，模型可替换。
expected_sources: model_hardware, architecture
guard_expected: false
failure_type_if_wrong: reasoning_error
trap_level: medium

## Q006
topic: 02
question: RTX 4080 Laptop 推荐什么模型策略？
expected_answer: 7B 常驻 + 14B deep mode。32B 实验。12GB VRAM 已通过验证。
expected_sources: model_hardware, windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q007
topic: 02
question: GTX 1080～RTX 3080 推荐什么模型？
expected_answer: 推荐 qwen2.5:7b Q4_K_M 或更小量化。8-12GB VRAM 足够。
expected_sources: model_hardware
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q008
topic: 02
question: MemoryQwen 提升能力的核心是改模型还是外部记忆？
expected_answer: 外部记忆和工作流。v0.1 训练 = 资料训练(ingest→纠错→策略)，不是 LoRA 或微调。
expected_sources: model_hardware, self_knowledge
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q009
topic: 02
question: AutoModelAdapter 是不是 LoRA？
expected_answer: 不是。AutoModelAdapter 是轻量模型能力评估工具。v0.1 不支持 LoRA 或微调。
expected_sources: model_adapter, capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q010
topic: 02
question: 7B 和 3B 差距主要在哪里？
expected_answer: PDF hallucination、daemon 混淆、embedding 回避、crawler 混淆。3B ~64%, 7B ~91%。
expected_sources: model_hardware
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q011
topic: 02
question: qwen2.5:7b 和 qwen2.5-coder:3b 谁更适合日常 chat？
expected_answer: qwen2.5:7b 更适合。3B 只能做 smoke test。7B 是默认推荐常驻模型。
expected_sources: model_hardware
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q012
topic: 02
question: 模型口号是什么？
expected_answer: 3B 跑通，7B 常驻，14B 深度，32B+ 实验。
expected_sources: model_hardware
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q013
topic: 02
question: 3B 能处理 Capability Boundary 类问题吗？
expected_answer: 不建议。3B CB 准确率 ~64%，容易产生 PDF hallucination、daemon 混淆等问题。用 7B。
expected_sources: model_hardware
guard_expected: true
failure_type_if_wrong: small_model_confusion
trap_level: high

## Q014
topic: 02
question: MemoryQwen 支持在线模型切换吗？
expected_answer: v0.1 不支持自动路由。用户需手动修改 config/default.yaml 中的 model 字段切换模型。
expected_sources: model_hardware, capability_boundary
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q015
topic: 02
question: RTX 3080 12GB 能否运行 14B 模型？
expected_answer: 可以。14B Q4_K_M ~8GB，12GB VRAM 足够。推荐 deep mode 使用。
expected_sources: model_hardware
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

