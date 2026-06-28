"""
MemoryQwen — 配置管理系统
"""

from __future__ import annotations

import os
import yaml
from pathlib import Path
from typing import Literal
from pydantic import BaseModel


class ProviderConfig(BaseModel):
    base_url: str = ""
    api_key: str = ""


class ModelConfig(BaseModel):
    default_provider: str = "ollama"
    default_light_model: str = "qwen2.5:7b"
    default_deep_model: str = "qwen2.5:14b"
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    embedding_device: Literal["cpu", "cuda"] = "cpu"
    embedding_dimension: int = 512
    providers: dict[str, ProviderConfig] = {}
    profiles_dir: str = "./config/model_profiles"


class ModelClientConfig(BaseModel):
    provider: str = "ollama"
    base_url: str = "http://localhost:11434"
    api_key: str = ""
    model: str = ""
    timeout: int = 60
    max_retries: int = 3
    default_temperature: float = 0.7
    default_max_tokens: int = 4096


class ModelProfileConfig(BaseModel):
    enabled: bool = True
    profile_path: str = "config/model_profiles/qwen_7b.yaml"
    auto_detect: bool = False


class MemoryStoreConfig(BaseModel):
    backend: Literal["sqlite"] = "sqlite"
    database_path: str = "memory/memoryqwen.db"


class RetrievalConfig(BaseModel):
    top_k: int = 5
    rrf_k: int = 60
    vector_weight: float = 0.7
    bm25_weight: float = 0.3
    min_score: float = 0.3
    index_load_limit: int = 500


class RetrievalKeywordConfig(BaseModel):
    enabled: bool = True
    default_top_k: int = 5
    min_score: float = 0.0
    tokenizer: str = "simple"


class ChunkingConfig(BaseModel):
    max_tokens: int = 512
    overlap_tokens: int = 32
    strategy: str = "semantic"


class ChatMemoryConfig(BaseModel):
    max_history: int = 50
    summary_interval: int = 20
    summary_model: str = "light"


class MemoryConfig(BaseModel):
    retrieval: RetrievalConfig = RetrievalConfig()
    retrieval_keyword: RetrievalKeywordConfig = RetrievalKeywordConfig()
    chunking: ChunkingConfig = ChunkingConfig()
    chat: ChatMemoryConfig = ChatMemoryConfig()


class AgentConfig(BaseModel):
    system_prompt: str = "你是 MemoryQwen，由用户部署在本地电脑上的个人 AI 助手。你不是任何云服务产品。\n\n规则：\n1. 你是 MemoryQwen，不要自称其他产品名。\n2. 优先使用本地资料片段回答。\n3. 资料不足请说明不确定。\n4. 引用来源使用 [S1]、[S2]。\n5. 使用中文回答。"
    default_top_k: int = 5
    max_recent_messages: int = 10
    cite_sources: bool = True
    save_chat_memory: bool = True
    use_error_memory: bool = True
    error_top_k: int = 3
    max_error_context_chars: int = 1200
    use_strategy_memory: bool = True
    strategy_top_k: int = 3
    max_strategy_context_chars: int = 1000
    enable_strategy_learning: bool = True
    error_memory_recent_fallback: bool = True
    strategy_memory_recent_fallback: bool = True
    use_retrieval_gate: bool = True
    retrieval_gate_mode: str = "heuristic"
    retrieval_gate_default_retrieve: bool = True
    retrieval_gate_min_confidence: float = 0.4
    retrieval_gate_casual_skip: bool = True
    retrieval_gate_max_top_k: int = 5


class IngestionConfig(BaseModel):
    inbox_path: str = "inbox"
    supported_extensions: list[str] = [".txt", ".md"]
    recursive: bool = True
    chunk_size: int = 800
    chunk_overlap: int = 120
    skip_hidden_files: bool = True
    archive_sources: bool = True
    source_archive_dir: str = "memory/sources"
    watcher_enabled: bool = False
    watch_delay: int = 5
    auto_index: bool = True


class ReasonerConfig(BaseModel):
    enable_multi_path: bool = False
    max_paths: int = 3
    enable_verifier: bool = True
    task_classification: bool = True
    deep_model_triggers: list[str] = ["math", "reasoning", "planning", "analysis", "debug", "code"]


class GPUGuardianConfig(BaseModel):
    enabled: bool = True
    provider: str = "nvidia_smi"
    light_yield_vram_ratio: float = 0.55
    full_yield_vram_ratio: float = 0.85
    game_mode_gpu_util_percent: int = 70
    game_process_names: list[str] = [
        "Cyberpunk2077.exe", "cs2.exe", "FortniteClient-Win64-Shipping.exe",
        "Minecraft.exe", "GenshinImpact.exe", "StarRail.exe", "eldenring.exe",
    ]
    creative_process_names: list[str] = [
        "blender.exe", "resolve.exe", "Adobe Premiere Pro.exe",
        "AfterFX.exe", "UnrealEditor.exe", "Unity.exe", "obs64.exe",
    ]
    full_yield_process_names: list[str] = []


class TaskRuntimeConfig(BaseModel):
    enabled: bool = True
    store: str = "memory"
    database_path: str = "memory/tasks.db"
    auto_resume_on_normal: bool = False


class JobRunnerConfig(BaseModel):
    enabled: bool = True
    check_guardian_on_checkpoint: bool = True


class WebConfig(BaseModel):
    """v0.1.5 Internet Query: controlled web access."""
    enabled: bool = False
    provider: str = "mock"
    search_max_results: int = 5
    fetch_timeout_seconds: int = 10
    fetch_max_bytes: int = 500_000
    fetch_max_chars: int = 12_000
    user_agent: str = "MemoryQwen/0.1.5"
    allow_private_network: bool = False
    allow_file_urls: bool = False
    default_ingest: bool = False
    require_explicit_ingest: bool = True


class BackupConfig(BaseModel):
    auto_backup: bool = False
    backup_dir: str = "./backup"
    backup_interval: int = 24
    keep_backups: int = 7
    include_dirs: list[str] = ["./memory", "./config"]


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 7860
    reload: bool = False
    cors_origins: list[str] = ["http://localhost:7860"]


class SystemConfig(BaseModel):
    name: str = "MemoryQwen"
    version: str = "0.1.0"
    data_dir: str = "./memory"
    inbox_dir: str = "./inbox"
    workspace_dir: str = "./workspace"
    log_level: str = "INFO"
    log_file: str = "./logs/memoryqwen.log"


class AppConfig(BaseModel):
    system: SystemConfig = SystemConfig()
    server: ServerConfig = ServerConfig()
    model: ModelConfig = ModelConfig()
    model_client: ModelClientConfig = ModelClientConfig()
    model_profile: ModelProfileConfig = ModelProfileConfig()
    memory_store: MemoryStoreConfig = MemoryStoreConfig()
    memory: MemoryConfig = MemoryConfig()
    ingestion: IngestionConfig = IngestionConfig()
    agent: AgentConfig = AgentConfig()
    reasoner: ReasonerConfig = ReasonerConfig()
    gpu_guardian: GPUGuardianConfig = GPUGuardianConfig()
    task_runtime: TaskRuntimeConfig = TaskRuntimeConfig()
    job_runner: JobRunnerConfig = JobRunnerConfig()
    backup: BackupConfig = BackupConfig()
    web: WebConfig = WebConfig()

    @classmethod
    def from_yaml(cls, path: str | Path) -> "AppConfig":
        path = Path(path)
        if not path.exists():
            return cls()
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        return cls(**raw) if raw else cls()


_config: AppConfig | None = None


def load_config(path: str | None = None) -> AppConfig:
    global _config
    if _config is not None:
        return _config
    search_paths = [path, os.environ.get("MEMORYQWEN_CONFIG"), "./config/default.yaml"]
    for p in search_paths:
        if p:
            p = Path(p)
            if p.exists():
                _config = AppConfig.from_yaml(p)
                return _config
    _config = AppConfig()
    return _config


def get_config() -> AppConfig:
    if _config is None:
        return load_config()
    return _config
