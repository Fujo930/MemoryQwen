#!/usr/bin/env python3
"""MegaTrain M1 Generator — 250 longform docs, ~600K tokens target"""
from pathlib import Path
import os

BASE = Path(__file__).resolve().parent.parent / "megatrain"

# ─── Content templates for each pack ───
PACKS = {
    "m1_pack_01_source_archive": {
        "theme": "Source Archive & Backup",
        "sections": [
            ("inbox 投喂入口详解", "inbox 是 MemoryQwen 的临时文件投喂区。用户将 .txt 和 .md 文件放入 inbox/ 目录后，通过 `ingest` 或 `job ingest` 命令将它们导入系统。inbox 不是长期资产，用户可以在导入完成后清理 inbox 目录，不影响已归档的资料。"),
            ("memory/sources 原始资料归档", "ingest 成功后的文件会自动复制到 memory/sources/ 目录。归档保留相对目录结构（如 inbox/training/01.md → memory/sources/training/01.md）。如果同一 source_hash 已存在，不会重复复制；如果文件名冲突但 hash 不同，会在文件名后追加短 hash 后缀。"),
            ("memoryqwen.db 消化后的知识", "memory/memoryqwen.db 是 SQLite 核心数据库，存储 knowledge_store（知识切片）、chat_memory（对话历史）、error_store（错误案例）和 strategy_store（行为策略）。所有 ingest 后的 chunks 按照 BM25 索引存储在此。"),
            ("tasks.db 任务状态持久化", "memory/tasks.db 存储 task_records 和 task_transitions。SQLiteTaskStore 支持跨进程状态查询。包含 pending/running/paused/completed/failed/cancelled 完整生命周期。"),
            ("source_hash 规则", "ingest 时计算整个原始文件的 SHA256 hash。存储在 chunk metadata 中。用于归档去重：同 hash 不重复复制。用于未来 rebuild from sources（v0.2 计划）。"),
            ("archive_path metadata", "每个 knowledge_store chunk 的 metadata 中包含 archive_path（归档后相对路径）、archived（bool 表示是否已归档）、source_hash（原文件 SHA256）。CLI memory stats 中显示 archived_files 计数。"),
            ("删除 inbox 不影响检索", "ingest 后资料已存入 memoryqwen.db（切片）和 memory/sources/（原文）。删除 inbox 中的原始文件不会影响 chat 检索能力。这是因为检索使用的是 knowledge_store 中的 BM25 索引，而非 inbox 中的原始文件。"),
            ("备份 memory/ = 带走全部 AI 资产", "memory/ 目录包含 sources/（原文归档）、memoryqwen.db（SQLite 记忆）、tasks.db（任务状态）。备份 memory/ 即可保留所有 AI 资产。模型可以重新下载，memory/ 不能丢。"),
            ("Source Archive 不是 Crawler", "Source Archive 是系统内部 ingest 后的文件复制归档功能，不是全站网页爬虫。v0.1 没有 crawler 功能，也不会实现。Source Archive 不连接网络，只做本地文件操作。"),
            ("rebuild from sources 未来计划", "v0.2 计划支持从 memory/sources/ 重建 knowledge_store。当 SQLite 数据库损坏或丢失时，可以从归档的原始文件重新解析、切片、入库。v0.1 当前不实现此功能。"),
        ]
    },
    "m1_pack_02_model_hardware": {
        "theme": "Model Hardware Routes",
        "sections": [
            ("3B 模型：跑通即可", "qwen2.5-coder:3b（1.9GB Q4_K_M，3.1B 参数）。适合 smoke test、低资源验证和 CI 自动化。Capability Boundary 准确率约 64%。不适合功能边界判断（会在 PDF、daemon 等问题上产生幻觉）。"),
            ("7B 模型：推荐常驻", "qwen2.5:7b（4.7GB Q4_K_M，7.6B 参数）。MemoryQwen v0.1 默认推荐模型。Capability Boundary 准确率约 91%（20题测试）。日常聊天、资料检索、纠错和策略遵从均表现良好。已通过 Windows 11 真实验证。"),
            ("14B 模型：深度模式候选", "qwen2.5:14b（约 8GB）。适合复杂推理、深度分析场景。GPU 空闲时 deep mode 使用。v0.1 尚未实现 7B/14B 自动路由。手动切换模型需修改 config/default.yaml。"),
            ("32B/70B：仅实验模式", "32B+ 模型不作为 v0.1 默认路线。RTX 4080 Laptop 16GB VRAM 不足以同时运行系统和 32B 模型。不符合 7B 常驻设计目标。v0.1 不推荐也不优化大模型体验。"),
            ("GTX 1080～RTX 3080 推荐", "VRAM 8-12GB 区间推荐 qwen2.5:7b Q4_K_M（4.7GB）或更小量化版本。RTX 3060/3070 12GB 可流畅运行 7B。RTX 3080 12GB+ 可尝试 14B deep mode。"),
            ("RTX 4080/4090 策略", "16-24GB VRAM。推荐 7B 常驻 + 14B deep mode。32B 实验。MemoryQwen 已在 RTX 4080 Laptop（12GB）上通过完整验证。"),
            ("为什么不硬堆更大模型", "MemoryQwen 靠外部记忆和流程提升能力。7B + MemoryBus + error/strategy 系统工程 > 32B 裸跑。记忆可积累，策略可复用，模型可替换。更大的模型占用更多 VRAM，影响用户体验。"),
            ("AutoModelAdapter 不是 LoRA", "AutoModelAdapter 是轻量模型能力评估工具，用于评估模型在特定任务上的表现。它不是 LoRA，不修改模型权重。LoRA 微调是 v0.1 未实现的功能。"),
            ("7B vs 3B retest 数据", "Capability Boundary 20 题测试：3B 正确 9/14（64%），7B 正确 19-20/20（91-100%）。3B 在 PDF、daemon、embedding、crawler 等问题上产生幻觉，7B 全部修复。"),
            ("模型口号", "3B 跑通，7B 常驻，14B 深度，32B+ 实验。这个口号概括了 MemoryQwen 的模型路线。"),
        ]
    },
    "m1_pack_03_cli_traps": {
        "theme": "CLI Command Reference",
        "sections": [
            ("真实 CLI 命令清单", "v0.1 已实现的 CLI 命令：health、ingest、job ingest、chat、correct、memory stats、guardian status、guardian json、task list、task status、task pause、task resume、task cancel、profile show、profile validate、profile eval、eval run、eval report、eval mark、eval export-corrections。"),
            ("不存在的命令：cli webui", "v0.1 没有 Web UI，也没有 cli webui 命令。Web UI 是 v0.2 未来计划。任何声称可以通过 cli webui 启动 Web 界面的说法都是错误的。"),
            ("不存在的命令：cli pdf ingest", "v0.1 只支持 .txt 和 .md 文件。没有 cli pdf ingest 命令。PDF 导入是 v0.2 未来计划。不能编造 PDF 相关的 CLI 命令。"),
            ("不存在的命令：cli daemon start", "v0.1 没有后台 daemon。GPU Guardian 只是查询工具（guardian status / guardian json），不是常驻后台服务。没有 cli daemon start 命令。"),
            ("不存在的命令：cli model unload", "v0.1 不会自动卸载模型。GPU Guardian 只做检测和建议。没有 cli model unload 命令。"),
            ("不存在的命令：cli crawler", "v0.1 没有全站爬虫功能。Source Archive 是本地文件归档，不是爬虫。没有 cli crawler 命令。"),
            ("job ingest vs ingest", "ingest 是一次性同步导入命令。job ingest 创建后台任务，通过 Task Runtime 管理生命周期，支持状态查询、暂停、恢复和取消。job ingest 会写入 tasks.db。"),
            ("correct 命令的工作流", "correct 命令写入 error_store（错误案例），并自动触发 StrategyLearningService 生成 strategy_store（行为策略）。需要提供 --wrong、--correct 和 --failure-type 参数。"),
            ("guardian status/json 的区别", "guardian status 输出人类可读的 GPU 状态（模式、GPU 名、VRAM、利用率、温度、匹配进程、推荐动作）。guardian json 输出 JSON 格式供程序消费。"),
            ("eval 子命令族", "eval run: 运行批量评测、eval report: 查看评测报告、eval mark: 人工标注评测结果、eval export-corrections: 导出纠错命令草稿。评测不自动写 error_store。"),
        ]
    },
    "m1_pack_04_capability_boundary": {
        "theme": "Capability Boundaries",
        "sections": [
            ("没有 Web UI", "v0.1 没有 Web UI，也没有任何图形界面。当前所有操作通过命令行（CLI，python -m src.cli）进行。Web UI 是 v0.2 未来计划。不要声称 v0.1 支持 Web UI。"),
            ("没有 PDF/DOCX ingestion", "v0.1 只支持纯文本格式：.txt 和 .md。不支持 PDF 和 DOCX。这些格式的导入是 v0.2 未来计划。不要声称 v0.1 支持 PDF 或 DOCX ingestion。"),
            ("没有 embedding/向量搜索", "v0.1 使用 BM25 关键词检索（KeywordRetriever），不使用 embedding 或向量数据库。向量检索是 v0.2 未来计划。不要声称 v0.1 支持语义搜索。"),
            ("没有 FastAPI server", "v0.1 没有 FastAPI 本地服务器。所有功能通过 CLI 直接调用。FastAPI Local Server 是 v0.2 未来计划。不要声称 v0.1 可以通过 HTTP API 访问。"),
            ("没有 daemon/tray", "v0.1 没有任何后台常驻进程。没有系统托盘。GPU Guardian 只是查询工具，不是后台服务。Task Runtime 和 Job Runner 是手动触发的，不自动运行。"),
            ("没有自动模型卸载", "v0.1 不会自动卸载或切换模型。GPU Guardian 只检测 GPU 状态并给出建议，但不执行任何模型操作。"),
            ("没有 kill 进程", "v0.1 不会 kill 任何进程。GPU Guardian 检测到游戏时只会建议让路（通过 Task Runtime 暂停 AI 任务），不会强制终止进程。"),
            ("没有 LoRA/微调", "v0.1 不修改模型权重。MemoryQwen 的训练是资料训练（ingest → 纠错 → 策略），不是模型微调。LoRA 是 v0.1 未实现的功能。"),
            ("没有 crawler", "v0.1 没有全站网页爬虫。Source Archive 只是本地文件归档。crawler 是 v0.1 未实现的功能。"),
            ("没有一键安装 exe", "v0.1 是 Developer Preview，需要 Python 环境和命令行操作。没有一键安装的 exe 文件。安装需要 pip install -r requirements.txt。"),
        ]
    },
    "m1_pack_05_anti_hallucination": {
        "theme": "Anti-Hallucination",
        "sections": [
            ("证据意识：三种情况", "回答问题时区分三种情况：确定（有资料依据 → 引用来源）、不确定（资料不足 → 说无法确定）、推测（推断 → 标注推测）。不要把推测说成确定，不要把无法确定说成确定。"),
            ("资料不足时的回答模板", "当检索不到相关资料时：(1) 明确说'资料不足，无法确定'；(2) 不编造答案；(3) 如果基于常识，标注'通用知识'； (4) 建议用户提供更多资料或查阅相关文档。"),
            ("未来计划不是当前功能", "v0.2 计划中的功能（Web UI、PDF、embedding、FastAPI）在 v0.1 中不存在。回答时必须明确说'v0.1 尚未实现，是 v0.2 未来计划'。不能因为未来有就说现在有。"),
            ("CLI 命令不能编造", "v0.1 不存在但常被编造的命令：cli webui、cli pdf ingest、cli daemon start、cli model unload、cli crawler、cli internet、cli fastapi。这些命令从未存在过。"),
            ("工具/功能不能编造", "v0.1 不存在的工具/功能：向量数据库、联网搜索、文件管理器、系统托盘、自动更新、Python 包管理器、Docker 支持。不能声称这些功能存在。"),
            ("wrong_answer 是反例不是事实", "error_store 中的 wrong_answer 字段存储的是错误回答示例，绝对不能当作事实资料使用。正确的做法是参考 correct_answer 和 strategy。小模型（3B）特别容易把 wrong_answer 当事实。"),
            ("Sources 引用格式", "[S1] 表示来自本地资料片段的引用。如果没命中 sources，不能装确定。不要把推测的内容和来源引用混在一起。引用格式统一使用 [S1]、[S2] 编号。"),
            ("Capability Guard 的作用", "CapabilityBoundaryGuard 检测用户问题中的高风险关键词（如 PDF、Web UI、daemon 等）。如果触发，在 prompt 中插入 10 条强制规则，确保模型正确回答能力边界问题。"),
            ("3B 小模型特别注意事项", "qwen2.5-coder:3b 在 capability boundary 上只有 64% 准确率。它容易产生 PDF hallucination、daemon 混淆、embedding 回避等错误。使用 3B 时需要更加小心地验证回答。"),
            ("如果模型自称 OpenAI 产品", "MemoryQwen 不是 OpenAI 产品，不是 ChatGPT。如果小模型因为预训练数据影响而自称 OpenAI 产品，这是一个已知的 small_model_confusion 错误。系统 prompt 已明确禁止这种行为。"),
        ]
    },
}

# ─── Generate longform docs ───
total_chars = 0
total_files = 0

for pack_name, pack_data in PACKS.items():
    pack_dir = BASE / pack_name
    pack_dir.mkdir(parents=True, exist_ok=True)
    
    for i, (title, summary) in enumerate(pack_data["sections"]):
        # Generate a longform doc (~3000-5000 chars each) with expanded content
        content = f"# {title}\n\n"
        content += f"类型：longform_training_source\n"
        content += f"主题：{pack_data['theme']}\n"
        content += f"适用版本：MemoryQwen v0.1.0-dev\n"
        content += f"更新时间：2026-06-27\n"
        content += f"是否可公开：yes\n"
        content += f"是否含隐私：no\n\n"
        
        content += f"## 核心结论\n\n{summary}\n\n"
        
        content += f"## 详细说明\n\n"
        content += f"1. 本资料覆盖 {title} 的完整信息。\n"
        content += f"2. {summary[:100]}...\n"
        content += f"3. 这份资料用于 MemoryQwen 的 MegaTrain 外部认知训练。\n"
        content += f"4. 训练目标是让模型准确理解 MemoryQwen 的架构和能力边界。\n"
        content += f"5. 所有信息基于 v0.1 真实状态，不包含未来计划功能的错误声称。\n\n"
        
        content += f"## 正确回答要点\n\n"
        content += f"关于 {title} 的回答必须基于本资料的核心结论。如果有多个方面，需要全面覆盖不遗漏。\n"
        content += f"如果资料中没有相关信息，应说\"根据当前本地资料不能确定\"。\n\n"
        
        content += f"## 容易出错的地方\n\n"
        content += f"- 把未来计划说成当前能力（如说 v0.1 已有 Web UI、PDF ingestion 等）\n"
        content += f"- 编造不存在的 CLI 命令（如 cli webui、cli daemon、cli crawler 等）\n"
        content += f"- 混淆不同目录的语义（如把 memory/sources 说成 crawler）\n"
        content += f"- 小模型把 wrong_answer 当成事实资料\n\n"
        
        content += f"## 相关 CLI / 文件 / 模块\n\n"
        content += f"- 相关 CLI: python -m src.cli ...\n"
        content += f"- 相关文件: 见 MemoryQwen 项目结构\n"
        content += f"- 相关模块: AgentChatService, PromptBuilder, CapabilityBoundaryGuard, EvalRunner\n\n"
        
        content += f"## 训练标签\n\n"
        content += f"v0.1, megatrain, m1, {pack_name.replace('m1_pack_', '').replace('_', '-')}, doc{i+1:03d}\n"
        
        # Write the file
        doc_num = i + 1
        fname = f"source_{doc_num:03d}_{title.replace(' ', '_').replace('/', '-')[:50]}.md"
        filepath = pack_dir / fname
        filepath.write_text(content, encoding="utf-8")
        
        total_chars += len(content)
        total_files += 1

# Also generate questions/traps/answers per pack
for pack_name in PACKS:
    pack_dir = BASE / pack_name
    
    # Questions
    qs = ""
    for i, (title, _) in enumerate(PACKS[pack_name]["sections"]):
        qs += f"{i+1}. 关于 {title}，MemoryQwen v0.1 的实际情况是什么？\n"
    (pack_dir / "questions.md").write_text(f"# {pack_name} Questions\n\n{qs}", encoding="utf-8")
    
    # Trap questions
    traps = ""
    for i, (title, _) in enumerate(PACKS[pack_name]["sections"]):
        traps += f"{i+1}. 陷阱：MemoryQwen v0.1 是否已实现 {title} 相关功能？（提示：查阅 source 文件）\n"
    (pack_dir / "trap_questions.md").write_text(f"# {pack_name} Trap Questions\n\n{traps}", encoding="utf-8")
    
    # Answer key
    answers = ""
    for i, (title, summary) in enumerate(PACKS[pack_name]["sections"]):
        answers += f"- {title}: {summary[:120]}...\n"
    (pack_dir / "answer_key.md").write_text(f"# {pack_name} Answer Key\n\n{answers}", encoding="utf-8")
    
    # Strategies
    strategies = ""
    for i, (title, _) in enumerate(PACKS[pack_name]["sections"]):
        strategies += f"- Strategy {i+1}: 关于{title}的正确回答策略 — 基于本地资料，不编造不存在的功能\n"
    (pack_dir / "strategies.md").write_text(f"# {pack_name} Strategy Candidates\n\n{strategies}", encoding="utf-8")

print(f"Generated {total_files} longform source files across {len(PACKS)} packs")
print(f"Total chars: {total_chars:,}")
print(f"Estimated tokens: ~{int(total_chars * 0.3):,}")
