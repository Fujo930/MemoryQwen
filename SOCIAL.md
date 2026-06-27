# MemoryQwen 宣传文案集

> 仓库地址: https://github.com/Fujo930/MemoryQwen
> 
> 适用于不同平台的推广文案。根据需要选择使用。

---

## 1. V2EX / 中文技术社区 (创造节点/分享创造)

**标题：** 我做了一个本地 AI Agent——能记住你教的所有东西，不依赖任何云服务

**正文：**

花了几个月，做了一个完全运行在本地的 AI agent 系统：MemoryQwen。

**它和 ChatGPT/云端 AI 有什么不同？**

- 🌍 **数据在你自己硬盘上**，不是别人的服务器
- 🧠 **真的会记住东西**——你导入的文档、纠正过的错误，都存在本地 SQLite 里，下次对话自动引用
- 📚 **引用来源精确到文件路径**——不会像 ChatGPT 那样编造引用
- 🎯 **纠错学习**——你说它错了，一键纠正，同类错误永不再犯
- 💰 **免费**——跑在你自己的 GPU 上，用 Ollama + Qwen2.5
- ⚡ **可以离线用**

**当前状态：**
- 429 个测试全绿
- 395 个知识片段已入库
- 130 道评估题验证，7B 模型准确率 ~91%
- GPU 让路策略：玩游戏/渲染时自动释放显存

**5 分钟跑起来：**
```bash
git clone https://github.com/Fujo930/MemoryQwen
cd MemoryQwen
pip install -r requirements.txt
ollama pull qwen2.5:7b
python -m src.cli job ingest inbox/
python -m src.cli chat "你的问题"
```

**v0.1 Developer Preview**，面向会用命令行的开发者。Web UI 在路线图上。

欢迎 star ⭐ 和试用反馈！

🔗 https://github.com/Fujo930/MemoryQwen

---

## 2. Reddit r/LocalLLaMA (English)

**Title:** MemoryQwen v0.1 — A local AI agent that remembers, cites sources, and learns from corrections (MIT, 429 tests, Qwen-based)

**Body:**

I've been building a local-first AI agent system called MemoryQwen and just released v0.1 Developer Preview.

**What it does:**
- Runs entirely locally (Ollama/LM Studio/llama.cpp)
- Persistent SQLite memory — your documents, chat history, and corrections survive across sessions
- BM25 keyword retrieval with exact source citations (file path + chunk index)
- **Error learning**: correct it once, it never makes that same mistake again
- **Strategy accumulation**: error patterns get distilled into reusable strategies
- **GPU Guardian**: auto-detects games/rendering and yields VRAM
- **Task queue** with pause/resume and persistent state
- **Capability boundary guard** — prevents hallucination about unimplemented features
- 130 eval questions with heuristic CJK-aware judge

**Current stats:**
- 429/429 pytest passing
- 395 knowledge chunks ingested
- 7B model hits ~91% accuracy on eval
- Pure Python, MIT licensed

**5-min setup:**
```bash
git clone https://github.com/Fujo930/MemoryQwen
pip install -r requirements.txt
ollama pull qwen2.5:7b
python -m src.cli job ingest inbox/
python -m src.cli chat "your question"
```

This is a CLI Developer Preview. Web UI planned for v0.2.

Would love feedback from fellow local LLM enthusiasts!

🔗 https://github.com/Fujo930/MemoryQwen

---

## 3. Twitter/X (简短版)

**中文：**

🚀 发布 MemoryQwen v0.1 — 本地 AI Agent 工作站

✅ 全本地运行 (Ollama + Qwen2.5)
✅ 持久化记忆 + 来源引用
✅ 纠错学习 (一次纠正，永不再犯)
✅ GPU 让路策略
✅ 429 测试全绿 | MIT 开源

5 分钟跑起来 👇
github.com/Fujo930/MemoryQwen

**English:**

🚀 MemoryQwen v0.1 — Local AI agent with real memory

✅ 100% local (Ollama/Qwen2.5)
✅ Persistent memory + source citations
✅ Error learning (correct once, never repeat)
✅ GPU auto-yield for games
✅ 429 tests | MIT licensed

github.com/Fujo930/MemoryQwen

---

## 4. Hacker News (Show HN)

**Title:** Show HN: MemoryQwen — A local AI agent with persistent memory and error learning

**Body:**

I built MemoryQwen because I wanted an AI assistant that:
1. Runs entirely on my machine (no cloud, no API keys)
2. Actually remembers what I teach it across sessions
3. Cites its sources precisely instead of hallucinating
4. Learns from corrections instead of repeating mistakes

It's a Python CLI app that sits on top of Ollama/LM Studio. The core insight is treating "memory" as a first-class citizen — not just chat history, but a multi-store SQLite backend with knowledge chunks, error cases, and reusable strategies.

The error learning loop is particularly interesting: when the model gives a wrong answer, you correct it once via CLI. The system hashes the correction pattern, stores it in error_store, and injects relevant past errors into future prompts. Over time, common failure patterns get promoted to reusable strategies.

Happy to answer questions. Looking for feedback, especially from folks who've tried building local RAG systems.

🔗 https://github.com/Fujo930/MemoryQwen

---

## 5. 知乎 (深度技术介绍)

**标题：** 我写了一个能「记住一切」的本地 AI Agent —— MemoryQwen 技术详解

**开头：**

市面上的 AI 助手都有一个共同问题：它们记不住东西。

ChatGPT 有上下文窗口限制，超出就忘。Claude 也是。它们无法在对话之间保持记忆，更不用说从错误中学习了。

我做了一个叫 MemoryQwen 的系统，试图解决"AI 记忆力"这个根本问题。

**核心设计：多存储记忆架构**

（这里展开技术细节...使用 README 中的架构图和模块说明）

**纠错学习机制：**

（解释 error_store → strategy_store 的闭环）

**能力边界守卫：**

（解释 CapabilityBoundaryGuard 如何防止模型幻觉）

**结尾：**

v0.1 是 Developer Preview，面向开发者。如果你对本地 AI 感兴趣，欢迎试用和反馈。

🔗 https://github.com/Fujo930/MemoryQwen

---

## 6. 即刻/微博 (极简版)

做了一款本地 AI 助手 MemoryQwen 🧠

- 全本地，不依赖云
- 真的能记住东西
- 一次纠错，永不再犯
- 429 测试全绿

github.com/Fujo930/MemoryQwen
