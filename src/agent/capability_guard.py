"""
MemoryQwen — CapabilityBoundaryGuard
检测用户问题是否涉及 v0.1 能力边界，如果是则注入强制规则。
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CapabilityGuardResult:
    is_capability_question: bool = False
    matched_terms: list[str] = field(default_factory=list)
    risk_level: str = "low"     # "high" | "medium" | "low"
    forced_instructions: list[str] = field(default_factory=list)


# ─── 关键词定义 ─────────────────────────────────────────

HIGH_RISK_TERMS_ZH = [
    "PDF", "DOCX", "Web UI", "GUI", "daemon", "tray", "托盘",
    "embedding", "向量", "vector", "crawler", "爬虫",
    "LoRA", "微调", "模型权重", "自动卸载", "kill", "进程", "FastAPI",
]
HIGH_RISK_TERMS_EN = [
    "pdf", "docx", "web ui", "gui", "daemon", "tray",
    "embedding", "vector", "crawler",
    "lora", "finetune", "fine-tune", "model weights", "auto unload",
    "kill process", "fastapi",
]

MEDIUM_RISK_TERMS_ZH = [
    "支持", "能不能", "有没有", "是否", "当前", "现在",
    "v0.1", "已实现", "未实现", "未来计划",
]
MEDIUM_RISK_TERMS_EN = [
    "support", "current", "implemented", "not implemented", "roadmap",
]

FORCED_INSTRUCTIONS = [
    "只根据本地资料、能力边界资料和已注入 sources 回答。",
    "如果功能在\"未实现\"列表中，必须明确说\"v0.1 尚未实现\"。",
    "不能把未来计划说成当前能力。",
    "不能把 CLI 说成 Web UI。",
    "不能把 GPU Guardian status detection 说成 daemon/tray/自动卸载。",
    "不能把 .md/.txt ingestion 说成 PDF/DOCX ingestion。",
    "不能把 source archive 说成 crawler。",
    "不能把 AutoModelAdapter 说成 LoRA 或模型微调。",
    "不能编造不存在的 CLI 命令，例如 cli webui。",
    "如果资料不足，必须回答\"根据当前本地资料不能确定\"。",
]


class CapabilityBoundaryGuard:
    """能力边界问题检测器"""

    def detect(self, user_message: str) -> CapabilityGuardResult:
        msg = user_message.lower()
        result = CapabilityGuardResult()

        # 收集命中的高风险词
        high_hits = []
        for term in HIGH_RISK_TERMS_ZH:
            if term.lower() in msg:
                high_hits.append(term)
        for term in HIGH_RISK_TERMS_EN:
            if term in msg:
                high_hits.append(term)

        # 收集命中的中风险词
        medium_hits = []
        for term in MEDIUM_RISK_TERMS_ZH:
            if term.lower() in msg:
                medium_hits.append(term)
        for term in MEDIUM_RISK_TERMS_EN:
            if term in msg:
                medium_hits.append(term)

        # 判断
        if high_hits:
            result.is_capability_question = True
            result.risk_level = "high"
            result.matched_terms = list(set(high_hits))
            result.forced_instructions = list(FORCED_INSTRUCTIONS)
        elif medium_hits:
            result.is_capability_question = True
            result.risk_level = "medium"
            result.matched_terms = list(set(medium_hits))
            result.forced_instructions = list(FORCED_INSTRUCTIONS)
        else:
            result.risk_level = "low"

        return result
