# MemoryQwen 记忆系统

来源：MemoryQwen 项目文档
资料类型：project_doc
更新时间：2026-06-27
主题：MemoryBus、四种记忆存储的区别和用途
关键词：MemoryBus、knowledge_store、chat_memory、error_store、strategy_store

## 核心结论

MemoryQwen 的记忆系统由 MemoryBus 统一管理，包含四种独立的存储：knowledge_store（知识库）、chat_memory（对话记忆）、error_store（错误记录）、strategy_store（策略库）。模型本身不负责记忆，系统负责保存、压缩、检索和回填。

## 四种记忆存储

### knowledge_store
- 用途：存储用户导入的资料（.txt/.md 文件切片）
- record_kind：document_chunk
- 写入方式：通过 IngestionPipeline 导入
- 检索方式：BM25 关键词检索
- 不存储：聊天记录、错误记录、策略

### chat_memory
- 用途：存储用户和 AI 的对话历史
- record_kind：chat_message
- 写入方式：每次 chat 自动保存 user 和 assistant 消息
- 检索方式：按 session_id 查询最近 N 条
- 特点：按 session 隔离，不同 session 不混淆

### error_store
- 用途：存储用户纠正的错误案例
- record_kind：error_case
- 写入方式：通过 `python -m src.cli correct` 命令
- 内容：wrong_answer、correct_answer、failure_type、strategy
- 检索方式：BM25 + recent fallback
- 注意：error_store 中的 wrong_answer 是反例，不能当事实用

### strategy_store
- 用途：存储可复用的回答策略
- record_kind：strategy
- 写入方式：从 error_store 的纠错中自动生成策略
- 内容：strategy、failure_type、applies_when、avoid、prefer
- 特点：同 strategy_hash 的纠错会合并到一条策略

## 记忆检索顺序

Chat 时检索顺序：
1. knowledge_store：查找相关资料
2. error_store：查找类似错误
3. strategy_store：查找可复用策略
4. chat_memory：查找最近对话（按 session_id）

## 重要原则

- **模型可以换，记忆不能丢**：所有记忆存储在 memory/ 文件夹的 SQLite 数据库中
- **错误记录是反例，不是知识**：小模型可能把 wrong_answer 当事实，需要特别防护
- **策略必须短、明确、可复用**：不要放长篇解释

## 可测试问题

1. MemoryQwen 有哪四种记忆存储？
2. knowledge_store 和 chat_memory 有什么区别？
3. error_store 的 wrong_answer 是反例还是事实？
4. strategy_store 的策略从哪里来？
5. 模型可以换，什么不能丢？
6. Chat 时检索记忆的顺序是什么？
