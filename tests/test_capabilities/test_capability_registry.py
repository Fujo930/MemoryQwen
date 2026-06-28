"""Tests for Capability Registry loading and lookup."""
import pytest, tempfile
from pathlib import Path
from src.capabilities.registry import CapabilityRegistry, load_registry
from src.capabilities.schema import CapabilityEntry


class TestCapabilityRegistry:
    def setup_method(self):
        self.registry = load_registry("config/capabilities.current.yaml")

    def test_registry_loads(self):
        assert self.registry is not None
        assert self.registry.data.version == "0.1.6"

    def test_internet_query_implemented(self):
        assert self.registry.is_implemented("internet_query") is True
        entry = self.registry.lookup("internet_query")
        assert entry.status == "implemented"
        assert entry.since == "0.1.5"
        assert "web search" in entry.commands

    def test_deep_mode_implemented(self):
        assert self.registry.is_implemented("deep_mode") is True
        entry = self.registry.lookup("deep_mode")
        assert entry.since == "0.1.6"

    def test_web_ui_not_implemented(self):
        assert self.registry.is_implemented("web_ui") is False
        entry = self.registry.lookup("web_ui")
        assert entry.status == "not_implemented"

    def test_pdf_not_implemented(self):
        assert self.registry.is_implemented("pdf_ingestion") is False

    def test_crawler_not_implemented(self):
        assert self.registry.is_implemented("crawler") is False

    def test_unknown_capability(self):
        entry = self.registry.lookup("nonexistent_feature_123")
        assert entry.status == "unknown"

    def test_web_ask_caveat_present(self):
        entry = self.registry.lookup("internet_query")
        caveats = " ".join(entry.caveats).lower()
        assert "does not write to memory" in caveats or "temporary" in caveats

    def test_web_ingest_caveat_present(self):
        entry = self.registry.lookup("internet_query")
        caveats = " ".join(entry.caveats).lower()
        assert "web-to-memory" in caveats or "explicit" in caveats

    def test_deep_mode_optional(self):
        entry = self.registry.lookup("deep_mode")
        caveats = " ".join(entry.caveats).lower()
        assert "optional" in caveats or "not required" in caveats

    def test_count(self):
        assert self.registry.implemented_count() >= 2
        assert self.registry.not_implemented_count() >= 8

    def test_status_string(self):
        assert self.registry.status("internet_query") == "implemented"
        assert self.registry.status("web_ui") == "not_implemented"
        assert self.registry.status("xyz") == "unknown"

    def test_prompt_context_generated(self):
        ctx = self.registry.to_prompt_context()
        assert "CAPABILITY REGISTRY" in ctx
        assert "0.1.6" in ctx
        assert "authoritative" in ctx.lower()

    def test_prompt_context_has_implemented(self):
        ctx = self.registry.to_prompt_context()
        assert "Internet Query" in ctx or "internet" in ctx.lower()

    def test_prompt_context_has_not_implemented(self):
        ctx = self.registry.to_prompt_context()
        assert "Web Ui" in ctx or "web_ui" in ctx.lower()
