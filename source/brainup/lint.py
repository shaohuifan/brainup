"""lint：健康检查 → 决策队列（P1）。

调研结论（research/raw/deep-dive-failure-modes.md §1.2，10 周遥测）：
- lint 只管检测，**修复是人的决策**（自动修复 185 条修好 0 条）
- 绝不自动建 stub 清零死链（移动数字不移动问题）
- 每条发现 = 一个待分诊决策：有稳定 key、有状态、有逐字证据，可批量裁决
- 监控监控者：lint 自报扫描基数（扫了几个页面/几条声明）
"""

from __future__ import annotations

import hashlib
import re
from typing import Literal

from pydantic import BaseModel, Field

from .vault import Vault, utcnow

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
_CLAIM_RE = re.compile(r"^- \[(C\d+)\] (.+)$", re.MULTILINE)
_CITE_RE = re.compile(r"\[\(源\)\]\(\.\./\.kb/extract/([0-9a-f]+)\.md#L(\d+)(?:-L(\d+))?\)")


class Decision(BaseModel):
    """一条待分诊决策。"""

    id: str
    kind: Literal[
        "broken_wikilink",
        "orphan_page",
        "claim_drift",
        "citation_unverifiable",
        "missing_citation",
        "page_missing",
    ]
    target: str
    detail: str = ""
    evidence: str = Field(description="逐字证据（页面/extract 原文行）")
    status: Literal["open", "resolved", "dismissed"] = "open"
    created_at: str
    resolved_at: str | None = None
    note: str | None = None


def _key(kind: str, target: str, detail: str) -> str:
    return hashlib.sha1(f"{kind}|{target}|{detail}".encode()).hexdigest()[:10]


def _make(kind: str, target: str, detail: str, evidence: str) -> Decision:
    return Decision(
        id=_key(kind, target, detail),
        kind=kind,
        target=target,
        detail=detail,
        evidence=evidence.strip()[:300],
        created_at=utcnow(),
    )


def _find_bullet(body: list[str], cid: str) -> str | None:
    prefix = f"- [{cid}] "
    for line in body:
        if line.startswith(prefix):
            return line
    return None


def _bullet_text(bullet: str) -> str:
    m = _CLAIM_RE.match(bullet)
    return m.group(2).strip() if m else bullet


# ---------- 检查器 ----------
def check_broken_wikilinks(vault: Vault) -> list[Decision]:
    out: list[Decision] = []
    for meta in vault.list_pages():
        page = vault.read_page(meta["slug"])
        for line in page.body:
            for m in _WIKILINK_RE.finditer(line):
                target = m.group(1).strip()
                if target and not vault.page_exists(target):
                    out.append(_make("broken_wikilink", meta["slug"], target, line))
    return out


def check_orphan_pages(vault: Vault) -> list[Decision]:
    """无入链页面。注意：搜索可发现的孤儿未必是问题（调研 2.1），交人裁决。"""
    inbound: set[str] = set()
    for meta in vault.list_pages():
        page = vault.read_page(meta["slug"])
        for m in _WIKILINK_RE.finditer("\n".join(page.body)):
            inbound.add(m.group(1).strip())
    return [
        _make("orphan_page", meta["slug"], "无入链", meta["summary"])
        for meta in vault.list_pages()
        if meta["slug"] not in inbound
    ]


def check_claims(vault: Vault) -> list[Decision]:
    """声明完整性：注册表 vs 页面文本（漂移/缺引用/引用失核）。"""
    from .actions import ActionError, Citation, verify_citation  # 局部导入避免环

    out: list[Decision] = []
    registry: dict[str, dict] = vault.load_json("claims.json", {})
    for _key_str, rec in registry.items():
        slug, cid = rec["page"], rec["claim_id"]
        if not vault.page_exists(slug):
            out.append(
                _make("page_missing", slug, f"{cid} 的注册页面消失", str(rec.get("quote", "")))
            )
            continue
        page = vault.read_page(slug)
        bullet = _find_bullet(page.body, cid)
        if bullet is None:
            out.append(
                _make("claim_drift", slug, f"{cid} 在页面上找不到", str(rec.get("quote", "")))
            )
            continue
        if not _CITE_RE.search(bullet):
            out.append(_make("missing_citation", slug, f"{cid} 缺引用链接", bullet))
        # 文本漂移：注册 hash vs 当前文本（弃用项跳过——~~包裹改变了文本）
        if rec.get("status") == "active":
            h = hashlib.sha256(_bullet_text(bullet).encode()).hexdigest()[:16]
            if h != rec.get("text_hash"):
                out.append(
                    _make("claim_drift", slug, f"{cid} 页面文本与注册表不符（人工编辑？）", bullet)
                )
        # 引用复核：注册表 quote 回溯源字节（证据抽验）
        if rec.get("quote") and rec.get("source_id"):
            try:
                verify_citation(
                    vault,
                    Citation(
                        source_id=rec["source_id"],
                        quote=rec["quote"],
                        start_line=int(rec.get("start_line", 1)),
                        end_line=int(rec.get("end_line", 1)),
                    ),
                )
            except (ActionError, ValueError):
                out.append(_make("citation_unverifiable", slug, f"{cid} 引用不再可核验", bullet))
    return out


# ---------- 队列 ----------
def run_lint(vault: Vault) -> list[Decision]:
    """执行全部检查，合并进决策队列（open 项保持 open，幂等）。"""
    fresh = [
        *check_broken_wikilinks(vault),
        *check_orphan_pages(vault),
        *check_claims(vault),
    ]
    queue: dict[str, dict] = vault.load_json("decisions.json", {})
    for d in fresh:
        existing = queue.get(d.id)
        if existing is None:
            queue[d.id] = d.model_dump()
        elif existing["status"] == "open":
            queue[d.id]["evidence"] = d.evidence  # 证据更新，状态保留
        # resolved/dismissed：不复活——人已裁决，重扫描不得推翻
    vault.save_json("decisions.json", queue)
    scanned_pages = len(vault.list_pages())
    registry: dict[str, dict] = vault.load_json("claims.json", {})
    vault.git_commit(
        f"lint: 扫描 {scanned_pages} 页 / {len(registry)} 条声明 → {len(fresh)} 项发现"
    )
    return open_decisions(vault)


def adjudicate(
    vault: Vault, decision_id: str, status: Literal["resolved", "dismissed"], note: str | None
) -> Decision:
    """人审裁决一条决策（resolved=已处理，dismissed=不处理/误报）。"""
    queue: dict[str, dict] = vault.load_json("decisions.json", {})
    if decision_id not in queue:
        raise KeyError(f"决策不存在：{decision_id}")
    queue[decision_id]["status"] = status
    queue[decision_id]["resolved_at"] = utcnow()
    if note:
        queue[decision_id]["note"] = note
    vault.save_json("decisions.json", queue)
    vault.git_commit(f"lint: 裁决 {decision_id} → {status}")
    return Decision(**queue[decision_id])


def open_decisions(vault: Vault) -> list[Decision]:
    queue: dict[str, dict] = vault.load_json("decisions.json", {})
    return [Decision(**v) for v in queue.values() if v["status"] == "open"]


def lint_stats(vault: Vault) -> dict[str, int]:
    """监控监控者：lint 自报扫描基数与队列分布。"""
    queue: dict[str, dict] = vault.load_json("decisions.json", {})
    stats = {
        "pages": len(vault.list_pages()),
        "claims": len(vault.load_json("claims.json", {})),
        "sources": len(vault.load_json("sources.json", {})),
        "open": sum(1 for v in queue.values() if v["status"] == "open"),
        "resolved": sum(1 for v in queue.values() if v["status"] == "resolved"),
        "dismissed": sum(1 for v in queue.values() if v["status"] == "dismissed"),
    }
    return stats
