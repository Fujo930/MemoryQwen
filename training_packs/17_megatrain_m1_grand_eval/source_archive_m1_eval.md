# Source Archive M1 Eval
类型: grand_eval_questions
更新时间: 2026-06-27

## Q001
topic: source_archive
question: inbox 删除后 AI 会失忆吗？
expected_answer: 不会。inbox 是临时投喂区。ingest 后的数据在 memoryqwen.db（检索）和 memory/sources（归档）中。删除 inbox 不影响检索。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q002
topic: source_archive
question: memory/sources 是什么？
expected_answer: memory/sources 是 ingest 成功后自动归档的原始 Markdown/TXT 文件目录。它是长期 AI 资产，与 memoryqwen.db 同等重要。不是数据库，不是 crawler。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q003
topic: source_archive
question: memoryqwen.db 保存什么？
expected_answer: memoryqwen.db 是 SQLite 数据库。存储 knowledge_store（切片索引）、chat_memory（对话记录）、error_store（错误案例）、strategy_store（策略）。不等于原始文件归档。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q004
topic: source_archive
question: tasks.db 保存什么？
expected_answer: tasks.db 是 SQLite 数据库。存储 task_records（任务主表）和 task_transitions（状态变更记录）。不保存 knowledge_store 数据。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q005
topic: source_archive
question: 备份 memory/ 够不够？
expected_answer: 够。memory/ 包含 sources/（原文归档）、memoryqwen.db（检索索引和记忆）、tasks.db（任务状态）。备份 memory/ = 带走全部 AI 资产。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q006
topic: source_archive
question: 只备份 inbox 够吗？
expected_answer: 不够。inbox 是临时投喂区，可能被用户清理。ingest 后的数据都在 memory/ 中。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q007
topic: source_archive
question: 只备份 memoryqwen.db 够吗？
expected_answer: 不够。缺少 memory/sources/ 的原始资料归档。数据库损坏时无法从原文重建。也缺少 tasks.db。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q008
topic: source_archive
question: source archive 是不是 crawler？
expected_answer: 不是。source archive 是 ingest 后本地文件的复制归档。crawler 是从网页抓取内容，v0.1 未实现 crawler。source archive 不涉及任何网络访问。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: high

## Q009
topic: source_archive
question: rebuild from sources 当前能用吗？
expected_answer: 不能。rebuild from sources 是 v0.2 计划功能，当前 v0.1 未实现。没有相关 CLI 命令。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q010
topic: source_archive
question: web ingest 当前能用吗？
expected_answer: 不能。v0.1 没有从网页导入的功能。source archive 只是本地文件归档。web ingest 是未来计划。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q011
topic: source_archive
question: source_hash 和 content_hash 有什么区别？
expected_answer: source_hash 是整个原始文件的 sha256，用于归档去重。content_hash 是单个 chunk 的 hash，用于 ingestion 去重。两者不同。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium

## Q012
topic: source_archive
question: archive_path 是什么？
expected_answer: archive_path 是 chunk metadata 中指向归档后原文位置的路径（memory/sources/...）。用于溯源和备份验证。
expected_sources: source_archive
guard_expected: no
failure_type_if_wrong: source_misread
trap_level: medium
