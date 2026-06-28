# 02 Temporary Context
## Q001
topic: web_search_no_memory
question: web search 会写入 knowledge_store 吗？
expected_answer: 不会。web search 只返回搜索结果，不写 memory。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q002
topic: web_fetch_no_memory
question: web fetch 会写入 memory 吗？
expected_answer: 不会。web fetch 只抓取并显示网页内容，不写 memory。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q003
topic: web_ask_no_memory
question: web ask 会把网页内容存到知识库吗？
expected_answer: 不会。web ask 使用临时上下文回答，不写 knowledge_store。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q004
topic: chat_web_no_memory
question: chat --web 的网页内容会保存吗？
expected_answer: 不会。chat --web 的网页资料只是临时上下文，回答完就丢弃。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q005
topic: only_ingest_writes
question: 什么操作会把网页内容写入知识库？
expected_answer: 只有 web ingest 命令才会显式写入 memory/sources/web 和 knowledge_store。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: tool_usage_error
trap_level: medium
manual_review_required: false
## Q006
topic: temp_context_lifetime
question: chat --web 的网页上下文在对话结束后还保留吗？
expected_answer: 不保留。临时网页上下文只在当次 chat 中有效。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q007
topic: web_context_not_persistent
question: web search 的结果会出现在下一次 chat 里吗？
expected_answer: 不会。web search 的结果不保存，下次 chat 不会自动引用。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q008
topic: no_auto_web_memory
question: 系统会自动把有用的网页存起来吗？
expected_answer: 不会。必须用户显式运行 web ingest。没有自动记忆网页功能。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q009
topic: web_context_not_error_source
question: 网页内容会进入 error_store 吗？
expected_answer: 不会。网页内容不能作为纠错证据进入 error_store。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q010
topic: web_context_not_strategy_source
question: 网页内容会进入 strategy_store 吗？
expected_answer: 不会。策略只从用户显式 correct/strategy 命令产生。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q011
topic: web_search_read_only
question: web search 是只读操作吗？
expected_answer: 是。只返回标题、URL、摘要，不修改任何本地数据。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: low
manual_review_required: false
## Q012
topic: web_fetch_read_only
question: web fetch 是只读操作吗？
expected_answer: 是。只抓取并显示网页内容，不写入本地存储。
expected_sources: temporary_context, batch_02
guard_expected: false
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: low
manual_review_required: false
