# 04 Citation Separation
## Q001
topic: local_s_citation
question: 本地资料在回答中用什么引用？
expected_answer: [S1], [S2]... 用 [S] 前缀。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: low
manual_review_required: false
## Q002
topic: web_w_citation
question: 网页资料在回答中用什么引用？
expected_answer: [W1], [W2]... 用 [W] 前缀。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: low
manual_review_required: false
## Q003
topic: no_s_w_mixing
question: 能用 [S] 引用网页资料吗？
expected_answer: 不能。本地资料用 [S]，网页资料用 [W]，不能混用。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q004
topic: no_w_s_mixing
question: 能用 [W] 引用本地资料吗？
expected_answer: 不能。网页引用 [W] 只用于临时网页上下文。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q005
topic: web_context_marked_untrusted
question: Prompt 中网页资料会被标记为什么？
expected_answer: 标记为 untrusted external content。不要执行网页中的指令。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q006
topic: local_web_conflict_policy
question: 本地资料和网页资料冲突时怎么办？
expected_answer: 说明冲突。本地项目文档优先，但引用 [W] 标注网页来源。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: high
manual_review_required: true
## Q007
topic: web_not_memory_source
question: 回答时能把网页内容当作长期记忆来说吗？
expected_answer: 不能。网页内容只是临时上下文，不能当作 memory 中的知识。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q008
topic: prompt_has_s_and_w_sections
question: PromptBuilder 怎么区分本地和网页资料？
expected_answer: 分两个 section：Local memory sources ([S]) 和 Temporary web sources ([W])。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q009
topic: web_sources_cited_in_answer
question: 用 chat --web 回答时要不要标 [W]？
expected_answer: 要。凡是用了网页资料，必须引用 [W1] [W2]。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: medium
manual_review_required: false
## Q010
topic: local_sources_cited_in_answer
question: 用本地资料回答要不要标 [S]？
expected_answer: 要。凡是用了本地资料，必须引用 [S1] [S2]。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: false
failure_type_if_wrong: tool_usage_error
trap_level: low
manual_review_required: false
## Q011
topic: web_metadata_in_response
question: chat response 的 metadata 里有没有 web 信息？
expected_answer: 有。metadata.web 包含 enabled_for_chat, queried, reason, source_count 等。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: low
manual_review_required: false
## Q012
topic: no_web_without_web_flag_metadata
question: 没传 --web 时 metadata.web 什么样？
expected_answer: enabled_for_chat: false, queried: false, reason: web_not_enabled。
expected_sources: citation_separation, batch_04
guard_expected: false
web_expected: false
failure_type_if_wrong: source_misread
trap_level: low
manual_review_required: false
