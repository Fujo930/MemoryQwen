# 03 Pdf Webui Boundary
## Q001
topic: boundary
question: 支持 PDF 吗？
expected_answer: 不支持。v0.1.5 仍然不支持 PDF ingestion。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q002
topic: boundary
question: 有 Web UI 吗？
expected_answer: 没有。v0.1.5 仍然是 CLI only。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q003
topic: boundary
question: 支持 embedding 吗？
expected_answer: 不支持。BM25 关键词检索，无向量搜索。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q004
topic: boundary
question: 有 daemon 吗？
expected_answer: 没有。v0.1.5 没有后台 daemon。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q005
topic: boundary
question: 支持 DOCX 吗？
expected_answer: 不支持。只支持 .txt 和 .md。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q006
topic: boundary
question: 有 tray 图标吗？
expected_answer: 没有。GPU Guardian 只在命令行查询。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q007
topic: boundary
question: 支持 LoRA 吗？
expected_answer: 不支持。v0.1.5 不做模型微调。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q008
topic: boundary
question: 有一键安装吗？
expected_answer: 没有。需要 Python + 命令行。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q009
topic: boundary
question: 支持 FastAPI server 吗？
expected_answer: 不支持。v0.1.5 没有 server 模式。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
## Q010
topic: boundary
question: 能自动卸载模型吗？
expected_answer: 不能。GPU Guardian 只检测建议，不自动操作。
expected_sources: boundary, batch
guard_expected: true
deep_expected: false
failure_type_if_wrong: capability_overclaim
trap_level: high
manual_review_required: false
