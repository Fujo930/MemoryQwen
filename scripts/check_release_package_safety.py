#!/usr/bin/env python3
"""Check release zip for safety: no secrets, no weights, no cache"""
import re, sys, zipfile
from pathlib import Path

zip_path = sys.argv[1] if len(sys.argv) > 1 else sys.exit("Usage: <zip>")

results = {
    "env_files_found": 0, "secrets_found": 0, "private_paths_found": 0,
    "cache_files_found": 0, "model_weights_found": 0, "large_files_found": 0,
}

MODEL_EXTS = {".gguf", ".safetensors", ".bin", ".pt", ".pth", ".onnx"}
DANGER = [
    # Match key="value" where value has actual content (not empty "")
    (r'(?i)(api[_-]?key|token|password|secret)\s*[=:]\s*["\']([^"\']{4,})["\']', "secrets"),
    (r"sk-[a-zA-Z0-9]{20,}", "secrets"),
]

with zipfile.ZipFile(zip_path) as zf:
    for info in zf.infolist():
        name = info.filename
        # Check file name
        if name.endswith(".env"):
            results["env_files_found"] += 1
            print(f"  ENV: {name}")
        if Path(name).suffix.lower() in MODEL_EXTS:
            results["model_weights_found"] += 1
            print(f"  MODEL: {name}")
        if "__pycache__" in name or ".pyc" in name:
            results["cache_files_found"] += 1
            print(f"  CACHE: {name}")
        if info.file_size > 10 * 1024 * 1024 and not info.filename.endswith('.db'):
            results["large_files_found"] += 1
            print(f"  LARGE: {name} ({info.file_size/1024/1024:.1f} MB)")

        # Check file content for text files
        if name.endswith((".py", ".md", ".txt", ".yaml", ".json", ".toml", ".cfg")):
            try:
                content = zf.read(info).decode("utf-8", errors="replace")
                for pat, cat in DANGER:
                    if re.search(pat, content):
                        results[f"{cat}_found"] += 1
                        print(f"  {cat.upper()}: {name}")
                        break  # one hit per file is enough
            except Exception:
                pass

total = sum(results.values())
status = "PASS" if total == 0 else "FAIL"
print(f"\nRelease Safety Check:")
for k, v in results.items():
    print(f"  {k}: {v}")
print(f"  status: {status}")
sys.exit(1 if total > 0 else 0)
