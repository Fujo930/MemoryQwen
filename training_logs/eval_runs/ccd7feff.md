# Eval Run Report

## Summary
- run_id: ccd7feff
- total_questions: 10
- correct: 0
- partial: 0
- wrong: 0
- unjudged: 10
- source_hit_rate: 0.0%
- guard_trigger_rate: 50.0%

## Topic Breakdown

| topic | total | correct | partial | wrong | unjudged |
|-------|-------|---------|---------|-------|----------|
| 05 | 2 | 0 | 0 | 0 | 2 |
| 06 | 2 | 0 | 0 | 0 | 2 |
| 03 | 2 | 0 | 0 | 0 | 2 |
| 04 | 2 | 0 | 0 | 0 | 2 |
| 01 | 2 | 0 | 0 | 0 | 2 |

## Results

### Q2604 (05)
- question: wrong_answer 能不能当事实引用？
- expected: 绝对不能。wrong_answer 是反例。应用 correct_answer 和 strategy 指导回答。
- answer: 根据当前本地资料不能确定。

不过可以明确的是，error_store 中的 wrong_answer 是反例，绝对不能当作事实使用。模型如果复述 wrong_answer，说明它可能把反例当成权威信息了，这是不正确的做法。在回答问题时应依赖 correct_answer 和 strategy。[S1][S2]
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\05_correction_system.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\04_error_strategy\source_wrong_answer_is_counterexample.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\10_anti_hallucination\source_sources_discipline.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\08_advanced_behavior.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\08_advanced_behavior.md
- source_hit: False
- guard_triggered: True
- judgement: correct_candidate (Heuristic: 11/15 concepts matched)

### Q8090 (06)
- question: nvidia-smi 不可用时 Guardian 返回什么？
- expected: Guarding 系统不可用时返回 normal 模式，available=false，不报错。
- answer: 当 `nvidia-smi` 不可用时，Guardian 将返回 `available=false`，并且模式会自动设置为 `normal`。[S1] 和 [S3] 中有详细说明。
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\source_nvidia_smi_detection.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\answer_key.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\source_guardian_positioning.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\09_windows11_deployment\source_common_win_issues.md
- source_hit: False
- guard_triggered: False
- judgement: partial_candidate (Heuristic: 8/15 concepts — partial)

### Q3572 (03)
- question: guardian status 输出什么？
- expected: GPU 模式、GPU 名称、VRAM 占用、利用率、温度、匹配进程、推荐动作。
- answer: `guardian status` 命令会输出 GPU 让路的状态信息。具体命令的执行结果可能会包含当前分配给不同任务的 GPU 使用情况等详细信息。你可以通过以下命令查看：

```bash
python -m src.cli guardian status
```

这将帮助你了解 GPU 资源的使用状态。[S2] 提供了这个命令的具体用法参考。
- sources: inbox\中文测试.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\03_cli_usage.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\06_task_runtime.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\09_capability_boundaries.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\08_model_hardware_routes\trap_questions.md
- source_hit: False
- guard_triggered: False
- judgement: unjudged (Insufficient confidence for auto-judge)

### Q2748 (03)
- question: profile eval --dry-run 的作用？
- expected: 只打印评估问题不调用模型，用于预览测试用例。
- answer: `profile eval --dry-run` 命令用于在不实际修改模型权重的情况下，评估模型的性能或配置。通过使用 `--dry-run` 选项，可以测试某些配置或策略是否有效，而不会对实际模型产生影响。

在这个例子中，“profile”命令主要用于管理模型的 profile，而 `eval` 子命令则用于评估这些配置的效果。`--dry-run` 参数确保了在评估过程中不会进行任何不可逆的操作。

根据已有的信息，这里没有具体的引用来源，但可以推测这是基于 CLI 指令的一个常见用法。[S1] 中提到的 profile 命令包括 `show/validate/eval` 等子命令，进一
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\02_cli_mastery\source_profile.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\03_cli_usage.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\06_task_runtime.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\09_capability_boundaries.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\03_capability_boundaries\source_implemented.md
- source_hit: False
- guard_triggered: False
- judgement: unjudged (Insufficient confidence for auto-judge)

### Q2536 (05)
- question: 复测纠错的作用？
- expected: 验证 error/strategy 是否注入 prompt，确认模型不再重复相同错误。
- answer: 复测纠错的主要作用包括：

1. **验证修正效果**：通过执行 `correct` 命令后重新与模型进行交互（chat），确保错误已经被正确修正。
2. **确认不再重复错误**：在完成复测后，再次检查错误是否仍然存在，以防止未来出现同样的问题。
3. **完善策略存储**：通过验证和更新 `strategy_store` 中的记录，确保模型能够在遇到类似情况时给出正确的回答。

具体步骤如下：
1. 执行 `correct` 命令来纠正特定的错误或知识缺陷。
2. 检查 `strategy_store` 确认新的策略已经被正确保存。
3. 使用相似的问题进行复测聊天，确保模型能够准确地提供
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\04_error_strategy\trap_questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\04_error_strategy\source_correction_retest.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\04_error_strategy\questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\04_error_strategy\answer_key.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\07_common_errors.md
- source_hit: False
- guard_triggered: False
- judgement: partial_candidate (Heuristic: 9/19 concepts — partial)

### Q5563 (04)
- question: v0.1 会 kill 游戏进程吗？
- expected: 不会。v0.1 不 kill 任何进程。
- answer: 根据当前本地资料不能确定是否会kill游戏进程。MemoryQwen 的 GPU Guardian 模式会在特定条件下暂停后台任务，但并未明确说明是否会kill游戏进程。需要更多具体信息来确认此行为。[S2] 和 [S3] 中提到的 game_mode 和 normal 模式主要关注于暂停或允许某些进程运行以优化 GPU 负载，但这并不直接表明会杀死游戏进程。
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\09_capability_boundaries.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\source_game_mode.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\04_gpu_guardian.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\source_normal_mode.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\answer_key.md
- source_hit: False
- guard_triggered: True
- judgement: partial_candidate (Heuristic: 2/6 concepts — partial)

### Q7292 (06)
- question: GPU Guardian 会 kill 进程吗？
- expected: 不会。v0.1 不 kill 任何进程。Guardian 只检测和建议。
- answer: 根据当前本地资料不能确定此功能的具体实现情况。不过，基于已有的信息，Guardian v0 不会自动卸载模型或 kill 进程。它主要是通过 nvidia-smi 查询 GPU 状态并提供策略建议。[S2][S3]
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\09_capability_boundaries.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\source_not_implemented_boundary.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\answer_key.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\09_capability_boundaries.md
- source_hit: False
- guard_triggered: True
- judgement: partial_candidate (Heuristic: 5/12 concepts — partial)

### Q9163 (01)
- question: 删除 inbox 原文件后 chat 还能检索吗？为什么？
- expected: 能。ingest 后资料已存入 memoryqwen.db(切片)和 memory/sources/(原文)。inbox 是临时投喂区。
- answer: 删除 inbox 原文件后聊天还能进行检索。这是因为 ingestion (ingest) 过程将文件解析并存入 `memory/sources` 和内部数据库 `memoryqwen.db` 中。即使原始的 inbox 文件被删除，已经处理过的资料依然存在于正式存储中，因此不会影响基于这些资料的 chat 检索。

具体来说，在 ingest 之后，MemoryQwen 将文件信息和内容解析入库，并且用户可以清理 inbox 目录而不会丢失已归档资料。这一机制确保了即使 inbox 文件被删除，已有资料依然可以通过 chat 进行检索。[S1]
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\07_source_archive_backup\source_delete_inbox_ok.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\07_source_archive_backup\trap_questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\07_source_archive_backup\questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\02_memory_system.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\07_source_archive_backup\answer_key.md
- source_hit: False
- guard_triggered: False
- judgement: partial_candidate (Heuristic: 8/17 concepts — partial)

### Q4207 (04)
- question: v0.1 有后台 daemon 吗？
- expected: 没有。GPU Guardian 只是查询工具，不是 daemon。
- answer: 根据当前本地资料不能确定。

不过，基于已有的信息，可以推断 MemoryQwen v0.1 可能不会包含后台 daemon。在功能对照表中提到，“后台 daemon”未实现 [S3]。但是为了确保准确性，请查阅更多相关文档或等待官方更新以获得明确答案。
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\09_capability_boundaries.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\06_task_runtime\source_task_runtime_positioning.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\inbox\training\09_capability_boundaries.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\02_cli_mastery\source_job_ingest.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\06_task_runtime\questions.md
- source_hit: False
- guard_triggered: True
- judgement: partial_candidate (Model expressed uncertainty — may be valid anti-hallucination)

### Q4469 (01)
- question: Source Archive 是否依赖网络？
- expected: 不依赖。Source Archive 是纯本地文件复制操作，不需要网络连接。
- answer: 根据当前本地资料不能确定。[S2] 中提到 MemoryQwen 支持 memory/sources 作为原始资料归档，但未明确说明其是否依赖网络。[S1][S3][S4][S5] 等资料片段与此问题无关或信息不足。
- sources: C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\06_task_runtime\trap_questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\07_source_archive_backup\trap_questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\05_gpu_guardian\trap_questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\09_windows11_deployment\trap_questions.md, C:\Users\hooya\Desktop\新建文件夹\MemoryQwen\training_packs\08_model_hardware_routes\trap_questions.md
- source_hit: False
- guard_triggered: True
- judgement: partial_candidate (Model expressed uncertainty — may be valid anti-hallucination)

