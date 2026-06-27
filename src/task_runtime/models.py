"""
MemoryQwen — TaskRuntime 数据模型
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

VALID_STATUSES = {"pending", "running", "paused", "completed", "failed", "cancelled"}
VALID_TYPES = {
    "ingestion", "index_refresh", "profile_eval", "model_chat",
    "error_learning", "strategy_learning", "embedding", "reasoning", "custom",
}
VALID_PAUSE_REASONS = {
    "gpu_light_yield", "gpu_game_mode", "gpu_full_yield",
    "user_pause", "error", "unknown",
}

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "pending":   {"running", "cancelled"},
    "running":   {"paused", "completed", "failed", "cancelled"},
    "paused":    {"running", "cancelled"},
    "completed": set(),
    "failed":    set(),
    "cancelled": set(),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TaskRecord:
    task_id: str = ""
    task_type: str = "custom"
    title: str = ""
    status: str = "pending"
    progress_current: int = 0
    progress_total: int = 0
    progress_message: str = ""
    created_at: str = ""
    updated_at: str = ""
    started_at: str = ""
    completed_at: str = ""
    paused_at: str = ""
    pause_reason: str = ""
    error_message: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class TaskTransition:
    task_id: str = ""
    from_status: str = ""
    to_status: str = ""
    reason: str = ""
    timestamp: str = ""
