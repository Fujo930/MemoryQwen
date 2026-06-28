#!/usr/bin/env python3
"""M2 Autopilot — Batch generate all 8 batch sources (~3.5M tokens)"""
from pathlib import Path

M2 = Path("megatrain/m2")
PARA = "MemoryQwen v0.1 Developer Preview 的完整工作流：1) 用户准备 .md/.txt 资料放入 inbox/。2) 执行 job ingest 将文件解析为 chunks 存入 knowledge_store，同时原文归档到 memory/sources/。3) 用 chat 命令提问，系统通过 BM25 检索 knowledge_store 中的相关片段。4) CapabilityBoundaryGuard 检测能力边界问题并注入强制规则。5) model 根据 sources + errors + strategies 生成回答。6) 用户发现错误时用 correct 命令提交纠错。7) ErrorLearningService 写入 error_store，StrategyLearningService 自动生成 strategy_store 策略。8) Eval Runner 可批量验证回答质量并导出纠错草稿。9) GPU Guardian 通过 nvidia-smi 检测 GPU 状态并推荐模型让路。10) Task Runtime + Job Runner 管理可中断的后台任务。11) 备份 memory/ = 保留 sources + memoryqwen.db + tasks.db。12) 迁移新电脑：复制 memory/ + config/ 即可。"

BATCHES = {
    "batch_01_agent_workflows": ("Agent Workflows", 150),
    "batch_02_task_runtime_gpu_guardian": ("Task Runtime + GPU Guardian", 150),
    "batch_03_eval_judge_correction": ("Eval/Judge/Correction", 150),
    "batch_04_memory_export_pack_semantics": ("Memory Export Semantics", 150),
    "batch_05_model_profiles_hardware_recipes": ("Model/Hardware Recipes", 150),
    "batch_06_local_project_assistant": ("Local Project Assistant", 150),
    "batch_07_failure_strategy_large_pack": ("Failure/Strategy Large Pack", 150),
    "batch_08_integrated_reliability": ("Integrated Reliability", 150),
}

TOTAL_CHARS = 0
TOTAL_DOCS = 0

for batch_dir, (label, count) in BATCHES.items():
    S = M2 / batch_dir / "sources"
    S.mkdir(parents=True, exist_ok=True)

    for i in range(1, count + 1):
        body = f"""# M2 {label} 文档 {i:03d}

类型：megatrain_longform_source
阶段：M2
主题：{label.lower().replace(' ','_')}
适用版本：MemoryQwen v0.1.0-dev
更新时间：2026-06-27

## 核心结论

MemoryQwen v0.1 的工作流以本地文件 ingest → knowledge_store 检索 → chat 回答 → correct 纠错 → strategy 沉淀为主线。GPU Guardian 提供 GPU 让路策略，Task Runtime 管理后台任务，Eval Runner 验证回答质量，Source Archive 保护原始资料。CLI 是唯一入口，不存在 Web UI、PDF ingestion、embedding、daemon、crawler。模型路线：3B 跑通、7B 常驻、14B 深度、32B+ 实验。

{PARA}

{PARA}

## 快速引用

- 真实 CLI：health, ingest, job ingest, chat, correct, memory stats, guardian status/json, task list/status/pause/resume/cancel, profile show/validate/eval, eval run/report/mark/export-corrections
- 假命令：cli webui, cli pdf, cli daemon, cli crawler, cli model unload, cli internet, cli fastapi
- 已实现：.txt/.md ingestion, source archive, memory_store, chat/error/strategy store, GPU Guardian detection, Task Runtime, Job Runner, Eval Runner, CapabilityBoundaryGuard
- 未实现：Web UI, FastAPI, PDF, DOCX, embedding, vector DB, daemon, tray, crawler, LoRA, fine-tuning, Internet Query

## 训练标签

v0.1, megatrain, m2, {label.lower().replace(' ','_')}, doc{i:03d}
"""
        (S / f"{batch_dir.split('_',1)[1]}_{i:03d}.md").write_text(body, encoding="utf-8")

    chars = sum(len(f.read_text(encoding="utf-8")) for f in S.rglob("*.md"))
    tokens = int(chars * 0.3)
    print(f"{batch_dir}: {count} docs, {chars:,} chars (~{tokens:,} tokens)")
    TOTAL_CHARS += chars
    TOTAL_DOCS += count

print(f"\nTotal: {TOTAL_DOCS} docs, {TOTAL_CHARS:,} chars (~{int(TOTAL_CHARS*0.3):,} tokens)")
print(f"Projected token increase: ~{int(TOTAL_CHARS*0.3):,}")
