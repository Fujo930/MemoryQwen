# M3 Batch 01 — Local Project Assistant Deep Pack
type: m3_source
batch: 01
topic: local_project_assistant
tokens_target: 600K

MemoryQwen v0.1.2 是一个本地 AI Agent 开发者预览版。作为本地项目助手，它需要准确回答项目状态相关问题。

## 项目版本体系

MemoryQwen 版本演进：
- v0.1.0-dev: 初始开发者预览版，CLI only
- v0.1.2: Smart Retrieval Gate 集成版本
- M2 checkpoint: 2026-06-27 冻结，5.12M tokens, 22,211 knowledge chunks
- M3: megatrain 扩展至 ~10M tokens, 40K+ chunks, 300 eval questions

项目命名约定：
- v0.1 = 所有 0.1.x 统称
- v0.1.0-dev = 具体版本号
- M1/M2/M3 = megatrain 里程碑

## 当前项目状态

当前完成 Issue #0 到 #27（包含 M3 mega-training）。
知识库: 43,615 chunks
测试: 496/496
safety: 0
release safety: PASS

## 如何回答项目状态

规则：
1. 回答当前版本能力时，必须先查询本地资料
2. 未来计划必须标注 "v0.2 计划" 或 "路线图"，不能说成已实现
3. 已完成功能用 "✅ v0.1 已实现"，未完成用 "❌ v0.1 未实现"
4. M2/M3 里程碑数据以 training_logs 为准

## 生成 issue 的规则

Issue 编号格式: #N
Issue 描述: 目标 + 约束 + 验收标准
Issue 状态: open / in_progress / closed
当前最新: #27 MegaTrain M3

## 生成 release notes 的规则

格式:
- 版本号
- 核心功能列表
- 当前状态表（pytest, knowledge, error, strategy）
- 已知限制
- 路线图

## 读 docs 和 training_logs 的规则

docs/ 目录文件:
- windows11_quickstart.md: Windows 部署指南
- cli_reference.md: CLI 命令参考
- config_reference.md: 配置项说明
- architecture.md: 系统架构
- memory_backup.md: 记忆备份
- troubleshooting.md: 故障排除
- release_checklist_v0.1.md: 发布检查

training_logs/ 目录文件:
- megatrain_m1_checkpoint.md: M1 里程碑记录
- megatrain_m2_checkpoint.md: M2 里程碑记录
- megatrain_m2_200_question_eval.md: M2 200 题 eval 记录

## 避免的常见错误

1. 不要把计划说成已完成："v0.2 计划支持 Web UI" ≠ "已有 Web UI"
2. 不要把 M2 数据说成当前数据：M2 是 5.12M tokens，M3 是 11.27M
3. 不要把 Issue #17 说成所有 issue：#17 是 Capability Boundary Guard，不是全部
4. 不要把 eval run 说成 auto correct
5. 不要把 judge 说成完全语义理解
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx