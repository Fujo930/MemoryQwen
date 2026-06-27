"""Judge v3 Tests (≥18)"""
import pytest
from src.eval_runner.models import EvalQuestion, EvalAnswer, EvalJudgement
from src.eval_runner.judge import judge_v3


def _judge(expected, answer, topic="capability_boundary"):
    q = EvalQuestion(question_id="Q001", topic=topic, question="test",
                     expected_answer=expected)
    a = EvalAnswer(question_id="Q001", answer=answer)
    return judge_v3(q, a)


class TestCautiousAsCorrect:
    def test_no_webui_cautious(self):
        j = _judge("没有 Web UI", "不能确定 v0.1 有 Web UI，应以当前 CLI 为准")
        assert j.correctness == "correct_candidate"

    def test_no_pdf_cautious(self):
        j = _judge("v0.1 不支持 PDF", "当前资料显示只支持 txt md，PDF 不能确定为已实现")
        assert j.correctness == "correct_candidate"

    def test_no_internet_cautious(self):
        j = _judge("v0.1 不支持 Internet Query", "当前资料不足以确认已实现联网，不能把未来计划说成当前能力")
        assert j.correctness == "correct_candidate"

    def test_future_plan_cautious(self):
        j = _judge("rebuild from sources 是未来计划", "不能确定当前已有 rebuild 命令，建议查看 CLI")
        assert j.correctness in ("correct_candidate", "partial_candidate")

    def test_uncertain_expected_with_cautious_answer(self):
        j = _judge("不能确定 未实现", "根据当前本地资料不能确定")
        assert j.correctness == "correct_candidate"

    def test_english_cautious(self):
        j = _judge("No, v0.1 does not support embedding", "I cannot confirm this from the current sources")
        assert j.correctness in ("correct_candidate", "partial_candidate")


class TestOverclaimStillWrong:
    def test_webui_with_overclaim(self):
        j = _judge("没有 Web UI", "不能确定，但 v0.1 应该已经有 Web UI 了")
        assert j.correctness == "wrong"

    def test_fake_cli(self):
        j = _judge("没有 cli webui", "不能确定，但可以用 cli webui 启动")
        assert j.correctness == "wrong"

    def test_archive_is_crawler(self):
        j = _judge("source archive 不是 crawler", "不能确定，但 source archive 会自动抓网页")
        assert j.correctness == "wrong"

    def test_32b_recommended(self):
        j = _judge("不推荐 32B", "不能确定，但 32B 是默认推荐模型")
        assert j.correctness == "wrong"

    def test_wrong_answer_as_fact(self):
        j = _judge("wrong_answer 是反例", "不能确定，但 wrong_answer 可以作为事实参考")
        assert j.correctness == "wrong"


class TestDefinitiveFactsNotUncertain:
    def test_txt_md_supported(self):
        j = _judge("v0.1 支持 .txt .md", "不能确定", topic="capability_boundary")
        assert j.correctness in ("partial_candidate", "wrong")

    def test_7b_default(self):
        j = _judge("7B 是默认推荐", "不能确定", topic="model_hardware")
        assert j.correctness in ("partial_candidate", "wrong")

    def test_sources_is_archive(self):
        j = _judge("memory/sources 是原文归档", "不能确定", topic="source_archive")
        assert j.correctness in ("partial_candidate", "wrong")


class TestRealFalseNegatives:
    def test_m2_embedding_cautious(self):
        # Real M2 case: model said "不能确定" about embedding
        j = _judge("不支持 embedding", "根据当前本地资料不能确定。使用 BM25 检索。", topic="capability_boundary")
        assert j.correctness != "wrong"

    def test_m2_source_archive_cautious(self):
        # Real M2 case: model said "不能确定" about archive vs crawler
        j = _judge("source archive 不是 crawler", "根据当前本地资料不能确定。source archive 与 crawler 是不同的概念", topic="source_archive")
        assert j.correctness != "wrong"

    def test_m2_kill_process_cautious(self):
        # Real M2 case: model said "不能确定" about kill process
        j = _judge("v0.1 不会 kill 进程", "不能确定。GPU Guardian 只做检测，但未明确说明是否会kill进程", topic="capability_boundary")
        assert j.correctness != "wrong"


class TestMetadata:
    def test_cautious_metadata(self):
        j = _judge("没有 Web UI", "不能确定 v0.1 有 Web UI")
        meta = j.metadata or {}
        assert meta.get("cautious_uncertainty_detected") is True
        assert meta.get("overclaim_detected") is False

    def test_overclaim_metadata(self):
        j = _judge("没有 Web UI", "不能确定，但 v0.1 已经有 Web UI")
        meta = j.metadata or {}
        assert meta.get("overclaim_detected") is True
