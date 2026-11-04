"""查询：三级渐进披露 + FTS 兜底（P5）。

L1 目录（frontmatter：title + summary，一行一页）
L2 页面全文（声明 + 关联）
L3 关联展开（沿 wikilink 走图）

原则（research/wiki/synthesis.md §四 P5）：
- 声称"不知道"前必须全文搜索（强制 FTS 兜底）
- 永不把模型 confidence 当信任信号——用引用替代
- 未配置 LLM 时输出检索包，人自己读（引擎与壳分离）
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .llm import LLMClient
from .vault import Page, Vault


@dataclass
class Hit:
    kind: str  # page | extract
    key: str  # slug 或 source_id
    title: str
    snippet: str


def catalog(vault: Vault) -> list[dict[str, str]]:
    """L1：页面目录（渐进披露第一级）。"""
    return vault.list_pages()


def read_page(vault: Vault, slug: str) -> str:
    """L2：读页面全文。"""
    return vault.read_page(slug).render()


def linked_pages(vault: Vault, slug: str) -> list[str]:
    """L3：页面声明的出链（wikilink）。"""
    return [link for link in _page_links(vault.read_page(slug)) if vault.page_exists(link)]


def _page_links(page: Page) -> list[str]:

    return re.findall(r"\[\[([^\]|#]+)", "\n".join(page.body))


def search(vault: Vault, query: str, limit: int = 10) -> list[Hit]:
    """FTS 检索：先 wiki 页面，再 extract 兜底。"""
    hits: list[Hit] = []
    with vault.db() as conn:
        rows = conn.execute(
            """
            SELECT slug, title, snippet(pages_fts, 3, '', '', '…', 12)
            FROM pages_fts WHERE pages_fts MATCH ? ORDER BY rank LIMIT ?
            """,
            (_fts_query(query), limit),
        ).fetchall()
        for slug, title, snip in rows:
            hits.append(Hit("page", slug, title or slug, snip or ""))

        rows = conn.execute(
            """
            SELECT source_id, snippet(extracts_fts, 1, '', '', '…', 12)
            FROM extracts_fts WHERE extracts_fts MATCH ? ORDER BY rank LIMIT ?
            """,
            (_fts_query(query), limit),
        ).fetchall()
        registry: dict[str, dict] = vault.load_json("sources.json", {})
        for sid, snip in rows:
            title = str(registry.get(sid, {}).get("title", sid))
            hits.append(Hit("extract", sid, title, snip or ""))
    return hits


def _fts_query(query: str) -> str:
    """自由文本 → FTS5 安全查询（CJK bigram OR 策略）。

    - 双引号包裹防语法注入
    - CJK 连续段切成 bigram 短语（"基 例"），短语之间用 OR 连接：
      自然问题里的虚词（"什么是"）不会导致整句匹配失败，BM25 按相关度排序。
    - ASCII 词保持整词短语。
    """
    from .vault import cjk_space

    tokens = [t for t in query.replace('"', " ").split() if t]
    phrases: list[str] = []
    for tok in tokens:
        parts = cjk_space(tok).split()
        if len(parts) <= 2:
            phrases.append(" ".join(parts))
        else:
            phrases.extend(f"{parts[i]} {parts[i + 1]}" for i in range(len(parts) - 1))
    if not phrases:
        return '""'
    return " OR ".join(f'"{p}"' for p in phrases)


def retrieval_pack(vault: Vault, question: str) -> str:
    """无 LLM 时的检索包：目录 + 命中 + 相关页面正文（人自己读）。

    声称"不知道"前必须先到这里——全文搜索是硬底线。
    """
    pages = catalog(vault)
    hits = search(vault, question)
    lines = [f"# 检索包：{question}", ""]
    lines.append("## 页面目录（L1）")
    lines += [f"- {p['slug']}（{p['type']}）：{p['summary']}" for p in pages] or ["（暂无页面）"]
    lines.append("")
    lines.append("## 全文命中（FTS）")
    for h in hits:
        lines.append(f"- [{h.kind}] {h.title}：{h.snippet}")
    if not hits:
        lines.append("（全文搜索无命中——此时才可回答『不知道』）")
    lines.append("")
    top_pages = [h.key for h in hits if h.kind == "page"][:3]
    for slug in top_pages:
        lines.append(f"---\n## 页面：{slug}\n\n{read_page(vault, slug)}\n")
    return "\n".join(lines)


def answer(vault: Vault, question: str, llm: LLMClient) -> tuple[str, dict]:
    """两步 LLM 作答（L1 选页 → L2 读页作答）。返回 (答案, 指标)。"""
    metrics: dict = {"total_tokens": 0}
    cat = catalog(vault)

    # 第一步：看目录选页（渐进披露——目录先入 context）
    step1, tok1 = llm.chat_json(
        [
            {"role": "system", "content": _SELECT_SYSTEM},
            {
                "role": "user",
                "content": "问题：" + question + "\n\n页面目录：\n"
                + "\n".join(f"- {p['slug']}（{p['type']}）：{p['summary']}" for p in cat)
                + '\n\n只输出 JSON：{"slugs": ["…"], "search_keywords": ["…"]}',
            },
        ],
    )
    metrics["total_tokens"] += tok1

    slugs = [s for s in step1.get("slugs", []) if vault.page_exists(s)]
    # 选页失败或为空 → 强制 FTS 兜底（"不知道"前的硬底线）
    if not slugs:
        hits = search(vault, question)
        slugs = [h.key for h in hits if h.kind == "page"][:3]

    # 第二步：读所选页面全文作答
    corpus = "\n\n".join(f"## {s}\n{read_page(vault, s)}" for s in slugs) or "（无相关页面）"
    result = llm.chat_text(
        [
            {"role": "system", "content": _ANSWER_SYSTEM},
            {
                "role": "user",
                "content": f"问题：{question}\n\n相关页面：\n{corpus}\n\n"
                "基于以上页面回答；引用页面里的 [(源)] 链接；页面上没有的，明说\"页面未覆盖\"。",
            },
        ],
    )
    metrics["total_tokens"] += result.tokens
    metrics["pages_read"] = slugs
    return result.text, metrics


_SELECT_SYSTEM = (
    "你是知识库的导航器。只依据给出的页面目录挑选相关页面 slug，"
    "并给出用于全文检索的关键词。不确定就少选。只输出 JSON。"
)

_ANSWER_SYSTEM = (
    "你是知识库的答题者。只基于给出的页面内容作答，保留页面中的 [(源)] 引用链接；"
    "页面未覆盖的内容必须明说\"页面未覆盖\"，不得编造。"
    "不得表达自己对答案正确性的信心，让引用替你说话。"
)
