#!/usr/bin/env python3
"""Convert Cisco EOT single-page HTML to wiki md corpus + combined raw markdown."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

PART_BOUNDARIES = [
    "About the Cisco Validated Design Program",
    "Technology Overview",
    "Solution Design",
    "Solution Deployment",
    "Generative Inferencing AI Model Deployment and Results",
    "About the Authors",
]


def slugify(text: str, max_len: int = 80) -> str:
    text = html.unescape(text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text or "section")[:max_len]


def heading_level(p_classes: list[str]) -> int:
    if "pToC_Subhead1" in p_classes:
        return 1
    if "pToC_Subhead2" in p_classes:
        return 2
    if "pToC_Subhead3" in p_classes:
        return 3
    return 0


def anchor_from_tag(tag: Tag) -> str | None:
    a = tag.find("a", attrs={"name": True})
    if a and a.get("name"):
        return slugify(a["name"])
    text = tag.get_text(strip=True)
    return slugify(text) if text else None


def inline_to_md(node: Tag | NavigableString) -> str:
    if isinstance(node, NavigableString):
        return html.unescape(str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name in {"script", "style"}:
        return ""
    if name == "a":
        href = node.get("href", "")
        text = node.get_text(strip=True)
        if href.startswith("#"):
            aid = slugify(href[1:])
            return f"[{text}](#{aid})" if text else ""
        if href.startswith("http"):
            return f"[{text}]({href})" if text else ""
        return text
    if name in {"b", "strong"}:
        inner = "".join(inline_to_md(c) for c in node.children)
        return f"**{inner.strip()}**" if inner.strip() else ""
    if name in {"i", "em"}:
        inner = "".join(inline_to_md(c) for c in node.children)
        return f"*{inner.strip()}*" if inner.strip() else ""
    if name == "br":
        return "\n"
    if name == "img":
        alt = node.get("alt", "image")
        src = node.get("src", "")
        if src:
            return f"![{alt}]({src})"
        return ""
    return "".join(inline_to_md(c) for c in node.children)


def block_to_md(tag: Tag) -> str:
    classes = tag.get("class", [])
    if "pToC_Subhead1" in classes or "pToC_Subhead2" in classes or "pToC_Subhead3" in classes:
        level = heading_level(classes)
        text = tag.get_text(strip=True)
        aid = anchor_from_tag(tag)
        prefix = "#" * level
        if aid:
            return f"{prefix} {text} {{#{aid}}}\n"
        return f"{prefix} {text}\n"
    if tag.name == "p":
        cls = " ".join(classes)
        if "pBullet" in cls or "pBulletCMT" in cls:
            body = inline_to_md(tag).strip()
            body = re.sub(r"^●\s*", "", body)
            return f"- {body}\n" if body else ""
        if "pBody" in cls or "pIndent" in cls or not cls:
            body = inline_to_md(tag).strip()
            return f"{body}\n\n" if body else ""
    if tag.name in {"ul", "ol"}:
        lines: list[str] = []
        for li in tag.find_all("li", recursive=False):
            body = inline_to_md(li).strip()
            if body:
                lines.append(f"- {body}")
        return "\n".join(lines) + "\n\n" if lines else ""
    if tag.name == "table":
        rows = []
        for tr in tag.find_all("tr"):
            cells = [inline_to_md(td).strip().replace("|", "\\|") for td in tr.find_all(["td", "th"])]
            if cells:
                rows.append("| " + " | ".join(cells) + " |")
        if not rows:
            return ""
        if len(rows) > 1:
            ncol = rows[0].count("|") - 1
            sep = "| " + " | ".join(["---"] * ncol) + " |"
            rows.insert(1, sep)
        return "\n".join(rows) + "\n\n"
    return ""


def extract_sections(wrapper: Tag) -> list[tuple[str, str]]:
    """Split by PART_BOUNDARIES on pToC_Subhead1 titles."""
    current_title = "front-matter"
    current_lines: list[str] = []
    sections: list[tuple[str, str]] = []

    def flush():
        nonlocal current_title, current_lines
        if current_lines:
            sections.append((current_title, "".join(current_lines).strip() + "\n"))
        current_lines = []

    for child in wrapper.find_all(["p", "table", "ul", "ol"]):
        if child.name == "p" and "pToC_Subhead1" in child.get("class", []):
            title = child.get_text(strip=True)
            if title in PART_BOUNDARIES or title == "Executive Summary" or title == "Solution Overview and Design":
                flush()
                current_title = title
        md = block_to_md(child)
        if md:
            current_lines.append(md)

    flush()
    return sections


def assign_parts(sections: list[tuple[str, str]]) -> list[tuple[int, str, str]]:
    """Map sections to part numbers."""
    part_titles = [
        "Executive Summary and Solution Overview",
        "Technology Overview",
        "Solution Design",
        "Solution Deployment",
        "Model Deployment and Results",
        "Appendices",
    ]
    # Merge early sections into part 1
    merged: list[str] = []
    part_idx = 0
    results: list[tuple[int, str, str]] = []
    buffer: list[str] = []

    boundary_map = {
        "Executive Summary": 1,
        "Solution Overview and Design": 1,
        "Technology Overview": 2,
        "Solution Design": 3,
        "Solution Deployment": 4,
        "Generative Inferencing AI Model Deployment and Results": 5,
        "About the Authors": 6,
        "Feedback": 6,
    }

    current_part = 1
    current_part_title = part_titles[0]
    current_content: list[str] = []

    for title, body in sections:
        if title in boundary_map:
            if current_content:
                results.append((current_part, current_part_title, "\n".join(current_content)))
            current_part = boundary_map[title]
            current_part_title = part_titles[current_part - 1] if current_part <= len(part_titles) else title
            current_content = [f"# {title}\n\n{body}"]
        else:
            if not current_content:
                current_content.append(f"# {title}\n\n{body}")
            else:
                current_content.append(body)

    if current_content:
        results.append((current_part, current_part_title, "\n".join(current_content)))

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Cisco EOT HTML → wiki md corpus")
    parser.add_argument("html", type=Path)
    parser.add_argument("--out", type=Path, required=True, help="wiki/sources/<slug>/md")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--raw-md", type=Path, help="combined raw markdown path")
    args = parser.parse_args()

    soup = BeautifulSoup(args.html.read_text(errors="replace"), "html.parser")
    wrapper = soup.select_one("#eot-doc-wrapper")
    if not wrapper:
        raise SystemExit("No #eot-doc-wrapper found")
    content = wrapper.select_one(".WordSection1") or wrapper
    sections = extract_sections(content)
    parts = assign_parts(sections)

    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    index_rows: list[str] = []
    combined: list[str] = []

    for num, title, body in parts:
        fname = f"part-{num:03d}.md"
        front = f"""---
type: source-md-part
source: {args.slug}
part: {num}
title: {title}
---

"""
        content = front + body
        (out / fname).write_text(content, encoding="utf-8")
        line_count = len(body.splitlines())
        index_rows.append(f"| {num} | [[md/{fname}\\|{fname}]] | {title} | {line_count} lines |")
        combined.append(f"---\npart: part-{num:03d}\ntitle: {title}\nsource: {args.slug}\n---\n\n{body}")

    index = f"""---
type: source-md-corpus
source: {args.slug}
---

# MD corpus — {args.slug}

| Part | File | Title | Size |
|------|------|-------|------|
{chr(10).join(index_rows)}
"""
    (out / "index.md").write_text(index, encoding="utf-8")

    if args.raw_md:
        args.raw_md.parent.mkdir(parents=True, exist_ok=True)
        args.raw_md.write_text("\n\n".join(combined), encoding="utf-8")

    print(f"Wrote {len(parts)} parts to {out}")


if __name__ == "__main__":
    main()
