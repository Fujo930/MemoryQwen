# Real Validation Questions

## Q001
topic: source_archive
question: 用户删除 inbox 里的 .md 文件后，MemoryQwen 还能检索到这些文件的内容吗？为什么？
expected_answer: 能。因为 ingest 后原始文件已归档到 memory/sources/，知识切片已存入 memory/memoryqwen.db。inbox 只是临时投喂入口。
expected_sources: source_archive_backup
guard_expected: false
trap_level: medium

## Q002
topic: source_archive
question: 只备份 memory/memoryqwen.db 够吗？还需要备份什么？
expected_answer: 不够。还需要备份 memory/sources/（原始资料归档）和 memory/tasks.db（任务状态）。备份整个 memory/ 文件夹即可带走全部 AI 资产。
expected_sources: source_archive_backup
guard_expected: false
trap_level: medium

## Q003
topic: source_archive
question: memory/sources 是不是全站爬虫 crawler？
expected_answer: 不是。memory/sources 是 ingest 成功后的原始资料归档目录，不是爬虫。v0.1 没有 crawler 功能。
expected_sources: capability_boundaries
guard_expected: true
trap_level: high

## Q004
topic: source_archive
question: source_hash 和 content_hash 有什么区别？
expected_answer: source_hash 是整个原始文件的 sha256，用于归档去重。content_hash 是每个切片的 hash，用于 knowledge_store 去重。两者不同。
expected_sources: source_archive_backup
guard_expected: false
trap_level: low

## Q005
topic: source_archive
question: ingest 后的文件去了哪里？
expected_answer: 文件被解析（parse）、切片（chunk）、存入 knowledge_store（切片+metadata）、然后原始文件被复制到 memory/sources/（归档）。同时 metadata 中写入 archive_path 和 source_hash。
expected_sources: source_archive_backup, ingestion
guard_expected: false
trap_level: low
