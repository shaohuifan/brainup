"""metrics：北极星指标埋点（P6）。

从第一天埋点（research/wiki/synthesis.md §四 P6）：
- 每查询 token（对比裸检索的成本变量）
- ingest 次数与来源数
- 已编译知识命中率（复用率——成本回本的直接变量，由 query 记录 pages_read）
- 源/编译页比率（写快于读警报：<1 说明 wiki 在空转）
"""

from __future__ import annotations

import json

from .vault import Vault, utcnow


def log_event(vault: Vault, kind: str, detail: dict[str, object]) -> None:
    with vault.db() as conn:
        conn.execute(
            "INSERT INTO events (ts, kind, detail) VALUES (?,?,?)",
            (utcnow(), kind, json.dumps(detail, ensure_ascii=False)),
        )


def summary(vault: Vault) -> dict[str, object]:
    with vault.db() as conn:
        rows = conn.execute("SELECT kind, COUNT(*) FROM events GROUP BY kind").fetchall()
        counts = {k: n for k, n in rows}
        tokens = conn.execute(
            "SELECT detail FROM events WHERE kind = 'query'"
        ).fetchall()
    total_query_tokens = 0
    pages_read_total = 0
    for (detail_json,) in tokens:
        try:
            d = json.loads(detail_json)
            total_query_tokens += int(d.get("total_tokens", 0))
            pages_read_total += len(d.get("pages_read", []))
        except Exception:  # noqa: BLE001
            continue
    sources = len(vault.load_json("sources.json", {}))
    pages = len(vault.list_pages())
    return {
        "events": counts,
        "queries": counts.get("query", 0),
        "total_query_tokens": total_query_tokens,
        "ingests": counts.get("ingest", 0),
        "sources": sources,
        "pages": pages,
        "source_page_ratio": round(sources / pages, 2) if pages else None,
        "avg_tokens_per_query": (
            total_query_tokens // counts.get("query", 1) if counts.get("query") else None
        ),
        "avg_pages_read": (
            round(pages_read_total / counts["query"], 2) if counts.get("query") else None
        ),
    }
