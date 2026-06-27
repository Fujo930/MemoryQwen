"""
MemoryQwen — Embedding 管理
统一的 embedding 生成和缓存
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Embedding 管理器——提供本地 embedding 能力"""

    def __init__(self, config: Any):
        self.config = config
        self._model = None
        self._model_name = config.model.embedding_model
        self._device = config.model.embedding_device
        self._dimension = config.model.embedding_dimension

    async def embed(self, text: str) -> list[float]:
        """将单条文本转为 embedding 向量"""
        results = await self.embed_batch([text])
        return results[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """将多条文本批量转为 embedding 向量"""
        if not texts:
            return []

        # 尝试通过 API embed
        try:
            return await self._api_embed(texts)
        except Exception as e:
            logger.debug("API embed failed, falling back to local: %s", e)
            return await self._local_embed(texts)

    async def _api_embed(self, texts: list[str]) -> list[list[float]]:
        """通过模型 API 获取 embedding"""
        from src.model_adapter import create_adapter
        adapter = create_adapter(self.config)
        result = await adapter.embed(texts)
        return result.embeddings

    async def _local_embed(self, texts: list[str]) -> list[list[float]]:
        """本地 embedding（sentence-transformers）"""
        try:
            from sentence_transformers import SentenceTransformer

            if self._model is None:
                logger.info("Loading local embedding model: %s (%s)",
                            self._model_name, self._device)
                self._model = SentenceTransformer(
                    self._model_name,
                    device=self._device,
                )

            embeddings = self._model.encode(texts, show_progress_bar=False)
            return embeddings.tolist()
        except ImportError:
            logger.error("sentence-transformers not installed")
            raise RuntimeError(
                "No embedding backend available. "
                "Install sentence-transformers or configure an API-based embedding provider."
            )

    @property
    def dimension(self) -> int:
        """返回 embedding 向量维度"""
        return self._dimension
