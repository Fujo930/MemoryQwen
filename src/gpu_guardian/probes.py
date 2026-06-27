"""
MemoryQwen — GPU Probes
第一版使用 nvidia-smi CLI，不直接依赖 pynvml。
"""

from __future__ import annotations

import subprocess
import logging

from src.gpu_guardian.models import GpuSnapshot, GpuProcess

logger = logging.getLogger(__name__)


class NvidiaSmiProbe:
    """通过 nvidia-smi 命令采集 GPU 信息"""

    @staticmethod
    def is_available() -> bool:
        """检查 nvidia-smi 是否可用"""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True, timeout=5,
            )
            return result.returncode == 0 and bool(result.stdout.strip())
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return False

    @staticmethod
    def snapshot() -> GpuSnapshot:
        """采集 GPU 快照"""
        snapshot = GpuSnapshot(available=False)

        if not NvidiaSmiProbe.is_available():
            snapshot.raw = {"error": "nvidia-smi not available"}
            return snapshot

        # GPU 信息
        try:
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=name,memory.total,memory.used,utilization.gpu,temperature.gpu",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0 and result.stdout.strip():
                line = result.stdout.strip().split("\n")[0]
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 5:
                    snapshot.available = True
                    snapshot.gpu_name = parts[0]
                    snapshot.total_vram_mb = int(float(parts[1]))
                    snapshot.used_vram_mb = int(float(parts[2]))
                    snapshot.gpu_util_percent = float(parts[3])
                    snapshot.temperature_c = float(parts[4])
        except Exception as e:
            logger.warning("nvidia-smi GPU query failed: %s", e)
            snapshot.raw["gpu_query_error"] = str(e)

        # 进程信息
        if snapshot.available:
            try:
                result = subprocess.run(
                    [
                        "nvidia-smi",
                        "--query-compute-apps=pid,process_name,used_memory",
                        "--format=csv,noheader,nounits",
                    ],
                    capture_output=True, text=True, timeout=10,
                )
                if result.returncode == 0 and result.stdout.strip():
                    for line in result.stdout.strip().split("\n"):
                        parts = [p.strip() for p in line.split(",", 2)]
                        if len(parts) >= 2:
                            try:
                                pid = int(parts[0])
                            except ValueError:
                                continue
                            name = parts[1]
                            vram = int(float(parts[2])) if len(parts) > 2 and parts[2] else 0
                            snapshot.processes.append(GpuProcess(
                                pid=pid, name=name, used_vram_mb=vram,
                            ))
            except Exception as e:
                logger.warning("nvidia-smi process query failed: %s", e)
                snapshot.raw["process_query_error"] = str(e)

        return snapshot
