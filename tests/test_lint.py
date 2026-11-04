"""lint 决策队列测试（P1）。"""

from __future__ import annotations

from brainup import lint as lint_mod
from brainup.vault import Page


def _seed_page(vault, slug: str, body: list[str], summary: str = "测试页。") -> None:
    page = Page(
        slug,
        {"type": "concept", "title": slug, "created": "2026-11-04", "status": "active",
         "summary": summary},
        body,
    )
    vault.write_page_atomic(page)


def test_broken_wikilink_becomes_decision(vault) -> None:
    _seed_page(vault, "页A", ["# 页A", "", "## 关联", "", "- [[不存在的页]]"])
    decisions = lint_mod.run_lint(vault)
    kinds = [d.kind for d in decisions]
    assert "broken_wikilink" in kinds
    d = next(d for d in decisions if d.kind == "broken_wikilink")
    assert d.evidence, "发现必须带逐字证据"


def test_orphan_detected(vault) -> None:
    _seed_page(vault, "孤立页", ["# 孤立页", ""])
    decisions = lint_mod.run_lint(vault)
    assert any(d.kind == "orphan_page" and d.target == "孤立页" for d in decisions)


def test_decisions_are_idempotent(vault) -> None:
    _seed_page(vault, "页B", ["# 页B", "", "## 关联", "", "- [[断链]]"])
    first = lint_mod.run_lint(vault)
    second = lint_mod.run_lint(vault)
    assert len(second) == len(first), "同一问题不得重复入队"


def test_adjudicate_resolves(vault) -> None:
    _seed_page(vault, "页C", ["# 页C", "", "## 关联", "", "- [[断链C]]"])
    decisions = lint_mod.run_lint(vault)
    assert len(decisions) >= 1
    for d in decisions:
        lint_mod.adjudicate(vault, d.id, "dismissed", "这是故意留的占位链接")
    assert lint_mod.open_decisions(vault) == []


def test_repeated_lint_keeps_resolved(vault) -> None:
    """已裁决项不因重新扫描复活。"""
    _seed_page(vault, "页D", ["# 页D", "", "## 关联", "", "- [[断链D]]"])
    for d in lint_mod.run_lint(vault):
        lint_mod.adjudicate(vault, d.id, "dismissed", None)
    lint_mod.run_lint(vault)
    assert lint_mod.open_decisions(vault) == []


def test_claim_drift_after_human_edit(vault, source_md) -> None:
    from brainup.actions import AddClaim, Citation, CreatePage, Plan, PlanExecutor
    from brainup.vault import utcnow
    from conftest import find_quote_lines

    start, end = find_quote_lines(
        vault, source_md["source_id"], "任何递归都需要基例，否则会导致无限循环。"
    )
    plan = Plan(
        plan_id="P-drift",
        origin="agent",
        created_at=utcnow(),
        actions=[
            CreatePage(
                type="create_page", page_type="concept", slug="漂移页",
                title="漂移页", summary="测试人工编辑后的漂移检测。",
            ),
            AddClaim(
                type="add_claim", page_slug="漂移页",
                text="原始声明内容。",
                citation=Citation(
                    source_id=source_md["source_id"],
                    quote="任何递归都需要基例，否则会导致无限循环。",
                    start_line=start, end_line=end,
                ),
            ),
        ],
    )
    PlanExecutor(vault).apply(plan)

    # 人工编辑页面声明（模拟 Obsidian 手改）
    page = vault.read_page("漂移页")
    for i, line in enumerate(page.body):
        if line.startswith("- [C1]"):
            page.body[i] = line.replace("原始声明内容。", "人工改过的声明。")
    vault.write_page_atomic(page)

    decisions = lint_mod.run_lint(vault)
    assert any(d.kind == "claim_drift" and d.target == "漂移页" for d in decisions)
