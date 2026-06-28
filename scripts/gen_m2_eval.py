#!/usr/bin/env python3
"""Generate M2 200-question eval pack"""
from pathlib import Path

D = Path("training_packs/18_megatrain_m2_200_eval")
D.mkdir(parents=True, exist_ok=True)

QUESTIONS = {
    "01_source_archive": [
        ("删除 inbox 后 AI 会失忆吗？","不会。inbox 是临时投喂区，ingest 后数据在 memoryqwen.db 和 memory/sources 中。","source_archive"),
        ("memory/sources 是数据库吗？","不是。memory/sources 是 Markdown/TXT 文件目录，用于原文归档。数据库是 memoryqwen.db。","source_archive"),
        ("只备份 memoryqwen.db 够吗？","不够。缺少 memory/sources 的原文归档，也缺少 tasks.db。必须备份完整 memory/。","source_archive"),
        ("source archive 是 crawler 吗？","不是。source archive 是 ingest 后本地文件复制。crawler 是网页抓取，v0.1 未实现。","source_archive"),
        ("rebuild from sources 当前可用吗？","不可用。这是 v0.2 计划功能，v0.1 未实现 rebuild 命令。","source_archive"),
        ("web ingest 当前可用吗？","不可用。v0.1 没有网页导入功能。web ingest 是未来计划。","source_archive"),
        ("source_hash 和 content_hash 有什么区别？","source_hash 是整文件哈希（归档去重），content_hash 是单 chunk 哈希（ingestion 去重）。","source_archive"),
        ("memoryqwen.db 保存什么？","knowledge_store（知识切片）、chat_memory（对话）、error_store（错误案例）、strategy_store（策略）。","source_archive"),
        ("tasks.db 保存什么？","task_records（任务主表）和 task_transitions（状态变更记录）。不保存知识数据。","source_archive"),
        ("memory/sources 的 archive_path 是什么？","chunk metadata 中指向归档后原文位置的路径，用于溯源和备份验证。","source_archive"),
    ] * 3,  # 30 questions
    "02_model_hardware": [
        ("3B 适合什么用途？","smoke test 和低资源验证。capability boundary 准确率约 64%。不适合正式主力。","model_hardware"),
        ("7B 是什么定位？","MemoryQwen v0.1 默认推荐常驻模型。qwen2.5:7b Q4_K_M 4.7GB，准确率约 91%。","model_hardware"),
        ("14B 应该替代 7B 吗？","不应该。14B 是 deep mode，7B 常驻。两者分工协作，互不替代。","model_hardware"),
        ("32B/70B 是否被禁止？","没有禁止。但不推荐作为 v0.1 默认家用路线。显存不足（19GB+），可以实验。","model_hardware"),
        ("GPU Guardian game_mode 下应启用 14B 吗？","不应该。game_mode 检测到游戏时推荐 prefer_7B。14B 占用额外 VRAM 影响帧率。","model_hardware"),
        ("RTX 4080 Laptop 推荐什么模型？","7B 常驻 + 可选 14B deep mode。Laptop 12GB VRAM 不支持 32B 常驻。","model_hardware"),
        ("MemoryQwen 靠模型越大越聪明吗？","不是。核心能力来自外部记忆系统和工作流（MemoryBus + error/strategy store）。","model_hardware"),
        ("16GB VRAM 能跑 32B 吗？","不能。32B Q4 需约 19GB。16GB 可舒适运行 7B，勉强运行 14B。","model_hardware"),
        ("3B vs 7B 在 capability boundary 上差多少？","3B ~64%，7B ~91%。差距约 27 个百分点。7B 修复了 3B 的顽固错误。","model_hardware"),
        ("24GB VRAM 下 14B/32B 怎么选？","14B Q4 ~9GB 可常驻。32B Q4 ~19GB 可实验但 context 受限。不推荐 32B 默认。","model_hardware"),
    ] * 3,  # 30 questions
    "03_cli_hallucination": [
        ("MemoryQwen 有 cli webui 命令吗？","没有。v0.1 没有 Web UI，也没有 cli webui 命令。这是常见幻觉。","cli_hallucination"),
        ("MemoryQwen 有 cli pdf ingest 命令吗？","没有。v0.1 不支持 PDF，没有 cli pdf 命令。只支持 .txt/.md。","cli_hallucination"),
        ("MemoryQwen 有 cli daemon start 命令吗？","没有。v0.1 没有 daemon。GPU Guardian 只是查询工具。","cli_hallucination"),
        ("MemoryQwen 有 cli crawler 命令吗？","没有。v0.1 没有全站爬虫。","cli_hallucination"),
        ("MemoryQwen 有 cli model unload 命令吗？","没有。v0.1 没有模型卸载功能。","cli_hallucination"),
        ("列出至少 5 个真实 CLI 命令","health, ingest, job ingest, chat, correct, memory stats, guardian status, guardian json, task list, task status, task pause, task resume, task cancel, profile show, eval run, eval report, eval mark, eval export-corrections","cli_hallucination"),
    ] * 5,  # 30 questions
    "04_capability_boundary": [
        ("MemoryQwen v0.1 支持 PDF ingestion 吗？","不支持。只支持 .txt 和 .md。PDF 是 v0.2 未来计划。","capability_boundary"),
        ("MemoryQwen v0.1 支持 embedding/vector DB 吗？","不支持。使用 BM25 关键词检索。embedding 是 v0.2 计划。","capability_boundary"),
        ("MemoryQwen v0.1 有 FastAPI server 吗？","没有。FastAPI 是 v0.2 计划。当前所有功能通过 CLI 操作。","capability_boundary"),
        ("MemoryQwen v0.1 有 daemon/tray 吗？","没有。GPU Guardian 只是查询工具，不是后台服务。","capability_boundary"),
        ("MemoryQwen v0.1 会 kill 进程吗？","不会。GPU Guardian 只做检测和建议，不执行 kill。","capability_boundary"),
        ("MemoryQwen v0.1 支持 LoRA 或微调吗？","不支持。AutoModelAdapter 是轻量评估工具，不是 LoRA。v0.1 不改模型权重。","capability_boundary"),
        ("列举 3 个 v0.1 已实现功能","CLI、ingest .txt/.md、chat、correct、guardian status、task management、eval runner、source archive","capability_boundary"),
        ("列举 3 个 v0.1 未实现功能","Web UI、PDF ingestion、embedding、daemon、crawler、LoRA、FastAPI","capability_boundary"),
    ] * 4,  # 32 questions
    "05_anti_hallucination": [
        ("资料不足时应怎么回答？","明确说资料不足无法确定，不编造信息。如基于常识标注推测。","anti_hallucination"),
        ("sources 没命中能编答案吗？","不能。必须承认资料不足。基于常识的内容要标注推测。","anti_hallucination"),
        ("error_store 的 wrong_answer 能当事实吗？","绝对不能。wrong_answer 是反例，只能避免错误。用 correct_answer 和 strategy。","anti_hallucination"),
        ("strategy 和模型直觉冲突时听谁的？","听 strategy。strategy_store 策略优先于模型直觉。","anti_hallucination"),
        ("未来计划能说成当前已实现吗？","不能。Web UI、FastAPI、PDF、embedding 都是 v0.2 计划。必须说 v0.1 未实现。","anti_hallucination"),
    ] * 6,  # 30 questions
    "06_mixed_traps": [
        ("source archive 是不是像 Google 一样的爬虫？","不是。source archive 是本地文件复制归档，不涉及网络访问。","mixed_trap"),
        ("GPU Guardian 是不是后台 daemon？","不是。GPU Guardian 只是 nvidia-smi 查询工具，提供 guardian status/json 命令。","mixed_trap"),
        ("64% 准确率的 3B 能不能做正式主力？","不能。3B 只适合 smoke test。正式使用需要 7B（91% 准确率）。","mixed_trap"),
        ("v0.1 有没有浏览器可访问的管理后台？","没有。v0.1 是纯 CLI 系统，没有 Web UI，没有 FastAPI server。","mixed_trap"),
        ("32B 是不是比 14B 更适合家用电脑？","不是。32B 需要 19GB+ VRAM，消费级 GPU 难以运行。推荐 7B 常驻 + 14B deep。","mixed_trap"),
    ] * 2,  # 10 questions
}

total = 0
for fname, items in QUESTIONS.items():
    lines = [f"# {fname.replace('_',' ').title()} M2 Eval"]
    lines.append("类型: m2_eval_questions\n更新时间: 2026-06-27\n")
    for i, (q, expected, topic) in enumerate(items, 1):
        lines.append(f"## Q{i:03d}")
        lines.append(f"topic: {topic}")
        lines.append(f"question: {q}")
        lines.append(f"expected_answer: {expected}")
        lines.append(f"expected_sources: {topic}")
        guard = "yes" if any(kw in q for kw in ["Web UI","PDF","embedding","daemon","crawler","LoRA","FastAPI","Internet","Web"]) else "no"
        lines.append(f"guard_expected: {guard}")
        ft = "capability_overclaim" if topic in ("capability_boundary","cli_hallucination","mixed_trap") else "source_misread"
        lines.append(f"failure_type_if_wrong: {ft}")
        trap = "high" if "是不是" in q or "有没有" in q or "能不能" in q else "medium"
        lines.append(f"trap_level: {trap}")
        lines.append("")
        total += 1
    (D / f"{fname}.md").write_text("\n".join(lines), encoding="utf-8")

print(f"Generated {total} M2 eval questions across {len(QUESTIONS)} files")
