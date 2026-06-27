# MemoryQwen v0.1 — Developer Preview

🌐 [English](README_EN.md) | **中文**

**本地 AI agent，你的家用 AI 工作站。**

MemoryQwen 是一个运行在你自己的电脑上的 AI agent 系统。它不依赖云端，所有数据留在本地。

## v0.1 能做什么

| 功能 | 状态 |
|------|------|
| 文档导入 (.txt, .md) | ✅ |
| 关键词检索 (BM25) | ✅ |
| 本地模型聊天 (Ollama/LM Studio) | ✅ |
| 聊天时引用来源 | ✅ |
| 用户纠错 + 错误学习 | ✅ |
| 策略沉淀 | ✅ |
| GPU 占用检测 + 让路策略 | ✅ |
| 任务队列 + 暂停/恢复 | ✅ |
| 持久化任务状态 (SQLite) | ✅ |
| 中文文件名 / UTF-8 | ✅ |

## v0.1 不能做什么

- ❌ 图形界面 (Web UI 待开发)
- ❌ 向量检索 / embedding
- ❌ 多路径推理
- ❌ 后台 daemon / 自动运行
- ❌ 一键安装包

**v0.1 是 Developer Preview，面向开发者。** 需要命令行操作。

## 系统要求

- **OS:** Windows 10/11 (推荐 11 23H2+)
- **Python:** 3.11+
- **GPU:** 非必需，但推荐 NVIDIA (RTX 系列)
- **RAM:** 16GB+
- **后端:** Ollama / LM Studio / llama.cpp (OpenAI-compatible)

### 模型推荐

| 模型 | 大小 | 推荐用途 | 功能边界准确率 |
|------|------|---------|---------------|
| qwen2.5-coder:3b | 1.9GB | smoke test / 低资源 | ~64% |
| **qwen2.5:7b** | **4.7GB** | **默认常驻模型** | **~91%** |
| qwen2.5:14b | ~8GB | deep mode | 待测 |

> **3B 跑通，7B 常驻，14B 深度，32B+ 实验。**

## 当前真实状态

- **pytest:** 429/429
- **knowledge_store:** 395 chunks
- **error_store:** 17 cases
- **strategy_store:** 11 strategies
- **eval questions:** 130 real, 0 placeholder
- **safety:** 0 issues

## v0.1 未实现

Web UI, PDF, DOCX, embedding, daemon, tray, crawler, LoRA, 一键安装 exe.

## v0.1.5 计划

Internet Query (web search + fetch + ask with [W] citations).

## 5 分钟快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动模型服务

**Ollama (推荐):**
```bash
ollama serve
ollama pull qwen2.5:7b
```

**LM Studio:**
- 打开 LM Studio → 加载模型 → 开启 Local Server

### 3. 配置

编辑 `config/default.yaml`:

```yaml
model_client:
  provider: "ollama"           # 或 "lm_studio" / "llamacpp" / "openai_compatible"
  base_url: "http://localhost:11434"  # LM Studio: http://localhost:1234/v1
  model: "qwen2.5:7b"          # 你的模型名
```

### 4. 验证

```bash
python -m src.cli health
```

### 5. 聊天

```bash
# 创建测试资料
mkdir inbox
echo "# MemoryQwen" > inbox/test.md
echo "支持文档检索和关键词搜索。" >> inbox/test.md

# 导入
python -m src.cli job ingest inbox/

# 聊天
python -m src.cli chat "MemoryQwen 支持什么功能？" --debug-memory
```

## 常用命令

```bash
python -m src.cli health              # 健康检查
python -m src.cli job ingest inbox/   # 导入文档
python -m src.cli chat "问题"         # 聊天
python -m src.cli correct --wrong ".." --correct ".."  # 纠错
python -m src.cli memory stats        # 查看存储统计
python -m src.cli guardian status     # GPU 让路状态
python -m src.cli task list           # 任务列表
```

完整命令参考: [docs/cli_reference.md](docs/cli_reference.md)

## ⚠️ 重要：备份记忆

**模型可以重新下载，memory 不能丢！**

定期备份 `memory/` 文件夹：

```bash
xcopy memory memory_backup_%date% /E /I
```

详见: [docs/memory_backup.md](docs/memory_backup.md)

## 文档

- [Windows 11 快速启动](docs/windows11_quickstart.md)
- [CLI 命令参考](docs/cli_reference.md)
- [配置参考](docs/config_reference.md)
- [记忆备份](docs/memory_backup.md)
- [故障排除](docs/troubleshooting.md)
- [v0.1 发布检查清单](docs/release_checklist_v0.1.md)

## License

MemoryQwen v0.1 Developer Preview. 仅供开发测试。
