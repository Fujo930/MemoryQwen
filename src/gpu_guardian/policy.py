"""
MemoryQwen — GPU Policy Engine
根据配置和快照判断当前模式。
"""

from __future__ import annotations

import os
from typing import Any

from src.gpu_guardian.models import GpuSnapshot, GuardianState

RECOMMENDED_NORMAL = [
    "allow_14b",
    "allow_background_ingestion",
    "allow_index_refresh",
]
RECOMMENDED_LIGHT_YIELD = [
    "pause_background_ingestion",
    "pause_index_refresh",
    "prefer_7b",
]
RECOMMENDED_GAME_MODE = [
    "pause_background_tasks",
    "prefer_7b",
    "disable_deep_reasoning",
]
RECOMMENDED_FULL_YIELD = [
    "pause_all_ai_tasks",
    "unload_models_if_supported",
    "keep_memory_store_only",
]


class PolicyEngine:
    """让路策略引擎"""

    def __init__(self, config: Any):
        self.config = config
        cfg = config.gpu_guardian

        self.light_yield_vram = cfg.light_yield_vram_ratio
        self.full_yield_vram = cfg.full_yield_vram_ratio
        self.game_util = cfg.game_mode_gpu_util_percent
        self.game_names = [n.lower() for n in cfg.game_process_names]
        self.creative_names = [n.lower() for n in cfg.creative_process_names]
        self.full_yield_names = [n.lower() for n in cfg.full_yield_process_names]

    def evaluate(self, snapshot: GpuSnapshot) -> GuardianState:
        """评估当前 GPU 状态，返回 GuardianState"""

        if not snapshot.available:
            return GuardianState(
                mode="normal",
                reason="gpu_unavailable",
                gpu_snapshot=snapshot,
                recommended_actions=RECOMMENDED_NORMAL,
            )

        # 收集命中的进程名
        matched = []
        for proc in snapshot.processes:
            base = os.path.basename(proc.name).lower()
            full = proc.name.lower()

            if any(n in base or n in full for n in self.full_yield_names):
                matched.append(proc.name)
                continue
            if any(n in base or n in full for n in self.game_names):
                matched.append(proc.name)
                continue
            if any(n in base or n in full for n in self.creative_names):
                matched.append(proc.name)
                continue

        # 判断优先级：full_yield > game_mode > light_yield > normal
        # Full yield: 命中 full_yield names 或 VRAM >= full_yield_vram
        full_hit = any(
            any(n in os.path.basename(m).lower() or n in m.lower() for n in self.full_yield_names)
            for m in matched
        )
        if full_hit or snapshot.used_vram_ratio >= self.full_yield_vram:
            return GuardianState(
                mode="full_yield",
                reason=self._reason("full_yield", full_hit, snapshot),
                gpu_snapshot=snapshot,
                matched_processes=matched,
                recommended_actions=RECOMMENDED_FULL_YIELD,
            )

        # Game mode: 命中 game/creative names 或 util >= threshold
        game_hit = any(
            any(n in os.path.basename(m).lower() or n in m.lower()
                for n in self.game_names + self.creative_names)
            for m in matched
        )
        if game_hit or snapshot.gpu_util_percent >= self.game_util:
            return GuardianState(
                mode="game_mode",
                reason=self._reason("game_mode", game_hit, snapshot),
                gpu_snapshot=snapshot,
                matched_processes=matched,
                recommended_actions=RECOMMENDED_GAME_MODE,
            )

        # Light yield
        if snapshot.used_vram_ratio >= self.light_yield_vram:
            return GuardianState(
                mode="light_yield",
                reason=self._reason("light_yield", False, snapshot),
                gpu_snapshot=snapshot,
                matched_processes=matched,
                recommended_actions=RECOMMENDED_LIGHT_YIELD,
            )

        return GuardianState(
            mode="normal",
            reason=self._reason("normal", False, snapshot),
            gpu_snapshot=snapshot,
            matched_processes=matched,
            recommended_actions=RECOMMENDED_NORMAL,
        )

    def _reason(self, mode: str, has_process_match: bool, snapshot: GpuSnapshot) -> str:
        if mode == "normal":
            return "all metrics within normal range"
        elif mode == "light_yield":
            return f"vram usage {snapshot.used_vram_ratio:.1%} >= light_yield threshold"
        elif mode == "game_mode":
            if has_process_match:
                return "gaming or creative process detected"
            return f"gpu utilization {snapshot.gpu_util_percent:.0f}% >= game_mode threshold"
        elif mode == "full_yield":
            if has_process_match:
                return "full_yield process detected"
            return f"vram usage {snapshot.used_vram_ratio:.1%} >= full_yield threshold"
        return mode
