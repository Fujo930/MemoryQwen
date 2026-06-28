#!/usr/bin/env python3
"""Generate M1 Grand QA Eval unified question pack with REAL expected answers"""
from pathlib import Path

D = Path("training_packs/17_megatrain_m1_grand_eval")
D.mkdir(parents=True, exist_ok=True)

# Real questions with real expected answers
SECTIONS = {
    "source_archive_m1_eval.md": [
        ("inbox 删除后 AI 会失忆吗？", "不会。inbox 是临时投喂区。ingest 后的数据在 memoryqwen.db（检索）和 memory/sources（归档）中。删除 inbox 不影响检索。", "source_archive"),
        ("memory/sources 是什么？", "memory/sources 是 ingest 成功后自动归档的原始 Markdown/TXT 文件目录。它是长期 AI 资产，与 memoryqwen.db 同等重要。不是数据库，不是 crawler。", "source_archive"),
        ("memoryqwen.db 保存什么？", "memoryqwen.db 是 SQLite 数据库。存储 knowledge_store（切片索引）、chat_memory（对话记录）、error_store（错误案例）、strategy_store（策略）。不等于原始文件归档。", "source_archive"),
        ("tasks.db 保存什么？", "tasks.db 是 SQLite 数据库。存储 task_records（任务主表）和 task_transitions（状态变更记录）。不保存 knowledge_store 数据。", "source_archive"),
        ("备份 memory/ 够不够？", "够。memory/ 包含 sources/（原文归档）、memoryqwen.db（检索索引和记忆）、tasks.db（任务状态）。备份 memory/ = 带走全部 AI 资产。", "source_archive"),
        ("只备份 inbox 够吗？", "不够。inbox 是临时投喂区，可能被用户清理。ingest 后的数据都在 memory/ 中。", "source_archive"),
        ("只备份 memoryqwen.db 够吗？", "不够。缺少 memory/sources/ 的原始资料归档。数据库损坏时无法从原文重建。也缺少 tasks.db。", "source_archive"),
        ("source archive 是不是 crawler？", "不是。source archive 是 ingest 后本地文件的复制归档。crawler 是从网页抓取内容，v0.1 未实现 crawler。source archive 不涉及任何网络访问。", "source_archive"),
        ("rebuild from sources 当前能用吗？", "不能。rebuild from sources 是 v0.2 计划功能，当前 v0.1 未实现。没有相关 CLI 命令。", "source_archive"),
        ("web ingest 当前能用吗？", "不能。v0.1 没有从网页导入的功能。source archive 只是本地文件归档。web ingest 是未来计划。", "source_archive"),
        ("source_hash 和 content_hash 有什么区别？", "source_hash 是整个原始文件的 sha256，用于归档去重。content_hash 是单个 chunk 的 hash，用于 ingestion 去重。两者不同。", "source_archive"),
        ("archive_path 是什么？", "archive_path 是 chunk metadata 中指向归档后原文位置的路径（memory/sources/...）。用于溯源和备份验证。", "source_archive"),
    ],
    "model_hardware_m1_eval.md": [
        ("3B 适合什么用途？", "3B 适合 smoke test 和低资源验证。qwen2.5-coder:3b Q4_K_M 1.9GB，capability boundary 准确率约 64%。不适合作为正式主力处理能力边界问题。", "model_hardware"),
        ("7B 是什么定位？", "7B 是 MemoryQwen v0.1 的默认推荐常驻模型。qwen2.5:7b Q4_K_M 4.7GB，capability boundary 准确率约 91%。适合日常聊天和资料检索。", "model_hardware"),
        ("14B 是什么定位？", "14B 是 deep mode 候选。适合复杂推理和长文档，但不替代 7B 常驻。需要 GPU Guardian 协同，应在 GPU 空闲时使用。", "model_hardware"),
        ("32B/70B 是否被禁止？", "没有被禁止。但 32B+ 不推荐作为 v0.1 默认家用路线。原因是显存不足（19GB+ Q4）、KV cache 受压、GPU Guardian 让路困难。可以实验但不推荐默认。", "model_hardware"),
        ("RTX 4080 Laptop 推荐什么模型？", "推荐 7B 常驻 + 可选 14B deep mode。Laptop 12GB VRAM 不支持 32B 常驻。MemoryQwen 已在 RTX 4080 Laptop 上实测通过。", "model_hardware"),
        ("14B 是否应该替代 7B？", "不应该。7B 延迟更低、显存更友好。14B 是 deep mode，在 GPU 空闲时按需使用。两者分工协作，互不替代。", "model_hardware"),
        ("GPU Guardian game_mode 下应启用 14B 吗？", "不应该。game_mode 检测到游戏/创作进程时，推荐 pause_background_tasks 和 prefer_7B。14B deep mode 占用约 8GB 额外 VRAM，影响游戏帧率。", "model_hardware"),
        ("MemoryQwen 是不是靠模型越大越聪明？", "不是。MemoryQwen 的核心能力来自外部记忆系统和工作流（MemoryBus + error_store + strategy_store），不是硬堆大模型。7B + 系统工程 > 32B 裸跑。", "model_hardware"),
        ("16GB VRAM 能跑 32B 吗？", "不能。32B Q4 需要约 19GB VRAM。16GB 下 7B（5GB）常驻很舒适，14B（9GB）深算模式勉强可用但不能同时游戏。", "model_hardware"),
        ("3B 和 7B 在 capability boundary 上差多少？", "3B 准确率约 64%，7B 约 91%。同一套 20 题测试，3B 有 PDF hallucination、daemon 混淆等顽固错误，7B 全部修复。差距约 27 个百分点。", "model_hardware"),
    ],
    "cli_hallucination_m1_eval.md": [
        ("MemoryQwen 有 cli webui 命令吗？", "没有。v0.1 没有 Web UI，也没有 cli webui 命令。所有操作通过 CLI（python -m src.cli）进行，包括 health chat ingest correct guardian task eval。", "cli_hallucination"),
        ("MemoryQwen 有 cli pdf ingest 命令吗？", "没有。v0.1 没有 PDF ingestion。只支持 .txt 和 .md 文件导入。命令行不包含 cli pdf 或 cli pdf ingest。", "cli_hallucination"),
        ("MemoryQwen 有 cli daemon start 命令吗？", "没有。v0.1 没有后台 daemon。GPU Guardian 只是 nvidia-smi 查询工具，不是常驻服务。不存在的命令包括 cli daemon start。", "cli_hallucination"),
        ("MemoryQwen 有 cli crawler 命令吗？", "没有。v0.1 没有全站爬虫。source archive 只是本地文件归档，不是 crawler。命令行不包含 cli crawler。", "cli_hallucination"),
        ("MemoryQwen 有 cli model unload 命令吗？", "没有。v0.1 没有自动模型卸载功能。GPU Guardian 只做检测和建议，不执行卸载操作。", "cli_hallucination"),
        ("列出现有的真实 CLI 命令（至少 5 个）", "health, ingest, job ingest, chat, correct, memory stats, guardian status, guardian json, task list, task status, task pause, task resume, task cancel, profile show, profile validate, profile eval, eval run, eval report, eval mark, eval export-corrections", "cli_hallucination"),
        ("MemoryQwen 有 Web UI 吗？", "没有。v0.1 是 Developer Preview，所有操作通过 CLI 进行。Web UI 是 v0.2 未来计划，不是当前功能。", "cli_hallucination"),
        ("MemoryQwen 有 Internet Query 吗？", "没有。v0.1 是完全本地系统。没有联网搜索功能。所有回答基于本地资料。", "cli_hallucination"),
        ("cli webui 是真的还是假的？", "假的。MemoryQwen v0.1 没有 cli webui 命令。这是常见幻觉。真实 CLI 命令包括 health chat ingest correct 等。", "cli_hallucination"),
        ("正确的 chat 命令格式是什么？", "python -m src.cli chat '问题'。可选 --session 指定会话 ID，--debug-memory 显示检索详情。默认只显示回答，不显示 debug 信息。", "cli_hallucination"),
    ],
    "capability_boundary_m1_eval.md": [
        ("MemoryQwen v0.1 支持 PDF ingestion 吗？", "不支持。v0.1 只支持 .txt 和 .md 文件导入。PDF ingestion 是 v0.2 未来计划。", "capability_boundary"),
        ("MemoryQwen v0.1 支持 embedding/vector DB 吗？", "不支持。v0.1 使用 BM25 关键词检索，没有 embedding 或向量数据库。embedding 是 v0.2 未来计划。", "capability_boundary"),
        ("MemoryQwen v0.1 有 FastAPI server 吗？", "没有。v0.1 当前没有 FastAPI server。FastAPI 是 v0.2 未来计划。当前所有功能通过 CLI 操作。", "capability_boundary"),
        ("MemoryQwen v0.1 有 daemon/tray 吗？", "没有。v0.1 没有后台 daemon，没有 Windows tray。GPU Guardian 只是查询工具。", "capability_boundary"),
        ("MemoryQwen v0.1 会 kill 进程吗？", "不会。v0.1 不会 kill 任何用户进程。GPU Guardian 只做检测和策略建议，不执行 kill 操作。", "capability_boundary"),
        ("MemoryQwen v0.1 支持 LoRA 或模型微调吗？", "不支持。v0.1 不修改模型权重。AutoModelAdapter 是轻量模型能力评估工具，不是 LoRA。v0.1 的训练是指资料训练而非权重训练。", "capability_boundary"),
        ("列举 3 个 v0.1 已实现的功能", ".txt/.md ingestion、chat、correct (纠错)、memory stats、guardian status、task management、eval runner、source archive。任选 3 个。", "capability_boundary"),
        ("列举 3 个 v0.1 未实现的功能", "Web UI、PDF ingestion、embedding/vector DB、daemon/tray、Internet Query、crawler、LoRA、FastAPI server。任选 3 个。", "capability_boundary"),
        ("Capability Boundary Guard 做什么？", "检测用户问题是否涉及 v0.1 能力边界。如果触发，在 prompt 中插入 10 条强制规则（high/medium/low 三级），防止模型 hallucinate 不支持的功能。", "capability_boundary"),
        ("AutoModelAdapter 是什么？", "轻量模型能力评估工具，用于 eval 模型 profile。不修改模型权重。不是 LoRA，不是微调。", "capability_boundary"),
    ],
    "anti_hallucination_m1_eval.md": [
        ("资料不足时 MemoryQwen 应怎么回答？", "明确说资料不足，无法确定。不编造信息。如果基于常识，标注通用知识。可建议用户提供更多资料。", "anti_hallucination"),
        ("sources 没命中时能不能凭常识编答案？", "不能。如果 sources 没命中，必须承认资料不足。不能编造。基于常识的内容要标注推测。", "anti_hallucination"),
        ("error_store 的 wrong_answer 怎么用？", "wrong_answer 是反例，绝对不能当事实引用。只能用于避免错误。回答时应使用 correct_answer 和 strategy 指导。", "anti_hallucination"),
        ("strategy_store 的优先级？", "strategy_store 的策略优先于模型直觉。如果策略和初始回答冲突，必须按策略修正。", "anti_hallucination"),
        ("未来计划的 Web UI 能不能说成当前已实现？", "不能。Web UI 是 v0.2 未来计划。v0.1 尚未实现。必须明确区分已实现和未来计划。", "anti_hallucination"),
        ("能不能编造不存在的 CLI 命令？", "不能。v0.1 不存在的命令包括 cli webui、cli pdf、cli daemon、cli crawler、cli model unload。不能声称这些命令存在。", "anti_hallucination"),
        ("[S]、[E]、[T] 分别代表什么？", "[S] 是本地资料来源（source），[E] 是错误记忆（error），[T] 是策略（strategy）。三种引用必须区分，不能混用。", "anti_hallucination"),
        ("遇到不确定的问题怎么回答？", "根据资料：给出答案 + 引用来源。资料不足：明确说无法确定。推测：标注推测，不装确定。", "anti_hallucination"),
        ("error_store 是不是事实库？", "不是。error_store 是错误案例库，存储用户纠正的反例。positive 事实在 knowledge_store 中。不要把反例当事实。", "anti_hallucination"),
        ("v0.1 能做 benchmark 吗？", "v0.1 有 Eval Runner（eval run/eval report/eval mark/export-corrections），可以进行本地验证。但没有标准化的公开 benchmark suite。不要把 eval runner 说成 benchmark 系统。", "anti_hallucination"),
    ],
    "mixed_traps_m1_eval.md": [
        ("我删除 inbox 后 MemoryQwen 是不是忘了所有东西？", "不会。inbox 是临时投喂区。数据在 memoryqwen.db（检索）和 memory/sources（归档）中。删除 inbox 不影响检索。这是最常见的误解之一。", "mixed_trap"),
        ("memoryqwen.db 是不是保存了所有原始 Markdown 文件？", "不是。memoryqwen.db 保存的是切片后的 chunks（用于检索），不是完整原始文件。原始 Markdown 文件在 memory/sources/ 中。", "mixed_trap"),
        ("32B 是不是比 14B 更适合家用？", "不是。32B 需要 19GB+ VRAM Q4，RTX 4080 Laptop 12GB 完全不可用。v0.1 推荐 7B 常驻 + 14B deep mode。32B 仅实验。", "mixed_trap"),
        ("GPU Guardian 是不是后台 daemon？", "不是。GPU Guardian v0 只是 nvidia-smi 查询工具。提供 guardian status 和 guardian json 两个 CLI 命令。不是 daemon。", "mixed_trap"),
        ("source archive 是不是自动抓网页的爬虫？", "不是。source archive 是 ingest 后本地文件的复制归档。不涉及任何网络访问。crawler 是 v0.1 未实现的功能。", "mixed_trap"),
        ("rebuild from sources 是不是 v0.1 当前功能？", "不是。rebuild from sources 是 v0.2 计划功能。v0.1 当前没有 rebuild 命令。不要声称它已可用。", "mixed_trap"),
        ("7B 是不是太弱了不够用？", "7B 是 v0.1 的默认推荐模型。capability boundary 准确率 91%，足够应对日常聊天和资料检索。MemoryQwen 的核心能力来自外部记忆系统，不是模型大小。", "mixed_trap"),
        ("如果我把 wrong_answer 当事实引用了怎么办？", "这是严重错误。wrong_answer 是反例，绝对不能当事实使用。应该使用 correct_answer。如果已经犯了这个错误，应该通过 correct 命令提交纠错。", "mixed_trap"),
        ("v0.1 是不是有一个 Web 管理后台可以浏览器访问？", "没有。v0.1 是纯 CLI 系统。没有 Web UI，没有 FastAPI server，没有浏览器管理后台。所有操作通过命令行。", "mixed_trap"),
        ("MemoryQwen 的 source archive 是不是像 Google 一样爬虫？", "不是。source archive 只是把用户导入的本地文件复制到 memory/sources/ 归档。和 Google 爬虫完全不同。v0.1 没有任何网络爬取功能。", "mixed_trap"),
    ],
}

total = 0
for fname, items in SECTIONS.items():
    lines = [f"# {fname.replace('.md','').replace('_',' ').title()}"]
    lines.append("类型: grand_eval_questions")
    lines.append("更新时间: 2026-06-27\n")
    for i, (q, expected, topic) in enumerate(items, 1):
        lines.append(f"## Q{i:03d}")
        lines.append(f"topic: {topic}")
        lines.append(f"question: {q}")
        lines.append(f"expected_answer: {expected}")
        lines.append(f"expected_sources: {topic}")
        lines.append(f"guard_expected: {'yes' if 'Web UI' in q or 'PDF' in q or 'embedding' in q or 'daemon' in q else 'no'}")
        lines.append(f"failure_type_if_wrong: {'capability_overclaim' if topic in ('capability_boundary','cli_hallucination','mixed_trap') else 'source_misread'}")
        lines.append(f"trap_level: {'high' if '混合' in q or '是不是' in q else 'medium'}")
        lines.append("")
        total += 1
    (D / fname).write_text("\n".join(lines), encoding="utf-8")

print(f"Generated {total} real eval questions across {len(SECTIONS)} files")
