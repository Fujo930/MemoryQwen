# M2 Task Runtime + GPU Guardian 文档 118

类型：megatrain_longform_source
阶段：M2
主题：task_runtime_+_gpu_guardian
适用版本：MemoryQwen v0.1.0-dev
更新时间：2026-06-27

## 核心结论

MemoryQwen v0.1 的工作流以本地文件 ingest → knowledge_store 检索 → chat 回答 → correct 纠错 → strategy 沉淀为主线。GPU Guardian 提供 GPU 让路策略，Task Runtime 管理后台任务，Eval Runner 验证回答质量，Source Archive 保护原始资料。CLI 是唯一入口，不存在 Web UI、PDF ingestion、embedding、daemon、crawler。模型路线：3B 跑通、7B 常驻、14B 深度、32B+ 实验。

MemoryQwen v0.1 Developer Preview 的完整工作流：1) 用户准备 .md/.txt 资料放入 inbox/。2) 执行 job ingest 将文件解析为 chunks 存入 knowledge_store，同时原文归档到 memory/sources/。3) 用 chat 命令提问，系统通过 BM25 检索 knowledge_store 中的相关片段。4) CapabilityBoundaryGuard 检测能力边界问题并注入强制规则。5) model 根据 sources + errors + strategies 生成回答。6) 用户发现错误时用 correct 命令提交纠错。7) ErrorLearningService 写入 error_store，StrategyLearningService 自动生成 strategy_store 策略。8) Eval Runner 可批量验证回答质量并导出纠错草稿。9) GPU Guardian 通过 nvidia-smi 检测 GPU 状态并推荐模型让路。10) Task Runtime + Job Runner 管理可中断的后台任务。11) 备份 memory/ = 保留 sources + memoryqwen.db + tasks.db。12) 迁移新电脑：复制 memory/ + config/ 即可。

MemoryQwen v0.1 Developer Preview 的完整工作流：1) 用户准备 .md/.txt 资料放入 inbox/。2) 执行 job ingest 将文件解析为 chunks 存入 knowledge_store，同时原文归档到 memory/sources/。3) 用 chat 命令提问，系统通过 BM25 检索 knowledge_store 中的相关片段。4) CapabilityBoundaryGuard 检测能力边界问题并注入强制规则。5) model 根据 sources + errors + strategies 生成回答。6) 用户发现错误时用 correct 命令提交纠错。7) ErrorLearningService 写入 error_store，StrategyLearningService 自动生成 strategy_store 策略。8) Eval Runner 可批量验证回答质量并导出纠错草稿。9) GPU Guardian 通过 nvidia-smi 检测 GPU 状态并推荐模型让路。10) Task Runtime + Job Runner 管理可中断的后台任务。11) 备份 memory/ = 保留 sources + memoryqwen.db + tasks.db。12) 迁移新电脑：复制 memory/ + config/ 即可。

## 快速引用

- 真实 CLI：health, ingest, job ingest, chat, correct, memory stats, guardian status/json, task list/status/pause/resume/cancel, profile show/validate/eval, eval run/report/mark/export-corrections
- 假命令：cli webui, cli pdf, cli daemon, cli crawler, cli model unload, cli internet, cli fastapi
- 已实现：.txt/.md ingestion, source archive, memory_store, chat/error/strategy store, GPU Guardian detection, Task Runtime, Job Runner, Eval Runner, CapabilityBoundaryGuard
- 未实现：Web UI, FastAPI, PDF, DOCX, embedding, vector DB, daemon, tray, crawler, LoRA, fine-tuning, Internet Query

## 训练标签

v0.1, megatrain, m2, task_runtime_+_gpu_guardian, doc118
