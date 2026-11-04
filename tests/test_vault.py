"""Vault 布局与页面读写测试。"""

from __future__ import annotations

from pathlib import Path

from brainup.vault import Vault, VaultError


def test_init_creates_layout(vault: Vault) -> None:
    assert (vault.root / "brainup.toml").is_file()
    assert vault.raw.is_dir()
    assert vault.wiki.is_dir()
    assert (vault.kb / "extract").is_dir()
    assert (vault.kb / "plans").is_dir()
    assert (vault.root / "AGENTS.md").is_file()
    assert vault.git("rev-parse", "--is-inside-work-tree").returncode == 0


def test_init_twice_fails(tmp_path: Path) -> None:
    Vault.init(tmp_path / "v1")
    try:
        Vault.init(tmp_path / "v1")
        raise AssertionError("应当抛 VaultError")
    except VaultError:
        pass


def test_find_walks_up(vault: Vault, tmp_path: Path) -> None:
    nested = vault.root / "raw" / "sub"
    nested.mkdir(exist_ok=True)
    found = Vault.find(nested)
    assert found.root == vault.root


def test_page_roundtrip(vault: Vault) -> None:
    from brainup.vault import Page

    p = Page(
        "递归",
        {"type": "concept", "title": "递归", "created": "2026-11-04", "status": "active"},
        ["# 递归", "", "函数调用自身。", ""],
    )
    vault.write_page_atomic(p)
    loaded = vault.read_page("递归")
    assert loaded.title == "递归"
    assert loaded.front["type"] == "concept"
    assert "# 递归" in loaded.body
