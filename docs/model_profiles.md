# Model Profiles

MemoryQwen uses a multi-tier model architecture. Users are not required to install all models.

## Current Model Roles

| Role | Model | Size | VRAM | Default? |
|------|-------|:----:|:----:|:--------:|
| **Daily Brain** | `qwen2.5:7b` (Q4_K_M) | 4.7 GB | ~4.8 GB | ✅ Yes |
| **Deep Brain** | `qwen2.5:14b` (Q4_K_M) | 9.0 GB | ~9.4 GB | ❌ Optional |
| Experimental | `qwen2.5:32b` (Q3+) | ~20 GB | TBD | ❌ No |

## 7B — Daily Brain

- Default model for all normal chat
- Fast: 1.2-5.6s per query (avg 3.6s)
- Runs easily on RTX 3060+ or any 6GB+ GPU
- Handles: casual chat, project questions, capability boundaries, web queries

## 14B — Deep Brain

- Optional deep mode via `chat --deep`
- Speed: 3.7-4.7s after warmup (comparable to 7B)
- VRAM: 9.4 GB on RTX 4080 Laptop (76% of 12GB)
- Use cases: capability conflict resolution, audit mode, complex planning
- **Not required** for base MemoryQwen operation
- `auto_escalate_to_deep: false` by default (user must explicitly use --deep)

## How to Install

```bash
# 7B (required for base operation)
ollama pull qwen2.5:7b

# 14B (optional deep mode)
ollama pull qwen2.5:14b
```

## How to Use

```bash
# Normal chat (7B)
python -m src.cli chat "问题"

# Deep mode (14B)
python -m src.cli chat "问题" --deep

# Web + Deep mode
python -m src.cli chat "问题" --web --deep
```

## Config

```yaml
model:
  default_light_model: qwen2.5:7b
  default_deep_model: qwen2.5:14b

agent:
  deep_mode_enabled: true
  deep_mode_model: qwen2.5:14b
  deep_mode_fallback_model: qwen2.5:7b
  auto_escalate_to_deep: false
```
