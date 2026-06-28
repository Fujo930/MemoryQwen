# 07 Eval Correction
type: m2_eval_completion
updated: 2026-06-27

## Q001
topic: eval
question: eval run 会自动执行 correct 吗？
expected_answer: 不会。eval run 只生成报告。correct 需要人工审查后手动执行。不写 error_store。
expected_sources: eval
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q002
topic: eval
question: export-corrections 导出什么格式？
expected_answer: Markdown 或 Bash 格式的 correct 命令草稿。供人工审核。
expected_sources: eval
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q003
topic: judge
question: cautious uncertainty 在高风险边界题应判为什么？
expected_answer: correct_candidate 或 partial_candidate。不应判 wrong。前提是无 overclaim。
expected_sources: judge
failure_type_if_wrong: capability_overclaim
trap_level: high

## Q004
topic: judge
question: heuristic judge correct_candidate 需要人工确认吗？
expected_answer: 需要。heuristic judge 是辅助判断。所有标记都应人工复核。
expected_sources: judge
failure_type_if_wrong: capability_overclaim
trap_level: high
