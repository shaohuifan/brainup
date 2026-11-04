"""CLI 入口：brainup（升级大脑）。

中文优先：强制 UTF-8 stdio（PEP 686 之前 Windows 默认跟随系统代码页）。
"""

from __future__ import annotations

import contextlib
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from brainup import __version__
from brainup import lint as lint_mod
from brainup import metrics as metrics_mod
from brainup import query as query_mod
from brainup import review as review_mod
from brainup.actions import ActionError, summarize_plan
from brainup.vault import Vault, VaultError

console = Console()


def _ensure_utf8_stdio() -> None:
    """中文优先：强制 UTF-8 输出（旧版 conhost 需 `chcp 65001`）。"""
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


_VAULT_OPTION = typer.Option(
    None,
    "--vault",
    "-v",
    envvar="BRAINUP_VAULT",
    help="vault 路径（默认从当前目录向上查找）",
)


def _open_vault(vault_arg: str | None) -> Vault:
    try:
        if vault_arg:
            return Vault(Path(vault_arg))
        return Vault.find()
    except VaultError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1) from e


@app.command()
def version() -> None:
    """显示版本。"""
    typer.echo(f"brainup {__version__}（升级大脑）")


@app.command()
def status(vault: str | None = _VAULT_OPTION) -> None:
    """显示 vault 状态：页面、来源、待审计划、开放决策、git 状态。"""
    v = _open_vault(vault)
    plans = review_mod.list_plans(v, status="pending")
    stats = lint_mod.lint_stats(v)
    table = Table(title=f"vault · {v.root}")
    table.add_column("项")
    table.add_column("值", justify="right")
    for label, key in (
        ("页面", "pages"),
        ("声明", "claims"),
        ("来源", "sources"),
        ("待审计划", None),
        ("开放决策", "open"),
    ):
        table.add_row(label, str(len(plans) if key is None else stats[key]))
    console.print(table)
    if plans:
        console.print("待审计划：")
        for p in plans:
            console.print(f"  {summarize_plan(p)}")


@app.command()
def init(
    path: Path = typer.Argument(Path("."), help="vault 目录"),
    language: str = typer.Option("zh", help="内容语言"),
) -> None:
    """脚手架一个 vault（三层布局 + git + 中文 AGENTS.md 规约）。"""
    try:
        v = Vault.init(path, language=language)
    except VaultError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1) from e
    console.print(f"[green]✓[/green] vault 已初始化：{v.root}")
    console.print("  raw/ 放来源 · brainup ingest 摄入 · brainup review 审批 · Obsidian 打开查看")


@app.command()
def ingest(
    sources: list[Path] = typer.Argument(None, help="本地文件（PDF/EPUB/MD/TXT/HTML）"),
    vault: str | None = _VAULT_OPTION,
    url: list[str] = typer.Option(None, "--url", "-u", help="抓取 URL（可多次）"),
    auto: bool = typer.Option(False, "--auto", help="配置了 LLM 时自动生成编译计划（仍需人审）"),
) -> None:
    """摄入来源：解析 → raw 归档 → extract 规范化 → FTS 索引。幂等（内容寻址）。"""
    from brainup import compile as compile_mod
    from brainup import ingest as ingest_mod
    from brainup.llm import load_llm

    v = _open_vault(vault)
    if not sources and not url:
        console.print("[red]请提供文件或 --url[/red]")
        raise typer.Exit(code=1)
    for src in sources or []:
        if not src.is_file():
            console.print(f"[red]文件不存在：{src}[/red]")
            raise typer.Exit(code=1)
        try:
            rec = ingest_mod.ingest_file(v, src)
            console.print(
                f"[green]✓[/green] {src.name} → {rec.source_id}（{rec.parser}，{rec.lines} 行）"
            )
            metrics_mod.log_event(v, "ingest", {"source_id": rec.source_id})
        except ActionError as e:
            console.print(f"[red]{src.name}：{e}[/red]")
    for u in url or []:
        try:
            rec = ingest_mod.ingest_url(v, u)
            console.print(f"[green]✓[/green] {u} → {rec.source_id}（{rec.parser}，{rec.lines} 行）")
            metrics_mod.log_event(v, "ingest", {"source_id": rec.source_id, "url": u})
        except Exception as e:  # noqa: BLE001 - 网络错误统一呈现
            console.print(f"[red]{u}：{e}[/red]")
    if auto:
        llm = load_llm(v)
        if llm is None:
            console.print(
                "[yellow]未配置 LLM（.kb/config.toml provider=none）。"
                "已归档来源；可让 agent 经 MCP submit_plan 提交编译计划。[/yellow]"
            )
            return
        registry: dict[str, dict] = v.load_json("sources.json", {})
        for sid, rec in registry.items():
            if rec.get("compiled"):
                continue
            try:
                plan = compile_mod.build_plan_for_source(v, sid, llm)
                review_mod.submit_plan(v, plan, validate=False)  # compile 已带校验信息
                rec["compiled"] = True
                console.print(f"[green]✓[/green] 编译计划已入队：{summarize_plan(plan)}")
            except Exception as e:  # noqa: BLE001
                console.print(f"[red]编译失败 {sid}：{e}[/red]")
        v.save_json("sources.json", registry)


@app.command()
def query(
    question: str = typer.Argument(..., help="问题"),
    vault: str | None = _VAULT_OPTION,
    pack: bool = typer.Option(False, "--pack", help="只输出检索包（不用 LLM）"),
) -> None:
    """查询：三级渐进披露 + FTS 兜底。未配置 LLM 时自动输出检索包。"""
    from brainup.llm import LLMError, load_llm

    v = _open_vault(vault)
    llm = None if pack else load_llm(v)
    if llm is None:
        console.print(query_mod.retrieval_pack(v, question))
        metrics_mod.log_event(v, "query", {"mode": "pack", "pages_read": []})
        return
    try:
        text, m = query_mod.answer(v, question, llm)
    except LLMError as e:
        console.print(f"[red]LLM 调用失败：{e}[/red]\n回落到检索包：")
        console.print(query_mod.retrieval_pack(v, question))
        raise typer.Exit(code=1) from e
    console.print(text)
    console.print(
        f"[dim]（读 {len(m.get('pages_read', []))} 页 · {m['total_tokens']} tokens）[/dim]"
    )
    metrics_mod.log_event(v, "query", {"mode": "llm", **m})


@app.command()
def lint(vault: str | None = _VAULT_OPTION) -> None:
    """健康扫描 → 决策队列（每项待人裁决，绝不自动修复）。"""
    v = _open_vault(vault)
    decisions = lint_mod.run_lint(v)
    stats = lint_mod.lint_stats(v)
    console.print(
        f"扫描 {stats['pages']} 页 / {stats['claims']} 条声明"
        f" → 开放决策 [bold]{len(decisions)}[/bold]"
    )
    for d in decisions:
        console.print(f"  [yellow][{d.id}][/yellow] {d.kind} @ {d.target}：{d.detail}")
        console.print(f"    证据：{d.evidence[:100]}")
    if not decisions:
        console.print("[green]✓ 队列干净[/green]")


@app.command()
def review(
    plan_id: str = typer.Argument(None, help="计划 ID（省略则列出队列）"),
    vault: str | None = _VAULT_OPTION,
    approve: bool = typer.Option(False, "--approve", help="批准并原子应用该计划"),
    reject: str = typer.Option(None, "--reject", help="拒绝该计划（附原因）"),
    resolve: str = typer.Option(None, "--resolve", help="裁决决策为已处理（附说明）"),
    dismiss: str = typer.Option(None, "--dismiss", help="裁决决策为不处理（附说明）"),
) -> None:
    """人审入口：批准/拒绝计划，裁决 lint 决策。"""
    v = _open_vault(vault)
    if resolve or dismiss:
        note = resolve or dismiss
        status = "resolved" if resolve else "dismissed"
        try:
            lint_mod.adjudicate(v, plan_id or "", status, note)  # type: ignore[arg-type]
        except KeyError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(code=1) from e
        console.print(f"[green]✓[/green] 决策 {plan_id} → {status}")
        return
    if plan_id and approve:
        try:
            review_mod.approve_plan(v, plan_id)
        except ActionError as e:
            console.print(f"[red]应用失败（零写入）：{e}[/red]")
            raise typer.Exit(code=1) from e
        console.print(f"[green]✓[/green] 计划 {plan_id} 已批准并写入（单次 git commit）")
        return
    if plan_id and reject:
        review_mod.reject_plan(v, plan_id, reject)
        console.print(f"[yellow]✗[/yellow] 计划 {plan_id} 已拒绝：{reject}")
        return
    if plan_id:
        from brainup.actions import dump_plan

        try:
            console.print(dump_plan(review_mod.get_plan(v, plan_id)))
        except ActionError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(code=1) from e
        return
    # 无参数：总览
    summary = review_mod.review_summary(v)
    for line in summary["pending_plans"]:  # type: ignore[union-attr]
        console.print(f"[yellow]待审[/yellow] {line}")
    for d in summary["open_decisions"]:  # type: ignore[union-attr]
        console.print(
            f"[yellow]决策[/yellow] [{d['id']}] {d['kind']}"
            f" @ {d['target']}：{d['detail']}"
        )
    for line in summary["recent_failed"]:  # type: ignore[union-attr]
        console.print(f"[red]失败[/red] {line}")


@app.command()
def metrics(vault: str | None = _VAULT_OPTION) -> None:
    """北极星指标：查询 token / 命中率 / 源页比 / 队列状态。"""
    v = _open_vault(vault)
    s = metrics_mod.summary(v)
    ratio = s["source_page_ratio"]
    table = Table(title="指标")
    table.add_column("指标")
    table.add_column("值", justify="right")
    for k, val in s.items():
        table.add_row(k, str(val))
    console.print(table)
    if ratio is not None and ratio < 1:
        console.print(
            "[red]⚠ 源/编译页比率 < 1：写快于读，wiki 在空转（无源页是未来的谎言）[/red]"
        )


@app.command()
def mcp(
    vault: str | None = _VAULT_OPTION,
) -> None:
    """启动 MCP server（stdio），供 Claude Code/Codex/Cursor/OpenCode 接入。"""
    from brainup import mcp_server

    v = _open_vault(vault)
    console.print(f"[dim]brainup MCP server · vault={v.root}[/dim]", file=sys.stderr)
    mcp_server.serve(str(v.root))


if __name__ == "__main__":
    app()
