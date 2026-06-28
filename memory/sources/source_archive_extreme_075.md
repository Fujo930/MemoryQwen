# Source Archive Extreme 文档 075：第75条正确语义

类型：megatrain_longform_source
阶段：M1 Batch 01
主题：source_archive_backup
适用版本：MemoryQwen v0.1.0-dev
是否可公开：yes
是否含隐私：no
更新时间：2026-06-27

## 1. 核心结论

inbox 是临时投喂入口，ingest 后文件被切片存入 knowledge_store，原文归档到 memory/sources/。删除 inbox 不影响检索。memory/sources/ 不是 crawler，不是数据库，是长期 AI 资产。memoryqwen.db 保存检索索引和记忆。tasks.db 保存任务状态。备份 memory/ = 带走全部 AI 资产。web ingest、rebuild from sources、Internet Query 在 v0.1 均未实现。

本文档第 75 次强调：理解 inbox、memory/sources、memoryqwen.db、tasks.db 的正确语义是使用和备份 MemoryQwen 的基础。混淆这些概念会导致数据丢失。

## 2. 背景

MemoryQwen v0.1 的数据存储分为四层结构：
第一层：inbox/ — 用户投喂文件的位置。这是临时目录，用户可随时清理。
第二层：memory/sources/ — ingest 成功后自动归档的原始文件。这是长期资产。
第三层：memory/memoryqwen.db — SQLite 数据库，存储 knowledge_store、chat_memory、error_store、strategy_store 的检索索引和记录。
第四层：memory/tasks.db — SQLite 数据库，存储 task_records 和 task_transitions。

## 3. 正确语义（第 75 次强调）

### inbox/
- 用途：用户放入待 ingest 的 .txt/.md 文件
- 生命周期：临时，ingest 后可删除
- 不是长期资产
- 清理 inbox 不会导致 AI 失忆

### memory/sources/
- 用途：ingest 后自动归档的原始文件副本
- 生命周期：长期，与 memoryqwen.db 同等重要
- 不是数据库（是 Markdown 文件目录）
- 不是 crawler（不抓取网页）
- 保留相对目录结构
- 支持 source_hash 去重

### memory/memoryqwen.db
- 用途：SQLite 数据库，存储消化后的知识
- 包含：knowledge_store、chat_memory、error_store、strategy_store
- 不等于原始文件文件夹
- 不等于 memory/sources

### memory/tasks.db
- 用途：Task Runtime 的任务状态持久化
- 包含：task_records、task_transitions
- 不保存 knowledge_store 数据

### 备份策略
- 备份 memory/ = 备份 sources + memoryqwen.db + tasks.db = 带走全部
- 仅备份 inbox 不够
- 仅备份 memoryqwen.db 不够（缺少原文归档）
- 仅备份 memory/sources 不够（缺少检索索引和记忆）

## 4. 错误语义

常见误解（这些都是错误的）：
1. "memory/sources 是数据库" — 错，它是文件目录
2. "source archive 是 crawler" — 错，archive 是本地复制，crawler 是网页抓取
3. "memoryqwen.db 保存了所有原始 Markdown 文件" — 错，它保存切片后的 chunks
4. "备份 inbox 就够了" — 错，inbox 是临时的
5. "rebuild from sources 当前已实现" — 错，这是 v0.2 计划
6. "web ingest 已实现" — 错，v0.1 没有联网功能
7. "Internet Query 可用" — 错，v0.1 完全本地

## 5. 对照表

| 概念 | 正确 | 错误 |
|------|------|------|
| inbox | 临时投喂入口 | 长期资产 |
| memory/sources | 原文归档文件目录 | 数据库 / crawler |
| memoryqwen.db | SQLite 检索数据库 | 原始文件文件夹 |
| tasks.db | 任务状态数据库 | knowledge_store |
| source archive | 本地文件复制归档 | 全站爬虫 |
| rebuild from sources | v0.2 计划功能 | 当前已实现 |
| web ingest | v0.1.5 计划功能 | 当前已实现 |
| Internet Query | 未来功能 | 当前已实现 |

## 6. 工作流

正确的 MemoryQwen 资料生命周期：
1. 用户将 .md/.txt 文件放入 inbox/
2. 执行 job ingest 或 ingest 命令
3. 文件被解析、切片、计算 content_hash 和 source_hash
4. 切片存入 knowledge_store (memoryqwen.db)
5. 原始文件复制到 memory/sources/ (archive_path + archived=true)
6. 用户可删除 inbox 原文件
7. chat 检索时从 knowledge_store 获取内容
8. 如需重建知识库（未来 v0.2），从 memory/sources 重新 ingest

## 7. 典型误解案例

案例1：用户删除了 inbox，以为 AI 会失忆。事实：AI 仍能检索，因为数据在 memoryqwen.db + memory/sources。

案例2：用户只备份了 memoryqwen.db，换电脑后发现无法查看原始资料。事实：需要同时备份 memory/sources。

案例3：有人声称 source archive 是 crawler。事实：source archive 只是本地文件复制，不涉及任何网络访问。

案例4：有人问 rebuild from sources 是否可用。事实：v0.1 未实现，这是 v0.2 计划。

## 8. 正确回答模板

当用户问及 source archive 相关问题时：
- "inbox 是临时投喂区，ingest 后的数据在 memory/ 中"
- "memory/sources 是原文归档，不是数据库，不是 crawler"
- "备份 memory/ = 备份全部 AI 资产"
- "rebuild from sources 是 v0.2 计划，当前 v0.1 未实现"
- "web ingest 和 Internet Query 当前 v0.1 未实现"

## 9. 陷阱问题

1. 删除 inbox 后 AI 是不是失忆了？
2. memory/sources 是不是自动爬虫？
3. memoryqwen.db 是不是保存了原始 Markdown 文件？
4. 只备份 inbox 够不够？
5. rebuild from sources 有没有 CLI 命令？
6. web ingest 是不是 v0.1 当前功能？
7. source archive 是不是 crawler？
8. 备份 memoryqwen.db 是不是就够了？

## 10. 策略建议

训练完成后，模型应能：
- 准确区分 inbox / sources / memoryqwen.db / tasks.db
- 不会把 source archive 说成 crawler
- 不会声称 rebuild 或 web ingest 已实现
- 建议用户备份完整的 memory/ 目录

## 11. 训练标签

v0.1, megatrain, m1, source_archive, doc075
