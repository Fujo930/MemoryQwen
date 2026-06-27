"""
MemoryQwen — KnowledgeStore 知识库存储
基于 ChromaDB 的向量检索 + 内存 BM25 关键词检索
"""

from __future__ import annotations

import json
import hashlib
import logging
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings

from src.memory_bus.base import BaseMemoryStore, MemoryEntry, ScoredEntry
from src.memory_bus.embedding import EmbeddingManager

logger = logging.getLogger(__name__)


class SimpleBM25:
    """简易 BM25 实现（纯 Python，无外部依赖）"""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_freqs: list[dict[str, int]] = []
        self.doc_count = 0
        self.avg_doc_len = 0
        self.idf: dict[str, float] = {}
        self.documents: list[str] = []

    def fit(self, documents: list[str]):
        """拟合 BM25 参数"""
        self.documents = documents
        self.doc_count = len(documents)
        self.doc_freqs = []
        total_terms = 0

        for doc in documents:
            terms = self._tokenize(doc)
            freq = {}
            for t in terms:
                freq[t] = freq.get(t, 0) + 1
            self.doc_freqs.append(freq)
            total_terms += len(terms)

        self.avg_doc_len = total_terms / max(self.doc_count, 1)

        # 计算 IDF
        all_terms = set()
        for freq in self.doc_freqs:
            all_terms.update(freq.keys())

        for term in all_terms:
            doc_with_term = sum(1 for f in self.doc_freqs if term in f)
            self.idf[term] = max(
                0.1,
                (self.doc_count - doc_with_term + 0.5)
                / (doc_with_term + 0.5) + 1.0,
            )

    def search(self, query: str, top_k: int = 5) -> list[tuple[int, float]]:
        """检索 BM25 分数"""
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        scores = []
        for i, freq in enumerate(self.doc_freqs):
            score = 0.0
            doc_len = sum(freq.values())
            for term in query_terms:
                if term in freq:
                    tf = freq[term] * (self.k1 + 1) / (freq[term] + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len))
                    if term in self.idf:
                        score += self.idf[term] * tf
            scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def add_document(self, document: str):
        """增量添加文档"""
        self.documents.append(document)
        terms = self._tokenize(document)
        freq = {}
        for t in terms:
            freq[t] = freq.get(t, 0) + 1
        self.doc_freqs.append(freq)
        self.doc_count = len(self.documents)
        total_terms = sum(sum(f.values()) for f in self.doc_freqs)
        self.avg_doc_len = total_terms / max(self.doc_count, 1)

        # 更新 IDF（简化处理）
        for term in freq:
            doc_with_term = sum(1 for f in self.doc_freqs if term in f)
            self.idf[term] = max(
                0.1,
                (self.doc_count - doc_with_term + 0.5)
                / (doc_with_term + 0.5) + 1.0,
            )

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """简单 tokenizer：支持中文和英文"""
        import re
        # 匹配中文字符、英文单词、数字
        tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+|\d+', text.lower())
        return tokens


class KnowledgeStore(BaseMemoryStore):
    """知识库存储——向量 + BM25 混合检索"""

    def __init__(self, config: Any):
        super().__init__(config)
        persist_dir = Path(config.system.data_dir) / "knowledge_store"
        persist_dir.mkdir(parents=True, exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_chunks",
            metadata={"hnsw:space": "cosine"},
        )

        self.embedding_manager = EmbeddingManager(config)
        self.bm25 = SimpleBM25()
        self._bm25_ready = False

    async def add_chunks(self, chunks: list[dict]) -> list[str]:
        """批量添加切片
        chunks: [{"content": str, "metadata": dict, "id": str}]
        """
        if not chunks:
            return []

        contents = [c["content"] for c in chunks]
        ids = [c.get("id", self._hash_content(c["content"])) for c in chunks]
        metadatas = [c.get("metadata", {}) for c in chunks]

        # 生成 embedding
        logger.debug("Generating embeddings for %d chunks...", len(contents))
        try:
            embeddings = await self.embedding_manager.embed_batch(contents)
        except Exception as e:
            logger.error("Embedding failed: %s", e)
            # 使用零向量作为 fallback
            dim = self.embedding_manager.dimension
            embeddings = [[0.0] * dim for _ in contents]

        # 写入 ChromaDB
        str_metadatas = []
        for m in metadatas:
            cleaned = {}
            for k, v in m.items():
                if isinstance(v, (str, int, float, bool)):
                    cleaned[k] = v
                else:
                    cleaned[k] = json.dumps(v, ensure_ascii=False)
            str_metadatas.append(cleaned)

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=str_metadatas,
            documents=contents,
        )

        # 更新 BM25
        for content in contents:
            self.bm25.add_document(content)
        self._bm25_ready = True

        logger.info("Indexed %d chunks", len(chunks))
        return ids

    async def add(self, entry: MemoryEntry) -> str:
        """添加单条记忆"""
        chunk_id = self._hash_content(entry.content)
        chunks = [{"content": entry.content, "metadata": entry.metadata, "id": chunk_id}]
        ids = await self.add_chunks(chunks)
        return ids[0] if ids else chunk_id

    async def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict | None = None,
    ) -> list[ScoredEntry]:
        """纯向量检索"""
        k = top_k or self.config.memory.retrieval.top_k
        return await self.hybrid_search(query, top_k=k, filters=filters)

    async def hybrid_search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict | None = None,
    ) -> list[ScoredEntry]:
        """混合检索（向量 + BM25 + RRF 融合）"""
        cfg = self.config.memory.retrieval
        k = top_k or cfg.top_k

        # 向量检索
        vector_results = await self._vector_search(query, top_k=k * 2, filters=filters)

        # BM25 检索
        bm25_results = self._bm25_search(query, top_k=k * 2)

        # RRF 融合
        return self._rrf_fusion(vector_results, bm25_results, k=k, rrf_k=cfg.rrf_k)

    async def _vector_search(
        self,
        query: str,
        top_k: int = 10,
        filters: dict | None = None,
    ) -> list[ScoredEntry]:
        """向量检索"""
        try:
            query_embedding = await self.embedding_manager.embed(query)
        except Exception as e:
            logger.warning("Vector search embedding failed: %s", e)
            return []

        where = None
        if filters:
            where = {k: v for k, v in filters.items() if isinstance(v, str)}

        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as e:
            logger.warning("ChromaDB query failed: %s", e)
            return []

        entries = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                distance = results["distances"][0][i] if results["distances"] else 1.0
                score = 1.0 - distance  # cosine distance → similarity
                entries.append(ScoredEntry(
                    id=doc_id,
                    content=results["documents"][0][i],
                    metadata=results["metadatas"][0][i] if results["metadatas"] else {},
                    score=score,
                ))
        return entries

    def _bm25_search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[ScoredEntry]:
        """BM25 关键词检索"""
        if not self._bm25_ready:
            return []

        results = self.bm25.search(query, top_k=top_k)

        entries = []
        # 从 ChromaDB 获取 BM25 命中的文档内容
        for idx, score in results:
            doc_id = self._hash_content(self.bm25.documents[idx])
            try:
                chroma_result = self.collection.get(
                    ids=[doc_id],
                    include=["documents", "metadatas"],
                )
                if chroma_result["ids"]:
                    entries.append(ScoredEntry(
                        id=doc_id,
                        content=chroma_result["documents"][0],
                        metadata=chroma_result["metadatas"][0] if chroma_result["metadatas"] else {},
                        score=float(score),
                    ))
                else:
                    entries.append(ScoredEntry(
                        id=doc_id,
                        content=self.bm25.documents[idx],
                        metadata={},
                        score=float(score),
                    ))
            except Exception:
                entries.append(ScoredEntry(
                    id=doc_id,
                    content=self.bm25.documents[idx],
                    metadata={},
                    score=float(score),
                ))

        return entries

    def _rrf_fusion(
        self,
        vector_results: list[ScoredEntry],
        bm25_results: list[ScoredEntry],
        k: int = 5,
        rrf_k: int = 60,
    ) -> list[ScoredEntry]:
        """Reciprocal Rank Fusion 融合排序"""
        scores: dict[str, ScoredEntry] = {}
        seen = set()

        # 向量检索排名
        for rank, entry in enumerate(vector_results):
            if entry.id not in seen:
                seen.add(entry.id)
                scores[entry.id] = ScoredEntry(
                    id=entry.id,
                    content=entry.content,
                    metadata=entry.metadata,
                    score=1.0 / (rrf_k + rank + 1),
                )

        # BM25 检索排名
        for rank, entry in enumerate(bm25_results):
            if entry.id in scores:
                scores[entry.id].score += 1.0 / (rrf_k + rank + 1)
            else:
                scores[entry.id] = ScoredEntry(
                    id=entry.id,
                    content=entry.content,
                    metadata=entry.metadata,
                    score=1.0 / (rrf_k + rank + 1),
                )

        # 按融合分数排序
        sorted_entries = sorted(
            scores.values(),
            key=lambda x: x.score,
            reverse=True,
        )
        return sorted_entries[:k]

    async def delete(self, entry_id: str) -> bool:
        """删除指定条目"""
        try:
            # 从 BM25 中删除（简化：重建索引）
            self.collection.delete(ids=[entry_id])
            self._rebuild_bm25()
            return True
        except Exception as e:
            logger.error("Delete failed: %s", e)
            return False

    def _rebuild_bm25(self):
        """从 ChromaDB 重建 BM25 索引"""
        all_docs = self.collection.get(include=["documents"])
        if all_docs["documents"]:
            self.bm25 = SimpleBM25()
            for doc in all_docs["documents"]:
                self.bm25.add_document(doc)
            self._bm25_ready = True

    async def count(self) -> int:
        """条目总数"""
        return self.collection.count()

    async def update(self, entry: MemoryEntry) -> bool:
        """更新条目"""
        return await self.delete(entry.id) and bool(await self.add(entry))

    async def list_documents(self) -> list[dict]:
        """列出所有文档摘要"""
        all_docs = self.collection.get(include=["metadatas"])
        summaries = []
        seen_sources = set()
        for i, doc_id in enumerate(all_docs["ids"]):
            meta = all_docs["metadatas"][i]
            source = meta.get("source_path", doc_id)
            if source not in seen_sources:
                seen_sources.add(source)
                summaries.append({
                    "id": doc_id,
                    "source": source,
                    "type": meta.get("source_type", "unknown"),
                    "title": meta.get("doc_title", source),
                })
        return summaries

    @staticmethod
    def _hash_content(content: str) -> str:
        """根据内容生成唯一 ID"""
        return hashlib.md5(content.encode("utf-8")).hexdigest()
