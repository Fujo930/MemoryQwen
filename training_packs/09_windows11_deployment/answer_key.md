# 09_windows11_deployment Answer Key

- Windows 11 23H2 smoke test: Build 10.0.22631。health, ingest, chat, correct, guardian, task 全部通过。
- Build 10.0.22631 是 Windows 11: Kernel version 10.0。22000+ 就是 Windows 11。不要因为看到 10.0 就觉得是 Windows 10。
- Ollama OpenAI-compatible 配置: provider: ollama, base_url: http://localhost:11434。model 名必须和 ollama list 一致。
- qwen2.5:7b 是默认模型: Q4_K_M 4.7GB。v0.1 默认推荐。capability boundary 91%。
- qwen2.5-coder:3b smoke test: 1.9GB Q4_K_M。适合快速验证。capability boundary 64%。API key 不需要。
- 中文路径 / UTF-8 支持: 中文文件名已通过。ingest 和 chat 均支持。不出现乱码。Git Bash 推荐。
- 终端支持: Git Bash(推荐,UTF-8) / PowerShell 均可用。bat 文件建议纯 ASCII。
- nvidia-smi RTX 4080 检测: RTX 4080 Laptop GPU 12GB 检测正常。guardian status/json 正常。
- 常见 Windows 问题: 编码乱码→Git Bash。模块找不到→cd项目根目录。SQLite lock→关闭其他进程。nvidia-smi不可用→确认驱动。bat闪退→检查Python路径。