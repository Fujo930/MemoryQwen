"""
MemoryQwen — ChatMemory 聊天记忆存储
基于 SQLite (aiosqlite) 的聊天记录管理
"""

from __future__ import annotations

import json
import uuid
import logging
from pathlib import Path
from datetime import datetime
from typing import Any

import aiosqlite

from src.memory_bus.base import BaseMemoryStore, MemoryEntry, ScoredEntry

logger = logging.getLogger(__name__)


class ChatMemory(BaseMemoryStore):
    """聊天记忆存储"""

    def __init__(self, config: Any):
        super().__init__(config)
        db_dir = Path(config.system.data_dir) / "chat_memory"
        db_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = str(db_dir / "chat_memory.db")

    async def _init_db(self):
        """初始化数据库表结构"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    summary TEXT,
                    model_used TEXT,
                    token_count INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    sources TEXT,
                    tokens INTEGER DEFAULT 0,
                    error_ref TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                );

                CREATE INDEX IF NOT EXISTS idx_messages_session
                    ON messages(session_id, created_at);
            """)
            await db.commit()

    async def create_session(self, title: str = "新对话") -> str:
        """创建新会话，返回 session_id"""
        await self._init_db()
        session_id = str(uuid.uuid4())
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO sessions (id, title) VALUES (?, ?)",
                (session_id, title),
            )
            await db.commit()
        return session_id

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        sources: list[dict] | None = None,
        tokens: int = 0,
        error_ref: str | None = None,
    ) -> str:
        """添加消息到会话"""
        await self._init_db()
        msg_id = str(uuid.uuid4())
        sources_json = json.dumps(sources, ensure_ascii=False) if sources else None

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO messages (id, session_id, role, content, sources, tokens, error_ref)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (msg_id, session_id, role, content, sources_json, tokens, error_ref),
            )
            await db.execute(
                "UPDATE sessions SET updated_at = CURRENT_TIMESTAMP, token_count = token_count + ? WHERE id = ?",
                (tokens, session_id),
            )
            await db.commit()
        return msg_id

    async def add(self, entry: MemoryEntry) -> str:
        """通用添加接口（拆解 MemoryEntry 为消息）"""
        role = entry.metadata.get("role", "user")
        session_id = entry.metadata.get("session_id", "default")
        return await self.add_message(
            session_id=session_id,
            role=role,
            content=entry.content,
            sources=entry.metadata.get("sources"),
            tokens=entry.metadata.get("tokens", 0),
        )

    async def get_session(self, session_id: str) -> dict | None:
        """获取会话信息"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM sessions WHERE id = ?",
                (session_id,),
            )
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def get_history(
        self,
        session_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        """获取会话历史消息"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT id, role, content, sources, tokens, error_ref, created_at
                   FROM messages
                   WHERE session_id = ?
                   ORDER BY created_at ASC
                   LIMIT ? OFFSET ?""",
                (session_id, limit, offset),
            )
            rows = await cursor.fetchall()
            messages = []
            for row in rows:
                msg = dict(row)
                if msg["sources"]:
                    try:
                        msg["sources"] = json.loads(msg["sources"])
                    except json.JSONDecodeError:
                        msg["sources"] = []
                messages.append(msg)
            return messages

    async def list_sessions(self, limit: int = 20) -> list[dict]:
        """列出最近会话"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT id, title, created_at, updated_at, summary,
                          model_used, token_count, is_active
                   FROM sessions
                   WHERE is_active = 1
                   ORDER BY updated_at DESC
                   LIMIT ?""",
                (limit,),
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def update_summary(self, session_id: str, summary: str):
        """更新会话摘要"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE sessions SET summary = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (summary, session_id),
            )
            await db.commit()

    async def search(
        self,
        query: str,
        top_k: int = 10,
        filters: dict | None = None,
    ) -> list[ScoredEntry]:
        """搜索聊天记录（关键词匹配）"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """SELECT id, session_id, role, content, sources, created_at
                   FROM messages
                   WHERE content LIKE ?
                   ORDER BY created_at DESC
                   LIMIT ?""",
                (f"%{query}%", top_k),
            )
            rows = await cursor.fetchall()
            return [
                ScoredEntry(
                    id=row["id"],
                    content=row["content"],
                    metadata={
                        "session_id": row["session_id"],
                        "role": row["role"],
                        "created_at": row["created_at"],
                    },
                    score=1.0,
                )
                for row in rows
            ]

    async def delete(self, entry_id: str) -> bool:
        """删除消息"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("DELETE FROM messages WHERE id = ?", (entry_id,))
            await db.commit()
            return cursor.rowcount > 0

    async def update(self, entry: MemoryEntry) -> bool:
        """更新消息（不支持）"""
        raise NotImplementedError("Chat messages are append-only")

    async def count(self) -> int:
        """消息总数"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM messages")
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def delete_session(self, session_id: str) -> bool:
        """删除整个会话"""
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            await db.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            await db.commit()
            return True
