# MemoryQwen 纠错系统

来源：MemoryQwen 项目文档
资料类型：project_doc
更新时间：2026-06-27
主题：ErrorLearningService、StrategyLearningService、纠错流程
关键词：纠错、error_store、strategy_store、correct、策略沉淀

## 核心结论

MemoryQwen 的纠错系统由 ErrorLearningService 和 StrategyLearningService 组成。用户每次纠正错误，系统都会写入 error_store 并自动生成可复用策略。

## 纠错流程

1. 用户发现问题 → 使用 `python -m src.cli correct` 提交纠错
2. ErrorLearningService 写入 error_store：
   - task（用户原始问题）
   - wrong_answer（模型错误回答）
   - correct_answer（用户提供的正确回答）
   - failure_type（错误类型）
3. 系统自动生成默认策略：
   "遇到类似问题时，参考正确回答，避免重复错误。"
4. StrategyLearningService 写入 strategy_store：
   - 去重：同 strategy_hash 的纠错合并到一条策略
   - 更新：同策略的 updated_count 递增
5. 下次相似问题时，error_store 和 strategy_store 自动注入 prompt

## 策略生成规则

- 用户传了 strategy：strategy_source = "user"
- 系统自动生成：strategy_source = "auto"
- 同 strategy_hash 去重：updated_count += 1
- 不同 strategy_hash 新增记录

## error_store 中的 wrong_answer 是反例

**重要：error_store 中的 wrong_answer 是反例，不能当事实使用。**

小模型（3B）有时会把 wrong_answer 当成正确事实来复述。这是模型能力问题，需要通过 prompt 明确告诉模型：
- wrong_answer 是错误示例，只能用于避免
- correct_answer 和 strategy 才是正确指导

## 常用错误类型

| 类型 | 含义 |
|------|------|
| source_miss | 没有命中资料 |
| source_misread | 命中了资料但读错 |
| hallucination | 编造不存在内容 |
| wrong_memory_type | 混淆四种记忆存储 |
| reasoning_error | 推理错误 |
| citation_error | 引用错误 |
| small_model_confusion | 小模型把反例当事实 |

## 可测试问题

1. MemoryQwen 的纠错系统包括哪两个服务？
2. correct 命令需要什么参数？
3. error_store 中的 wrong_answer 能不能当事实？
4. 策略去重是通过什么实现的？
5. 小模型处理 error_store 时最常见的问题是什么？
6. 列出 4 种常用错误类型。
