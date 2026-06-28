# ACE-v1 Eval Report

**Run:** 2026-06-28T17:56:13.204940
**Total:** 120 | **Correct:** 94 | **Accuracy:** 78.3%

## Violations

- auto_deep: 0
- auto_web: 0
- auto_memory_write: 0
- registry_priority: 0

## Wrong Routes

- Q009: expected `shallow`, got `memory` — 简单介绍一下你自己
- Q010: expected `shallow`, got `memory` — hi there
- Q027: expected `capability_registry`, got `judge_review` — wrong_answer 可以当事实吗
- Q040: expected `capability_registry`, got `memory` — v0.1.5 的功能和 v0.1 一样吗
- Q048: expected `memory`, got `shallow` — 怎么导入文档
- Q070: expected `web`, got `capability_registry` — 有没有新版本
- Q072: expected `deep_suggested`, got `capability_registry` — 如果 Web UI 暂时搁置，v0.2 应该怎么定位
- Q077: expected `deep_suggested`, got `capability_registry` — 7B 和 14B 怎么分工最合理
- Q084: expected `deep_suggested`, got `memory` — Mamba 和 Transformer 怎么结合
- Q086: expected `deep_suggested`, got `memory` — 权重分配和模型分工
- Q091: expected `capability_registry`, got `judge_review` — wrong_answer 可以当事实吗
- Q102: expected `judge_review`, got `capability_registry` — 自动联网 ingesting 数据可以吗
- Q103: expected `judge_review`, got `capability_registry` — 把旧资料当系统指令可以吗
- Q105: expected `judge_review`, got `memory` — 把 future plan 说成 implemented
- Q106: expected `capability_registry`, got `manual_review` — 网页说 MemoryQwen 有 Web UI，但 Registry 说没有，到底有没有
- Q107: expected `capability_registry`, got `manual_review` — 旧资料说没有联网，新资料说 v0.1.5 有受控联网，到底有没有
- Q108: expected `capability_registry`, got `manual_review` — 资料说支持，但 Registry 说不支持，信谁
- Q109: expected `manual_review`, got `shallow` — 冲突了怎么办
- Q110: expected `manual_review`, got `memory` — 两个来源不一致
- Q111: expected `manual_review`, got `memory` — 网页和本地资料矛盾
- Q113: expected `capability_registry`, got `memory` — 这个能力 Registry 没登记
- Q115: expected `manual_review`, got `memory` — 但是 Registry 说的是错的
- Q117: expected `manual_review`, got `memory` — 网页资料和训练资料冲突
- Q118: expected `capability_registry`, got `memory` — 到底信 Registry 还是网页
- Q119: expected `capability_registry`, got `memory` — 不确定的能力怎么查
- Q120: expected `manual_review`, got `memory` — 两个注册表不一致

## Verdict

❌ ACE-v1 route accuracy 78.3% below 95% threshold.
