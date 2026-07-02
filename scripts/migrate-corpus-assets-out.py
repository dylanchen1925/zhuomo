#!/usr/bin/env python3
"""Move wiki/sources/*/md/assets/ to ~/zhuomo-data/corpus/<slug>/assets/ and rewrite links.

Creates {vault_root}/corpus symlink -> {corpus_root}/corpus so Obsidian resolves /corpus/... paths.
(Vault root is parent of wiki/ when .obsidian lives there.)
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from corpus_assets import (
    DEFAULT_CORPUS_ROOT,
    WIKI_CORPUS_LINK,
    asset_vault_path,
    corpus_root_from_arg,
    ensure_wiki_corpus_link,
    rewrite_legacy_asset_refs,
    slug_assets_dir,
    vault_root_from_wiki,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path, help="Path to vault wiki/ folder")
    p.add_argument(
        "--corpus-root",
        type=Path,
        default=DEFAULT_CORPUS_ROOT,
        help=f"Corpus storage root (default: {DEFAULT_CORPUS_ROOT})",
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument(
        "--skip-symlink",
        action="store_true",
        help="Do not create wiki/corpus symlink",
    )
    p.add_argument(
        "--skip-move",
        action="store_true",
        help="Only rewrite markdown paths (assets already moved)",
    )
    return p.parse_args()


def move_assets(
    wiki_dir: Path, corpus_root: Path, dry_run: bool
) -> tuple[int, int, list[str]]:
    """Returns (files_moved, dirs_removed, slugs)."""
    sources = wiki_dir / "sources"
    moved = 0
    removed_dirs = 0
    slugs: list[str] = []

    for assets_dir in sorted(sources.glob("*/md/assets")):
        if not assets_dir.is_dir():
            continue
        slug = assets_dir.parent.parent.name
        dest_dir = slug_assets_dir(corpus_root, slug)
        slugs.append(slug)
        files = [f for f in assets_dir.iterdir() if f.is_file()]
        if not files:
            if not dry_run:
                assets_dir.rmdir()
            removed_dirs += 1
            continue
        print(f"{slug}: {len(files)} files -> {dest_dir}")
        if dry_run:
            moved += len(files)
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        for src in files:
            dest = dest_dir / src.name
            if dest.exists() and dest.stat().st_size != src.stat().st_size:
                stem, suffix = dest.stem, dest.suffix
                n = 2
                while dest.exists():
                    dest = dest_dir / f"{stem}-migrated-{n}{suffix}"
                    n += 1
            if dest.exists():
                src.unlink()
            else:
                shutil.move(str(src), str(dest))
            moved += 1
        try:
            assets_dir.rmdir()
            removed_dirs += 1
        except OSError:
            pass
    return moved, removed_dirs, slugs


def rewrite_wiki_markdown(wiki_dir: Path, dry_run: bool) -> int:
    changed = 0
    for md in sorted(wiki_dir.rglob("*.md")):
        rel = md.relative_to(wiki_dir)
        slug: str | None = None
        parts = rel.parts
        if len(parts) >= 3 and parts[0] == "sources" and parts[2] == "md":
            slug = parts[1]

        original = md.read_text(encoding="utf-8", errors="replace")
        updated = rewrite_legacy_asset_refs(original, slug=slug)
        if updated != original:
            changed += 1
            print(f"rewrite: {rel}")
            if not dry_run:
                md.write_text(updated, encoding="utf-8")
    return changed


def main() -> int:
    args = parse_args()
    wiki_dir = args.wiki_dir.expanduser().resolve()
    corpus_root = corpus_root_from_arg(args.corpus_root)

    if not wiki_dir.is_dir():
        print(f"wiki dir not found: {wiki_dir}", file=sys.stderr)
        return 1

    moved = dirs = 0
    if not args.skip_move:
        moved, dirs, _ = move_assets(wiki_dir, corpus_root, args.dry_run)

    rewritten = rewrite_wiki_markdown(wiki_dir, args.dry_run)

    if not args.skip_symlink and not args.dry_run:
        link = ensure_wiki_corpus_link(wiki_dir, corpus_root)
        vault_root = vault_root_from_wiki(wiki_dir)
        print(f"symlink: {vault_root / WIKI_CORPUS_LINK} -> {link.resolve()}")

    action = "Would" if args.dry_run else "Done"
    print(
        f"{action}: moved {moved} asset file(s), removed {dirs} empty assets/ dir(s), "
        f"rewrote {rewritten} markdown file(s)"
    )
    print(f"Corpus root: {corpus_root / 'corpus'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
