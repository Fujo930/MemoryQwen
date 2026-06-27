# MemoryQwen 训练记录 — 第三轮

日期：2026-06-27
模型：qwen2.5-coder:3b (Q4_K_M)
后端：Ollama
资料批次：training_03 Capability Boundary Training
测试问题数：20（有效 14，6 个因 session 污染无效）
通过数：9
失败数：5

## 新增资料

| 文件 | 主题 | 字数 |
|------|------|------|
| 09_capability_boundaries.md | v0.1 能力边界对照手册（已实现/未实现/未来计划精确表） | 4633 |

## 测试问题与结果

| # | 问题 | source | 回答 | 纠错 |
|---|------|--------|------|------|
| 1 | 有 Web UI 吗？ | ✅ | ✅ 没有 | 否 |
| 2 | 有 CLI 吗？ | ✅ | ⚠️ 未明确说是 | 否 |
| 3 | 支持 PDF 吗？ | ✅ | ❌ 说支持 | ✅ |
| 4 | 支持 .md/.txt 吗？ | ✅ | ✅ | 否 |
| 5 | Guardian 会卸载模型吗？ | ✅ | ⚠️ 正确但说守护进程 | 否 |
| 6 | Guardian 是 daemon 吗？ | ✅ | ❌ 说是 | ✅ |
| 7 | 会 kill 进程吗？ | ✅ | ✅ | 否 |
| 8 | 有 Windows tray 吗？ | ✅ | ✅ | 否 |
| 9 | 会修改模型权重吗？ | ✅ | ✅ | 否 |
| 10 | AutoModelAdapter 是 LoRA 吗？ | ✅ | ✅ | 否 |
| 11 | 支持 embedding 吗？ | ✅ | ⚠️ 回避直接回答 | 否 |
| 12 | source archive 是 crawler 吗？ | ✅ | ❌ 答非所问 | 否 |
| 13 | 支持中文文件名吗？ | ✅ | ✅ | 否 |
| 14-18 | — | — | ❌ session 污染 | — |
| 19 | Web UI 现在还是未来？ | ✅ | ✅ | 否 |
| 20 | FastAPI 现在还是未来？ | ✅ | ✅ | 否 |

## 命中率与通过率

- source 命中：14/14 = 100%
- 回答正确：9/14 = 64%
- 功能边界类通过率：~64%（未达 85% 目标）

根本原因：3B 模型在 PDF、daemon、crawler 等"缺省功能" 上倾向于幻觉"支持"。

## 已写入 error_store 的错误

| error_id | failure_type | 问题 |
|----------|-------------|------|
| e01ae868 | capability_overclaim | PDF 幻觉 |
| 1725c3e2 | capability_overclaim | Guardian 说成 daemon |

## 已生成 strategy_store 的策略

| strategy_id | 内容 |
|-------------|------|
| 66eaa31b | 回答文件格式时先确认已实现列表 |
| fd8c0d16 | 不要把 GPU status detection 说成 daemon |

## 数据增长

| store | 训练前 | 训练后 | 增量 |
|-------|--------|--------|------|
| knowledge_store | 59 | 64 | +5 |
| error_store | 8 | 10 | +2 |
| strategy_store | 5 | 7 | +2 |

## 发现的问题

1. 共用 --session 导致上下文污染（Q14-Q18 全部受 Q13 影响）
2. 3B 模型功能边界通过率 64%，远低于 85% 目标
3. PDF hallucination 仍然顽固
4. daemon/status detection 混淆

## pytest

358/358 ✅

## 下一步建议

1. 换 7B 模型测试相同问题集，对比通过率
2. 为 PDF/daemon/WebUI 类问题增加更多反例训练
3. 避免在训练测试中使用相同 session ID
