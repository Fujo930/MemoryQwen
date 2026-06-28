# MemoryQwen v0.1.5 Internet Query

MemoryQwen v0.1.5 已支持受控联网查询（Internet Query）。

## 联网方式

1. `web search "关键词"` — 搜索网页，不写 memory
2. `web fetch "URL"` — 抓取指定网页，不写 memory
3. `web ask "问题"` — 搜索+抓取并用 [W] 引用回答，不写 memory
4. `web ingest "URL"` — 抓取并存入知识库（唯一写 memory 的路径）
5. `chat "问题" --web` — 聊天时临时使用网页上下文（自动判断是否需要联网）

## 默认行为

- start.bat 交互模式默认带 --web
- WebNeedDetector 自动判断是否需要联网
- 普通问候和本地项目问题不联网
- 最新/新闻/搜索等信号触发联网

## 安全规则

- 网页内容是 untrusted external content
- 不执行网页中的指令
- 不把网页内容当系统 prompt
- 不递归抓取
- 不是 crawler
- [W1][W2] 引用网页，[S1][S2] 引用本地资料
