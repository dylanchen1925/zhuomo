#!/usr/bin/env python3
"""OCR scanned PDF pages to per-chapter Markdown under wiki/sources/<slug>/md/."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# 释放你的炒股潜力 — 薛松 (A5 scan, 286 PDF pages). Printed page + 12 = PDF page.
XUESONG_SHIFANG_CHAPTERS: list[tuple[str, int, int]] = [
    ("Front Matter", 1, 13),
    ("三种钱与5%抄底时机", 14, 20),
    ("RSI指标实战指数与个股", 21, 33),
    ("分时的最大秘密", 34, 52),
    ("卷王孤勇者与跳着脚追", 53, 63),
    ("卖出指标与只吃一段抄底", 64, 78),
    ("涨停游戏至刀起刀落", 79, 104),
    ("圈住富贵至低位股AB面", 105, 121),
    ("25%无赖打法至量价真实", 122, 139),
    ("与牛共舞至跟随趋势", 140, 158),
    ("极限迸发至成功路径", 159, 195),
    ("下篇归真 有术无道至概率思维", 196, 228),
    ("下篇 楚门世界至扛过逆境", 229, 274),
    ("后记", 275, 286),
]

PRESETS: dict[str, list[tuple[str, int, int]]] = {
    "xuesong-shifang-potential": XUESONG_SHIFANG_CHAPTERS,
    "shifang-potential": XUESONG_SHIFANG_CHAPTERS,
    "释放你的炒股潜力": XUESONG_SHIFANG_CHAPTERS,
}


def slugify(text: str, max_len: int = 80) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s\u4e00-\u9fff-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text or "section")[:max_len]


def ocr_page(pdf: Path, page: int, dpi: int, lang: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "page"
        subprocess.run(
            [
                "pdftoppm",
                "-png",
                "-f",
                str(page),
                "-l",
                str(page),
                "-r",
                str(dpi),
                str(pdf),
                str(prefix),
            ],
            check=True,
            capture_output=True,
        )
        pngs = sorted(Path(tmp).glob("page-*.png"))
        if not pngs:
            return ""
        result = subprocess.run(
            ["tesseract", str(pngs[0]), "stdout", "-l", lang],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return ""
        return result.stdout


def clean_ocr(text: str) -> str:
    lines = [ln.rstrip() for ln in text.splitlines()]
    out: list[str] = []
    for line in lines:
        if not line.strip():
            if out and out[-1] != "":
                out.append("")
            continue
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def promote_headings(md: str, title: str) -> tuple[str, list[str]]:
    headings: list[str] = [title]
    lines = md.split("\n")
    out: list[str] = [f"# {title}", ""]
    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append("")
            continue
        if stripped == title:
            continue
        # Short standalone lines likely headings (Chinese or mixed)
        if len(stripped) <= 40 and not stripped.endswith(("。", "，", "；", "：", "?", "？")):
            if re.match(r"^[\u4e00-\u9fffA-Za-z0-9（）()「」\s·—-]+$", stripped):
                if len(stripped) >= 4:
                    anchor = slugify(stripped)
                    out.append(f"## {stripped} {{#{anchor}}}")
                    headings.append(stripped)
                    out.append("")
                    continue
        out.append(line)
    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return body, headings


def main() -> int:
    parser = argparse.ArgumentParser(description="OCR scanned PDF → wiki/sources/<slug>/md/")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--slug", type=str, default="")
    parser.add_argument("--preset", type=str, default="")
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--lang", type=str, default="chi_sim+eng")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = args.slug or pdf.stem.lower()

    preset_key = args.preset or slug
    chapters = PRESETS.get(preset_key)
    if not chapters:
        print(f"No OCR preset for {preset_key!r}", file=sys.stderr)
        return 1

    index_lines = [
        "---",
        "type: source-md-corpus",
        f"raw: {pdf}",
        "ocr: tesseract chi_sim+eng",
        "---",
        "",
        f"# Markdown corpus — {slug}",
        "",
        "Scanned PDF OCR for provenance links. Concept pages cite `[[md/part-NNN#heading]]`.",
        "",
        "| Part | File | Chapter | PDF pages | First headings |",
        "|------|------|---------|-----------|----------------|",
    ]

    part = 0
    for title, start, end in chapters:
        pages_text: list[str] = []
        for page in range(start, end + 1):
            raw = clean_ocr(ocr_page(pdf, page, args.dpi, args.lang))
            if raw:
                pages_text.append(f"<!-- pdf-page {page} -->\n\n{raw}")
            if page % 10 == 0:
                print(f"  OCR page {page}/{end} ({title})", file=sys.stderr)
        combined = "\n\n".join(pages_text)
        if len(combined.strip()) < 40:
            continue
        part += 1
        md, headings = promote_headings(combined, title)
        fname = f"part-{part:03d}.md"
        (out_dir / fname).write_text(md, encoding="utf-8")
        preview = "; ".join(headings[:3])
        index_lines.append(
            f"| {part} | [[md/{fname}\\|{fname}]] | {title} | {start}–{end} | {preview[:100]} |"
        )
        print(f"Wrote {fname} ({start}-{end})", file=sys.stderr)

    index_lines.extend(
        [
            "",
            "## Provenance link format",
            "",
            "```markdown",
            "## Evidence",
            "- [[md/part-002#rsi指标实战应用之指数篇]] — RSI chapter",
            "```",
            "",
        ]
    )
    (out_dir / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Done: {part} parts → {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
