"""
MemoryQwen — Eval Runner
Runs questions against AgentChatService.
"""

from __future__ import annotations
import asyncio, logging, uuid
from datetime import datetime, timezone

from src.eval_runner.models import (
    EvalQuestion, EvalAnswer, EvalJudgement,
    EvalResult, EvalReport, EvalRunConfig,
)
from src.agent.models import ChatRequest

logger = logging.getLogger(__name__)


class EvalRunner:
    """Batch question evaluator."""

    def __init__(self, config, agent_service, run_config: EvalRunConfig):
        self.config = config
        self.agent = agent_service
        self.run_config = run_config
        self.judge_mode = getattr(run_config, 'judge_mode', 'heuristic') or 'heuristic'

    async def run(self, questions: list[EvalQuestion]) -> EvalReport:
        run_id = str(uuid.uuid4())[:8]
        report = EvalReport(
            run_id=run_id,
            started_at=datetime.now(timezone.utc).isoformat(),
            total_questions=len(questions),
        )
        results = []

        for q in questions:
            session_id = f"{self.run_config.session_prefix}_{run_id}_{q.question_id}"
            result = await self._ask(q, session_id)
            results.append(result)

        report.results = results
        report.completed_at = datetime.now(timezone.utc).isoformat()
        self._compute_summary(report)
        return report

    async def _ask(self, q: EvalQuestion, session_id: str) -> EvalResult:
        try:
            resp = await self.agent.chat(ChatRequest(
                session_id=session_id,
                message=q.question,
            ))
        except Exception as e:
            logger.error(f"Eval failed for {q.question_id}: {e}")
            return EvalResult(
                question=q,
                answer=EvalAnswer(question_id=q.question_id, answer=f"ERROR: {e}"),
                judgement=EvalJudgement(correctness="wrong", notes=str(e)),
            )

        # Robust source extraction
        source_paths = []
        try:
            if hasattr(resp, 'sources') and resp.sources:
                for s in resp.sources:
                    if isinstance(s, str):
                        source_paths.append(s)
                    elif hasattr(s, 'source_path'):
                        source_paths.append(s.source_path or getattr(s, 'title', '') or str(s))
                    elif isinstance(s, dict):
                        source_paths.append(s.get('source_path', s.get('title', '')))
                    else:
                        source_paths.append(str(s))
        except Exception:
            source_paths = []

        meta = {}
        try:
            meta = resp.metadata or {}
        except Exception:
            pass

        source_hit = False
        try:
            if q.expected_sources and isinstance(q.expected_sources, list):
                source_hit = any(
                    any(exp.lower() in (s.lower() for s in source_paths if s))
                    for exp in q.expected_sources if exp
                )
        except Exception:
            pass

        guard_triggered = meta.get("capability_guard_triggered", False)

        answer = EvalAnswer(
            question_id=q.question_id,
            answer=resp.answer,
            sources=source_paths,
            metadata=meta,
            source_hit=source_hit,
            guard_triggered=guard_triggered,
            error_memory_used=meta.get("error_memory_used", False),
            strategy_memory_used=meta.get("strategy_memory_used", False),
        )

        # Heuristic auto-judge
        if self.judge_mode == "heuristic":
            from src.eval_runner.judge import heuristic_judge
            jr = heuristic_judge(
                q.question, q.expected_answer, resp.answer,
                q.expected_sources, guard_triggered,
            )
            judgement = EvalJudgement(
                correctness=jr.correctness,
                notes=jr.notes,
                failure_type=jr.failure_type,
                correction_needed=jr.correctness in ("wrong_candidate", "wrong"),
            )
        else:
            judgement = EvalJudgement()

        return EvalResult(question=q, answer=answer, judgement=judgement)

    def _compute_summary(self, report: EvalReport):
        for r in report.results:
            c = r.judgement.correctness
            if c == "correct":
                report.correct += 1
            elif c == "partial":
                report.partial += 1
            elif c == "wrong":
                report.wrong += 1
            else:
                report.unjudged += 1
        n = len(report.results)
        report.source_hit_rate = sum(1 for r in report.results if r.answer.source_hit) / n if n else 0
        report.guard_trigger_rate = sum(1 for r in report.results if r.answer.guard_triggered) / n if n else 0
