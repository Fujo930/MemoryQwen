"""
AutoModelAdapter 测试
"""

import pytest
from src.model_adapter.models import EvalCase, EvalCaseResult, EvalReport
from src.model_adapter.eval_cases import BASIC_EVAL_CASES
from src.model_adapter.auto_adapter import AutoModelAdapter
from src.model_client.base import ChatResponse
from src.model_profile.models import ModelProfile


class FakeModelClient:
    """响应内容可配置的 fake client"""
    def __init__(self, responses: dict[str, str] | None = None):
        self.responses = responses or {}
        self.calls: list[dict] = []

    async def chat(self, messages, model=None, temperature=None, max_tokens=None, stream=False):
        self.calls.append({"messages": messages, "temperature": temperature, "max_tokens": max_tokens})
        # 根据 case_id 返回预设或默认
        for case_id, resp in self.responses.items():
            # 简单匹配 case_id
            if case_id in self.calls[-1].get("messages", [{}])[0].get("content", ""):
                return ChatResponse(content=resp, model="fake", usage={"total_tokens": 10})
            if case_id in str(self.calls[-1].get("messages", [])):
                return ChatResponse(content=resp, model="fake", usage={"total_tokens": 10})
        # default
        return ChatResponse(content="OK", model="fake", usage={"total_tokens": 5})


class FailingModelClient:
    async def chat(self, *args, **kwargs):
        raise RuntimeError("模型不可用")


class TestAutoAdapter:
    @pytest.mark.asyncio
    async def test_full_basic_eval(self):
        """6 个 cases 全部完成"""
        client = FakeModelClient()
        adapter = AutoModelAdapter(client)
        report = await adapter.run_basic_eval("test-model")
        assert report.model_id == "test-model"
        assert len(report.results) == 6
        assert all(isinstance(r, EvalCaseResult) for r in report.results)
        # 至少所有 cases 都有结果
        assert all(r.case_id for r in report.results)

    @pytest.mark.asyncio
    async def test_case_failure_non_fatal(self):
        """某个 case 抛异常不影响整体"""
        client = FailingModelClient()
        adapter = AutoModelAdapter(client)
        report = await adapter.run_basic_eval("test-model")
        # 所有 cases 都有结果（score=0, passed=False, 有 reason）
        assert len(report.results) == 6
        for r in report.results:
            assert r.passed is False
            assert r.score == 0.0
            assert r.reason is not None
            assert "RuntimeError" in r.reason

    @pytest.mark.asyncio
    async def test_build_profile_from_report(self):
        client = FakeModelClient()
        adapter = AutoModelAdapter(client)
        report = await adapter.run_basic_eval("test-model")
        profile = adapter.build_profile_from_report(report)
        assert isinstance(profile, ModelProfile)
        assert profile.model_id == "test-model"
        assert profile.roles is not None

    @pytest.mark.asyncio
    async def test_recommended_roles(self):
        client = FakeModelClient()
        adapter = AutoModelAdapter(client)
        report = await adapter.run_basic_eval("test-model")
        assert "main_chat" in report.recommended_roles

    @pytest.mark.asyncio
    async def test_preferred_format(self):
        client = FakeModelClient()
        adapter = AutoModelAdapter(client)
        report = await adapter.run_basic_eval("test-model")
        assert report.preferred_format in ("json", "plain")

    @pytest.mark.asyncio
    async def test_role_reasons(self):
        client = FakeModelClient()
        adapter = AutoModelAdapter(client)
        report = await adapter.run_basic_eval("test-model")
        assert "role_reasons" in report.metadata
        assert "main_chat" in report.metadata["role_reasons"]

    @pytest.mark.asyncio
    async def test_eval_case_temperature(self):
        client = FakeModelClient()
        adapter = AutoModelAdapter(client)
        await adapter.run_basic_eval("t")
        # 确认至少有一个调用用了 temperature=0.1 (JSON case)
        temps = [c.get("temperature") for c in client.calls]
        assert 0.1 in temps

    @pytest.mark.asyncio
    async def test_exception_reason(self):
        client = FailingModelClient()
        adapter = AutoModelAdapter(client)
        report = await adapter.run_basic_eval("t")
        failing = [r for r in report.results if r.reason]
        assert len(failing) > 0
        assert "RuntimeError" in failing[0].reason


class TestModels:
    def test_eval_case_model(self):
        case = EvalCase(case_id="test", category="test", messages=[])
        assert case.temperature == 0.1
        assert case.max_tokens == 256

    def test_eval_report_model(self):
        report = EvalReport(model_id="m", capability_scores={"a": 0.5})
        assert report.model_id == "m"
        assert report.capability_scores["a"] == 0.5


class TestEvalCases:
    def test_all_cases_valid(self):
        for case in BASIC_EVAL_CASES:
            assert case.case_id
            assert case.category
            assert len(case.messages) > 0
            assert 0 <= case.temperature <= 1
            assert case.max_tokens > 0
