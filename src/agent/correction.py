"""
MemoryQwen — Correction Handler 错误记录机制
检测用户的纠正意图，自动写入 error_store
"""

from __future__ import annotations

import re
import logging
from typing import Any

from src.memory_bus.error_store import ErrorStore

logger = logging.getLogger(__name__)

# 纠正关键词
CORRECTION_PATTERNS = [
    r"不对",
    r"错了",
    r"不是",
    r"不正确",
    r"错误",
    r"正确的是",
    r"应该是",
    r"其实是",
    r"更正",
    r"纠正",
    r"修正",
    r"你说错了",
    r"你说得不对",
    r"不是这样的",
    r"错了，",
    r"不对，",
    r"No[，,.]",
    r"Wrong[，,.]",
    r"Actually[，,.]",
    r"Correction[：:]",
]

# 简单回答模式（用于识别用户对模型回答的反馈）
SIMPLE_ANSWER_PATTERN = r"(?:等于|是|应该是|正确的是)(.+)$"


class CorrectionHandler:
    """错误记录处理器"""

    def __init__(self, error_store: ErrorStore, config: Any | None = None):
        self.error_store = error_store
        self.config = config or {}
        self.threshold = getattr(config.agent.error_learning, "correction_threshold", 0.7) if config else 0.7

    async def detect_and_record(
        self,
        user_message: str,
        last_assistant_response: str | None = None,
        history: list[dict] | None = None,
    ) -> dict | None:
        """检测纠正意图并记录错误"""
        is_correction, correction_text = self._is_correction(user_message)
        if not is_correction:
            return None

        # 尝试提取纠正内容
        correct_answer = self._extract_correct_answer(user_message)
        trigger_query = self._find_trigger_query(history) if history else ""

        if not trigger_query:
            # 尝试从纠正文本推导触发查询
            trigger_query = user_message[:100]

        if not correct_answer:
            correct_answer = correction_text or user_message

        # 记录错误
        error_id = await self.error_store.add_error(
            trigger_query=trigger_query,
            wrong_answer=last_assistant_response or "unknown",
            correct_answer=correct_answer,
            root_cause="用户纠正",
            fix_strategy=f"根据用户纠正更新回答: {correct_answer}",
            error_type="user_correction",
            tags=["correction"],
        )

        logger.info("Correction recorded: %s → %s", trigger_query[:50], correct_answer[:50])
        return {
            "error_id": error_id,
            "trigger_query": trigger_query,
            "correct_answer": correct_answer,
        }

    def _is_correction(self, message: str) -> tuple[bool, str]:
        """检测是否为纠正消息"""
        for pattern in CORRECTION_PATTERNS:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return True, message
        return False, ""

    def _extract_correct_answer(self, message: str) -> str:
        """提取纠正中的正确答案"""
        match = re.search(SIMPLE_ANSWER_PATTERN, message)
        if match:
            return match.group(1).strip()
        return ""

    def _find_trigger_query(self, history: list[dict]) -> str:
        """从历史记录中找到触发当前对话的用户问题"""
        for msg in reversed(history):
            if msg.get("role") == "user":
                return msg.get("content", "")
        return ""
