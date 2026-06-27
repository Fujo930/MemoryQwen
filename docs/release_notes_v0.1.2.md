# v0.1.2 Release Notes

## Urgent Fix: Smart Retrieval Gate

### Problem
v0.1.0/v0.1.1 performed full BM25 index retrieval on **every** chat message — even casual greetings like "你好" or "hi". After MegaTrain M1/M2 expanded knowledge_store to 22K+ chunks, this caused:
- Unnecessarily high chat latency (~3-4s even for simple greetings)
- BM25 index loaded for every query regardless of need
- pytest times inflated by repeated index refreshes

### Fix: Smart Retrieval Gate (v0.1.2)

Introduced `RetrievalGate` — a deterministic heuristic that decides **whether** and **which** stores to retrieve **before** calling the retriever.

| Query Type | Retrieves? | Stores | Example |
|-----------|-----------|--------|---------|
| Casual greeting | ❌ Skip | none | "你好", "hi", "谢谢" |
| High-risk boundary | ✅ Required | all 3 | "支持 PDF 吗？" |
| Project question | ✅ Required | knowledge + strategy | "MemoryQwen 有什么功能？" |
| Error/strategy | ✅ Required | error + strategy | "wrong_answer 怎么处理？" |
| Model/hardware | ✅ Required | knowledge + strategy | "3B 够用吗？" |
| Unknown | ✅ Conservative | knowledge | "这是什么系统？" |

### Changes

- **New:** `src/agent/retrieval_gate.py` — heuristic gate with 7 rule tiers
- **Modified:** `src/agent/chat_service.py` — gate integration before retrieval
- **Modified:** `src/config.py` + `config/default.yaml` — gate config fields
- **Modified:** `src/cli.py` — debug-memory shows gate decision
- **New:** `tests/test_agent/test_retrieval_gate.py` — 29 tests

### Impact

- Casual chat: retrieval skipped → lower latency
- High-risk questions: still fully retrieved
- Backward compatible: gate can be disabled via config
- 463/463 tests passing

### Config

```yaml
agent:
  use_retrieval_gate: true
  retrieval_gate_mode: "heuristic"
  retrieval_gate_default_retrieve: true
  retrieval_gate_max_top_k: 5
```
