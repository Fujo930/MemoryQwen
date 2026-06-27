"""
MemoryQwen — OpenAI-compatible API 适配器
支持通过 OpenAI 兼容协议调用 Ollama / LM Studio / llama.cpp 等后端
"""

from __future__ import annotations

import time
import logging
from typing import Any

from openai import AsyncOpenAI
from src.model_adapter.base import (
    BaseModelAdapter, ChatResult, EmbeddingResult, ModelProfile,
)

logger = logging.getLogger(__name__)


class OpenAICompatAdapter(BaseModelAdapter):
    """OpenAI-compatible API 适配器"""

    def __init__(self, config: Any):
        super().__init__(config)
        provider_cfg = config.model.providers.get(
            config.model.default_provider, {}
        )
        base_url = provider_cfg.base_url.rstrip("/") + "/v1"
        api_key = provider_cfg.api_key or "not-needed"

        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.base_url = base_url
        self.default_embed_model = config.model.embedding_model

    async def chat(
        self,
        messages: list[dict],
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        tools: list[dict] | None = None,
        stream: bool = False,
    ) -> ChatResult:
        """统一聊天接口"""
        if model == "default":
            model = self.config.model.default_light_model

        start = time.time()
        kwargs = dict(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
        )
        if tools:
            kwargs["tools"] = tools

        try:
            if stream:
                return await self._chat_stream(**kwargs)
            response = await self.client.chat.completions.create(**kwargs)
        except Exception as e:
            logger.error("Chat API call failed: %s", e)
            raise

        elapsed = (time.time() - start) * 1000
        choice = response.choices[0]

        return ChatResult(
            content=choice.message.content or "",
            token_usage={
                "prompt": response.usage.prompt_tokens if response.usage else 0,
                "completion": response.usage.completion_tokens if response.usage else 0,
                "total": response.usage.total_tokens if response.usage else 0,
            },
            model=response.model,
            latency_ms=round(elapsed, 2),
            finish_reason=choice.finish_reason or "stop",
            tool_calls=choice.message.tool_calls,
        )

    async def _chat_stream(self, **kwargs):
        """流式聊天（累积返回）"""
        kwargs["stream"] = True
        response = await self.client.chat.completions.create(**kwargs)

        content = ""
        token_usage = {}
        model = kwargs["model"]
        start = time.time()

        async for chunk in response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                content += delta.content
            if chunk.usage:
                token_usage = {
                    "prompt": chunk.usage.prompt_tokens or 0,
                    "completion": chunk.usage.completion_tokens or 0,
                    "total": chunk.usage.total_tokens or 0,
                }
            if chunk.model:
                model = chunk.model

        elapsed = (time.time() - start) * 1000
        return ChatResult(
            content=content,
            token_usage=token_usage,
            model=model,
            latency_ms=round(elapsed, 2),
        )

    async def embed(
        self,
        texts: list[str],
        model: str = "default",
    ) -> EmbeddingResult:
        """统一 embedding 接口"""
        if model == "default":
            model = self.default_embed_model

        start = time.time()
        try:
            # Ollama 的 embedding API 通过 OpenAI compat 调用
            response = await self.client.embeddings.create(
                model=model,
                input=texts,
            )
        except Exception as e:
            logger.warning("Embedding via OpenAI compat failed: %s", e)
            # 回退到本地 sentence-transformers
            return await self._fallback_embed(texts)

        elapsed = (time.time() - start) * 1000
        embeddings = [item.embedding for item in response.data]

        return EmbeddingResult(
            embeddings=embeddings,
            model=model,
            token_usage=response.usage.total_tokens if response.usage else 0,
            latency_ms=round(elapsed, 2),
        )

    async def _fallback_embed(self, texts: list[str]) -> EmbeddingResult:
        """回退 embed：使用本地 sentence-transformers"""
        try:
            from sentence_transformers import SentenceTransformer
            model_name = self.config.model.embedding_model
            device = self.config.model.embedding_device

            logger.info("Using local embedding model: %s (%s)", model_name, device)
            model = SentenceTransformer(model_name, device=device)
            embeddings = model.encode(texts, show_progress_bar=False)

            return EmbeddingResult(
                embeddings=embeddings.tolist(),
                model=model_name,
                latency_ms=0.0,
            )
        except ImportError:
            logger.error("sentence-transformers not installed, cannot embed")
            raise RuntimeError("No embedding backend available")
