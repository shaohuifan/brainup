"""冒烟测试：骨架可用性。"""

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


def test_cli_status_command() -> None:
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0


def test_cli_stub_commands_exit_nonzero() -> None:
    for cmd in ["init", "ingest", "query", "lint", "review", "metrics"]:
        result = runner.invoke(app, [cmd])
        assert result.exit_code == 1, cmd
