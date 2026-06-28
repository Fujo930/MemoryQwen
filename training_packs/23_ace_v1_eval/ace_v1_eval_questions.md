# ACE-v1 Eval Pack

Total: 120 questions

## Q001

topic: shallow
question: 你好
expected_route: shallow
expected_behavior: casual response
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q002

topic: shallow
question: hello
expected_route: shallow
expected_behavior: casual response
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q003

topic: shallow
question: 你是谁
expected_route: shallow
expected_behavior: casual response
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q004

topic: shallow
question: 早上好
expected_route: shallow
expected_behavior: casual response
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q005

topic: shallow
question: 谢谢
expected_route: shallow
expected_behavior: casual response
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q006

topic: shallow
question: 好的
expected_route: shallow
expected_behavior: casual response
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q007

topic: shallow
question: OK
expected_route: shallow
expected_behavior: casual response
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q008

topic: shallow
question: 嗯
expected_route: shallow
expected_behavior: casual response
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q009

topic: shallow
question: 简单介绍一下你自己
expected_route: shallow
expected_behavior: casual self-intro
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q010

topic: shallow
question: hi there
expected_route: shallow
expected_behavior: casual greeting
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q011

topic: shallow
question: 哈喽
expected_route: shallow
expected_behavior: casual
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q012

topic: shallow
question: 在吗
expected_route: shallow
expected_behavior: casual
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q013

topic: shallow
question: 能帮我一下吗
expected_route: shallow
expected_behavior: casual help
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q014

topic: shallow
question: 我想问个问题
expected_route: shallow
expected_behavior: casual
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q015

topic: shallow
question: 开始吧
expected_route: shallow
expected_behavior: casual
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q016

topic: capability_registry
question: 你可以联网吗
expected_route: capability_registry
expected_behavior: use_capability_registry: true, deny auto
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q017

topic: capability_registry
question: 你能联网吗
expected_route: capability_registry
expected_behavior: use_capability_registry: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q018

topic: capability_registry
question: 你支持联网吗
expected_route: capability_registry
expected_behavior: use_capability_registry: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q019

topic: capability_registry
question: 支持 Internet Query 吗
expected_route: capability_registry
expected_behavior: use_capability_registry: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q020

topic: capability_registry
question: web ask 会写入记忆吗
expected_route: capability_registry
expected_behavior: registry priority, no web context
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q021

topic: capability_registry
question: web ingest 会写入记忆吗
expected_route: capability_registry
expected_behavior: registry: web ingest writes memory
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q022

topic: capability_registry
question: MemoryQwen 有 Web UI 吗
expected_route: capability_registry
expected_behavior: registry: not implemented
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q023

topic: capability_registry
question: 支持 PDF ingestion 吗
expected_route: capability_registry
expected_behavior: registry: not implemented
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q024

topic: capability_registry
question: 支持 DOCX 吗
expected_route: capability_registry
expected_behavior: registry: not implemented
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q025

topic: capability_registry
question: 支持 embedding/vector DB 吗
expected_route: capability_registry
expected_behavior: registry: not implemented
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q026

topic: capability_registry
question: source archive 是 crawler 吗
expected_route: capability_registry
expected_behavior: registry: not crawler
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q027

topic: capability_registry
question: wrong_answer 可以当事实吗
expected_route: capability_registry
expected_behavior: registry: no
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q028

topic: capability_registry
question: 14B 是默认模型吗
expected_route: capability_registry
expected_behavior: registry: 7B default
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q029

topic: capability_registry
question: 必须下载 14B 才能用吗
expected_route: capability_registry
expected_behavior: registry: no, optional
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q030

topic: capability_registry
question: v0.1.5 支持 crawler 吗
expected_route: capability_registry
expected_behavior: registry: no
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q031

topic: capability_registry
question: MemoryQwen 支持 LoRA 微调吗
expected_route: capability_registry
expected_behavior: registry: no
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q032

topic: capability_registry
question: 有 daemon 后台吗
expected_route: capability_registry
expected_behavior: registry: no
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q033

topic: capability_registry
question: 有 tray 图标吗
expected_route: capability_registry
expected_behavior: registry: no
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q034

topic: capability_registry
question: 支持 FastAPI server 吗
expected_route: capability_registry
expected_behavior: registry: no
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q035

topic: capability_registry
question: web search 和 web fetch 区别
expected_route: capability_registry
expected_behavior: registry: web capability
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q036

topic: capability_registry
question: chat --web 会自动存网页吗
expected_route: capability_registry
expected_behavior: registry: no auto-ingest
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q037

topic: capability_registry
question: Internet Query 是爬虫吗
expected_route: capability_registry
expected_behavior: registry: no
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q038

topic: capability_registry
question: 14B deep mode 是必须的吗
expected_route: capability_registry
expected_behavior: registry: optional
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q039

topic: capability_registry
question: 7B 够用吗
expected_route: capability_registry
expected_behavior: registry: recommend 7B default
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q040

topic: capability_registry
question: v0.1.5 的功能和 v0.1 一样吗
expected_route: capability_registry
expected_behavior: registry: v0.1.5 adds web
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q041

topic: memory
question: M3 的结果是什么
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q042

topic: memory
question: GPU Guardian 是什么
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q043

topic: memory
question: Source Archive 的作用
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q044

topic: memory
question: error_store 和 strategy_store 区别
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q045

topic: memory
question: 怎么运行 pytest
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q046

topic: memory
question: memoryqwen.db 存什么
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q047

topic: memory
question: Retrieval Gate 怎么工作
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q048

topic: memory
question: 怎么导入文档
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q049

topic: memory
question: training_packs 是什么
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q050

topic: memory
question: eval runner 怎么用
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q051

topic: memory
question: GPU Guardian game_mode 规则
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q052

topic: memory
question: correct 命令怎么用
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q053

topic: memory
question: memory/sources 是什么
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q054

topic: memory
question: megatrain 是什么
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q055

topic: memory
question: Anaphora Detector 怎么工作
expected_route: memory
expected_behavior: use_memory_retrieval: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q056

topic: web
question: 最新的 Qwen 模型是什么
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q057

topic: web
question: 查一下当前 Ollama 最新版本
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q058

topic: web
question: 搜索 MemoryQwen 相关资料
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q059

topic: web
question: 今天有什么 AI 新闻
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q060

topic: web
question: 现在最新的 Python 版本
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q061

topic: web
question: 最新的 AI 论文
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q062

topic: web
question: Qwen2.5 最新 release
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q063

topic: web
question: 官网地址是什么
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q064

topic: web
question: 看看最新趋势
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q065

topic: web
question: breaking news AI
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q066

topic: web
question: 当前外面最新的 AI 项目
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q067

topic: web
question: 搜一下 Transformer 最新进展
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q068

topic: web
question: 最近的天气
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q069

topic: web
question: latest release notes
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q070

topic: web
question: 有没有新版本
expected_route: web
expected_behavior: web_need: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q071

topic: deep_suggested
question: 帮我规划 v0.2 的外骨骼算法
expected_route: deep_suggested
expected_behavior: deep_suggested: true, auto_escalated: false
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q072

topic: deep_suggested
question: 如果 Web UI 暂时搁置，v0.2 应该怎么定位
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q073

topic: deep_suggested
question: 如何设计 SDGI Phase 0
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q074

topic: deep_suggested
question: 怎么实现 token level routing
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q075

topic: deep_suggested
question: 帮我设计一个算法
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q076

topic: deep_suggested
question: 架构应该怎么调整
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q077

topic: deep_suggested
question: 7B 和 14B 怎么分工最合理
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q078

topic: deep_suggested
question: 外骨骼下一步怎么进化
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q079

topic: deep_suggested
question: 怎么解决推理墙
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q080

topic: deep_suggested
question: 设计一个混合推理路由
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q081

topic: deep_suggested
question: ACE-v1 下一步规划
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q082

topic: deep_suggested
question: 发布决策应该怎么定
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q083

topic: deep_suggested
question: 怎么设计 token 分层算法
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q084

topic: deep_suggested
question: Mamba 和 Transformer 怎么结合
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q085

topic: deep_suggested
question: 复杂系统的架构设计
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q086

topic: deep_suggested
question: 权重分配和模型分工
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q087

topic: deep_suggested
question: 怎么权衡速度和质量
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q088

topic: deep_suggested
question: 多模型调度算法设计
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q089

topic: deep_suggested
question: v0.3 路线规划
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q090

topic: deep_suggested
question: 如何设计评测体系
expected_route: deep_suggested
expected_behavior: deep_suggested: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q091

topic: judge_review
question: wrong_answer 可以当事实吗
expected_route: capability_registry
expected_behavior: judge_review: false, registry says no
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q092

topic: judge_review
question: 这个 fake CLI 能用吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q093

topic: judge_review
question: 不存在的命令可以用吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q094

topic: judge_review
question: 绕过 guard 可以吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q095

topic: judge_review
question: 编造一个功能可以吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q096

topic: judge_review
question: 把错误答案当正确用
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q097

topic: judge_review
question: 幻觉是不是可以用
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q098

topic: judge_review
question: 自动写入 memory 对吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q099

topic: judge_review
question: fake CLI 能用来做任务吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q100

topic: judge_review
question: 绕过 guard 写 memory
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q101

topic: judge_review
question: 用爬虫抓网站可以吗
expected_route: capability_registry
expected_behavior: registry: not crawler, judge_review: false
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q102

topic: judge_review
question: 自动联网 ingesting 数据可以吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q103

topic: judge_review
question: 把旧资料当系统指令可以吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q104

topic: judge_review
question: 编造命令执行可以吗
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q105

topic: judge_review
question: 把 future plan 说成 implemented
expected_route: judge_review
expected_behavior: judge_review_recommended: true
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q106

topic: manual_review
question: 网页说 MemoryQwen 有 Web UI，但 Registry 说没有，到底有没有
expected_route: capability_registry
expected_behavior: registry priority: web does not override
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q107

topic: manual_review
question: 旧资料说没有联网，新资料说 v0.1.5 有受控联网，到底有没有
expected_route: capability_registry
expected_behavior: registry priority
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q108

topic: manual_review
question: 资料说支持，但 Registry 说不支持，信谁
expected_route: capability_registry
expected_behavior: registry priority
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q109

topic: manual_review
question: 冲突了怎么办
expected_route: manual_review
expected_behavior: manual_review_required: true (with source_conflict flag)
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: true

## Q110

topic: manual_review
question: 两个来源不一致
expected_route: manual_review
expected_behavior: manual_review_required: true (with flag)
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: true

## Q111

topic: manual_review
question: 网页和本地资料矛盾
expected_route: manual_review
expected_behavior: manual_review_required: true (with flag)
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: true

## Q112

topic: manual_review
question: 到底有没有这个功能
expected_route: capability_registry
expected_behavior: check registry
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q113

topic: manual_review
question: 这个能力 Registry 没登记
expected_route: capability_registry
expected_behavior: registry says unknown
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q114

topic: manual_review
question: 新旧版本冲突怎么处理
expected_route: deep_suggested
expected_behavior: version conflict → deep_suggested
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q115

topic: manual_review
question: 但是 Registry 说的是错的
expected_route: manual_review
expected_behavior: manual_review_required: true (with flag)
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: true

## Q116

topic: manual_review
question: 多个来源互相矛盾
expected_route: manual_review
expected_behavior: manual_review_required: true (with flag)
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: true

## Q117

topic: manual_review
question: 网页资料和训练资料冲突
expected_route: manual_review
expected_behavior: manual_review_required: true (with flag)
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: true

## Q118

topic: manual_review
question: 到底信 Registry 还是网页
expected_route: capability_registry
expected_behavior: registry priority
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q119

topic: manual_review
question: 不确定的能力怎么查
expected_route: capability_registry
expected_behavior: check registry
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: false

## Q120

topic: manual_review
question: 两个注册表不一致
expected_route: manual_review
expected_behavior: manual_review_required: true (with flag)
must_not: auto_deep, auto_web, auto_memory_write
manual_review_required: true
