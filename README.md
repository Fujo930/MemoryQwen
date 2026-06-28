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
# 1. 安装
git clone https://github.com/Fujo930/MemoryQwen
cd MemoryQwen
pip install -r requirements.txt

# 2. 拉取模型 (Ollama)
ollama pull qwen2.5:7b

# 3. 导入你的文档
mkdir inbox
echo "# 项目文档" > inbox/test.md
echo "API 地址是 http://localhost:8080" >> inbox/test.md
python -m src.cli job ingest inbox/

# 4. 开始聊天
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

## ✅ v0.1 功能概览

| 模块 | 功能 | 状态 |
|------|------|:----:|
| 📥 导入 | 文档导入 (.txt/.md) → SQLite | ✅ |
| 🔍 检索 | BM25 关键词检索，多库搜索 | ✅ |
| 💬 聊天 | 本地模型 (Ollama/LM Studio) + 来源引用 | ✅ |
| 🧠 记忆 | 对话历史 + 知识库持久化存储 | ✅ |
| 🐛 纠错 | 用户纠正错误 → 自动学习 → 不再重犯 | ✅ |
| 📋 策略 | 错误模式归纳 → 可复用策略沉淀 | ✅ |
| 🎮 GPU | GPU 占用检测 + 游戏/渲染/后台自动让路 | ✅ |
| 📊 任务 | 任务队列 + 暂停/恢复 + 持久化 | ✅ |
| 🧪 评估 | 130 道评估题 + 启发式判定器 + 自动导出纠正 | ✅ |
| 🛡️ 边界 | 能力边界守卫，防止模型幻觉夸大功能 | ✅ |
| 🌐 联网 | Internet Query：web search/fetch/ask，[W] 引用，不是 crawler | ✅ v0.1.5 |
| 🏷️ 来源 | 文件归档 → memory/sources/，聊天时精确引用 | ✅ |

## v0.1 尚未实现

> Web UI · PDF/DOCX · embedding/向量检索 · daemon 后台 · tray 图标 · 爬虫 · LoRA 微调 · 一键安装 exe

*这些在 v0.2+ 路线图中。v0.1.5 已支持受控联网查询。*

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

## 🛠️ 常用命令

```bash
python -m src.cli health              # 健康检查
python -m src.cli job ingest inbox/   # 导入文档
python -m src.cli chat "问题"         # 聊天 (自动检索本地资料)
python -m src.cli correct \           # 纠错学习
  --wrong "旧错误回答" \
  --correct "正确答案" \
  --strategy "避免策略"
python -m src.cli memory stats        # 存储统计
python -m src.cli guardian status     # GPU 让路状态
python -m src.cli task list           # 任务列表
python -m src.cli eval run training_packs/  # 运行评估
```

📖 [完整命令参考](docs/cli_reference.md)

## ⚠️ 备份记忆

**模型可以重新下载，memory 不能丢！**

```bash
xcopy memory memory_backup_%date% /E /I
```

详见 [记忆备份指南](docs/memory_backup.md)

## 📖 文档

| 文档 | 说明 |
|------|------|
| [Windows 11 快速启动](docs/windows11_quickstart.md) | 从零开始搭建 |
| [CLI 命令参考](docs/cli_reference.md) | 所有命令详解 |
| [配置参考](docs/config_reference.md) | YAML 配置项说明 |
| [系统架构](docs/architecture.md) | 技术架构文档 |
| [记忆备份](docs/memory_backup.md) | 备份策略 |
| [故障排除](docs/troubleshooting.md) | 常见问题 |
| [发布说明](docs/release_notes_v0.1.0-dev.md) | v0.1 更新日志 |

## 🗺️ 路线图

- **v0.1** (当前) — Developer Preview，CLI 形态
- **v0.1.5** ✅ — Internet Query (联网查询 + [W] 引用)
- **v0.2** — Web UI 图形界面
- **v0.3** — Embedding 向量检索 + 混合搜索

## 🤝 参与贡献

v0.1 是 Developer Preview，欢迎提 Issue 和 PR。

```bash
# 运行测试
python -m pytest tests/ -q --basetemp=/tmp/mqwen-pytest

# 格式化
pip install black && black src/ tests/
```

## 📄 License

MIT License © 2026 Fujo930 (MemoryQwen Contributors)

---

<p align="center">
  <sub>Built with ❤️ for local-first AI. No cloud required.</sub>
</p>
