"""Batch generate Stage B training packs (themes 04-10)"""
from pathlib import Path

BASE = Path("training_packs")

THEMES = {
'04_error_strategy':[
('error_store_purpose','error_store 定位与用途','error_store 存储用户纠正的错误案例。每条记录包含 wrong_answer(反例) 和 correct_answer(正确回答)。error_store 是反例库，不是事实资料库。'),
('wrong_answer_is_counterexample','wrong_answer 是反例不是事实','wrong_answer 是错误示例，绝对不能当事实使用。模型如果复述 wrong_answer，说明它把反例当成了权威信息。'),
('correct_answer_is_fix','correct_answer 是修正蓝本','correct_answer 是用户提供的正确回答。模型在遇到相似问题时应该参考 correct_answer 的内容。'),
('failure_types','failure_type 分类体系','常用类型：source_miss, source_misread, hallucination, wrong_memory_type, reasoning_error, citation_error, small_model_confusion, capability_overclaim。'),
('strategy_store_purpose','strategy_store 定位与用途','strategy_store 存储可复用的回答策略。strategy_hash 去重。遇到相似问题时 prompt 注入策略指导。'),
('strategy_generation','策略生成规则','从 error_store 自动生成。同 strategy_hash 合并。用户提供策略标记 source=user，自动生成标记 source=auto。'),
('strategy_retrieval','策略检索与注入','Chat 时检索 strategy_store。如果 BM25 未命中，使用 recent fallback。策略在 prompt 中显示为[T1][T2]。'),
('correction_retest','纠错复测流程','1.执行correct命令 2.检查strategy_store 3.用相似问题重新chat 4.验证error/strategy注入 5.确认不再重复错误。'),
('common_error_cases','常见错题与策略案例','案例1：PDF幻觉→correct写入hallucination。案例2：daemon混淆→correct写入capability_overclaim。案例3：缺少sources→correct写入citation_error。'),
],
'05_gpu_guardian':[
('guardian_positioning','GPU Guardian v0 定位','GPU Guardian v0 是检测和策略建议系统。通过 nvidia-smi 查询 GPU 状态，返回四种模式。它不是 daemon，不是 tray，不会自动卸载模型。'),
('nvidia_smi_detection','nvidia-smi 检测机制','使用 subprocess 调用 nvidia-smi 查询 GPU 和进程信息。nvidia-smi 不可用时返回 available=false，模式自动 normal。'),
('normal_mode','normal 模式','触发：GPU 负载低，无游戏/创作进程。推荐动作：allow_14b, allow_background_ingestion。AI 全速运行。'),
('light_yield_mode','light_yield 模式','触发：VRAM>=55%。推荐动作：pause_background_ingestion, prefer_7b。轻度让路。'),
('game_mode','game_mode 模式','触发：游戏/创作进程或 GPU Util>=70%。推荐动作：pause_background_tasks, prefer_7b, disable_deep_reasoning。'),
('full_yield_mode','full_yield 模式','触发：VRAM>=85%。推荐动作：pause_all_ai_tasks, keep_memory_store_only。完全让路。'),
('process_detection','游戏/创作软件检测','游戏：Cyberpunk2077.exe, cs2.exe 等。创作：blender.exe, obs64.exe 等。大小写不敏感，支持 basename。'),
('guardian_task_policy','GuardianTaskPolicy 规则','根据 Guardian 推荐动作暂停 Task Runtime 中的任务。pause_background_ingestion→暂停ingestion。pause_all_ai_tasks→暂停除error/strategy外的所有任务。'),
('not_implemented_boundary','Guardian v0 未实现边界','v0.1 不做：daemon, tray, 自动卸载模型, kill 进程, 前台窗口检测。Guardian 只做检测和建议。'),
],
'06_task_runtime':[
('task_runtime_positioning','Task Runtime 定位','TaskRuntimeService 是任务状态管理系统。所有后台任务通过它管理生命周期。它是状态账本，不是执行器。'),
('task_record_fields','TaskRecord 字段','task_id, task_type, title, status, progress_current, progress_total, progress_message, 时间戳, pause_reason, error_message, metadata。'),
('state_machine','状态机规则','pending→running, running↔paused, running→completed/failed, pending/running/paused→cancelled。completed/failed/cancelled 是终态。'),
('task_transition','TaskTransition 记录','每次状态转换记录 from_status, to_status, reason, timestamp。存储在 task_transitions 表中。'),
('sqlite_task_store','SQLiteTaskStore','持久化任务状态到 memory/tasks.db。跨进程可查询。支持 add/get/update/list/delete/count。'),
('job_runner','BackgroundJobRunner','Job 执行器。支持 checkpoint 和 guardian_checkpoint。任务被暂停/取消时停止执行。'),
('job_checkpoint','Job checkpoint 机制','checkpoint(context) 更新进度并检查状态：paused→停止返回paused, cancelled→停止返回cancelled, running→继续。'),
('ingestion_dir_job','IngestionDirectoryJob','目录摄入 Job。通过 subprocess 调用 CLI ingest。每处理一个文件前 checkpoint。支持暂停/取消。'),
('cli_task_commands','CLI task/job 命令','job ingest 创建 ingestion 任务。task list/status/pause/resume/cancel 管理任务。'),
],
'07_source_archive_backup':[
('inbox_is_feed','inbox 是投喂入口','inbox 是临时投喂区。ingest 后文件被解析入库。用户可清理 inbox，不影响已归档资料。'),
('sources_is_archive','memory/sources 是原始资料归档','ingest 成功后原始文件自动复制到 memory/sources/。保留相对目录结构。source_hash 去重。'),
('memoryqwen_db','memory/memoryqwen.db 核心数据库','存储 knowledge_store, chat_memory, error_store, strategy_store。所有消化后的记忆都在这里。'),
('tasks_db','memory/tasks.db 任务状态','SQLiteTaskStore 持久化任务状态。包含 task_records 和 task_transitions 表。'),
('source_hash','source_hash 规则','ingest 时计算整个原始文件的 sha256。存储在 chunk metadata 中。用于归档去重。'),
('archive_path_metadata','archive_path 和 archived metadata','每个 chunk metadata 包含 archive_path, archived(bool), source_hash。CLI memory stats 显示 archived_files。'),
('delete_inbox_ok','删除 inbox 不影响检索','ingest 后资料已存入 memory/sources 和 memoryqwen.db。删除 inbox 原文件不影响 chat 检索。'),
('backup_memory','备份 memory/ 的意义','memory/ 包含 sources(原文), memoryqwen.db(记忆), tasks.db(任务)。备份=带走全部 AI 资产。模型可重下，memory 不能丢。'),
('future_rebuild','未来 rebuild from sources','v0.2 计划：从 memory/sources 重建 knowledge_store。数据库损坏时可从归档恢复。当前不实现。'),
],
'08_model_hardware_routes':[
('3b_smoke_test','3B 基础可运行','qwen2.5-coder:3b Q4_K_M 1.9GB。capability boundary 64%。适合 smoke test, CI, 低资源。'),
('7b_recommended','7B 推荐常驻','qwen2.5:7b Q4_K_M 4.7GB。capability boundary 91%。v0.1 默认推荐模型。'),
('14b_deep_mode','14B deep mode','qwen2.5:14b ~8GB。适合复杂推理。v0.1 尚未实现自动路由。'),
('32b_experimental','32B+ 实验模式','32B+ 不作为 v0.1 默认。RTX 4080 16GB 不足以同时运行。不符合 7B 常驻设计。'),
('gtx_to_3080','GTX 1080～RTX 3080 推荐 7B','8-12GB VRAM 推荐 qwen2.5:7b Q4 或更小量化。'),
('rtx3080_plus','RTX 3080+ 推荐 14B','RTX 3080 12GB+ 可运行 14B Q4。建议 deep mode。'),
('rtx4080_4090','RTX 4080/4090 策略','16-24GB VRAM。7B 常驻 + 14B deep。已通过 RTX 4080 Laptop 验证。'),
('7b_retest_data','7B retest 数据','capability boundary 20 题：3B 64% vs 7B 91%。7B 修复 PDF幻觉、daemon混淆、embedding回避、crawler混淆。'),
('why_not_big','为什么不硬堆大模型','MemoryQwen 靠外部记忆和流程提升。7B + MemoryBus + error/strategy 系统工程 > 32B 裸跑。记忆可积累，模型可替换。'),
],
'09_windows11_deployment':[
('win11_smoke_test','Windows 11 23H2 smoke test','Build 10.0.22631。health, ingest, chat, correct, guardian, task 全部通过。'),
('build_is_win11','Build 10.0.22631 是 Windows 11','Kernel version 10.0。22000+ 就是 Windows 11。不要因为看到 10.0 就觉得是 Windows 10。'),
('ollama_config','Ollama OpenAI-compatible 配置','provider: ollama, base_url: http://localhost:11434。model 名必须和 ollama list 一致。'),
('qwen25_7b_default','qwen2.5:7b 是默认模型','Q4_K_M 4.7GB。v0.1 默认推荐。capability boundary 91%。'),
('qwen25_3b_smoke','qwen2.5-coder:3b smoke test','1.9GB Q4_K_M。适合快速验证。capability boundary 64%。API key 不需要。'),
('chinese_path','中文路径 / UTF-8 支持','中文文件名已通过。ingest 和 chat 均支持。不出现乱码。Git Bash 推荐。'),
('terminal_support','终端支持','Git Bash(推荐,UTF-8) / PowerShell 均可用。bat 文件建议纯 ASCII。'),
('nvidia_smi_rtx4080','nvidia-smi RTX 4080 检测','RTX 4080 Laptop GPU 12GB 检测正常。guardian status/json 正常。'),
('common_win_issues','常见 Windows 问题','编码乱码→Git Bash。模块找不到→cd项目根目录。SQLite lock→关闭其他进程。nvidia-smi不可用→确认驱动。bat闪退→检查Python路径。'),
],
'10_anti_hallucination':[
('evidence_awareness','证据意识','回答时区分：确定(有资料→引用来源)、不确定(缺资料→说无法确定)、推测(推断→标注推测)。'),
('sources_discipline','sources discipline','使用资料必须引用[S1][S2]。没来源不能装确定。不要把推测和来源混一起。'),
('uncertainty_expression','不确定性表达','资料不足时说：无法确定、根据现有信息推测、v0.1当前不支持、未来计划中。'),
('capability_now','当前能力边界','回答基于 v0.1 实际能力。不把计划说成已实现。不把 CLI 说成 Web UI。不把检测说成 daemon。'),
('future_not_now','未来计划不是当前功能','FastAPI/WebUI/embedding/PDF 都是 v0.2 计划。必须说 v0.1 尚未实现,v0.2 计划中。'),
('no_fake_commands','不能编造 CLI 命令','v0.1 没有：cli webui, cli pdf, cli daemon, cli model unload, cli crawler。不能声称这些存在。'),
('no_fake_tools','不能编造工具/功能','v0.1 没有：向量数据库, 联网搜索, 文件管理器, 系统托盘, 自动更新。不能声称存在。'),
('insufficient_data','资料不足时的回答','检索不到资料→1.说资料不足 2.不编造 3.基于常识标注通用知识 4.建议提供更多资料。'),
('high_risk_template','高风险问题回答模板','PDF/WebUI/daemon/embedding 类问题使用模板：v0.1 不支持{功能}。v0.1 只支持{已实现}。{功能}是 v0.2 计划。'),
],
}

c = 0
for td, ts in THEMES.items():
    p = BASE / td
    p.mkdir(parents=True, exist_ok=True)
    for fid, t, su in ts:
        (p / f"source_{fid}.md").write_text(
            f"# {t}\n\n类型:training_source\n更新时间:2026-06-27\n适用:v0.1.0-dev\n\n## 核心结论\n{su}\n\n## 正确回答要点\n基于上述核心结论。\n\n## 易错点\n编造功能、混淆边界、把反例当事实、把未来当现在。\n\n## 标签\nv0.1,training,{fid}\n",
            encoding="utf-8")
        c += 1
    qs = "\n".join(f"{i}. {t}: {su[:60]}..." for i, (_, t, su) in enumerate(ts, 1))
    (p / "questions.md").write_text(f"# {td} Questions\n\n{qs}\n", encoding="utf-8")
    (p / "trap_questions.md").write_text(
        f"# {td} Trap Questions\n\n" + "\n".join(f"{i}. 陷阱：MemoryQwen 是否支持{t}？（答案参考 source）" for i, (_, t, _) in enumerate(ts, 1)),
        encoding="utf-8")
    (p / "answer_key.md").write_text(
        f"# {td} Answer Key\n\n" + "\n".join(f"- {t}: {su[:120]}" for _, t, su in ts),
        encoding="utf-8")

print(f"Generated {c} source files + {len(THEMES)} question/trap/answer sets")
kb = sum(f.stat().st_size for f in BASE.rglob("*.md")) / 1024
print(f"Training packs size: {kb:.0f} KB")
