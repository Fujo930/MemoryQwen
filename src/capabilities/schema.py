"""Capability Registry schema types."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CapabilityEntry:
    """A single capability entry."""
    name: str
    status: str = "unknown"        # "implemented" | "not_implemented" | "unknown"
    since: str = ""                # version when implemented
    summary: str = ""
    commands: list[str] = field(default_factory=list)
    caveats: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class CapabilityRegistryData:
    """Full capability registry loaded from YAML."""
    version: str = "0.0.0"
    implemented: dict[str, CapabilityEntry] = field(default_factory=dict)
    not_implemented: dict[str, CapabilityEntry] = field(default_factory=dict)
