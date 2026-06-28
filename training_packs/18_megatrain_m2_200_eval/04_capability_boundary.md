# 04 Capability Boundary M2 Eval
类型: m2_eval_questions
更新时间: 2026-06-27

## Q001
topic: capability_boundary
question: MemoryQwen v0.1 支持 PDF ingestion 吗？
expected_answer: 不支持。只支持 .txt 和 .md。PDF 是 v0.2 未来计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q002
topic: capability_boundary
question: MemoryQwen v0.1 支持 embedding/vector DB 吗？
expected_answer: 不支持。使用 BM25 关键词检索。embedding 是 v0.2 计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q003
topic: capability_boundary
question: MemoryQwen v0.1 有 FastAPI server 吗？
expected_answer: 没有。FastAPI 是 v0.2 计划。当前所有功能通过 CLI 操作。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q004
topic: capability_boundary
question: MemoryQwen v0.1 有 daemon/tray 吗？
expected_answer: 没有。GPU Guardian 只是查询工具，不是后台服务。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q005
topic: capability_boundary
question: MemoryQwen v0.1 会 kill 进程吗？
expected_answer: 不会。GPU Guardian 只做检测和建议，不执行 kill。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q006
topic: capability_boundary
question: MemoryQwen v0.1 支持 LoRA 或微调吗？
expected_answer: 不支持。AutoModelAdapter 是轻量评估工具，不是 LoRA。v0.1 不改模型权重。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q007
topic: capability_boundary
question: 列举 3 个 v0.1 已实现功能
expected_answer: CLI、ingest .txt/.md、chat、correct、guardian status、task management、eval runner、source archive
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q008
topic: capability_boundary
question: 列举 3 个 v0.1 未实现功能
expected_answer: Web UI、PDF ingestion、embedding、daemon、crawler、LoRA、FastAPI
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q009
topic: capability_boundary
question: MemoryQwen v0.1 支持 PDF ingestion 吗？
expected_answer: 不支持。只支持 .txt 和 .md。PDF 是 v0.2 未来计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q010
topic: capability_boundary
question: MemoryQwen v0.1 支持 embedding/vector DB 吗？
expected_answer: 不支持。使用 BM25 关键词检索。embedding 是 v0.2 计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q011
topic: capability_boundary
question: MemoryQwen v0.1 有 FastAPI server 吗？
expected_answer: 没有。FastAPI 是 v0.2 计划。当前所有功能通过 CLI 操作。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q012
topic: capability_boundary
question: MemoryQwen v0.1 有 daemon/tray 吗？
expected_answer: 没有。GPU Guardian 只是查询工具，不是后台服务。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q013
topic: capability_boundary
question: MemoryQwen v0.1 会 kill 进程吗？
expected_answer: 不会。GPU Guardian 只做检测和建议，不执行 kill。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q014
topic: capability_boundary
question: MemoryQwen v0.1 支持 LoRA 或微调吗？
expected_answer: 不支持。AutoModelAdapter 是轻量评估工具，不是 LoRA。v0.1 不改模型权重。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q015
topic: capability_boundary
question: 列举 3 个 v0.1 已实现功能
expected_answer: CLI、ingest .txt/.md、chat、correct、guardian status、task management、eval runner、source archive
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q016
topic: capability_boundary
question: 列举 3 个 v0.1 未实现功能
expected_answer: Web UI、PDF ingestion、embedding、daemon、crawler、LoRA、FastAPI
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q017
topic: capability_boundary
question: MemoryQwen v0.1 支持 PDF ingestion 吗？
expected_answer: 不支持。只支持 .txt 和 .md。PDF 是 v0.2 未来计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q018
topic: capability_boundary
question: MemoryQwen v0.1 支持 embedding/vector DB 吗？
expected_answer: 不支持。使用 BM25 关键词检索。embedding 是 v0.2 计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q019
topic: capability_boundary
question: MemoryQwen v0.1 有 FastAPI server 吗？
expected_answer: 没有。FastAPI 是 v0.2 计划。当前所有功能通过 CLI 操作。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q020
topic: capability_boundary
question: MemoryQwen v0.1 有 daemon/tray 吗？
expected_answer: 没有。GPU Guardian 只是查询工具，不是后台服务。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q021
topic: capability_boundary
question: MemoryQwen v0.1 会 kill 进程吗？
expected_answer: 不会。GPU Guardian 只做检测和建议，不执行 kill。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q022
topic: capability_boundary
question: MemoryQwen v0.1 支持 LoRA 或微调吗？
expected_answer: 不支持。AutoModelAdapter 是轻量评估工具，不是 LoRA。v0.1 不改模型权重。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q023
topic: capability_boundary
question: 列举 3 个 v0.1 已实现功能
expected_answer: CLI、ingest .txt/.md、chat、correct、guardian status、task management、eval runner、source archive
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q024
topic: capability_boundary
question: 列举 3 个 v0.1 未实现功能
expected_answer: Web UI、PDF ingestion、embedding、daemon、crawler、LoRA、FastAPI
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q025
topic: capability_boundary
question: MemoryQwen v0.1 支持 PDF ingestion 吗？
expected_answer: 不支持。只支持 .txt 和 .md。PDF 是 v0.2 未来计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q026
topic: capability_boundary
question: MemoryQwen v0.1 支持 embedding/vector DB 吗？
expected_answer: 不支持。使用 BM25 关键词检索。embedding 是 v0.2 计划。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q027
topic: capability_boundary
question: MemoryQwen v0.1 有 FastAPI server 吗？
expected_answer: 没有。FastAPI 是 v0.2 计划。当前所有功能通过 CLI 操作。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q028
topic: capability_boundary
question: MemoryQwen v0.1 有 daemon/tray 吗？
expected_answer: 没有。GPU Guardian 只是查询工具，不是后台服务。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q029
topic: capability_boundary
question: MemoryQwen v0.1 会 kill 进程吗？
expected_answer: 不会。GPU Guardian 只做检测和建议，不执行 kill。
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q030
topic: capability_boundary
question: MemoryQwen v0.1 支持 LoRA 或微调吗？
expected_answer: 不支持。AutoModelAdapter 是轻量评估工具，不是 LoRA。v0.1 不改模型权重。
expected_sources: capability_boundary
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q031
topic: capability_boundary
question: 列举 3 个 v0.1 已实现功能
expected_answer: CLI、ingest .txt/.md、chat、correct、guardian status、task management、eval runner、source archive
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q032
topic: capability_boundary
question: 列举 3 个 v0.1 未实现功能
expected_answer: Web UI、PDF ingestion、embedding、daemon、crawler、LoRA、FastAPI
expected_sources: capability_boundary
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium
## Q033
topic: capability_boundary
question: MemoryQwen v0.1 是否已完成 120-question benchmark？
expected_answer: 没有。M2 执行了 162 题 eval pilot，full benchmark 系统在开发中。不要把 pilot 说成 benchmark。
expected_sources: capability_boundary
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q034
topic: capability_boundary
question: v0.1 的 CapabilityBoundaryGuard 的三种风险等级？
expected_answer: high (PDF/WebUI/daemon 等)、medium (是否/支持/当前/已实现)、low (不确定)。
expected_sources: capability_boundary
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q035
topic: capability_boundary
question: v0.1 完成了 120-question benchmark 吗？
expected_answer: 没有。M2 163 题是 eval pilot。full benchmark 系统在开发中。
expected_sources: capability_boundary
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q036
topic: capability_boundary
question: CapabilityBoundaryGuard 的三种风险等级？
expected_answer: high(PDF/WebUI/daemon), medium(支持/是否/当前), low(不确定)。
expected_sources: capability_boundary
failure_type_if_wrong: capability_overclaim
trap_level: high

