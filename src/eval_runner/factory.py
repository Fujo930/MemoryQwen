"""
MemoryQwen — Eval Runner Factory
"""

from src.eval_runner.runner import EvalRunner
from src.eval_runner.models import EvalRunConfig


def create_eval_runner(config, agent_service, run_config: EvalRunConfig = None):
    if run_config is None:
        run_config = EvalRunConfig()
    return EvalRunner(config, agent_service, run_config)
