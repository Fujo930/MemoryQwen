# MemoryQwen MVP 开发计划

## 目标

**MVP 最小闭环：**
```
用户拖入资料 → 解析 → 切片 → 索引 → Web UI 聊天 → Agent 检索资料
→ 调用本地模型 → 输出带来源的回答 → 保存聊天记忆 → 用户纠正错误
→ 错误写入 error_store → 下次检索错误经验
```

## 开发阶段

### Phase 0: 骨架 (预计 1 天)
完成时间：Day 1

| 步骤 | 任务 | 产出 |
|------|------|------|
| 0.1 | 创建目录结构 + `__init__.py` | 完整项目树 |
| 0.2 | 实现 `config.py`（yaml 加载 + pydantic 校验） | 配置系统 |
| 0.3 | 实现 `start.bat` + `requirements.txt` | 一键启动 |
| 0.4 | 初始化 `tests/` 框架 | pytest 运行环境 |

### Phase 1: 模型 + 记忆 (预计 2-3 天)
完成时间：Day 2-3

| 步骤 | 任务 | 产出 |
|------|------|------|
| 1.1 | `model_adapter/base.py` + `openai_compat.py` | 模型通信层 |
| 1.2 | `memory_bus/embedding.py` | Embedding 管理 |
| 1.3 | `memory_bus/knowledge_store.py` | 知识库存储 |
| 1.4 | `memory_bus/chat_memory.py` | 聊天记忆 |
| 1.5 | `memory_bus/error_store.py` | 错误经验库 |

### Phase 2: 文档摄入 (预计 2 天)
完成时间：Day 4-5

| 步骤 | 任务 | 产出 |
|------|------|------|
| 2.1 | `ingestion/parser.py` | 文件解析器 |
| 2.2 | `ingestion/chunker.py` | 切片器 |
| 2.3 | `ingestion/indexer.py` | 索引 Pipeline |

### Phase 3: Agent (预计 2-3 天)
完成时间：Day 6-7

| 步骤 | 任务 | 产出 |
|------|------|------|
| 3.1 | `agent/context.py` | 上下文构建器 |
| 3.2 | `agent/core.py` | Agent 主循环 |
| 3.3 | `agent/correction.py` | 错误记录机制 |

### Phase 4: Web UI (预计 2 天)
完成时间：Day 8-9

| 步骤 | 任务 | 产出 |
|------|------|------|
| 4.1 | `server/api.py` | REST API |
| 4.2 | `server/websocket.py` | WebSocket 流式 |
| 4.3 | `ui/templates/chat.html` + `ui/static/js/chat.js` | 聊天页面 |

### Phase 5: 集成测试 (预计 1 天)
完成时间：Day 10

| 步骤 | 任务 | 产出 |
|------|------|------|
| 5.1 | 端到端集成测试 | 完整闭环验证 |
| 5.2 | README + 用户文档 | 使用说明 |

## MVP 里程碑

| 里程碑 | 时间 | 检查点 |
|--------|------|--------|
| M1: 骨架搭建 | Day 1 | `python -m src` 启动成功 |
| M2: 模型通信 | Day 3 | 调用 Ollama 返回回答 |
| M3: 记忆存储 | Day 4 | 资料入库可检索 |
| M4: 文档摄入 | Day 5 | 文件解析→切片→索引全通 |
| M5: Agent 闭环 | Day 7 | 对话 + 检索 + 错误记录 |
| M6: Web UI | Day 9 | 浏览器可对话 |
| **M7: MVP Release** | **Day 10** | **完整闭环通过** |

## 风险与缓解

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| Ollama 无法调用 | 低 | 高 | 先用 mock 测试，保证接口层抽象 |
| PDF 解析质量差 | 中 | 中 | MVP 先支持 txt/md，PDF 用 pypdf 基本版 |
| 中文 embedding 效果差 | 低 | 中 | 用 bge-small-zh-v1.5，已验证效果好 |
| ChromaDB 持久化问题 | 中 | 中 | 测试阶段用临时目录，确认持久化正确 |
| 上下文超长 | 中 | 高 | ContextBuilder 有 token 预算机制兜底 |
