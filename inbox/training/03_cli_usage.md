# MemoryQwen CLI 使用说明

来源：MemoryQwen 项目文档
资料类型：project_doc
更新时间：2026-06-27
主题：CLI 全部命令、参数、使用场景
关键词：CLI、health、ingest、chat、correct、memory stats、guardian、task、profile

## 核心结论

MemoryQwen 通过命令行界面 (CLI) 操作。所有命令使用 `python -m src.cli` 作为入口。

## 全部命令

### health
检查系统状态：配置、Memory Store、Model Client。
```bash
python -m src.cli health
```

### ingest
导入文件或目录到 knowledge_store（一次性）。
```bash
python -m src.cli ingest inbox/
```

### job ingest
创建后台 ingestion 任务（写入 task runtime，可查询状态）。
```bash
python -m src.cli job ingest inbox/
```

### chat
发送聊天消息。默认只显示回答。加 `--debug-memory` 显示检索详情。
```bash
python -m src.cli chat "问题"
python -m src.cli chat "问题" --debug-memory
python -m src.cli chat "问题" --session my-session
```

### correct
提交用户纠错，写入 error_store，自动生成 strategy_store。
```bash
python -m src.cli correct --wrong "错误回答" --correct "正确回答" --failure-type "错误类型"
```

### memory stats
显示各 memory store 的记录计数。
```bash
python -m src.cli memory stats
```

### guardian status
查看 GPU 让路状态。
```bash
python -m src.cli guardian status
python -m src.cli guardian json
```

### task
管理后台任务。
```bash
python -m src.cli task list
python -m src.cli task status <task_id>
python -m src.cli task pause <task_id>
python -m src.cli task resume <task_id>
python -m src.cli task cancel <task_id>
```

### profile
模型 profile 管理。
```bash
python -m src.cli profile show
python -m src.cli profile validate <path>
```

### 启动脚本（Windows）
双击 `scripts/start_windows.bat` 进入交互聊天模式。输入 `/exit` 退出。

## 常用错误类型（correct 命令）

- source_miss：没有命中资料
- source_misread：命中了资料但读错
- hallucination：编造不存在内容
- wrong_memory_type：混淆 knowledge/error/strategy/chat
- reasoning_error：推理错误
- small_model_confusion：小模型把反例当事实
- citation_error：引用错误

## 可测试问题

1. MemoryQwen 的 CLI 入口是什么？
2. 如何查看 memory store 的统计信息？
3. chat 命令的 --debug-memory 参数有什么作用？
4. correct 命令需要哪些参数？
5. 如何在 Windows 上启动交互聊天？
6. 列出 5 种常用的 correct failure_type。
