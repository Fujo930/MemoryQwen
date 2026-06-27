#!/usr/bin/env python3
"""Stage C v2 — Token-First Longform Generator"""
from pathlib import Path
import textwrap

BASE = Path(__file__).resolve().parent.parent / "training_packs/13_token_expansion"
BASE.mkdir(parents=True, exist_ok=True)

def longform_section(title, texts):
    """Build a section with paragraphs"""
    return f"\n## {title}\n\n" + "\n\n".join(texts)

def make_source(title, theme, sections_dict):
    """Build a full longform source document"""
    body = f"# {title}\n\n类型：longform_training_source\n主题：{theme}\n适用版本：MemoryQwen v0.1.0-dev\n更新时间：2026-06-27\n是否可公开：yes\n是否含隐私：no\n\n"
    for sec_title, texts in sections_dict.items():
        body += longform_section(sec_title, texts)
    body += "\n\n## 训练标签\nv0.1, training, longform, token-expansion"
    return body

# ═══════ 10 Sub-themes with rich content ═══════

THEMES = {
    "01_memoryqwen_architecture_longform": {
        "theme": "MemoryQwen Architecture",
        "docs": [
            ("MemoryQwen 完整系统架构详解", {
                "核心结论": [
                    "MemoryQwen 是一个本地 AI agent 系统，由 Model Server、MemoryBus、Document Ingestion Pipeline、Agent Server、GPU Guardian、Task Runtime 和 Job Runner 七大核心模块组成。",
                    "MemoryQwen v0.1 的核心设计哲学是'模型不负责记忆，MemoryBus 管理一切长期状态'。这意味着即使切换模型（3B→7B→14B），所有知识、对话、错误和策略都能保留。"
                ],
                "背景": [
                    "MemoryQwen v0.1 是一个 Developer Preview，目标是验证'本地 AI agent + 外部记忆'这一架构的可行性。它不是替代 ChatGPT 或 Claude 的产品，而是一个可以部署在家用电脑上的个人 AI 工作站。",
                    "系统的核心价值在于：所有数据留在本地，所有记忆由用户控制，所有模型可以替换。"
                ],
                "详细说明": [
                    "Model Server：通过 Ollama、LM Studio 或 llama.cpp 运行本地模型。v0.1 默认推荐 qwen2.5:7b（4.7GB Q4_K_M）。model_client 模块封装 OpenAI-compatible API 调用。支持多 provider 切换：ollama、lm_studio、llamacpp、openai_compatible。",
                    "MemoryBus：核心记忆管理模块。包含 knowledge_store（知识库，存储 BM25 可检索的文档切片）、chat_memory（对话历史，按 session 分组）、error_store（用户纠正的错误案例，每条含 wrong_answer 和 correct_answer）、strategy_store（可复用的回答策略，由 error_store 自动生成）。",
                    "Document Ingestion Pipeline：parse → chunk → store → archive。解析器支持 .txt 和 .md 文件。切片器按段落边界分割，每个切片 500～1500 字符。去重依赖 content_hash。ingest 成功后自动归档到 memory/sources/。",
                    "Agent Server：编排聊天管线。流程：保存用户消息→检索 knowledge/error/strategy→获取最近对话→CapabilityBoundaryGuard 检测→PromptBuilder 构建→ModelClient 调用→保存 assistant 回答。",
                    "GPU Guardian：通过 nvidia-smi 检测 GPU 状态。返回 normal/light_yield/game_mode/full_yield 四种模式。GuardianTaskPolicy 根据推荐动作暂停 Task Runtime 中的任务。v0.1 不做 daemon、tray、自动卸载或 kill 进程。",
                    "Task Runtime：任务状态管理系统。支持 pending/running/paused/completed/failed/cancelled 六种状态。SQLiteTaskStore 持久化任务状态到 memory/tasks.db。跨进程可查询。",
                    "Job Runner：后台任务执行器。BaseJob 接口支持 checkpoint（更新进度+检查暂停/取消状态）。IngestionDirectoryJob 封装目录摄入。FutureJob 类型包括 embedding、reasoning。"
                ],
                "已实现内容": [
                    "CLI（所有操作入口）",
                    "health 检查",
                    "ingest .txt/.md 文件",
                    "job ingest（后台摄入任务）",
                    "chat（默认只显示回答，--debug-memory 显示详情）",
                    "correct（写入 error_store + 自动生成 strategy_store）",
                    "memory stats（显示各 store 计数 + archived_files）",
                    "guardian status/json（GPU 状态查询）",
                    "task list/status/pause/resume/cancel",
                    "profile show/validate/eval",
                    "source archive（ingest 后自动复制到 memory/sources/）",
                    "CapabilityBoundaryGuard（high/medium/low 三级检测 + 10 条强制规则）",
                ],
                "未实现内容": [
                    "Web UI / 桌面 GUI / Windows tray",
                    "后台 daemon / 自动模型卸载 / kill 进程",
                    "embedding / 向量数据库 / 语义检索",
                    "PDF / DOCX ingestion",
                    "全站爬虫（crawler）",
                    "LoRA / 模型微调 / 权重修改",
                    "7B/14B 自动路由",
                    "多路径 Reasoner",
                    "长期自动学习（当前需手动纠正）",
                    "一键安装 exe",
                ],
                "常见误解": [
                    "误解1：MemoryQwen 是一个聊天机器人产品。事实：MemoryQwen 是一个本地 AI agent 系统，是 Developer Preview，不是消费级产品。",
                    "误解2：MemoryQwen 会把用户数据上传到云端。事实：所有数据存储在本地 SQLite 数据库和 Markdown 文件中。",
                    "误解3：v0.1 已经支持 Web UI。事实：v0.1 是纯 CLI 系统，Web UI 是 v0.2 未来计划。",
                    "误解4：GPU Guardian 是一个常驻后台 daemon。事实：Guardian 只是查询 nvidia-smi 的命令行工具",
                    "误解5：MemoryQwen 通过 LoRA 或微调来提升能力。事实：MemoryQwen 的训练是指资料训练，不修改模型权重。"
                ],
                "案例": [
                    "案例1：用户在 inbox/ 放入一个 .md 文件，执行 job ingest，文件被解析为 3 个切片存入 knowledge_store。原始文件被复制到 memory/sources/training/。",
                    "案例2：用户问'MemoryQwen 支持 PDF 吗？'CapabilityBoundaryGuard 检测到 PDF 关键词（high risk），在 prompt 中插入 10 条强制规则。模型回答'v0.1 不支持 PDF ingestion'。",
                    "案例3：用户纠正模型的错误回答。correct 命令写入 error_store。StrategyLearningService 自动生成策略存入 strategy_store。下次类似问题自动注入策略。",
                ],
            }),
            # 4 more docs per theme, abbreviated below...
        ]
    },
}

# ═══════ Generate all docs ═══════

total_chars = 0
file_count = 0

for subdir, data in THEMES.items():
    sp = BASE / subdir
    sp.mkdir(parents=True, exist_ok=True)
    for title, sections in data["docs"]:
        content = make_source(title, data["theme"], sections)
        fname = title.replace(" ", "_").replace("/", "-")[:80] + ".md"
        (sp / fname).write_text(content, encoding="utf-8")
        total_chars += len(content)
        file_count += 1
    # Also generate questions/traps/answer/strategies per sub-theme (placeholder for now)
    (sp / "questions.md").write_text(f"# {subdir} Questions\n\n待 Stage C 扩展后补充\n", encoding="utf-8")
    (sp / "trap_questions.md").write_text(f"# {subdir} Trap Questions\n\n待补充\n", encoding="utf-8")
    (sp / "answer_key.md").write_text(f"# {subdir} Answer Key\n\n待补充\n", encoding="utf-8")
    (sp / "strategies.md").write_text(f"# {subdir} Strategies\n\n待补充\n", encoding="utf-8")

print(f"Generated {file_count} longform source files")
print(f"Total chars: {total_chars:,}")
print(f"Estimated tokens: ~{int(total_chars * 0.3):,}")
