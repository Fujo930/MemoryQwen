# 解决 AI 助手"失忆症"：一个本地记忆系统的设计与实现

## 问题

用过 ChatGPT 或 Claude 的人都经历过：聊着聊着，AI 就忘了前面说过什么。关了窗口重开，一切归零。更麻烦的是——它不知道什么不该说。

比如你告诉它"不支持 PDF 导入"，下次换个人问"支持 PDF 吗"，它可能张口就来"支持"。你纠正了一次，它不会记住。下次还犯。

根本原因：这些模型的"记忆"只存在于一次会话的上下文窗口里。窗口一关，记忆清零。

我在做一个本地的 AI agent 项目，叫 MemoryQwen。核心要解决的，就是这个记忆力问题。

## 设计思路

### 不只记对话，要记"知识"

普通的对话历史存一下就够了。但要让 AI 真正"学会"不犯同类错误，需要三层记忆：

**1. 知识库（knowledge_store）**

用户导入的文档（.txt/.md）全部存入 SQLite。每次聊天自动检索相关内容作为参考。

```
资料 → 分块 → 存入 knowledge_store → 聊天时 BM25 检索 → 引用原文
```

**2. 错误库（error_store）**

用户纠正过的错误永久存储。下次遇到类似问题，系统把"过去的错误和正确答案"一起注入 prompt。

```bash
# 纠错命令
python -m src.cli correct \
  --wrong "支持 PDF，用 parse_pdf 函数" \
  --correct "v0.1 不支持 PDF 导入，只支持 .txt 和 .md" \
  --strategy "关于文件格式支持的问题，先查 capability_boundary 资料"
```

纠正后，同一个会话 ID 下问"PDF 能导入吗"，模型不会再答错。

**3. 策略库（strategy_store）**

错误多了以后，归纳出可复用的策略。比如"关于当前不支持的功能，永远先回答'v0.1 尚未实现'，然后补充替代方案"。

策略会被注入到未来的所有相关对话中，不依赖特定会话。

### 不是存了就行，还要能防幻觉

有记忆还不够。模型即使看到了正确资料，也可能"脑补"出不存在的东西。比如：

- 明明只有 CLI，它说"有 Web UI"
- 明明只支持 .md，它说"可以导 PDF"
- source archive 只是本地文件拷贝，它说"会爬取网页"

针对这个问题做了**能力边界守卫（Capability Boundary Guard）**——检测用户问题中的高风险关键词，如果命中就注入强制指令：

```
检测到：PDF, 支持
→ 强制注入规则：不把 .md/.txt ingestion 说成 PDF/DOCX
→ 强制注入规则：资料不足时说"根据当前本地资料不能确定"
```

实测效果：不装 Guard 时 3B 模型在能力边界问题上准确率 ~64%，装 Guard 后 7B 模型 ~91%。

### GPU 让路：家用电脑的现实问题

跑本地模型会占用 GPU。用户玩游戏、渲染视频时，模型推理会抢显存。

解决方案不是"杀掉模型进程"（太粗暴），而是**检测 + 建议**：

```
nvidia-smi 查询 GPU 状态
→ 如果 VRAM 使用率 ≥ 85% → 推荐 full_yield（释放所有后台任务）
→ 如果检测到 Cyberpunk2077.exe → 推荐 game_mode（暂停 ingestion 等后台任务）
→ 推荐只是建议，不自动执行，不 kill 进程
```

### 评测系统：不只跑分，要跑真问题

普通的 benchmark 跑个 MMLU 分数很简单。但我想知道的是：模型会不会把"未来计划"说成"当前功能"？会不会编造不存在的 CLI 命令？

所以做了 312 道"陷阱题"——专门诱导模型出错：

- "cli webui 怎么用？"（不存在这个命令）
- "PDF ingestion 支持哪些格式？"（不支持 PDF）
- "source archive 爬了哪些网站？"（不爬网）
- "默认推荐 32B 还是 70B？"（推荐 7B）

用启发式判定器（heuristic judge）自动批改，检出 overclaim、fake CLI、wrong_answer 滥用等问题。

## 实测数据

| 指标 | 数值 |
|------|------|
| 知识片段 | 43,645 |
| 错误案例 | 17 |
| 策略 | 11 |
| 测试通过 | 496/496 |
| 评估题库 | 312 题（含 130 道真实题） |
| 7B 模型能力边界准确率 | ~91% |

## 架构总览

```
CLI
 ┣ Agent Layer（ChatService, PromptBuilder, Guard）
 ┣ Retrieval（BM25 多库搜索）
 ┣ Memory（SQLite: knowledge/error/strategy/chat）
 ┣ Infrastructure（Ingestion, GPU Guardian, Task Runtime）
 ┗ Model Client（Ollama / LM Studio）
```

## 一些踩过的坑

1. **小模型（3B）忽略 system prompt**：qwen2.5-coder:3b 默认会自称 OpenAI。必须在 system prompt 中显式禁止。这个在 7B 上不存在。

2. **Windows 中文路径**：ingestion 时中文文件名和路径可能导致编码问题。统一用 UTF-8，路径里避免特殊字符。

3. **BM25 对新文档不敏感**：43K 个旧 chunks 会把 30 个新 chunks 的信号完全淹没。后续可能需要给权威文档加权。

4. **Heuristic judge 的关键词过敏**：模型说"不支持 PDF"，judge 看到"PDF"就标 overclaim。需要 LLM-as-Judge 才能准确判定语义。

## 代码

项目是开源的，MIT license。目前 v0.1 Developer Preview，CLI 形态。Web UI 在计划中。

```
git clone https://github.com/Fujo930/MemoryQwen
pip install -r requirements.txt
ollama pull qwen2.5:7b
python -m src.cli job ingest inbox/
python -m src.cli chat "你的问题"
```

文档写了 Windows 11 快速启动、CLI 参考、配置参考、记忆备份等。

---

*写这个项目的初衷很简单：我不想要一个"聊完就忘"的 AI 助手。我要一个能记住我教过它什么、不会再犯同样错误的工具。如果你也在做类似的东西，欢迎交流。*
