"""
MemoryQwen — GuardianTaskPolicy
根据 Guardian recommended_actions 决定暂停哪些任务
"""

from __future__ import annotations

from src.task_runtime.models import TaskRecord


class GuardianTaskPolicy:
    """Guardian → Task 让路策略"""

    # 哪些 action 暂停哪些 task_type
    PAUSE_RULES: list[tuple[str, set[str]]] = [
        # (recommended_action_keyword, task_types_to_pause)
        ("pause_background_ingestion", {"ingestion"}),
        ("pause_index_refresh", {"index_refresh"}),
        ("pause_background_tasks", {
            "ingestion", "index_refresh", "profile_eval", "embedding", "reasoning",
        }),
        ("pause_all_ai_tasks", {
            "ingestion", "index_refresh", "profile_eval", "embedding",
            "reasoning", "model_chat",
        }),
    ]

    def evaluate(self, recommended_actions: list[str], running_tasks: list[TaskRecord]) -> list[str]:
        """返回应暂停的 task_id 列表"""
        to_pause: set[str] = set()
        for action in recommended_actions:
            for keyword, types in self.PAUSE_RULES:
                if keyword in action:
                    for t in running_tasks:
                        if t.task_type in types:
                            to_pause.add(t.task_id)

        return list(to_pause)
