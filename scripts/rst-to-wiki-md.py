#!/usr/bin/env python3
"""Convert Sphinx/RST book repo to per-section Markdown under wiki/sources/<slug>/md/."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from corpus_assets import DEFAULT_CORPUS_ROOT, asset_vault_path, corpus_root_from_arg, slug_assets_dir

# Book reading order (index.rst toctree, excluding meta pages).
CHAPTER_ROOTS = [
    "foreword.rst",
    "foreword_1e.rst",
    "preface.rst",
    "foundation.rst",
    "direct.rst",
    "internetworking.rst",
    "scaling.rst",
    "e2e.rst",
    "congestion.rst",
    "data.rst",
    "security.rst",
    "applications.rst",
]

SECURITY_CHAPTER_ROOTS = [
    "foreword.rst",
    "preface.rst",
    "intro.rst",
    "principles.rst",
    "crypto.rst",
    "key-distro.rst",
    "authentication.rst",
    "tls.rst",
    "systems.rst",
    "infra.rst",
    "firewall.rst",
]

TCPCC_CHAPTER_ROOTS = [
    "foreword.rst",
    "preface.rst",
    "intro.rst",
    "tcp_ip.rst",
    "design.rst",
    "algorithm.rst",
    "avoidance.rst",
    "aqm.rst",
    "variants.rst",
    "biblio.rst",
]

SDN_CHAPTER_ROOTS = [
    "foreword.rst",
    "preface.rst",
    "intro.rst",
    "uses.rst",
    "arch.rst",
    "switch.rst",
    "stratum.rst",
    "onos.rst",
    "trellis.rst",
    "netvirt.rst",
    "access.rst",
    "future.rst",
]

PRESETS: dict[str, list[str]] = {
    "book": CHAPTER_ROOTS,
    "security": SECURITY_CHAPTER_ROOTS,
    "tcpcc": TCPCC_CHAPTER_ROOTS,
    "sdn": SDN_CHAPTER_ROOTS,
}


def slugify(text: str, max_len: int = 80) -> str:
    text = re.sub(r"\{#[^}]+\}", "", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text or "section")[:max_len]


def parse_toctree(rst_path: Path) -> list[str]:
    text = rst_path.read_text(encoding="utf-8")
    entries: list[str] = []
    in_tree = False
    for line in text.splitlines():
        if line.strip().startswith(".. toctree::"):
            in_tree = True
            continue
        if in_tree:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(":"):
                continue
            if stripped.endswith(".rst"):
                entries.append(stripped)
            else:
                in_tree = False
    return entries


def collect_rst_files(book_root: Path) -> list[Path]:
    return collect_rst_files_for_roots(book_root, CHAPTER_ROOTS)


def collect_rst_files_for_roots(book_root: Path, roots: list[str]) -> list[Path]:
    ordered: list[Path] = []
    seen: set[Path] = set()

    def add(path: Path) -> None:
        path = path.resolve()
        if path.exists() and path not in seen:
            seen.add(path)
            ordered.append(path)

    for entry in roots:
        path = book_root / entry
        add(path)
        for sub in parse_toctree(path):
            add(book_root / sub)
    return ordered


def pandoc_convert(rst_path: Path, book_root: Path) -> str:
    result = subprocess.run(
        ["pandoc", "-f", "rst", "-t", "markdown", "--wrap=none", str(rst_path)],
        capture_output=True,
        text=True,
        cwd=str(book_root),
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc failed on {rst_path}: {result.stderr[:500]}")
    return result.stdout


def add_heading_anchors(md: str) -> tuple[str, list[str]]:
    headings: list[str] = []

    def repl(m: re.Match[str]) -> str:
        level = len(m.group(1))
        title = m.group(2).strip()
        anchor = slugify(title)
        headings.append(title)
        return f"{'#' * level} {title} {{#{anchor}}}"

    md = re.sub(r"^(#{1,6})\s+(.+)$", repl, md, flags=re.MULTILINE)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    return md, headings


def fix_image_paths(md: str, rst_path: Path, assets_dir: Path, book_root: Path, slug: str) -> str:
    def copy_and_relink(match: re.Match[str]) -> str:
        alt = match.group(1)
        src = match.group(2)
        if src.startswith(("http://", "https://", "data:")):
            return match.group(0)
        src_path = (rst_path.parent / src).resolve()
        if not src_path.exists():
            src_path = (book_root / src).resolve()
        if not src_path.exists():
            return match.group(0)
        dest = assets_dir / src_path.name
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest)
        return f"![{alt}]({asset_vault_path(slug, dest.name)})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", copy_and_relink, md)


def main() -> int:
    parser = argparse.ArgumentParser(description="RST book repo → wiki/sources/<slug>/md/")
    parser.add_argument("book_root", type=Path, help="Root of cloned RST book repo")
    parser.add_argument("--out", type=Path, required=True, help="Output dir, e.g. wiki/sources/foo/md")
    parser.add_argument("--slug", type=str, default="", help="Source slug for index")
    parser.add_argument(
        "--corpus-root",
        type=Path,
        default=DEFAULT_CORPUS_ROOT,
        help=f"External corpus root (default: {DEFAULT_CORPUS_ROOT})",
    )
    parser.add_argument(
        "--preset",
        type=str,
        default="book",
        choices=sorted(PRESETS),
        help="Chapter root list (default: book = Computer Networks)",
    )
    args = parser.parse_args()

    book_root = args.book_root.resolve()
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = args.slug or book_root.name
    corpus_root = corpus_root_from_arg(args.corpus_root)
    assets_dir = slug_assets_dir(corpus_root, slug)
    assets_dir.mkdir(parents=True, exist_ok=True)
    chapter_roots = PRESETS[args.preset]

    rst_files = collect_rst_files_for_roots(book_root, chapter_roots)

    index_lines = [
        "---",
        "type: source-md-corpus",
        f"raw: {book_root}",
        "---",
        "",
        f"# Markdown corpus — {slug}",
        "",
        "Full RST text converted for provenance links. Concept pages cite `[[md/part-NNN#heading]]`.",
        "",
        "| Part | File | Source RST | First headings |",
        "|------|------|------------|----------------|",
    ]

    part = 0
    image_names: set[str] = set()

    for rst_path in rst_files:
        md = pandoc_convert(rst_path, book_root)
        if len(md.strip()) < 60:
            continue
        md, headings = add_heading_anchors(md)
        md = fix_image_paths(md, rst_path, assets_dir, book_root, slug)
        for m in re.finditer(rf"\]\({ASSETS_DIR}/([^)]+)\)", md):
            image_names.add(m.group(1))

        part += 1
        title = headings[0] if headings else rst_path.stem
        if not md.startswith("#"):
            md = f"# {title}\n\n{md}"
        fname = f"part-{part:03d}.md"
        (out_dir / fname).write_text(md, encoding="utf-8")
        rel_rst = rst_path.relative_to(book_root)
        preview = "; ".join(headings[:3]) if headings else rel_rst.stem
        index_lines.append(
            f"| {part} | [[md/{fname}\\|{fname}]] | `{rel_rst}` | {preview[:100]} |"
        )

    if image_names:
        index_lines.insert(
            8,
            f"Images extracted to `md/{ASSETS_DIR}/` ({len(image_names)} files) and embedded in part Markdown.\n",
        )

    index_lines.extend(
        [
            "",
            "## Provenance link format",
            "",
            "On concept pages:",
            "",
            "```markdown",
            "## Evidence",
            "- [[md/part-003#internetworking]] — Internetworking chapter",
            "```",
            "",
        ]
    )
    (out_dir / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Wrote {part} parts to {out_dir}; {len(image_names)} images in {ASSETS_DIR}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
