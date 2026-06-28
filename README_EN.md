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
git clone https://github.com/Fujo930/MemoryQwen
cd MemoryQwen
pip install -r requirements.txt
ollama pull qwen2.5:7b
mkdir inbox
echo "# Project Docs" > inbox/test.md
python -m src.cli job ingest inbox/
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

## ✅ v0.1.5 Features

| Module | Feature | Status |
|--------|---------|:------:|
| 📥 Ingestion | Document import (.txt/.md) → SQLite | ✅ |
| 🔍 Retrieval | BM25 keyword search, multi-store | ✅ |
| 💬 Chat | Local model + source citations | ✅ |
| 🌐 Web | Internet Query: web search/fetch/ask, [W] citations, not a crawler | ✅ v0.1.5 |
| 🧠 Memory | Persistent chat history + knowledge base | ✅ |
| 🐛 Correction | User correction → auto-learning → never repeats | ✅ |
| 📋 Strategy | Error patterns → reusable strategies | ✅ |
| 🎮 GPU | GPU detection + auto-yield for games/rendering | ✅ |
| 📊 Tasks | Task queue + pause/resume + persistent state | ✅ |
| 🧪 Evaluation | 396 eval questions + heuristic judge + auto-export | ✅ |
| 🛡️ Guard | Capability boundary guard prevents hallucination | ✅ |
| 🏷️ Archive | Source file archive → memory/sources/ | ✅ |

## Not Yet Implemented

> Web UI · PDF/DOCX · embedding/vector search · daemon · tray icon · crawler · LoRA fine-tuning · one-click installer

## 📊 Live Stats

| Metric | Value |
|--------|-------|
| 🧪 pytest | **631/631** (100%) |
| 📚 Knowledge chunks | **43,645** |
| 🐛 Error cases | **17** |
| 📋 Strategies | **11** |
| 📝 Eval questions | **396** real (M3 312 + web 84) |
| 🛡️ Safety scan | **0** issues |

## 🧠 Model Recommendations

| Model | Size | Use Case | Accuracy |
|-------|------|----------|:--------:|
| `qwen2.5-coder:3b` | 1.9 GB | smoke test / low-resource | ~64% |
| **`qwen2.5:7b`** ⭐ | **4.7 GB** | **daily driver** | **~91%** |
| `qwen2.5:14b` | ~8 GB | deep reasoning | TBD |

> 💡 **3B to run, 7B as default, 14B for depth, 32B+ experimental.**

## 🧱 Dev Challenges & Known Bottlenecks

Honest status — no sugarcoating.

### 🚧 The Reasoning Wall

The 7B model cannot reliably reason when sources conflict. The system prompt says "v0.1.5 supports web search" but 43K training chunks say "v0.1 has no web" — the model **oscillates randomly** between both answers. Same question, three tries, three different answers.

**This is not fixable with prompt engineering.** It needs 14B+ parameters or a new reasoning architecture. RTX 4080 can run 14B: `ollama pull qwen2.5:14b`.

### ⚖️ Heuristic Judge Keyword Hypersensitivity

The v4 heuristic judge misclassifies correct answers. Model says "v0.1 does **not** support PDF" — judge sees "PDF" and flags overclaim. In the M3 300-question eval, **100% of "wrong" verdicts were judge false positives** (36/36). Zero real violations. Needs Judge v5 (LLM-as-Judge).

### 🔍 Retrieval Quality Bottleneck

BM25 favors high-frequency old documents among 43K chunks. New M3 batch docs (30 chunks) are completely drowned out. Eval source_hit rate: **0%** — not because answers are wrong, but because retrieval can't find the right docs. Needs Retrieval Quality v2.

### 🧩 Solo Development

All code, docs, tests, training data, and eval maintained by one person. Contributors welcome.

## ⚠️ Backup Your Memory

**Models can be re-downloaded. Memory cannot be replaced!**

```bash
xcopy memory memory_backup_%date% /E /I
```

See [Memory Backup Guide](docs/memory_backup.md)

## 🛠️ Common Commands

```bash
python -m src.cli health              # health check
python -m src.cli job ingest inbox/   # import documents
python -m src.cli chat "question"     # chat with auto-retrieval
python -m src.cli web search "query"  # web search (v0.1.5)
python -m src.cli correct --wrong "wrong" --correct "right"
python -m src.cli memory stats        # storage statistics
python -m src.cli guardian status     # GPU yield status
python -m src.cli eval run training_packs/  # run evaluation
```

📖 [Full CLI Reference](docs/cli_reference.md)

## 📖 Documentation

| Doc | Description |
|-----|-------------|
| [Windows 11 Quick Start](docs/windows11_quickstart.md) | Setup from scratch |
| [Internet Query](docs/internet_query.md) | Web access guide |
| [CLI Reference](docs/cli_reference.md) | All commands |
| [Config Reference](docs/config_reference.md) | YAML config options |
| [Architecture](docs/architecture.md) | Technical architecture |
| [Security Model](docs/security_model.md) | Security design |
| [Memory Backup](docs/memory_backup.md) | Backup strategy |

## 🗺️ Roadmap

- **v0.1** ✅ — CLI Developer Preview
- **v0.1.5** ✅ — Internet Query (web search + [W] citations)
- **v0.2** — Web UI
- **v0.3** — Embedding + hybrid search

## 🤝 Contributing

Issues and PRs welcome.

```bash
python -m pytest tests/ -q --basetemp=/tmp/mqwen-pytest
```

## 📄 License

MIT License © 2026 Fujo930 (MemoryQwen Contributors)

---

<p align="center">
  <sub>Built with ❤️ for local-first AI. No cloud required.</sub>
</p>
