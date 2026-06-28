"""
MemoryQwen — KeywordRetriever
BM25 关键词检索，支持多 store_types。
"""

from __future__ import annotations

import json
import math
import logging
from typing import Any

from src.retrieval.base import BaseRetriever
from src.retrieval.models import RetrievalQuery, RetrievalResult
from src.retrieval.tokenizer import SimpleTokenizer

logger = logging.getLogger(__name__)

# BM25 参数
K1 = 1.5
B = 0.75

RECORD_KIND_BY_STORE: dict[str, str] = {
    "knowledge_store": "document_chunk",
    "error_store": "error_case",
    "strategy_store": "strategy",
    "example_store": "example_case",
}

DEFAULT_STORE_TYPES = ["knowledge_store"]


class KeywordRetriever(BaseRetriever):
    """基于 BM25 的关键词检索器，支持多 store 检索"""

    def __init__(self, config: Any, store, store_types: list[str] | None = None):
        self.config = config
        self.store = store
        self.tokenizer = SimpleTokenizer()
        self.store_types = store_types or DEFAULT_STORE_TYPES
        self._docs: list[dict] = []          # 原始记录列表
        self._doc_tokens: list[list[str]] = []
        self._doc_stores: list[str] = []     # 每条 doc 所属 store
        self._idf: dict[str, float] = {}
        self._avgdl: float = 0.0
        self._initialized = False

    async def refresh_index(self) -> None:
        """从配置的 store_types 重新加载索引"""
        self._docs = []
        self._doc_tokens = []
        self._doc_stores = []
        self._idf = {}
        self._avgdl = 0.0

        for store_type in self.store_types:
            record_kind = RECORD_KIND_BY_STORE.get(store_type)
            if record_kind is None:
                logger.debug("Skipping unknown store_type: %s", store_type)
                continue

            try:
                # 限制首次加载数量，避免 22K+ docs 导致超时
                mem_cfg = getattr(self.config, "memory", None)
                retrieval_sec = getattr(mem_cfg, "retrieval", None) if mem_cfg else None
                idx_limit = getattr(retrieval_sec, "index_load_limit", 5000) if retrieval_sec else 5000
                all_records = await self.store.list(store_type, limit=idx_limit)
            except Exception as e:
                logger.warning("Failed to load %s: %s", store_type, e)
                continue

            for rec in all_records:
                meta = rec.get("metadata", {})
                if isinstance(meta, str):
                    try:
                        meta = json.loads(meta)
                    except (json.JSONDecodeError, TypeError):
                        meta = {}
                if meta.get("record_kind") == record_kind:
                    self._docs.append(rec)
                    self._doc_stores.append(store_type)
                    content = rec.get("content", "")
                    tokens = self.tokenizer.tokenize(content)
                    self._doc_tokens.append(tokens)

        if not self._docs:
            self._initialized = True
            return

        total_len = sum(len(t) for t in self._doc_tokens)
        self._avgdl = total_len / len(self._docs)

        N = len(self._docs)
        all_terms = set()
        for tokens in self._doc_tokens:
            all_terms.update(tokens)

        for term in all_terms:
            df = sum(1 for t in self._doc_tokens if term in t)
            self._idf[term] = max(0.1, math.log((N - df + 0.5) / (df + 0.5) + 1.0))

        self._initialized = True
        logger.info("Index refreshed: %d docs from %s", len(self._docs), self.store_types)

    async def _ensure_init(self):
        if not self._initialized:
            await self.refresh_index()

    async def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict | None = None,
    ) -> list[RetrievalResult]:
        """关键词检索"""
        await self._ensure_init()

        cfg = self.config.memory.retrieval_keyword
        k = top_k or cfg.default_top_k
        min_score = cfg.min_score

        if not query or not query.strip():
            return []

        query_tokens = self.tokenizer.tokenize(query)
        if not query_tokens:
            return []

        scores: list[tuple[int, float]] = []
        for i, doc_tokens in enumerate(self._doc_tokens):
            score = self._bm25_score(query_tokens, doc_tokens)
            if score > 0:
                scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for doc_idx, score in scores[:k * 2]:
            if score <= min_score:
                continue
            doc = self._docs[doc_idx]
            store_type = self._doc_stores[doc_idx] if doc_idx < len(self._doc_stores) else ""
            meta = doc.get("metadata", {})
            if isinstance(meta, str):
                try:
                    meta = json.loads(meta)
                except (json.JSONDecodeError, TypeError):
                    meta = {}

            if filters and not self._match_filters(meta, filters):
                continue

            results.append(RetrievalResult(
                record_id=doc.get("id", ""),
                store_type=store_type,
                title=doc.get("title", ""),
                content=doc.get("content", ""),
                metadata=meta,
                score=round(score, 4),
                source_path=meta.get("source_path", ""),
                chunk_index=meta.get("chunk_index", 0),
                total_chunks=meta.get("total_chunks", 0),
            ))

        return results[:k]

    async def search_structured(self, request: RetrievalQuery) -> list[RetrievalResult]:
        return await self.search(
            query=request.query, top_k=request.top_k, filters=request.filters,
        )

    def _bm25_score(self, query_tokens: list[str], doc_tokens: list[str]) -> float:
        score = 0.0
        doc_len = len(doc_tokens)
        tf_map: dict[str, int] = {}
        for t in doc_tokens:
            tf_map[t] = tf_map.get(t, 0) + 1
        for term in query_tokens:
            tf = tf_map.get(term, 0)
            if tf == 0:
                continue
            idf = self._idf.get(term, 0.0)
            numerator = tf * (K1 + 1)
            denominator = tf + K1 * (1 - B + B * doc_len / max(self._avgdl, 1))
            score += idf * numerator / denominator
        return score

    def _match_filters(self, metadata: dict, filters: dict) -> bool:
        for key, value in filters.items():
            if metadata.get(key) != value:
                return False
        return True
