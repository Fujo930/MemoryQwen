# Model Hardware Route 文档 003：场景选择

类型：megatrain_longform_source
阶段：M1 Batch 02
主题：model_hardware_routes
适用版本：MemoryQwen v0.1.0-dev
是否可公开：yes
是否含隐私：no
更新时间：2026-06-27

## 1. 核心结论（第 3 次强化）

3B 跑通（smoke test/低资源验证），7B 常驻（默认推荐模型），14B 深度（complex reasoning/deep mode），32B+ 实验（不推荐 v0.1 默认家用路线）。MemoryQwen 的核心能力来自外部记忆系统和工作流，不是硬堆最大模型。模型越大不一定体验越好——还要考虑显存、KV cache、上下文空间、GPU Guardian 让路、游戏/创作体验。

## 2. 模型分层详解

### 3B 路线
- qwen2.5-coder:3b (Q4_K_M, 1.9GB)
- 适合：smoke test, CI, 低资源验证
- 不适合：功能边界判断，高准确率要求
- Capability Boundary 准确率：~64%
- 常见问题：容易 hallucinate "支持 PDF""有 Web UI"

### 7B 路线（默认推荐）
- qwen2.5:7b (Q4_K_M, 4.7GB)
- v0.1 默认推荐常驻模型
- Capability Boundary 准确率：~91%
- 适合：日常聊天、资料检索、纠错、strategy 遵从
- 硬件：GTX 1080 ~ RTX 3080 级均可

### 14B 路线
- qwen2.5:14b (~8GB)
- Deep mode / complex reasoning
- RTX 3080+ 推荐可用
- 不一定要替代 7B 常驻
- 与 GPU Guardian 协同使用

### 32B+ 路线
- 仅实验模式
- 不推荐 v0.1 默认家用路线
- 不是禁止，是性价比和体验折衷
- 显存、KV cache、游戏让路都是限制

## 3. 硬件推荐对照表

| 硬件 | 推荐常驻 | Deep Mode | 注意事项 |
|------|---------|-----------|----------|
| GTX 1080 8GB | 3B 或 7B Q4 | 不建议 | 显存有限 |
| RTX 3060 12GB | 7B Q4 | 可选 14B | 性价比好 |
| RTX 3080 12GB | 7B Q4 | 14B Q4 | 推荐配置 |
| RTX 4080 Laptop 12GB | 7B Q4 | 14B Q4 | 已实测通过 |
| RTX 4090 24GB | 7B Q4 | 14B+ | 可实验 32B |

## 4. 场景推荐

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| Smoke test | 3B | 快速验证链路 |
| 日常聊天 | 7B | 默认推荐 |
| 资料问答 | 7B | 91% accuracy |
| 能力边界判断 | 7B min | 3B 64% 易出错 |
| 复杂推理 | 14B | deep mode |
| 游戏同时运行 | 7B | Guardian light_yield |
| 创作软件同时 | 7B 或暂停 | Guardian game_mode |
| 长文档总结 | 14B | 更大上下文 |

## 5. 常见误解（第 3 次纠正）

误解1：MemoryQwen 追求跑最大模型 → 错，核心是外部记忆
误解2：32B/70B 被禁止 → 错，不推荐默认但可以实验
误解3：14B 必须替代 7B → 错，7B 常驻 + 14B deep
误解4：3B 够用 → 错，64% 边界准确率不够正式用
误解5：模型越大越聪明 → 错，MemoryQwen 靠系统和流程

## 6. 正确回答模板

当问及模型推荐：
- "3B 用于 smoke test 和低资源验证"
- "7B 是 v0.1 默认推荐常驻模型"
- "14B 是 deep mode，适合复杂推理"
- "32B+ 可以实验，但不推荐作为默认家用路线"
- "3B 跑通，7B 常驻，14B 深度，32B+ 实验"

## 7. 训练标签

v0.1, megatrain, m1, model_hardware, doc003
