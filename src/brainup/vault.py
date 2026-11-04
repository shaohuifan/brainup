"""Vault：三层布局、页面读写与基础设施。

数据流单向（research/wiki/synthesis.md P3）：
    raw/（不可变原始层，人写 LLM 读）
      → .kb/extract/（规范化文本，可重建，引用锚点）
        → wiki/（append-only 声明层，LLM 写人审读）

wiki/*.md 是唯一权威产物（人可用 Obsidian 直接编辑）；
.kb/ 中的索引（FTS）可随时重建，注册表与队列是 git 版本化的状态。

注意（P4）：index.md / log.md 是写热点，本工具不依赖它们——
页面描述入 frontmatter，历史入 git commit。
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import yaml

VAULT_MARKER = "brainup.toml"

PAGE_TYPES = ("concept", "person", "work", "chapter", "topic", "disagreement", "review")

_DEFAULT_CONFIG = """\
# brainup vault 配置。API key 永不写入本文件，只从环境变量读取。
[llm]
provider = "none"            # none | openai-compat | anthropic
# base_url = "https://api.deepseek.com/v1"
# model = "deepseek-chat"
# small_model = "deepseek-chat"   # 路由用小模型（决策），省 token
# api_key_env = "DEEPSEEK_API_KEY"
"""

_VAULT_AGENTS_MD = """\
# 本 Vault 的操作规约（schema 层）

> 本文件由 brainup 维护，人与 LLM 共同演化。改规约 = 改产品行为。

## 三层（单向流，勿违反）

- `raw/` 不可变原始层：书/论文/文章。**任何写路径都不得改动 raw/。**
- `.kb/extract/` 规范化文本（可重建）：引用锚点指向这里（`source_id` + 行号）。
- `wiki/` 声明层：概念/人物/作品/章节/主题/分歧页。LLM 经"封闭动作词表"写入，人审后落盘。

## 引用规则

- 每条声明必须带引用：`[(源)](../.kb/extract/<id>.md#L10-L12)`。
- 引用 = 逐字摘录（8-300 字符）+ 行号；工具会回读核验，**伪造引用会被拒绝**。
- wiki 产出（答案写回）不得作为来源引用（单向流防火墙）。

## 矛盾与过时

- 矛盾不强行调和：写成分歧声明或独立"disagreement"页，各自标注来源。
- 过时声明用弃用动作标记（~~删除线~~ + 理由），**不删除**（负面知识保留）。

## 维护

- `brainup lint` 产出**决策队列**，不是自动修复：每条待裁决项由人拍板。
- 页面上限 400 行，超出自动溢出到 `<slug>-2` 页并留指针。
"""


def utcnow() -> str:
    """UTC ISO 时间戳（秒级）。"""
    return datetime.now(UTC).isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def slugify(name: str) -> str:
    """slug 即文件名主干：中文允许，仅排除路径危险字符。"""
    slug = name.strip()
    if not slug or slug in {".", ".."} or "/" in slug or "\\" in slug or "\x00" in slug:
        raise ValueError(f"非法 slug：{name!r}")
    if slug.endswith(".md"):
        slug = slug[:-3]
    return slug[:120]


class VaultError(Exception):
    """Vault 相关错误。"""


class Page:
    """一个 wiki 页面：frontmatter + 正文行。"""

    def __init__(self, slug: str, front: dict[str, object], body: list[str]) -> None:
        self.slug = slug
        self.front = front
        self.body = body

    @property
    def title(self) -> str:
        return str(self.front.get("title", self.slug))

    @property
    def summary(self) -> str:
        return str(self.front.get("summary", ""))

    def render(self) -> str:
        front = yaml.safe_dump(
            self.front, allow_unicode=True, sort_keys=False, default_flow_style=False
        ).strip()
        return f"---\n{front}\n---\n" + "\n".join(self.body)


class Vault:
    """三层布局与基础操作。"""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        if not (self.root / VAULT_MARKER).is_file():
            raise VaultError(f"不是 brainup vault（缺少 {VAULT_MARKER}）：{self.root}")

    # ---------- 路径 ----------
    @property
    def raw(self) -> Path:
        return self.root / "raw"

    @property
    def kb(self) -> Path:
        return self.root / ".kb"

    @property
    def wiki(self) -> Path:
        return self.root / "wiki"

    @property
    def extract_dir(self) -> Path:
        return self.kb / "extract"

    @property
    def plans_dir(self) -> Path:
        return self.kb / "plans"

    @property
    def db_path(self) -> Path:
        return self.kb / "index.db"

    # ---------- 初始化 ----------
    @classmethod
    def init(cls, path: Path, language: str = "zh") -> Vault:
        root = path.resolve()
        root.mkdir(parents=True, exist_ok=True)
        marker = root / VAULT_MARKER
        if marker.exists():
            raise VaultError(f"已存在 vault：{root}")
        marker.write_text(f"language = {json.dumps(language)}\n", encoding="utf-8")
        for d in (root / "raw", root / ".kb" / "extract", root / ".kb" / "plans", root / "wiki"):
            d.mkdir(parents=True, exist_ok=True)
        (root / ".kb" / "config.toml").write_text(_DEFAULT_CONFIG, encoding="utf-8")
        (root / "AGENTS.md").write_text(_VAULT_AGENTS_MD, encoding="utf-8")
        for name, default in (("sources.json", {}), ("claims.json", {}), ("decisions.json", {})):
            (root / ".kb" / name).write_text(
                json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        vault = cls(root)
        vault.rebuild_index()
        vault.git("init", check=False)
        vault.git_commit("vault: 初始化三层布局")
        return vault

    @classmethod
    def find(cls, start: Path | None = None) -> Vault:
        """从 start（默认 cwd）向上查找 vault。"""
        cur = (start or Path.cwd()).resolve()
        for candidate in (cur, *cur.parents):
            if (candidate / VAULT_MARKER).is_file():
                return cls(candidate)
        raise VaultError("未找到 brainup vault（请先 brainup init）")

    # ---------- JSON 注册表（原子写） ----------
    def load_json(self, name: str, default: object) -> object:
        path = self.kb / name
        if not path.is_file():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def save_json(self, name: str, data: object) -> None:
        write_atomic(self.kb / name, json.dumps(data, ensure_ascii=False, indent=2))

    # ---------- 页面 ----------
    def page_path(self, slug: str) -> Path:
        return self.wiki / f"{slugify(slug)}.md"

    def page_exists(self, slug: str) -> bool:
        return self.page_path(slug).is_file()

    def read_page(self, slug: str) -> Page:
        path = self.page_path(slug)
        if not path.is_file():
            raise VaultError(f"页面不存在：{slug}")
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            raise VaultError(f"页面缺少 frontmatter：{slug}")
        rest = text[4:]
        try:
            front_raw, body = rest.split("\n---\n", 1)
        except ValueError as e:
            raise VaultError(f"页面 frontmatter 不完整：{slug}") from e
        front = yaml.safe_load(front_raw) or {}
        return Page(slug, front, body.split("\n"))

    def list_pages(self) -> list[dict[str, str]]:
        metas: list[dict[str, str]] = []
        for path in sorted(self.wiki.glob("*.md")):
            try:
                page = self.read_page(path.stem)
            except VaultError:
                continue
            metas.append(
                {
                    "slug": page.slug,
                    "type": str(page.front.get("type", "")),
                    "title": page.title,
                    "summary": page.summary,
                    "status": str(page.front.get("status", "")),
                }
            )
        return metas

    def write_page_atomic(self, page: Page) -> None:
        write_atomic(self.page_path(page.slug), page.render())
        self.reindex_page(page.slug)

    def delete_page(self, slug: str) -> None:  # 仅供测试/工具内部，写路径不暴露
        path = self.page_path(slug)
        if path.exists():
            path.unlink()
        with self.db() as conn:
            conn.execute("DELETE FROM pages_fts WHERE slug = ?", (slug,))

    # ---------- FTS 索引（SQLite） ----------
    def db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        self._ensure_schema(conn)
        return conn

    def _ensure_schema(self, conn: sqlite3.Connection) -> None:
        conn.executescript(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts USING fts5(
                slug UNINDEXED, title, summary, content
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS extracts_fts USING fts5(
                source_id UNINDEXED, content
            );
            CREATE TABLE IF NOT EXISTS events (
                ts TEXT NOT NULL, kind TEXT NOT NULL, detail TEXT NOT NULL
            );
            """
        )
        conn.commit()

    def reindex_page(self, slug: str) -> None:
        path = self.page_path(slug)
        if not path.is_file():
            return
        text = path.read_text(encoding="utf-8")
        try:
            page = self.read_page(slug)
            title, summary = page.title, page.summary
        except VaultError:
            title, summary = slug, ""
        with self.db() as conn:
            conn.execute("DELETE FROM pages_fts WHERE slug = ?", (slug,))
            conn.execute(
                "INSERT INTO pages_fts (slug, title, summary, content) VALUES (?,?,?,?)",
                (slug, title, summary, cjk_space(text)),
            )

    def reindex_extract(self, source_id: str) -> None:
        path = self.extract_dir / f"{source_id}.md"
        if not path.is_file():
            return
        with self.db() as conn:
            conn.execute("DELETE FROM extracts_fts WHERE source_id = ?", (source_id,))
            conn.execute(
                "INSERT INTO extracts_fts (source_id, content) VALUES (?,?)",
                (source_id, cjk_space(path.read_text(encoding="utf-8"))),
            )

    def rebuild_index(self) -> None:
        """FTS 可从 wiki/ + extract/ 全量重建。"""
        with self.db() as conn:
            conn.execute("DELETE FROM pages_fts")
            conn.execute("DELETE FROM extracts_fts")
        for path in self.wiki.glob("*.md"):
            self.reindex_page(path.stem)
        for path in self.extract_dir.glob("*.md"):
            self.reindex_extract(path.stem)

    # ---------- git ----------
    def git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            ["git", "-C", str(self.root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if check and proc.returncode != 0:
            raise VaultError(f"git {' '.join(args)} 失败：{proc.stderr.strip()}")
        return proc

    def git_commit(self, message: str) -> str | None:
        """提交 vault 全部变更，返回 commit hash（无 git 或无变更时返回 None）。"""
        probe = self.git("rev-parse", "--is-inside-work-tree", check=False)
        if probe.returncode != 0:
            return None
        self.git("add", "-A")
        status = self.git("status", "--porcelain")
        if not status.stdout.strip():
            return None
        self.git("commit", "-m", message)
        return self.git("rev-parse", "--short", "HEAD").stdout.strip()

    def is_clean(self) -> bool:
        return not self.git("status", "--porcelain").stdout.strip()


# ---------- 模块级工具 ----------
_CJK_RE = re.compile(r"([\u4e00-\u9fff\u3400-\u4dbf])")


def cjk_space(text: str) -> str:
    """CJK 逐字分词：unicode61 不切中文，需在索引与查询两侧同步加空格。

    查询侧用短语匹配（"无 序" = 相邻 token），等价于子串匹配。
    """
    return _CJK_RE.sub(r" \1 ", text)


def write_atomic(path: Path, text: str) -> None:
    """原子写：同目录临时文件 → os.replace（P0 写路径防护）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):  # replace 失败时清理
            os.remove(tmp)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")
