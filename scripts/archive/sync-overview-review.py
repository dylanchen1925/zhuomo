#!/usr/bin/env python3
"""Sync Review and Explain-back columns in domain overview progress tables from concept frontmatter."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
PROGRESS_HEADINGS = ("## 学习进度", "## 进度")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path, help="Path to wiki/ (contains concepts/)")
    p.add_argument(
        "--overview",
        action="append",
        default=[],
        help="Path to domains/<domain>/overview.md (repeatable)",
    )
    p.add_argument("--write", action="store_true", help="Write changes (default: dry-run)")
    return p.parse_args()


def fm_val(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    return v or None


def read_concept_meta(concepts_dir: Path, slug: str) -> dict[str, str | None]:
    path = concepts_dir / f"{slug}.md"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FM_RE.match(text)
    fm = m.group(1) if m else ""
    return {
        "reviewed": fm_val(fm, "reviewed"),
        "explain_back": fm_val(fm, "explain_back") or "not_started",
        "mastery": fm_val(fm, "mastery") or fm_val(fm, "status") or "learning",
    }


def slug_from_cell(cell: str) -> str | None:
    m = WIKILINK_RE.search(cell)
    if not m:
        return None
    slug = m.group(1).strip()
    if slug.startswith("sources/") or slug.startswith("domains/"):
        return None
    return slug.split("/")[-1]


def split_table_row(line: str) -> list[str]:
    inner = line.strip().strip("|")
    return [c.strip() for c in inner.split("|")]


def find_progress_section(lines: list[str]) -> tuple[int, int] | None:
    start = None
    for i, line in enumerate(lines):
        if line.strip() in PROGRESS_HEADINGS:
            start = i
            break
    if start is None:
        return None
    end = start + 1
    while end < len(lines) and not (lines[end].startswith("## ") and end > start + 2):
        end += 1
    return start, end


def normalize_header(cells: list[str]) -> list[str]:
    """Ensure progress table has Review and Explain-back columns."""
    lower = [c.lower() for c in cells]
    if "review" in lower and "explain-back" in lower:
        return cells
    # Insert after mastery/status column
    out: list[str] = []
    inserted = False
    for c in cells:
        out.append(c)
        cl = c.lower()
        if not inserted and cl in ("掌握度", "status", "mastery"):
            out.extend(["Review", "Explain-back"])
            inserted = True
    if not inserted and len(cells) >= 2:
        out = cells[:2] + ["Review", "Explain-back"] + cells[2:]
    return out


def pad_row(cells: list[str], width: int) -> list[str]:
    if len(cells) < width:
        return cells + [""] * (width - len(cells))
    return cells[:width]


def sync_table_block(
    block_lines: list[str], concepts_dir: Path
) -> tuple[list[str], int]:
    """Return updated block and number of rows changed."""
    if not block_lines:
        return block_lines, 0
    out: list[str] = []
    changes = 0
    header_width = 0
    review_idx = explain_idx = mastery_idx = -1

    for line in block_lines:
        if not line.strip().startswith("|"):
            out.append(line)
            continue
        cells = split_table_row(line)
        if all(set(c) <= {"-", " "} for c in cells):
            if header_width:
                out.append("|" + "|".join([" --- "] * header_width) + "|")
            else:
                out.append(line)
            continue

        if header_width == 0:
            cells = normalize_header(cells)
            header_width = len(cells)
            lower = [c.lower() for c in cells]
            review_idx = lower.index("review") if "review" in lower else -1
            explain_idx = lower.index("explain-back") if "explain-back" in lower else -1
            mastery_idx = next(
                (i for i, c in enumerate(lower) if c in ("掌握度", "status", "mastery")),
                -1,
            )
            out.append("|" + "|".join(f" {c} " for c in cells) + "|")
            continue

        cells = pad_row(cells, header_width)
        slug = slug_from_cell(cells[0])
        if slug:
            meta = read_concept_meta(concepts_dir, slug)
            if meta:
                if review_idx >= 0:
                    new_review = meta["reviewed"] or "—"
                    if cells[review_idx] != new_review:
                        changes += 1
                    cells[review_idx] = new_review
                if explain_idx >= 0:
                    eb = meta["explain_back"] or "not_started"
                    if cells[explain_idx] != eb:
                        changes += 1
                    cells[explain_idx] = eb
                if mastery_idx >= 0 and meta.get("mastery"):
                    cells[mastery_idx] = meta["mastery"]

        out.append("|" + "|".join(f" {c} " for c in cells) + "|")

    return out, changes


def sync_overview(path: Path, concepts_dir: Path, write: bool) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    bare = [ln.rstrip("\n") for ln in lines]
    section = find_progress_section(bare)
    if not section:
        print(f"{path}: no progress section found", file=sys.stderr)
        return 1

    start, end = section
    block = bare[start:end]
    updated_block, changes = sync_table_block(block, concepts_dir)
    if changes == 0 and "Review" in "".join(block):
        print(f"{path}: already synced ({changes} row updates)")
        return 0

    new_bare = bare[:start] + updated_block + bare[end:]
    new_text = "\n".join(new_bare)
    if text.endswith("\n"):
        new_text += "\n"

    print(f"{path}: {changes} row(s) updated")
    if write:
        path.write_text(new_text, encoding="utf-8")
    else:
        print("  (dry-run; pass --write to save)")
    return 0


def default_overviews(wiki: Path) -> list[Path]:
    domains = wiki / "domains"
    paths = []
    for name in ("cisco-aci", "ai-dc-networking", "technical-analysis"):
        p = domains / name / "overview.md"
        if p.is_file():
            paths.append(p)
    return paths


def main() -> int:
    args = parse_args()
    wiki = args.wiki_dir.resolve()
    concepts = wiki / "concepts"
    if not concepts.is_dir():
        print(f"Missing concepts dir: {concepts}", file=sys.stderr)
        return 1

    overviews = [Path(p).resolve() for p in args.overview] or default_overviews(wiki)
    rc = 0
    for ov in overviews:
        if not ov.is_file():
            print(f"Not found: {ov}", file=sys.stderr)
            rc = 1
            continue
        rc |= sync_overview(ov, concepts, args.write)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
