# MemoryQwen 项目定位

来源：MemoryQwen 项目文档
资料类型：project_doc
更新时间：2026-06-27
主题：MemoryQwen 是什么、不是什么、核心设计原则
关键词：MemoryQwen、本地 AI agent、RTX 4080、7B、14B、记忆系统

## 核心结论

MemoryQwen 是一个运行在用户自己电脑上的本地 AI agent 系统。它不是云服务，不是普通的聊天机器人，而是一个可以长期养成的本地 AI 工作站。

## 项目定位

- **本地优先**：所有数据和模型运行在用户本地电脑上，不依赖云端
- **记忆独立**：记忆由 MemoryBus 外部管理，不依赖模型上下文窗口
- **模型可换**：不绑定特定模型，支持 Qwen/通用 7B～14B
- **用户优先**：用户玩游戏或高 GPU 负载时，AI 自动让路
- **长期养成**：用户不断喂资料、纠错，系统持续学习

## 硬件目标

- GPU：RTX 4080 16GB
- 内存：32GB～64GB
- 硬盘：1TB～2TB NVMe
- 系统：优先 Windows，后续兼容 Linux

## 核心限制

- 默认模型卡在 7B～14B，不依赖 32B/70B
- 7B 作为常驻轻量 agent，14B 作为深度思考模型
- AI 不能长期霸占 GPU
- 记忆不能依赖模型上下文，必须由外部 MemoryBus 管理
- 模型可以随时替换，但 memory/ 文件夹不能丢

## 系统架构

MemoryQwen 由以下核心模块组成：

1. Model Server：支持 Ollama/LM Studio/llama.cpp/OpenAI-compatible
2. MemoryBus：管理所有长期记忆（knowledge_store、chat_memory、error_store、strategy_store）
3. Document Ingestion：解析 .txt/.md 文件 → 切片 → 索引 → 入库
4. Agent Server：编排检索 → 构建 prompt → 调用模型 → 保存记忆
5. Reasoner：7B 处理简单任务，14B 处理复杂推理
6. GPU Guardian：监测 GPU 负载，自动让路
7. Web UI：本地浏览器界面（待开发）

## 当前版本

v0.1 Developer Preview
- 已完成：模型客户端、记忆存储、文档导入、BM25 检索、Agent 聊天、错误学习、策略沉淀、GPU Guardian、任务运行时
- 测试：349 个测试全部通过
- 已在 Windows 11 + Ollama + RTX 4080 上通过真实冒烟测试

## 可测试问题

1. MemoryQwen 是什么？
2. MemoryQwen 的核心设计原则有哪些？
3. MemoryQwen 为什么不用 32B 模型做默认核心？
4. MemoryQwen 的系统架构包含哪些模块？
5. MemoryQwen 的记忆系统为什么独立于模型？
6. MemoryQwen v0.1 完成了哪些功能？
