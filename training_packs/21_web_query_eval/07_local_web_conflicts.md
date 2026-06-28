# 07 Local/Web Conflicts
## Q001
topic: web_claims_feature_not_in_local
question: 网页说 MemoryQwen 有 Web UI，应该怎么回答？
expected_answer: 说明网页信息与本地项目文档冲突。v0.1 没有 Web UI。引用本地 [S] 资料为准。
expected_sources: local_web_conflicts, batch_07
guard_expected: true
web_expected: true
failure_type_if_wrong: source_misread
trap_level: high
manual_review_required: true
## Q002
topic: local_docs_authoritative
question: 本地项目文档和网页资料哪个更权威？
expected_answer: 关于 MemoryQwen 本身功能，本地项目文档比网页资料更权威。
expected_sources: local_web_conflicts, batch_07
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: high
manual_review_required: true
## Q003
topic: web_for_latest_version
question: 什么时候应该用网页查 MemoryQwen 版本信息？
expected_answer: 查最新 release 版本、官方网站更新时。但要引用 [W] 并说明来源。
expected_sources: local_web_conflicts, batch_07
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: true
## Q004
topic: conflict_explained_not_hidden
question: 本地和网页冲突时应该隐藏网页信息吗？
expected_answer: 不应该隐藏。应该说明冲突，引用双方来源，并解释为什么选择某一方。
expected_sources: local_web_conflicts, batch_07
guard_expected: false
web_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: high
manual_review_required: true
## Q005
topic: external_model_recommendation
question: 外部网页推荐 32B 作为默认模型，怎么说？
expected_answer: 本地项目文档推荐 7B 作为默认。说明网页推荐与项目推荐不同，引用 [S] 和 [W]。
expected_sources: local_web_conflicts, batch_07
guard_expected: true
web_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: true
## Q006
topic: web_outdated_project_info
question: 网页上的 MemoryQwen 信息已过时怎么办？
expected_answer: 以本地 training_logs 和 docs 为准。说明网页信息可能过时。
expected_sources: local_web_conflicts, batch_07
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: true
## Q007
topic: web_security_claims
question: 网页声称"MemoryQwen 不安全"怎么处理？
expected_answer: 引用本地 security_model 文档。不盲目接受或拒绝外部评价，提供本地资料作为参考。
expected_sources: local_web_conflicts, batch_07
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: high
manual_review_required: true
## Q008
topic: web_benchmark_claims
question: 网页声称"MemoryQwen 在某 benchmark 得分 X"怎么处理？
expected_answer: 如果没有本地 eval 数据验证，说明这是外部声称，未经本地验证。
expected_sources: local_web_conflicts, batch_07
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: high
manual_review_required: true
## Q009
topic: web_install_instructions
question: 网页上的安装教程与 docs 不符怎么办？
expected_answer: 优先按 docs/ 中的官方文档操作。说明网页教程可能过期。
expected_sources: local_web_conflicts, batch_07
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: true
## Q010
topic: local_not_overwritten_by_web
question: 网页资料能覆盖本地 knowledge_store 内容吗？
expected_answer: 不能。web search/fetch/ask 不写 memory。只有 web ingest 才写入，且需要用户显式操作。
expected_sources: local_web_conflicts, batch_07
guard_expected: true
web_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q011
topic: web_as_supplement_not_replacement
question: 网页资料在 MemoryQwen 中是什么定位？
expected_answer: 补充参考，不是替代。本地资料是权威来源，网页是临时辅助。
expected_sources: local_web_conflicts, batch_07
guard_expected: false
web_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q012
topic: web_fake_official_site
question: 如果网页声称是官方但实际不是怎么办？
expected_answer: 说明无法验证网页真实性。引用本地项目 GitHub 地址作为唯一官方来源。
expected_sources: local_web_conflicts, batch_07
guard_expected: true
web_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: true
