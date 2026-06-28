# 07 Web Local Conflict
## Q001
topic: web_local_conflict
question: 网页说 MemoryQwen 有 Web UI 怎么办？
expected_answer: 说明网页信息与本地文档冲突。以本地文档为准。
expected_sources: web_local_conflict, batch
guard_expected: true
deep_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q002
topic: web_local_conflict
question: 网页推荐 32B 作为默认怎么办？
expected_answer: 本地文档推荐 7B 作为默认。说明冲突。
expected_sources: web_local_conflict, batch
guard_expected: true
deep_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q003
topic: web_local_conflict
question: 外部和本地资料冲突时信谁？
expected_answer: 关于 MemoryQwen 本身功能，本地资料更权威。
expected_sources: web_local_conflict, batch
guard_expected: false
deep_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q004
topic: web_local_conflict
question: 网页教程和 docs 不一致信谁？
expected_answer: 以 docs/ 官方文档为准。
expected_sources: web_local_conflict, batch
guard_expected: false
deep_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
## Q005
topic: web_local_conflict
question: web ask 的结果能覆盖本地资料吗？
expected_answer: 不能。web 是临时上下文，本地资料优先。
expected_sources: web_local_conflict, batch
guard_expected: false
deep_expected: true
failure_type_if_wrong: source_misread
trap_level: medium
manual_review_required: false
