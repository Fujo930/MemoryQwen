"""
MemoryQwen — OpenAI-compatible ModelClient
支持 Ollama / LM Studio / llama.cpp / 任意 OpenAI-compatible API。
"""

from __future__ import annotations

import json
import logging
from typing import AsyncIterator, Any

import httpx

from src.model_client.base import (
    ModelClient, ChatResponse, CompleteResponse, ChatStreamEvent,
    ChatMessage,
    ModelClientError, ConnectionError, TimeoutError,
    AuthenticationError, ModelNotFoundError, RateLimitError,
)

logger = logging.getLogger(__name__)

ERROR_CODE_MAP: dict[int, type[ModelClientError]] = {
    401: AuthenticationError,
    404: ModelNotFoundError,
    429: RateLimitError,
}


class OpenAICompatibleClient(ModelClient):
    """
    OpenAI-compatible API 客户端。

    适用于：
    - Ollama (http://localhost:11434/v1)
    - LM Studio (http://localhost:1234/v1)
    - llama.cpp server (http://localhost:8080/v1)
    - OpenAI API (https://api.openai.com/v1)
    - 任何实现了 /v1/chat/completions 和 /v1/completions 的 API
    """

    def __init__(self, config: Any):
        super().__init__(config)
        cfg = config.model_client

        self.base_url = cfg.base_url.rstrip("/")
        if not self.base_url.endswith("/v1"):
            self.base_url += "/v1"

        self.api_key = cfg.api_key or "not-needed"
        self._timeout = cfg.timeout
        self._max_retries = cfg.max_retries
        self._default_model = cfg.model or None
        self._default_temperature = cfg.default_temperature
        self._default_max_tokens = cfg.default_max_tokens

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self._timeout),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

    # ─── Chat ──────────────────────────────────────────────

    async def chat(
        self,
        messages: list[dict] | list[ChatMessage],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
    ) -> ChatResponse | AsyncIterator[ChatStreamEvent]:
        """聊天补全"""
        payload = self._build_chat_payload(messages, model, temperature, max_tokens, stream)

        if stream:
            return self._chat_stream(payload)

        return await self._chat_sync(payload)

    def _build_chat_payload(
        self,
        messages: list[dict] | list[ChatMessage],
        model: str | None,
        temperature: float | None,
        max_tokens: int | None,
        stream: bool,
    ) -> dict:
        """构建 chat 请求 payload"""
        # 统一消息格式
        raw_messages: list[dict] = []
        for m in messages:
            if isinstance(m, ChatMessage):
                raw_messages.append({"role": m.role, "content": m.content})
            elif isinstance(m, dict):
                raw_messages.append(m)
            else:
                raise TypeError(f"Unexpected message type: {type(m)}")

        payload: dict = {
            "model": model or self._default_model or "",
            "messages": raw_messages,
            "temperature": temperature if temperature is not None else self._default_temperature,
            "max_tokens": max_tokens if max_tokens is not None else self._default_max_tokens,
            "stream": stream,
        }
        return payload

    async def _chat_sync(self, payload: dict) -> ChatResponse:
        """非流式 chat"""
        try:
            response = await self._client.post(
                "/chat/completions",
                json=payload,
            )
        except httpx.ConnectError as e:
            raise ConnectionError(f"无法连接到模型服务: {e}") from e
        except httpx.TimeoutException as e:
            raise TimeoutError(f"模型请求超时: {e}") from e
        except httpx.HTTPError as e:
            raise ModelClientError(f"HTTP 请求失败: {e}") from e

        if response.status_code != 200:
            await self._raise_on_error(response)

        data = response.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})

        return ChatResponse(
            content=choice["message"]["content"] or "",
            model=data.get("model", payload.get("model", "")),
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            finish_reason=choice.get("finish_reason", "stop"),
        )

    async def _chat_stream(self, payload: dict) -> AsyncIterator[ChatStreamEvent]:
        """流式 chat"""
        payload["stream"] = True
        try:
            async with self._client.stream("POST", "/chat/completions", json=payload) as response:
                if response.status_code != 200:
                    body = await response.aread()
                    await self._raise_on_error(response, body)
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    if line.startswith("data: "):
                        raw = line[6:].strip()
                        if raw == "[DONE]":
                            yield ChatStreamEvent(finish_reason="stop")
                            return
                        try:
                            chunk = json.loads(raw)
                        except json.JSONDecodeError:
                            continue
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        finish = chunk.get("choices", [{}])[0].get("finish_reason")
                        event = ChatStreamEvent(text=content, finish_reason=finish)
                        yield event
                        if finish:
                            return
        except httpx.ConnectError as e:
            raise ConnectionError(f"流式连接失败: {e}") from e
        except httpx.TimeoutException as e:
            raise TimeoutError(f"流式请求超时: {e}") from e

    # ─── Complete ───────────────────────────────────────────

    async def complete(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False,
    ) -> CompleteResponse | AsyncIterator[ChatStreamEvent]:
        """文本补全"""
        payload = self._build_complete_payload(prompt, model, temperature, max_tokens, stream)

        if stream:
            return self._complete_stream(payload)

        return await self._complete_sync(payload)

    def _build_complete_payload(
        self,
        prompt: str,
        model: str | None,
        temperature: float | None,
        max_tokens: int | None,
        stream: bool,
    ) -> dict:
        """构建 complete 请求 payload"""
        return {
            "model": model or self._default_model or "",
            "prompt": prompt,
            "temperature": temperature if temperature is not None else self._default_temperature,
            "max_tokens": max_tokens if max_tokens is not None else self._default_max_tokens,
            "stream": stream,
        }

    async def _complete_sync(self, payload: dict) -> CompleteResponse:
        """非流式 complete"""
        try:
            response = await self._client.post("/completions", json=payload)
        except httpx.ConnectError as e:
            raise ConnectionError(f"无法连接到模型服务: {e}") from e
        except httpx.TimeoutException as e:
            raise TimeoutError(f"模型请求超时: {e}") from e
        except httpx.HTTPError as e:
            raise ModelClientError(f"HTTP 请求失败: {e}") from e

        if response.status_code != 200:
            await self._raise_on_error(response)

        data = response.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})

        return CompleteResponse(
            content=choice.get("text", ""),
            model=data.get("model", payload.get("model", "")),
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            finish_reason=choice.get("finish_reason", "stop"),
        )

    async def _complete_stream(self, payload: dict) -> AsyncIterator[ChatStreamEvent]:
        """流式 complete"""
        payload["stream"] = True
        try:
            async with self._client.stream("POST", "/completions", json=payload) as response:
                if response.status_code != 200:
                    body = await response.aread()
                    await self._raise_on_error(response, body)
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    if line.startswith("data: "):
                        raw = line[6:].strip()
                        if raw == "[DONE]":
                            yield ChatStreamEvent(finish_reason="stop")
                            return
                        try:
                            chunk = json.loads(raw)
                        except json.JSONDecodeError:
                            continue
                        choices = chunk.get("choices", [{}])
                        text = choices[0].get("text", "") if choices else ""
                        finish = choices[0].get("finish_reason") if choices else None
                        yield ChatStreamEvent(text=text, finish_reason=finish)
                        if finish:
                            return
        except httpx.ConnectError as e:
            raise ConnectionError(f"流式连接失败: {e}") from e
        except httpx.TimeoutException as e:
            raise TimeoutError(f"流式请求超时: {e}") from e

    # ─── Health / Models ───────────────────────────────────

    async def health_check(self) -> bool:
        """检查服务是否可用"""
        try:
            response = await self._client.get("/models", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        """列出可用模型"""
        try:
            response = await self._client.get("/models")
            if response.status_code == 200:
                data = response.json()
                return [m["id"] for m in data.get("data", [])]
            return []
        except Exception as e:
            logger.warning("Failed to list models: %s", e)
            return []

    # ─── Cleanup ────────────────────────────────────────────

    async def close(self):
        """关闭 HTTP 连接"""
        await self._client.aclose()

    # ─── 内部方法 ──────────────────────────────────────────

    async def _raise_on_error(self, response: httpx.Response, body: bytes | None = None) -> None:
        """根据状态码抛出特定异常"""
        status = response.status_code
        body_text = (body or response.content).decode("utf-8", errors="replace")[:500]

        error_cls = ERROR_CODE_MAP.get(status, ModelClientError)
        raise error_cls(
            message=f"模型 API 返回错误 ({status}): {body_text}",
            status_code=status,
            response_body=body_text,
        )
