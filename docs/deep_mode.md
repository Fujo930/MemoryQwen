# Deep Mode (14B)

Deep mode is an optional feature that uses the 14B model for complex reasoning tasks. It is **not required** for base MemoryQwen operation.

## When to Use Deep Mode

- Capability boundary questions with conflicting sources
- Version conflict resolution (v0.1 vs v0.1.5)
- Complex multi-topic questions
- Audit / verification of answers
- Planning and release decisions

## When NOT to Use

- Casual greetings
- Simple project questions
- Routine chat

## Speed

14B deep mode on RTX 4080 Laptop:
- First query: ~11s (model load)
- Steady state: 3.7-4.7s
- VRAM: 9.4 GB (76% of 12GB)

Comparable to 7B (3.6s avg) — the overhead is minimal on RTX 4080.

## Consistency

14B shows 100% consistency on Internet Query capability questions (9/9), compared to 7B's 89% (8/9). The improvement is most visible in version-aware answers (v0.1 vs v0.1.5).

## Metadata

Chat responses in deep mode include:

```json
{
  "model_mode": "deep",
  "model": "qwen2.5:14b",
  "fallback_used": false
}
```

## Config

```yaml
agent:
  deep_mode_enabled: true       # Enable deep mode feature
  deep_mode_model: qwen2.5:14b  # Model for deep mode
  auto_escalate_to_deep: false   # Never auto-escalate
```

## CLI

```bash
python -m src.cli chat "问题" --deep
python -m src.cli chat "问题" --web --deep
```
