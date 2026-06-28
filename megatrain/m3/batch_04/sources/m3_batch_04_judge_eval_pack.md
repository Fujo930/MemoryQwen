# M3 Batch 04 — Judge v4 / v5 Evaluation Pack
type: m3_source
batch: 04
topic: judge_eval
tokens_target: 500K

MemoryQwen Eval System 包含启发式判定器 (Heuristic Judge) 和可选的 LLM-as-Judge。

## Judge 版本演进

### Judge v3
- 问题：cautious uncertainty false negatives
- 当一个回答谨慎地说"不能确定"时，v3 会错误地判定为 wrong
- 修复：识别 cautious uncertainty 模式

### Judge v4 (当前)
- 改进：negation-aware（否定感知）
- 减少 false positives
- 限制：不能处理 complex double negation
- 复杂语义题必须 manual review
- 不能完全替代人工判定

### Judge v5 (计划)
- 候选方案：LLM-as-Judge
- 用模型评估模型
- 风险：成本高、速度慢、模型偏见

## heuristic judge 的限制

1. 双重否定检测不完善
   - "并非不支持" → 可能误判
   - "没有不正确的" → 可能误判
   
2. overclaim 检测可能过于激进
   - 提"PDF"不代表声称支持 PDF
   - 模型说"不支持 PDF"也可能被标记为 PDF overclaim
   - 这是 known false positive，不是模型错误

3. temporal shift 检测：不能区分"现在是"vs"将来是"
4. negation + affirmation 混合句无力处理

## manual review 规则

这些情况必须进入 manual_review：
- 复杂双重否定
- temporal shift
- negation + affirmation 混合
- judge false positive 嫌疑
- 答案被标记 wrong 但有 citation

## eval run 行为

eval run 不自动 correct。只生成报告。
judgement 类型：
- correct: 答案正确
- correct_candidate: 可能正确（需要人工确认）
- partial: 部分正确
- partial_candidate: 可能部分正确
- wrong: 错误
- unjudged: 无法判定

## eval mark 命令

手动标记：
python -m src.cli eval mark <run_id> <qid> --correctness correct
python -m src.cli eval mark <run_id> <qid> --correctness wrong --failure-type capability_overclaim

## eval correction export

导出纠正草稿：
python -m src.cli eval corrections <run_id>
生成 correct 命令草稿供人工审查。
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx