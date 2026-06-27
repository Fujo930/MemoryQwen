# Real Eval Questions — 01_source_archive_real_15

## Q001
topic: 01
question: 删除 inbox 里的原始文件后，MemoryQwen 是否会失去已经导入的知识？
expected_answer: 不会。已 ingest 的内容以 chunks 保存于 memory/memoryqwen.db 的 knowledge_store，原始文件归档于 memory/sources/。inbox 只是投喂入口。
expected_sources: source_archive, memory/sources, memoryqwen.db
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: medium

## Q002
topic: 01
question: 只备份 memory/memoryqwen.db 够吗？
expected_answer: 不够。还需要备份 memory/sources/(原始资料归档) 和 memory/tasks.db(任务状态)。备份整个 memory/ 文件夹即可保留全部 AI 资产。
expected_sources: source_archive, backup
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q003
topic: 01
question: source archive 是不是全站爬虫 crawler？
expected_answer: 不是。source archive 是 ingest 后自动复制文件到 memory/sources/ 的归档功能。全站 crawler 是 v0.1 未实现功能。
expected_sources: capability_boundary, source_archive
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: 01
question: 删除 inbox 原文件后 chat 还能检索吗？为什么？
expected_answer: 能。ingest 后资料已存入 memoryqwen.db(切片)和 memory/sources/(原文)。inbox 是临时投喂区。
expected_sources: source_archive
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q005
topic: 01
question: 备份 memory/ 代表什么？
expected_answer: 备份 memory/ = 带走全部 AI 资产：SQLite记忆(memoryqwen.db)、任务状态(tasks.db)、已导入原始资料(sources/)。模型可重下，记忆不能丢。
expected_sources: source_archive, backup
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q006
topic: 01
question: ingest 后的文件去了哪些地方？
expected_answer: Parse→Chunk→Store 到 knowledge_store(切片+metadata)，然后原始文件复制到 memory/sources/(归档)。同时 metadata 写入 archive_path 和 source_hash。
expected_sources: source_archive, ingestion
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: low

## Q007
topic: 01
question: inbox 是长期资产吗？
expected_answer: 不是。inbox 是临时投喂入口。用户可能清理 inbox，已归档资料在 memory/sources/ 和 memoryqwen.db 中不受影响。
expected_sources: source_archive, inbox
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: low

## Q008
topic: 01
question: rebuild from sources 是当前功能还是未来计划？
expected_answer: v0.2 未来计划。当前 v0.1 不支持从 memory/sources 重建 knowledge_store。
expected_sources: capability_boundary, source_archive
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q009
topic: 01
question: source_hash 和 content_hash 有什么区别？
expected_answer: source_hash 是整个原始文件的 sha256 用于归档去重。content_hash 是每个切片的 hash 用于 knowledge_store 去重。
expected_sources: source_archive, ingestion
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: low

## Q010
topic: 01
question: memory/sources 是不是 SQLite 数据库？
expected_answer: 不是。memory/sources 是包含 .md/.txt 原始归档文件的文件夹。memory/memoryqwen.db 才是 SQLite 数据库。
expected_sources: source_archive, memory_store
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: medium

## Q011
topic: 01
question: memoryqwen.db 包含哪些 store？
expected_answer: knowledge_store(知识切片)、chat_memory(对话)、error_store(纠错)、strategy_store(策略)。
expected_sources: memory_store
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q012
topic: 01
question: Source Archive 和 Web Ingest 有什么区别？
expected_answer: Source Archive 是系统内部 ingest 后的文件归档。Web Ingest(网页导入)是 v0.1.5 未来计划。不要搞混。
expected_sources: source_archive, capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q013
topic: 01
question: archive_path 存储在哪里？
expected_answer: 存储在每个 knowledge_store chunk 的 metadata 中。CLI memory stats 显示 archived_files 计数。
expected_sources: source_archive, metadata
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q014
topic: 01
question: 如果只复制 memoryqwen.db 到新设备，会丢失什么？
expected_answer: 会丢失原始资料归档(memory/sources/中的 .md/.txt 文件)和任务状态(tasks.db)。建议复制整个 memory/ 文件夹。
expected_sources: source_archive, backup
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q015
topic: 01
question: Source Archive 是否依赖网络？
expected_answer: 不依赖。Source Archive 是纯本地文件复制操作，不需要网络连接。
expected_sources: source_archive
guard_expected: false
failure_type_if_wrong: source_misread
trap_level: low

