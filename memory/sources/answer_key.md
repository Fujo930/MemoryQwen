# 04_error_strategy Answer Key

- error_store 定位与用途: error_store 存储用户纠正的错误案例。每条记录包含 wrong_answer(反例) 和 correct_answer(正确回答)。error_store 是反例库，不是事实资料库。
- wrong_answer 是反例不是事实: wrong_answer 是错误示例，绝对不能当事实使用。模型如果复述 wrong_answer，说明它把反例当成了权威信息。
- correct_answer 是修正蓝本: correct_answer 是用户提供的正确回答。模型在遇到相似问题时应该参考 correct_answer 的内容。
- failure_type 分类体系: 常用类型：source_miss, source_misread, hallucination, wrong_memory_type, reasoning_error, citation_error, small_model_confusi
- strategy_store 定位与用途: strategy_store 存储可复用的回答策略。strategy_hash 去重。遇到相似问题时 prompt 注入策略指导。
- 策略生成规则: 从 error_store 自动生成。同 strategy_hash 合并。用户提供策略标记 source=user，自动生成标记 source=auto。
- 策略检索与注入: Chat 时检索 strategy_store。如果 BM25 未命中，使用 recent fallback。策略在 prompt 中显示为[T1][T2]。
- 纠错复测流程: 1.执行correct命令 2.检查strategy_store 3.用相似问题重新chat 4.验证error/strategy注入 5.确认不再重复错误。
- 常见错题与策略案例: 案例1：PDF幻觉→correct写入hallucination。案例2：daemon混淆→correct写入capability_overclaim。案例3：缺少sources→correct写入citation_error。