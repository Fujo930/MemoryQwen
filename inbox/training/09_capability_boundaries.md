# MemoryQwen v0.1 能力边界对照手册

来源：MemoryQwen 训练资料
资料类型：training_rules
更新时间：2026-06-27
主题：v0.1 已实现 vs 未实现 vs 未来计划 — 精确对照表
关键词：capability boundary、已实现、未实现、v0.2、WebUI、PDF、embedding、LoRA、daemon

## 核心硬规则

1. 如果用户问"是否支持某功能"，必须先查本手册
2. 功能在"未实现"列表中 → 回答"v0.1 尚未实现"
3. 功能在"未来计划"列表中 → 回答"这是未来计划，v0.1 尚未实现"
4. 不能把 CLI 说成 Web UI
5. 不能把 `.md/.txt` ingestion 说成 PDF ingestion
6. 不能把 GPU status detection 说成 daemon
7. 不能把 source archive 说成 crawler
8. 不能把 AutoModelAdapter 说成 LoRA/微调
9. 不确定 → 说"根据本地资料不能确定"
10. 不要把未来计划和已实现搞混

## 功能对照表

| 功能 | v0.1 状态 | 说明 |
|------|----------|------|
| CLI (命令行) | ✅ 已实现 | 当前主要入口，`python -m src.cli` |
| Web UI (网页界面) | ❌ 未实现 | 未来 v0.2 计划，当前没有 |
| 桌面 GUI | ❌ 未实现 | 没有桌面图形界面 |
| Windows tray (托盘) | ❌ 未实现 | 没有系统托盘 |
| 后台 daemon | ❌ 未实现 | 没有后台自动运行 |
| 自动模型卸载 | ❌ 未实现 | GPU Guardian 只检测，不卸载模型 |
| kill 进程 | ❌ 未实现 | GPU Guardian 不杀任何进程 |
| health 检查 | ✅ 已实现 | `python -m src.cli health` |
| .txt / .md 导入 | ✅ 已实现 | `python -m src.cli ingest` |
| job ingest | ✅ 已实现 | 后台摄入任务 |
| PDF ingestion | ❌ 未实现 | v0.1 不支持 PDF |
| DOCX ingestion | ❌ 未实现 | v0.1 不支持 DOCX |
| 全站 crawler | ❌ 未实现 | 不支持递归抓取网站 |
| chat | ✅ 已实现 | 本地模型聊天 |
| correct (纠错) | ✅ 已实现 | 写入 error_store |
| error_store | ✅ 已实现 | 错误案例存储 |
| strategy_store | ✅ 已实现 | 策略沉淀 |
| memory stats | ✅ 已实现 | 存储统计 |
| source archive | ✅ 已实现 | 资料归档到 memory/sources |
| guardian status | ✅ 已实现 | GPU 状态检测 |
| guardian json | ✅ 已实现 | JSON 格式输出 |
| task list/status/pause/resume/cancel | ✅ 已实现 | 任务管理 |
| profile show/validate | ✅ 已实现 | 模型 profile 管理 |
| embedding / 向量搜索 | ❌ 未实现 | v0.1 只有 BM25 关键词检索 |
| 向量数据库 | ❌ 未实现 | 没有 FAISS/Chroma |
| LoRA | ❌ 未实现 | 当前不修改模型权重 |
| 模型微调 | ❌ 未实现 | 当前不做权重训练 |
| AutoModelAdapter basic eval | ✅ 已实现基础版 | 轻量模型能力评估，不是微调 |
| 7B/14B 自动路由 | ❌ 未实现 | 未来计划 |
| 多路径 Reasoner | ❌ 未实现 | 未来计划 |
| 长期自动后台学习 | ❌ 未实现 | 当前需要手动纠正 |
| 一键安装 exe | ❌ 未实现 | Developer Preview，需要命令行 |

## v0.2 未来计划功能

以下功能在 v0.1 中不存在，不要声称已支持：

- FastAPI Local Server
- Web UI 最小聊天页
- embedding / 向量检索
- PDF / DOCX parser
- prompt hardening
- model router (7B/14B)
- GPU Guardian daemon / tray
- source archive rebuild
- stronger verifier / reasoner

## 容易混淆的点

1. CLI ≠ Web UI — 有 CLI 不代表有网页界面
2. GPU status detection ≠ daemon — Guardian 只检测，不后台持续运行
3. source archive ≠ crawler — 归档是复制，不是抓网站
4. AutoModelAdapter ≠ LoRA — 轻量 eval，不训练权重
5. .md/.txt ingestion ≠ PDF — 只支持纯文本/标记文件
6. job ingest ≠ 自动后台 — 需要手动触发

## 可测试问题

1. MemoryQwen v0.1 有 Web UI 吗？
2. MemoryQwen v0.1 有 CLI 吗？
3. MemoryQwen v0.1 支持 PDF ingestion 吗？
4. MemoryQwen v0.1 支持 .md / .txt ingestion 吗？
5. GPU Guardian v0 会不会真的卸载模型？
6. GPU Guardian v0 是 daemon 吗？
7. MemoryQwen 当前会不会 kill 游戏进程？
8. MemoryQwen v0.1 有没有 Windows tray？
9. MemoryQwen 是否会修改模型权重？
10. AutoModelAdapter 是不是 LoRA？
11. MemoryQwen 目前支持 embedding/vector DB 吗？
12. source archive 是不是全站 crawler？
13. MemoryQwen v0.1 支持中文文件名吗？
14. MemoryQwen v0.1 的主要入口是什么？
15. task runtime 是否会自动后台恢复执行？
16. job ingest 是否已实现？
17. correct 是否会写入 error_store？
18. strategy_store 是否已实现？
19. Web UI 是现在功能还是未来计划？
20. FastAPI server 是现在功能还是未来计划？
