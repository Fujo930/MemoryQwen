"""ACE-v1 — Context plan building (what to include in prompt)."""

from __future__ import annotations
from .schema import ContextPlan, ModelPlan, ReviewPlan, ACEDecision


def build_ace_context(decision: ACEDecision) -> str:
    """Build the ACE context string for prompt injection."""
    lines: list[str] = []

    cp = decision.context_plan
    mp = decision.model_plan
    rp = decision.review_plan

    # Routing banner
    lines.append(f"[ACE v1 — Route: {decision.route}]")

    # Context flags
    flags = []
    if cp.use_capability_registry: flags.append("CapabilityRegistry")
    if cp.use_memory_retrieval: flags.append("MemoryRetrieval")
    if cp.use_web_context: flags.append("WebContext")
    if cp.use_guard: flags.append("Guard")
    if cp.include_deep_mode_hint: flags.append("DeepModeHint")
    lines.append("Active modules: " + (", ".join(flags) if flags else "none"))

    # Model plan
    lines.append(f"Model: {mp.selected_model or 'default'} (role: {mp.selected_model_role})")

    if mp.deep_suggested and not mp.auto_escalated:
        lines[-1] += " [deep mode suggested — use --deep for better reasoning]"

    # Review plan
    if rp.judge_review_recommended:
        lines.append("⚠ Judge review recommended: verify answer against Registry and Guard before finalizing.")
    if rp.manual_review_required:
        lines.append("⚠ Manual review required: conflicting sources detected. Prioritize Capability Registry.")

    # Reasons
    if decision.reasons:
        lines.append("Reasons:")
        for r in decision.reasons:
            lines.append(f"  - {r}")

    # Priority rule
    lines.append("Priority: Capability Registry > new docs > old training data > web sources.")

    return "\n".join(lines)


def build_ace_prompt_injection(decision: ACEDecision) -> str:
    """Build the full ACE injection for the user prompt."""
    return "[ACE COGNITIVE EXOSKELETON — SYSTEM CONTEXT]\n" + build_ace_context(decision) + "\n"
