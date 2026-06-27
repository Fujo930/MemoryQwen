# 06_task_runtime Answer Key

- Task Runtime 定位: TaskRuntimeService 是任务状态管理系统。所有后台任务通过它管理生命周期。它是状态账本，不是执行器。
- TaskRecord 字段: task_id, task_type, title, status, progress_current, progress_total, progress_message, 时间戳, pause_reason, error_message,
- 状态机规则: pending→running, running↔paused, running→completed/failed, pending/running/paused→cancelled。completed/failed/cancelled 是
- TaskTransition 记录: 每次状态转换记录 from_status, to_status, reason, timestamp。存储在 task_transitions 表中。
- SQLiteTaskStore: 持久化任务状态到 memory/tasks.db。跨进程可查询。支持 add/get/update/list/delete/count。
- BackgroundJobRunner: Job 执行器。支持 checkpoint 和 guardian_checkpoint。任务被暂停/取消时停止执行。
- Job checkpoint 机制: checkpoint(context) 更新进度并检查状态：paused→停止返回paused, cancelled→停止返回cancelled, running→继续。
- IngestionDirectoryJob: 目录摄入 Job。通过 subprocess 调用 CLI ingest。每处理一个文件前 checkpoint。支持暂停/取消。
- CLI task/job 命令: job ingest 创建 ingestion 任务。task list/status/pause/resume/cancel 管理任务。