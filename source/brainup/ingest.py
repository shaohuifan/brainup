"""摄入：解析 → raw 归档 → extract 规范化 → FTS 索引。

安全（P7）：源文件内嵌指令 = 不可信内容。extract 以纯文本存储，
不解释任何内容；内容中的"指令"对动作词表无授权能力。

幂等：raw 层不可变——同内容重复 ingest 直接跳过（内容寻址）。
"""

from __future__ import annotations

import io
import json
import re
from dataclasses import dataclass
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

from .actions import ActionError
from .vault import Vault, sha256_bytes, utcnow, write_atomic

SUPPORTED_EXTS = {".md", ".markdown", ".txt", ".pdf", ".epub", ".html", ".htm"}

_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class SourceRecord:
    source_id: str
    original_name: str
    stored_name: str
    title: str
    parser: str
    ingested_at: str
    lines: int


# ---------- 解析器 ----------
def parse_markdown(data: bytes, name: str) -> tuple[str, str]:
    """markdown/txt：原样入库（去掉 frontmatter 与 BOM）。"""
    text = _decode(data)
    text = _FRONTMATTER.sub("", text, count=1)
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = m.group(1).strip() if m else Path(name).stem
    return text, title


def _decode(data: bytes) -> str:
    """解码并去 BOM（Windows 工具常写带 BOM 的 UTF-8）。"""
    return data.decode("utf-8-sig", errors="replace")


def parse_pdf(data: bytes, name: str) -> tuple[str, str]:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    pages = []
    for i, page in enumerate(reader.pages):
        pages.append(f"## 第 {i + 1} 页\n\n{page.extract_text() or ''}")
    text = "\n\n".join(pages)
    meta_title = (reader.metadata or {}).get("/Title") if reader.metadata else None
    title = str(meta_title).strip() if meta_title else Path(name).stem
    return text, title


def parse_epub(data: bytes, name: str) -> tuple[str, str]:
    import ebooklib
    from ebooklib import epub

    book = epub.read_epub(io.BytesIO(data))
    parts: list[str] = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        html = item.get_content().decode("utf-8", errors="replace")
        soup = BeautifulSoup(html, "html.parser")
        text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n")).strip()
        if text:
            parts.append(text)
    text = "\n\n---\n\n".join(parts)
    title = Path(name).stem
    try:
        meta = book.get_metadata("DC", "title") or []
        if meta and meta[0] and isinstance(meta[0], tuple | list) and meta[0][0]:
            title = str(meta[0][0]).strip() or title
    except Exception:  # noqa: BLE001 - 元数据缺失不致命
        pass
    return text or "（EPUB 无可提取文本）", title


def parse_html(data: bytes, name: str) -> tuple[str, str]:
    soup = BeautifulSoup(data, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    title = (soup.title.string.strip() if soup.title and soup.title.string else "") or name
    text = re.sub(r"\n{3,}", "\n\n", soup.get_text("\n")).strip()
    return text, title


def parse_bytes(data: bytes, name: str) -> tuple[str, str]:
    """按扩展名分派。extract 输出为 markdown 文本。"""
    ext = Path(name).suffix.lower()
    if ext in {".md", ".markdown"}:
        return parse_markdown(data, name)
    if ext == ".txt":
        return _decode(data), Path(name).stem
    if ext == ".pdf":
        return parse_pdf(data, name)
    if ext == ".epub":
        return parse_epub(data, name)
    if ext in {".html", ".htm"}:
        return parse_html(data, name)
    raise ActionError(f"不支持的格式 {ext}（支持：{', '.join(sorted(SUPPORTED_EXTS))}）")


# ---------- 摄入 ----------
def ingest_file(vault: Vault, path: Path) -> SourceRecord:
    """归档一个本地文件。幂等（内容寻址）。"""
    data = path.read_bytes()
    return _ingest_bytes(vault, data, path.name)


def ingest_url(vault: Vault, url: str) -> SourceRecord:
    """抓取 URL（HTML）。"""
    resp = httpx.get(
        url,
        follow_redirects=True,
        timeout=30.0,
        headers={"User-Agent": "brainup/0.1"},
    )
    resp.raise_for_status()
    name = url.rsplit("/", 1)[-1] or "page"
    if "." not in Path(name).suffix:
        name = f"{name or 'page'}.html"
    record = _ingest_bytes(vault, resp.content, name, url=url)
    return record


def _ingest_bytes(vault: Vault, data: bytes, name: str, url: str | None = None) -> SourceRecord:
    source_id = sha256_bytes(data)[:8]
    registry: dict[str, dict] = vault.load_json("sources.json", {})
    if source_id in registry:
        rec = registry[source_id]
        return SourceRecord(
            **{
                k: rec[k]
                for k in (
                    "source_id",
                    "original_name",
                    "stored_name",
                    "title",
                    "parser",
                    "ingested_at",
                    "lines",
                )
            }
        )

    text, title = parse_bytes(data, name)
    ext = Path(name).suffix.lower() or ".bin"
    stored_name = f"{Path(name).stem}-{source_id}{ext}"
    (vault.raw / stored_name).write_bytes(data)

    extract = _render_extract(title, name, url, text)
    write_atomic(vault.extract_dir / f"{source_id}.md", extract)
    vault.reindex_extract(source_id)

    record = SourceRecord(
        source_id=source_id,
        original_name=name,
        stored_name=stored_name,
        title=title,
        parser=ext.lstrip("."),
        ingested_at=utcnow(),
        lines=len(extract.split("\n")),
    )
    registry[source_id] = {
        **record.__dict__,
        "url": url,
        "sha256": sha256_bytes(data),
    }
    vault.save_json("sources.json", registry)
    vault.git_commit(f"ingest: {name} → {source_id}")
    return record


def _render_extract(title: str, name: str, url: str | None, text: str) -> str:
    """extract 文件：frontmatter + 正文。行号锚点指向本文件的行（含 frontmatter）。"""
    def q(value: str) -> str:
        return json.dumps(re.sub(r"[\r\n]+", " ", value).strip(), ensure_ascii=False)

    lines = [
        "---",
        f"title: {q(title)}",
        f"original: {q(name)}",
    ]
    if url:
        lines.append(f"url: {q(url)}")
    lines += ["---", "", text.rstrip(), ""]
    return "\n".join(lines)
