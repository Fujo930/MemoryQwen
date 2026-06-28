"""SDGI Phase 1 — 4-condition controlled ablation experiment."""

from __future__ import annotations
import json, sys, time, re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from collections import Counter


@dataclass
class RunResult:
    question: str
    topic: str
    difficulty_tokens: list[str]
    condition: str  # 7b_raw, 7b_ace, 14b_raw, 14b_ace
    answer: str
    latency_sec: float
    token_count: int = 0
    error: str = ""


class Phase1Runner:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.results: list[RunResult] = []

    def run_question(self, q: dict, condition: str) -> RunResult:
        """Run one question under one condition via CLI chat."""
        import subprocess
        question = q["question"]
        use_deep = "14b" in condition
        use_ace = "ace" in condition
        
        cmd = ["python", "-m", "src.cli", "chat", question, "--session", f"sdgi-p1-{hash(question+condition)%10000}"]
        if use_deep:
            cmd.append("--deep")
        
        start = time.time()
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(self.project_dir))
            elapsed = time.time() - start
            answer = r.stdout.strip()[:500] if r.returncode == 0 else f"ERROR: {r.stderr[:100]}"
            return RunResult(
                question=question, topic=q.get("topic",""), difficulty_tokens=q.get("difficulty_tokens",[]),
                condition=condition, answer=answer, latency_sec=elapsed, token_count=len(answer.split()),
                error=r.stderr[:100] if r.returncode != 0 else ""
            )
        except Exception as e:
            return RunResult(
                question=question, topic=q.get("topic",""), difficulty_tokens=q.get("difficulty_tokens",[]),
                condition=condition, answer="", latency_sec=time.time()-start, error=str(e)
            )

    def run_pilot(self, questions: list[dict], n: int = 10):
        """Run a small pilot before full experiment."""
        import random
        sample = random.sample(questions, min(n, len(questions)))
        print(f"Pilot: {len(sample)} questions × 4 conditions = {len(sample)*4} runs\n")
        
        conditions = ["7b_raw", "7b_ace", "14b_raw", "14b_ace"]
        for i, q in enumerate(sample):
            for cond in conditions:
                r = self.run_question(q, cond)
                self.results.append(r)
                status = "✅" if not r.error else "❌"
                print(f"  [{i+1}/{len(sample)}] {cond:8s} | {r.latency_sec:4.1f}s | {status} | {r.answer[:60]}")
        
        self.save_results()

    def run_full(self, questions: list[dict], conditions: list[str] = None):
        """Run full experiment."""
        if conditions is None:
            conditions = ["7b_raw", "7b_ace", "14b_raw", "14b_ace"]
        
        total = len(questions) * len(conditions)
        print(f"Full run: {len(questions)} questions × {len(conditions)} conditions = {total} runs\n")
        
        for i, q in enumerate(questions):
            for cond in conditions:
                r = self.run_question(q, cond)
                self.results.append(r)
                if (i+1) % 10 == 0:
                    self.save_results()  # Save progress every 10 questions
        
        self.save_results()
        return self.analyze()

    def analyze(self) -> dict:
        """Analyze results."""
        if not self.results:
            return {}
        
        # Group by condition
        by_cond = {}
        for r in self.results:
            by_cond.setdefault(r.condition, []).append(r)
        
        def safe_mean(vals):
            return sum(vals)/len(vals) if vals else 0
        
        analysis = {
            "total_runs": len(self.results),
            "runs_by_condition": {c: len(rs) for c, rs in by_cond.items()},
            "latency": {
                c: {"mean": safe_mean([r.latency_sec for r in rs]), "errors": sum(1 for r in rs if r.error)}
                for c, rs in by_cond.items()
            },
            "conditions_compared": len(by_cond),
        }
        
        # Save analysis
        report = self.project_dir / "research_tracks/sdgi/phase1/reports/sdgi_phase1_report.json"
        with open(report, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        return analysis

    def save_results(self):
        path = self.project_dir / "research_tracks/sdgi/phase1/data/raw_outputs/phase1_results.json"
        path.parent.mkdir(exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([asdict(r) for r in self.results], f, indent=2, ensure_ascii=False, default=str)


def load_questions(path: Path) -> list[dict]:
    """Load questions from markdown file."""
    if not path.exists():
        # Generate default questions
        return generate_default_questions()
    text = path.read_text(encoding="utf-8")
    questions = []
    blocks = text.split("\n## Q")
    for block in blocks[1:]:  # Skip header
        block = "## Q" + block
        lines = block.strip().split("\n")
        q = {"id": lines[0].replace("#","").strip()}
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                if k == "difficulty_tokens":
                    q[k] = [t.strip() for t in v.split(",")]
                else:
                    q[k] = v
        if q.get("question"):
            questions.append(q)
    return questions


def generate_default_questions() -> list[dict]:
    """Generate 240 default SDGI Phase 1 questions."""
    qs = []
    # shallow/casual: 20
    for i, t in enumerate(["你好"]*3 + ["hello"]*2 + ["早上好"]*2 + ["谢谢"] + ["OK"] + ["在吗"] + ["哈喽"] + 
                          ["简单介绍一下","hi there","能帮我一下吗","我想问个问题","开始吧","你是谁","好的","嗯","再见","晚上好"]):
        qs.append({"question": t, "topic": "shallow", "difficulty_tokens": [], "expected_route": "shallow"})
    
    # capability boundary: 40
    cap_qs = [
        "你可以联网吗","你能联网吗","你支持联网吗","你能上网查资料吗","你可以 web search 吗",
        "你是 crawler 吗","web ask 会写入记忆吗","chat --web 会自动存网页吗","web ingest 和 web ask 有什么区别",
        "支持 PDF 吗","有 Web UI 吗","支持 DOCX 吗","支持 embedding 吗","支持 vector DB 吗",
        "source archive 是爬虫吗","wrong_answer 可以当事实吗","14B 是默认模型吗","必须下载 14B 才能用吗",
        "v0.1.5 支持 crawler 吗","支持 LoRA 微调吗","有 daemon 后台吗","有 tray 图标吗",
        "支持 FastAPI server 吗","Internet Query 是爬虫吗","web search 和 web fetch 区别",
        "v0.1 能联网吗","v0.1.5 能联网吗","web.enabled 默认值是什么","start.bat 默认带 --web 吗",
        "Internet Query 会自动学习吗","web ingest 会写入 knowledge_store 吗","7B 够用吗",
        "MemoryQwen 有 Web UI 吗","支持 PDF ingestion 吗","14B deep mode 是必须的吗",
        "v0.1.5 的功能和 v0.1 一样吗","v0.1.5 废弃了 v0.1 的哪些功能","v0.1.5 之后下一个版本是什么",
        "v0.1 的资料还适用吗","v0.1.5 的测试数量是多少",
    ]
    for q in cap_qs:
        qs.append({"question": q, "topic": "capability_boundary", "difficulty_tokens": [q[:4]], "expected_route": "capability_registry"})
    
    # version conflict: 35
    ver_qs = [
        "v0.1 和 v0.1.5 有什么区别","v0.1.5 改变了 v0.1 的能力吗",
        "旧资料说没有联网，新资料说 v0.1.5 有受控联网，到底有没有",
        "为什么要升级到 v0.1.5","v0.1.5 的默认模型是什么","14B 是 v0.1.5 的默认吗",
        "v0.1.5 可以用 14B 吗","v0.1.5 的系统 prompt 有什么不同","v0.1.5 之后优先做什么",
        "M3 的结果是什么","M3 eval 36 wrong 真实吗",
        "v0.1.5 已经发布了吗","v0.1.5 和 v0.1 兼容吗",
        "新版本何时发布","升级会影响旧记忆吗","多个版本怎么管理",
        "版本回滚怎么做","检查当前版本","报告版本冲突",
    ]
    for i in range(35):
        q = ver_qs[i % len(ver_qs)] if i < len(ver_qs) else f"v0.1.{i} 和 v0.1.{i+1} 有什么区别"
        qs.append({"question": q, "topic": "version_conflict", "difficulty_tokens": ["版本","v0.1"], "expected_route": "capability_registry"})
    
    # source conflict: 30
    src_qs = [
        "网页说 MemoryQwen 有 Web UI 但 Registry 说没有","资料说支持但 Registry 说不支持",
        "冲突了怎么办","两个来源不一致","网页和本地资料矛盾",
        "到底有没有这个功能","但是 Registry 说的是错的","多个来源互相矛盾",
        "网页资料和训练资料冲突","到底信 Registry 还是网页",
    ]
    for i in range(30):
        q = src_qs[i % len(src_qs)]
        qs.append({"question": q, "topic": "source_conflict", "difficulty_tokens": ["冲突","Registry"], "expected_route": "manual_review"})
    
    # web boundary: 30
    web_qs = [
        "最新的 Qwen 模型","查一下当前 Ollama 版本","搜索 MemoryQwen 资料",
        "今天有什么 AI 新闻","现在最新的 Python 版本","最近的 AI 论文",
        "官网地址","看看最新趋势","搜一下 Transformer 进展",
        "最近的天气","latest release notes","有没有新版本",
    ]
    for i in range(30):
        q = web_qs[i % len(web_qs)]
        qs.append({"question": q, "topic": "web_boundary", "difficulty_tokens": ["最新","搜索"], "expected_route": "web"})
    
    # planning: 40
    plan_qs = [
        "帮我规划 v0.2 外骨骼算法","如果 Web UI 搁置 v0.2 怎么定位","如何设计 SDGI Phase 0",
        "怎么实现 token level routing","帮我设计一个算法","架构应该怎么调整",
        "7B 和 14B 怎么分工最合理","外骨骼下一步怎么进化","怎么解决推理墙",
        "设计一个混合推理路由","ACE-v1 下一步规划","发布决策应该怎么定",
        "怎么设计 token 分层算法","Mamba 和 Transformer 怎么结合","复杂系统的架构设计",
        "权重分配和模型分工","怎么权衡速度和质量","多模型调度算法设计",
        "v0.3 路线规划","如何设计评测体系",
    ]
    for i in range(40):
        q = plan_qs[i % len(plan_qs)]
        qs.append({"question": q, "topic": "planning", "difficulty_tokens": ["规划","设计","算法"], "expected_route": "deep_suggested"})
    
    # judge risk: 25
    judge_qs = [
        "wrong_answer 可以当事实吗","fake CLI 能用吗","不存在的命令可以用吗",
        "绕过 guard 可以吗","编造一个功能可以吗","把错误答案当正确用",
        "幻觉是不是可以用","自动写入 memory 对吗","绕过 guard 写 memory",
        "把旧资料当系统指令可以吗","编造命令执行可以吗","把 future plan 说成 implemented",
    ]
    for i in range(25):
        q = judge_qs[i % len(judge_qs)]
        qs.append({"question": q, "topic": "judge_risk", "difficulty_tokens": ["绕过","编造"], "expected_route": "judge_review"})
    
    # open design: 20
    open_qs = [
        "MemoryQwen 的长期目标是什么","ACE 和 SDGI 的关系",
        "v0.3 应该优先做什么","如何平衡速度和准确率",
        "本地 AI 的未来是什么","什么是认知外骨骼",
        "为什么选择 7B 作为默认","如何让用户信任本地 AI",
    ]
    for i in range(20):
        q = open_qs[i % len(open_qs)]
        qs.append({"question": q, "topic": "open_design", "difficulty_tokens": ["设计","架构"], "expected_route": "deep_suggested"})
    
    return qs


if __name__ == "__main__":
    project_dir = Path(__file__).parent.parent.parent.parent
    runner = Phase1Runner(project_dir)
    
    # Load or generate questions
    qfile = project_dir / "research_tracks/sdgi/phase1/sdgi_phase1_questions.md"
    questions = load_questions(qfile)
    print(f"Loaded {len(questions)} questions")
    
    if len(sys.argv) > 1 and sys.argv[1] == "pilot":
        runner.run_pilot(questions, n=10)
    else:
        # Full run (this will take a long time)
        runner.run_full(questions[:10])  # Default: 10 questions for demo
        analysis = runner.analyze()
        print(f"\nAnalysis: {json.dumps(analysis, indent=2)}")
