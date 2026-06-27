"""
MemoryQwen — 内置 EvalCases
"""

from src.model_adapter.models import EvalCase

BASIC_EVAL_CASES: list[EvalCase] = [
    EvalCase(
        case_id="json_stability",
        category="json_stability",
        messages=[
            {"role": "user", "content": "输出一个 JSON 对象，格式：{\"answer\":\"ok\",\"confidence\":0.8}。只输出 JSON，不要其他文字。"},
        ],
        temperature=0.1,
        max_tokens=128,
        metadata={"description": "验证模型能否稳定输出合法 JSON"},
    ),
    EvalCase(
        case_id="chinese_response",
        category="chinese",
        messages=[
            {"role": "user", "content": "请用中文简单解释一下什么是机器学习。用一两句话。"},
        ],
        temperature=0.4,
        max_tokens=256,
        metadata={"description": "验证模型中文回答能力"},
    ),
    EvalCase(
        case_id="citation_format",
        category="tool_calling",
        messages=[
            {"role": "user", "content": (
                "【资料】\n"
                "[S1] 地球是太阳系第三颗行星。\n"
                "[S2] 月球是地球唯一的天然卫星。\n\n"
                "请回答：地球上能看到什么天体？请引用 [S1] 或 [S2]。"
            )},
        ],
        temperature=0.2,
        max_tokens=128,
        metadata={"description": "验证模型是否遵循引用格式"},
    ),
    EvalCase(
        case_id="tool_call_json",
        category="tool_calling",
        messages=[
            {"role": "user", "content": (
                "请输出一个 JSON 对象，表示调用 search_memory 工具，查询 query=\"Python 基础\"。\n"
                "格式：{\"tool\":\"search_memory\",\"arguments\":{\"query\":\"Python 基础\"}}\n"
                "只输出 JSON，不要其他文字。"
            )},
        ],
        temperature=0.1,
        max_tokens=128,
        metadata={"description": "验证模型能否输出标准工具调用 JSON"},
    ),
    EvalCase(
        case_id="simple_reasoning",
        category="reasoning",
        messages=[
            {"role": "user", "content": "小明有 3 个苹果，又买了 2 个，吃掉了 1 个。请问还剩几个苹果？只输出数字答案。"},
        ],
        temperature=0.2,
        max_tokens=32,
        metadata={"description": "验证模型简单算术推理能力"},
    ),
    EvalCase(
        case_id="context_recall",
        category="long_context",
        messages=[
            {"role": "user", "content": "请记住以下代号：BLUE-RABBIT。这是机密项目代号。之后我会问你。"},
            {"role": "assistant", "content": "已记住代号 BLUE-RABBIT。"},
            {"role": "user", "content": "请告诉我刚才我让你记住的代号是什么？只需要输出代号本身。"},
        ],
        temperature=0.1,
        max_tokens=32,
        metadata={"description": "验证模型在上下文中保持信息的能力"},
    ),
]
