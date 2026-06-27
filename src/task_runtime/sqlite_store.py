"""
MemoryQwen — SQLiteTaskStore
持久化任务存储
"""

from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path

from src.task_runtime.models import TaskRecord, TaskTransition


CREATE_TASK_TABLE = """
CREATE TABLE IF NOT EXISTS task_records (
    task_id TEXT PRIMARY KEY,
    task_type TEXT NOT NULL DEFAULT 'custom',
    title TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'pending',
    progress_current INTEGER NOT NULL DEFAULT 0,
    progress_total INTEGER NOT NULL DEFAULT 0,
    progress_message TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT '',
    started_at TEXT NOT NULL DEFAULT '',
    completed_at TEXT NOT NULL DEFAULT '',
    paused_at TEXT NOT NULL DEFAULT '',
    pause_reason TEXT NOT NULL DEFAULT '',
    error_message TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}'
)
"""

CREATE_TRANSITION_TABLE = """
CREATE TABLE IF NOT EXISTS task_transitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    from_status TEXT NOT NULL DEFAULT '',
    to_status TEXT NOT NULL DEFAULT '',
    reason TEXT NOT NULL DEFAULT '',
    timestamp TEXT NOT NULL DEFAULT ''
)
"""

RECORD_COLUMNS = [
    "task_id", "task_type", "title", "status",
    "progress_current", "progress_total", "progress_message",
    "created_at", "updated_at", "started_at", "completed_at",
    "paused_at", "pause_reason", "error_message", "metadata_json",
]

WRITABLE_COLUMNS = set(RECORD_COLUMNS) - {"task_id", "created_at"}


class SQLiteTaskStore:
    """SQLite 任务存储"""

    def __init__(self, database_path: str = "memory/tasks.db"):
        self.db_path = database_path
        self._local = threading.local()
        self._init_db()

    def _init_db(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(CREATE_TASK_TABLE)
        conn.execute(CREATE_TRANSITION_TABLE)
        conn.commit()
        conn.close()

    def _get_conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    # ─── CRUD ──────────────────────────────────────────

    def add(self, task: TaskRecord):
        conn = self._get_conn()
        conn.execute(
            """INSERT INTO task_records (task_id, task_type, title, status,
               progress_current, progress_total, progress_message,
               created_at, updated_at, started_at, completed_at,
               paused_at, pause_reason, error_message, metadata_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                task.task_id, task.task_type, task.title, task.status,
                task.progress_current, task.progress_total, task.progress_message,
                task.created_at, task.updated_at, task.started_at, task.completed_at,
                task.paused_at, task.pause_reason, task.error_message,
                json.dumps(task.metadata, ensure_ascii=False),
            ),
        )
        conn.commit()

    def get(self, task_id: str) -> TaskRecord | None:
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM task_records WHERE task_id = ?", (task_id,)).fetchone()
        if row is None:
            return None
        return self._row_to_task(row)

    def update(self, task_id: str, patch: dict):
        conn = self._get_conn()
        allowed = {k: v for k, v in patch.items() if k in WRITABLE_COLUMNS}
        if "metadata" in allowed:
            allowed["metadata_json"] = json.dumps(allowed.pop("metadata"), ensure_ascii=False)
        if not allowed:
            return
        sets = ", ".join(f"{k}=?" for k in allowed)
        vals = list(allowed.values()) + [task_id]
        conn.execute(f"UPDATE task_records SET {sets} WHERE task_id=?", vals)
        conn.commit()

    def list(self, status: str | None = None, task_type: str | None = None, limit: int = 100) -> list[TaskRecord]:
        conn = self._get_conn()
        where = []
        params = []
        if status:
            where.append("status=?")
            params.append(status)
        if task_type:
            where.append("task_type=?")
            params.append(task_type)
        sql = "SELECT * FROM task_records"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(sql, params).fetchall()
        return [self._row_to_task(r) for r in rows]

    def delete(self, task_id: str):
        conn = self._get_conn()
        conn.execute("DELETE FROM task_records WHERE task_id=?", (task_id,))
        conn.commit()

    def count(self, status: str | None = None, task_type: str | None = None) -> int:
        conn = self._get_conn()
        where = []
        params = []
        if status:
            where.append("status=?")
            params.append(status)
        if task_type:
            where.append("task_type=?")
            params.append(task_type)
        sql = "SELECT COUNT(*) FROM task_records"
        if where:
            sql += " WHERE " + " AND ".join(where)
        row = conn.execute(sql, params).fetchone()
        return row[0] if row else 0

    def add_transition(self, transition: TaskTransition):
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO task_transitions (task_id, from_status, to_status, reason, timestamp) VALUES (?,?,?,?,?)",
            (transition.task_id, transition.from_status, transition.to_status,
             transition.reason, transition.timestamp),
        )
        conn.commit()

    def list_transitions(self, task_id: str) -> list[TaskTransition]:
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT * FROM task_transitions WHERE task_id=? ORDER BY timestamp ASC", (task_id,)
        ).fetchall()
        return [
            TaskTransition(task_id=r["task_id"], from_status=r["from_status"],
                           to_status=r["to_status"], reason=r["reason"], timestamp=r["timestamp"])
            for r in rows
        ]

    def close(self):
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None

    # ─── Internal ──────────────────────────────────────

    def _row_to_task(self, row: sqlite3.Row) -> TaskRecord:
        meta_str = row["metadata_json"] or "{}"
        try:
            metadata = json.loads(meta_str)
        except (json.JSONDecodeError, TypeError):
            metadata = {}
        return TaskRecord(
            task_id=row["task_id"], task_type=row["task_type"], title=row["title"],
            status=row["status"], progress_current=row["progress_current"],
            progress_total=row["progress_total"], progress_message=row["progress_message"],
            created_at=row["created_at"], updated_at=row["updated_at"],
            started_at=row["started_at"], completed_at=row["completed_at"],
            paused_at=row["paused_at"], pause_reason=row["pause_reason"],
            error_message=row["error_message"], metadata=metadata,
        )
