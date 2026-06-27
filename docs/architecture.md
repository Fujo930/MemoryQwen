# MemoryQwen 项目架构文档

## 一、项目定位

MemoryQwen 是一个运行在普通家用电脑上的本地 AI agent 系统。
它不是聊天机器人，而是可长期养成的本地 AI 宠物 / 本地 AI 工作站。

**核心原则：**
- 模型可以换，记忆不能丢
- 7B 常驻轻量 agent，14B 深度思考
- 32B/70B 不作为 RTX 4080 默认路线
- 记忆由 MemoryBus 管理，不依赖模型自身上下文
- 用户游戏/渲染时 AI 自动释放 GPU
- 完全模块化，每模块有测试

---

## 二、完整目录结构

```
MemoryQwen/
│
├── start.bat                         # Windows 一键启动
├── start.sh                          # Linux 启动脚本
├── requirements.txt                  # Python 依赖
├── pyproject.toml                    # 项目元数据
├── README.md
│
├── config/                           # 配置文件目录
│   ├── default.yaml                  # 全局默认配置
│   ├── logging.yaml                  # 日志配置
│   └── model_profiles/              # 模型适配配置
│       ├── qwen-7b.yaml
│       └── qwen-14b.yaml
│
├── models/                           # 模型文件目录（用户自行放置或软链）
│
├── memory/                           # 记忆存储目录（永不丢失）
│   ├── knowledge_store/             # 知识库（ChromaDB + BM25 索引）
│   ├── chat_memory/                 # 聊天记录（SQLite）
│   ├── error_store/                 # 错误经验库（SQLite + 向量）
│   ├── strategy_store/             # 策略库（SQLite + 向量）
│   ├── example_store/              # 成功案例库（SQLite + 向量）
│   └── sessions/                   # Session 摘要库
│
├── inbox/                            # 用户拖入资料目录
│   ├── pdf/
│   ├── txt/
│   ├── md/
│   ├── docx/
│   └── code/
│
├── workspace/                        # Agent 临时工作目录
│
├── tools/                            # Agent 可用工具
│   ├── __init__.py
│   ├── python_executor.py           # Python 沙箱执行
│   ├── file_ops.py                  # 文件操作
│   ├── web_search.py                # 网页搜索（可选）
│   └── command_executor.py          # 命令执行
│
├── ui/                               # Web UI 静态文件
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── assets/
│   └── templates/
│       ├── chat.html
│       ├── knowledge.html
│       ├── memory.html
│       ├── errors.html
│       ├── strategies.html
│       ├── tasks.html
│       ├── gpu_status.html
│       ├── models.html
│       └── settings.html
│
├── backup/                           # 备份目录
│
├── docs/                             # 文档
│   ├── architecture.md               # 本文件
│   ├── mvp-plan.md                   # MVP 计划
│   ├── issues.md                     # Issue 列表
│   ├── api-spec.md                   # API 接口规范
│   └── dev-guide.md                  # 开发指南
│
├── tests/                            # 测试目录
│   ├── test_ingestion/
│   ├── test_memory_bus/
│   ├── test_agent/
│   ├── test_reasoner/
│   ├── test_gpu_guardian/
│   ├── test_model_adapter/
│   └── test_server/
│
└── src/                              # 源代码
    ├── __init__.py
    ├── __main__.py                   # 入口: python -m src
    ├── main.py                       # 应用启动逻辑
    │
    ├── config.py                     # 全局配置加载
    │
    ├── model_adapter/               # 模型适配层
    │   ├── __init__.py
    │   ├── base.py                   # BaseModelAdapter 接口
    │   ├── openai_compat.py          # OpenAI-compatible API 适配器
    │   ├── ollama_adapter.py         # Ollama 适配器
    │   ├── llamacpp_adapter.py       # llama.cpp 适配器
    │   └── profiler.py              # 模型测试/画像生成
    │
    ├── memory_bus/                   # 记忆总线
    │   ├── __init__.py
    │   ├── base.py                   # BaseMemoryStore 接口
    │   ├── embedding.py              # Embedding 管理
    │   ├── knowledge_store.py        # 知识库存储
    │   ├── chat_memory.py            # 聊天记忆存储
    │   ├── error_store.py            # 错误经验库
    │   ├── strategy_store.py         # 策略库
    │   ├── example_store.py          # 成功案例库
    │   └── retrieval.py             # 统一检索接口（多路召回）
    │
    ├── ingestion/                    # 资料摄入
    │   ├── __init__.py
    │   ├── parser.py                 # 文件解析器
    │   ├── chunker.py                # 文本切片器
    │   ├── indexer.py                # 索引构建
    │   └── watcher.py               # 文件监听（inbox 监控）
    │
    ├── agent/                        # Agent 核心
    │   ├── __init__.py
    │   ├── core.py                   # Agent 主循环
    │   ├── context.py                # 上下文构建器
    │   ├── system_prompt.py          # 系统提示词模板
    │   └── session.py               # Session 管理
    │
    ├── reasoner/                     # 推理增强
    │   ├── __init__.py
    │   ├── base.py                   # BaseReasoner
    │   ├── multi_path.py             # 多路径推理
    │   ├── verifier.py               # 验证器
    │   └── router.py                # 任务路由（7B vs 14B）
    │
    ├── gpu_guardian/                 # GPU 守护
    │   ├── __init__.py
    │   ├── monitor.py                # GPU 监控
    │   ├── process_watcher.py        # 进程监控
    │   └── policy.py                # 让路策略
    │
    └── server/                       # 服务层
        ├── __init__.py
        ├── api.py                    # REST API
        ├── websocket.py             # WebSocket 实时通信
        └── lifecycle.py             # 服务生命周期管理
```

---

## 三、技术栈选择

| 层次 | 技术 | 理由 |
|------|------|------|
| **语言** | Python 3.11+ | AI 生态最佳，全家桶覆盖 |
| **Web 框架** | FastAPI + Uvicorn | 异步高性能，自动 API 文档 |
| **前端** | Jinja2 服务端模板 + 原生 JS | MVP 不引入前端构建工具链，快速迭代 |
| **关系库** | SQLAlchemy + aiosqlite → SQLite | 零配置，文件即可迁移 |
| **向量库** | ChromaDB（MVP）→ LanceDB（后续） | 嵌入式零依赖，MVP 够用 |
| **Embedding** | sentence-transformers (BAAI/bge-small-zh) | 本地运行，14B 也可用同款 |
| **模型适配** | openai SDK（兼容协议） | 统一 Ollama/LM Studio/llama.cpp |
| **切分** | tiktoken + 自定义策略 | 精确 token 计数 |
| **GPU 监控** | nvidia-ml-py / psutil + GPUtil | 跨平台 GPU 检测 |
| **文件监听** | watchdog | 跨平台文件系统监控 |
| **测试** | pytest + pytest-asyncio | 标准方案 |
| **配置** | pydantic-settings + yaml | 类型安全配置 |
| **文档解析** | pypdf + python-docx + markdown 标准库 | 轻量无外部服务 |

---

## 四、核心模块职责

### 1. Model Adapter Layer

**职责：** 抽象所有模型后端差异，提供统一的 chat/completion/embedding 接口。

```
输入: 消息列表 + 模型标识 + 参数
输出: 模型回复 + token 用量 + 延迟信息
```

**关键设计：**
- 每个模型一个 `model_profile.yaml`，描述能力、参数、限制
- `profiler.py` 自动对模型进行标准化测试（tool calling、JSON 输出、指令跟随、上下文保持）
- 支持多后端自动切换：Ollama ↔ LM Studio ↔ llama.cpp ↔ 任意 OpenAI-compatible API

### 2. MemoryBus

**职责：** 所有长期记忆的单一入口。禁止模型直接读写记忆。

```
输入: 查询文本 + 记忆类型 + 检索参数
输出: 相关记忆片段列表 + 元数据
```

**子模块：**

| 仓库 | 存储内容 | 检索方式 |
|------|---------|---------|
| knowledge_store | 用户资料解析后的切片 | 向量 + BM25 混合检索 |
| chat_memory | 聊天历史 | 时间线 + 关键词 |
| error_store | 错误经验 | 向量 + 分类标签 |
| strategy_store | 行动策略 | 向量 + 标签 |
| example_store | 成功案例 | 向量 + 标签 |

**统一检索接口 `retrieval.py`：**
- 多路召回（向量检索 + 关键词检索 + 时间线）
- RRF（Reciprocal Rank Fusion）融合排序
- 去重 + 上下文压缩

### 3. Document Ingestion

**职责：** 自动监听 inbox/ 目录，解析文档，切片建索引。

```
输入: 文件路径（PDF/txt/md/docx/code）
处理: 解析 → 清洗 → 切片 → 建向量索引 → 建 BM25 索引
输出: 知识库条目（写入 knowledge_store）
```

**切片策略：**
- 按语义段落切分（markdown 标题、空行、段落边界）
- tiktoken 控制 token 上限（默认 512 tokens）
- 保留文档元数据（来源、路径、标题、页码）

### 4. Agent Server

**职责：** 用户与模型的中间层，负责上下文构建、记忆检索、工具调用。

```
输入: 用户消息
处理: 
  1. 构建系统提示
  2. 检索 session 摘要
  3. 检索长期记忆
  4. 检索错误经验
  5. 调用模型
  6. 必要时调用工具
  7. 保存新记忆
输出: agent 回复 + 来源引用
```

**上下文构建器 `context.py`：**
- 按优先级分层的上下文窗口
- Token 预算管理（7B 模型 8K → 14B 模型 32K 上下文）
- 自动压缩历史（超出时做 session_summary）

### 5. Reasoner

**职责：** 弥补 7B/14B 推理能力不足，用工程手段增强可靠性。

```
输入: 用户问题 + 上下文 + 任务类型
处理:
  - 评估任务复杂度，路由到 7B 或 14B
  - 需要推理时：多路径生成 + 验证器过滤
  - 可验证任务：优先工具验证（Python 执行、JSON schema、引用检查）
输出: 验证后的答案
```

### 6. GPU Guardian

**职责：** 确保 AI 不影响用户正常使用电脑。

```
监控维度:
  - GPU 使用率（每 5 秒采样）
  - 显存占用
  - 前台进程列表
  - 已知高 GPU 负载应用列表

让路等级:
  L0: 正常模式 - 所有服务运行
  L1: 轻度让路 - 暂停 embedding，降低推理优先级
  L2: 中度让路 - 卸载 14B，只保留 7B
  L3: 深度让路 - 卸载所有模型，只保留后台监听
  L4: 完全休眠 - 卸载所有模型，暂停所有后台任务
```

---

## 五、MVP 最小闭环

MVP 必须完整跑通的流程：

```
用户拖入资料到 inbox/
   → watcher 检测到新文件
   → parser 解析文件内容
   → chunker 切片（512 tokens）
   → indexer 建向量索引 + BM25 索引
   → 写入 knowledge_store

用户在 Web UI 聊天
   → Agent 接收消息
   → Agent 检索 knowledge_store（相关文档）
   → Agent 检索 error_store（相关错误经验）
   → Agent 构建上下文
   → Agent 调用模型（7B 或 14B）
   → 模型生成回复
   → Agent 输出带来源的回答
   → Agent 保存聊天记录到 chat_memory

用户指出回答有误
   → Agent 记录错误到 error_store
   → 下次类似问题时自动检索并参考
```

**MVP 模块依赖关系：**

```
MVP 涉及模块（按构建顺序）：
1. config.py                        ← 基础配置
2. model_adapter/*                  ← 模型通信
3. memory_bus/embedding.py          ← 向量化
4. ingestion/parser.py + chunker.py ← 文档处理
5. memory_bus/knowledge_store.py    ← 知识存储
6. memory_bus/chat_memory.py        ← 聊天存储
7. memory_bus/error_store.py        ← 错误存储
8. memory_bus/retrieval.py          ← 统一检索
9. agent/core.py + context.py       ← Agent 核心
10. server/api.py                   ← API 服务
11. ui/templates/*                  ← 前端页面
12. ingestion/indexer.py            ← 索引构建
13. ingestion/watcher.py            ← 文件监听
```

---

## 六、模块接口设计

### 6.1 ModelAdapter 接口

```python
class BaseModelAdapter(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: list[dict] | None = None,
    ) -> ChatResult:
        """统一聊天接口"""
        ...

    @abstractmethod
    async def embed(
        self,
        texts: list[str],
        model: str = "default",
    ) -> EmbeddingResult:
        """统一 embedding 接口"""
        ...

    @abstractmethod
    async def test_profile(self) -> ModelProfile:
        """测试模型能力，生成 profile"""
        ...
```

### 6.2 MemoryBus 接口

```python
class BaseMemoryStore(ABC):
    @abstractmethod
    async def add(self, entry: MemoryEntry) -> str:
        """添加记忆条目，返回 ID"""
        ...

    @abstractmethod
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[MemoryEntry]:
        """检索相关记忆"""
        ...

    @abstractmethod
    async def delete(self, entry_id: str) -> bool:
        """删除记忆"""
        ...

    @abstractmethod
    async def update(self, entry: MemoryEntry) -> bool:
        """更新记忆"""
        ...


class MemoryBus:
    """统一入口，组合所有 store"""
    
    def __init__(self, config):
        self.knowledge = KnowledgeStore(config)
        self.chat = ChatMemory(config)
        self.errors = ErrorStore(config)
        self.strategies = StrategyStore(config)
        self.examples = ExampleStore(config)
    
    async def hybrid_search(
        self,
        query: str,
        stores: list[str] = ["knowledge", "errors", "strategies"],
        top_k: int = 5,
    ) -> list[ScoredEntry]:
        """跨存储混合检索"""
        ...
```

### 6.3 Agent 接口

```python
class Agent:
    def __init__(self, config, model_adapter, memory_bus):
        self.adapter = model_adapter
        self.memory = memory_bus
    
    async def process_message(
        self,
        user_message: str,
        session_id: str,
        model_tier: str = "light",  # "light"=7B, "deep"=14B
    ) -> AgentResponse:
        """处理单条用户消息"""
        # 1. 构建上下文
        context = await self.build_context(user_message, session_id)
        # 2. 检索记忆
        memories = await self.memory.hybrid_search(user_message)
        # 3. 调用模型
        response = await self.adapter.chat(
            messages=context.to_messages(memories),
            model=self._select_model(model_tier),
        )
        # 4. 后处理
        result = self.post_process(response)
        # 5. 保存聊天记录
        await self.memory.chat.add(session_id, user_message, result)
        return result
    
    async def build_context(
        self,
        message: str,
        session_id: str,
    ) -> AgentContext:
        """构建上下文窗口，管理 token 预算"""
        ...
```

### 6.4 Ingestion 接口

```python
class DocumentParser:
    async def parse(self, file_path: str) -> Document:
        """解析文件为结构化文档"""
        ...

class DocumentChunker:
    def chunk(
        self,
        document: Document,
        max_tokens: int = 512,
        overlap: int = 32,
    ) -> list[Chunk]:
        """将文档切片"""
        ...

class Indexer:
    async def index(self, chunks: list[Chunk]) -> IndexResult:
        """为切片建立向量和 BM25 索引"""
        ...

class InboxWatcher:
    """监听 inbox/ 目录，自动触发 ingestion pipeline"""
    ...
```

### 6.5 GPU Guardian 接口

```python
class GPUGuardian:
    @dataclass
    class GPUState:
        gpu_util: float        # 0-100
        vram_used: float       # GB
        vram_total: float      # GB
        yield_level: int       # 0-4
        culprit_process: str | None
    
    async def get_state(self) -> GPUState:
        """获取当前 GPU 状态"""
        ...
    
    async def start_monitoring(self):
        """启动后台监控循环"""
        ...
    
    def on_yield_change(self, callback: Callable[[int], Awaitable[None]]):
        """注册让路等级变化回调"""
        ...
```

### 6.6 Server API 接口

```python
# REST API

POST /api/chat                    # 发送消息
  Request:  {"message": str, "session_id": str, "model_tier": str}
  Response: {"response": str, "sources": [...], "token_usage": {...}}

GET  /api/sessions                # 获取会话列表
POST /api/sessions                # 创建新会话

GET  /api/memory/knowledge        # 搜索知识库
  Query:    ?q=str&top_k=int
GET  /api/memory/errors           # 搜索错误库
GET  /api/memory/strategies       # 搜索策略库

POST /api/ingestion               # 手动触发文件摄入
  Request:  {"file_path": str}

GET  /api/system/status           # 系统状态（GPU、模型加载等）
GET  /api/system/gpu              # GPU 状态详情

# WebSocket
WS   /ws/chat                     # 实时聊天（流式输出）
WS   /ws/status                   # 实时状态推送（GPU 变化等）
```

---

## 七、数据库 Schema 草案

### 7.1 SQLite (chat_memory, sessions)

```sql
-- 会话表
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,           -- UUID
    title TEXT,                    -- 会话标题
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    summary TEXT,                  -- session 摘要（自动生成）
    model_used TEXT,               -- 使用的模型
    token_count INTEGER DEFAULT 0, -- 总 token 数
    is_active BOOLEAN DEFAULT 1
);

-- 消息表
CREATE TABLE messages (
    id TEXT PRIMARY KEY,           -- UUID
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,            -- 'user', 'assistant', 'system', 'tool'
    content TEXT NOT NULL,
    sources TEXT,                  -- JSON: 引用的知识来源
    tokens INTEGER DEFAULT 0,
    error_ref TEXT,                -- 关联的错误条目 ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- 错误经验表
CREATE TABLE error_experiences (
    id TEXT PRIMARY KEY,
    trigger_query TEXT NOT NULL,   -- 触发错误的用户问题
    error_type TEXT,               -- 错误分类
    wrong_answer TEXT,             -- 当时给出的错误回答
    correct_answer TEXT,           -- 纠正后的正确回答
    root_cause TEXT,               -- 根因分析
    fix_strategy TEXT,             -- 修正策略
    context_snapshot TEXT,         -- 错误发生时的上下文快照
    tags TEXT,                     -- JSON 标签数组
    similarity_hash TEXT,          -- 用于快速相似度比较
    hit_count INTEGER DEFAULT 1,   -- 被检索命中次数
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 策略表
CREATE TABLE strategies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    trigger_conditions TEXT,       -- 触发条件描述
    procedure TEXT,                -- 执行步骤
    tags TEXT,
    effectiveness REAL DEFAULT 0.5, -- 效果评分 0-1
    use_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 成功案例表
CREATE TABLE examples (
    id TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    successful_response TEXT NOT NULL,
    outcome TEXT,                  -- 结果评估
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7.2 ChromaDB Collections (向量索引)

```python
# 集合名称 → 用途
collections = {
    "knowledge_chunks":   "知识库文档切片",
    "error_experiences":  "错误经验向量",
    "strategies":         "策略向量",
    "examples":           "成功案例向量",
}

# 每个条目的 metadata 结构
metadata_schema = {
    "source_type": str,      # "pdf", "txt", "md", "docx", "code"
    "source_path": str,      # 原始文件路径
    "doc_title": str,        # 文档标题
    "chunk_index": int,      # 切片序号
    "chunk_of": str,         # 所属文档 ID
    "created_at": str,       # ISO 时间
    "tags": str,             # JSON 数组
    "token_count": int,
}
```

---

## 八、配置文件 Schema

### config/default.yaml

```yaml
# MemoryQwen 全局配置
# 文件路径: config/default.yaml

system:
  name: "MemoryQwen"
  version: "0.1.0"
  data_dir: "./memory"      # 记忆数据存储根目录
  inbox_dir: "./inbox"      # 资料输入目录
  workspace_dir: "./workspace"
  log_level: "INFO"
  log_file: "./logs/memoryqwen.log"

server:
  host: "127.0.0.1"
  port: 7860
  reload: false
  cors_origins: ["http://localhost:7860"]

model:
  default_provider: "ollama"    # ollama | lm_studio | llamacpp | openai
  default_light_model: "qwen2.5:7b"
  default_deep_model: "qwen2.5:14b"
  embedding_model: "BAAI/bge-small-zh-v1.5"
  embedding_device: "cpu"       # cpu | cuda
  embedding_dimension: 512      # bge-small-zh 输出维度

  # 各 provider 配置
  providers:
    ollama:
      base_url: "http://localhost:11434"
      api_key: ""
    lm_studio:
      base_url: "http://localhost:1234"
      api_key: ""
    llamacpp:
      base_url: "http://localhost:8080"
      api_key: ""
    openai:
      base_url: ""              # 自定义 OpenAI-compatible API
      api_key: ""

  profiles_dir: "./config/model_profiles"

memory:
  # 知识库检索配置
  retrieval:
    top_k: 5
    rrf_k: 60
    vector_weight: 0.7
    bm25_weight: 0.3
    min_score: 0.3
  
  # 切片配置
  chunking:
    max_tokens: 512
    overlap_tokens: 32
    strategy: "semantic"        # semantic | fixed | heading
  
  # 聊天记忆配置
  chat:
    max_history: 50             # 保留最近 N 条消息
    summary_interval: 20        # 每 N 条消息生成一次摘要
    summary_model: "light"      # 摘要使用 light 还是 deep 模型

ingestion:
  watcher_enabled: true
  watch_delay: 5                # 文件稳定后等待秒数再处理
  auto_index: true
  supported_extensions:
    - ".txt"
    - ".md"
    - ".pdf"
    - ".docx"
    - ".py"
    - ".js"
    - ".ts"
    - ".java"
    - ".cpp"
    - ".rs"
    - ".go"

agent:
  system_prompt_template: "templates/system/default.j2"
  max_tool_calls: 10
  tool_call_timeout: 30
  enable_tools: true
  
  # 上下文窗口预算（按 token）
  context_budget:
    system_prompt: 1024
    session_summary: 512
    memories: 2048
    chat_history: 2048
    tool_results: 1024
    response_reserved: 1024
  
  # 自动错误记录
  error_learning:
    enabled: true
    correction_threshold: 0.7   # 用户修正相似度阈值

reasoner:
  enable_multi_path: true
  max_paths: 3
  enable_verifier: true
  task_classification: true
  
  # 什么任务路由到 deep 模型
  deep_model_triggers:
    - "math"
    - "reasoning"
    - "planning"
    - "analysis"
    - "debug"
    - "code"

gpu_guardian:
  enabled: true
  check_interval: 5             # 检测间隔（秒）
  
  # 让路触发条件
  triggers:
    gpu_util_threshold: 60      # GPU 使用率超过此值触发
    vram_threshold: 0.8         # 显存占用超过 80%
    high_priority_processes:
      - "Game*
      - "UnrealEditor*
      - "Unity*
      - "blender*
      - "premiere*
      - "afterfx*
      - "obs64*
      - "davinci*
      - "Minecraft*
      - "eldenring*
      - "cyberpunk*
  
  # 让路等级定义
  yield_levels:
    L0:
      name: "normal"
      description: "正常全速运行"
    L1:
      name: "light_yield"
      description: "暂停 embedding，降低推理优先级"
      actions:
        - pause_embedding: true
        - reduce_batch_size: true
    L2:
      name: "medium_yield"
      description: "卸载 14B 模型"
      actions:
        - unload_deep_model: true
        - pause_embedding: true
        - reduce_batch_size: true
    L3:
      name: "deep_yield"
      description: "卸载所有模型"
      actions:
        - unload_all_models: true
        - pause_all_tasks: true
    L4:
      name: "hibernate"
      description: "完全休眠"
      actions:
        - unload_all_models: true
        - pause_all_tasks: true
        - minimize_memory: true

backup:
  auto_backup: false
  backup_dir: "./backup"
  backup_interval: 24           # 小时
  keep_backups: 7
  include_dirs:
    - "./memory"
    - "./config"
```

---

## 九、第一阶段 GitHub Issues

### Phase 0: 项目脚手架 (预计 1-2 天)

| Issue | 标题 | 描述 |
|-------|------|------|
| #1 | 搭建项目目录结构和配置系统 | 创建完整目录树，实现 config.py 加载 default.yaml |
| #2 | 创建 start.bat 一键启动脚本 | 检测 Python 环境、安装依赖、启动 server |
| #3 | 初始化测试框架 | 配置 pytest，创建基础 conftest.py 和测试辅助工具 |

### Phase 1: 模型通信 + 记忆核心 (预计 2-3 天)

| Issue | 标题 | 描述 |
|-------|------|------|
| #4 | 实现 ModelAdapter 基类和 OpenAI-compatible 适配器 | 统一 chat/embed 接口，支持 Ollama |
| #5 | 实现 Embedding 管理和 ChromaDB 封装 | 初始化 vector store，支持增删查 |
| #6 | 实现 KnowledgeStore（知识库存储） | 基于 ChromaDB + BM25 的知识存储 |
| #7 | 实现 ChatMemory（聊天记忆存储） | SQLite 存储聊天历史，支持时间线检索 |
| #8 | 实现 ErrorStore（错误经验库） | 错误记录、向量索引、相似检索 |

### Phase 2: 文档摄入 (预计 2 天)

| Issue | 标题 | 描述 |
|-------|------|------|
| #9 | 实现 DocumentParser（多格式文件解析） | 支持 txt/md/pdf/docx 格式 |
| #10 | 实现 DocumentChunker（语义切片器） | 按段落/标题切分，tiktoken 控制 token |
| #11 | 实现 Indexer（向量+关键词索引构建） | 解析→切片→索引整条 pipeline |
| #12 | 实现 InboxWatcher（文件监听器） | watchdog 监听 inbox 目录自动触发 |

### Phase 3: Agent + Reasoner 核心 (预计 2-3 天)

| Issue | 标题 | 描述 |
|-------|------|------|
| #13 | 实现 Agent 主循环 | 接收消息 → 检索记忆 → 调用模型 → 返回结果 |
| #14 | 实现 ContextBuilder（上下文构建器） | Token 预算管理，分层上下文窗口 |
| #15 | 实现 TaskRouter（7B vs 14B 路由） | 任务复杂度分类，自动选择模型 |
| #16 | 实现 MultiPathReasoner（多路径推理） | 多路径生成 + 验证器过滤 |
| #17 | 实现错误自动记录机制 | 用户纠正时自动写入 error_store |

### Phase 4: Web UI + API (预计 2 天)

| Issue | 标题 | 描述 |
|-------|------|------|
| #18 | 实现 FastAPI 服务层 | REST API + WebSocket |
| #19 | 实现聊天页面 | 实时对话，流式输出，来源显示 |
| #20 | 实现知识库浏览页面 | 搜索、查看、删除文档 |
| #21 | 实现错误本页面 | 查看、搜索、管理错误经验 |
| #22 | 实现 GPU 状态页面 | 实时显示 GPU 状态和让路等级 |

### Phase 5: GPU Guardian (预计 1-2 天)

| Issue | 标题 | 描述 |
|-------|------|------|
| #23 | 实现 GPU 监控器 | nvidia-smi 轮询，GPU 使用率/显存/进程 |
| #24 | 实现让路策略引擎 | 让路等级判定 + 动作执行 |
| #25 | 实现进程监听器 | 检测游戏/创作软件进程 |

### Phase 6: MVP 集成测试 (预计 1 天)

| Issue | 标题 | 描述 |
|-------|------|------|
| #26 | MVP 端到端集成测试 | 从资料拖入到聊天检索的完整闭环测试 |
| #27 | 编写 README 和用户文档 | MVP 使用说明，配置指南 |

---

## 十、MVP 阶段专注于子集

MVP 只实现上述 Issue 的一个子集，按依赖顺序：

```
#1  →  #2  →  #3  →  #4  →  #5  →  #6  →  #7  →  #8
 →  #9  →  #10 →  #11 →  #13 →  #14 →  #17 →  #18
 →  #19 →  #26 →  #27
```

**MVP 不包括：**
- #12 InboxWatcher（先手动触发）
- #15 TaskRouter（MVP 固定使用 light 模型）
- #16 MultiPathReasoner（MVP 使用单路径）
- #20-#22 Web UI 扩展页面（MVP 只做聊天页）
- #23-#25 GPU Guardian（MVP 不做，后续版本）
- 多 provider 支持（MVP 只支持 Ollama）
