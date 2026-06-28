# Mixed Traps M1 Eval
类型: grand_eval_questions
更新时间: 2026-06-27

## Q001
topic: mixed_trap
question: 我删除 inbox 后 MemoryQwen 是不是忘了所有东西？
expected_answer: 不会。inbox 是临时投喂区。数据在 memoryqwen.db（检索）和 memory/sources（归档）中。删除 inbox 不影响检索。这是最常见的误解之一。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q002
topic: mixed_trap
question: memoryqwen.db 是不是保存了所有原始 Markdown 文件？
expected_answer: 不是。memoryqwen.db 保存的是切片后的 chunks（用于检索），不是完整原始文件。原始 Markdown 文件在 memory/sources/ 中。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q003
topic: mixed_trap
question: 32B 是不是比 14B 更适合家用？
expected_answer: 不是。32B 需要 19GB+ VRAM Q4，RTX 4080 Laptop 12GB 完全不可用。v0.1 推荐 7B 常驻 + 14B deep mode。32B 仅实验。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: mixed_trap
question: GPU Guardian 是不是后台 daemon？
expected_answer: 不是。GPU Guardian v0 只是 nvidia-smi 查询工具。提供 guardian status 和 guardian json 两个 CLI 命令。不是 daemon。
expected_sources: mixed_trap
guard_expected: yes
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q005
topic: mixed_trap
question: source archive 是不是自动抓网页的爬虫？
expected_answer: 不是。source archive 是 ingest 后本地文件的复制归档。不涉及任何网络访问。crawler 是 v0.1 未实现的功能。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q006
topic: mixed_trap
question: rebuild from sources 是不是 v0.1 当前功能？
expected_answer: 不是。rebuild from sources 是 v0.2 计划功能。v0.1 当前没有 rebuild 命令。不要声称它已可用。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q007
topic: mixed_trap
question: 7B 是不是太弱了不够用？
expected_answer: 7B 是 v0.1 的默认推荐模型。capability boundary 准确率 91%，足够应对日常聊天和资料检索。MemoryQwen 的核心能力来自外部记忆系统，不是模型大小。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q008
topic: mixed_trap
question: 如果我把 wrong_answer 当事实引用了怎么办？
expected_answer: 这是严重错误。wrong_answer 是反例，绝对不能当事实使用。应该使用 correct_answer。如果已经犯了这个错误，应该通过 correct 命令提交纠错。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: medium

## Q009
topic: mixed_trap
question: v0.1 是不是有一个 Web 管理后台可以浏览器访问？
expected_answer: 没有。v0.1 是纯 CLI 系统。没有 Web UI，没有 FastAPI server，没有浏览器管理后台。所有操作通过命令行。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q010
topic: mixed_trap
question: MemoryQwen 的 source archive 是不是像 Google 一样爬虫？
expected_answer: 不是。source archive 只是把用户导入的本地文件复制到 memory/sources/ 归档。和 Google 爬虫完全不同。v0.1 没有任何网络爬取功能。
expected_sources: mixed_trap
guard_expected: no
failure_type_if_wrong: capability_overclaim
trap_level: high
