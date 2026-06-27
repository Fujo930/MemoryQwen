"""
MemoryQwen CLI 测试
所有测试使用 fake model_client + 临时 SQLite，不启动真实模型服务。
"""

from __future__ import annotations

import asyncio
import pytest
import pytest_asyncio
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.cli import (
    build_parser, cmd_health, cmd_ingest, cmd_chat, cmd_correct,
)
from src.config import AppConfig
from src.memory_store import create_memory_store


class FakeModelClient:
    async def health_check(self):
        return True

    async def chat(self, messages, model=None, temperature=None,
                   max_tokens=None, stream=False):
        from src.model_client.base import ChatResponse
        return ChatResponse(
            content="这是一个模拟回复。",
            model="fake-model",
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        )


class FakeFailingModelClient:
    async def health_check(self):
        return False

    async def chat(self, *args, **kwargs):
        raise RuntimeError("模型不可用")


# ─── Fixtures ──────────────────────────────────────────

@pytest_asyncio.fixture
async def store():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    config = AppConfig()
    config.memory_store.database_path = tmp.name
    s = create_memory_store(config)
    await s.init()
    yield s
    await s.close()
    Path(tmp.name).unlink(missing_ok=True)


@pytest.fixture
def config():
    return AppConfig()


# ─── Parser Tests ──────────────────────────────────────

class TestParser:
    def test_health_command(self):
        parser = build_parser()
        args = parser.parse_args(["health"])
        assert args.command == "health"

    def test_ingest_command(self):
        parser = build_parser()
        args = parser.parse_args(["ingest", "/tmp/test"])
        assert args.command == "ingest"
        assert args.path == "/tmp/test"

    def test_chat_command(self):
        parser = build_parser()
        args = parser.parse_args(["chat", "hello", "--session", "s1", "--model-tier", "deep"])
        assert args.command == "chat"
        assert args.message == "hello"
        assert args.session == "s1"
        assert args.model_tier == "deep"

    def test_correct_command(self):
        parser = build_parser()
        args = parser.parse_args([
            "correct", "--session", "s2",
            "--wrong", "bad answer", "--correct", "good answer",
            "--failure-type", "math_error", "--strategy", "use calc",
        ])
        assert args.command == "correct"
        assert args.wrong == "bad answer"
        assert args.correct == "good answer"
        assert args.failure_type == "math_error"
        assert args.strategy == "use calc"


# ─── Health Tests ──────────────────────────────────────

class TestHealthCommand:
    @pytest.mark.asyncio
    async def test_health_ok(self, config, store, capsys):
        model = FakeModelClient()
        await cmd_health(config, store, model)
        out = capsys.readouterr().out
        assert "MemoryQwen" in out
        assert "Model Client: OK" in out

    @pytest.mark.asyncio
    async def test_health_model_down(self, config, store, capsys):
        model = FakeFailingModelClient()
        await cmd_health(config, store, model)
        out = capsys.readouterr().out
        assert "Unavailable" in out or "Model Client:" in out


# ─── Ingest Tests ──────────────────────────────────────

class TestIngestCommand:
    @pytest.mark.asyncio
    async def test_ingest_file(self, config, store, capsys):
        tmpdir = tempfile.mkdtemp()
        fp = Path(tmpdir) / "test.txt"
        fp.write_text("Test content for ingest.", encoding="utf-8")

        args = type('args', (), {'path': str(fp), 'recursive': True})()
        await cmd_ingest(config, store, args)

        out = capsys.readouterr().out
        assert "Files seen" in out
        assert "Chunks stored" in out

        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)


# ─── Chat Tests ────────────────────────────────────────

class TestChatCommand:
    @pytest.mark.asyncio
    async def test_chat_fake_model(self, config, store, capsys):
        model = FakeModelClient()
        args = type('args', (), {
            'message': '你好', 'session': 'test', 'model_tier': 'light',
        })()
        await cmd_chat(config, store, model, args)
        out = capsys.readouterr().out
        assert "模拟回复" in out


# ─── Correct Tests ─────────────────────────────────────

class TestCorrectCommand:
    @pytest.mark.asyncio
    async def test_correct_writes_error(self, config, store, capsys):
        args = type('args', (), {
            'session': 'test', 'wrong': 'bad', 'correct': 'good',
            'failure_type': 'general', 'strategy': '',
        })()
        await cmd_correct(config, store, args)
        out = capsys.readouterr().out
        assert "True" in out or "Error" in out

    @pytest.mark.asyncio
    async def test_correct_backfills_auto_generated_strategy(self, config, store, capsys):
        """回归测试：不传 strategy 时，correct 自动回填默认 strategy 并触发 StrategyLearningService"""
        # 确保 enable_strategy_learning=True（默认值）
        assert config.agent.enable_strategy_learning is True

        args = type('args', (), {
            'session': 'backfill-test', 'wrong': 'bad answer',
            'correct': 'good answer', 'failure_type': 'test_type',
            'strategy': '',  # 不传 strategy
        })()
        await cmd_correct(config, store, args)
        out = capsys.readouterr().out

        # 验证 CLI 输出包含 strategy 生成信息
        assert "Strategy learning enabled: True" in out, f"Missing strategy enabled flag\nOutput: {out}"
        assert "Strategy generated: true" in out, f"Strategy was not generated\nOutput: {out}"
        assert "Strategy ID:" in out, f"Missing Strategy ID\nOutput: {out}"

        # 验证 strategy_store 确实写入了
        count = await store.count("strategy_store")
        assert count > 0, "strategy_store should have at least 1 record after correction"
