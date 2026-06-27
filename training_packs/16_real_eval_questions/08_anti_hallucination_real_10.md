# Real Eval Questions — 08_anti_hallucination_real_10

## Q001
topic: 08
question: 资料不足时怎么回答？
expected_answer: 明确说'资料不足，无法确定'。不编造。可建议用户提供更多资料。
expected_sources: anti_hallucination
guard_expected: false
failure_type_if_wrong: hallucination
trap_level: high

## Q002
topic: 08
question: 能不能编造 CLI 命令？
expected_answer: 绝对不能。v0.1 没有的命令：cli webui, cli pdf ingest, cli daemon start, cli model unload, cli crawler。
expected_sources: anti_hallucination, cli_mastery
guard_expected: true
failure_type_if_wrong: tool_usage_error
trap_level: high

## Q003
topic: 08
question: 未来计划能不能说成已实现？
expected_answer: 绝对不能。Web UI/PDF/embedding/FastAPI 都是 v0.2 计划，必须说 v0.1 未实现。
expected_sources: anti_hallucination, capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: 08
question: [S] [E] [T] 代表什么？
expected_answer: [S]: 本地资料 sources。[E]: 错误记忆 error_store。[T]: 策略记忆 strategy_store。
expected_sources: anti_hallucination
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q005
topic: 08
question: sources 没命中时能装确定吗？
expected_answer: 不能。必须说资料不足或无法确定。不要把推测当事实。
expected_sources: anti_hallucination
guard_expected: false
failure_type_if_wrong: hallucination
trap_level: high

## Q006
topic: 08
question: 如果不确定，应该说推测还是确定？
expected_answer: 推测。并明确标注'根据现有信息推测'。不要暗示确定。
expected_sources: anti_hallucination
guard_expected: false
failure_type_if_wrong: hallucination
trap_level: medium

## Q007
topic: 08
question: Capability Bound Guard 的作用？
expected_answer: 检测用户问题是否涉及能力边界。高风险词(PDF/WebUI/daemon)触发 → 插入 10 条强制规则到 prompt。
expected_sources: anti_hallucination, capability_guard
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q008
topic: 08
question: 把 .md 导入说成 PDF 导入是什么错误？
expected_answer: capability_overclaim 和 hallucination。坚决不能说 v0.1 支持 PDF。
expected_sources: anti_hallucination, capability_boundary
guard_expected: true
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q009
topic: 08
question: Small Model Confusion 指什么？
expected_answer: 3B 等小模型把错误案例中的 wrong_answer 当成事实回答。7B 表现更好。
expected_sources: anti_hallucination, error_strategy
guard_expected: true
failure_type_if_wrong: small_model_confusion
trap_level: high

## Q010
topic: 08
question: 回答模板应该包含什么？
expected_answer: 结论(一句话直接答) + 依据(引用 sources [S1]) + 分析 + 不确定点 + 下一步建议。
expected_sources: anti_hallucination
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

