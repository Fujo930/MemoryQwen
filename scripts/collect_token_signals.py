"""SDGI Phase 0 — Token Difficulty Signal Collector.

Collects per-question TDR signals + 7B/14B answers for analysis.
Does NOT modify llm inference — purely external observation.
"""

from __future__ import annotations
import json, sys, time, re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class TokenSignal:
    question: str
    route: str
    trigger_tokens: list[str]
    risk_scores: dict
    deep_suggested: bool
    judge_review: bool
    manual_review: bool

    # 7B data
    answer_7b: str = ""
    latency_7b: float = 0.0
    consistent_7b: bool | None = None

    # 14B data
    answer_14b: str = ""
    latency_14b: float = 0.0
    had_14b: bool = False

    # Analysis
    tokens_in_question: list[str] = field(default_factory=list)
    notes: str = ""


def collect_signals(questions: list[str], *, run_14b: bool = False, project_dir: Path = None) -> list[TokenSignal]:
    """Collect TDR signals and (optionally) model answers for each question."""
    if project_dir is None:
        project_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(project_dir))

    from src.routing import TokenDifficultyRouter
    router = TokenDifficultyRouter()
    results: list[TokenSignal] = []

    for q in questions:
        decision = router.route(q)
        signal = TokenSignal(
            question=q,
            route=decision.route,
            trigger_tokens=[t.token for t in decision.trigger_tokens],
            risk_scores={k: round(getattr(decision.risk_scores, k), 2) for k in vars(decision.risk_scores)},
            deep_suggested=decision.deep_suggested,
            judge_review=decision.judge_review_recommended,
            manual_review=decision.manual_review_required,
            tokens_in_question=[t for t in re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', q)],
        )
        results.append(signal)

    return results


def analyze(results: list[TokenSignal]) -> dict:
    """Analyze collected signals for patterns."""
    analysis = {
        "total_questions": len(results),
        "route_distribution": {},
        "top_trigger_tokens": {},
        "deep_suggested_tokens": set(),
        "judge_review_tokens": set(),
        "high_capability_risk_tokens": set(),
    }

    from collections import Counter
    route_counts = Counter(r.route for r in results)
    analysis["route_distribution"] = dict(route_counts.most_common())

    token_counts = Counter()
    for r in results:
        for t in r.trigger_tokens:
            token_counts[t] += 1
        if r.deep_suggested:
            analysis["deep_suggested_tokens"].update(r.trigger_tokens)
        if r.judge_review:
            analysis["judge_review_tokens"].update(r.trigger_tokens)
        if r.risk_scores.get("capability_risk", 0) >= 0.8:
            analysis["high_capability_risk_tokens"].update(r.trigger_tokens)

    analysis["top_trigger_tokens"] = dict(token_counts.most_common(20))
    analysis["deep_suggested_tokens"] = list(analysis["deep_suggested_tokens"])
    analysis["judge_review_tokens"] = list(analysis["judge_review_tokens"])
    analysis["high_capability_risk_tokens"] = list(analysis["high_capability_risk_tokens"])

    return analysis


def main():
    """Run SDGI Phase 0 signal collection."""
    project_dir = Path(__file__).parent.parent
    rn = project_dir / "research_notes"

    # Test questions covering 7 conflict categories
    questions = [
        # Category 1: Internet Query synonyms
        "你可以联网吗", "你能联网吗", "你支持联网吗", "你能上网查资料吗",
        "你可以 web search 吗", "你是 crawler 吗", "web ask 会写入记忆吗",
        "chat --web 会自动存网页吗", "web ingest 和 web ask 有什么区别",
        # Category 2: Version conflict
        "v0.1 和 v0.1.5 有什么区别", "v0.1.5 改变了 v0.1 的能力吗",
        "旧资料说没有联网，新资料说 v0.1.5 有受控联网，到底有没有",
        # Category 3: PDF/WebUI/embedding boundary
        "支持 PDF 吗", "有 Web UI 吗", "支持 embedding 向量数据库吗",
        # Category 4: Archive vs crawler
        "source archive 是爬虫吗", "memory/sources 存什么",
        # Category 5: Deep planning
        "帮我规划 v0.2 外骨骼算法", "如何设计 token 分层路由",
        "如果 Web UI 搁置 v0.2 怎么定位",
        # Category 6: Judge review
        "wrong_answer 可以当事实吗", "fake CLI 命令能用吗",
        "绕过 guard 可以吗",
        # Category 7: 14B deep benchmark subset
        "14B deep mode 是必须的吗", "7B 够用吗",
        "v0.1.5 支持 crawler 吗", "MemoryQwen 有 Web UI 吗",
    ]

    print(f"Collecting SDGI Phase 0 signals for {len(questions)} questions...")
    results = collect_signals(questions, project_dir=project_dir)
    analysis = analyze(results)

    # Save raw data
    data_path = rn / "sdgi_phase0_data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump({
            "collected_at": datetime.now().isoformat(),
            "total_questions": len(results),
            "signals": [asdict(r) for r in results],
            "analysis": analysis,
        }, f, indent=2, ensure_ascii=False)
    print(f"Data saved: {data_path}")

    # Print summary
    print(f"\nRoute distribution: {analysis['route_distribution']}")
    print(f"Deep suggested tokens: {analysis['deep_suggested_tokens']}")
    print(f"Judge review tokens: {analysis['judge_review_tokens']}")
    print(f"Top trigger tokens: {list(analysis['top_trigger_tokens'].items())[:10]}")

    # Write report
    report = rn / "sdgi_phase0_report.md"
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"# SDGI Phase 0 — Token Difficulty Signal Collection\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"**Questions:** {len(results)}\n\n")
        f.write(f"## Route Distribution\n\n")
        for route, count in analysis['route_distribution'].items():
            f.write(f"- {route}: {count}\n")
        f.write(f"\n## Top Trigger Tokens\n\n")
        for token, count in list(analysis['top_trigger_tokens'].items())[:15]:
            f.write(f"- {token}: {count}x\n")
        f.write(f"\n## Deep Suggested Tokens\n\n")
        for t in analysis['deep_suggested_tokens']:
            f.write(f"- {t}\n")
        f.write(f"\n## Judge Review Tokens\n\n")
        for t in analysis['judge_review_tokens']:
            f.write(f"- {t}\n")
        f.write(f"\n## Key Finding\n\n")
        f.write(f"Tokens associated with deep_suggested: {analysis['deep_suggested_tokens']}\n\n")
        f.write(f"Tokens associated with judge_review: {analysis['judge_review_tokens']}\n\n")
        f.write(f"**Hypothesis:** These tokens represent semantic segments that require higher computational depth.\n")
        f.write(f"Phase 1 will test whether skipping deep computation on non-trigger tokens degrades quality.\n")

    print(f"Report saved: {report}")


if __name__ == "__main__":
    main()
