"""冒烟测试：CLI 入口可用性。"""

from __future__ import annotations

from typer.testing import CliRunner

from brainup import __version__
from brainup.cli import app

runner = CliRunner()


def test_version_export() -> None:
    assert __version__ == "0.1.0"


def test_cli_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_help_lists_all_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for cmd in ("init", "ingest", "query", "lint", "review", "metrics", "mcp", "status"):
        assert cmd in result.output


def test_status_outside_vault_fails(tmp_path) -> None:
    result = runner.invoke(app, ["status", "--vault", str(tmp_path / "nope")])
    assert result.exit_code == 1
