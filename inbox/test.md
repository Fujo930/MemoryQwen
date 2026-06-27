MemoryQwen 是一个本地 AI agent。
它的核心记忆包括 knowledge_store、chat_memory、error_store 和 strategy_store。
默认策略是 7B 常驻，14B 用于深度思考。
用户玩游戏或高 GPU 负载时，未来 GPU Guardian 会让 AI 自动让路。
