#!/usr/bin/env python3
"""MemoryQwen Release Package Builder"""
import hashlib, os, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
VERSION = (BASE / "VERSION").read_text(encoding="utf-8").strip()
DIST = BASE / "dist"
DIST.mkdir(exist_ok=True)

EXCLUDE_DIRS = {
    ".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", "memory/web_cache", "node_modules", ".hermes",
    "model_eval_reports",  # exclude old eval dirs from source
}
EXCLUDE_FILES = {
    ".env", ".DS_Store", "Thumbs.db",
}
EXCLUDE_EXTS = {
    ".gguf", ".safetensors", ".bin", ".pt", ".pth", ".onnx",
    ".key", ".pem", ".pyc",
}

# Source package files
SOURCE_DIRS = [
    "src/", "tests/", "config/", "docs/", "examples/",
    "scripts/", "training_packs/",
]
SOURCE_ROOT_FILES = [
    "README.md", "VERSION", "requirements.txt",
]

# Devpack additions (on top of source)
DEVPACK_EXTRA = [
    "memory/sources/",
    "training_logs/",
    "docs/v0.1_checkpoint.md",
    "docs/release_notes_v0.1.0-dev.md",
]
DEVPACK_OPTIONAL = [
    "memory/memoryqwen.db",
    "memory/tasks.db",
]


def should_exclude(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    for p in parts:
        if p in EXCLUDE_DIRS:
            return True
    if Path(path).name in EXCLUDE_FILES:
        return True
    if Path(path).suffix.lower() in EXCLUDE_EXTS:
        return True
    return False


def build_zip(name, include_paths, label):
    zip_path = DIST / name
    print(f"\nBuilding {label}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for inc in include_paths:
            full = BASE / inc
            if "*" in inc:
                # glob pattern for root files
                continue
            if not full.exists():
                print(f"  Skip (missing): {inc}")
                continue
            if full.is_dir():
                for root, dirs, files in os.walk(str(full)):
                    # Exclude dirs in-place
                    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                    for fn in files:
                        fp = Path(root) / fn
                        if fp.suffix.lower() in EXCLUDE_EXTS or fn in EXCLUDE_FILES:
                            continue
                        arc = fp.relative_to(BASE)
                        zf.write(fp, arc)
            else:
                zf.write(full, full.relative_to(BASE))

    size_mb = zip_path.stat().st_size / 1024 / 1024
    sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    count = 0
    with zipfile.ZipFile(zip_path) as zf:
        count = len(zf.namelist())
    print(f"  {name}: {size_mb:.2f} MB, {count} files")
    print(f"  SHA256: {sha}")
    return {
        "name": name,
        "path": str(zip_path),
        "size_mb": size_mb,
        "files": count,
        "sha256": sha,
    }


# ─── Build ───────────────────────────────────────────

print(f"MemoryQwen {VERSION} Release Builder")
print(f"Time: {datetime.now(timezone.utc).isoformat()}")

# Source paths to include
source_paths = list(SOURCE_DIRS) + SOURCE_ROOT_FILES

devpack_paths = list(SOURCE_DIRS) + SOURCE_ROOT_FILES + DEVPACK_EXTRA
for opt in DEVPACK_OPTIONAL:
    if (BASE / opt).exists():
        devpack_paths.append(opt)

result_source = build_zip(f"MemoryQwen-{VERSION}-source.zip", source_paths, "Source Package")
result_devpack = build_zip(f"MemoryQwen-{VERSION}-devpack.zip", devpack_paths, "DevPack")

print(f"\n=== Build Complete ===")
print(f"Source: {result_source['name']} ({result_source['size_mb']:.2f} MB, {result_source['files']} files)")
print(f"DevPack: {result_devpack['name']} ({result_devpack['size_mb']:.2f} MB, {result_devpack['files']} files)")
print(f"Output dir: {DIST}")
