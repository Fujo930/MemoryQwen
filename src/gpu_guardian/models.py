"""
MemoryQwen — GPU Guardian 数据模型
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GpuProcess:
    """GPU 上的进程信息"""
    pid: int = 0
    name: str = ""
    used_vram_mb: int = 0
    gpu_util_percent: float = 0.0


@dataclass
class GpuSnapshot:
    """GPU 状态快照"""
    available: bool = False
    gpu_name: str = ""
    total_vram_mb: int = 0
    used_vram_mb: int = 0
    gpu_util_percent: float = 0.0
    temperature_c: float = 0.0
    processes: list[GpuProcess] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    @property
    def used_vram_ratio(self) -> float:
        if self.total_vram_mb == 0:
            return 0.0
        return self.used_vram_mb / self.total_vram_mb


@dataclass
class GuardianState:
    """Guardian 决策结果"""
    mode: str = "normal"          # normal | light_yield | game_mode | full_yield
    reason: str = ""
    gpu_snapshot: GpuSnapshot = field(default_factory=GpuSnapshot)
    matched_processes: list[str] = field(default_factory=list)
    recommended_actions: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
