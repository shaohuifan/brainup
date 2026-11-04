"""信任写路径测试（P0）——本项目最关键的不变量。"""

from __future__ import annotations

import pytest

from brainup.actions import (
    ActionError,
    AddClaim,
    Citation,
    CreatePage,
    DeprecateClaim,
    LinkPages,
    Plan,
    PlanExecutor,
    ReviseClaim,
    parse_action,
)
from brainup.review import approve_plan, list_plans, reject_plan, submit_plan
from brainup.vault import utcnow
from conftest import find_quote_lines


def _citation(vault, source_md: dict, quote: str) -> Citation:
    start, end = find_quote_lines(vault, source_md["source_id"], quote)
    return Citation(source_id=source_md["source_id"], quote=quote, start_line=start, end_line=end)


def _plan(actions: list[object], origin: str = "agent") -> Plan:
    return Plan(plan_id="P-test", origin=origin, created_at=utcnow(), actions=actions)  # type: ignore[arg-type]


GOOD_QUOTE = "任何递归都需要基例，否则会导致无限循环。"
WRONG_QUOTE = "这句话不存在于来源中的任何位置，是纯伪造的引用。"


def _create(slug: str, title: str, summary: str) -> CreatePage:
    return CreatePage(
        type="create_page", page_type="concept", slug=slug, title=title, summary=summary
    )


# ---------- 封闭词表 ----------
def test_action_vocab_rejects_unknown_type() -> None:
    with pytest.raises(ActionError):
        parse_action({"type": "delete_raw_file", "path": "raw/x.md"})


def test_action_vocab_rejects_extra_fields() -> None:
    """raw 层从动作枚举上不可达——模型发明字段也过不了校验（多余字段被拒）。"""
    with pytest.raises(ActionError):
        parse_action(
            {
                "type": "add_claim",
                "page_slug": "x",
                "text": "内容内容内容",
                "citation": {
                    "source_id": "0123456789ab",
                    "quote": "一段足够长的逐字摘录内容",
                    "start_line": 1,
                    "end_line": 2,
                },
                "raw_write": "evil",
            }
        )


# ---------- 引用逐字核验 ----------
def test_good_citation_passes(vault, source_md) -> None:
    plan = _plan(
        [
            _create("递归", "递归", "函数调用自身的定义方式。"),
            AddClaim(
                type="add_claim",
                page_slug="递归",
                text="递归必须有基例才能终止。",
                citation=_citation(vault, source_md, GOOD_QUOTE),
            ),
        ]
    )
    executor = PlanExecutor(vault)
    assert executor.validate(plan) == []
    executor.apply(plan)
    page = vault.read_page("递归")
    assert any("基例" in line and "C1" in line for line in page.body)


def test_forged_citation_rejected(vault, source_md) -> None:
    # 用真实行号 + 伪造文本：验证逐字核验（不是行号核验）
    start, end = find_quote_lines(vault, source_md["source_id"], GOOD_QUOTE)
    forged = Citation(
        source_id=source_md["source_id"], quote=WRONG_QUOTE, start_line=start, end_line=end
    )
    plan = _plan(
        [
            _create("伪造", "伪造", "测试伪造引用被拒绝的页面。"),
            AddClaim(
                type="add_claim",
                page_slug="伪造",
                text="来源里没有的声明。",
                citation=forged,
            ),
        ]
    )
    executor = PlanExecutor(vault)
    errors = executor.validate(plan)
    assert any("逐字核验失败" in e for e in errors)
    with pytest.raises(ActionError):
        executor.apply(plan)
    assert not vault.page_exists("伪造"), "失败的计划不得产生任何写入"


def test_line_out_of_range_rejected(vault, source_md) -> None:
    start, _ = find_quote_lines(vault, source_md["source_id"], GOOD_QUOTE)
    cite = Citation(
        source_id=source_md["source_id"], quote=GOOD_QUOTE, start_line=start, end_line=999
    )
    plan = _plan(
        [
            _create("越界", "越界", "测试行号越界被拒绝的页面。"),
            AddClaim(type="add_claim", page_slug="越界", text="越界引用的声明。", citation=cite),
        ]
    )
    assert any("越界" in e for e in PlanExecutor(vault).validate(plan))


# ---------- Extend, don't create ----------
def test_create_existing_page_rejected(vault, source_md) -> None:
    PlanExecutor(vault).apply(_plan([_create("递归", "递归", "先建一次的页面。")]))
    errors = PlanExecutor(vault).validate(_plan([_create("递归", "递归2", "重复创建的页面。")]))
    assert any("已存在" in e and "勿重建" in e for e in errors)


# ---------- 声明生命周期 ----------
def _setup_page_with_claim(vault, source_md) -> None:
    plan = _plan(
        [
            _create("递归", "递归", "函数调用自身的定义方式。"),
            AddClaim(
                type="add_claim",
                page_slug="递归",
                text="递归必须有基例才能终止。",
                citation=_citation(vault, source_md, GOOD_QUOTE),
            ),
        ]
    )
    PlanExecutor(vault).apply(plan)


def test_revise_claim(vault, source_md) -> None:
    _setup_page_with_claim(vault, source_md)
    plan = _plan(
        [
            ReviseClaim(
                type="revise_claim",
                page_slug="递归",
                claim_id="C1",
                new_text="递归必须先定义基例（终止条件）。",
            )
        ]
    )
    PlanExecutor(vault).apply(plan)
    page = vault.read_page("递归")
    assert any("终止条件" in line and "C1" in line for line in page.body)


def test_deprecate_claim_keeps_history(vault, source_md) -> None:
    _setup_page_with_claim(vault, source_md)
    plan = _plan(
        [DeprecateClaim(type="deprecate_claim", page_slug="递归", claim_id="C1", reason="来源过时")]
    )
    PlanExecutor(vault).apply(plan)
    page = vault.read_page("递归")
    line = next(line for line in page.body if "C1" in line)
    assert "~~" in line and "来源过时" in line, "弃用保留历史（不删除）"


def test_link_pages_requires_target(vault, source_md) -> None:
    _setup_page_with_claim(vault, source_md)
    plan = _plan([LinkPages(type="link_pages", from_slug="递归", to_slug="不存在页")])
    assert any("目标页面不存在" in e for e in PlanExecutor(vault).validate(plan))


def test_claims_registry_updated(vault, source_md) -> None:
    _setup_page_with_claim(vault, source_md)
    registry: dict[str, dict] = vault.load_json("claims.json", {})
    assert "递归::C1" in registry
    assert registry["递归::C1"]["quote"] == GOOD_QUOTE


# ---------- 人审队列 ----------
def test_plan_requires_human_approval(vault, source_md) -> None:
    """计划必须先进队列，批准才落盘。"""
    plan = _plan([_create("人审测试", "人审测试", "验证批准前不落盘的页面。")])
    submit_plan(vault, plan)
    assert list_plans(vault, status="pending"), "计划应进入待审队列"
    assert not vault.page_exists("人审测试"), "批准前不得有任何写入"
    approve_plan(vault, plan.plan_id)
    assert vault.page_exists("人审测试")
    assert not list_plans(vault, status="pending")


def test_rejected_plan_never_applies(vault, source_md) -> None:
    plan = _plan([_create("拒绝测试", "拒绝测试", "验证拒绝路径的页面。")])
    submit_plan(vault, plan)
    reject_plan(vault, plan.plan_id, "不想要")
    assert not vault.page_exists("拒绝测试")
