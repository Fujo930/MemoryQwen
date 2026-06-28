"""
MemoryQwen — Agent 数据模型
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChatRequest:
    session_id: str
    message: str
    top_k: int = 5
    include_recent: bool = True
    max_recent_messages: int = 10
    use_web: bool = False


@dataclass
class SourceCitation:
    record_id: str = ""
    title: str = ""
    source_path: str = ""
    chunk_index: int = 0
    score: float = 0.0
    snippet: str = ""


@dataclass
class ErrorCitation:
    record_id: str = ""
    task: str = ""
    failure_type: str = ""
    strategy: str = ""
    score: float = 0.0
    snippet: str = ""


@dataclass
class StrategyCitation:
    record_id: str = ""
    title: str = ""
    strategy: str = ""
    failure_type: str = ""
    score: float = 0.0
    snippet: str = ""
    source_error_ids: list[str] = field(default_factory=list)


@dataclass
class AgentChatResponse:
    answer: str = ""
    session_id: str = ""
    sources: list[SourceCitation] = field(default_factory=list)
    error_sources: list[ErrorCitation] = field(default_factory=list)
    strategy_sources: list[StrategyCitation] = field(default_factory=list)
    memory_used: list[str] = field(default_factory=list)
    model: str = ""
    prompt_tokens_estimate: int = 0
    metadata: dict = field(default_factory=dict)


@dataclass
class CorrectionRequest:
    session_id: str = ""
    user_message: str = ""
    wrong_answer: str = ""
    correct_answer: str = ""
    failure_type: str = ""
    strategy: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class CorrectionResponse:
    error_id: str = ""
    saved: bool = False
    failure_type: str = ""
    strategy: str = ""
    metadata: dict = field(default_factory=dict)
