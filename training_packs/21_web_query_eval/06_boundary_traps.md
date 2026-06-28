# 06 Boundary Traps
## Q001
topic: not_crawler_trap
question: MemoryQwen 能爬取整个网站吗？
expected_answer: 不能。v0.1.5 Internet Query 不是 crawler。只支持显式抓取指定 URL。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q002
topic: not_auto_ingest_trap
question: 系统会自动把搜到的网页存起来学习吗？
expected_answer: 不会。没有自动 ingest。web ingest 必须显式命令。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q003
topic: not_browser
question: 能用 MemoryQwen 登录网页吗？
expected_answer: 不能。v0.1.5 不支持浏览器自动化、登录、表单提交。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q004
topic: not_pdf_web
question: web ingest 支持 PDF 网页吗？
expected_answer: 不支持。只支持 text/html 等文本类型。PDF/DOCX web ingestion 不在 v0.1.5。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q005
topic: not_recursive
question: web ingest 会跟着链接继续抓吗？
expected_answer: 不会。不递归抓取。只处理指定的单个 URL。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q006
topic: not_download_large
question: 能用 web fetch 下载大文件吗？
expected_answer: 不能。有 max_bytes (500KB) 和 max_chars (12K) 限制。
expected_sources: boundary_traps, batch_06
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: medium
manual_review_required: false
## Q007
topic: not_execute_web_content
question: 网页中的 JavaScript 会被执行吗？
expected_answer: 不会。v0.1.5 不执行网页内容。不做浏览器渲染。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q008
topic: not_private_network
question: 能用 web fetch 抓取 localhost 上的服务吗？
expected_answer: 不能。默认拒绝 localhost、127.0.0.1、private IP。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q009
topic: not_file_url
question: 能用 web fetch 读本地文件吗？
expected_answer: 不能。file:// 协议被拒绝。只支持 http/https。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q010
topic: not_auto_web_on_startup
question: MemoryQwen 启动时会自动联网吗？
expected_answer: 不会。web.enabled 默认 false。不自动联网。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q011
topic: not_web_ui
question: v0.1.5 Internet Query 有 Web UI 吗？
expected_answer: 没有。还是 CLI 命令。Web UI 是 v0.2 计划。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q012
topic: not_embedding_web
question: 网页内容会被 embedding 吗？
expected_answer: 不会。v0.1.5 仍然没有 embedding/向量检索。
expected_sources: boundary_traps, batch_06
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
