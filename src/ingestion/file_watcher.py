"""
MemoryQwen — File Watcher（预留接口）
监听 inbox 目录，扫描待处理文件。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class FileWatcher:
    """文件监听器（预留实现）"""

    def __init__(self, config: Any):
        self.config = config
        self.inbox_path = Path(config.ingestion.inbox_path)

    def scan_inbox(self) -> list[str]:
        """扫描 inbox 目录，返回待处理文件列表"""
        if not self.inbox_path.exists():
            return []

        supported = self.config.ingestion.supported_extensions
        recursive = self.config.ingestion.recursive
        skip_hidden = self.config.ingestion.skip_hidden_files

        file_paths = []
        glob_pattern = "**/*" if recursive else "*"

        for ext in supported:
            for f in self.inbox_path.glob(f"{glob_pattern}{ext}"):
                if skip_hidden and f.name.startswith("."):
                    continue
                file_paths.append(str(f))

        file_paths = list(set(file_paths))
        file_paths.sort()
        return file_paths

    def get_pending_files(self) -> list[str]:
        """获取待处理文件（当前 = scan_inbox）"""
        return self.scan_inbox()

    @property
    def inbox_dir(self) -> Path:
        return self.inbox_path
