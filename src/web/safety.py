"""
MemoryQwen — Web safety: URL validation, SSRF prevention, prompt injection detection.
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse

# ── Private / reserved IP ranges (IPv4) ──────────────────────
_PRIVATE_IPV4_NETS = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv4Network("169.254.0.0/16"),
    ipaddress.IPv4Network("127.0.0.0/8"),
    ipaddress.IPv4Network("0.0.0.0/8"),
]

# ── Prompt injection detection patterns ─────────────────────
_PROMPT_INJECTION_PATTERNS: list[re.Pattern] = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(a\s+)?(system|admin|root|god)", re.IGNORECASE),
    re.compile(r"(delete|remove|erase)\s+(all\s+)?(files?|memory|data)", re.IGNORECASE),
    re.compile(r"(run|execute)\s+(this\s+)?(command|code|script)", re.IGNORECASE),
    re.compile(r"(write|save)\s+(to|into)\s+(memory|database|config)", re.IGNORECASE),
    re.compile(r"(change|modify|override)\s+(your\s+)?(config|system|rules|prompt)", re.IGNORECASE),
    re.compile(r"(exfiltrate|send|upload|leak)\s+(secrets?|keys?|tokens?|data)", re.IGNORECASE),
    re.compile(r"forget\s+(everything|all\s+rules)", re.IGNORECASE),
    re.compile(r"you\s+are\s+(not|no\s+longer)\s+(a\s+)?(MemoryQwen|assistant|AI)", re.IGNORECASE),
]


def is_private_ip(hostname: str) -> bool:
    """Check if a hostname resolves to a private/reserved IP.

    Returns True if the IP is private, loopback, link-local, or multicast.
    Returns False for public IPs or unresolvable hostnames (DNS check deferred).
    """
    try:
        addr = ipaddress.IPv4Address(hostname)
    except ValueError:
        # Not a raw IP — DNS hostname, allow (safe after fetch)
        return False

    for net in _PRIVATE_IPV4_NETS:
        if addr in net:
            return True
    return addr.is_multicast or addr.is_reserved


def validate_url(url: str, allow_private: bool = False) -> tuple[bool, str | None]:
    """Validate a URL for safety.

    Returns (is_safe, error_message).
    """
    if not url or not isinstance(url, str):
        return False, "empty URL"

    parsed = urlparse(url)

    # Block non-HTTP schemes
    if parsed.scheme not in ("http", "https"):
        return False, f"scheme '{parsed.scheme}' not allowed (http/https only)"

    # Check hostname
    hostname = parsed.hostname
    if not hostname:
        return False, "no hostname in URL"

    # Block raw IPs in hostname position
    hostname_lower = hostname.lower()

    # Block localhost variants
    if hostname_lower in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
        return False, "localhost not allowed"

    # Block private IPs unless explicitly allowed
    if not allow_private and is_private_ip(hostname):
        return False, f"private/reserved IP not allowed: {hostname}"

    return True, None


def detect_prompt_injection(text: str) -> list[str]:
    """Detect potential prompt injection patterns in web content.

    Returns a list of matched category descriptions (empty = clean).
    """
    hits: list[str] = []
    for pattern in _PROMPT_INJECTION_PATTERNS:
        if pattern.search(text):
            # Get a human-readable label from the pattern
            label = pattern.pattern[:60].rstrip("\\")
            hits.append(label)
    return hits


def has_suspicious_content(text: str) -> bool:
    """Quick check: does text contain any prompt injection patterns?"""
    return len(detect_prompt_injection(text)) > 0
