"""
MemoryQwen — SQLite MemoryStore
使用 aiosqlite 实现所有记忆存储操作。
"""

from __future__ import annotations

import json
import uuid
import logging
from pathlib import Path
from typing import Any

import aiosqlite

from src.memory_store.base import MemoryStore, TABLE_NAMES
from src.memory_store.models import TABLE_SCHEMAS, TABLE_COLUMNS, TABLE_SEARCH_COLUMNS

logger = logging.getLogger(__name__)


class SQLiteStore(MemoryStore):
    """基于 SQLite 的记忆存储"""

    def __init__(self, config: Any):
        self.db_path = str(Path(config.memory_store.database_path))
        self._conn: aiosqlite.Connection | None = None
        self._initialized = False

    async def init(self) -> None:
        """初始化数据库，创建所有表"""
        if self._initialized:
            return

        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row

        for table_name, schema in TABLE_SCHEMAS.items():
            await self._conn.executescript(schema)
        await self._conn.commit()

        self._initialized = True
        logger.info("SQLiteStore initialized at %s", self.db_path)

    async def _ensure_init(self):
        """懒初始化"""
        if not self._initialized:
            await self.init()

    # ─── CRUD ────────────────────────────────────────────

    async def add(self, table: str, record: dict) -> str:
        """添加记录，返回 ID"""
        await self._ensure_init()
        self._validate_table(table)

        record = dict(record)
        record_id = record.get("id") or str(uuid.uuid4())
        record["id"] = record_id
        record.setdefault("created_at", "")
        record.setdefault("updated_at", "")

        # 序列化 JSON 字段
        record = self._serialize_json_fields(table, record)

        columns = TABLE_COLUMNS[table]
        values = [record.get(c, "") for c in columns]
        placeholders = ",".join("?" * len(columns))
        cols_str = ",".join(columns)

        await self._conn.execute(
            f"INSERT OR REPLACE INTO {table} ({cols_str}) VALUES ({placeholders})",
            values,
        )
        await self._conn.commit()
        return record_id

    async def get(self, table: str, record_id: str) -> dict | None:
        """获取单条记录"""
        await self._ensure_init()
        self._validate_table(table)

        cursor = await self._conn.execute(
            f"SELECT * FROM {table} WHERE id = ?",
            (record_id,),
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        return self._deserialize_json_fields(table, dict(row))

    async def update(self, table: str, record_id: str, patch: dict) -> bool:
        """更新记录"""
        await self._ensure_init()
        self._validate_table(table)

        if not patch:
            return True

        existing = await self.get(table, record_id)
        if existing is None:
            return False

        # 合并 patch
        merged = {**existing, **patch, "id": record_id}
        merged["updated_at"] = ""  # SQLite will set via default
        merged = self._serialize_json_fields(table, merged)

        set_clause = []
        values = []
        for k, v in merged.items():
            if k == "id":
                continue
            set_clause.append(f"{k} = ?")
            values.append(v)
        values.append(record_id)

        await self._conn.execute(
            f"UPDATE {table} SET {', '.join(set_clause)}, updated_at = datetime('now') WHERE id = ?",
            values,
        )
        await self._conn.commit()
        return True

    async def delete(self, table: str, record_id: str) -> bool:
        """删除记录"""
        await self._ensure_init()
        self._validate_table(table)

        cursor = await self._conn.execute(
            f"DELETE FROM {table} WHERE id = ?",
            (record_id,),
        )
        await self._conn.commit()
        return cursor.rowcount > 0

    async def list(
        self, table: str, limit: int = 20, offset: int = 0
    ) -> list[dict]:
        """分页列出"""
        await self._ensure_init()
        self._validate_table(table)

        cursor = await self._conn.execute(
            f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
        rows = await cursor.fetchall()
        return [self._deserialize_json_fields(table, dict(r)) for r in rows]

    async def search_keyword(
        self, table: str, query: str, limit: int = 10
    ) -> list[dict]:
        """关键词 LIKE 搜索"""
        await self._ensure_init()
        self._validate_table(table)

        search_cols = TABLE_SEARCH_COLUMNS.get(table, ["content"])
        conditions = " OR ".join(f"{c} LIKE ?" for c in search_cols)
        params = [f"%{query}%"] * len(search_cols)

        cursor = await self._conn.execute(
            f"SELECT * FROM {table} WHERE {conditions} ORDER BY created_at DESC LIMIT ?",
            params + [limit],
        )
        rows = await cursor.fetchall()
        return [self._deserialize_json_fields(table, dict(r)) for r in rows]

    async def count(self, table: str) -> int:
        """记录总数"""
        await self._ensure_init()
        self._validate_table(table)

        cursor = await self._conn.execute(f"SELECT COUNT(*) FROM {table}")
        row = await cursor.fetchone()
        return row[0] if row else 0

    async def close(self) -> None:
        """关闭连接"""
        if self._conn:
            await self._conn.close()
            self._conn = None
            self._initialized = False

    async def exists_by_metadata(
        self, store_type: str, filters: dict[str, str]
    ) -> bool:
        """通过 metadata JSON 字段值检查记录是否存在"""
        await self._ensure_init()
        self._validate_table(store_type)

        if not filters:
            return False

        # metadata 在 SQLite 中以 JSON 字符串存储
        # 使用 LIKE 匹配 JSON 片段，转义特殊字符
        conditions = []
        params = []
        for key, value in filters.items():
            # 转义 LIKE 通配符和 Windows 路径反斜杠
            safe_value = value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            json_fragment = f'"{key}": "{safe_value}"'
            conditions.append("metadata LIKE ? ESCAPE '\\'")
            params.append(f"%{json_fragment}%")

        where = " AND ".join(conditions)
        cursor = await self._conn.execute(
            f"SELECT 1 FROM {store_type} WHERE {where} LIMIT 1",
            params,
        )
        row = await cursor.fetchone()
        return row is not None

    async def list_by_metadata(
        self,
        store_type: str,
        filters: dict[str, str],
        limit: int = 100,
        order_by: str = "created_at",
        descending: bool = False,
    ) -> list[dict]:
        """按 metadata 过滤并排序列出记录"""
        await self._ensure_init()
        self._validate_table(store_type)

        conditions = []
        params = []
        for key, value in filters.items():
            safe_value = value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            json_fragment = f'"{key}": "{safe_value}"'
            conditions.append("metadata LIKE ? ESCAPE '\\'")
            params.append(f"%{json_fragment}%")

        where = " AND ".join(conditions) if conditions else "1=1"
        direction = "DESC" if descending else "ASC"
        safe_order = order_by.replace("'", "''")  # basic injection guard

        cursor = await self._conn.execute(
            f"SELECT * FROM {store_type} WHERE {where} ORDER BY {safe_order} {direction} LIMIT ?",
            params + [limit],
        )
        rows = await cursor.fetchall()
        return [self._deserialize_json_fields(store_type, dict(r)) for r in rows]

    # ─── 内部方法 ────────────────────────────────────────

    def _serialize_json_fields(self, table: str, record: dict) -> dict:
        """将 dict/list 字段序列化为 JSON 字符串"""
        result = dict(record)
        columns = TABLE_COLUMNS.get(table, [])
        # 确保 JSON 字段存在且被序列化
        json_fields = {"metadata": "{}", "tags": "[]"}
        for field, default_json in json_fields.items():
            if field not in columns:
                continue
            if field in result:
                val = result[field]
                if isinstance(val, (dict, list)):
                    result[field] = json.dumps(val, ensure_ascii=False)
                elif val == "" or val is None:
                    result[field] = default_json
            else:
                result[field] = default_json
        return result

    def _deserialize_json_fields(self, table: str, record: dict) -> dict:
        """将 JSON 字符串字段反序列化为 dict/list"""
        result = dict(record)
        columns = TABLE_COLUMNS.get(table, [])
        json_fields = {"metadata", "tags"}
        for field in json_fields:
            if field not in columns:
                continue
            if field in result and isinstance(result[field], str):
                try:
                    result[field] = json.loads(result[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        return result

    def _validate_table(self, table: str):
        if table not in TABLE_NAMES:
            raise ValueError(
                f"Unknown table: {table}. Valid tables: {TABLE_NAMES}"
            )
