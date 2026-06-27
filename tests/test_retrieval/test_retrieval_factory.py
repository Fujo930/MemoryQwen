"""
Retriever 工厂测试
"""

from src.retrieval.factory import create_keyword_retriever
from src.retrieval.keyword import KeywordRetriever


class MockConfig:
    class Memory:
        class RetrievalKeyword:
            enabled = True
            default_top_k = 5
            min_score = 0.0
            tokenizer = "simple"
        retrieval_keyword = RetrievalKeyword()
        class Retrieval:
            top_k = 5
        retrieval = Retrieval()
    memory = Memory()
    memory_store = type('obj', (), {'backend': 'sqlite', 'database_path': ':memory:'})()

class MockStore:
    async def list(self, table, limit=100000):
        return []


def test_create_keyword_retriever():
    r = create_keyword_retriever(MockConfig(), MockStore())
    assert isinstance(r, KeywordRetriever)
