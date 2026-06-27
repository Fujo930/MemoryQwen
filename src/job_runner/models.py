"""
MemoryQwen — JobRunner 数据模型
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class JobResult:
    task_id: str = ""
    status: str = ""               # completed | paused | cancelled | failed
    processed: int = 0
    total: int = 0
    message: str = ""
    metadata: dict = field(default_factory=dict)
