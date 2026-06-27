# MemoryQwen v0.1.0-dev Developer Preview

## Highlights

- **Local memory-first AI agent** — runs entirely on your machine
- **OpenAI-compatible local model client** — Ollama, LM Studio, llama.cpp
- **SQLite memory stores** — knowledge, chat, error, strategy
- **Document ingestion** — .txt/.md file parsing, chunking, BM25 indexing
- **Source archive** — automatic file backup to memory/sources/
- **GPU Guardian** — nvidia-smi detection, 4 yield modes
- **Task Runtime** — state machine with pause/resume/cancel
- **Background Job Runner** — interruptible ingestion jobs
- **Capability Boundary Guard** — prevents hallucination about v0.1 limits
- **Eval Runner** — batch validation with correction export
- **Asset Metrics v2** — disk/file/content/database stats

## Recommended Model

| Model | Role | Accuracy |
|-------|------|----------|
| qwen2.5-coder:3b | Smoke test | ~64% |
| **qwen2.5:7b** | **Default** | **~91%** |
| qwen2.5:14b | Deep mode candidate | TBD |

> 3B runs it, 7B runs it well, 14B runs it deep, 32B+ experimental only.

## Quick Start

```bash
ollama pull qwen2.5:7b
pip install -r requirements.txt
python -m src.cli health
python -m src.cli job ingest inbox/
python -m src.cli chat "hello"
```

## Not Yet Implemented

MemoryQwen v0.1 is a **Developer Preview**. These are NOT included:

- ❌ Web UI
- ❌ Internet query / web search
- ❌ FastAPI server
- ❌ PDF / DOCX ingestion
- ❌ Embedding / vector database
- ❌ Daemon / system tray
- ❌ Automatic model unload
- ❌ Process killing
- ❌ Web crawler
- ❌ LoRA / fine-tuning

## Safety

- No model weights included
- No private data (API keys, passwords, personal chats)
- No cached build artifacts

## Tests

```bash
python -m pytest tests/ -q
```

## License

Developer Preview — for local use and evaluation.
