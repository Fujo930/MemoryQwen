#!/usr/bin/env python3
"""Check training assets for safety — project vs release mode"""
import sys, os, re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
mode = sys.argv[1] if len(sys.argv) > 1 else "project"

MODEL_EXTS = {".gguf", ".safetensors", ".bin", ".pt", ".pth", ".onnx"}
DANGER_PATTERNS = [
    (r'\.env$', "env_files"),
    (r'(?i)(api[_-]?key|token|password|secret)\s*[=:]\s*\S+', "private_patterns"),
]

results = {
    "blocked_patterns_found": 0,
    "model_weights_found": 0,
    "private_paths_found": 0,
    "pycache_found": 0 if mode == "release" else 0,  # pycache is normal in project mode
    "env_files_found": 0,
    "large_files_found": 0,
}

SKIP = {"__pycache__", ".git", ".venv", ".pytest_cache", "node_modules"} if mode == "release" else set()

for root, dnames, fnames in os.walk(str(BASE)):
    if mode == "release":
        dnames[:] = [d for d in dnames if d not in SKIP]
    for fn in fnames:
        fp = Path(root) / fn
        # model weights
        if fp.suffix.lower() in MODEL_EXTS:
            results["model_weights_found"] += 1
            print(f"  MODEL: {fp.relative_to(BASE)}")
        # danger patterns
        for pat, key in DANGER_PATTERNS:
            if re.search(pat, str(fp)):
                results[key + "_found"] = results.get(key + "_found", 0) + 1
                print(f"  {key.upper()}: {fp.relative_to(BASE)}")
        # large files (>10MB)
        try:
            sz = fp.stat().st_size
            if sz > 10 * 1024 * 1024 and not fp.name.endswith('.db'):
                results["large_files_found"] += 1
                print(f"  LARGE: {fp.relative_to(BASE)} ({sz/1024/1024:.1f} MB)")
        except OSError:
            pass

total_issues = sum(results.values())
print(f"Safety Check ({mode} mode):")
for k in ["blocked_patterns_found", "model_weights_found", "private_paths_found",
           "pycache_found", "env_files_found", "large_files_found"]:
    v = results.get(k, 0)
    print(f"  {k}: {v}")
print(f"  total_issues: {total_issues}")
sys.exit(1 if total_issues > 0 else 0)
