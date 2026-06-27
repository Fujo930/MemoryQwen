"""
MemoryQwen — StrategyLearningService
从纠错记录生成可复用策略。
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from src.agent.models import CorrectionRequest

logger = logging.getLogger(__name__)

STRATEGY_STORE = "strategy_store"
RECORD_KIND = "strategy"


class StrategyLearningService:
    """策略学习服务"""

    def __init__(self, config: Any, store):
        self.config = config
        self.store = store

    async def upsert_strategy_from_correction(
        self, request: CorrectionRequest, error_id: str
    ) -> dict:
        """从纠错请求创建或更新策略记录"""
        strategy_text = request.strategy.strip()
        if not strategy_text:
            return {"created": False, "reason": "empty_strategy"}

        failure_type = request.failure_type.strip() or "general"

        # 计算 strategy_hash
        normalized = f"{failure_type.lower()}::{strategy_text.lower()}"
        strategy_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()

        # 检查是否已存在
        exists = await self.store.exists_by_metadata(STRATEGY_STORE, {
            "strategy_hash": strategy_hash,
        })

        if exists:
            # 更新 existing 策略
            return await self._update_existing(strategy_hash, error_id)

        # 新增策略
        return await self._create_new(
            request, strategy_text, failure_type, strategy_hash, error_id,
        )

    async def _create_new(
        self, request: CorrectionRequest, strategy_text: str,
        failure_type: str, strategy_hash: str, error_id: str,
    ) -> dict:
        """创建新策略记录"""
        short_title = request.user_message[:40] if request.user_message else "unknown"
        title = f"strategy:{failure_type}:{short_title}"

        # 构建 content
        content = (
            f"Strategy: {strategy_text}\n"
            f"Applies When: {failure_type}\n"
            f"Avoid: {request.wrong_answer[:200]}\n"
            f"Prefer: {request.correct_answer[:200]}"
        )

        metadata = {
            "record_kind": RECORD_KIND,
            "failure_type": failure_type,
            "strategy_hash": strategy_hash,
            "created_by": "correction",
            "source_error_ids": [error_id],
            "success_count": 0,
            "use_count": 0,
            "updated_count": 1,
            "tags": [],
            "last_used_at": None,
        }

        strategy_id = await self.store.add(STRATEGY_STORE, {
            "title": title,
            "content": content,
            "metadata": metadata,
        })

        logger.info("Strategy created: %s", strategy_id[:8])
        return {
            "created": True,
            "strategy_id": strategy_id,
            "strategy_hash": strategy_hash,
        }

    async def _update_existing(
        self, strategy_hash: str, error_id: str,
    ) -> dict:
        """更新已存在的策略记录"""
        # 找到已有记录
        records = await self.store.list_by_metadata(
            STRATEGY_STORE, {"strategy_hash": strategy_hash}, limit=1,
        )
        if not records:
            return {"created": False, "reason": "not_found"}

        record = records[0]
        meta = record.get("metadata", {})
        if isinstance(meta, str):
            import json
            try:
                meta = json.loads(meta)
            except (json.JSONDecodeError, TypeError):
                meta = {}

        # 更新 source_error_ids
        source_ids = meta.get("source_error_ids", [])
        if error_id not in source_ids:
            source_ids.append(error_id)

        # 更新 updated_count
        updated_count = meta.get("updated_count", 1) + 1

        patch = {
            "metadata": {
                **meta,
                "source_error_ids": source_ids,
                "updated_count": updated_count,
            },
        }
        await self.store.update(STRATEGY_STORE, record.get("id", ""), patch)

        logger.info("Strategy updated: %s (count=%d)", record.get("id", "")[:8], updated_count)
        return {
            "created": False,
            "updated": True,
            "strategy_id": record.get("id"),
            "strategy_hash": strategy_hash,
            "updated_count": updated_count,
        }
