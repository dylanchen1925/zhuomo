#!/usr/bin/env python3
"""Remove image files in wiki/sources/*/md/assets/ not referenced by any wiki markdown."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path, help="Path to vault wiki/ folder")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    wiki_dir = args.wiki_dir.resolve()
    sources = wiki_dir / "sources"
    combined = "\n".join(
        p.read_text(encoding="utf-8", errors="replace")
        for p in wiki_dir.rglob("*.md")
    )

    removed = 0
    for assets_dir in sorted(sources.glob("*/md/assets")):
        for img in sorted(assets_dir.iterdir()):
            if not img.is_file():
                continue
            name = img.name
            if name in combined or f"assets/{name}" in combined:
                continue
            removed += 1
            rel = img.relative_to(wiki_dir)
            print(rel)
            if not args.dry_run:
                img.unlink()

    action = "Would remove" if args.dry_run else "Removed"
    print(f"{action} {removed} orphan asset(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
