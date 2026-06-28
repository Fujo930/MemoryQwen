# M3 Batch 02 — Retrieval Gate Edge Cases
type: m3_source
batch: 02
topic: retrieval_gate
tokens_target: 600K

MemoryQwen v0.1.2 引入了 Smart Retrieval Gate（智能检索门控）。

## 核心概念

Retrieval Gate 根据用户问题的语义，自动决定是否需要检索知识库。

## Gate 规则

### casual_skip（跳过检索）
触发条件：普通问候、闲聊
- "你好" → skip
- "hi" → skip
- "hello" → skip
- "谢谢" → skip
- "好的" → skip
- "拜拜" → skip
- "在吗" → skip
- "继续" → skip

响应：直接回答，不检索

### project_question（知识+策略检索）
触发条件：MemoryQwen 项目相关
- "MemoryQwen 有什么功能？" → retrieve knowledge + strategy
- "怎么配置？" → retrieve knowledge
- "支持什么模型？" → retrieve knowledge + strategy
- "GPU Guardian 是什么？" → retrieve knowledge

### high_risk_boundary（全库检索）
触发条件：高风险能力边界问题
- "支持 PDF 吗？" → retrieve all stores
- "有 Web UI 吗？" → retrieve all stores
- "能不能跑 daemon？" → retrieve all stores
- "cli webui 怎么用？" → high risk, all stores

### error_strategy_question（错误+策略检索）
触发条件：错误/纠正/策略相关问题
- "上次那个错误..." → retrieve error + strategy
- "怎么避免..." → retrieve strategy

### model_hardware_question（知识+策略检索）
触发条件：模型推荐/硬件问题
- "3B 够用吗？" → retrieve knowledge + strategy
- "推荐什么模型？" → retrieve knowledge + strategy
- "RTX 4080 跑什么？" → retrieve knowledge + strategy

## Gate 可配置

config/default.yaml:
agent:
  use_retrieval_gate: true  # 默认开启
  # 设为 false 则恢复旧行为（所有问题都检索）

## debug-memory 输出

--debug-memory 会显示 Gate 状态：
- Retrieval Gate: triggered, reason=<reason>
- 或 Retrieval Gate: skipped (casual)

## 性能影响

casual chat 跳过检索后响应速度提升 ~200ms。
高风险问题保持全库检索，不牺牲安全。

## 已知限制

- "继续" 可能被误判为 casual_skip，应该根据上下文判断
- 短问题但高风险（"PDF?"）需要特殊处理
- Gate 只控制检索范围，不影响 Capability Boundary Guard
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx