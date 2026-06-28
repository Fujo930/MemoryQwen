# M3 Batch 03 — Capability Boundary Extreme Pack
type: m3_source
batch: 03
topic: capability_boundary
tokens_target: 700K

MemoryQwen v0.1 Capability Boundary Guard 负责防止模型声称支持未实现的功能。

## 已实现 vs 未实现

### ✅ v0.1 已实现
- CLI 聊天 (chat)
- 文档导入 (.txt, .md)
- BM25 关键词检索
- 聊天引用来源（精确到文件路径）
- 用户纠错 (correct)
- 策略沉淀 (strategy_store)
- GPU Guardian 检测
- 任务队列 + 暂停/恢复
- SQLite 持久化任务
- Source Archive (memory/sources/)
- Smart Retrieval Gate (v0.1.2)
- Capability Boundary Guard
- Eval Runner + Heuristic Judge
- 中文文件名 UTF-8 支持
- 训练资产 stats/safety 脚本

### ❌ v0.1 未实现
- Web UI / 图形界面
- PDF / DOCX 导入
- Embedding / 向量检索
- Background daemon / 自动运行
- Windows tray 图标
- 网络爬虫 / crawler
- Internet Query（v0.1.5 计划）
- LoRA fine-tuning
- 模型卸载
- 一键安装 exe
- FastAPI server
- 远程访问
- 模型路由/自动切换
- 对话摘要

### ❌ v0.1 不存在的 CLI 命令
以下命令不存在：
- cli webui
- cli pdf
- cli daemon
- cli crawler
- cli embedding
- cli lora
- cli serve
- cli remote

## Capability Boundary Guard 规则

强制指令（注入到 system prompt 中）：
1. 只根据本地资料回答
2. 未实现功能→"v0.1尚未实现"
3. 不把未来计划说成当前能力
4. 不把CLI说成WebUI
5. 不把Guardian检测说成daemon/tray
6. 不把.md/.txt ingestion说成PDF/DOCX
7. 不把source archive说成crawler
8. 不把AutoModelAdapter说成LoRA/微调
9. 不编造CLI命令
10. 资料不足→"根据当前本地资料不能确定"

## 高风险术语检测

Guard 检测以下高风险术语：
- PDF, Web UI, daemon, embedding, LoRA, crawler, FastAPI
- 支持, 有没有, 是否, 当前, 已实现

命中高风险术语 → guard_triggered=True → 注入强制指令

## 常见陷阱

Q: "MemoryQwen 支持 PDF 吗？"
A: ❌ 错误："支持 PDF..."  
A: ✅ 正确："v0.1 不支持 PDF 导入。只支持 .txt 和 .md。"

Q: "有 Web UI 吗？"
A: ❌ 错误："有 Web UI..."  
A: ✅ 正确："v0.1 没有 Web UI。是 CLI only。v0.2 计划支持。"

Q: "source archive 是爬虫吗？"
A: ❌ 错误："是爬虫..."  
A: ✅ 正确："不是爬虫。source archive 复制本地文件到 memory/sources/。" 
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx