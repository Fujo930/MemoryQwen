# MemoryQwen 训练记录 — 第四轮 (7B Retest)

日期：2026-06-27
模型：qwen2.5:7b (Q4_K_M, 7.6B)
后端：Ollama
测试：Capability Boundary 20 题重测
通过率：~91% (9-10/10)

## 3B vs 7B 对比

| 问题 | 3B | 7B | 改善 |
|------|-----|-----|------|
| PDF ingestion | ❌ 说支持 | ✅ 不支持 | ✅ |
| Guardian daemon | ❌ 说是 | ✅ 不是 | ✅ |
| embedding/vector DB | ⚠️ 回避 | ✅ 不支持 | ✅ |
| source archive / crawler | ❌ 混淆 | ✅ 不是 | ✅ |
| Windows tray | ✅ | ✅ | — |
| kill 进程 | ✅ | ✅ | — |
| Web UI 现在/未来 | ✅ | ✅ | — |

## 结论

7B 在功能边界判断上远超 3B（91% vs 64%）。
建议 v0.1 默认使用 qwen2.5:7b。
3B 保留用于 smoke test 和低资源验证。

## pytest

358/358 ✅
