# v0.1 Release Checklist

## 代码质量

- [x] pytest 全部通过: `python -m pytest tests/ -q` → **429 passed**
- [x] 所有 Python 模块无导入错误
- [x] 无硬编码密钥或敏感信息
- [x] safety check 通过 (0 secrets, 0 weights, 0 cache)

## Windows 11 环境验证

- [x] health 通过
- [x] 本地模型 (qwen2.5:7b) chat 成功
- [x] 中文文件名 ingest 通过
- [x] chat sources 显示正常
- [x] correct + strategy 生成
- [x] guardian status 正常 (RTX 4080 Laptop)
- [x] guardian json 正常
- [x] job ingest 写入 task
- [x] task list 持久化 (SQLiteTaskStore)
- [x] memory stats 正常

## 文档

- [x] README.md (含模型推荐)
- [x] windows11_quickstart.md
- [x] cli_reference.md
- [x] config_reference.md
- [x] memory_backup.md
- [x] troubleshooting.md
- [x] release_notes_v0.1.0-dev.md
- [x] v0.1_checkpoint.md
- [x] model_recommendations.md
- [x] release_checklist_v0.1.md (本文件)

## 示例

- [x] examples/inbox/test.md
- [x] examples/inbox/中文测试.md

## 脚本

- [x] scripts/start_windows.bat (交互聊天)
- [x] scripts/smoke_test_windows.bat
- [x] scripts/run_tests.bat
- [x] scripts/training_asset_stats.py (v2)
- [x] scripts/check_training_asset_safety.py
- [x] scripts/check_release_package_safety.py
- [x] scripts/check_eval_question_quality.py
- [x] scripts/build_release_package.py

## 发布包

- [x] Source zip built (0.39 MB, 388 files)
- [x] DevPack zip built (1.12 MB, 882 files)
- [x] Release manifest written
- [x] No model weights included
- [x] No secrets in packages
- [x] No cache files
- [x] VERSION 文件: 0.1.0-dev
- [x] Known limitations documented

## 未实现功能 (已文档化)

- [x] Web UI → 标记为 v0.2 计划
- [x] PDF/DOCX → 标记为不支持
- [x] embedding/vector DB → 标记为不支持
- [x] daemon/tray → 标记为不支持
- [x] LoRA/微调 → 标记为不支持

---

最后验证:
```bash
python -m pytest tests/ -q
```

预期: **429 passed**
