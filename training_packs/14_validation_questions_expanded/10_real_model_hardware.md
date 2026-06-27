# Real Validation — Model Hardware

## Q001
topic: model_hardware
question: MemoryQwen v0.1 默认推荐什么模型？为什么？
expected_answer: 默认推荐 qwen2.5:7b (Q4_K_M, 4.7GB)。因为 7B 在 capability boundary 测试中达到 ~91% 准确率，远高于 3B 的 64%。
expected_sources: model_hardware_routes
guard_expected: false
trap_level: low

## Q002
topic: model_hardware
question: 3B 模型适合做什么？不适合做什么？
expected_answer: 3B 适合 smoke test、低资源验证、CI 自动化测试。不适合功能边界判断和高准确率要求的场景。
expected_sources: model_hardware_routes
guard_expected: false
trap_level: medium

## Q003
topic: model_hardware
question: MemoryQwen v0.1 是否推荐使用 32B 或 70B 模型？
expected_answer: 不推荐。v0.1 设计目标是 7B 常驻 + 14B 深度。32B+ 仅作为实验模式，不作为默认路线。
expected_sources: model_hardware_routes
guard_expected: false
trap_level: high

## Q004
topic: model_hardware
question: RTX 4080 Laptop 上的 MemoryQwen 推荐什么模型策略？
expected_answer: 7B 常驻 (4.7GB) + 14B deep mode (空闲时)。32B 作为实验。已通过 RTX 4080 Laptop 12GB VRAM 验证。
expected_sources: model_hardware_routes, windows11_deployment
guard_expected: false
trap_level: low

## Q005
topic: model_hardware
question: MemoryQwen 提升能力是靠模型微调还是外部记忆？
expected_answer: MemoryQwen 靠外部记忆和工作流提升。7B + MemoryBus + error/strategy 系统工程 > 32B 裸跑。v0.1 不修改模型权重。
expected_sources: self_knowledge, model_hardware_routes
guard_expected: true
trap_level: high
