"""Smart Retrieval Gate Tests (≥26)"""
import pytest
from src.agent.retrieval_gate import RetrievalGate, RetrievalDecision


GATE = RetrievalGate()


class TestCasualSkip:
    def test_hello_skips(self):
        d = GATE.decide("你好")
        assert d.should_retrieve is False
        assert d.store_types == []
        assert d.skipped_retrieval is True

    def test_hi_skips(self):
        d = GATE.decide("hi")
        assert d.should_retrieve is False

    def test_thanks_skips(self):
        d = GATE.decide("谢谢")
        assert d.should_retrieve is False

    def test_ok_skips(self):
        d = GATE.decide("好的")
        assert d.should_retrieve is False

    def test_continue_short_casual_may_skip(self):
        d = GATE.decide("继续")
        assert d.should_retrieve is False

    def test_bye_skips(self):
        d = GATE.decide("拜拜")
        assert d.should_retrieve is False

    def test_short_question_retrieves(self):
        """Short but with question mark should retrieve"""
        d = GATE.decide("吗？")
        assert d.should_retrieve is True  # has "吗" question marker


class TestExplicitNoMemory:
    def test_no_memory_skips(self):
        d = GATE.decide("不用查资料，直接回答")
        assert d.should_retrieve is False
        assert d.reason == "explicit_no_memory"

    def test_skip_retrieval_skips(self):
        d = GATE.decide("不要查 memory")
        assert d.should_retrieve is False


class TestProjectTerms:
    def test_memoryqwen_retrieves(self):
        d = GATE.decide("MemoryQwen 有哪些功能？")
        assert d.should_retrieve is True
        assert "knowledge_store" in d.store_types

    def test_issue_retrieves(self):
        d = GATE.decide("Issue #23 做了什么？")
        assert d.should_retrieve is True

    def test_source_archive_retrieves(self):
        d = GATE.decide("source archive 是什么？")
        assert d.should_retrieve is True

    def test_memoryqwen_db_retrieves(self):
        d = GATE.decide("memoryqwen.db 保存什么？")
        assert d.should_retrieve is True

    def test_tasks_db_retrieves(self):
        d = GATE.decide("tasks.db 保存什么？")
        assert d.should_retrieve is True


class TestHighRisk:
    def test_pdf_high_risk_all(self):
        d = GATE.decide("支持 PDF 吗？")
        assert d.should_retrieve is True
        assert d.risk_level == "high"
        assert all(s in d.store_types for s in ["knowledge_store", "error_store", "strategy_store"])

    def test_webui_high_risk_all(self):
        d = GATE.decide("有没有 Web UI？")
        assert d.risk_level == "high"

    def test_fake_cli_high_risk_all(self):
        d = GATE.decide("cli webui 怎么用？")
        assert d.risk_level == "high"

    def test_crawler_high_risk(self):
        d = GATE.decide("是不是有 crawler 功能？")
        assert d.risk_level == "high"

    def test_lora_high_risk(self):
        d = GATE.decide("MemoryQwen 支持 LoRA 微调吗？")
        assert d.risk_level == "high"


class TestErrorStrategy:
    def test_wrong_answer_retrieves_error_strategy(self):
        d = GATE.decide("wrong_answer 怎么处理？")
        assert d.should_retrieve is True
        assert "error_store" in d.store_types
        assert "strategy_store" in d.store_types

    def test_strategy_retrieves_strategy(self):
        d = GATE.decide("有什么策略？")
        assert d.should_retrieve is True
        assert "strategy_store" in d.store_types

    def test_failure_type_retrieves_error_strategy(self):
        d = GATE.decide("failure_type 有哪些？")
        assert d.should_retrieve is True


class TestModelHardware:
    def test_3b_retrieves(self):
        d = GATE.decide("3B 够用吗？")
        assert d.should_retrieve is True
        assert "knowledge_store" in d.store_types

    def test_7b_retrieves(self):
        d = GATE.decide("7B 和 14B 选哪个？")
        assert d.should_retrieve is True

    def test_rtx_retrieves(self):
        d = GATE.decide("RTX 4080 用什么模型？")
        assert d.should_retrieve is True


class TestDefaultBehavior:
    def test_unknown_question_defaults_retrieve(self):
        d = GATE.decide("这是什么系统？")
        assert d.should_retrieve is True
        assert d.reason == "low_confidence_default_retrieve"


class TestGateDisabled:
    def test_disabled_gate_always_retrieves(self):
        g = RetrievalGate()
        g.enabled = False
        d = g.decide("你好")
        assert d.should_retrieve is True


class TestStoreDedup:
    def test_stores_not_duplicated(self):
        d = GATE.decide("wrong_answer 和 memoryqwen 的关系")
        assert len(d.store_types) == len(set(d.store_types))  # no duplicates


class TestTopKCapped:
    def test_top_k_cannot_exceed_max(self):
        g = RetrievalGate()
        g.max_top_k = 3
        d = g.decide("支持 PDF 吗？")
        assert d.top_k <= 3
