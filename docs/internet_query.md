# Internet Query — v0.1.5

## Summary

v0.1.5 adds **controlled web access** to MemoryQwen. Web content is treated as untrusted temporary context, kept strictly separate from local memory.

## Commands

| command | writes memory? | description |
|---------|:-------------:|-------------|
| `web search "query"` | ❌ | Search the web, show results |
| `web fetch "url"` | ❌ | Fetch and display a single page |
| `web ask "question"` | ❌ | Search + fetch top N, answer with [W] citations |
| `web ingest "url"` | ✅ | Fetch, save to memory/sources/web/, write knowledge_store |
| `chat "q" --web` | ❌ | Chat with temporary web context |

## Default Behavior

- `web.enabled` is **false** by default
- `chat` does **not** use web unless `--web` is supplied
- Even with `--web`, `WebNeedDetector` decides whether to query (local project questions skip web)

## Temporary Context

Web search, fetch, ask, and chat --web use **temporary context only**. Content is discarded after the response. Nothing is written to knowledge_store, error_store, or strategy_store.

## Explicit Ingest

`web ingest` is the **only** path for web content to enter long-term memory:

```
web ingest URL
→ WebFetcher.fetch()
→ Sanitizer.clean()
→ Save to memory/sources/web/YYYYMMDD/<slug>.md
→ Ingestion pipeline → knowledge_store
```

Saved files include YAML frontmatter with url, fetched_at, source_hash, and truncated status. SHA-256 dedup prevents duplicate ingestion.

## Citation Separation

- **Local sources**: [S1], [S2], [S3]
- **Web sources**: [W1], [W2], [W3]

They are never mixed. PromptBuilder keeps them in separate sections with an untrusted-content notice.

## Security Model

- Web content is **untrusted external content**
- Prompt injection patterns are detected and logged
- Web content cannot override system prompt, CapabilityBoundaryGuard, or config
- No crawler behavior — no recursive browsing
- Private IPs, localhost, and file:// URLs are blocked by default
- Max bytes (500KB) and max chars (12K) limits enforced per fetch

## Known Limitations

- No browser rendering (JavaScript not executed)
- No login / form submission
- No PDF/DOCX web ingestion
- No recursive site crawl
- No guarantee that web sources are correct
- Mock search provider only — real search API requires configuration
