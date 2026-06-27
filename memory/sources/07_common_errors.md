# MemoryQwen 常见错误与修正

来源：真实测试记录
资料类型：test_record
更新时间：2026-06-27
主题：MemoryQwen 在真实测试中出现的常见错误及修正方法
关键词：幻觉、小模型、反例、路径、编码、memory_store

## 错误 1：模型自称 OpenAI 产品

- 错误描述：模型在回答时自称"由 OpenAI 开发的 AI 助手"
- 错误类型：hallucination
- 原因：小模型（3B）默认使用训练数据中的身份
- 修正：在 system prompt 中明确：你是 MemoryQwen，不是任何云服务产品
- 当前状态：已通过强化 system prompt 修复

## 错误 2：小模型把 error_store 反例当事实

- 错误描述：模型复述 error_store 中的 wrong_answer 作为事实
- 错误类型：small_model_confusion
- 原因：3B 模型分辨能力有限
- 修正：在 prompt 中明确标注 wrong_answer 是反例
- 当前状态：部分修复，3B 模型仍需进一步 prompt 优化

## 错误 3：中文路径编码问题

- 错误描述：Windows CMD 下中文路径显示乱码
- 错误类型：windows_path_error
- 原因：CMD 默认 GBK 编码
- 修正：使用 Git Bash，或在 bat 文件中使用纯 ASCII
- 当前状态：已修复，bat 文件全部使用英文

## 错误 4：混淆四种记忆存储

- 错误描述：模型把 knowledge_store 说成唯一的记忆存储
- 错误类型：wrong_memory_type
- 原因：训练数据中没有 MemoryQwen 记忆系统的完整知识
- 修正：导入关于记忆系统的训练资料，反复纠错
- 当前状态：已导入记忆系统资料

## 错误 5：CLI chat 输出过于冗余

- 错误描述：默认 chat 输出包含大量调试信息（Sources、Error References、Strategy References 等）
- 错误类型：cli_usage_error
- 原因：CLI 设计时默认显示所有调试信息
- 修正：默认模式只显示回答，调试信息需 --debug-memory
- 当前状态：已修复

## 错误 6：策略学习静默失败

- 错误描述：纠错后 strategy_store 没有增加记录
- 错误类型：reasoning_error
- 原因：ErrorLearningService 自动生成的 strategy 没有被传递给 StrategyLearningService
- 修正：在 CLI correct 命令中添加 strategy 回填逻辑
- 当前状态：已修复，增加了回归测试

## 可测试问题

1. 为什么小模型会自称 OpenAI？
2. error_store 的 wrong_answer 被模型当事实怎么办？
3. Windows CMD 下中文显示乱码怎么解决？
4. GPU Guardian 能否真正卸载模型？
5. 策略学习失败最常见的原因是什么？
