# MemoryQwen 本地真实模型冒烟测试

本文档描述如何在本地真实模型运行时，手动验证 MemoryQwen 的完整闭环。

## 前置条件

- Python 3.11+
- 已安装依赖: `pip install -r requirements.txt`
- 至少一个本地模型服务运行中

## A. LM Studio 启动方式

1. 打开 LM Studio
2. 加载模型 (推荐 Qwen 2.5 7B)
3. 开启 **Local Server** (Developer → Local Server → Start Server)
4. 默认端口: `http://localhost:1234`

**配置 config/default.yaml:**
```yaml
model_client:
  provider: "lm_studio"
  base_url: "http://localhost:1234/v1"
  model: ""   # 留空使用 LM Studio 当前加载的模型
```

## B. Ollama 启动方式

```bash
# 启动 Ollama 服务
ollama serve

# 拉取模型（如未安装）
ollama pull qwen2.5:7b

# 确认模型可用
ollama list
```

**配置 config/default.yaml:**
```yaml
model_client:
  provider: "ollama"
  base_url: "http://localhost:11434"
  model: "qwen2.5:7b"
```

## C. llama.cpp server 启动方式

```bash
# 下载模型文件并启动 server
llama-server \
  -m models/qwen2.5-7b-instruct-q4_k_m.gguf \
  --host 127.0.0.1 \
  --port 8080
```

**配置 config/default.yaml:**
```yaml
model_client:
  provider: "llamacpp"
  base_url: "http://localhost:8080/v1"
  model: ""   # llama.cpp server 通常不需要指定
```

## D. 冒烟测试流程

### 1. 健康检查

```bash
python -m src.cli health
```

预期输出：
```
MemoryQwen Health Check
========================================
✓ Config: MemoryQwen v0.1.0
✓ Memory Store: OK (0 knowledge chunks)
✓ Model Client: OK
========================================
```

### 2. 准备测试资料

创建 `inbox/test.md`:
```markdown
# MemoryQwen 使用指南

MemoryQwen 是一个运行在本地电脑上的 AI agent 系统。
它支持文档导入、关键词检索、错误学习和策略沉淀。

## 核心功能
- 文档导入：支持 .txt 和 .md 格式
- 关键词检索：基于 BM25 的中英文检索
- 错误学习：用户纠错后系统记住并避免重复
- 策略沉淀：错误经验自动生成可复用策略
```

### 3. 导入资料

```bash
python -m src.cli ingest inbox/
```

预期输出：
```
Ingesting: inbox/
  Files seen:    1
  Files ingested:1
  Files skipped: 0
  Chunks created:2
  Chunks stored: 2
  Duplicates:    0
```

### 4. 首次聊天

```bash
python -m src.cli chat "MemoryQwen 有哪些核心功能？" --session test-run
```

预期：
- 模型回复提到文档导入、关键词检索、错误学习等
- 显示 Sources 引用 test.md

### 5. 提交纠错

假设模型在某个问题上回答不够准确：

```bash
python -m src.cli correct \
  --session test-run \
  --wrong "MemoryQwen 只支持 PDF 导入" \
  --correct "MemoryQwen 支持 .txt 和 .md 格式的文档导入" \
  --failure-type "knowledge_error"
```

预期：
```
Correction recorded: True
  Error ID:     xxx...
  Failure Type: knowledge_error
  Strategy created: xxx...
```

### 6. 验证错误/策略注入

```bash
python -m src.cli chat "MemoryQwen 支持导入什么文件格式？" --session test-run2
```

预期：
- answer 提到 .txt 和 .md
- 显示 Error References（如果相关）
- 显示 Strategy References（如果命中策略库）

### 7. 验证重复 ingest 去重

```bash
# 再次导入同一目录
python -m src.cli ingest inbox/
```

预期：
```
Duplicates:    2  (之前导入的 chunks 被识别为重复)
Chunks stored: 0
```

## 故障排查

| 问题 | 检查 |
|------|------|
| Model Client: Unavailable | 确认模型服务正在运行，base_url 正确 |
| 中文回答乱码 | 确认终端使用 UTF-8 编码 |
| ingest 找不到文件 | 确认 inbox/ 目录在项目根目录下 |
| chat 无 Sources | retriever 可能未加载 chunk，尝试重启 |
