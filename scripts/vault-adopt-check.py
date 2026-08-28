#!/usr/bin/env python3
"""Pre-flight check for Adopt vault — refuse destructive overwrite."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

MARKER = ".zhuomo-adopted"
CORPUS_DIRS = ("concepts", "sources", "domains")


def count_markdown(d: Path) -> int:
    if not d.is_dir():
        return 0
    return sum(1 for _ in d.rglob("*.md"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki", type=Path, help="Path to vault wiki/")
    args = ap.parse_args()
    wiki = args.wiki
    if not wiki.is_dir():
        print(f"ERROR: not a directory: {wiki}", file=sys.stderr)
        return 2

    marker = wiki / MARKER
    if marker.exists():
        print(f"OK: zhuomo marker present ({marker})")
        return 0

    total = 0
    for name in CORPUS_DIRS:
        total += count_markdown(wiki / name)

    if total == 0:
        print("OK: empty or no corpus markdown — safe to adopt/bootstrap merge")
        return 0

    print(f"REFUSE: non-empty corpus ({total} md files under concepts/sources/domains)")
    print("  Existing vault without .zhuomo-adopted marker.")
    print("  Use Adopt with explicit user confirmation to merge templates only,")
    print("  or pick a fresh wiki subdirectory.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
