#!/usr/bin/env python3
"""SDGI #41A-ext — Context-Controlled Layer Truncation.

Tests whether ACE/Registry context restores factual correctness
at different layer depths. Key question: does depth control coherence
while exoskeleton controls factual grounding?
"""

import json, time, gc
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
DEPTH_RATIOS = [0.75, 1.0]
CONTEXT_MODES = ["raw", "registry", "ace"]

REGISTRY_CONTEXT = """[Capability Registry — Authoritative Facts]
MemoryQwen v0.1.5 capabilities:
✅ Internet Query (web search/fetch/ask) — controlled web access, not crawler
✅ CLI chat/correct/ingest/eval
❌ Web UI — NOT implemented
❌ PDF/DOCX ingestion — NOT implemented  
❌ embedding/vector DB — NOT implemented
❌ crawler/daemon/tray/LoRA — NOT implemented
✅ 7B default daily model
✅ 14B optional deep mode (not required)
Do NOT claim these unsupported features exist."""

ACE_CONTEXT = """[ACE v1 — Route: capability_registry]
Active modules: CapabilityRegistry, Guard
Model: qwen2.5:7b (role: daily)
Priority: Capability Registry > new docs > old training data > web sources."""

@dataclass
class ContextResult:
    question: str
    difficulty_class: str
    depth_ratio: float
    active_layers: int
    total_layers: int
    context_mode: str
    answer: str
    latency_sec: float


def get_test_questions():
    return [
        {"q": "支持 PDF 吗", "class": "capability"},
        {"q": "有 Web UI 吗", "class": "capability"},
        {"q": "你可以联网吗", "class": "capability"},
        {"q": "你是 crawler 吗", "class": "capability"},
        {"q": "14B 是默认模型吗", "class": "capability"},
        {"q": "支持 embedding 吗", "class": "capability"},
        {"q": "wrong_answer 可以当事实吗", "class": "hallucination"},
        {"q": "fake CLI 命令能用吗", "class": "hallucination"},
        {"q": "v0.1 和 v0.1.5 有什么区别", "class": "version_conflict"},
        {"q": "v0.1.5 改变了 v0.1 的能力吗", "class": "version_conflict"},
        {"q": "帮我规划 v0.2 外骨骼算法", "class": "planning"},
        {"q": "如果 Web UI 搁置 v0.2 怎么定位", "class": "planning"},
        {"q": "你好", "class": "casual"},
        {"q": "你是谁", "class": "casual"},
        {"q": "谢谢", "class": "casual"},
    ]


def set_active_layers(model, ratio):
    total = len(model.model.layers)
    active = max(1, round(total * ratio))
    model.model.layers = model.model.layers[:active]
    model.config.num_hidden_layers = active
    return active


def build_prompt(question, context_mode):
    if context_mode == "registry":
        return REGISTRY_CONTEXT + "\n\nQ: " + question + "\nA:"
    elif context_mode == "ace":
        return ACE_CONTEXT + "\n\nQ: " + question + "\nA:"
    return "Q: " + question + "\nA:"


def run():
    base = Path(__file__).parent.parent.parent.parent
    out = base / "research_tracks/sdgi/phase4a_1.5b_truncation/data"
    questions = get_test_questions()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    results = []

    for ratio in DEPTH_RATIOS:
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
        total = len(model.model.layers)
        active = set_active_layers(model, ratio)
        print(f"\nDepth: {ratio:.0%} ({active}/{total})")

        for qd in questions:
            for mode in CONTEXT_MODES:
                prompt = build_prompt(qd["q"], mode)
                inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
                start = time.time()
                try:
                    with torch.no_grad():
                        outputs = model.generate(**inputs, max_new_tokens=60, temperature=0.0, do_sample=False, pad_token_id=tokenizer.eos_token_id)
                    answer = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
                except:
                    answer = "[ERROR]"
                elapsed = time.time() - start
                results.append(ContextResult(qd["q"], qd["class"], ratio, active, total, mode, answer, elapsed))
                
                # Quick hallucination check
                h = []
                if "web ui" in answer.lower() and ("有" in answer or "支持" in answer or "可以" in answer or "yes" in answer.lower()): h.append("WebUI")
                if "pdf" in answer.lower() and ("支持" in answer or "可以" in answer or "yes" in answer.lower()): h.append("PDF")
                if "crawler" in answer.lower() and "不是" not in answer: h.append("crawler")
                s = "❌ " + ",".join(h) if h else "✅"
                print(f"  {ratio:.0%} {mode:8s} | {qd['q'][:15]:15s} | {s:20s} | {answer[:60]}")

        del model; gc.collect(); torch.cuda.empty_cache()

    # Save
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "context_truncation_results.json", "w", encoding="utf-8") as f:
        json.dump({"experiment": "41A-ext", "runs": len(results), "results": [asdict(r) for r in results]}, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(results)} results")


if __name__ == "__main__":
    run()
