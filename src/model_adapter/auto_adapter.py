"""
MemoryQwen — AutoModelAdapter
自动评估模型能力并生成 ModelProfile。
"""

from __future__ import annotations

import logging
from typing import Any

from src.model_adapter.models import EvalCase, EvalCaseResult, EvalReport
from src.model_adapter.eval_cases import BASIC_EVAL_CASES
from src.model_adapter.scorers import (
    score_json_validity,
    score_chinese_response,
    score_citation_format,
    score_tool_call_json,
    score_simple_reasoning,
    score_context_recall,
)
from src.model_profile.models import ModelProfile, Capabilities, Limits, Protocol, Runtime, Roles

logger = logging.getLogger(__name__)

SCORER_MAP: dict[str, callable] = {
    "json_stability": score_json_validity,
    "chinese": score_chinese_response,
    "tool_call_json": score_tool_call_json,
    "citation_format": score_citation_format,
    "simple_reasoning": score_simple_reasoning,
    "context_recall": score_context_recall,
}


class AutoModelAdapter:
    """自动模型适配器"""

    def __init__(self, model_client):
        self.model_client = model_client

    async def run_basic_eval(self, model_id: str, cases: list[EvalCase] | None = None) -> EvalReport:
        """运行基础评估"""
        cases = cases or BASIC_EVAL_CASES
        results: list[EvalCaseResult] = []

        for case in cases:
            result = await self._eval_single(case)
            results.append(result)

        # 计算 capability scores
        capability_scores = self._compute_capabilities(results)

        # 推荐 roles
        recommended_roles = self._recommend_roles(capability_scores)

        # 推荐 preferred_format
        preferred_format = self._recommend_format(results)

        # role_reasons
        role_reasons = self._build_role_reasons(capability_scores)

        return EvalReport(
            model_id=model_id,
            results=results,
            capability_scores=capability_scores,
            recommended_roles=recommended_roles,
            preferred_format=preferred_format,
            metadata={"role_reasons": role_reasons},
        )

    async def _eval_single(self, case: EvalCase) -> EvalCaseResult:
        """执行单个评估用例"""
        result = EvalCaseResult(case_id=case.case_id, category=case.category)
        try:
            response = await self.model_client.chat(
                messages=case.messages,
                temperature=case.temperature,
                max_tokens=case.max_tokens,
            )
            result.raw_output = response.content

            # 选择对应 scorer
            scorer = None
            if case.case_id == "tool_call_json":
                scorer = SCORER_MAP.get("tool_call_json")
            elif case.case_id == "citation_format":
                scorer = SCORER_MAP.get("citation_format")
            elif case.case_id == "simple_reasoning":
                scorer = SCORER_MAP.get("simple_reasoning")
            elif case.case_id == "context_recall":
                scorer = SCORER_MAP.get("context_recall")
            else:
                scorer = SCORER_MAP.get(case.category)

            if scorer:
                result.score = scorer(result.raw_output)
            else:
                result.score = 0.5

            result.passed = result.score >= 0.5

        except Exception as e:
            result.passed = False
            result.score = 0.0
            result.reason = f"{type(e).__name__}: {e}"
            result.raw_output = ""
            logger.warning("Eval case %s failed: %s", case.case_id, e)

        return result

    def build_profile_from_report(self, report: EvalReport) -> ModelProfile:
        """从评估报告生成 ModelProfile"""
        caps = Capabilities(
            json_stability=report.capability_scores.get("json_stability", 0.5),
            tool_calling=report.capability_scores.get("tool_calling", 0.5),
            chinese=report.capability_scores.get("chinese", 0.5),
            reasoning=report.capability_scores.get("reasoning", 0.5),
            long_context=report.capability_scores.get("long_context", 0.5),
            coding=report.capability_scores.get("coding", 0.5),
        )
        fmt = report.preferred_format
        return ModelProfile(
            model_id=report.model_id,
            family=None,
            size_b=None,
            backend="openai_compatible",
            capabilities=caps,
            limits=Limits(),
            protocol=Protocol(preferred_format=fmt),
            runtime=Runtime(),
            roles=Roles(suitable_for=report.recommended_roles),
        )

    def save_profile(self, profile: ModelProfile, path: str):
        """保存 profile 到文件"""
        from src.model_profile.loader import save_profile
        save_profile(profile, path)

    # ─── 内部 ─────────────────────────────────────────

    def _compute_capabilities(self, results: list[EvalCaseResult]) -> dict[str, float]:
        """从评估结果计算能力分数"""
        scores: dict[str, list[float]] = {}

        for r in results:
            cat = r.category
            if cat not in scores:
                scores[cat] = []
            scores[cat].append(r.score)

        caps = {}
        # json_stability = avg(json_stability + tool_call_json)
        json_vals = scores.get("json_stability", [])
        tool_vals = scores.get("tool_calling", [])
        caps["json_stability"] = self._safe_avg(json_vals + tool_vals)
        # tool_calling = tool_call_json * 0.7 + citation * 0.3
        tool_tcj = self._safe_avg([r.score for r in results if r.case_id == "tool_call_json"])
        tool_cit = self._safe_avg([r.score for r in results if r.case_id == "citation_format"])
        caps["tool_calling"] = round(tool_tcj * 0.7 + tool_cit * 0.3, 2)
        caps["chinese"] = self._safe_avg(scores.get("chinese", []))
        caps["reasoning"] = self._safe_avg(scores.get("reasoning", []))
        caps["long_context"] = self._safe_avg(scores.get("long_context", []))
        caps["coding"] = 0.5  # placeholder

        return caps

    def _recommend_roles(self, caps: dict[str, float]) -> list[str]:
        """根据能力分数推荐角色"""
        roles = ["main_chat"]  # always

        if caps.get("reasoning", 0) >= 0.7:
            roles.append("reasoner")
        if caps.get("json_stability", 0) >= 0.7 and caps.get("tool_calling", 0) >= 0.6:
            roles.append("router")
        if caps.get("long_context", 0) >= 0.6:
            roles.append("summarizer")
        if caps.get("coding", 0) >= 0.7:
            roles.append("coder")
        # low_vram_mode: if size unknown or small
        roles.append("low_vram_mode")

        return roles

    def _recommend_format(self, results: list[EvalCaseResult]) -> str:
        """推荐 preferred_format"""
        tool_result = next((r for r in results if r.case_id == "tool_call_json"), None)
        if tool_result and tool_result.score >= 0.7:
            return "json"
        return "plain"

    def _build_role_reasons(self, caps: dict[str, float]) -> dict[str, str]:
        reasons = {"main_chat": "default"}
        if caps.get("reasoning", 0) >= 0.7:
            reasons["reasoner"] = "reasoning>=0.7"
        if caps.get("json_stability", 0) >= 0.7 and caps.get("tool_calling", 0) >= 0.6:
            reasons["router"] = "json_stability>=0.7 and tool_calling>=0.6"
        if caps.get("long_context", 0) >= 0.6:
            reasons["summarizer"] = "long_context>=0.6"
        reasons["low_vram_mode"] = "default"
        return reasons

    @staticmethod
    def _safe_avg(vals: list[float]) -> float:
        if not vals:
            return 0.0
        return round(sum(vals) / len(vals), 2)
