# CLI 命令参考

## health

检查系统状态：配置、Memory Store、Model Client。

```bash
python -m src.cli health
```

## ingest

导入文件或目录到 knowledge_store（一次性，不生成 task）。

```bash
python -m src.cli ingest inbox/
python -m src.cli ingest inbox/test.md
```

## job ingest

创建 ingestion 任务并执行（写入 task runtime，可查询状态）。

```bash
python -m src.cli job ingest inbox/
python -m src.cli job ingest inbox/ --guardian    # 启用 GPU 让路检查
```

## chat

发送聊天消息。模型会检索 knowledge_store + error_store + strategy_store。

```bash
python -m src.cli chat "MemoryQwen 的核心记忆是什么？"
python -m src.cli chat "问题" --session my-session
python -m src.cli chat "问题" --debug-memory       # 显示检索详情
```

`--debug-memory` 会显示：
- query, top_k, 各 store 计数
- prompt 包含哪些 section (local_sources / error_memory / strategy_memory / recent_chat)

## correct

提交用户纠错，写入 error_store，自动生成 strategy_store。

```bash
python -m src.cli correct \
  --wrong "错误的回答" \
  --correct "正确的回答" \
  --failure-type knowledge_error \
  --strategy "建议的策略"    # 可选
```

## memory stats

显示各 memory store 的记录计数。

```bash
python -m src.cli memory stats
```

输出示例:
```
knowledge_store      4
chat_messages        22
error_store          3
strategy_store       2
examples             0
```

## guardian status / json

查看 GPU 让路状态。

```bash
python -m src.cli guardian status    # 人类可读
python -m src.cli guardian json      # JSON 格式
```

## task list / status / pause / resume / cancel

管理后台任务。

```bash
python -m src.cli task list                    # 列出所有任务
python -m src.cli task status <task_id>        # 查看任务详情
python -m src.cli task pause <task_id>         # 暂停任务
python -m src.cli task resume <task_id>        # 恢复任务
python -m src.cli task cancel <task_id>        # 取消任务
python -m src.cli task pause <id> --reason gpu_game_mode
```

## profile show / validate / eval

模型 profile 管理。

```bash
python -m src.cli profile show                  # 显示当前 profile
python -m src.cli profile validate <path>       # 校验 profile 文件
python -m src.cli profile eval --model-id qwen-test --dry-run  # 预览评估用例
```
