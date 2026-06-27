# 05_gpu_guardian Answer Key

- GPU Guardian v0 定位: GPU Guardian v0 是检测和策略建议系统。通过 nvidia-smi 查询 GPU 状态，返回四种模式。它不是 daemon，不是 tray，不会自动卸载模型。
- nvidia-smi 检测机制: 使用 subprocess 调用 nvidia-smi 查询 GPU 和进程信息。nvidia-smi 不可用时返回 available=false，模式自动 normal。
- normal 模式: 触发：GPU 负载低，无游戏/创作进程。推荐动作：allow_14b, allow_background_ingestion。AI 全速运行。
- light_yield 模式: 触发：VRAM>=55%。推荐动作：pause_background_ingestion, prefer_7b。轻度让路。
- game_mode 模式: 触发：游戏/创作进程或 GPU Util>=70%。推荐动作：pause_background_tasks, prefer_7b, disable_deep_reasoning。
- full_yield 模式: 触发：VRAM>=85%。推荐动作：pause_all_ai_tasks, keep_memory_store_only。完全让路。
- 游戏/创作软件检测: 游戏：Cyberpunk2077.exe, cs2.exe 等。创作：blender.exe, obs64.exe 等。大小写不敏感，支持 basename。
- GuardianTaskPolicy 规则: 根据 Guardian 推荐动作暂停 Task Runtime 中的任务。pause_background_ingestion→暂停ingestion。pause_all_ai_tasks→暂停除error/strategy外的所有任务。
- Guardian v0 未实现边界: v0.1 不做：daemon, tray, 自动卸载模型, kill 进程, 前台窗口检测。Guardian 只做检测和建议。