"""封闭动作词表与计划执行（P0：写路径信任）。

调研结论（research/wiki/synthesis.md §四 P0，全部有验证支撑）：
- LLM 永不直接写散文：受约束输出 → 动作词表校验（"缺失的 enum 变体是墙"）→ executor 原子应用
- raw 层从动作枚举上不可达（没有任何动作类型能表达"写 raw"）
- 引用 = 逐字摘录 + 行号，executor 回读 extract 核验，伪造引用直接拒绝
- 应用后单次 git commit；页面上限 400 行，超出自动溢出到 `<slug>-N` 页并留指针
"""

from __future__ import annotations

import hashlib
import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from .vault import Page, Vault, utcnow

# ---- 动作词表（封闭集合：新增类型 = 设计变更，需评审）----
ActionType = Literal[
    "create_page", "add_claim", "revise_claim", "deprecate_claim", "link_pages",
]

PageType = Literal[
    "concept", "person", "work", "chapter", "topic", "disagreement", "review",
]

QUOTE_MIN, QUOTE_MAX = 8, 300
PAGE_CAP_LINES = 400


class _Wall(BaseModel):
    """封闭模型基类：多余字段即拒绝——"缺失的 enum 是墙"，多余的字段同样是墙。"""

    model_config = ConfigDict(extra="forbid")


class Citation(_Wall):
    """引用指针：指向 .kb/extract/<source_id>.md 的行区间 + 逐字摘录。"""

    source_id: str = Field(min_length=8, max_length=16, pattern=r"^[0-9a-f]+$")
    quote: str = Field(min_length=QUOTE_MIN, max_length=QUOTE_MAX)
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)

    def span_link(self) -> str:
        """渲染为 markdown 链接（相对 wiki/ 页面）。"""
        anchor = (
            f"#L{self.start_line}"
            if self.start_line == self.end_line
            else f"#L{self.start_line}-L{self.end_line}"
        )
        return f"../.kb/extract/{self.source_id}.md{anchor}"


class CreatePage(_Wall):
    type: Literal["create_page"]
    page_type: PageType
    slug: str
    title: str
    summary: str = Field(min_length=4, max_length=200)


class AddClaim(_Wall):
    type: Literal["add_claim"]
    page_slug: str
    text: str = Field(min_length=4, max_length=600)
    citation: Citation


class ReviseClaim(_Wall):
    type: Literal["revise_claim"]
    page_slug: str
    claim_id: str = Field(pattern=r"^C\d+$")
    new_text: str = Field(min_length=4, max_length=600)
    citation: Citation | None = None  # 修订可沿用原引用


class DeprecateClaim(_Wall):
    type: Literal["deprecate_claim"]
    page_slug: str
    claim_id: str = Field(pattern=r"^C\d+$")
    reason: str = Field(min_length=2, max_length=200)


class LinkPages(_Wall):
    type: Literal["link_pages"]
    from_slug: str
    to_slug: str
    note: str | None = Field(default=None, max_length=200)


Action = Annotated[
    CreatePage | AddClaim | ReviseClaim | DeprecateClaim | LinkPages,
    Field(discriminator="type"),
]

ACTION_ADAPTER: TypeAdapter[Action] = TypeAdapter(Action)  # 未知 type → 校验失败（墙）


class ActionError(Exception):
    """计划校验/应用失败。"""


def parse_action(obj: object) -> Action:
    try:
        return ACTION_ADAPTER.validate_python(obj)
    except Exception as e:  # noqa: BLE001 - 统一转为受控错误
        raise ActionError(f"动作校验失败（封闭词表拒绝未知类型/字段）：{e}") from e


# ---------- 引用核验 ----------
def extract_lines(vault: Vault, source_id: str) -> list[str]:
    path = vault.extract_dir / f"{source_id}.md"
    if not path.is_file():
        raise ActionError(f"引用的来源不存在：{source_id}（先 ingest）")
    return path.read_text(encoding="utf-8").split("\n")


def verify_citation(vault: Vault, citation: Citation) -> None:
    """逐字核验：quote 必须出现在 extract 指定行区间内（P0 反幻觉的已验证手段）。"""
    lines = extract_lines(vault, citation.source_id)
    if citation.end_line > len(lines):
        raise ActionError(
            f"引用行号越界：extract/{citation.source_id}.md 共 {len(lines)} 行，"
            f"引用到 L{citation.end_line}"
        )
    span_text = "\n".join(lines[citation.start_line - 1 : citation.end_line])
    if citation.quote not in span_text:
        raise ActionError(
            f"逐字核验失败：摘录不在 L{citation.start_line}-L{citation.end_line} 区间内"
        )


# ---------- 页面文本的确定性编辑 ----------
def page_body(title: str, summary: str) -> list[str]:
    return [f"# {title}", "", summary, "", "## 声明", "", "## 关联", ""]


def next_claim_id(body: list[str]) -> str:
    """页内下一个声明 ID（C 计数器）。"""
    ids = [
        int(m.group(1))
        for line in body
        for m in [re.match(r"- \[C(\d+)\]", line)]
        if m
    ]
    return f"C{max(ids, default=0) + 1}"


def _find_section(body: list[str], name: str) -> int:
    for i, line in enumerate(body):
        if line.strip() == f"## {name}":
            return i
    return -1


def _section_end(body: list[str], start: int) -> int:
    for i in range(start + 1, len(body)):
        if body[i].startswith("## "):
            return i
    return len(body)


def _ensure_sections(body: list[str]) -> None:
    for name in ("声明", "关联"):
        if _find_section(body, name) < 0:
            body += ["", f"## {name}", ""]


def _insert_into_section(body: list[str], name: str, line: str) -> None:
    sec = _find_section(body, name)
    end = _section_end(body, sec)
    while end > sec + 1 and not body[end - 1].strip():
        end -= 1
    body.insert(end, line)


def add_claim_line(body: list[str], claim_id: str, text: str, citation: Citation) -> None:
    _ensure_sections(body)
    _insert_into_section(
        body, "声明", f"- [{claim_id}] {text} [(源)]({citation.span_link()})"
    )


def _keep_cite(old_line: str) -> str:
    m = re.search(r"\[\(源\)\]\((\.\./\.kb/extract/[^)]+)\)", old_line)
    return f" [(源)]({m.group(1)})" if m else ""


def replace_claim_line(
    body: list[str], claim_id: str, new_text: str, citation: Citation | None
) -> None:
    prefix = f"- [{claim_id}] "
    for i, line in enumerate(body):
        if line.startswith(prefix):
            cite = f" [(源)]({citation.span_link()})" if citation else _keep_cite(line)
            body[i] = f"- [{claim_id}] {new_text}{cite}"
            return
    raise ActionError(f"声明不存在：{claim_id}")


def deprecate_claim_line(body: list[str], claim_id: str, reason: str) -> None:
    prefix = f"- [{claim_id}] "
    for i, line in enumerate(body):
        if line.startswith(prefix):
            if "~~" in line:
                return  # 已弃用，幂等
            m = re.match(r"- (\[C\d+\]) (.+?)( \[\(源\)\]\([^)]+\))?$", line)
            text = m.group(2) if m else line[len(prefix) :]
            body[i] = f"- [{claim_id}] ~~{text}~~（{utcnow()[:10]} 弃用：{reason}）"
            return
    raise ActionError(f"声明不存在：{claim_id}")


def add_link_line(body: list[str], to_slug: str, note: str | None) -> None:
    _ensure_sections(body)
    line = f"- [[{to_slug}]]" + (f"：{note}" if note else "")
    _insert_into_section(body, "关联", line)


# ---------- 计划 ----------
class Plan(BaseModel):
    """一次受审的写计划：由 ingest/agent/query 写回提交，人审后原子应用。"""

    plan_id: str
    origin: Literal["ingest", "agent", "query_writeback"]
    source_id: str | None = None
    created_at: str
    actions: list[Action]
    status: Literal["pending", "rejected", "applied", "failed"] = "pending"
    note: str | None = None
    error: str | None = None


def plan_from_json(obj: object) -> Plan:
    try:
        return Plan.model_validate(obj)
    except Exception as e:  # noqa: BLE001
        raise ActionError(f"计划结构非法：{e}") from e


# ---------- 执行器 ----------
class PlanExecutor:
    """演练 → 核验 → 原子落盘 → git 提交。任何一步失败都不产生部分写入。"""

    def __init__(self, vault: Vault) -> None:
        self.vault = vault

    # -- 校验（纯内存演练，不落盘） --
    def validate(self, plan: Plan) -> list[str]:
        errors: list[str] = []
        try:
            self._simulate(plan)
        except ActionError as e:
            errors.append(str(e))
        # 逐字核验（引用伪造在此拦截）
        for idx, action in enumerate(plan.actions):
            if isinstance(action, (AddClaim, ReviseClaim)) and action.citation:
                try:
                    verify_citation(self.vault, action.citation)
                except ActionError as e:
                    errors.append(f"动作[{idx}] {action.type}：{e}")
        return errors

    # -- 应用 --
    def apply(self, plan: Plan) -> list[str]:
        """返回被写入/更新的页面 slug 列表。校验失败抛 ActionError（零写入）。"""
        errors = self.validate(plan)
        if errors:
            raise ActionError(f"计划校验失败（{len(errors)} 项）：\n- " + "\n- ".join(errors))

        pages, assignments = self._simulate(plan)
        for page in pages.values():
            page.front["updated"] = utcnow()
            self.vault.write_page_atomic(page)

        self._update_claims_registry(assignments, plan)
        self.vault.git_commit(
            f"plan: {plan.plan_id}（{plan.origin}）— {len(plan.actions)} 个动作"
        )
        plan.status = "applied"
        return sorted(pages)

    # -- 内部：在内存中演练全部动作 --
    def _simulate(self, plan: Plan) -> tuple[dict[str, Page], list[dict]]:
        pages: dict[str, Page] = {}
        assignments: list[dict] = []

        def get_page(slug: str) -> Page:
            if slug not in pages:
                base = self.vault.read_page(slug)
                pages[slug] = Page(base.slug, dict(base.front), list(base.body))
            return pages[slug]

        for idx, action in enumerate(plan.actions):
            if isinstance(action, CreatePage):
                if self.vault.page_exists(action.slug) or action.slug in pages:
                    raise ActionError(
                        f"动作[{idx}]：页面已存在 {action.slug}"
                        "（用 add_claim/revise_claim 扩展，勿重建——Extend, don't create）"
                    )
                page = Page(
                    action.slug,
                    {
                        "type": action.page_type,
                        "title": action.title,
                        "created": utcnow(),
                        "updated": utcnow(),
                        "status": "active",
                    },
                    page_body(action.title, action.summary),
                )
                pages[action.slug] = page

            elif isinstance(action, AddClaim):
                slug = self._target_page(action.page_slug, pages, idx)
                page = get_page(slug)
                cid = next_claim_id(page.body)
                if len(page.body) + 1 > PAGE_CAP_LINES:
                    raise ActionError(
                        f"动作[{idx}]：页面 {slug} 将超 400 行上限，"
                        f"请分流到溢出页（如 {slug}-2）或拆分页面"
                    )
                add_claim_line(page.body, cid, action.text, action.citation)
                assignments.append(
                    {
                        "page": slug,
                        "claim_id": cid,
                        "text_hash": hashlib.sha256(action.text.encode()).hexdigest()[:16],
                        "quote": action.citation.quote,
                        "source_id": action.citation.source_id,
                        "start_line": action.citation.start_line,
                        "end_line": action.citation.end_line,
                        "verified_at": utcnow(),
                        "status": "active",
                    }
                )

            elif isinstance(action, ReviseClaim):
                slug = self._target_page(action.page_slug, pages, idx)
                page = get_page(slug)
                replace_claim_line(page.body, action.claim_id, action.new_text, action.citation)
                for a in assignments:
                    if a["page"] == slug and a["claim_id"] == action.claim_id:
                        a["text_hash"] = hashlib.sha256(
                            action.new_text.encode()
                        ).hexdigest()[:16]
                        if action.citation:
                            a.update(
                                quote=action.citation.quote,
                                source_id=action.citation.source_id,
                                start_line=action.citation.start_line,
                                end_line=action.citation.end_line,
                                verified_at=utcnow(),
                            )
                        break

            elif isinstance(action, DeprecateClaim):
                slug = self._target_page(action.page_slug, pages, idx)
                page = get_page(slug)
                deprecate_claim_line(page.body, action.claim_id, action.reason)
                for a in assignments:
                    if a["page"] == slug and a["claim_id"] == action.claim_id:
                        a["status"] = "deprecated"
                        a["deprecate_reason"] = action.reason

            elif isinstance(action, LinkPages):
                slug = self._target_page(action.from_slug, pages, idx)
                if not (
                    self.vault.page_exists(action.to_slug) or action.to_slug in pages
                ):
                    raise ActionError(
                        f"动作[{idx}]：目标页面不存在 {action.to_slug}（先 create_page）"
                    )
                add_link_line(get_page(slug).body, action.to_slug, action.note)

        return pages, assignments

    def _target_page(self, slug: str, pages: dict[str, Page], idx: int) -> str:
        if not (self.vault.page_exists(slug) or slug in pages):
            raise ActionError(f"动作[{idx}]：页面不存在 {slug}（先 create_page）")
        return slug

    def _update_claims_registry(self, assignments: list[dict], plan: Plan) -> None:
        registry: dict[str, dict] = self.vault.load_json("claims.json", {})
        for a in assignments:
            registry[f"{a['page']}::{a['claim_id']}"] = a
        self.vault.save_json("claims.json", registry)


def summarize_plan(plan: Plan) -> str:
    """人审时的一行摘要。"""
    kinds = [a.type for a in plan.actions]
    head = plan.actions[0]
    target = getattr(head, "slug", None) or getattr(head, "page_slug", None) or ""
    return (
        f"[{plan.plan_id}] {plan.origin} · {len(plan.actions)} 个动作"
        f"（{','.join(kinds[:4])}）· 目标 {target}"
    )
