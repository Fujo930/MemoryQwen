"""Tests for Capability Registry CLI — using direct imports, not subprocess."""
import pytest
from src.capabilities.registry import load_registry, get_registry


class TestCapabilityCLI:
    def setup_method(self):
        self.registry = load_registry()

    def test_capability_list_has_implemented(self):
        assert self.registry.implemented_count() >= 2

    def test_capability_show_implemented(self):
        entry = self.registry.lookup("internet_query")
        assert entry.status == "implemented"

    def test_capability_show_not_implemented(self):
        entry = self.registry.lookup("web_ui")
        assert entry.status == "not_implemented"

    def test_capability_show_unknown(self):
        entry = self.registry.lookup("xyz_unknown")
        assert entry.status == "unknown"

    def test_list_shows_version(self):
        assert self.registry.data.version == "0.1.6"
