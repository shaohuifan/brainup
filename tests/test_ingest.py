"""摄入与查询测试。"""

from __future__ import annotations

import zipfile

from brainup import ingest as ingest_mod
from brainup import query as query_mod
from brainup.vault import Vault


def test_ingest_markdown_idempotent(vault: Vault) -> None:
    path = vault.root / "a.md"
    path.write_text("# 标题甲\n\n知识就是复利。", encoding="utf-8")
    rec1 = ingest_mod.ingest_file(vault, path)
    rec2 = ingest_mod.ingest_file(vault, path)
    assert rec1.source_id == rec2.source_id, "内容寻址幂等"
    assert (vault.raw / rec1.stored_name).is_file()
    assert (vault.extract_dir / f"{rec1.source_id}.md").is_file()


def test_ingest_txt(vault: Vault) -> None:
    path = vault.root / "b.txt"
    path.write_text("第一行\n第二行", encoding="utf-8")
    rec = ingest_mod.ingest_file(vault, path)
    text = (vault.extract_dir / f"{rec.source_id}.md").read_text(encoding="utf-8")
    assert "第二行" in text


def test_ingest_epub(vault: Vault) -> None:
    """构造最小合法 EPUB（zip + container + 章节.xhtml）。"""
    epub_path = vault.root / "book.epub"
    container = (
        '<?xml version="1.0"?>'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>'
        "</rootfiles></container>"
    )
    opf = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
        '<dc:identifier id="id">test</dc:identifier>'
        "<dc:title>测试之书</dc:title>"
        "<dc:language>zh</dc:language>"
        "</metadata>"
        '<manifest><item id="ch1" href="ch1.xhtml" media-type="application/xhtml+xml"/></manifest>'
        '<spine><itemref idref="ch1"/></spine></package>'
    )
    chapter = (
        '<?xml version="1.0" encoding="utf-8"?>'
        "<html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>ch</title></head>"
        "<body><p>本书讲解知识的复利效应。</p></body></html>"
    )
    with zipfile.ZipFile(epub_path, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip")
        zf.writestr("META-INF/container.xml", container)
        zf.writestr("content.opf", opf)
        zf.writestr("ch1.xhtml", chapter)
    rec = ingest_mod.ingest_file(vault, epub_path)
    assert rec.title == "测试之书"
    extract = (vault.extract_dir / f"{rec.source_id}.md").read_text(encoding="utf-8")
    assert "知识的复利效应" in extract


def test_fts_search_finds_extract(vault: Vault) -> None:
    path = vault.root / "c.md"
    path.write_text("# 熵\n\n熵是系统无序程度的度量。", encoding="utf-8")
    ingest_mod.ingest_file(vault, path)
    hits = query_mod.search(vault, "熵 无序")
    # CJK 逐字分词后 snippet 含空格，比较时去空格
    assert any(h.kind == "extract" and "无序" in h.snippet.replace(" ", "") for h in hits)


def test_catalog_and_retrieval_pack(vault: Vault) -> None:
    from brainup.actions import AddClaim, Citation, CreatePage, Plan, PlanExecutor
    from brainup.vault import utcnow
    from conftest import find_quote_lines

    path = vault.root / "d.md"
    path.write_text("# 网络\n\n小世界网络具有短路径特征。", encoding="utf-8")
    rec = ingest_mod.ingest_file(vault, path)
    quote = "小世界网络具有短路径特征。"
    start, end = find_quote_lines(vault, rec.source_id, quote)
    plan = Plan(
        plan_id="P-q",
        origin="agent",
        created_at=utcnow(),
        actions=[
            CreatePage(
                type="create_page",
                page_type="concept",
                slug="小世界网络",
                title="小世界网络",
                summary="短路径特征的社会网络。",
            ),
            AddClaim(
                type="add_claim",
                page_slug="小世界网络",
                text="小世界网络具有短路径特征。",
                citation=Citation(
                    source_id=rec.source_id, quote=quote, start_line=start, end_line=end
                ),
            ),
        ],
    )
    PlanExecutor(vault).apply(plan)

    cat = query_mod.catalog(vault)
    assert any(p["slug"] == "小世界网络" for p in cat)
    hits = query_mod.search(vault, "短路径")
    assert any(h.kind == "page" and h.key == "小世界网络" for h in hits)
    pack = query_mod.retrieval_pack(vault, "什么是小世界网络")
    assert "小世界网络" in pack and "无命中" not in pack, pack[:300]
