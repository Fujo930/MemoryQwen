"""
MemoryQwen — ErrorStore 错误经验库
存储 AI 犯过的错误，支持相似问题检索
"""

from __future__ import annotations

import json
import uuid
import logging
from pathlib import Path
from datetime import datetime
from typing import Any

import aiosqlite
import chromadb
from chromadb.config import Settings

from src.memory_bus.base import BaseMemoryStore, MemoryEntry, ScoredEntry
from src.memory_bus.embedding import EmbeddingManager

logger = logging.getLogger(__name__)


class ErrorStore(BaseMemoryStore):
    """错误经验存储——SQLite 元数据 + ChromaDB 向量"""

    def __init__(self, config: Any):
        super().__init__(config)
        db_dir = Path(config.system.data_dir) / "error_store"
        db_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = str(db_dir / "errors.db")

        # ChromaDB vector store
        self.chroma_client = chromadb.PersistentClient(
            path=str(db_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="error_experiences",
            metadata={"hnsw:space": "cosine"},
        )

        self.embedding_manager = EmbeddingManager(config)

    async def _init_db(self):
        """初始化 SQLite 表"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS error_experiences (
                    id TEXT PRIMARY KEY,
                    trigger_query TEXT NOT NULL,
                    error_type TEXT,
                    wrong_answer TEXT,
                    correct_answer TEXT,
                    root_cause TEXT,
                    fix_strategy TEXT,
                    context_snapshot TEXT,
                    tags TEXT,
                    hit_count INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_errors_type ON error_experiences(error_type);
                CREATE INDEX IF NOT EXISTS idx_errors_hits ON error_experiences(hit_count DESC);
            """)
            await db.commit()

    async def add_error(
        self,
        trigger_query: str,
        wrong_answer: str,
        correct_answer: str,
        root_cause: str = "",
        fix_strategy: str = "",
        error_type: str = "general",
        tags: list[str] | None = None,
        context_snapshot: str = "",
    ) -> str:
        """添加一条错误经验"""
        await self._init_db()
        error_id = str(uuid.uuid4())
        tags_json = json.dumps(tags or [], ensure_ascii=False)

        # SQLite 存储
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO error_experiences
                   (id, trigger_query, error_type, wrong_answer, correct_answer,
                    root_cause, fix_strategy, context_snapshot, tags)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (error_id, trigger_query, error_type, wrong_answer,
                 correct_answer, root_cause, fix_strategy, context_snapshot, tags_json),
            )
            await db.commit()

        # ChromaDB 向量存储
        vector_text = f"问题: {trigger_query}\n正确: {correct_answer}\n根因: {root_cause}"
        try:
            embedding = await self.embedding_manager.embed(vector_text)
            self.collection.add(
                ids=[error_id],
                embeddings=[embedding],
                metadatas=[{
                    "error_type": error_type,
                    "trigger_query": trigger_query[:200],
                    "tags": tags_json,
                    "created_at": datetime.now().isoformat(),
                }],
                documents=[vector_text],
            )
        except Exception as e:
            logger.warning("Failed to store error embedding: %s", e)

        logger.info("Error recorded: %s — %s", error_id, trigger_query[:50])
        return error_id

    async def add(self, entry: MemoryEntry) -> str:
        """通用添加接口"""
        meta = entry.metadata
        return await self.add_error(
            trigger_query=entry.content,
            wrong_answer=meta.get("wrong_answer", ""),
            correct_answer=meta.get("correct_answer", ""),
            root_cause=meta.get("root_cause", ""),
            fix_strategy=meta.get("fix_strategy", ""),
            error_type=meta.get("error_type", "general"),
            tags=meta.get("tags"),
        )

    async def search_similar(
        self,
        query: str,
        top_k: int = 5,
        error_type: str | None = None,
    ) -> list[dict]:
        """搜索相似错误经验（向量 + 关键词）"""
        await self._init_db()

        # 向量检索
        vector_results = await self._vector_search(query, top_k=top_k * 2)

        # 关键词检索（SQLite LIKE）
        keyword_results = await self._keyword_search(query, top_k=top_k * 2)

        # 合并去重
        seen_ids = set()
        merged = []

        for result in vector_results + keyword_results:
            if result["id"] not in seen_ids:
                seen_ids.add(result["id"])
                merged.append(result)

        # 按分数排序
        merged.sort(key=lambda x: x.get("score", 0), reverse=True)

        # 按类型过滤
        if error_type:
            merged = [r for r in merged if r.get("error_type") == error_type]

        return merged[:top_k]

    async def _vector_search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[dict]:
        """向量检索错误经验"""
        try:
            query_embedding = await self.embedding_manager.embed(query)
        except Exception as e:
            logger.warning("Vector search failed: %s", e)
            return []

        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"],
            )
        except Exception:
            return []

        entries = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                distance = results["distances"][0][i] if results["distances"] else 1.0
                score = 1.0 - distance
                meta = results["metadatas"][0][i] if results["metadatas"] else {}

                # 从 SQLite 获取完整信息
                full = await self._get_full_error(doc_id)
                if full:
                    full["score"] = score
                    full["match_type"] = "vector"
                    entries.append(full)

                # 更新命中计数
                await self._increment_hit(doc_id)

        return entries

    async def _keyword_search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[dict]:
        """关键词检索错误经验"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT * FROM error_experiences
                   WHERE trigger_query LIKE ? OR correct_answer LIKE ?
                   ORDER BY hit_count DESC, created_at DESC
                   LIMIT ?""",
                (f"%{query}%", f"%{query}%", top_k),
            )
            rows = await cursor.fetchall()
            return [
                {**dict(row), "score": 0.5, "match_type": "keyword"}
                for row in rows
            ]

    async def _get_full_error(self, error_id: str) -> dict | None:
        """从 SQLite 获取完整错误信息"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM error_experiences WHERE id = ?",
                (error_id,),
            )
            row = await cursor.fetchone()
            if row:
                result = dict(row)
                if result["tags"]:
                    try:
                        result["tags"] = json.loads(result["tags"])
                    except json.JSONDecodeError:
                        result["tags"] = []
                return result
            return None

    async def _increment_hit(self, error_id: str):
        """增加命中计数"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE error_experiences SET hit_count = hit_count + 1 WHERE id = ?",
                    (error_id,),
                )
                await db.commit()
        except Exception:
            pass

    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[ScoredEntry]:
        """统一检索接口"""
        results = await self.search_similar(
            query,
            top_k=top_k,
            error_type=filters.get("error_type") if filters else None,
        )
        return [
            ScoredEntry(
                id=r["id"],
                content=f"问题: {r['trigger_query']}\n正确回答: {r['correct_answer']}\n根因: {r.get('root_cause', '')}",
                metadata=r,
                score=r.get("score", 0.5),
            )
            for r in results
        ]

    async def get_error(self, error_id: str) -> dict | None:
        """获取单条错误记录"""
        return await self._get_full_error(error_id)

    async def list_errors(self, limit: int = 20, offset: int = 0) -> list[dict]:
        """列出错误记录"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT id, trigger_query, error_type, correct_answer, root_cause,
                          hit_count, created_at
                   FROM error_experiences
                   ORDER BY hit_count DESC, created_at DESC
                   LIMIT ? OFFSET ?""",
                (limit, offset),
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def delete(self, entry_id: str) -> bool:
        """删除错误记录"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "DELETE FROM error_experiences WHERE id = ?",
                (entry_id,),
            )
            await db.commit()
            deleted = cursor.rowcount > 0

        if deleted:
            try:
                self.collection.delete(ids=[entry_id])
            except Exception:
                pass
        return deleted

    async def update(self, entry: MemoryEntry) -> bool:
        """更新错误记录"""
        meta = entry.metadata
        error_id = entry.id
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """UPDATE error_experiences
                   SET trigger_query=?, wrong_answer=?, correct_answer=?,
                       root_cause=?, fix_strategy=?, tags=?,
                       updated_at=CURRENT_TIMESTAMP
                   WHERE id=?""",
                (
                    meta.get("trigger_query", ""),
                    meta.get("wrong_answer", ""),
                    meta.get("correct_answer", ""),
                    meta.get("root_cause", ""),
                    meta.get("fix_strategy", ""),
                    json.dumps(meta.get("tags", []), ensure_ascii=False),
                    error_id,
                ),
            )
            await db.commit()
        return True

    async def count(self) -> int:
        """错误总数"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM error_experiences")
            row = await cursor.fetchone()
            return row[0] if row else 0
