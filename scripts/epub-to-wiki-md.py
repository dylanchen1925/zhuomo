#!/usr/bin/env python3
"""Convert EPUB to per-spine-item Markdown under wiki/sources/<slug>/md/."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import ebooklib
from bs4 import BeautifulSoup, NavigableString, Tag
from ebooklib import epub


def slugify(text: str, max_len: int = 80) -> str:
    text = html.unescape(text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text or "section")[:max_len]


def node_to_md(node: Tag | NavigableString, lines: list[str]) -> None:
    if isinstance(node, NavigableString):
        text = str(node).strip()
        if text:
            lines.append(text)
        return

    if not isinstance(node, Tag):
        return

    name = node.name.lower()
    if name in {"script", "style", "svg", "img"}:
        return

    if name == "a" and node.get("name"):
        text = node.get_text(" ", strip=True)
        if (
            text
            and len(text) < 200
            and not text.startswith("_Toc")
            and not re.match(r"^Figure\s+\d", text, re.I)
        ):
            anchor = slugify(text)
            lines.append("")
            lines.append(f"## {text} {{#{anchor}}}")
            lines.append("")
        return

    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = min(int(name[1]) + 1, 6)  # h1 → ## to leave # for part title
        text = node.get_text(" ", strip=True)
        if text:
            anchor = slugify(text)
            lines.append("")
            lines.append(f"{'#' * level} {text} {{#{anchor}}}")
            lines.append("")
        return

    if name == "p":
        # Bold-only line as pseudo-heading (common in publisher EPUBs)
        bold = node.find(["b", "strong"])
        if bold and not node.get_text(strip=True).replace(bold.get_text(strip=True), "").strip():
            text = bold.get_text(" ", strip=True)
            if text and len(text) < 120:
                anchor = slugify(text)
                lines.append("")
                lines.append(f"## {text} {{#{anchor}}}")
                lines.append("")
                return
        text = node.get_text(" ", strip=True)
        if text:
            lines.append(text)
            lines.append("")
        return

    if name in {"ul", "ol"}:
        ordered = name == "ol"
        for i, li in enumerate(node.find_all("li", recursive=False), start=1):
            text = li.get_text(" ", strip=True)
            if not text:
                continue
            prefix = f"{i}." if ordered else "-"
            lines.append(f"{prefix} {text}")
        lines.append("")
        return

    if name == "table":
        rows = []
        for tr in node.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            if cells:
                rows.append(cells)
        if rows:
            lines.append("")
            lines.append("| " + " | ".join(rows[0]) + " |")
            lines.append("| " + " | ".join(["---"] * len(rows[0])) + " |")
            for row in rows[1:]:
                while len(row) < len(rows[0]):
                    row.append("")
                lines.append("| " + " | ".join(row[: len(rows[0])]) + " |")
            lines.append("")
        return

    for child in node.children:
        node_to_md(child, lines)


def html_to_markdown(content: bytes, part_title: str) -> tuple[str, list[str]]:
    soup = BeautifulSoup(content, "html.parser")
    body = soup.body or soup
    lines: list[str] = [f"# {part_title}", ""]
    for child in body.children:
        node_to_md(child, lines)
    md = "\n".join(lines)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    md = promote_standalone_titles(md)
    headings = re.findall(r"^#{1,6} (.+?) \{#", md, flags=re.MULTILINE)
    return md, headings


def promote_standalone_titles(md: str) -> str:
    """Turn short standalone lines (publisher section titles) into ## headings."""
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        next_content = lines[j].strip() if j < len(lines) else ""
        if (
            line
            and not line.startswith("#")
            and len(line) < 100
            and not line.endswith(".")
            and not line.endswith(":")
            and next_content
            and len(next_content) > 80
            and re.match(r"^[A-Za-z]", line)
        ):
            anchor = slugify(line)
            out.append(f"## {line} {{#{anchor}}}")
        else:
            out.append(lines[i])
        i += 1
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="EPUB → wiki/sources/<slug>/md/")
    parser.add_argument("epub", type=Path, help="Path to .epub file")
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory, e.g. wiki/sources/my-book/md",
    )
    parser.add_argument("--slug", type=str, default="", help="Source slug for index")
    args = parser.parse_args()

    book = epub.read_epub(str(args.epub))
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = args.slug or args.epub.stem
    index_lines = [
        "---",
        "type: source-md-corpus",
        f"raw: {args.epub}",
        "---",
        "",
        f"# Markdown corpus — {slug}",
        "",
        "Full EPUB text converted for provenance links. Concept pages cite `[[md/part-NNN#heading]]`.",
        "",
        "| Part | File | First headings |",
        "|------|------|----------------|",
    ]

    part = 0
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        name = item.get_name() or ""
        if "nav" in name.lower() or "toc" in name.lower():
            continue
        part += 1
        part_title = f"Part {part}"
        md, headings = html_to_markdown(item.get_content(), part_title)
        if len(md.strip()) < 80:
            part -= 1
            continue
        if headings:
            part_title = headings[0]
            md_lines = md.split("\n", 1)
            md = f"# {part_title}\n\n" + (md_lines[1] if len(md_lines) > 1 else "")
        fname = f"part-{part:03d}.md"
        (out_dir / fname).write_text(md, encoding="utf-8")
        preview = "; ".join(headings[:3]) if headings else name
        index_lines.append(f"| {part} | [[md/{fname}\\|{fname}]] | {preview[:120]} |")

    index_lines.extend(
        [
            "",
            "## Provenance link format",
            "",
            "On concept pages:",
            "",
            "```markdown",
            "## Evidence",
            "- [[md/part-003#tenant-common]] — Tenant common naming rules",
            "```",
            "",
        ]
    )
    (out_dir / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Wrote {part} parts to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
