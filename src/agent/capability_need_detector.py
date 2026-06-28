"""Capability Need Detector — detects if user is asking about project capabilities."""

from __future__ import annotations

from dataclasses import dataclass

_CAPABILITY_KEYWORDS = [
    "支持", "可以", "能不能", "有没有", "是否已经实现", "是否支持",
    "当前版本", "最新版本", "版本", "现在",
    "联网", "web", "webui", "web ui",
    "pdf", "docx", "embedding", "vector", "crawler", "爬虫",
    "lora", "fine-tuning", "微调",
    "deep mode", "14b", "十四b", "32b", "三十二b",
    "web ask", "web ingest", "web search", "web fetch",
    "source archive", "daemon", "tray",
    "默认模型", "必须下载", "强制",
    "does", "support", "is.*implemented",
    "what.*version", "which model",
]


@dataclass
class CapabilityNeedResult:
    is_capability_question: bool = False
    confidence: float = 0.0
    matched_keywords: list[str] = None

    def __post_init__(self):
        if self.matched_keywords is None:
            self.matched_keywords = []


class CapabilityNeedDetector:
    """Detects whether a user message is asking about project capabilities.

    Returns a CapabilityNeedResult with confidence and matched keywords.
    """

    def detect(self, user_message: str) -> CapabilityNeedResult:
        msg_lower = user_message.lower().strip()
        matched = [kw for kw in _CAPABILITY_KEYWORDS if kw in msg_lower]

        if not matched:
            return CapabilityNeedResult(is_capability_question=False)

        confidence = min(0.5 + 0.1 * len(matched), 1.0)

        # Short messages with capability keywords are almost certainly capability questions
        if len(user_message) <= 30 and matched:
            confidence = max(confidence, 0.9)

        return CapabilityNeedResult(
            is_capability_question=True,
            confidence=confidence,
            matched_keywords=matched,
        )
