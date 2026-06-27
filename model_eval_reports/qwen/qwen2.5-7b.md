# qwen2.5:7b 评估

- 模型: qwen2.5:7b
- 量化: Q4_K_M
- 大小: 4.7GB
- 参数: 7.6B
- 后端: Ollama

## Capability Boundary 测试

| 正确 | 错误 |
|------|------|
| 9-10 | 0-1 |

通过率: ~91%

## 改进

- ✅ PDF hallucination 修复
- ✅ Guardian daemon 正确区分
- ✅ embedding 正确回答不支持
- ✅ crawler 正确区分
- ✅ 引用来源正确
- ✅ 使用策略指导

## 推荐

✅ v0.1 默认常驻模型
