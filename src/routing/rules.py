"""MemoryQwen — TDR-v1 routing rules."""

from __future__ import annotations

# ── Route priority order (highest first) ──────────────────
ROUTE_PRIORITY = [
    "manual_review",
    "judge_review",
    "capability_registry",
    "web",
    "deep_suggested",
    "memory",
    "shallow",
]

# ── Capability-registry trigger tokens ────────────────────
CAPABILITY_TOKENS: list[str] = [
    "支持", "能不能", "可以吗", "有没有", "是否已经实现",
    "当前版本", "联网", "web ask", "web ingest", "Web UI",
    "PDF", "DOCX", "embedding", "vector", "crawler", "爬虫",
    "默认模型", "必须下载", "14B", "deep mode",
    "internet query", "web search", "web fetch",
    "loRA", "微调", "daemon", "tray", "托盘",
]

# ── Web-need trigger tokens ───────────────────────────────
WEB_TOKENS: list[str] = [
    "最新", "现在", "查一下", "搜索", "新闻", "官网",
    "当前外部版本", "release", "news", "latest",
    "trending", "weather", "price", "stock",
]

# ── Deep-suggested trigger tokens ─────────────────────────
DEEP_TOKENS: list[str] = [
    "规划", "架构", "算法", "外骨骼", "路线", "发布决策",
    "版本冲突", "新旧资料冲突", "多来源冲突", "权衡", "设计",
    "token", "routing", "分层", "推理", "ace", "tdr",
    "debug", "复杂", "难点",
]

# ── Judge-review trigger tokens ───────────────────────────
JUDGE_TOKENS: list[str] = [
    "fake CLI", "不存在的命令", "wrong_answer", "错误答案",
    "当事实", "自动写入", "绕过 guard",
    "绕过", "编造", "幻觉",
]

# ── Manual-review trigger conditions ──────────────────────
MANUAL_TOKENS: list[str] = [
    "网页说", "资料说", "但是 Registry", "到底有没有",
    "冲突", "不一致", "矛盾",
]
