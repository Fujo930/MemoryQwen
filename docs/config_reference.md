# 配置参考

MemoryQwen 所有配置项及默认值。

## model_client

```yaml
model_client:
  provider: "ollama"              # ollama | lm_studio | llamacpp | openai_compatible
  base_url: "http://localhost:11434"
  api_key: ""
  model: "qwen2.5:7b"            # 必须与后端已有模型名一致
  timeout: 60
  max_retries: 3
  default_temperature: 0.7
  default_max_tokens: 4096
```

## memory_store

```yaml
memory_store:
  backend: sqlite
  database_path: "memory/memoryqwen.db"
```

## ingestion

```yaml
ingestion:
  inbox_path: "inbox"
  supported_extensions: [".txt", ".md"]
  recursive: true
  chunk_size: 800
  chunk_overlap: 120
  skip_hidden_files: true
  auto_index: true
```

## retrieval

```yaml
memory:
  retrieval:
    top_k: 5
    min_score: 0.0
  retrieval_keyword:
    enabled: true
    default_top_k: 5
    min_score: 0.0
    tokenizer: "simple"
```

## agent

```yaml
agent:
  system_prompt: "你是 MemoryQwen..."
  default_top_k: 5
  max_recent_messages: 10
  cite_sources: true
  save_chat_memory: true
  use_error_memory: true
  use_strategy_memory: true
  enable_strategy_learning: true
  error_memory_recent_fallback: true     # 无命中时获取最近错误
  strategy_memory_recent_fallback: true  # 无命中时获取最近策略
```

## model_profile

```yaml
model_profile:
  enabled: true
  profile_path: "config/model_profiles/qwen_7b.yaml"
  auto_detect: false
```

## gpu_guardian

```yaml
gpu_guardian:
  enabled: true
  provider: "nvidia_smi"
  light_yield_vram_ratio: 0.55          # VRAM 超过 55% → light_yield
  full_yield_vram_ratio: 0.85           # VRAM 超过 85% → full_yield
  game_mode_gpu_util_percent: 70        # GPU 占用 >70% → game_mode
  game_process_names:                   # 游戏进程列表
    - "Cyberpunk2077.exe"
    - "cs2.exe"
  creative_process_names:               # 创作软件进程列表
    - "blender.exe"
    - "obs64.exe"
  full_yield_process_names: []          # 最高优先级让路进程
```

## task_runtime

```yaml
task_runtime:
  enabled: true
  store: "sqlite"                       # memory | sqlite
  database_path: "memory/tasks.db"
  auto_resume_on_normal: false
```

## job_runner

```yaml
job_runner:
  enabled: true
  check_guardian_on_checkpoint: true     # checkpoint 时检查 GPU 状态
```
