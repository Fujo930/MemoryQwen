# MemoryQwen v0.2-alpha

## Highlights

- **ACE-v1 Adaptive Cognitive Exoskeleton** — unified cognitive routing pipeline
- **Capability Registry** — authoritative facts override old training data
- **Token-Difficulty Routing v1** — 7 route types (shallow → manual_review)
- **14B optional deep mode** — never auto-escalated
- **Unified ACE metadata** — full audit trail in every response
- **7B remains default daily model**

## What Changed

- New `src/ace/` module (schema, controller, context_plan)
- New `src/routing/` module (TDR-v1)
- New `src/capability/` module (Capability Registry)
- CLI: `ace inspect`, `route inspect`, `web search/fetch/ask/ingest`
- PromptBuilder: ACE context injection, recent chat priority
- AgentChatService: unified ACE decision flow
- 716 tests (up from 496)

## Safety Model

- Registry > new docs > old training data > web sources
- Guard always enabled regardless of route
- 14B never auto-escalated
- Web never auto-enabled
- Web content never auto-ingested into memory

## Known Limitations

No Web UI, PDF/DOCX, embedding/vector DB, crawler, LoRA, or SDGI.
14B is optional — not required for base MemoryQwen.

## Recommended Setup

```bash
ollama pull qwen2.5:7b          # default daily model
ollama pull qwen2.5:14b         # optional deep mode
python -m src.cli chat "hello"  # 7B
python -m src.cli chat "complex" --deep  # 14B
```

## Next

ACE-v1 Eval Pack + SDGI Research Track Phase 0
