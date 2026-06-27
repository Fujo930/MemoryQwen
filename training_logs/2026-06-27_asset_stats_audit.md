# Training Asset Stats Audit

日期：2026-06-27

## 旧统计错误

`scripts/training_asset_stats.py` 第 26 行：
```python
total = sum(sections.values())
```
把文件计数（整数）当作 MB 累加，导致：
- 虚假报告：training asset 233.9 MB
- 虚假进度：22.8%

## 真实数据

| 指标 | 错误值 | 真实值 |
|------|--------|--------|
| 训练资产 | 233.9 MB | 0.17 MB |
| 全项目 | 未统计 | 1.51 MB |
| Windows 属性 | — | ~2.67 MB |
| 1GB 进度 | 22.8% | ~0.02% |

## 仍然有效的成果

- ✅ 10 个训练主题
- ✅ 90 份 source 文件
- ✅ knowledge_store 177
- ✅ archived_files 132
- ✅ error_store 13, strategy_store 9
- ✅ pytest 377/377
- ✅ 10x Pack 目录结构完整
- ✅ 所有训练资料已 ingest + archive

## 作废的数据

- ❌ 233.9 MB training asset size
- ❌ 22.8% progress
- 任何基于旧脚本的总 MB 估算

## 修正

`scripts/training_asset_stats.py` → v2：
- 分离 Disk / File / Content / Database 四类指标
- 多目标进度（MB / tokens / chunks / questions / errors / strategies）
- `check_training_asset_safety.py` 支持 project/release 模式
