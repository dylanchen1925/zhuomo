#!/usr/bin/env python3
"""Recover wiki damage from an over-aggressive fix-table-wikilink-pipes run.

1. Split merged source index rows (many parts on one line via lost newlines).
2. Restore `||` row separators corrupted to ` |  | ` before separator rows.
3. Rebuild sources/*/md/index.md bodies from part-*.md when mega-line detected.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MEGA_INDEX = re.compile(r"^\| \d+ \| \[\[md/part-\d+\.md\]\].*\|\| \d+ \|")
MERGED_ROW = re.compile(r" \|\| \d+ \| ")
DOMAIN_MERGED = re.compile(r"^\|.*\|\|")
SEP_CORRUPT = re.compile(r" \|  \| (?=---|\*\*\*)")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def split_merged_table_line(line: str) -> list[str]:
    if not line.strip().startswith("|") or " || " not in line:
        return [line]
    if not MERGED_ROW.search(line) and not DOMAIN_MERGED.match(line.strip()):
        return [line]
    chunks = line.split(" || ")
    rows = [chunks[0].rstrip()]
    for chunk in chunks[1:]:
        row = chunk if chunk.startswith("|") else "| " + chunk
        row = row.rstrip()
        if not row.endswith("|"):
            row += " |"
        rows.append(row)
    return rows


def first_preview(part_path: Path) -> str:
    for line in part_path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:][:120]
        if s and not s.startswith("---"):
            return s[:120]
    return ""


def rebuild_index_body(md_dir: Path) -> list[str] | None:
    index_path = md_dir / "index.md"
    if not index_path.is_file():
        return None
    parts = sorted(md_dir.glob("part-*.md"))
    if not parts:
        return None

    text = index_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith("|") and "Part" in line and "File" in line:
            header_end = i + 2  # header + separator
            break
    if header_end < 2:
        return None

    header = lines[:header_end]
    col_count = header[0].count("|") - 1
    rows: list[str] = []
    for part in parts:
        num = int(part.stem.split("-")[1])
        fname = part.name
        preview = first_preview(part)
        link = f"[[md/{fname}]]"
        if col_count >= 5:
            rows.append(f"| {num} | {link} | — | — | {preview} |")
        elif col_count == 4:
            rows.append(f"| {num} | {link} | — | {preview} |")
        else:
            rows.append(f"| {num} | {link} | {preview} |")

    tail_start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Provenance link format":
            tail_start = i
            break
    tail = lines[tail_start:] if tail_start is not None else []
    return header + rows + ([""] if tail else []) + tail


def process_file(path: Path, dry_run: bool) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text
    lines = text.splitlines()
    new_lines: list[str] = []
    splits = 0
    sep_fixes = 0

    for line in lines:
        if MEGA_INDEX.match(line.strip()):
            rebuilt = rebuild_index_body(path.parent)
            if rebuilt is not None:
                # replace entire file via rebuild at first mega line — handled below
                pass
        expanded = split_merged_table_line(line)
        splits += max(0, len(expanded) - 1)
        for exp in expanded:
            fixed, n = SEP_CORRUPT.subn(" || ", exp)
            sep_fixes += n
            new_lines.append(fixed)

    if path.name == "index.md" and any(MEGA_INDEX.match(l.strip()) for l in lines):
        rebuilt = rebuild_index_body(path.parent)
        if rebuilt is not None:
            new_text = "\n".join(rebuilt) + "\n"
            if new_text != original:
                if not dry_run:
                    path.write_text(new_text, encoding="utf-8")
                return splits + 1, sep_fixes

    new_text = "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")
    if new_text != original:
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")
    return splits, sep_fixes


def main() -> int:
    args = parse_args()
    wiki = args.wiki_dir
    total_splits = 0
    total_sep = 0
    files = 0
    for path in sorted(wiki.rglob("*.md")):
        splits, sep = process_file(path, args.dry_run)
        if splits or sep:
            files += 1
            total_splits += splits
            total_sep += sep
    mode = "dry-run" if args.dry_run else "recovered"
    print(f"{mode}: {files} file(s); {total_splits} row split(s); {total_sep} separator fix(es)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
