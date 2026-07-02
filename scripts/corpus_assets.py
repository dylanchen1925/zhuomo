"""Shared paths for source MD corpus assets outside the Obsidian vault."""

from __future__ import annotations

import re
from pathlib import Path

DEFAULT_CORPUS_ROOT = Path.home() / "zhuomo-data"
CORPUS_DIR_NAME = "corpus"
WIKI_CORPUS_LINK = "corpus"  # wiki/corpus -> {corpus_root}/corpus

# Vault-absolute Obsidian image paths (leading slash = vault root).
VAULT_ASSET_RE = re.compile(
    r"(?<![\w/-])/corpus/([a-z0-9-]+)/assets/([^\s)\]\"']+)",
    re.I,
)
LEGACY_SOURCE_ASSET_RE = re.compile(
    r"sources/([a-z0-9-]+)/md/assets/([^\s)\]\"']+)",
    re.I,
)
REL_ASSET_IN_MD_RE = re.compile(
    r"!\[([^\]]*)\]\(assets/([^)]+)\)|\]\(assets/([^)]+)\)",
    re.I,
)


def corpus_root_from_arg(value: Path | str | None) -> Path:
    if value is None:
        return DEFAULT_CORPUS_ROOT.expanduser().resolve()
    return Path(value).expanduser().resolve()


def slug_assets_dir(corpus_root: Path, slug: str) -> Path:
    return corpus_root / CORPUS_DIR_NAME / slug / "assets"


def vault_root_from_wiki(wiki_dir: Path) -> Path:
    """Obsidian vault root (parent of wiki/ when layout is vault/wiki/…)."""
    wiki_dir = wiki_dir.resolve()
    if wiki_dir.name == "wiki" and (wiki_dir.parent / ".obsidian").is_dir():
        return wiki_dir.parent
    return wiki_dir


def asset_vault_path(slug: str, filename: str) -> str:
    """Obsidian vault-root path; requires {vault}/corpus symlink to corpus_root/corpus."""
    name = Path(filename).name
    return f"/corpus/{slug}/assets/{name}"


def ensure_vault_corpus_link(wiki_dir: Path, corpus_root: Path) -> Path:
    """Create {vault_root}/corpus -> {corpus_root}/corpus (Obsidian /corpus/… paths)."""
    vault_root = vault_root_from_wiki(wiki_dir)
    link = vault_root / WIKI_CORPUS_LINK
    target = (corpus_root / CORPUS_DIR_NAME).resolve()
    target.mkdir(parents=True, exist_ok=True)
    if link.is_symlink():
        if link.resolve() == target:
            return link
        raise RuntimeError(f"{link} exists but points to {link.resolve()}, expected {target}")
    if link.exists():
        raise RuntimeError(f"{link} exists and is not a symlink — move aside manually")
    link.symlink_to(target, target_is_directory=True)
    return link


def ensure_wiki_corpus_link(wiki_dir: Path, corpus_root: Path) -> Path:
    """Ensure vault-root corpus link; also wiki/corpus when wiki is a subfolder."""
    primary = ensure_vault_corpus_link(wiki_dir, corpus_root)
    wiki_dir = wiki_dir.resolve()
    vault_root = vault_root_from_wiki(wiki_dir)
    if vault_root == wiki_dir:
        return primary
    target = (corpus_root / CORPUS_DIR_NAME).resolve()
    wiki_link = wiki_dir / WIKI_CORPUS_LINK
    if wiki_link.is_symlink() and wiki_link.resolve() == target:
        return primary
    if not wiki_link.exists():
        wiki_link.symlink_to(target, target_is_directory=True)
    return primary


def rewrite_legacy_asset_refs(text: str, *, slug: str | None = None) -> str:
    """Rewrite legacy vault paths to /corpus/<slug>/assets/..."""

    def leg(m: re.Match[str]) -> str:
        return asset_vault_path(m.group(1), m.group(2))

    text = LEGACY_SOURCE_ASSET_RE.sub(leg, text)

    if slug:

        def rel_img(m: re.Match[str]) -> str:
            alt, p1, p2 = m.group(1), m.group(2), m.group(3)
            path = p1 or p2
            if p1:
                return f"![{alt}]({asset_vault_path(slug, path)})"
            return f"]({asset_vault_path(slug, path)})"

        text = REL_ASSET_IN_MD_RE.sub(rel_img, text)
    return text
