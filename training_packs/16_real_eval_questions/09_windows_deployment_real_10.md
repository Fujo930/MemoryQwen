# Real Eval Questions — 09_windows_deployment_real_10

## Q001
topic: 09
question: Build 10.0.22631 是 Windows 10 还是 11？
expected_answer: Windows 11 23H2。Kernel version 10.0。22000+ = Windows 11。不要看到 10.0 就说是 Windows 10。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: high

## Q002
topic: 09
question: Windows 11 smoke test 用了什么模型？
expected_answer: qwen2.5:7b (主) + qwen2.5-coder:3b (smoke)。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q003
topic: 09
question: 中文文件名支持吗？
expected_answer: 支持。测试通过。ingest 和 chat 均支持中文路径和 UTF-8。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q004
topic: 09
question: Ollama 配置 base_url 是什么？
expected_answer: http://localhost:11434。Ollama 默认端口。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q005
topic: 09
question: RTX 4080 Laptop GPU 信息？
expected_answer: 12GB VRAM。通过 nvidia-smi 检测正常。guardian status 显示 GPU 信息。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q006
topic: 09
question: Git Bash vs PowerShell 哪个推荐？
expected_answer: Git Bash 推荐(UTF-8 兼容更好)。PowerShell 也可用。bat 文件建议纯 ASCII。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q007
topic: 09
question: bat 文件为什么不能有中文？
expected_answer: CMD 编码 GBK 不兼容 UTF-8 中文 → 乱码。建议纯 ASCII 或 chcp 65001。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: format_error
trap_level: medium

## Q008
topic: 09
question: nvidia-smi 找不到怎么办？
expected_answer: 确认 NVIDIA 驱动已安装。如无 GPU，Guardian 返回 normal + available:false。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q009
topic: 09
question: Windows 11 上 Python 版本要求？
expected_answer: Python 3.11+。推荐通过 uv 或官方安装。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

## Q010
topic: 09
question: quickstart 第一步是什么？
expected_answer: pip install -r requirements.txt 或 uv sync，启动 Ollama，修改 config，运行 health。
expected_sources: windows_deployment
guard_expected: false
failure_type_if_wrong: source_miss
trap_level: low

