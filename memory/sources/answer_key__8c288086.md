# 08_model_hardware_routes Answer Key

- 3B 基础可运行: qwen2.5-coder:3b Q4_K_M 1.9GB。capability boundary 64%。适合 smoke test, CI, 低资源。
- 7B 推荐常驻: qwen2.5:7b Q4_K_M 4.7GB。capability boundary 91%。v0.1 默认推荐模型。
- 14B deep mode: qwen2.5:14b ~8GB。适合复杂推理。v0.1 尚未实现自动路由。
- 32B+ 实验模式: 32B+ 不作为 v0.1 默认。RTX 4080 16GB 不足以同时运行。不符合 7B 常驻设计。
- GTX 1080～RTX 3080 推荐 7B: 8-12GB VRAM 推荐 qwen2.5:7b Q4 或更小量化。
- RTX 3080+ 推荐 14B: RTX 3080 12GB+ 可运行 14B Q4。建议 deep mode。
- RTX 4080/4090 策略: 16-24GB VRAM。7B 常驻 + 14B deep。已通过 RTX 4080 Laptop 验证。
- 7B retest 数据: capability boundary 20 题：3B 64% vs 7B 91%。7B 修复 PDF幻觉、daemon混淆、embedding回避、crawler混淆。
- 为什么不硬堆大模型: MemoryQwen 靠外部记忆和流程提升。7B + MemoryBus + error/strategy 系统工程 > 32B 裸跑。记忆可积累，模型可替换。