"""
MemoryQwen — Eval Runner Models
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class EvalQuestion:
    question_id: str = ""
    topic: str = ""
    question: str = ""
    expected_answer: str = ""
    expected_sources: list[str] = field(default_factory=list)
    guard_expected: bool | None = None
    failure_type_if_wrong: str = ""
    trap_level: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class EvalRunConfig:
    model_id: str = ""
    session_prefix: str = "eval"
    max_questions: int = 0
    shuffle: bool = False
    require_independent_session: bool = True
    use_debug_metadata: bool = True
    judge_mode: str = "heuristic"  # manual | heuristic | llm


@dataclass
class EvalAnswer:
    question_id: str = ""
    answer: str = ""
    sources: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    source_hit: bool = False
    guard_triggered: bool = False
    error_memory_used: bool = False
    strategy_memory_used: bool = False


@dataclass
class EvalJudgement:
    correctness: str = "unjudged"  # correct / partial / wrong / unjudged
    notes: str = ""
    failure_type: str = ""
    correction_needed: bool = False


@dataclass
class EvalResult:
    question: EvalQuestion = field(default_factory=EvalQuestion)
    answer: EvalAnswer = field(default_factory=EvalAnswer)
    judgement: EvalJudgement = field(default_factory=EvalJudgement)


@dataclass
class EvalReport:
    run_id: str = ""
    started_at: str = ""
    completed_at: str = ""
    total_questions: int = 0
    correct: int = 0
    partial: int = 0
    wrong: int = 0
    unjudged: int = 0
    source_hit_rate: float = 0.0
    guard_trigger_rate: float = 0.0
    results: list[EvalResult] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
