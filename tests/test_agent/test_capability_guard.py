"""
Capability Boundary Guard 测试 (≥22)
"""

import pytest
from src.agent.capability_guard import CapabilityBoundaryGuard, CapabilityGuardResult
from src.agent.prompt_builder import PromptBuilder


# ─── Guard Tests ──────────────────────────────────────

GUARD = CapabilityBoundaryGuard()


class TestDetectHighRisk:
    def test_detects_pdf(self):
        r = GUARD.detect("MemoryQwen v0.1 支持 PDF ingestion 吗？")
        assert r.is_capability_question
        assert r.risk_level == "high"
        assert any("PDF" in t for t in r.matched_terms)

    def test_detects_web_ui(self):
        r = GUARD.detect("MemoryQwen 有没有 Web UI？")
        assert r.is_capability_question
        assert r.risk_level == "high"

    def test_detects_daemon(self):
        r = GUARD.detect("GPU Guardian 是 daemon 吗？")
        assert r.is_capability_question
        assert r.risk_level == "high"

    def test_detects_embedding(self):
        r = GUARD.detect("MemoryQwen 支持 embedding 向量检索吗？")
        assert r.is_capability_question
        assert r.risk_level == "high"

    def test_detects_lora(self):
        r = GUARD.detect("AutoModelAdapter 是不是 LoRA？")
        assert r.is_capability_question
        assert r.risk_level == "high"

    def test_detects_finetune(self):
        r = GUARD.detect("MemoryQwen 会不会微调模型？")
        assert r.is_capability_question
        assert r.risk_level == "high"

    def test_detects_crawler(self):
        r = GUARD.detect("source archive 是不是全站 crawler？")
        assert r.is_capability_question
        assert r.risk_level == "high"

    def test_detects_fastapi(self):
        r = GUARD.detect("FastAPI server 是现在功能还是未来计划？")
        assert r.is_capability_question
        assert r.risk_level == "high"

    def test_detects_tray(self):
        r = GUARD.detect("MemoryQwen 有没有托盘？")
        assert r.is_capability_question
        assert r.risk_level == "high"


class TestDetectMediumRisk:
    def test_detects_support_question(self):
        r = GUARD.detect("MemoryQwen 支持什么功能？")
        assert r.is_capability_question
        assert r.risk_level == "medium"

    def test_detects_current_question(self):
        r = GUARD.detect("当前 v0.1 实现了哪些？")
        assert r.is_capability_question
        assert r.risk_level == "medium"


class TestIgnoresGeneral:
    def test_ignores_general_chat(self):
        r = GUARD.detect("你好，今天天气不错")
        assert not r.is_capability_question
        assert r.risk_level == "low"

    def test_ignores_simple_fact(self):
        r = GUARD.detect("MemoryQwen 的核心记忆有哪些？")
        assert not r.is_capability_question


class TestForcedInstructions:
    def test_has_no_pdf_rule(self):
        r = GUARD.detect("支持 PDF 吗？")
        assert any("PDF" in i for i in r.forced_instructions)

    def test_has_no_webui_rule(self):
        r = GUARD.detect("有 Web UI 吗？")
        assert any("Web UI" in i for i in r.forced_instructions)

    def test_has_no_cli_webui_rule(self):
        r = GUARD.detect("有 Web UI 吗？")
        assert any("cli webui" in i for i in r.forced_instructions)


# ─── PromptBuilder Tests ──────────────────────────────

class TestPromptBuilder:
    def test_includes_capability_section(self):
        pb = PromptBuilder("你是 MemoryQwen。")
        r = GUARD.detect("支持 PDF 吗？")
        msgs = pb.build("支持 PDF 吗？", capability_guard_result=r)
        user_content = msgs[1]["content"]
        assert "能力边界检查" in user_content

    def test_no_capability_section_when_not_triggered(self):
        pb = PromptBuilder("你是 MemoryQwen。")
        msgs = pb.build("你好")
        user_content = msgs[1]["content"]
        assert "能力边界检查" not in user_content

    def test_capability_section_before_sources(self):
        pb = PromptBuilder("你是 MemoryQwen。")
        r = GUARD.detect("有 Web UI 吗？")
        from src.retrieval.models import RetrievalResult
        sources = [RetrievalResult(
            record_id="1", store_type="knowledge_store",
            title="t", content="c", score=1.0,
            source_path="p", chunk_index=0, total_chunks=1, metadata={}
        )]
        msgs = pb.build("有 Web UI 吗？", retrieved=sources, capability_guard_result=r)
        content = msgs[1]["content"]
        cap_pos = content.index("能力边界检查")
        source_pos = content.index("本地资料片段")
        assert cap_pos < source_pos
