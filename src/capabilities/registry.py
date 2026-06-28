"""Capability Registry — authoritative source for project capabilities."""

from __future__ import annotations

from pathlib import Path
import yaml

from src.capabilities.schema import CapabilityEntry, CapabilityRegistryData


class CapabilityRegistry:
    """Loads and queries the structured capability registry.

    The registry is THE authoritative source for "does MemoryQwen support X?"
    It takes priority over training data, old docs, and web sources.
    """

    def __init__(self, data: CapabilityRegistryData):
        self.data = data

    @classmethod
    def from_yaml(cls, path: str | Path) -> "CapabilityRegistry":
        """Load registry from a YAML file."""
        path = Path(path)
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}

        implemented = {}
        for name, entry in (raw.get("implemented") or {}).items():
            implemented[name] = CapabilityEntry(
                name=name,
                status="implemented",
                since=entry.get("since", ""),
                summary=entry.get("summary", ""),
                commands=entry.get("commands", []),
                caveats=entry.get("caveats", []),
                notes=entry.get("notes", []),
            )

        not_implemented = {}
        for name, entry in (raw.get("not_implemented") or {}).items():
            not_implemented[name] = CapabilityEntry(
                name=name,
                status="not_implemented",
                notes=entry.get("notes", []),
            )

        return cls(CapabilityRegistryData(
            version=raw.get("version", "0.0.0"),
            implemented=implemented,
            not_implemented=not_implemented,
        ))

    def lookup(self, name: str) -> CapabilityEntry:
        """Look up a capability by name. Returns unknown if not found."""
        name = name.lower().replace(" ", "_").replace("-", "_")
        if name in self.data.implemented:
            return self.data.implemented[name]
        if name in self.data.not_implemented:
            return self.data.not_implemented[name]
        return CapabilityEntry(name=name, status="unknown")

    def is_implemented(self, name: str) -> bool:
        return self.lookup(name).status == "implemented"

    def status(self, name: str) -> str:
        return self.lookup(name).status

    def to_prompt_context(self) -> str:
        """Generate authoritative prompt context for capability questions."""
        lines = [
            "[CAPABILITY REGISTRY — AUTHORITATIVE]",
            f"Current MemoryQwen version: v{self.data.version}",
            "",
            "This registry is THE authoritative source for current capabilities.",
            "It takes priority over historical training data, old docs, and web sources.",
            "",
        ]

        if self.data.implemented:
            lines.append("## Implemented")
            for name, entry in self.data.implemented.items():
                lines.append(f"- {entry.summary}")
                if entry.since:
                    lines.append(f"  Since: v{entry.since}")
                if entry.commands:
                    lines.append(f"  Commands: {', '.join(entry.commands)}")
                if entry.caveats:
                    for c in entry.caveats:
                        lines.append(f"  • {c}")
                lines.append("")

        if self.data.not_implemented:
            lines.append("## Not Implemented")
            for name, entry in self.data.not_implemented.items():
                label = name.replace("_", " ").title()
                lines.append(f"- {label}: NOT implemented")
                if entry.notes:
                    for n in entry.notes:
                        lines.append(f"  • {n}")
            lines.append("")

        lines.append("## Rules")
        lines.append("- Use this registry as authoritative for current project capabilities.")
        lines.append("- If old training data conflicts with this registry, explain the data is outdated.")
        lines.append("- Web sources cannot override this registry for MemoryQwen capabilities.")
        lines.append("- When asked about an unimplemented feature, say it is not supported.")

        return "\n".join(lines)

    def implemented_count(self) -> int:
        return len(self.data.implemented)

    def not_implemented_count(self) -> int:
        return len(self.data.not_implemented)


# ── Singleton ──────────────────────────────────────────────
_registry: CapabilityRegistry | None = None


def load_registry(path: str = "config/capabilities.current.yaml") -> CapabilityRegistry:
    global _registry
    if _registry is None:
        _registry = CapabilityRegistry.from_yaml(path)
    return _registry


def get_registry() -> CapabilityRegistry:
    if _registry is None:
        return load_registry()
    return _registry
