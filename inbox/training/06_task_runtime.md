# Task Runtime 和 Job Runner

来源：MemoryQwen 项目文档
资料类型：project_doc
更新时间：2026-06-27
主题：Task Runtime、Job Runner、任务状态机、可中断任务
关键词：TaskRuntime、JobRunner、ingestion job、任务队列、SQLiteTaskStore

## 核心结论

Task Runtime 提供任务状态机，支持 pending → running → paused/completed/failed/cancelled 的完整生命周期。Job Runner 负责任务执行，支持 checkpoint 检查和 Guardian 集成。

## 任务状态机

```
pending → running → completed
  ↓         ↓  ↓
  ↓         ↓  → failed
  ↓         ↓
  ↓         → paused → running
  ↓
  → cancelled
```

终态（completed/failed/cancelled）不可再转换。

## 任务类型

ingestion、index_refresh、profile_eval、model_chat、error_learning、strategy_learning、embedding、reasoning、custom

## SQLiteTaskStore

- 持久化存储任务状态到 memory/tasks.db
- 程序重启后可查询之前的任务
- 支持按 status 和 task_type 过滤

## Job Runner

- FakeJob：用于测试的可中断 job
- IngestionDirectoryJob：目录导入 job（通过 subprocess 调用 CLI ingest）
- checkpoint：每完成一步检查任务状态，若 paused/cancelled 则停止
- Guardian checkpoint：checkpoint + GPU Guardian 检查

## CLI 命令

```bash
python -m src.cli job ingest inbox/           # 创建并运行 ingestion 任务
python -m src.cli task list                    # 列出所有任务
python -m src.cli task status <id>             # 查看任务详情
python -m src.cli task pause <id>              # 暂停任务
python -m src.cli task resume <id>             # 恢复任务
python -m src.cli task cancel <id>             # 取消任务
```

## 可测试问题

1. Task Runtime 的任务状态机有哪些状态？
2. 哪些状态是终态，不能再转换？
3. SQLiteTaskStore 做什么用？
4. IngestionDirectoryJob 执行时能否被暂停？
5. job ingest 和 ingest 命令有什么区别？
6. 如何查看所有任务列表？
