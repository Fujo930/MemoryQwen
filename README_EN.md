# MemoryQwen v0.1 — Developer Preview

🌐 **English** | [中文](README.md)

**Local AI agent — your personal AI workstation.**

MemoryQwen is an AI agent system that runs entirely on your own computer. No cloud, all data stays local.

## What v0.1 Can Do

| Feature | Status |
|---------|--------|
| Document import (.txt, .md) | ✅ |
| Keyword retrieval (BM25) | ✅ |
| Local model chat (Ollama/LM Studio) | ✅ |
| Source citations in chat | ✅ |
| User correction + error learning | ✅ |
| Strategy accumulation | ✅ |
| GPU detection + yield modes | ✅ |
| Task queue + pause/resume | ✅ |
| Persistent task state (SQLite) | ✅ |
| Chinese filenames / UTF-8 | ✅ |

## What v0.1 Cannot Do

- ❌ GUI (Web UI planned for v0.2)
- ❌ Vector search / embedding
- ❌ Multi-path reasoning
- ❌ Background daemon / auto-run
- ❌ One-click installer

**v0.1 is a Developer Preview for developers.** CLI required.

## System Requirements

- **OS:** Windows 10/11 (11 23H2+ recommended)
- **Python:** 3.11+
- **GPU:** Not required, NVIDIA RTX recommended
- **RAM:** 16GB+
- **Backend:** Ollama / LM Studio / llama.cpp (OpenAI-compatible)

### Model Recommendations

| Model | Size | Use Case | Capability Accuracy |
|-------|------|----------|---------------------|
| qwen2.5-coder:3b | 1.9GB | smoke test / low-resource | ~64% |
| **qwen2.5:7b** | **4.7GB** | **default model** | **~91%** |
| qwen2.5:14b | ~8GB | deep mode | TBD |

> **3B to run, 7B as default, 14B for depth, 32B+ experimental.**

## Current Status

- **pytest:** 429/429
- **knowledge_store:** 395 chunks
- **error_store:** 17 cases
- **strategy_store:** 11 strategies
- **eval questions:** 130 real, 0 placeholder
- **safety:** 0 issues

## Not Implemented in v0.1

Web UI, PDF, DOCX, embedding, daemon, tray, crawler, LoRA, one-click installer.

## v0.1.5 Planned

Internet Query (web search + fetch + chat with [W] citations).

## 5-Minute Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Model Service

**Ollama (recommended):**
```bash
ollama serve
ollama pull qwen2.5:7b
```

**LM Studio:**
- Open LM Studio → Load model → Start Local Server

### 3. Configure

Edit `config/default.yaml`:

```yaml
model_client:
  provider: "ollama"
  base_url: "http://localhost:11434"
  model: "qwen2.5:7b"
```

### 4. Verify

```bash
python -m src.cli health
```

### 5. Chat

```bash
mkdir inbox
echo "# MemoryQwen" > inbox/test.md
echo "Supports document retrieval and keyword search." >> inbox/test.md

python -m src.cli job ingest inbox/
python -m src.cli chat "What does MemoryQwen support?" --debug-memory
```

## Common Commands

```bash
python -m src.cli health              # health check
python -m src.cli job ingest inbox/   # import documents
python -m src.cli chat "question"     # chat
python -m src.cli correct --wrong ".." --correct ".."  # correction
python -m src.cli memory stats        # view storage stats
python -m src.cli guardian status     # GPU yield status
python -m src.cli task list           # task list
```

Full reference: [docs/cli_reference.md](docs/cli_reference.md)

## ⚠️ Important: Backup Your Memory

**Models can be re-downloaded. Memory cannot be lost!**

Back up the `memory/` folder regularly:

```bash
xcopy memory memory_backup_%date% /E /I
```

See: [docs/memory_backup.md](docs/memory_backup.md)

## Docs

- [Windows 11 Quick Start](docs/windows11_quickstart.md)
- [CLI Reference](docs/cli_reference.md)
- [Config Reference](docs/config_reference.md)
- [Memory Backup](docs/memory_backup.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Release Checklist](docs/release_checklist_v0.1.md)

## License

MemoryQwen v0.1 Developer Preview. For development and testing.
