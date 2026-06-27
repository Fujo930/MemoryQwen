"""
MemoryQwen — Eval Question Loader
Loads validation questions from Markdown format.
"""

from __future__ import annotations
import logging, re
from pathlib import Path
from src.eval_runner.models import EvalQuestion

logger = logging.getLogger(__name__)

# Parses lines like: "key: value" or "key: value1, value2"
KV_RE = re.compile(r"^([a-z_]+):\s*(.+)$", re.IGNORECASE)


def _parse_block(block: str) -> EvalQuestion | None:
    """Parse one Q-block. Returns None if malformed."""
    q = EvalQuestion()
    lines = block.strip().split("\n")
    for line in lines:
        m = KV_RE.match(line)
        if not m:
            continue
        key, val = m.group(1).strip().lower(), m.group(2).strip()
        if key == "question_id" or key == "## q":
            # "## Q001" format — extract the number
            n = re.search(r"Q?(\d+)", line, re.IGNORECASE)
            if n:
                q.question_id = f"Q{n.group(1).zfill(3)}"
        elif key == "topic":
            q.topic = val
        elif key == "question":
            q.question = val
        elif key == "expected_answer":
            q.expected_answer = val
        elif key == "expected_sources":
            q.expected_sources = [s.strip() for s in val.split(",") if s.strip()]
        elif key == "guard_expected":
            q.guard_expected = val.lower() in ("yes", "true", "1")
        elif key == "failure_type_if_wrong":
            q.failure_type_if_wrong = val
        elif key == "trap_level":
            q.trap_level = val

    # Fallback: if question_id is missing but question exists, generate one
    if not q.question_id and q.question:
        q.question_id = f"Q{hash(q.question) % 10000:04d}"
    if not q.question:
        logger.warning("Ignoring question block with no question text")
        return None
    return q


def load_questions_from_markdown(file_path: str | Path) -> list[EvalQuestion]:
    """Load questions from a single .md file."""
    path = Path(file_path)
    if not path.exists():
        logger.warning(f"File not found: {path}")
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return _parse_all_blocks(text)


def load_questions_from_directory(dir_path: str | Path, topic_filter: str = "",
                                   max_questions: int = 0,
                                   shuffle: bool = False) -> list[EvalQuestion]:
    """Load all .md files recursively from a directory."""
    path = Path(dir_path)
    if not path.is_dir():
        return []
    questions = []
    for fp in sorted(path.rglob("*.md")):
        qs = load_questions_from_markdown(fp)
        if topic_filter:
            qs = [q for q in qs if topic_filter.lower() in q.topic.lower()]
        questions.extend(qs)
    if shuffle:
        import random
        random.shuffle(questions)
    if max_questions and max_questions > 0:
        questions = questions[:max_questions]
    return questions


def _parse_all_blocks(text: str) -> list[EvalQuestion]:
    """Parse all `## Q...` blocks from the text."""
    # Split on ## Q prefix
    blocks = re.split(r"\n(?=##\s)", text)
    questions = []
    for block in blocks:
        q = _parse_block(block)
        if q and q.question:
            questions.append(q)
    return questions
