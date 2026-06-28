<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.5-blue" alt="version">
  <img src="https://img.shields.io/badge/python-3.11+-blue" alt="python">
  <img src="https://img.shields.io/badge/tests-631%2F631-brightgreen" alt="tests">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey" alt="platform">
</p>

<p align="center">
  <b>🌐 <a href="README_EN.md">English</a> | 中文</b>
</p>

<h1 align="center">MemoryQwen</h1>
<h3 align="center">本地 AI Agent — 你的家用 AI 工作站</h3>

---

> **你的数据，你的模型，你的规则。** MemoryQwen 是一个完全运行在你电脑上的 AI agent 系统。不依赖任何云服务，所有数据留在本地。它会记住你教给它的一切，并在每次对话中引用来源。

## ✨ 为什么用 MemoryQwen？

| 对比 | ChatGPT / 云端 AI | MemoryQwen |
|------|-------------------|------------|
| 🌍 数据位置 | 云端服务器 | **你的硬盘** |
| 🔒 隐私 | 对话被记录 | **100% 本地** |
| 🧠 记忆力 | 依赖会话窗口 | **持久化 SQLite 记忆** |
| 📚 引用来源 | 幻觉 + 可能编造 | **精确引用原文 + 路径** |
| 🎯 纠错学习 | 无法纠正 | **一键纠错，永不再犯同类错误** |
| 💰 费用 | 按月付费 | **免费，用自己的 GPU** |
| ⚡ 离线可用 | ❌ | ✅ |

## ⚡ 5 分钟快速启动

```bash
git clone https://github.com/Fujo930/MemoryQwen
cd MemoryQwen
pip install -r requirements.txt
ollama pull qwen2.5:7b
mkdir inbox
echo "# 项目文档" > inbox/test.md
python -m src.cli job ingest inbox/
python -m src.cli chat "API 地址是什么？" --debug-memory
```

> 详细步骤见 [Windows 11 快速启动](docs/windows11_quickstart.md)

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────┐
│                     CLI / API                        │
├─────────────────────────────────────────────────────┤
│  Agent Layer  │ ChatService │ PromptBuilder          │
│               │ ErrorLearning │ StrategyLearning     │
│               │ CapabilityBoundaryGuard              │
├─────────────────────────────────────────────────────┤
│  Retrieval    │ BM25 Tokenizer │ Multi-Store Search  │
├─────────────────────────────────────────────────────┤
│  Memory       │ knowledge_store │ error_store        │
│  (SQLite)     │ strategy_store  │ chat_messages      │
│               │ task_records     │                   │
├─────────────────────────────────────────────────────┤
│  Infrastructure │ Ingestion │ FileWatcher            │
│                 │ GPU Guardian │ BackgroundJobRunner │
│                 │ TaskRuntime │ EvalRunner           │
├─────────────────────────────────────────────────────┤
│  Model Client  │ Ollama / LM Studio / llama.cpp      │
└─────────────────────────────────────────────────────┘
```

## ✅ v0.1.5 功能概览

| 模块 | 功能 | 状态 |
|------|------|:----:|
| 📥 导入 | 文档导入 (.txt/.md) → SQLite | ✅ |
| 🔍 检索 | BM25 关键词检索，多库搜索 | ✅ |
| 💬 聊天 | 本地模型 (Ollama/LM Studio) + 来源引用 | ✅ |
| 🌐 联网 | Internet Query：web search/fetch/ask，[W] 引用，不是 crawler | ✅ v0.1.5 |
| 🧠 记忆 | 对话历史 + 知识库持久化存储 | ✅ |
| 🐛 纠错 | 用户纠正错误 → 自动学习 → 不再重犯 | ✅ |
| 📋 策略 | 错误模式归纳 → 可复用策略沉淀 | ✅ |
| 🎮 GPU | GPU 占用检测 + 游戏/渲染/后台自动让路 | ✅ |
| 📊 任务 | 任务队列 + 暂停/恢复 + 持久化 | ✅ |
| 🧪 评估 | 130 道评估题 + 启发式判定器 + 自动导出纠正 | ✅ |
| 🛡️ 边界 | 能力边界守卫，防止模型幻觉夸大功能 | ✅ |
| 🏷️ 来源 | 文件归档 → memory/sources/，聊天时精确引用 | ✅ |

## v0.1.5 尚未实现

> Web UI · PDF/DOCX · embedding/向量检索 · daemon 后台 · tray 图标 · 爬虫 · LoRA 微调 · 一键安装 exe

## 📊 当前真实数据

| 指标 | 数值 |
|------|------|
| 🧪 pytest 测试 | **631/631** (100%) |
| 📚 知识片段 | **43,645** chunks |
| 🐛 错误案例 | **17** cases |
| 📋 策略 | **11** strategies |
| 📝 评估题目 | **396** real (M3 312 + web 84) |
| 🛡️ 安全扫描 | **0** issues |

## 🧠 模型推荐

| 模型 | 大小 | 用途 | 准确率 |
|------|------|------|:------:|
| `qwen2.5-coder:3b` | 1.9 GB | smoke test / 低配机 | ~64% |
| **`qwen2.5:7b`** ⭐ | **4.7 GB** | **日常使用** | **~91%** |
| `qwen2.5:14b` | ~8 GB | 深度推理 | 待测 |

> 💡 **3B 跑通，7B 常驻，14B 深度，32B+ 实验。**

## 🧱 开发困境 & 已知瓶颈

以下是在开发中遇到的实际困难，不美化、不隐藏。

### 🚧 推理墙

7B 模型在多源信息冲突时无法稳定推理。系统 prompt 说"v0.1.5 支持联网"，但 43K 条旧训练数据说"v0.1 不支持联网"——模型会在两者之间**随机摇摆**。同一个问题问三次，可能得到三种不同答案。

**这不是 prompt 工程能解决的。** 需要 14B+ 参数规模或新的推理架构。RTX 4080 刚好能跑 14B：`ollama pull qwen2.5:14b`。

### ⚖️ Heuristic Judge 关键词过敏

v4 启发式判定器会误判正确回答。模型说"v0.1 **不支持** PDF"，判定器看到"PDF"就标 overclaim。M3 300 题 eval 中 36 个"wrong"**100% 是判定器误判**，0 个真实违规。需要 Judge v5（LLM-as-Judge）。

### 🔍 检索质量瓶颈

BM25 在 43K chunks 中偏向高频旧文档。新增文档信号完全被淹没。eval 的 source_hit 率 **0%**——不是答案错了，是检索引擎拉不到正确资料。需要 Retrieval Quality v2。

### 🧩 单兵作战

所有代码、文档、测试、训练数据、eval 系统均为一人维护。欢迎贡献者。

## ⚠️ 备份记忆

**模型可以重新下载，memory 不能丢！**

```bash
xcopy memory memory_backup_%date% /E /I
```

详见 [记忆备份指南](docs/memory_backup.md)

## 🛠️ 常用命令

```bash
python -m src.cli health              # 健康检查
python -m src.cli job ingest inbox/   # 导入文档
python -m src.cli chat "问题"         # 聊天 (自动检索本地资料)
python -m src.cli web search "关键词" # 网页搜索 (v0.1.5)
python -m src.cli correct --wrong "旧错误" --correct "正确答案"
python -m src.cli memory stats        # 存储统计
python -m src.cli guardian status     # GPU 让路状态
python -m src.cli eval run training_packs/  # 运行评估
```

📖 [完整命令参考](docs/cli_reference.md)

## 📖 文档

| 文档 | 说明 |
|------|------|
| [Windows 11 快速启动](docs/windows11_quickstart.md) | 从零开始搭建 |
| [Internet Query](docs/internet_query.md) | 联网查询指南 |
| [CLI 命令参考](docs/cli_reference.md) | 所有命令详解 |
| [配置参考](docs/config_reference.md) | YAML 配置项说明 |
| [系统架构](docs/architecture.md) | 技术架构文档 |
| [安全模型](docs/security_model.md) | 安全设计 |
| [记忆备份](docs/memory_backup.md) | 备份策略 |

## 🗺️ 路线图

- **v0.1** ✅ — CLI 形态，Developer Preview
- **v0.1.5** ✅ — Internet Query (联网查询 + [W] 引用)
- **v0.2** — Web UI 图形界面
- **v0.3** — Embedding 向量检索 + 混合搜索

## 🤝 参与贡献

欢迎提 Issue 和 PR。

```bash
python -m pytest tests/ -q --basetemp=/tmp/mqwen-pytest
```

## 📄 License

MIT License © 2026 Fujo930 (MemoryQwen Contributors)

---

<p align="center">
  <sub>Built with ❤️ for local-first AI. No cloud required.</sub>
</p>
