"""CLI 入口：brainup（升级大脑）。

v0.1 骨架阶段：仅 status 可用，其余命令为规划中的占位。
命令面依据 design/design-proposal-v0.1.md 第 3.1 节。
"""

import contextlib
import sys

import typer

from brainup import __version__


def _ensure_utf8_stdio() -> None:
    """中文优先：强制 UTF-8 输出。

    PEP 686（Python 3.15 才默认 UTF-8 模式）之前，Windows 上 Python 的 stdio
    跟随系统代码页（中文系统为 GBK），管道/终端重定向时会把中文写坏。
    本工具面向中文用户，统一以 UTF-8 输出；旧版 conhost 用户需 `chcp 65001`。
    """
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            with contextlib.suppress(OSError, ValueError):
                stream.reconfigure(encoding="utf-8")


_ensure_utf8_stdio()

app = typer.Typer(
    name="brainup",
    help="升级大脑 — 读书人的复利知识库引擎（LLM Wiki 模式，CLI + MCP）。",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """显示版本。"""
    typer.echo(f"brainup {__version__}")


@app.command()
def status() -> None:
    """显示当前 vault 状态。"""
    typer.echo("brainup v0.1.0 · 骨架阶段，尚未支持 vault 操作")
    typer.echo("规划命令面：init / ingest / query / lint / review / metrics（见 design/）")


def _not_implemented(name: str) -> None:
    typer.echo(f"`brainup {name}` 尚未实现（v0.1 骨架阶段），见 design/design-proposal-v0.1.md")
    raise typer.Exit(code=1)


@app.command()
def init() -> None:
    """脚手架一个 vault（中文默认，OKF v0.2 兼容）。"""
    _not_implemented("init")


@app.command()
def ingest() -> None:
    """摄入来源（PDF/EPUB/MD/URL）→ 编译计划 → 人审队列 → 原子应用。"""
    _not_implemented("ingest")


@app.command()
def query() -> None:
    """三级渐进披露查询 → FTS 兜底 → 引用作答。"""
    _not_implemented("query")


@app.command()
def lint() -> None:
    """健康扫描 → 决策队列（分诊 inbox，绝非自动修复）。"""
    _not_implemented("lint")


@app.command()
def review() -> None:
    """审批待定动作（action 粒度）。"""
    _not_implemented("review")


@app.command()
def metrics() -> None:
    """北极星指标：每查询 token / 已编译知识命中率 / 决策队列吞吐 / 源页比。"""
    _not_implemented("metrics")


if __name__ == "__main__":
    app()
