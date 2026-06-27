# MemoryQwen — 第一批可执行 Issue

每个 Issue 包含：目标、输入、输出、验收标准、测试方式。

---

## Phase 0: 项目脚手架

### Issue #1: 搭建项目目录结构和配置系统

**目标：** 创建完整的 MemoryQwen 项目骨架，包括目录树、配置文件加载、日志系统。

**输入：**
- `docs/architecture.md` 中的目录结构
- `config/default.yaml` 配置模板

**输出：**
```
MemoryQwen/
├── requirements.txt
├── config/default.yaml
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py
│   └── config.py
├── ... (目录占位文件)
```

**验收标准：**
- [x] 所有目录已创建且有 `__init__.py` 或 `.gitkeep` 占位
- [x] `src/config.py` 能正确加载 `config/default.yaml` 并返回 pydantic 模型
- [x] 配置缺失时有明确的默认值
- [x] 配置覆盖机制：环境变量 > 自定义路径 > default.yaml
- [x] 日志系统已配置，使用 `structlog` 或标准 `logging` 格式化输出

**测试方式：**
```bash
cd MemoryQwen
python -c "from src.config import load_config; cfg = load_config(); print(cfg.model.name)"
# 应输出: "MemoryQwen"
```

---

### Issue #2: 创建 start.bat 一键启动脚本

**目标：** 用户双击即可启动整个系统。

**输入：** 项目目录、`requirements.txt`、依赖清单

**输出：** `start.bat`

**验收标准：**
- [x] 检查 Python 3.11+ 是否安装
- [x] 自动创建并激活 virtualenv
- [x] pip install -r requirements.txt
- [x] 启动 uvicorn
- [x] 打开浏览器到 http://localhost:7860
- [x] Ctrl+C 优雅停止

**测试方式：**
```bash
# 在干净环境中测试
./start.bat
# 浏览器应能访问 http://localhost:7860
```

---

### Issue #3: 初始化测试框架

**目标：** 配置 pytest 环境和测试辅助工具。

**输入：** `tests/` 目录、项目结构

**输出：**
- `tests/conftest.py`（全局 fixtures）
- `tests/helpers.py`（测试辅助函数）
- 能运行的示例测试

**验收标准：**
- [x] `pytest` 能发现并运行所有测试
- [x] 有 fixture 创建临时测试目录
- [x] 有 fixture 创建测试用的 ChromaDB 实例
- [x] 有 fixture  mock 模型调用（返回预设回复）

**测试方式：**
```bash
cd MemoryQwen
pytest tests/ -v --cov=src
# 应输出测试进度和覆盖率
```

---

## Phase 1: 模型通信 + 记忆核心

### Issue #4: 实现 ModelAdapter 基类和 OpenAI-compatible 适配器

**目标：** 实现统一的模型通信层，支持通过 OpenAI-compatible API 调用 Ollama。

**输入：**
- Ollama 服务运行在 `http://localhost:11434`
- 模型 `qwen2.5:7b` 已安装

**输出：**
- `src/model_adapter/base.py` — `BaseModelAdapter` 抽象基类
- `src/model_adapter/openai_compat.py` — `OpenAICompatAdapter` 实现
- `src/model_adapter/__init__.py` — 工厂函数

**核心接口：**
```python
class ChatResult:
    content: str
    token_usage: dict       # {"prompt": n, "completion": n, "total": n}
    model: str
    latency_ms: float

class BaseModelAdapter:
    async def chat(messages, model, temperature, max_tokens, tools) -> ChatResult
    async def embed(texts, model) -> list[list[float]]
```

**验收标准：**
- [x] `chat()` 能正确调用 Ollama 并返回结构化结果
- [x] `embed()` 能正确获取 embedding 向量
- [x] 错误处理：Ollama 不可用时返回明确的 ConnectionError
- [x] token 用量统计准确
- [x] 支持 tools/function calling 传输（即使模型不用也保持格式兼容）

**测试方式：**
```python
# 单元测试（mock）
adapter = OpenAICompatAdapter(base_url="http://localhost:11434")
result = await adapter.chat(
    messages=[{"role": "user", "content": "你好"}],
    model="qwen2.5:7b",
)
assert len(result.content) > 0
assert result.token_usage["total"] > 0

# embedding 测试
embeddings = await adapter.embed(["测试文本"])
assert len(embeddings[0]) > 0  # 512 or 768 dims
```

---

### Issue #5: 实现 Embedding 管理和 ChromaDB 封装

**目标：** 封装向量数据库操作，提供统一的 embedding 管理和向量检索接口。

**输入：**
- `config/default.yaml` 中的 embedding 配置
- `memory/` 目录

**输出：**
- `src/memory_bus/embedding.py` — EmbeddingManager
- `src/memory_bus/vector_store.py` — VectorStore 封装

**核心接口：**
```python
class EmbeddingManager:
    async def embed(text: str) -> list[float]
    async def embed_batch(texts: list[str]) -> list[list[float]]

class VectorStore:
    def __init__(self, collection_name: str, persist_dir: str)
    async def add(ids, embeddings, metadatas, documents)
    async def search(query_embedding, top_k, filters) -> list[ScoredEntry]
    async def delete(ids)
    async def count() -> int
```

**验收标准：**
- [x] ChromaDB 集合创建和持久化正常
- [x] 添加文档后能正确检索
- [x] 支持 metadata 过滤
- [x] 支持批量操作
- [x] 持久化目录可配置

**测试方式：**
```python
store = VectorStore("test_knowledge", "./memory/test_chroma")
await store.add(
    ids=["doc1"],
    embeddings=[[0.1, 0.2, ...]],  # 实际用真实 embedding
    metadatas=[{"source": "test.md"}],
    documents=["这是测试文档"],
)
results = await store.search(query_embedding=[0.1, 0.2, ...], top_k=1)
assert len(results) == 1
assert results[0].content == "这是测试文档"
```

---

### Issue #6: 实现 KnowledgeStore（知识库存储）

**目标：** 知识库存储模块，管理用户资料的向量索引 + BM25 关键词索引，支持混合检索。

**输入：**
- `config.yaml` 检索配置（top_k, RRF 权重）
- 切片后的文档块

**输出：** `src/memory_bus/knowledge_store.py`

**核心接口：**
```python
class KnowledgeStore:
    async def add_chunk(chunk: Chunk) -> str
    async def add_chunks(chunks: list[Chunk]) -> list[str]
    async def search(query: str, top_k: int = 5) -> list[SearchResult]
    async def hybrid_search(query: str, top_k: int = 5) -> list[SearchResult]
    async def delete(doc_id: str) -> bool
    async def list_documents() -> list[DocumentInfo]
    async def count() -> int
```

**验收标准：**
- [x] 支持向量检索（embedding -> ChromaDB）
- [x] 支持 BM25 关键词检索（纯内存 BM25 或 tiny 实现）
- [x] 支持 RRF（Reciprocal Rank Fusion）混合排序
- [x] 返回结果包含来源元数据（文件名、段落位置）
- [x] 支持按文档来源删除

**测试方式：**
```python
store = KnowledgeStore(config)
await store.add_chunks([
    Chunk(content="Python 是一种编程语言", metadata={"source": "test.md"}),
    Chunk(content="Java 也是一种编程语言", metadata={"source": "test.md"}),
])
results = await store.hybrid_search("Python 编程", top_k=3)
assert len(results) > 0
assert "Python" in results[0].content
assert results[0].metadata["source"] == "test.md"
```

---

### Issue #7: 实现 ChatMemory（聊天记忆存储）

**目标：** 存储聊天记录，支持按 session 检索、时间线回放、摘要管理。

**输入：** SQLite 数据库路径、session 配置

**输出：** `src/memory_bus/chat_memory.py`

**核心接口：**
```python
class ChatMemory:
    async def create_session(title: str) -> str  # 返回 session_id
    async def add_message(session_id, role, content, sources, tokens)
    async def get_session(session_id) -> Session
    async def list_sessions(limit=20) -> list[SessionSummary]
    async def get_history(session_id, limit=50) -> list[Message]
    async def update_summary(session_id, summary: str)
    async def delete_session(session_id)
    async def search_messages(query: str, limit=10) -> list[Message]
```

**验收标准：**
- [x] 创建 session 返回唯一 ID
- [x] 消息保存完整（role, content, sources, tokens, timestamp）
- [x] 支持按 session 检索历史
- [x] 支持 session 摘要的生成和更新
- [x] SQLite 文件创建在 `memory/chat_memory/` 下

**测试方式：**
```python
chat = ChatMemory(config)
sid = await chat.create_session("测试会话")
await chat.add_message(sid, "user", "你好")
await chat.add_message(sid, "assistant", "你好！有什么可以帮助你的？")
msgs = await chat.get_history(sid)
assert len(msgs) == 2
assert msgs[0].content == "你好"

sessions = await chat.list_sessions()
assert len(sessions) >= 1
```

---

### Issue #8: 实现 ErrorStore（错误经验库）

**目标：** 存储 AI 犯过的错误，支持相似问题检索，避免重复犯错。

**输入：** SQLite + ChromaDB 配置

**输出：** `src/memory_bus/error_store.py`

**核心接口：**
```python
class ErrorStore:
    async def add_error(entry: ErrorEntry) -> str
    async def search_similar(query: str, top_k: int = 5) -> list[ErrorEntry]
    async def get_error(error_id: str) -> ErrorEntry
    async def list_errors(limit=20) -> list[ErrorSummary]
    async def mark_hit(error_id: str)  # 增加命中计数
    async def delete_error(error_id: str) -> bool
```

**验收标准：**
- [x] 错误记录包含：触发问题、错误回答、正确回答、根因
- [x] 支持向量相似度检索（通过 embedding）
- [x] 支持标签分类筛选
- [x] 命中计数自动更新
- [x] 新错误加入后，Agent 遇到相似问题时能检索到

**测试方式：**
```python
store = ErrorStore(config)
eid = await store.add_error(ErrorEntry(
    trigger_query="1+1等于几？",
    wrong_answer="3",
    correct_answer="2",
    root_cause="基础算术错误",
    tags=["math", "arithmetic"],
))
results = await store.search_similar("1+1等于多少", top_k=3)
assert len(results) > 0
assert results[0].trigger_query == "1+1等于几？"
```

---

## Phase 2: 文档摄入

### Issue #9: 实现 DocumentParser（多格式文件解析器）

**目标：** 将 PDF、txt、md、docx、代码文件解析为统一的结构化文档格式。

**输入：** 文件路径

**输出：** `src/ingestion/parser.py`

**核心接口：**
```python
@dataclass
class Document:
    file_path: str
    file_type: str          # "pdf" | "txt" | "md" | "docx" | "code"
    title: str
    content: str            # 纯文本内容
    metadata: dict          # 原始元数据
    pages: int | None
    char_count: int

class DocumentParser:
    async def parse(file_path: str) -> Document
    def can_handle(file_path: str) -> bool
    def supported_extensions() -> list[str]
```

**验收标准：**
- [x] txt 文件直接读取
- [x] md 文件解析为纯文本（保留标题层级信息）
- [x] PDF 文件提取全部文本（至少第一页）
- [x] docx 文件提取文本
- [x] 代码文件按文件类型读取
- [x] 不支持的格式抛出明确的 UnsupportedFormatError
- [x] 返回 Document 包含文件路径、类型、标题、内容

**测试方式：**
```python
parser = DocumentParser()

# 测试 md
doc = await parser.parse("test.md")
assert doc.content is not None
assert len(doc.content) > 0

# 测试 txt
doc = await parser.parse("test.txt")
assert doc.content is not None

# 测试不支持格式
try:
    await parser.parse("test.xyz")
    assert False, "应抛出异常"
except UnsupportedFormatError:
    pass
```

---

### Issue #10: 实现 DocumentChunker（语义切片器）

**目标：** 将长文档按语义边界切片，控制每块 token 数不超过上限。

**输入：** Document 对象

**输出：** `src/ingestion/chunker.py`

**核心接口：**
```python
@dataclass
class Chunk:
    doc_id: str
    content: str
    token_count: int
    chunk_index: int
    metadata: dict

class DocumentChunker:
    def chunk(
        document: Document,
        max_tokens: int = 512,
        overlap: int = 32,
    ) -> list[Chunk]
```

**切片策略（按优先级）：**
1. Markdown 标题边界分割
2. 段落空行分割
3. 句子边界分割（句号、问号、感叹号）
4. 固定 token 数截断

**验收标准：**
- [x] 切片后每个 Chunk 不超过 max_tokens
- [x] Chunk 之间保留 overlap_tokens 重叠（避免断句丢失语义）
- [x] markdown 文件按标题层级分组切片
- [x] 每个 Chunk 携带来源 metadata
- [x] 短文档（< max_tokens）返回单块
- [x] token 计数使用 tiktoken

**测试方式：**
```python
chunker = DocumentChunker(max_tokens=512)
doc = Document(content="..." * 1000, ...)
chunks = chunker.chunk(doc)
assert all(c.token_count <= 600 for c in chunks)  # 允许少量超出
assert len(chunks) > 0
assert all(c.doc_id == doc.file_path for c in chunks)
```

---

### Issue #11: 实现 Indexer（索引构建 Pipeline）

**目标：** 将解析→切片→索引串联为完整的 pipeline。

**输入：** 文件路径列表

**输出：** `src/ingestion/indexer.py`

**核心接口：**
```python
@dataclass
class IndexResult:
    doc_id: str
    file_path: str
    chunks_count: int
    total_tokens: int
    success: bool
    error: str | None

class Indexer:
    def __init__(self, parser, chunker, knowledge_store)
    
    async def index_file(file_path: str) -> IndexResult
    async def index_files(file_paths: list[str]) -> list[IndexResult]
    async def remove_document(doc_id: str) -> bool
```

**验收标准：**
- [x] 单个文件索引完整走通（parse → chunk → embed → store）
- [x] 多次索引同一文件时自动更新（先删除旧版本再写入）
- [x] 错误文件不会中断批量索引
- [x] 返回每个文件的索引结果（成功/失败/原因）

**测试方式：**
```python
indexer = Indexer(parser, chunker, knowledge_store)
result = await indexer.index_file("test.md")
assert result.success == True
assert result.chunks_count > 0
assert result.doc_id is not None

# 验证已入库
results = await knowledge_store.search("test content")
assert len(results) > 0
```

---

## Phase 3: Agent 核心

### Issue #13: 实现 Agent 主循环

**目标：** 构建 Agent 的核心处理循环，接收用户消息 → 检索 → 调用模型 → 返回结果。

**输入：**
- 用户消息
- Session ID
- 模型 tier（light/deep）

**输出：** `src/agent/core.py`, `src/agent/context.py`

**核心接口：**
```python
@dataclass
class AgentResponse:
    content: str
    sources: list[SourceRef]
    token_usage: dict
    model_used: str
    latency_ms: float

class Agent:
    def __init__(self, config, model_adapter, memory_bus)
    
    async def process_message(
        message: str,
        session_id: str,
        model_tier: str = "light",
    ) -> AgentResponse
    
    async def process_message_stream(
        message: str,
        session_id: str,
    ) -> AsyncIterator[str]
```

**上下文构建逻辑：**
```
上下文分层（按 token 预算从高到低）：
1. System Prompt（固定的系统指令）
2. Session Summary（当前会话摘要）
3. Memory Results（记忆检索结果 + 错误经验）
4. Recent History（最近 N 条消息）
5. Current Message（当前用户输入）
```

**验收标准：**
- [x] 消息能正确经过 Agent 处理并返回回答
- [x] 回答中包含来源引用（如果检索到相关记忆）
- [x] 上下文 token 预算管理有效（不超出模型限制）
- [x] 支持流式输出
- [x] 对话历史自动保存到 chat_memory
- [x] 新 session 正常创建

**测试方式：**
```python
# 集成测试
agent = Agent(config, adapter, memory)
response = await agent.process_message("什么是 Python？", session_id="test")
assert len(response.content) > 0
assert response.model_used is not None

# 流式测试
async for chunk in agent.process_message_stream("你好", session_id="test"):
    assert len(chunk) > 0
```

---

### Issue #14: 实现 ContextBuilder（上下文构建器）

**目标：** 管理有限的上下文窗口，按优先级分层构建提示词。

**输入：** 用户消息、session_id、配置

**输出：** `src/agent/context.py`

**核心接口：**
```python
@dataclass
class AgentContext:
    system_prompt: str
    memories: list[MemoryEntry]
    chat_history: list[Message]
    current_message: str
    total_tokens: int
    budget: dict

class ContextBuilder:
    def __init__(self, config, chat_memory, memory_bus)
    
    async def build(
        message: str,
        session_id: str,
        model_max_tokens: int = 8192,
    ) -> AgentContext
    
    async def build_system_prompt(
        session_summary: str | None,
        error_memories: list[ErrorEntry],
    ) -> str
```

**预算策略：**
```
1. 预留 response_reserved tokens 给模型输出
2. system_prompt 固定占用
3. session_summary 压缩到 budget
4. memories 按分数排序截断
5. 剩余 token 给 chat_history（从最新消息往前截断）
```

**验收标准：**
- [x] 最终 token 总数不超过 model_max_tokens
- [x] 记忆按相关性排序，低分优先丢弃
- [x] 历史消息从旧到新保留，超出时从旧消息开始丢弃
- [x] 系统提示词包含错误记忆提示
- [x] token 计数准确

**测试方式：**
```python
builder = ContextBuilder(config, chat_memory, memory_bus)
context = await builder.build("你好", "test_session")
assert context.total_tokens <= 8192
assert len(context.system_prompt) > 0
```

---

### Issue #17: 实现错误自动记录机制

**目标：** 用户指出 AI 回答错误时，自动将修正写入 error_store。

**输入：** 用户消息、AI 回答、纠正反馈

**输出：** `src/agent/correction.py`

**核心接口：**
```python
class CorrectionHandler:
    def __init__(self, error_store)
    
    async def detect_and_record(
        user_message: str,
        assistant_response: str,
        user_feedback: str,         # 用户的纠正/补充
    ) -> ErrorEntry | None
    
    async def is_correction(
        user_message: str,
        history: list[Message],
    ) -> tuple[bool, str]   # (is_correction, corrected_text)
```

**触发模式：**
- "不对" / "错了" / "正确的是" / "应该是"
- 用户直接给出纠正内容
- 用户对同一问题重复问不同答案

**验收标准：**
- [x] 能检测用户的纠正意图
- [x] 自动提取纠正内容
- [x] 写入 error_store
- [x] 标记与此错误相关的原始回答

**测试方式：**
```python
handler = CorrectionHandler(error_store)
entry = await handler.detect_and_record(
    user_message="1+1等于几？",
    assistant_response="3",
    user_feedback="不对，1+1=2",
)
assert entry is not None
assert entry.correct_answer == "2"
```

---

## Phase 4: Web UI + API

### Issue #18: 实现 FastAPI 服务层

**目标：** 构建 REST API + WebSocket 服务，将所有核心功能暴露为 API。

**输入：** Agent、MemoryBus、Ingestion 模块

**输出：** `src/server/api.py`, `src/server/websocket.py`

**API 端点：**
```
POST /api/chat              → Agent.process_message()
GET  /api/sessions          → ChatMemory.list_sessions()
POST /api/sessions          → ChatMemory.create_session()
GET  /api/sessions/{id}     → ChatMemory.get_session() + get_history()
POST /api/ingestion         → Indexer.index_file()
GET  /api/memory/knowledge  → KnowledgeStore.hybrid_search()
GET  /api/memory/errors     → ErrorStore.search_similar()
POST /api/correction        → CorrectionHandler.detect_and_record()
GET  /api/system/status     → 系统状态汇总
WS   /ws/chat               → 流式聊天
```

**验收标准：**
- [x] 所有 API 端点响应正确
- [x] 自动生成 OpenAPI 文档 (http://localhost:7860/docs)
- [x] CORS 配置正确
- [x] WebSocket 端支持流式输出
- [x] 错误返回结构化 JSON

**测试方式：**
```bash
# 启动 server
python -m src
# 测试 API
curl http://localhost:7860/api/sessions
curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "session_id": "test"}'
```

---

### Issue #19: 实现聊天页面

**目标：** 用户可以在浏览器中与 AI 对话。

**输入：** API 服务

**输出：** `ui/templates/chat.html`, `ui/static/js/chat.js`

**页面功能：**
- 消息列表（用户 vs AI 气泡式布局）
- 输入框 + 发送按钮
- Markdown 渲染（AI 回答）
- 来源引用显示（来源文件名、段落预览）
- 新对话按钮
- 会话列表侧边栏
- 流式打字效果

**验收标准：**
- [x] 能发送消息并看到 AI 回复
- [x] 流式输出实时显示（非一次性渲染）
- [x] Markdown 渲染正常（代码块、表格、列表）
- [x] 来源引用可点击展开
- [x] 会话切换和新建正常
- [x] 页面美观、响应式

**测试方式：**
```bash
# 打开浏览器访问
http://localhost:7860
# 发送消息，观察回复
```

---

## Phase 5: GPU Guardian（MVP 后）

### Issue #23: 实现 GPU 监控器

**目标：** 实时监控 GPU 使用率、显存占用、关键进程。

**输入：** nvidia-smi 或 nvidia-ml-py

**输出：** `src/gpu_guardian/monitor.py`

**验收标准：**
- [x] 每 5 秒采集一次 GPU 数据
- [x] 检测 GPU 使用率 %
- [x] 检测显存占用 GB
- [x] 检测前台高 GPU 负载进程
- [x] 数据可通过 API 查询

### Issue #24: 实现让路策略引擎

**目标：** 根据 GPU 状态自动切换让路等级。

**验收标准：**
- [x] 从 L0 到 L4 的自动切换
- [x] 用户恢复空闲后自动升回 L0
- [x] 可配置的触发阈值
- [x] 让路事件可查询和展示

---

## 各 Issue 依赖关系图

```
#1 ──→ #2 ──→ #3 ──→ #4 ──→ #5 ──→ #6 ──→ #7 ──→ #8
                       │                       │
                       ▼                       ▼
                      #9 ──→ #10 ──→ #11      #17
                               │               │
                               ▼               ▼
                              #13 ──→ #14 ──→ #18 ──→ #19
                                                │
                                                ▼
                                               #26
                                                │
                                                ▼
                                               #27
```

**说明：** 箭头表示依赖关系，后面的 Issue 依赖前面的 Issue 完成。
- #12 InboxWatcher → 可选，MVP 阶段手动触发摄入（POST /api/ingestion）
- #15 TaskRouter → MVP 后，MVP 固定使用 7B
- #16 MultiPathReasoner → MVP 后
- #20-#22 页面 → MVP 后，MVP 只做聊天页面 #19
- #23-#25 GPU Guardian → MVP 后

---

## MVP 验收 checklist（端到端）

```
[ ] 1. 双击 start.bat 启动系统
[ ] 2. 浏览器打开 http://localhost:7860 看到聊天页面
[ ] 3. 发送消息，AI 回复（通过 Ollama + 7B 模型）
[ ] 4. 拖入 test.md 到 inbox/
[ ] 5. 手动触发索引（API 或 UI 按钮）
[ ] 6. 询问与文档内容相关的问题，AI 能引用文档回答
[ ] 7. 指出回答错误，错误被记录
[ ] 8. 再次问类似问题，AI 参考错误记录不再犯同样错误
[ ] 9. 新建对话，历史记忆仍可检索
[ ] 10. 查看 OpenAPI 文档确认接口完整
```
