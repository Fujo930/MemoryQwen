"""
MemoryQwen — 应用主模块
负责服务生命周期管理
"""

import os
import sys
import logging
from pathlib import Path

from src.config import load_config, get_config


def setup_logging():
    """配置日志系统"""
    config = get_config()
    log_dir = Path(config.system.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config.system.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(config.system.log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def ensure_directories(config):
    """确保所有必要目录存在"""
    dirs = [
        config.system.data_dir,
        config.system.inbox_dir,
        config.system.workspace_dir,
        "config/model_profiles",
        "logs",
        "backup",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def main():
    """应用入口"""
    # 加载配置
    config = load_config()
    setup_logging()
    ensure_directories(config)

    logger = logging.getLogger(__name__)
    logger.info("MemoryQwen v%s starting...", config.system.version)
    logger.info("Data dir: %s", config.system.data_dir)
    logger.info("Model: %s (light) / %s (deep)",
                config.model.default_light_model,
                config.model.default_deep_model)

    # 延迟导入避免循环依赖
    from src.server.api import create_app
    import uvicorn

    app = create_app(config)
    logger.info("Starting server at http://%s:%d", config.server.host, config.server.port)

    uvicorn.run(
        app,
        host=config.server.host,
        port=config.server.port,
        reload=config.server.reload,
        log_level=config.system.log_level.lower(),
    )


if __name__ == "__main__":
    main()
