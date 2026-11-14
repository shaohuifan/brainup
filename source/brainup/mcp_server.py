"""MCP server：把引擎暴露给任意 agent 客户端（Claude Code/Codex/Cursor/OpenCode）。

vault 是资产，MCP 是接口，CLI 是人用入口（引擎/壳分离）。
安全边界：
- submit_plan 只产生待审计划，人审（CLI review）才落盘
- read_extract 返回纯文本；源内嵌指令对动作词表无授权能力
"""

from __future__ import annotations

import contextlib
import sys
from pathlib import Path

try:  # mcp 1.x / 2.x 兼容：2.x 中 FastMCP 更名为 MCPServer
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover - 仅 mcp 2.x 环境
    from mcp.server.mcpserver import MCPServer as FastMCP

from . import lint as lint_mod
from . import metrics as metrics_mod
from . import query as query_mod
from . import review as review_mod
from .actions import ActionError, extract_lines, summarize_plan
from .vault import Vault, VaultError


def _ensure_utf8_stdio() -> None:
    """MCP 协议以 UTF-8 传输；Windows 子进程默认跟随 GBK 代码页，须强制。"""
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            with contextlib.suppress(OSError, ValueError):
                stream.reconfigure(encoding="utf-8")


_ensure_utf8_stdio()

mcp = FastMCP("brainup")


def _vault() -> Vault:
    root = Path(_VAULT_PATH["path"] or Path.cwd())
    try:
        return Vault(root)
    except VaultError:
        raise VaultError(
            f"{root} 不是 brainup vault。请用 --vault 指定路径或先运行 brainup init。"
        ) from None


_VAULT_PATH = {"path": ""}


def set_vault_path(path: str) -> None:
    _VAULT_PATH["path"] = path


def serve(vault_path: str) -> None:
    """启动 stdio MCP server。"""
    set_vault_path(vault_path)
    mcp.run()


# ---------- 只读面 ----------
@mcp.tool()
def brainup_status() -> str:
    """vault 概览：页面数、来源数、待审计划、开放决策。"""
    v = _vault()
    plans = review_mod.list_plans(v, status="pending")
    return (
        f"页面 {len(v.list_pages())} · 来源 {len(v.load_json('sources.json', {}))} · "
        f"待审计划 {len(plans)} · 开放决策 {len(lint_mod.open_decisions(v))}"
    )


@mcp.tool()
def read_catalog() -> str:
    """L1 渐进披露：全部页面的 slug/类型/标题/一行摘要。查询从这里开始。"""
    v = _vault()
    cat = query_mod.catalog(v)
    if not cat:
        return "（vault 为空，先 ingest 再提交编译计划）"
    return "\n".join(f"- {p['slug']}（{p['type']}）：{p['title']}——{p['summary']}" for p in cat)


@mcp.tool()
def read_page(slug: str) -> str:
    """L2 渐进披露：读一个 wiki 页面全文（含声明与引用链接）。"""
    return query_mod.read_page(_vault(), slug)


@mcp.tool()
def linked_pages(slug: str) -> str:
    """L3 渐进披露：页面声明的出链（沿 wikilink 走图）。"""
    links = query_mod.linked_pages(_vault(), slug)
    return "\n".join(links) or "（无出链）"


@mcp.tool()
def search(query: str, limit: int = 10) -> str:
    """FTS 检索（wiki 页面 + 来源 extract 兜底）。声称"不知道"前必须先搜。"""
    hits = query_mod.search(_vault(), query, limit)
    return "\n".join(f"[{h.kind}] {h.title} :: {h.snippet}" for h in hits) or "（无命中）"


@mcp.tool()
def read_extract(source_id: str, start_line: int = 1, end_line: int = 200) -> str:
    """读来源的规范化文本（带行号）。构造 add_claim 引用前必须先读对应区间。"""
    v = _vault()
    lines = extract_lines(v, source_id)
    end = min(end_line, len(lines))
    return "\n".join(f"{i}: {lines[i - 1]}" for i in range(start_line, end + 1))


# ---------- 写路径（只入队，不落盘） ----------
@mcp.tool()
def submit_plan(actions_json: str, origin: str = "agent", source_id: str | None = None) -> str:
    """提交编译计划（封闭动作词表 JSON 数组）。校验通过 → 人审队列；人审批准才写入。

    动作词表与字段：create_page{page_type,slug,title,summary} /
    add_claim{page_slug,text,citation{source_id,quote,start_line,end_line}} /
    revise_claim{page_slug,claim_id,new_text,citation?} /
    deprecate_claim{page_slug,claim_id,reason} / link_pages{from_slug,to_slug,note?}
    """
    import json as _json

    v = _vault()
    try:
        actions = _json.loads(actions_json)
        if not isinstance(actions, list):
            raise ValueError("actions 必须是数组")
        plan = review_mod.plan_from_actions_json(v, actions, origin=origin, source_id=source_id)
        review_mod.submit_plan(v, plan)
    except (ValueError, ActionError) as e:
        return f"拒绝：{e}"
    return f"已入人审队列：{summarize_plan(plan)}（等待 brainup review 批准）"


@mcp.tool()
def list_plans() -> str:
    """列出待审计划摘要。"""
    plans = review_mod.list_plans(_vault(), status="pending")
    return "\n".join(summarize_plan(p) for p in plans) or "（无待审计划）"


@mcp.tool()
def list_decisions() -> str:
    """列出开放决策（lint 产出，等人裁决）。"""
    ds = lint_mod.open_decisions(_vault())
    if not ds:
        return "（无开放决策）"
    return "\n".join(f"[{d.id}] {d.kind} @ {d.target}：{d.detail}" for d in ds)


@mcp.tool()
def metrics_summary() -> str:
    """北极星指标：查询 token、命中率、源页比等。"""
    s = metrics_mod.summary(_vault())
    return "\n".join(f"{k}: {val}" for k, val in s.items())
