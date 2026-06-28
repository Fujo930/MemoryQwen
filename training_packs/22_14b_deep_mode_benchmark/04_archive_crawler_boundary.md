# 04 Archive Crawler Boundary
## Q001
topic: archive_boundary
question: source archive 是爬虫吗？
expected_answer: 不是。source archive 复制本地文件到 memory/sources。
expected_sources: archive_boundary, batch
guard_expected: true
deep_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q002
topic: archive_boundary
question: memory/sources 里是互联网资料吗？
expected_answer: 不是。是用户本地文件的归档副本。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q003
topic: archive_boundary
question: 删除 inbox 文件后 AI 会失忆吗？
expected_answer: 不会。资料已存入 memoryqwen.db。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q004
topic: archive_boundary
question: web ingest 和 source archive 的区别？
expected_answer: web ingest 抓取网页并归档，source archive 归档本地文件。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q005
topic: archive_boundary
question: source archive 会自动去重吗？
expected_answer: 会。SHA-256 哈希去重。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q006
topic: archive_boundary
question: memory/sources/web/ 是什么？
expected_answer: web ingest 保存网页的目录。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q007
topic: archive_boundary
question: source archive 能恢复已删除的 inbox 文件吗？
expected_answer: 能。归档在 memory/sources 中的文件可以复制回来。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q008
topic: archive_boundary
question: source_hash 和 content_hash 的区别？
expected_answer: source_hash 是整个文件的 SHA-256；content_hash 是单个 chunk 的。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q009
topic: archive_boundary
question: memoryqwen.db 能删除吗？
expected_answer: 不能。删除即丢失所有记忆。定期备份。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q010
topic: archive_boundary
question: memory 文件夹备份就够吗？
expected_answer: 够。memory/ 包含 SQLite DB + source archive + tasks.db。
expected_sources: archive_boundary, batch
guard_expected: false
deep_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
