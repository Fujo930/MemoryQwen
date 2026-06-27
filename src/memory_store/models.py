"""
MemoryQwen — MemoryStore 数据模型
定义每种 store 的标准字段。
"""

from __future__ import annotations

# ─── 通用字段 ────────────────────────────────────────

COMMON_FIELDS = ("id", "metadata", "created_at", "updated_at")

# ─── knowledge_chunks ─────────────────────────────────

KNOWLEDGE_COLUMNS = [
    "id", "source_path", "title", "content",
    "metadata", "created_at", "updated_at",
]

KNOWLEDGE_SCHEMA = """
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id TEXT PRIMARY KEY,
    source_path TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL,
    metadata TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

# ─── chat_messages ────────────────────────────────────

CHAT_COLUMNS = [
    "id", "session_id", "role", "content",
    "session_summary", "metadata", "created_at", "updated_at",
]

CHAT_SCHEMA = """
CREATE TABLE IF NOT EXISTS chat_messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user','assistant','system','tool')),
    content TEXT NOT NULL,
    session_summary TEXT NOT NULL DEFAULT '',
    metadata TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_chat_session
    ON chat_messages(session_id, created_at);
"""

# ─── error_experiences ────────────────────────────────

ERROR_COLUMNS = [
    "id", "task", "wrong_answer", "correct_answer",
    "failure_type", "strategy", "metadata", "created_at", "updated_at",
]

ERROR_SCHEMA = """
CREATE TABLE IF NOT EXISTS error_experiences (
    id TEXT PRIMARY KEY,
    task TEXT NOT NULL,
    wrong_answer TEXT NOT NULL DEFAULT '',
    correct_answer TEXT NOT NULL DEFAULT '',
    failure_type TEXT NOT NULL DEFAULT 'general',
    strategy TEXT NOT NULL DEFAULT '',
    metadata TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

# ─── strategies ───────────────────────────────────────

STRATEGY_COLUMNS = [
    "id", "title", "content", "tags",
    "success_count", "last_used_at", "metadata", "created_at", "updated_at",
]

STRATEGY_SCHEMA = """
CREATE TABLE IF NOT EXISTS strategies (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '[]',
    success_count INTEGER NOT NULL DEFAULT 0,
    last_used_at TEXT DEFAULT NULL,
    metadata TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

# ─── examples ─────────────────────────────────────────

EXAMPLE_COLUMNS = [
    "id", "task", "answer", "reasoning_pattern",
    "tags", "metadata", "created_at", "updated_at",
]

EXAMPLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS examples (
    id TEXT PRIMARY KEY,
    task TEXT NOT NULL,
    answer TEXT NOT NULL,
    reasoning_pattern TEXT NOT NULL DEFAULT '',
    tags TEXT NOT NULL DEFAULT '[]',
    metadata TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

# ─── 聚合 ─────────────────────────────────────────────

TABLE_SCHEMAS: dict[str, str] = {
    "knowledge_store": KNOWLEDGE_SCHEMA.replace("knowledge_chunks", "knowledge_store"),
    "knowledge_chunks": KNOWLEDGE_SCHEMA,
    "chat_messages": CHAT_SCHEMA,
    "error_store": ERROR_SCHEMA.replace("error_experiences", "error_store"),
    "error_experiences": ERROR_SCHEMA,
    "strategy_store": STRATEGY_SCHEMA.replace("strategies", "strategy_store"),
    "strategies": STRATEGY_SCHEMA,
    "examples": EXAMPLE_SCHEMA,
}

TABLE_COLUMNS: dict[str, list[str]] = {
    "knowledge_store": KNOWLEDGE_COLUMNS,
    "knowledge_chunks": KNOWLEDGE_COLUMNS,
    "chat_messages": CHAT_COLUMNS,
    "error_store": ERROR_COLUMNS,
    "error_experiences": ERROR_COLUMNS,
    "strategy_store": STRATEGY_COLUMNS,
    "strategies": STRATEGY_COLUMNS,
    "examples": EXAMPLE_COLUMNS,
}

TABLE_SEARCH_COLUMNS: dict[str, list[str]] = {
    "knowledge_store": ["title", "content"],
    "knowledge_chunks": ["title", "content"],
    "chat_messages": ["content"],
    "error_store": ["task", "wrong_answer", "correct_answer"],
    "error_experiences": ["task", "wrong_answer", "correct_answer"],
    "strategy_store": ["title", "content"],
    "strategies": ["title", "content"],
    "examples": ["task", "answer"],
}
