#!/usr/bin/env python3
"""Remove wikilink aliases inside markdown table rows.

Obsidian/GitHub tables split on `|`; `[[path|alias]]` breaks columns.
Fix: `[[path|alias]]` or `[[path\\|alias]]` → `[[path]]` in table rows only.
Also merges cells where a wikilink was already split across columns.

Does NOT rewrite table structure (preserves `||` row markers and column count).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PIPED_WIKILINK = re.compile(r"\[\[([^\]|\\]+)(?:\\?\|[^\]]+)?\]\]")
TABLE_SEP = re.compile(r"^\|[-: |]+\|$")
# Only wiki-style paths (not CLI `[[be ]` corpus artifacts).
NEEDS_FIX = re.compile(
    r"\[\[(?:domains|sources|concepts|notes)/[^\]]+?(?:\\?\|)[^\]]+?\]\]"
    r"|\[\[md/[^\]]+?(?:\\?\|)[^\]]+?\]\]"
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path, help="Path to wiki/")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def is_table_row(line: str) -> bool:
    s = line.strip()
    if not s.startswith("|"):
        return False
    return not TABLE_SEP.match(s)


def split_table_row(line: str) -> list[str]:
    inner = line.strip().strip("|")
    return [c.strip() for c in inner.split("|")]


def repair_split_cells(cells: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(cells):
        cell = cells[i]
        if "[[" in cell and "]]" not in cell:
            merged = cell
            i += 1
            while i < len(cells) and "]]" not in merged:
                merged += "|" + cells[i]
                i += 1
            out.append(merged)
        else:
            out.append(cell)
            i += 1
    return out


def strip_piped_aliases(text: str) -> str:
    return PIPED_WIKILINK.sub(r"[[\1]]", text)


def has_split_wikilink(cells: list[str]) -> bool:
    repaired = repair_split_cells(cells)
    if repaired == cells:
        return False
    merged = "|".join(repaired)
    return bool(re.search(r"\[\[(?:domains|sources|concepts|notes|md)/", merged))


def line_needs_fix(line: str) -> bool:
    if not is_table_row(line):
        return False
    if NEEDS_FIX.search(line):
        return True
    cells = split_table_row(line)
    return has_split_wikilink(cells)


def fix_table_line(line: str) -> tuple[str, bool]:
    if not line_needs_fix(line):
        return line, False
    cells = repair_split_cells(split_table_row(line))
    fixed_cells = [strip_piped_aliases(c) for c in cells]
    new_line = "| " + " | ".join(fixed_cells) + " |"
    changed = new_line != line.rstrip("\n")
    if line.endswith("\n"):
        new_line += "\n"
    return new_line, changed


def process_file(path: Path, dry_run: bool, verbose: bool) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    changes = 0
    new_lines: list[str] = []
    for line in lines:
        body = line.rstrip("\n")
        fixed, changed = fix_table_line(body)
        if changed:
            changes += 1
            if verbose:
                print(f"{path}")
                print(f"  - {body}")
                print(f"  + {fixed.rstrip()}")
            if not line.endswith("\n"):
                fixed = fixed.rstrip("\n")
            elif not fixed.endswith("\n"):
                fixed += "\n"
            new_lines.append(fixed)
        else:
            new_lines.append(line)
    if changes and not dry_run:
        path.write_text("".join(new_lines), encoding="utf-8")
    return changes


def main() -> int:
    args = parse_args()
    wiki = args.wiki_dir
    if not wiki.is_dir():
        print(f"Not a directory: {wiki}", file=sys.stderr)
        return 1
    total_files = 0
    total_lines = 0
    for path in sorted(wiki.rglob("*.md")):
        n = process_file(path, args.dry_run, args.verbose)
        if n:
            total_files += 1
            total_lines += n
    mode = "dry-run" if args.dry_run else "fixed"
    print(f"{mode}: {total_lines} table line(s) in {total_files} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
