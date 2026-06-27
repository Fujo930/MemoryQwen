# GPU Guardian 规则

来源：MemoryQwen 项目文档
资料类型：project_doc
更新时间：2026-06-27
主题：GPU Guardian 的四种模式、触发条件、推荐动作
关键词：GPU Guardian、normal、light_yield、game_mode、full_yield、让路、RTX 4080

## 核心结论

GPU Guardian 检测本机 GPU 负载，在用户玩游戏或使用创作软件时自动让 AI 让路。用户永远优先，AI 永远让路。

## 四种模式

### normal
- 触发条件：GPU 负载低，无游戏/创作进程
- 推荐动作：allow_14b、allow_background_ingestion、allow_index_refresh
- 含义：AI 全速运行

### light_yield
- 触发条件：VRAM 使用率 >= 55%
- 推荐动作：pause_background_ingestion、pause_index_refresh、prefer_7b
- 含义：暂停重型后台任务，轻度让路

### game_mode
- 触发条件：检测到游戏或创作软件进程，或 GPU 占用 >= 70%
- 推荐动作：pause_background_tasks、prefer_7b、disable_deep_reasoning
- 含义：用户正在玩游戏/创作，AI 只做轻量响应

### full_yield
- 触发条件：VRAM >= 85%
- 推荐动作：pause_all_ai_tasks、unload_models_if_supported、keep_memory_store_only
- 含义：GPU 几乎满载，AI 完全让路

## 优先级规则

full_yield > game_mode > light_yield > normal

高优先级条件满足时，忽略低优先级条件。

## 检测的进程

### 游戏进程
Cyberpunk2077.exe、cs2.exe、Minecraft.exe、GenshinImpact.exe、StarRail.exe、eldenring.exe

### 创作软件进程
blender.exe、resolve.exe、Premiere Pro.exe、AfterFX.exe、UnrealEditor.exe、Unity.exe、obs64.exe

## 当前版本限制

v0.1 只做检测和策略决策，不做真实模型卸载。检测通过 nvidia-smi 命令实现。

## 可测试问题

1. GPU Guardian 有哪四种模式？
2. game_mode 的触发条件是什么？
3. GPU Guardian 的最高优先级模式是什么？
4. 检测到 blender.exe 时应该进入什么模式？
5. GPU Guardian v0.1 能不能卸载模型？
6. light_yield 模式下推荐做什么？
