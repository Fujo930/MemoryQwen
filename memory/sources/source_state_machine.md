# 状态机规则

类型:training_source
更新时间:2026-06-27
适用:v0.1.0-dev

## 核心结论
pending→running, running↔paused, running→completed/failed, pending/running/paused→cancelled。completed/failed/cancelled 是终态。

## 正确回答要点
基于上述核心结论。

## 易错点
编造功能、混淆边界、把反例当事实、把未来当现在。

## 标签
v0.1,training,state_machine
