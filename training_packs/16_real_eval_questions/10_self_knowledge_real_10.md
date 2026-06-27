# Real Eval Questions — 10_self_knowledge_real_10

## Q001
topic: 10
question: MemoryQwen 是什么？
expected_answer: 本地 AI agent 系统。在自己的电脑上运行，数据不离本机。不是云服务，不是 ChatGPT。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q002
topic: 10
question: MemoryQwen 的核心设计哲学？
expected_answer: 模型不负责记忆。MemoryBus 管理一切长期状态。即使切换模型，知识/对话/错误/策略都保留。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q003
topic: 10
question: AgentChatService 的流程？
expected_answer: 保存用户消息→检索 knowledge/error/strategy→获取最近对话→CapabilityBoundGuard 检测→PromptBuilder 构建→调用 ModelClient→保存 assistant 回答。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q004
topic: 10
question: PromptBuilder 包含哪些部分？
expected_answer: 能力边界检查(如有)→本地资料片段[S1]→错误案例[E1]→策略[T1]→最近对话→用户问题。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q005
topic: 10
question: MemoryQwen 支持哪些 model provider？
expected_answer: Ollama, LM Studio, llama.cpp, 及任意 OpenAI-compatible API。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q006
topic: 10
question: BM25 检索支持中文吗？
expected_answer: 支持。tokenizer 使用 unigram+bigram 做中文分词。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q007
topic: 10
question: Source Archive 是什么？
expected_answer: ingest 成功后自动复制原始文件到 memory/sources/ 的归档功能。保留相对目录结构，source_hash 去重。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q008
topic: 10
question: Capability Bound Guard 做什么？
expected_answer: 检测用户问题关键词(high/medium risk) → 如果是能力边界问题 → 注入 10 条强制规则到 prompt。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: medium

## Q009
topic: 10
question: Eval Runner 做什么？
expected_answer: 加载验证题库 → 批量调用 AgentChatService(每题独立 session) → 生成 JSON+MD 报告。支持人工 mark 和 export corrections。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q010
topic: 10
question: MemoryQwen 的数据是否上传云端？
expected_answer: 不上传。所有数据存储在本地 memory/ 目录的 SQLite 数据库和 Markdown 文件中。
expected_sources: self_knowledge
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: high

