# qwen2.5-coder:3b 评估

- 模型: qwen2.5-coder:3b
- 量化: Q4_K_M
- 大小: 1.9GB
- 参数: 3.1B
- 后端: Ollama

## Capability Boundary 测试

| 正确 | 错误 | 模糊 | 污染 |
|------|------|------|------|
| 9 | 5 | 2 | 4 |

通过率: ~64% (9/14 有效)

## 顽固错误

- PDF ingestion hallucination
- GPU Guardian daemon confusion
- source archive / crawler confusion
- embedding 回避/混淆

## 适用场景

- ✅ smoke test / 低资源验证
- ✅ 快速跑通系统
- ✅ CI / 自动化测试
- ❌ 功能边界判断
- ❌ 高准确率要求
