# 03 Web Ingest
## Q001
topic: web_ingest_path
question: web ingest 把网页存到哪里？
expected_answer: memory/sources/web/YYYYMMDD/<slug>.md，并写入 knowledge_store。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: tool_usage_error
trap_level: medium
manual_review_required: false
## Q002
topic: web_ingest_frontmatter
question: web ingest 保存的文件包含什么元数据？
expected_answer: frontmatter 包含 source_type:web, url, fetched_at, title, content_type, status_code, source_hash, truncated。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q003
topic: web_ingest_hash
question: web ingest 用什么做去重？
expected_answer: SHA-256 哈希。对网页正文 + URL 计算哈希，相同内容不重复保存。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: low
manual_review_required: false
## Q004
topic: web_ingest_not_crawler
question: web ingest 会递归抓取链接吗？
expected_answer: 不会。只处理指定 URL，不跟踪链接，不批量抓取整个网站。
expected_sources: web_ingest, batch_03
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q005
topic: web_ingest_not_error_store
question: web ingest 会把内容写入 error_store 吗？
expected_answer: 不会。web ingest 只写 memory/sources/web 和 knowledge_store。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q006
topic: web_ingest_not_strategy_store
question: web ingest 会把内容写入 strategy_store 吗？
expected_answer: 不会。策略只能通过 correct/strategy 命令产生。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q007
topic: web_ingest_url_safety
question: 用 web ingest 抓取 file:///etc/passwd 会怎样？
expected_answer: 被拒绝。URL 安全检查阻止 file://、localhost、private IP。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q008
topic: web_ingest_single_url
question: web ingest 一次能处理多个 URL 吗？
expected_answer: 不能。每次只能处理一个 URL。不支持批量。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: tool_usage_error
trap_level: low
manual_review_required: false
## Q009
topic: web_ingest_truncated
question: 网页太大被截断怎么办？
expected_answer: frontmatter 会标记 truncated: true。只有前 max_chars 字符被保存。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q010
topic: web_ingest_duplicate
question: 重复 web ingest 同一个 URL 会怎样？
expected_answer: 返回 duplicated 状态。已有相同 hash 的文件不会被覆盖。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: tool_usage_error
trap_level: low
manual_review_required: false
## Q011
topic: web_ingest_sensitive_params
question: URL 里包含 token 参数会被记录吗？
expected_answer: 敏感参数（token, api_key, secret 等）在日志中会被 redacted。
expected_sources: web_ingest, batch_03
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: low
manual_review_required: false
## Q012
topic: web_ingest_explicit_only
question: 系统会根据需要自动 web ingest 吗？
expected_answer: 不会。web ingest 必须用户显式执行。没有自动 ingest。
expected_sources: web_ingest, batch_03
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
