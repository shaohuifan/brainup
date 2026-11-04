"""指标与 MCP 层测试（打桩 LLM，零网络依赖）。"""

from __future__ import annotations

from brainup import metrics as metrics_mod
from brainup import review as review_mod


def test_metrics_summary(vault) -> None:
    metrics_mod.log_event(vault, "ingest", {"source_id": "deadbeef"})
    metrics_mod.log_event(vault, "query", {"total_tokens": 120, "pages_read": ["递归"]})
    metrics_mod.log_event(vault, "query", {"total_tokens": 80, "pages_read": []})
    s = metrics_mod.summary(vault)
    assert s["ingests"] == 1
    assert s["queries"] == 2
    assert s["total_query_tokens"] == 200
    assert s["avg_tokens_per_query"] == 100


def test_mcp_submit_plan_paths_to_review(vault, source_md, monkeypatch) -> None:
    """MCP submit_plan → 人审队列（不落盘）。"""
    from brainup import mcp_server
    from brainup.actions import summarize_plan
    from conftest import find_quote_lines

    mcp_server.set_vault_path(str(vault.root))
    quote = "任何递归都需要基例，否则会导致无限循环。"
    start, end = find_quote_lines(vault, source_md["source_id"], quote)
    actions = [
        {
            "type": "create_page",
            "page_type": "concept",
            "slug": "MCP测试页",
            "title": "MCP测试页",
            "summary": "经 MCP 提交的页面。",
        },
        {
            "type": "add_claim",
            "page_slug": "MCP测试页",
            "text": "MCP 提交的声明必须带引用。",
            "citation": {
                "source_id": source_md["source_id"],
                "quote": quote,
                "start_line": start,
                "end_line": end,
            },
        },
    ]
    import json

    out = mcp_server.submit_plan(json.dumps(actions, ensure_ascii=False))
    assert "已入人审队列" in out, out
    assert not vault.page_exists("MCP测试页"), "批准前不得写入"
    pending = review_mod.list_plans(vault, status="pending")
    assert len(pending) == 1
    assert summarize_plan(pending[0]).startswith("[")

    # 非法动作被拒
    out = mcp_server.submit_plan(json.dumps([{"type": "nuke_everything"}]))
    assert out.startswith("拒绝")


def test_mcp_read_tools(vault, source_md) -> None:
    from brainup import mcp_server

    mcp_server.set_vault_path(str(vault.root))
    status = mcp_server.brainup_status()
    assert "来源 1" in status
    cat = mcp_server.read_catalog()
    assert "vault 为空" in cat  # 尚无页面
    text = mcp_server.read_extract(source_md["source_id"], 1, 10)
    assert "递归的概念" in text


def test_answer_with_stub_llm(vault, source_md, monkeypatch) -> None:
    """query.answer 用打桩 LLM：验证两步流程与 FTS 兜底。"""
    from brainup import query as query_mod
    from brainup.llm import LLMClient, LLMResult
    from conftest import find_quote_lines

    class StubLLM(LLMClient):
        def __init__(self) -> None:
            pass  # 跳过配置校验

        def chat_json(self, messages, model=None):
            return {"slugs": ["不存在的页面"]}, 10  # 故意选错 → 触发 FTS 兜底

        def chat_text(self, messages, model=None):
            return LLMResult("这是打桩答案。", 20)

    # 先建一个页面供兜底命中
    from brainup.actions import AddClaim, Citation, CreatePage, Plan, PlanExecutor
    from brainup.vault import utcnow

    quote = "任何递归都需要基例，否则会导致无限循环。"
    start, end = find_quote_lines(vault, source_md["source_id"], quote)
    PlanExecutor(vault).apply(
        Plan(
            plan_id="P-ans",
            origin="agent",
            created_at=utcnow(),
            actions=[
                CreatePage(
                    type="create_page", page_type="concept", slug="递归",
                    title="递归", summary="函数调用自身的方法。",
                ),
                AddClaim(
                    type="add_claim", page_slug="递归",
                    text="递归需要基例。",
                    citation=Citation(
                        source_id=source_md["source_id"],
                        quote=quote,
                        start_line=start, end_line=end,
                    ),
                ),
            ],
        )
    )

    text, m = query_mod.answer(vault, "什么是基例", StubLLM())
    assert text == "这是打桩答案。"
    assert m["total_tokens"] == 30
    assert m["pages_read"] == ["递归"], "选页失败必须走 FTS 兜底"
