#!/usr/bin/env python3
"""List sources with ingest_status partial or missing complete marker."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def scan_sources(wiki: Path) -> list[tuple[str, dict[str, str]]]:
    sources_dir = wiki / "sources"
    if not sources_dir.is_dir():
        return []
    rows: list[tuple[str, dict[str, str]]] = []
    for p in sorted(sources_dir.glob("*.md")):
        if p.name == "index.md":
            continue
        fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        status = fm.get("ingest_status", "")
        if status == "partial" or (status and status != "complete" and status != "archive-only"):
            rows.append((p.stem, fm))
        elif not status and "Topic map" in p.read_text(encoding="utf-8", errors="replace"):
            # legacy page without status — treat as unknown
            rows.append((p.stem, {**fm, "ingest_status": "(unset)"}))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="List partial / resume-needed sources")
    ap.add_argument("wiki", type=Path, help="Path to vault wiki/")
    args = ap.parse_args()
    rows = scan_sources(args.wiki)
    if not rows:
        print("INGEST RESUME: no partial sources found")
        return 0
    print("INGEST RESUME (partial / unset status)")
    print("-" * 60)
    for slug, fm in rows:
        status = fm.get("ingest_status", "?")
        nxt = fm.get("next_sections", "[]")
        deep = fm.get("concepts_deepened", "?")
        print(f"  {slug}")
        print(f"    status={status}  concepts_deepened={deep}  next_sections={nxt}")
        print(f"    → Ingest continue: {slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
