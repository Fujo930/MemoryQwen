# 记忆备份

## ⚠️ 最重要的事情

**模型可以重新下载。memory 不能丢。**

MemoryQwen 的所有长期记忆、对话记录、错误经验、策略都存储在本地文件中。丢失这些文件意味着丢失所有 AI 的"记忆"。

## 需要备份的文件夹

```
MemoryQwen/
├── memory/              ← 最重要！一次备份全带走
│   ├── sources/         ← v0.1.0+：已导入资料的原文归档
│   │   └── *.md, *.txt  ← 原始资料文件
│   ├── memoryqwen.db    ← 核心数据库（knowledge、chat、error、strategy）
│   └── tasks.db         ← 任务状态
├── config/              ← 你的配置
│   ├── default.yaml
│   └── model_profiles/  ← 模型 profile
├── inbox/               ← 投喂入口（建议一起备份）
└── backup/              ← 自动备份目录
```

> **v0.1.0-dev 起：** 导入成功的 `.md/.txt` 会自动归档到 `memory/sources/`。
> inbox/ 是投喂入口，memory/sources/ 是长期原文归档。
> 备份 `memory/` 即可同时保留 SQLite 记忆、任务状态和已导入的原始资料。

## Windows 备份命令

```bash
# 创建带日期的备份
xcopy memory memory_backup_%date:~0,10% /E /I

# 或使用 robocopy
robocopy memory backup\memory_%date:~0,10% /E

# 备份到外部硬盘
robocopy memory D:\Backups\MemoryQwen\memory /E
```

## 恢复

```bash
# 恢复 memory 文件夹
xcopy backup\memory_backup_2024-01-15\* memory\ /E /Y
```

## 不需要备份的

- `__pycache__/` (Python 缓存)
- `.pytest_cache/` (测试缓存)
- `models/` (模型文件太重，可以重新下载)
- `logs/` (日志文件)

## 建议

1. 每天备份一次 `memory/`
2. 修改配置前备份 `config/`
3. 重大操作前做一次完整备份
4. 考虑版本控制: `git init && git add config/ && git commit`
