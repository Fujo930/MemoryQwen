# 06 Mixed Traps M2 Eval
类型: m2_eval_questions
更新时间: 2026-06-27

## Q001
topic: mixed_trap
question: source archive 是不是像 Google 一样的爬虫？
expected_answer: 不是。source archive 是本地文件复制归档，不涉及网络访问。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q002
topic: mixed_trap
question: GPU Guardian 是不是后台 daemon？
expected_answer: 不是。GPU Guardian 只是 nvidia-smi 查询工具，提供 guardian status/json 命令。
expected_sources: mixed_trap
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q003
topic: mixed_trap
question: 64% 准确率的 3B 能不能做正式主力？
expected_answer: 不能。3B 只适合 smoke test。正式使用需要 7B（91% 准确率）。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: mixed_trap
question: v0.1 有没有浏览器可访问的管理后台？
expected_answer: 没有。v0.1 是纯 CLI 系统，没有 Web UI，没有 FastAPI server。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q005
topic: mixed_trap
question: 32B 是不是比 14B 更适合家用电脑？
expected_answer: 不是。32B 需要 19GB+ VRAM，消费级 GPU 难以运行。推荐 7B 常驻 + 14B deep。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q006
topic: mixed_trap
question: source archive 是不是像 Google 一样的爬虫？
expected_answer: 不是。source archive 是本地文件复制归档，不涉及网络访问。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q007
topic: mixed_trap
question: GPU Guardian 是不是后台 daemon？
expected_answer: 不是。GPU Guardian 只是 nvidia-smi 查询工具，提供 guardian status/json 命令。
expected_sources: mixed_trap
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q008
topic: mixed_trap
question: 64% 准确率的 3B 能不能做正式主力？
expected_answer: 不能。3B 只适合 smoke test。正式使用需要 7B（91% 准确率）。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q009
topic: mixed_trap
question: v0.1 有没有浏览器可访问的管理后台？
expected_answer: 没有。v0.1 是纯 CLI 系统，没有 Web UI，没有 FastAPI server。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q010
topic: mixed_trap
question: 32B 是不是比 14B 更适合家用电脑？
expected_answer: 不是。32B 需要 19GB+ VRAM，消费级 GPU 难以运行。推荐 7B 常驻 + 14B deep。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high
