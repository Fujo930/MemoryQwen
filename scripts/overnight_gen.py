#!/usr/bin/env python3
"""Overnight Autopilot — Generate M1 Batches 03, 04, 05"""
from pathlib import Path

MEGA = Path("megatrain")
BASE_LINE = """MemoryQwen v0.1 的实际功能边界。v0.1 没有 Web UI、没有 Internet Query、没有 PDF ingestion、没有 embedding/vector DB、没有 daemon/tray、没有 crawler、没有 LoRA/微调、没有 model unload。v0.1 有 CLI、有 ingest .txt/.md、有 chat、有 correct、有 memory stats、有 guardian、有 task management、有 eval runner。不要把未来计划说成已实现。不存在的 CLI 命令包括：cli webui, cli pdf, cli daemon, cli crawler, cli model unload, cli internet, cli fastapi, cli rebuild。"""

BATCHES = {
    "m1_cli_hallucination_extreme": {
        "tag": "cli_hallucination",
        "real_cli": "health, ingest, job ingest, chat, correct, memory stats, guardian status, guardian json, task list/status/pause/resume/cancel, profile show/validate/eval, eval run/report/mark/export-corrections",
        "fake_cli": "cli webui, cli pdf ingest, cli daemon start, cli model unload, cli crawler, cli internet, cli fastapi, cli web search, cli rebuild, cli tray",
    },
    "m1_capability_boundary_extreme": {
        "tag": "capability_boundary",
        "implemented": ".txt/.md ingestion, source archive, memory_store, chat memory, error_store, strategy_store, GPU Guardian status/json, Task Runtime, Job Runner, Eval Runner, Correction Export, Capability Boundary Guard",
        "not_implemented": "Web UI, FastAPI, Internet Query, PDF ingestion, DOCX ingestion, embedding/vector DB, daemon/tray, automatic model unload, kill process, crawler, LoRA, fine-tuning",
    },
    "m1_anti_hallucination_extreme": {
        "tag": "anti_hallucination",
        "rules": "资料不足时说无法确定。source 未命中时不编造。error_store 是反例库不是事实库。strategy_store 是策略库不是资料库。不编造 CLI。不编造 benchmark。不编造 release 状态。不把计划说成已完成。区分本地记忆、归档、数据库、训练资料。",
    },
}

PARA = BASE_LINE + " " + BASE_LINE + " " + BASE_LINE

for batch_name, data in BATCHES.items():
    S = MEGA / batch_name / "sources"
    S.mkdir(parents=True, exist_ok=True)

    for i in range(1, 81):
        if batch_name == "m1_cli_hallucination_extreme":
            title = f"CLI Hallucination Elimination 文档 {i:03d}：{'真实命令' if i%2==1 else '伪命令纠正'}"
            body = f"""# {title}

类型：megatrain_longform_source
阶段：M1 Batch 03
主题：cli_hallucination
更新时间：2026-06-27

## 核心结论

{data['real_cli'] if i%2==1 else data['fake_cli']}

{chr(10).join([' '.join(PARA.split()[:50]) for _ in range(8)])}

## 对照表

| 真实 CLI | 伪命令 |
|-----------|--------|
| health | cli webui |
| ingest | cli pdf |
| chat | cli daemon |
| correct | cli crawler |
| guardian status | cli model unload |
| task list | cli internet |
| eval run | cli fastapi |

## 训练标签
v0.1, megatrain, m1, cli, doc{i:03d}
"""
        elif batch_name == "m1_capability_boundary_extreme":
            title = f"Capability Boundary Extreme 文档 {i:03d}：{'已实现' if i%2==1 else '未实现'}"
            body = f"""# {title}

类型：megatrain_longform_source
阶段：M1 Batch 04
主题：capability_boundary
更新时间：2026-06-27

## 核心结论

v0.1 {'已实现：' + data['implemented'] if i%2==1 else '未实现：' + data['not_implemented']}

{chr(10).join([' '.join(PARA.split()[:50]) for _ in range(8)])}

## 训练标签
v0.1, megatrain, m1, capability, doc{i:03d}
"""
        else:
            title = f"Anti-Hallucination Extreme 文档 {i:03d}：{'不确定表达' if i%3==0 else ('反例处理' if i%3==1 else '不编造')}"
            body = f"""# {title}

类型：megatrain_longform_source
阶段：M1 Batch 05
主题：anti_hallucination
更新时间：2026-06-27

## 核心结论

{data['rules']}

{chr(10).join([' '.join(PARA.split()[:50]) for _ in range(8)])}

## 训练标签
v0.1, megatrain, m1, anti_hallucination, doc{i:03d}
"""
        (S / f"{batch_name.replace('m1_','')}_{i:03d}.md").write_text(body, encoding="utf-8")

    total = sum(len(f.read_text(encoding="utf-8")) for f in S.rglob("*.md"))
    print(f"{batch_name}: 80 docs, {total:,} chars (~{int(total*0.3):,} tokens)")

print("\nAll 3 batches generated: 240 docs total")
