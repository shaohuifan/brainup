"""测试夹具：临时 vault（配置 git 身份以免 CI 无全局配置）。"""

from __future__ import annotations

from pathlib import Path

import pytest

from brainup.vault import Vault


@pytest.fixture()
def vault(tmp_path: Path) -> Vault:
    v = Vault.init(tmp_path / "mykb")
    v.git("config", "user.name", "test")
    v.git("config", "user.email", "test@example.com")
    return v


@pytest.fixture()
def source_md(vault: Vault) -> dict:
    """摄入一个 markdown 来源，返回 {source_id, text}。"""
    from brainup import ingest as ingest_mod

    content = (
        "# 递归的概念\n\n"
        "递归是一种函数调用自身的计算方法。\n"
        "任何递归都需要基例，否则会导致无限循环。\n"
        "尾递归可以被编译器优化为循环，但 Python 不支持。\n"
        "递归与数学归纳法在结构上同构。\n"
    )
    path = vault.root / "tmp_article.md"
    path.write_text(content, encoding="utf-8")
    rec = ingest_mod.ingest_file(vault, path)
    return {"source_id": rec.source_id, "text": content, "lines": rec.lines}


def find_quote_lines(vault: Vault, source_id: str, quote: str) -> tuple[int, int]:
    """在 extract 中定位 quote 所在行区间（引用锚点必须来自真实行号）。"""
    text = (vault.extract_dir / f"{source_id}.md").read_text(encoding="utf-8")
    lines = text.split("\n")
    for i, line in enumerate(lines, 1):
        if quote in line:
            return i, i
    raise AssertionError(f"quote 不在 extract 中：{quote[:40]}")
