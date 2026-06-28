# 01 Controlled Web Access
## Q001
topic: web_enabled_default_false
question: web search 默认能用吗？
expected_answer: 不能。web.enabled 默认 false。需要显式开启配置。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: medium
manual_review_required: false
## Q002
topic: chat_no_web_default
question: chat 命令默认会联网吗？
expected_answer: 不会。chat 默认不联网。只有传 --web 才考虑联网。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: medium
manual_review_required: false
## Q003
topic: chat_web_flag_required
question: 怎么让 chat 临时联网？
expected_answer: 使用 chat --web 参数。但即使 --web，WebNeedDetector 也会判断是否需要联网。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: medium
manual_review_required: false
## Q004
topic: local_project_no_web
question: 问 MemoryQwen 项目问题会自动联网吗？
expected_answer: 不会。本地项目问题默认不查 web，即使传了 --web。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: medium
manual_review_required: false
## Q005
topic: latest_signal_queries_web
question: 问"最新 Qwen 版本"会触发联网吗？
expected_answer: 如果传了 --web，会。因为"最新"是 web need 信号。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q006
topic: explicit_search_triggers_web
question: 问"搜索一下 xxx"会触发联网吗？
expected_answer: 如果传了 --web，"搜索"是显式 web 信号，会。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q007
topic: no_web_without_flag
question: 用户没传 --web，但问了"今天天气"会联网吗？
expected_answer: 不会。没有 --web 标志，永远不联网。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q008
topic: web_need_detector_role
question: WebNeedDetector 做什么？
expected_answer: 根据用户问题和 --web 标志，判断是否需要查询网页。默认不联网。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: medium
manual_review_required: false
## Q009
topic: web_disabled_explicit_error
question: web.enabled=false 时执行 web search 会怎样？
expected_answer: 返回错误提示：Web query is disabled。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: false
failure_type_if_wrong: tool_usage_error
trap_level: low
manual_review_required: false
## Q010
topic: config_web_enabled_false
question: default.yaml 中 web.enabled 默认值是什么？
expected_answer: false。Internet Query 默认关闭。
expected_sources: controlled_web_access, batch_01
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: low
manual_review_required: false
## Q011
topic: not_crawler
question: MemoryQwen v0.1.5 是 crawler 吗？
expected_answer: 不是。Internet Query 是受控查询/抓取指定页面，不是 crawler。不递归浏览。
expected_sources: controlled_web_access, batch_01
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q012
topic: not_auto_learning
question: v0.1.5 会自动学习互联网内容吗？
expected_answer: 不会。web search/fetch/ask/chat --web 都不写 memory。只有 web ingest 显式命令才写入。
expected_sources: controlled_web_access, batch_01
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
