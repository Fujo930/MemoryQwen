"""
MemoryQwen — Eval Scorers
每个 scorer 接收模型原始输出字符串，返回 0-1 分数。
"""

from __future__ import annotations

import json
import re


def _extract_json(text: str) -> dict | None:
    """从文本中提取 JSON：直接解析 → 代码块 → 首个 {...}"""
    # 1. 直接解析
    try:
        return json.loads(text.strip())
    except (json.JSONDecodeError, ValueError):
        pass

    # 2. 提取 ```json ... ``` 代码块
    m = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', text)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except (json.JSONDecodeError, ValueError):
            pass

    # 3. 提取首个 {...} 对象
    m = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
    if m:
        try:
            return json.loads(m.group(0))
        except (json.JSONDecodeError, ValueError):
            pass

    return None


def score_json_validity(output: str) -> float:
    """验证 JSON 合法性"""
    obj = _extract_json(output)
    if obj and "answer" in obj:
        return 1.0
    if obj:
        return 0.5  # JSON 有效但缺少关键字段
    return 0.0


def score_chinese_response(output: str) -> float:
    """验证中文回答能力"""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', output))
    if len(output) < 20:
        return chinese_chars / max(len(output), 1) * 0.5
    ratio = chinese_chars / max(len(output), 1)
    return min(1.0, ratio * 1.5)


def score_citation_format(output: str) -> float:
    """验证是否包含 [S1] 或 [S2] 引用"""
    if re.search(r'\[S\d\]', output):
        return 1.0
    return 0.0


def score_tool_call_json(output: str) -> float:
    """验证工具调用 JSON 格式"""
    obj = _extract_json(output)
    if not obj:
        return 0.0
    score = 0.0
    if "tool" in obj:
        score += 0.3
    if "arguments" in obj and isinstance(obj["arguments"], dict):
        score += 0.3
        if "query" in obj["arguments"]:
            score += 0.4
    return score


def score_simple_reasoning(output: str) -> float:
    """验证简单推理：答案应该是 4，且不包含否定短语"""
    clean = output.strip().lower()

    # 检测否定模式
    negate_patterns = [
        r'(?:不是|不等于|不对|并非).*?4',
        r'4.*(?:不是|不对|不正确)',
        r'not\s+4',
        r"isn['\u2019]t\s+4",
        r'answer.*?not.*?4',
    ]
    for pat in negate_patterns:
        if re.search(pat, clean):
            return 0.0

    # 检测包含 4
    if re.search(r'(?:^|\s)4(?:[\s.,!?$]|$)', clean):
        return 1.0
    if "four" in clean:
        return 1.0

    # 检测 "四个" / "4个"
    if re.search(r'[四4]\s*个', clean):
        return 1.0

    return 0.0


def score_context_recall(output: str) -> float:
    """验证上下文保持：是否包含 BLUE-RABBIT"""
    if "BLUE-RABBIT" in output:
        return 1.0
    if "blue-rabbit" in output.lower():
        return 0.5
    return 0.0
