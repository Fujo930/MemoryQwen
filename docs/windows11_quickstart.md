# Windows 11 快速启动

## 前提

- Windows 11 (23H2 或更新)
- Python 3.11+
- Git Bash 或 PowerShell

## 1. 安装 Python

从 https://www.python.org/downloads/ 下载安装。

确保 `python` 和 `pip` 在 PATH 中：

```bash
python --version  # 应显示 3.11+
pip --version
```

## 2. 安装依赖

```bash
cd MemoryQwen
pip install -r requirements.txt
```

## 3. 安装模型服务

### 选项 A: Ollama (推荐，最简单)

```bash
# 下载安装 Ollama
# https://ollama.com/download/windows

# 拉取模型
ollama pull qwen2.5:7b
# 或使用已有小模型
ollama pull qwen2.5-coder:3b
```

### 选项 B: LM Studio

1. 下载 LM Studio: https://lmstudio.ai/
2. 加载模型
3. 开启 Local Server (默认端口 1234)

## 4. 配置

编辑 `config/default.yaml`:

**Ollama:**
```yaml
model_client:
  provider: "ollama"
  base_url: "http://localhost:11434"
  model: "qwen2.5:7b"
```

**LM Studio:**
```yaml
model_client:
  provider: "lm_studio"
  base_url: "http://localhost:1234/v1"
  model: "your-model-name"
```

## 5. 验证环境

```bash
# 运行所有测试
python -m pytest tests/ -q

# 健康检查
python -m src.cli health
```

输出应包含:
```
✓ Config: MemoryQwen v0.1.0
✓ Memory Store: OK
✓ Model Client: OK
```

## 6. 创建示例资料

```bash
mkdir inbox

cat > inbox/test.md << 'EOF'
# MemoryQwen 介绍
MemoryQwen 是一个运行在本地电脑上的 AI agent 系统。
它支持文档导入、关键词检索、错误学习和策略沉淀。
```

## 7. 导入资料

```bash
python -m src.cli job ingest inbox/
```

## 8. 首次聊天

```bash
python -m src.cli chat "MemoryQwen 支持什么功能？" --debug-memory
```

## 9. 纠错 + 策略生成

```bash
python -m src.cli correct \
  --wrong "MemoryQwen 不支持文档" \
  --correct "MemoryQwen 支持 .txt 和 .md 导入" \
  --failure-type knowledge_error
```

## 10. 验证 GPU Guardian

```bash
python -m src.cli guardian status
python -m src.cli guardian json
```

## 11. 查看任务

```bash
python -m src.cli task list
```

## 下一步

- [CLI 命令参考](cli_reference.md)
- [配置参考](config_reference.md)
- [故障排除](troubleshooting.md)
