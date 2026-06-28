<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.5-blue" alt="version">
  <img src="https://img.shields.io/badge/python-3.11+-blue" alt="python">
  <img src="https://img.shields.io/badge/tests-631%2F631-brightgreen" alt="tests">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey" alt="platform">
</p>

<p align="center">
  <b>🌐 English | <a href="README.md">中文</a></b>
</p>

<h1 align="center">MemoryQwen</h1>
<h3 align="center">Local AI Agent — Your Personal AI Workstation</h3>

---

> **Your data, your model, your rules.** MemoryQwen is an AI agent system that runs entirely on your computer — no cloud, no API keys, no data leaving your machine. It remembers everything you teach it, cites sources precisely, and learns from corrections.

## ✨ Why MemoryQwen?

| | ChatGPT / Cloud AI | MemoryQwen |
|---|-------------------|------------|
| 🌍 Data location | Cloud servers | **Your hard drive** |
| 🔒 Privacy | Conversations logged | **100% local** |
| 🧠 Memory | Session window only | **Persistent SQLite memory** |
| 📚 Citations | Hallucination-prone | **Exact quotes + file paths** |
| 🎯 Error learning | Can't correct | **One-command correction, never repeats** |
| 💰 Cost | Monthly subscription | **Free, runs on your GPU** |
| ⚡ Offline | ❌ | ✅ |

## ⚡ 5-Minute Quick Start

```bash
# 1. Install
git clone https://github.com/Fujo930/MemoryQwen
cd MemoryQwen
pip install -r requirements.txt

# 2. Pull a model (Ollama)
ollama pull qwen2.5:7b

# 3. Import your documents
mkdir inbox
echo "# Project Docs" > inbox/test.md
echo "API endpoint: http://localhost:8080" >> inbox/test.md
python -m src.cli job ingest inbox/

# 4. Start chatting
python -m src.cli chat "What is the API endpoint?" --debug-memory
```

> See [Windows 11 Quick Start](docs/windows11_quickstart.md) for detailed instructions.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                     CLI / API                        │
├─────────────────────────────────────────────────────┤
│  Agent Layer  │ ChatService │ PromptBuilder          │
│               │ ErrorLearning │ StrategyLearning     │
│               │ CapabilityBoundaryGuard              │
├─────────────────────────────────────────────────────┤
│  Retrieval    │ BM25 Tokenizer │ Multi-Store Search  │
├─────────────────────────────────────────────────────┤
│  Memory       │ knowledge_store │ error_store        │
│  (SQLite)     │ strategy_store  │ chat_messages      │
│               │ task_records     │                   │
├─────────────────────────────────────────────────────┤
│  Infrastructure │ Ingestion │ FileWatcher            │
│                 │ GPU Guardian │ BackgroundJobRunner │
│                 │ TaskRuntime │ EvalRunner           │
├─────────────────────────────────────────────────────┤
│  Model Client  │ Ollama / LM Studio / llama.cpp      │
└─────────────────────────────────────────────────────┘
```

## ✅ v0.1 Features

| Module | Feature | Status |
|--------|---------|:------:|
| 📥 Ingestion | Document import (.txt/.md) → SQLite | ✅ |
| 🔍 Retrieval | BM25 keyword search, multi-store | ✅ |
| 💬 Chat | Local model (Ollama/LM Studio) + source citations | ✅ |
| 🧠 Memory | Persistent chat history + knowledge base | ✅ |
| 🐛 Correction | User correction → auto-learning → never repeats | ✅ |
| 📋 Strategy | Error patterns → reusable strategies | ✅ |
| 🎮 GPU | GPU detection + auto-yield for games/rendering | ✅ |
| 📊 Tasks | Task queue + pause/resume + persistent state | ✅ |
| 🧪 Evaluation | 396 eval questions + heuristic judge + auto-export | ✅ |
| 🌐 Web | Internet Query: web search/fetch/ask, [W] citations | ✅ v0.1.5 |
| 🛡️ Guard | Capability boundary guard prevents hallucination | ✅ |
| 🏷️ Archive | Source file archive → memory/sources/ with citations | ✅ |

## Not Yet Implemented

> Web UI · PDF/DOCX · embedding/vector search · daemon · tray icon · crawler · LoRA fine-tuning · one-click installer

*These are on the v0.2+ roadmap. v0.1 is a Developer Preview for CLI users.*

## 📊 Live Stats

| Metric | Value |
|--------|-------|
| 🧪 pytest | **631/631** (100%) |
| 📚 Knowledge chunks | **395** |
| 🐛 Error cases | **17** |
| 📋 Strategies | **11** |
| 📝 Eval questions | **396** real, 0 placeholder |
| 🛡️ Safety scan | **0** issues |

## 🧠 Model Recommendations

| Model | Size | Use Case | Accuracy |
|-------|------|----------|:--------:|
| `qwen2.5-coder:3b` | 1.9 GB | smoke test / low-resource | ~64% |
| **`qwen2.5:7b`** ⭐ | **4.7 GB** | **daily driver** | **~91%** |
| `qwen2.5:14b` | ~8 GB | deep reasoning | TBD |

> 💡 **3B to run, 7B as default, 14B for depth, 32B+ experimental.**

## 🛠️ Common Commands

```bash
python -m src.cli health              # health check
python -m src.cli job ingest inbox/   # import documents
python -m src.cli chat "question"     # chat with auto-retrieval
python -m src.cli correct \           # correction learning
  --wrong "wrong answer" \
  --correct "right answer" \
  --strategy "rule to remember"
python -m src.cli memory stats        # storage statistics
python -m src.cli guardian status     # GPU yield status
python -m src.cli task list           # task list
python -m src.cli eval run training_packs/  # run evaluation
```

📖 [Full CLI Reference](docs/cli_reference.md)

## ⚠️ Backup Your Memory

**Models can be re-downloaded. Memory cannot be replaced!**

```bash
xcopy memory memory_backup_%date% /E /I
```

See [Memory Backup Guide](docs/memory_backup.md)

## 📖 Documentation

| Doc | Description |
|-----|-------------|
| [Windows 11 Quick Start](docs/windows11_quickstart.md) | Setup from scratch |
| [CLI Reference](docs/cli_reference.md) | All commands |
| [Config Reference](docs/config_reference.md) | YAML config options |
| [Architecture](docs/architecture.md) | Technical architecture |
| [Memory Backup](docs/memory_backup.md) | Backup strategy |
| [Troubleshooting](docs/troubleshooting.md) | Common issues |
| [Release Notes](docs/release_notes_v0.1.0-dev.md) | v0.1 changelog |

## 🗺️ Roadmap

- **v0.1** (current) — Developer Preview, CLI only
- **v0.1.5** — Internet Query (web search + [W] citations)
- **v0.2** — Web UI
- **v0.3** — Embedding + hybrid search

## 🤝 Contributing

v0.1 is a Developer Preview. Issues and PRs welcome!

```bash
# Run tests
python -m pytest tests/ -q --basetemp=/tmp/mqwen-pytest

# Format
pip install black && black src/ tests/
```

## 📄 License

MIT License © 2026 Fujo930 (MemoryQwen Contributors)

---

<p align="center">
  <sub>Built with ❤️ for local-first AI. No cloud required.</sub>
</p>
