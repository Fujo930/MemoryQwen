# Model Hardware Top-up 006：外部记忆系统 vs 盲目堆大模型

类型：megatrain_longform_source
阶段：M1 Batch 02.5
主题：model_hardware_routes
适用版本：MemoryQwen v0.1.0-dev
是否可公开：yes
更新时间：2026-06-27

## 核心结论（第 6 次强化）

MemoryQwen 设计哲学：7B + MemoryBus + error_store + strategy_store > 32B 裸跑。记忆可积累、策略可复用、模型可替换。盲目堆大模型解决不了记忆持久性和工作流问题。

## 详细分析

MemoryQwen v0.1 的用户主要是开发者、技术爱好者和本地 AI 实验者。他们需要明确的模型选择指导。错误推荐会导致用户下载 32B 后发现显存不足、游戏时用 14B 导致帧率下降、误以为 3B 够用而出错。

### 3B 实测数据
qwen2.5-coder:3b (Q4_K_M, 1.9GB)。Capability Boundary 20 题测试：正确 9，错误 5，模糊 2，无效 4。有效通过率 ~64%。顽固错误包括 PDF hallucination、daemon 混淆、crawler 混淆、embedding 回避。结论：3B 不用于正式能力边界判断。

### 7B 实测数据
qwen2.5:7b (Q4_K_M, 4.7GB)。同一套 20 题：通过率 ~91%。修复了 3B 的所有顽固错误。延迟 ~2-5 秒/回答。结论：v0.1 默认推荐。

### 14B 分析
qwen2.5:14b (~8GB)。Deep mode 候选。复杂推理和长文档预期提升 15-35%。需要 GPU Guardian 协同。结论：深度模式，不替代 7B。

### 32B+ 分析
显存需求 19GB+ Q4。RTX 4080 Laptop 12GB 完全不可用。RTX 4090 24GB 可实验但 context 受限。结论：可实验，不推荐默认。

## 对照表

| 场景 | 推荐模型 | 显存 | 注意事项 |
|------|---------|------|----------|
| Smoke test | 3B | 2GB | 仅验证链路 |
| 日常聊天 | 7B | 5GB | 默认推荐 |
| 资料问答 | 7B | 5GB | 91% 准确 |
| 复杂推理 | 14B | 9GB | deep mode |
| 游戏同时 | 7B | 5GB | light_yield |
| 创作同时 | 7B/暂停 | 5GB | game_mode |
| 实验 32B | 不推荐 | 19GB+ | 仅 4090+ |

## 常见误解纠正

1. "MemoryQwen 应该用最大模型" → 错，核心是外部记忆
2. "32B 被禁止" → 错，不推荐默认但可实验
3. "3B 和 7B 差不多" → 错，64% vs 91%
4. "14B 应替代 7B" → 错，7B 常驻 + 14B deep
5. "模型越大越聪明" → 错，MemoryQwen 靠系统和流程

## 训练标签

v0.1, megatrain, m1, model_hardware, topup, doc006
