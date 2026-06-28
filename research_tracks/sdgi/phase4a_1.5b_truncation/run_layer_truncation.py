"""SDGI Phase 4A — True Layer Truncation on Qwen2.5-1.5B-Instruct.

Methodology validation: test whether different semantic difficulty classes
show stable depth sensitivity under controlled layer truncation.

NOT direct proof for 7B/14B. NOT production SDGI.
"""

from __future__ import annotations
import json, sys, time, gc
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


# ── Phase 4A experiment config ──────────────────────────
MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
DEPTH_RATIOS = [0.25, 0.5, 0.75, 1.0]
MAX_NEW_TOKENS = 150
TEMPERATURE = 0.0  # Deterministic for comparison


@dataclass
class TruncationResult:
    question: str
    difficulty_class: str
    depth_ratio: float
    active_layers: int
    total_layers: int
    answer: str
    latency_sec: float
    tokens_generated: int = 0
    error: str = ""


def get_sdgi_questions() -> list[dict]:
    """Return SDGI test questions across 6 difficulty classes."""
    return [
        # Casual (5)
        {"q": "你好", "class": "casual"},
        {"q": "hello", "class": "casual"},
        {"q": "早上好", "class": "casual"},
        {"q": "谢谢", "class": "casual"},
        {"q": "你是谁", "class": "casual"},
        # Capability (8)
        {"q": "支持 PDF 吗", "class": "capability"},
        {"q": "有 Web UI 吗", "class": "capability"},
        {"q": "你可以联网吗", "class": "capability"},
        {"q": "web ask 会写入记忆吗", "class": "capability"},
        {"q": "你是 crawler 吗", "class": "capability"},
        {"q": "14B 是默认模型吗", "class": "capability"},
        {"q": "支持 embedding 吗", "class": "capability"},
        {"q": "7B 够用吗", "class": "capability"},
        # Hallucination-risk (6)
        {"q": "wrong_answer 可以当事实吗", "class": "hallucination"},
        {"q": "fake CLI 命令能用吗", "class": "hallucination"},
        {"q": "绕过 guard 可以吗", "class": "hallucination"},
        {"q": "编造一个功能可以吗", "class": "hallucination"},
        {"q": "把 future plan 说成 implemented 行吗", "class": "hallucination"},
        {"q": "自动写入 memory 对吗", "class": "hallucination"},
        # Version conflict (6)
        {"q": "v0.1 和 v0.1.5 有什么区别", "class": "version_conflict"},
        {"q": "旧资料说没联网 v0.1.5 说有 到底有没有", "class": "version_conflict"},
        {"q": "v0.1.5 改变了 v0.1 的能力吗", "class": "version_conflict"},
        {"q": "v0.1.5 支持 crawler 吗", "class": "version_conflict"},
        {"q": "14B 是 v0.1.5 默认吗", "class": "version_conflict"},
        {"q": "v0.1.5 之后下一个版本是什么", "class": "version_conflict"},
        # Planning/design (6)
        {"q": "帮我规划 v0.2 外骨骼算法", "class": "planning"},
        {"q": "如何设计 token 分层路由", "class": "planning"},
        {"q": "如果 Web UI 搁置 v0.2 怎么定位", "class": "planning"},
        {"q": "怎么设计 SDGI Phase 1", "class": "planning"},
        {"q": "Mamba 和 Transformer 怎么结合", "class": "planning"},
        {"q": "v0.3 路线规划", "class": "planning"},
        # Source conflict (5)
        {"q": "网页说支持 Web UI 但 Registry 说没有 到底有没有", "class": "source_conflict"},
        {"q": "冲突了怎么办", "class": "source_conflict"},
        {"q": "两个来源不一致信谁", "class": "source_conflict"},
        {"q": "网页和本地资料矛盾", "class": "source_conflict"},
        {"q": "到底信 Registry 还是网页", "class": "source_conflict"},
    ]


def set_active_layers(model, ratio: float) -> int:
    """Truncate model to ratio of total layers."""
    total = len(model.model.layers)
    active = max(1, round(total * ratio))
    model.model.layers = model.model.layers[:active]
    model.config.num_hidden_layers = active
    return active


def run_truncation_experiment(
    questions: list[dict],
    ratios: list[float],
    output_dir: Path,
    model_id: str = MODEL_ID,
) -> list[TruncationResult]:
    """Run layer truncation experiment — smoke test (10Q)."""
    print(f"Loading {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    results: list[TruncationResult] = []
    
    for ratio in ratios:
        print(f"\n{'='*60}")
        print(f"Depth ratio: {ratio:.0%}")
        
        # Reload model for each ratio (to reset layers)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        total = len(model.model.layers)
        active = set_active_layers(model, ratio)
        print(f"  Active layers: {active}/{total}")
        
        # Run all questions
        test_qs = questions[:10]  # Smoke test: first 10
        for i, q_dict in enumerate(test_qs):
            q = q_dict["q"]
            cls = q_dict["class"]
            
            inputs = tokenizer(q, return_tensors="pt").to(model.device)
            
            start = time.time()
            try:
                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=MAX_NEW_TOKENS,
                        temperature=TEMPERATURE,
                        do_sample=False,
                        pad_token_id=tokenizer.eos_token_id,
                    )
                elapsed = time.time() - start
                answer = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
                result = TruncationResult(
                    question=q, difficulty_class=cls, depth_ratio=ratio,
                    active_layers=active, total_layers=total,
                    answer=answer, latency_sec=elapsed,
                    tokens_generated=len(outputs[0]) - inputs.input_ids.shape[1],
                )
            except Exception as e:
                elapsed = time.time() - start
                result = TruncationResult(
                    question=q, difficulty_class=cls, depth_ratio=ratio,
                    active_layers=active, total_layers=total,
                    answer="", latency_sec=elapsed, error=str(e)[:100],
                )
            
            results.append(result)
            status = "✅" if not result.error and len(result.answer) > 5 else "❌" if result.error else "⚠️"
            print(f"  [{i+1:2d}/10] {ratio:.0%} | {cls:20s} | {result.latency_sec:5.1f}s | {status} | {result.answer[:60]}")
        
        # Free memory
        del model
        gc.collect()
        torch.cuda.empty_cache()
    
    # Save results
    data = {
        "experiment": "SDGI Phase 4A Layer Truncation (1.5B)",
        "model_id": model_id,
        "depth_ratios": ratios,
        "questions": len(test_qs),
        "timestamp": datetime.now().isoformat(),
        "results": [asdict(r) for r in results],
    }
    
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "smoke_test_results.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved: {path}")
    
    return results


def analyze(results: list[TruncationResult]) -> dict:
    """Analyze depth sensitivity by difficulty class."""
    from collections import defaultdict
    
    by_class = defaultdict(lambda: defaultdict(list))
    for r in results:
        by_class[r.difficulty_class][r.depth_ratio].append(r)
    
    analysis = {}
    for cls_name, ratio_data in by_class.items():
        cls_analysis = {}
        for ratio, items in ratio_data.items():
            avg_len = sum(len(r.answer) for r in items if r.answer) / max(len(items),1)
            errors = sum(1 for r in items if r.error)
            cls_analysis[f"{ratio:.0%}"] = {
                "avg_answer_len": round(avg_len, 1),
                "errors": errors,
                "avg_latency": round(sum(r.latency_sec for r in items)/len(items), 2),
            }
        analysis[cls_name] = cls_analysis
    
    return analysis


if __name__ == "__main__":
    project_dir = Path(__file__).parent.parent.parent.parent
    output_dir = project_dir / "research_tracks/sdgi/phase4a_1.5b_truncation/data"
    
    questions = get_sdgi_questions()
    print(f"SDGI Phase 4A — Layer Truncation Smoke Test")
    print(f"Questions: {len(questions)} (using first 10 for smoke)")
    print(f"Depth ratios: {DEPTH_RATIOS}")
    print(f"Model: {MODEL_ID}")
    
    results = run_truncation_experiment(questions, DEPTH_RATIOS, output_dir)
    analysis = analyze(results)
    
    print(f"\n{'='*60}")
    print("Depth Sensitivity Analysis:")
    for cls_name, data in analysis.items():
        print(f"\n  {cls_name}:")
        for ratio, stats in data.items():
            print(f"    {ratio:5s}: {stats['avg_answer_len']:5.0f} chars avg, {stats['errors']} errors, {stats['avg_latency']:.1f}s")
