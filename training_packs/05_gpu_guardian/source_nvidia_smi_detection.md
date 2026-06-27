# nvidia-smi 检测机制

类型:training_source
更新时间:2026-06-27
适用:v0.1.0-dev

## 核心结论
使用 subprocess 调用 nvidia-smi 查询 GPU 和进程信息。nvidia-smi 不可用时返回 available=false，模式自动 normal。

## 正确回答要点
基于上述核心结论。

## 易错点
编造功能、混淆边界、把反例当事实、把未来当现在。

## 标签
v0.1,training,nvidia_smi_detection
