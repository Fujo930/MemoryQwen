#!/usr/bin/env python3
"""Quick eval question quality check — counts, format validation"""
import re, sys
from pathlib import Path

d = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("training_packs/14_validation_questions_expanded")
if not d.exists():
    print(f"Directory not found: {d}")
    sys.exit(0)

total = 0
with_question = 0
with_expected = 0
with_topic = 0
issues = []

for fp in d.rglob("*.md"):
    text = fp.read_text(encoding="utf-8", errors="replace")
    blocks = re.split(r"\n(?=##\sQ\d+)", text)
    for b in blocks:
        if not b.strip():
            continue
        total += 1
        if re.search(r"question:", b): with_question += 1
        if re.search(r"expected_answer:", b): with_expected += 1
        if re.search(r"topic:", b): with_topic += 1

print(f"Eval Question Quality Check")
print(f"  total blocks:     {total}")
print(f"  with question:    {with_question} ({with_question/total*100:.0f}%)" if total else "  0")
print(f"  with expected:    {with_expected} ({with_expected/total*100:.0f}%)" if total else "  0")
print(f"  with topic:       {with_topic} ({with_topic/total*100:.0f}%)" if total else "  0")
status = "PASS" if total > 0 and with_question == total else "WARN"
print(f"  status:           {status}")
