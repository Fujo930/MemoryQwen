"""
GPU Guardian 测试 (≥24)
"""

from __future__ import annotations

import json
import pytest
import tempfile
from pathlib import Path

from src.gpu_guardian.models import GpuSnapshot, GpuProcess, GuardianState
from src.gpu_guardian.probes import NvidiaSmiProbe
from src.gpu_guardian.policy import PolicyEngine
from src.gpu_guardian.service import GpuGuardianService


# ─── Mock Config ───────────────────────────────────────

class MockGuardianConfig:
    enabled = True
    provider = "nvidia_smi"
    light_yield_vram_ratio = 0.55
    full_yield_vram_ratio = 0.85
    game_mode_gpu_util_percent = 70
    game_process_names = ["Cyberpunk2077.exe", "cs2.exe", "Minecraft.exe"]
    creative_process_names = ["blender.exe", "obs64.exe"]
    full_yield_process_names = []


class MockConfig:
    gpu_guardian = MockGuardianConfig()


# ─── Models Tests ──────────────────────────────────────

class TestGpuProcess:
    def test_defaults(self):
        p = GpuProcess()
        assert p.pid == 0
        assert p.name == ""


class TestGpuSnapshot:
    def test_defaults(self):
        s = GpuSnapshot()
        assert s.available is False
        assert s.used_vram_ratio == 0.0

    def test_vram_ratio(self):
        s = GpuSnapshot(total_vram_mb=100, used_vram_mb=30)
        assert s.used_vram_ratio == 0.3


class TestGuardianState:
    def test_defaults(self):
        s = GuardianState()
        assert s.mode == "normal"


# ─── Probe Tests ───────────────────────────────────────

class TestNvidiaSmiProbe:
    def test_unavailable(self, monkeypatch):
        def mock_is_avail():
            return False
        monkeypatch.setattr(NvidiaSmiProbe, "is_available", mock_is_avail)
        snap = NvidiaSmiProbe.snapshot()
        assert snap.available is False
        assert "error" in snap.raw

    def test_parse_gpu_snapshot(self, monkeypatch):
        def mock_avail(): return True
        monkeypatch.setattr(NvidiaSmiProbe, "is_available", mock_avail)

        import subprocess
        class FakeResult:
            returncode = 0
            stdout = "RTX 4080, 16384, 4096, 45, 62\n"
        def mock_run(cmd, **kw):
            if "gpu" in str(cmd) and "process" not in str(cmd):
                return FakeResult()
            return type('r', (), {'returncode': 0, 'stdout': ''})()
        monkeypatch.setattr(subprocess, "run", mock_run)

        snap = NvidiaSmiProbe.snapshot()
        assert snap.available is True
        assert snap.gpu_name == "RTX 4080"
        assert snap.total_vram_mb == 16384
        assert snap.used_vram_mb == 4096
        assert snap.gpu_util_percent == 45.0
        assert snap.temperature_c == 62.0

    def test_parse_processes(self, monkeypatch):
        def mock_avail(): return True
        monkeypatch.setattr(NvidiaSmiProbe, "is_available", mock_avail)

        import subprocess
        call_count = [0]
        class FakeGpu:
            returncode = 0
            stdout = "RTX 4080, 16384, 8000, 60, 70\n"
        class FakeProc:
            returncode = 0
            stdout = "1234, Cyberpunk2077.exe, 2048\n5678, C:/Games/test.exe, 1024\n"
        def mock_run(cmd, **kw):
            call_count[0] += 1
            if call_count[0] == 1:
                return FakeGpu()
            return FakeProc()
        monkeypatch.setattr(subprocess, "run", mock_run)

        snap = NvidiaSmiProbe.snapshot()
        assert len(snap.processes) == 2
        assert snap.processes[0].pid == 1234
        assert snap.processes[0].name == "Cyberpunk2077.exe"
        assert snap.processes[0].used_vram_mb == 2048

    def test_empty_process_output(self, monkeypatch):
        def mock_avail(): return True
        monkeypatch.setattr(NvidiaSmiProbe, "is_available", mock_avail)
        import subprocess
        class FakeGpu:
            returncode = 0; stdout = "GPU, 100, 50, 30, 50\n"
        class FakeEmpty:
            returncode = 0; stdout = ""
        call = [0]
        def mock_run(cmd, **kw):
            call[0] += 1
            return FakeGpu() if call[0] == 1 else FakeEmpty()
        monkeypatch.setattr(subprocess, "run", mock_run)
        snap = NvidiaSmiProbe.snapshot()
        assert snap.available is True
        assert len(snap.processes) == 0


# ─── Policy Tests ──────────────────────────────────────

def make_snap(vram_ratio=0.0, util=0.0, processes=None):
    s = GpuSnapshot(available=True, total_vram_mb=16000, used_vram_mb=int(16000*vram_ratio),
                    gpu_util_percent=util)
    if processes:
        s.processes = processes
    return s


AP = PolicyEngine(MockConfig())


class TestPolicy:
    def test_normal(self):
        state = AP.evaluate(make_snap(vram_ratio=0.1, util=10))
        assert state.mode == "normal"

    def test_light_yield_by_vram(self):
        state = AP.evaluate(make_snap(vram_ratio=0.6, util=30))
        assert state.mode == "light_yield"

    def test_game_mode_by_process(self):
        state = AP.evaluate(make_snap(processes=[GpuProcess(pid=1, name="Cyberpunk2077.exe")]))
        assert state.mode == "game_mode"

    def test_game_mode_by_creative_process(self):
        state = AP.evaluate(make_snap(processes=[GpuProcess(pid=1, name="blender.exe")]))
        assert state.mode == "game_mode"

    def test_game_mode_by_util(self):
        state = AP.evaluate(make_snap(vram_ratio=0.3, util=85))
        assert state.mode == "game_mode"

    def test_full_yield_by_vram(self):
        state = AP.evaluate(make_snap(vram_ratio=0.9, util=50))
        assert state.mode == "full_yield"

    def test_priority_full_over_game(self):
        # VRAM high even with game process → full_yield wins
        state = AP.evaluate(make_snap(vram_ratio=0.9, util=50, processes=[GpuProcess(pid=1, name="cs2.exe")]))
        assert state.mode == "full_yield"

    def test_case_insensitive(self):
        state = AP.evaluate(make_snap(processes=[GpuProcess(pid=1, name="MINECRAFT.EXE")]))
        assert state.mode == "game_mode"

    def test_basename_windows_path(self):
        state = AP.evaluate(make_snap(processes=[GpuProcess(pid=1, name=r"C:\Program Files\Game\Cyberpunk2077.exe")]))
        assert state.mode == "game_mode"

    def test_recommended_actions_normal(self):
        state = AP.evaluate(make_snap(vram_ratio=0.1))
        assert "allow_14b" in state.recommended_actions

    def test_recommended_actions_light_yield(self):
        state = AP.evaluate(make_snap(vram_ratio=0.6))
        assert "prefer_7b" in state.recommended_actions

    def test_recommended_actions_game_mode(self):
        state = AP.evaluate(make_snap(processes=[GpuProcess(pid=1, name="cs2.exe")]))
        assert "disable_deep_reasoning" in state.recommended_actions

    def test_recommended_actions_full_yield(self):
        state = AP.evaluate(make_snap(vram_ratio=0.9))
        assert "pause_all_ai_tasks" in state.recommended_actions

    def test_snapshot_unavailable_returns_normal(self):
        snap = GpuSnapshot(available=False)
        state = AP.evaluate(snap)
        assert state.mode == "normal"
        assert state.reason == "gpu_unavailable"


# ─── Service Tests ─────────────────────────────────────

class TestGuardianService:
    @pytest.mark.asyncio
    async def test_check_once(self, monkeypatch):
        fake_snap = GpuSnapshot(available=True, total_vram_mb=16000, used_vram_mb=2000,
                                gpu_util_percent=15)
        def fake_snapshot(_self):
            return fake_snap
        monkeypatch.setattr(NvidiaSmiProbe, "snapshot", fake_snapshot)

        svc = GpuGuardianService(MockConfig())
        state = await svc.check_once()
        assert state.mode == "normal"

    def test_to_dict(self):
        svc = GpuGuardianService(MockConfig())
        state = GuardianState(mode="game_mode", reason="test")
        d = svc.to_dict(state)
        assert d["mode"] == "game_mode"
        assert "reason" in d


# ─── CLI Parser Tests ──────────────────────────────────

class TestGuardianCLI:
    def test_status_parser(self):
        from src.cli import build_parser
        parser = build_parser()
        args = parser.parse_args(["guardian", "status"])
        assert args.command == "guardian"
        assert args.guardian_cmd == "status"

    def test_json_parser(self):
        from src.cli import build_parser
        parser = build_parser()
        args = parser.parse_args(["guardian", "json"])
        assert args.guardian_cmd == "json"
