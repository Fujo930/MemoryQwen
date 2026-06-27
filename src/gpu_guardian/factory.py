"""
MemoryQwen — GPU Guardian 工厂
"""

from src.gpu_guardian.service import GpuGuardianService


def create_guardian_service(config):
    """创建 GpuGuardianService 实例"""
    return GpuGuardianService(config)
