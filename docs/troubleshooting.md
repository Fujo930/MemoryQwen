# 故障排除

## health 失败

**"Model Client: FAIL"**

1. 确认模型服务在运行:
   - Ollama: 任务栏有图标, `ollama list` 有输出
   - LM Studio: Local Server 已开启
2. 确认 `config/default.yaml` 中 `base_url` 正确
3. 确认 `model` 名与后端一致

```bash
# 检查模型列表
ollama list
# 测试端点
curl http://localhost:11434/api/tags
```

## Ollama 连接失败

- 确认 Ollama 在运行: 系统托盘有图标
- 手动启动: `ollama serve`
- 检查端口: `netstat -an | findstr 11434`

## base_url 错误

- Ollama: `http://localhost:11434`
- LM Studio: `http://localhost:1234/v1` (注意 `/v1`)
- llama.cpp: `http://localhost:8080/v1`

配置中 `provider` 和 `base_url` 要匹配。

## model 名称错误

Ollama model 名必须和 `ollama list` 输出一致:
```yaml
# ✅ 正确
model: "qwen2.5:7b"

# ❌ 错误
model: "qwen2.5-7b"
```

## 中文路径问题

如果中文文件名 ingest 失败:
1. 确保终端使用 UTF-8: `chcp 65001` (CMD)
2. Git Bash 默认支持 UTF-8
3. PowerShell 7+ 支持良好

## SQLite lock

如果看到 `database is locked`:
- 关闭其他正在运行的 MemoryQwen 进程
- 删除 `memory/*.db-journal` 文件
- `memory/*.db-wal` 是正常文件，不要删

## nvidia-smi 找不到

Guardian 依赖 `nvidia-smi`:
```bash
# 检查是否可用
nvidia-smi

# 如果找不到，确认 NVIDIA 驱动已安装
# 或在 config 中设置:
gpu_guardian:
  enabled: false
```

## guardian status unavailable

Guardian 输出 `GPU: unavailable`:
1. 确认 `nvidia-smi` 可用
2. 如果在笔记本电脑上，确认独显已启用
3. 如果无 NVIDIA GPU，这是正常的

## chat 没有 sources

1. 确认先导入了资料: `python -m src.cli job ingest inbox/`
2. 确认 `knowledge_store` 有数据: `python -m src.cli memory stats`
3. 提问要明确匹配资料内容（当前是 BM25 关键词检索）

## correct 没有生成 strategy

1. 确认 `enable_strategy_learning: true`
2. 查看 correct 输出中的 "Strategy" 行
3. 如果 "Strategy" 为空，尝试加 `--strategy` 参数

## task list 为空

如果使用 `store: "sqlite"`:
1. 确认 `memory/tasks.db` 存在
2. 如果切换了 store 类型，旧数据的 store 类型下看不到

如果使用 `store: "memory"`:
- 每次 CLI 进程重启后数据丢失（正常）

## pytest 失败

1. 清除缓存: `find . -name "__pycache__" -type d -exec rm -rf {} +`
2. 确认在项目根目录运行
3. Windows 下使用 Git Bash 而非 CMD

如果看到 `PermissionError` 关于 temp 目录，这是 Windows pytest cleanup 的已知问题，不影响测试结果。
