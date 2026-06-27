"""
MemoryQwen — ErrorLearningService
用户纠错记录 + 错误经验管理。
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from src.agent.models import CorrectionRequest, CorrectionResponse

logger = logging.getLogger(__name__)

ERROR_STORE = "error_store"
RECORD_KIND = "error_case"
DEFAULT_FAILURE_TYPE = "general"
DEFAULT_STRATEGY_TEMPLATE = (
    "遇到类似问题时，参考正确回答，避免重复错误。"
)


class ErrorLearningService:
    """错误学习服务"""

    def __init__(self, config: Any, store):
        self.config = config
        self.store = store

    async def record_correction(
        self, request: CorrectionRequest
    ) -> CorrectionResponse:
        """记录一条用户纠错"""
        if not request.wrong_answer.strip():
            raise ValueError("wrong_answer 不能为空")
        if not request.correct_answer.strip():
            raise ValueError("correct_answer 不能为空")

        failure_type = request.failure_type.strip() or DEFAULT_FAILURE_TYPE
        strategy = request.strategy.strip() or self._default_strategy()

        # 计算去重 hash
        correction_hash = hashlib.sha256(
            (request.session_id + request.user_message +
             request.wrong_answer + request.correct_answer).encode("utf-8")
        ).hexdigest()

        # 去重检查
        exists = await self.store.exists_by_metadata(ERROR_STORE, {
            "correction_hash": correction_hash,
        })
        if exists:
            logger.info("Duplicate correction, skipping: %s", correction_hash[:16])
            return CorrectionResponse(
                error_id="",
                saved=False,
                failure_type=failure_type,
                strategy=strategy,
                metadata={"reason": "duplicate"},
            )

        # 构建 content
        content = self._build_content(request, failure_type, strategy)

        # 构建 title
        short_task = request.user_message[:50] if request.user_message else "unknown"
        title = f"error_case:{failure_type}:{short_task}"

        # metadata
        strategy_source = "user" if request.strategy.strip() else "auto"
        metadata = {
            "record_kind": RECORD_KIND,
            "session_id": request.session_id,
            "failure_type": failure_type,
            "strategy": strategy,
            "has_strategy": True,  # 始终为 true（有默认生成）
            "strategy_source": strategy_source,
            "correction_hash": correction_hash,
            "created_by": "user_correction",
        }

        # 写入
        error_id = await self.store.add(ERROR_STORE, {
            "task": request.user_message,
            "wrong_answer": request.wrong_answer,
            "correct_answer": request.correct_answer,
            "failure_type": failure_type,
            "strategy": strategy,
            "metadata": metadata,
        })

        logger.info("Error recorded: %s (%s)", error_id[:8], failure_type)

        return CorrectionResponse(
            error_id=error_id,
            saved=True,
            failure_type=failure_type,
            strategy=strategy,
            metadata={
                "correction_hash": correction_hash,
                "strategy_source": strategy_source,
            },
        )

    def _build_content(
        self, request: CorrectionRequest, failure_type: str, strategy: str
    ) -> str:
        """构建 error_store content 文本"""
        return (
            f"Task: {request.user_message or '用户未提供原始问题'}\n"
            f"Wrong Answer: {request.wrong_answer}\n"
            f"Correct Answer: {request.correct_answer}\n"
            f"Failure Type: {failure_type}\n"
            f"Strategy: {strategy}"
        )

    def _default_strategy(self) -> str:
        return DEFAULT_STRATEGY_TEMPLATE
