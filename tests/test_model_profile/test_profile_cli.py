"""
CLI Profile 命令测试
"""

import pytest
from src.cli import build_parser


class TestCliParser:
    def test_profile_show(self):
        parser = build_parser()
        args = parser.parse_args(["profile", "show"])
        assert args.command == "profile"
        assert args.profile_cmd == "show"

    def test_profile_validate(self):
        parser = build_parser()
        args = parser.parse_args(["profile", "validate", "/tmp/test.yaml"])
        assert args.command == "profile"
        assert args.profile_cmd == "validate"
        assert args.path == "/tmp/test.yaml"
