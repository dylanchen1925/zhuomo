#!/usr/bin/env python3
"""Remove corpus image files not referenced by any wiki markdown."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from corpus_assets import DEFAULT_CORPUS_ROOT, corpus_root_from_arg


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path, help="Path to vault wiki/ folder")
    p.add_argument(
        "--corpus-root",
        type=Path,
        default=DEFAULT_CORPUS_ROOT,
        help=f"External corpus root (default: {DEFAULT_CORPUS_ROOT})",
    )
    p.add_argument("--dry-run", action="store_true")
    p.add_argument(
        "--slug",
        action="append",
        default=[],
        help="Limit cleanup to corpus slug(s), e.g. cisco-sdwan-design-guide (repeatable)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    wiki_dir = args.wiki_dir.resolve()
    corpus_root = corpus_root_from_arg(args.corpus_root)
    corpus_dir = corpus_root / "corpus"
    combined = "\n".join(
        p.read_text(encoding="utf-8", errors="replace")
        for p in wiki_dir.rglob("*.md")
    )

    removed = 0
    if not corpus_dir.is_dir():
        print(f"No corpus dir at {corpus_dir}")
        return 0

    slug_filter = set(args.slug)
    asset_dirs = sorted(corpus_dir.glob("*/assets"))
    if slug_filter:
        asset_dirs = [d for d in asset_dirs if d.parent.name in slug_filter]

    for assets_dir in asset_dirs:
        for img in sorted(assets_dir.iterdir()):
            if not img.is_file():
                continue
            slug = assets_dir.parent.name
            name = img.name
            if (
                name in combined
                or f"/corpus/{slug}/assets/{name}" in combined
                or f"sources/{slug}/md/assets/{name}" in combined
                or f"assets/{name}" in combined
            ):
                continue
            removed += 1
            print(img)
            if not args.dry_run:
                img.unlink()

    action = "Would remove" if args.dry_run else "Removed"
    print(f"{action} {removed} orphan asset(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
