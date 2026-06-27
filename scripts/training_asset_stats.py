#!/usr/bin/env python3
"""MemoryQwen Training Asset Stats v2 — Disk / File / Content / DB metrics"""
import sys, os, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKIP = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", ".hermes"}

def walk(p: Path):
    if not p.exists(): return
    for root, dnames, fnames in os.walk(str(p)):
        dnames[:] = [d for d in dnames if d not in SKIP]
        for fn in fnames:
            yield Path(root) / fn

def dir_size(p: Path):
    return sum(f.stat().st_size for f in walk(p)) if p.exists() else 0

def list_files(p: Path, ext=None):
    return [f for f in walk(p) if ext is None or f.suffix.lower() == ext] if p.exists() else []

def read_text(p: Path):
    try: return p.read_text(encoding="utf-8", errors="replace")
    except: return ""

def count_chars_and_words(text: str):
    chars = len(text)
    words = len(text.split())
    # rough token est: zh chars * 1.1 + en words * 1.3
    zh = len(re.findall(r'[\u4e00-\u9fff]', text))
    en = max(words - zh, 0)
    tokens = int(zh * 1.1 + en * 1.3)
    return chars, words, tokens

def db_count(table: str) -> int:
    import sqlite3
    db = BASE / "memory/memoryqwen.db"
    if not db.exists(): return 0
    try:
        c = sqlite3.connect(str(db))
        r = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        c.close()
        return r[0] if r else 0
    except: return 0

def db_count_tasks() -> int:
    import sqlite3
    db = BASE / "memory/tasks.db"
    if not db.exists(): return 0
    try:
        c = sqlite3.connect(str(db))
        r = c.execute("SELECT COUNT(*) FROM task_records").fetchone()
        c.close()
        return r[0] if r else 0
    except: return 0

# ─── Metrics ─────────────────────────────────────────

# A. Disk
disk = {}
disk["project_total_mb"] = dir_size(BASE) / 1024 / 1024
disk["training_packs_mb"] = dir_size(BASE / "training_packs") / 1024 / 1024
disk["training_logs_mb"] = dir_size(BASE / "training_logs") / 1024 / 1024
disk["memory_mb"] = dir_size(BASE / "memory") / 1024 / 1024
disk["memory_sources_mb"] = dir_size(BASE / "memory/sources") / 1024 / 1024
disk["docs_mb"] = dir_size(BASE / "docs") / 1024 / 1024
disk["examples_mb"] = dir_size(BASE / "examples") / 1024 / 1024
disk["tests_mb"] = dir_size(BASE / "tests") / 1024 / 1024
disk["sqlite_db_mb"] = (dir_size(BASE / "memory/memoryqwen.db") + dir_size(BASE / "memory/tasks.db")) / 1024 / 1024

# B. Files
training_sources = list_files(BASE / "training_packs", ".md")
archived = list_files(BASE / "memory/sources")
log_files = list_files(BASE / "training_logs", ".md")

file_metrics = {}
file_metrics["total_files"] = sum(1 for _ in walk(BASE))
file_metrics["training_source_files"] = len(training_sources)
file_metrics["archived_source_files"] = len(archived)
file_metrics["training_topics"] = len([d for d in (BASE/"training_packs").iterdir() if d.is_dir()]) if (BASE/"training_packs").exists() else 0
file_metrics["log_files"] = len(log_files)

# C. Content
def content_stats(files):
    tc = tw = tt = 0
    for f in files:
        txt = read_text(f)
        c, w, t = count_chars_and_words(txt)
        tc += c; tw += w; tt += t
    return tc, tw, tt

tp_chars, tp_words, tp_tokens = content_stats(training_sources)
src_chars, src_words, src_tokens = content_stats(archived)

# count questions/traps/answers from dedicated files
def count_lines_in(pattern):
    files = list(BASE.rglob(f"training_packs/*/{pattern}"))
    total = 0
    for f in files:
        txt = read_text(f)
        # count lines that look like numbered questions
        total += len(re.findall(r'^\d+[\.\、）\)]\s', txt, re.MULTILINE))
    return total

content = {}
content["total_chars"] = tp_chars + src_chars
content["total_words_approx"] = tp_words + src_words
content["estimated_tokens"] = tp_tokens + src_tokens
content["training_pack_chars"] = tp_chars
content["memory_sources_chars"] = src_chars
content["questions_count"] = count_lines_in("questions.md")
content["trap_questions_count"] = count_lines_in("trap_questions.md")
content["answer_key_count"] = sum(len(re.findall(r'^- ', read_text(f), re.MULTILINE)) for f in BASE.rglob("training_packs/*/answer_key.md"))
content["strategies_count"] = db_count("strategy_store")

# D. Database
db = {}
db["knowledge_store_count"] = db_count("knowledge_store")
db["chat_memory_count"] = db_count("chat_messages")
db["error_store_count"] = db_count("error_store")
db["strategy_store_count"] = db_count("strategy_store")
db["task_count"] = db_count_tasks()

# ─── Output ─────────────────────────────────────────

print(f"Project: {BASE}")
print()

print("A. Disk Metrics")
for k, v in disk.items():
    print(f"  {k:<25s} {v:.2f} MB")

print(f"\nB. File Metrics")
for k, v in file_metrics.items():
    print(f"  {k:<25s} {v}")

print(f"\nC. Content Metrics")
for k, v in content.items():
    print(f"  {k:<25s} {v:,}")

print(f"\nD. Database Metrics")
for k, v in db.items():
    print(f"  {k:<25s} {v}")

# ─── Multi-target progress ──────────────────────────
print(f"\n=== Progress ===")

targets = {
    "training_packs_mb": (disk.get("training_packs_mb", 0), 1024),
    "estimated_tokens": (content.get("estimated_tokens", 0), 10_000_000),
    "knowledge_chunks": (db.get("knowledge_store_count", 0), 10_000),
    "questions": (content.get("questions_count", 0), 5_000),
    "error_cases": (db.get("error_store_count", 0), 500),
    "strategies": (content.get("strategies_count", 0), 200),
}

for label, (val, target) in targets.items():
    pct = round(val / target * 100, 2) if target else 0
    bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
    print(f"  {label:<25s} {pct:6.2f}%  {bar}  ({val:,}/{target:,})")
