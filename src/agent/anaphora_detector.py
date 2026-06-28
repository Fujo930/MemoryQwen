"""MemoryQwen — Anaphora-aware retrieval gate.

Detects short follow-up questions with pronouns (它/这个/那个/this/that)
and skips retrieval so recent chat context takes priority.
"""

from __future__ import annotations

ANAPHORA_MARKERS: list[str] = [
    "它", "他", "她", "这个", "那个", "这", "那",
    "this ", "that ", "it ",
]

def is_anaphora_followup(message: str) -> bool:
    """Return True if message is a short anaphoric follow-up question."""
    msg = message.strip()
    if len(msg) > 20:
        return False
    return any(m in msg for m in ANAPHORA_MARKERS)
