"""
MemoryQwen — GPU Guardian Service
"""

from __future__ import annotations

from typing import Any

from src.gpu_guardian.probes import NvidiaSmiProbe
from src.gpu_guardian.policy import PolicyEngine
from src.gpu_guardian.models import GuardianState


class GpuGuardianService:
    """GPU Guardian 服务"""

    def __init__(self, config: Any, probe=None, policy_engine=None):
        self.config = config
        self.probe = probe or NvidiaSmiProbe()
        self.policy_engine = policy_engine or PolicyEngine(config)

    async def check_once(self) -> GuardianState:
        """单次检查 GPU 状态并返回决策"""
        snapshot = self.probe.snapshot()
        return self.policy_engine.evaluate(snapshot)

    def to_dict(self, state: GuardianState) -> dict:
        """将 GuardianState 转为可序列化 dict"""
        return {
            "mode": state.mode,
            "reason": state.reason,
            "gpu_name": state.gpu_snapshot.gpu_name,
            "total_vram_mb": state.gpu_snapshot.total_vram_mb,
            "used_vram_mb": state.gpu_snapshot.used_vram_mb,
            "gpu_util_percent": state.gpu_snapshot.gpu_util_percent,
            "temperature_c": state.gpu_snapshot.temperature_c,
            "matched_processes": state.matched_processes,
            "recommended_actions": state.recommended_actions,
            "metadata": state.metadata,
        }
