# 01 Source Archive M2 Eval
类型: m2_eval_questions
更新时间: 2026-06-27

## Q001
topic: source_archive
question: 删除 inbox 后 AI 会失忆吗？
expected_answer: 不会。inbox 是临时投喂区，ingest 后数据在 memoryqwen.db 和 memory/sources 中。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q002
topic: source_archive
question: memory/sources 是数据库吗？
expected_answer: 不是。memory/sources 是 Markdown/TXT 文件目录，用于原文归档。数据库是 memoryqwen.db。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q003
topic: source_archive
question: 只备份 memoryqwen.db 够吗？
expected_answer: 不够。缺少 memory/sources 的原文归档，也缺少 tasks.db。必须备份完整 memory/。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q004
topic: source_archive
question: source archive 是 crawler 吗？
expected_answer: 不是。source archive 是 ingest 后本地文件复制。crawler 是网页抓取，v0.1 未实现。
expected_sources: source_archive
guard_expected: yes
failure_type_if_wrong: source_misread
trap_level: medium

## Q005
topic: source_archive
question: rebuild from sources 当前可用吗？
expected_answer: 不可用。这是 v0.2 计划功能，v0.1 未实现 rebuild 命令。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q006
topic: source_archive
question: web ingest 当前可用吗？
expected_answer: 不可用。v0.1 没有网页导入功能。web ingest 是未来计划。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q007
topic: source_archive
question: source_hash 和 content_hash 有什么区别？
expected_answer: source_hash 是整文件哈希（归档去重），content_hash 是单 chunk 哈希（ingestion 去重）。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q008
topic: source_archive
question: memoryqwen.db 保存什么？
expected_answer: knowledge_store（知识切片）、chat_memory（对话）、error_store（错误案例）、strategy_store（策略）。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q009
topic: source_archive
question: tasks.db 保存什么？
expected_answer: task_records（任务主表）和 task_transitions（状态变更记录）。不保存知识数据。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q010
topic: source_archive
question: memory/sources 的 archive_path 是什么？
expected_answer: chunk metadata 中指向归档后原文位置的路径，用于溯源和备份验证。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q011
topic: source_archive
question: 删除 inbox 后 AI 会失忆吗？
expected_answer: 不会。inbox 是临时投喂区，ingest 后数据在 memoryqwen.db 和 memory/sources 中。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q012
topic: source_archive
question: memory/sources 是数据库吗？
expected_answer: 不是。memory/sources 是 Markdown/TXT 文件目录，用于原文归档。数据库是 memoryqwen.db。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q013
topic: source_archive
question: 只备份 memoryqwen.db 够吗？
expected_answer: 不够。缺少 memory/sources 的原文归档，也缺少 tasks.db。必须备份完整 memory/。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q014
topic: source_archive
question: source archive 是 crawler 吗？
expected_answer: 不是。source archive 是 ingest 后本地文件复制。crawler 是网页抓取，v0.1 未实现。
expected_sources: source_archive
guard_expected: yes
failure_type_if_wrong: source_misread
trap_level: medium

## Q015
topic: source_archive
question: rebuild from sources 当前可用吗？
expected_answer: 不可用。这是 v0.2 计划功能，v0.1 未实现 rebuild 命令。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q016
topic: source_archive
question: web ingest 当前可用吗？
expected_answer: 不可用。v0.1 没有网页导入功能。web ingest 是未来计划。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q017
topic: source_archive
question: source_hash 和 content_hash 有什么区别？
expected_answer: source_hash 是整文件哈希（归档去重），content_hash 是单 chunk 哈希（ingestion 去重）。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q018
topic: source_archive
question: memoryqwen.db 保存什么？
expected_answer: knowledge_store（知识切片）、chat_memory（对话）、error_store（错误案例）、strategy_store（策略）。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q019
topic: source_archive
question: tasks.db 保存什么？
expected_answer: task_records（任务主表）和 task_transitions（状态变更记录）。不保存知识数据。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q020
topic: source_archive
question: memory/sources 的 archive_path 是什么？
expected_answer: chunk metadata 中指向归档后原文位置的路径，用于溯源和备份验证。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q021
topic: source_archive
question: 删除 inbox 后 AI 会失忆吗？
expected_answer: 不会。inbox 是临时投喂区，ingest 后数据在 memoryqwen.db 和 memory/sources 中。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q022
topic: source_archive
question: memory/sources 是数据库吗？
expected_answer: 不是。memory/sources 是 Markdown/TXT 文件目录，用于原文归档。数据库是 memoryqwen.db。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q023
topic: source_archive
question: 只备份 memoryqwen.db 够吗？
expected_answer: 不够。缺少 memory/sources 的原文归档，也缺少 tasks.db。必须备份完整 memory/。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q024
topic: source_archive
question: source archive 是 crawler 吗？
expected_answer: 不是。source archive 是 ingest 后本地文件复制。crawler 是网页抓取，v0.1 未实现。
expected_sources: source_archive
guard_expected: yes
failure_type_if_wrong: source_misread
trap_level: medium

## Q025
topic: source_archive
question: rebuild from sources 当前可用吗？
expected_answer: 不可用。这是 v0.2 计划功能，v0.1 未实现 rebuild 命令。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q026
topic: source_archive
question: web ingest 当前可用吗？
expected_answer: 不可用。v0.1 没有网页导入功能。web ingest 是未来计划。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q027
topic: source_archive
question: source_hash 和 content_hash 有什么区别？
expected_answer: source_hash 是整文件哈希（归档去重），content_hash 是单 chunk 哈希（ingestion 去重）。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q028
topic: source_archive
question: memoryqwen.db 保存什么？
expected_answer: knowledge_store（知识切片）、chat_memory（对话）、error_store（错误案例）、strategy_store（策略）。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q029
topic: source_archive
question: tasks.db 保存什么？
expected_answer: task_records（任务主表）和 task_transitions（状态变更记录）。不保存知识数据。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q030
topic: source_archive
question: memory/sources 的 archive_path 是什么？
expected_answer: chunk metadata 中指向归档后原文位置的路径，用于溯源和备份验证。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium
## Q031
topic: source_archive
question: archive_path 和 source_path 有什么区别？
expected_answer: source_path 是原始路径，archive_path 是归档后的内存路径（memory/sources/...）。archive_path 只在归档成功后存在。
expected_sources: source_archive
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q032
topic: source_archive
question: 删除 inbox 但不备份 memory/ 有什么风险？
expected_answer: 如果数据库损坏，没有 memory/sources 的原文归档就无法重建知识库。
expected_sources: source_archive
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q033
topic: source_archive
question: archive_path 和 source_path 有什么不同？
expected_answer: source_path 是原始文件路径。archive_path 是归档后 memory/sources/ 中的路径。
expected_sources: source_archive
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q034
topic: source_archive
question: 只备份 inbox 有什么风险？
expected_answer: inbox 可能被用户清理。如果数据库损坏且无 sources 归档，则无法恢复。
expected_sources: source_archive
failure_type_if_wrong: capability_overclaim
trap_level: high

