"""
MemoryQwen — API 服务层
FastAPI REST API + WebSocket
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json

from src.config import AppConfig
from src.model_adapter import create_adapter
from src.memory_bus import MemoryBus
from src.agent.core import Agent
from src.agent.correction import CorrectionHandler
from src.ingestion.parser import DocumentParser
from src.ingestion.chunker import DocumentChunker
from src.ingestion.indexer import Indexer

logger = logging.getLogger(__name__)


# ─── 全局状态 ───────────────────────────────────────

class AppState:
    def __init__(self, config: AppConfig):
        self.config = config
        self.model_adapter = create_adapter(config)
        self.memory_bus = MemoryBus(config)
        self.agent = Agent(config, self.model_adapter, self.memory_bus)
        self.parser = DocumentParser(config)
        self.chunker = DocumentChunker(config)
        self.indexer = Indexer(self.parser, self.chunker, self.memory_bus.knowledge)
        self.correction_handler = CorrectionHandler(self.memory_bus.errors, config)


state: AppState | None = None


# ─── 请求模型 ───────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str = ""
    model_tier: str = "light"


class ChatResponse(BaseModel):
    response: str
    sources: list[dict] = []
    token_usage: dict = {}
    model_used: str = ""
    latency_ms: float = 0.0


class SessionCreate(BaseModel):
    title: str = "新对话"


class IndexRequest(BaseModel):
    file_path: str


class CorrectionRequest(BaseModel):
    user_message: str
    assistant_response: str
    user_feedback: str


class IngestionStatusRequest(BaseModel):
    directory: str = ""


# ─── 应用工厂 ───────────────────────────────────────

def create_app(config: AppConfig) -> FastAPI:
    global state
    state = AppState(config)

    app = FastAPI(
        title="MemoryQwen",
        version=config.system.version,
        description="本地 AI Agent 系统",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.server.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Static files
    from pathlib import Path as PPath
    static_dir = PPath("ui/static").resolve()
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # ─── Routes ───────────────────────────────────

    @app.get("/", response_class=HTMLResponse)
    async def root():
        """主页"""
        from pathlib import Path as PPath2
        template_path = PPath2("ui/templates/chat.html")
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")
        return "<html><body><h1>MemoryQwen</h1><p>Chat UI not found</p></body></html>"

    @app.get("/api/status")
    async def get_status():
        """系统状态"""
        try:
            memory_count = await state.memory_bus.knowledge.count()
            error_count = await state.memory_bus.errors.count()
        except Exception:
            memory_count = 0
            error_count = 0

        return {
            "name": config.system.name,
            "version": config.system.version,
            "model_light": config.model.default_light_model,
            "model_deep": config.model.default_deep_model,
            "knowledge_chunks": memory_count,
            "errors": error_count,
            "status": "running",
        }

    # ─── Chat ─────────────────────────────────────

    @app.post("/api/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        """发送聊天消息"""
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="消息不能为空")

        # 自动创建 session
        session_id = request.session_id
        if not session_id:
            session_id = await state.memory_bus.chat.create_session()

        # 处理消息
        response = await state.agent.process_message(
            message=request.message,
            session_id=session_id,
            model_tier=request.model_tier,
        )

        return ChatResponse(
            response=response.content,
            sources=[s.__dict__ if hasattr(s, '__dict__') else s for s in response.sources],
            token_usage=response.token_usage,
            model_used=response.model_used,
            latency_ms=response.latency_ms,
        )

    @app.get("/api/chat/stream/{session_id}")
    async def chat_stream(session_id: str, message: str, model_tier: str = "light"):
        """流式聊天 (SSE)"""
        from fastapi.responses import StreamingResponse

        if not session_id:
            session_id = await state.memory_bus.chat.create_session()

        async def generate():
            response = await state.agent.process_message(message, session_id, model_tier)
            for char in response.content:
                yield f"data: {json.dumps({'text': char, 'session_id': session_id})}\n\n"
            yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    # ─── WebSocket ─────────────────────────────────

    @app.websocket("/ws/chat")
    async def websocket_chat(websocket: WebSocket):
        """WebSocket 实时聊天"""
        await websocket.accept()
        session_id = None

        try:
            while True:
                data = await websocket.receive_text()
                payload = json.loads(data)
                message = payload.get("message", "")
                session_id = payload.get("session_id", session_id or "")
                model_tier = payload.get("model_tier", "light")

                if not session_id:
                    session_id = await state.memory_bus.chat.create_session()

                response = await state.agent.process_message(
                    message=message,
                    session_id=session_id,
                    model_tier=model_tier,
                )

                await websocket.send_json({
                    "type": "response",
                    "content": response.content,
                    "sources": [s.__dict__ if hasattr(s, '__dict__') else s for s in response.sources],
                    "session_id": session_id,
                    "model_used": response.model_used,
                    "latency_ms": response.latency_ms,
                })

        except WebSocketDisconnect:
            logger.info("WebSocket disconnected")
        except Exception as e:
            logger.error("WebSocket error: %s", e)
            try:
                await websocket.send_json({"type": "error", "content": str(e)})
            except Exception:
                pass

    # ─── Sessions ──────────────────────────────────

    @app.get("/api/sessions")
    async def list_sessions():
        """列出最近会话"""
        sessions = await state.memory_bus.chat.list_sessions()
        return {"sessions": sessions}

    @app.post("/api/sessions")
    async def create_session(request: SessionCreate):
        """创建新会话"""
        session_id = await state.memory_bus.chat.create_session(request.title)
        return {"session_id": session_id, "title": request.title}

    @app.get("/api/sessions/{session_id}")
    async def get_session(session_id: str):
        """获取会话详情和消息"""
        session = await state.memory_bus.chat.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        history = await state.memory_bus.chat.get_history(session_id)
        return {"session": session, "messages": history}

    # ─── Ingestion ─────────────────────────────────

    @app.post("/api/ingestion")
    async def index_file(request: IndexRequest):
        """手动触发文件索引"""
        result = await state.indexer.index_file(request.file_path)
        return {
            "success": result.success,
            "doc_id": result.doc_id,
            "chunks_count": result.chunks_count,
            "total_tokens": result.total_tokens,
            "error": result.error,
        }

    @app.post("/api/ingestion/inbox")
    async def index_inbox(request: IngestionStatusRequest):
        """索引 inbox 目录"""
        inbox_dir = request.directory or config.system.inbox_dir
        results = await state.indexer.index_inbox(inbox_dir)
        return {
            "total": len(results),
            "success": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "results": [
                {
                    "file": r.file_path,
                    "success": r.success,
                    "chunks": r.chunks_count,
                    "error": r.error,
                }
                for r in results
            ],
        }

    # ─── Memory / Knowledge ────────────────────────

    @app.get("/api/memory/knowledge")
    async def search_knowledge(q: str = "", top_k: int = 5):
        """搜索知识库"""
        if not q.strip():
            docs = await state.memory_bus.knowledge.list_documents()
            return {"documents": docs, "results": []}
        results = await state.memory_bus.knowledge.hybrid_search(q, top_k=top_k)
        return {
            "results": [
                {
                    "id": r.id,
                    "content": r.content[:300],
                    "score": r.score,
                    "metadata": r.metadata,
                }
                for r in results
            ],
        }

    # ─── Errors ────────────────────────────────────

    @app.get("/api/memory/errors")
    async def list_errors(limit: int = 20):
        """列出错误经验"""
        errors = await state.memory_bus.errors.list_errors(limit=limit)
        return {"errors": errors}

    @app.post("/api/correction")
    async def report_correction(request: CorrectionRequest):
        """报告纠正"""
        result = await state.correction_handler.detect_and_record(
            user_message=request.user_feedback,
            last_assistant_response=request.assistant_response,
            history=[{"role": "user", "content": request.user_message}],
        )
        if result:
            return {"recorded": True, "error_id": result["error_id"]}
        return {"recorded": False, "reason": "未检测到纠正意图"}

    # ─── System ────────────────────────────────────

    @app.get("/api/system/gpu")
    async def gpu_status():
        """GPU 状态（预留）"""
        return {
            "gpu_guardian_enabled": config.gpu_guardian.enabled,
            "status": "not_implemented",
        }

    return app
