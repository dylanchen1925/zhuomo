#!/usr/bin/env python3
"""Split monolithic chan blog md into per-lesson files under md/lessons/."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TOC_LINE = re.compile(r"^\s*\d+\.\s+")
LESSON_IN_LINE = re.compile(
    r"教你炒\s*股\s*票\s*([\d\s]+)\s*[：:]\s*(.*)$"
)


def lesson_num(raw: str) -> int:
    return int(re.sub(r"\s+", "", raw))


def split_lessons(part_path: Path, out_dir: Path) -> list[tuple[int, str, Path]]:
    lines = part_path.read_text(encoding="utf-8").splitlines()
    candidates: dict[int, list[tuple[int, str, bool]]] = {}

    for i, line in enumerate(lines):
        m = LESSON_IN_LINE.search(line)
        if not m:
            continue
        num = lesson_num(m.group(1))
        if num < 1 or num > 108:
            continue
        tail = m.group(2).strip()
        is_toc = bool(TOC_LINE.match(line))
        candidates.setdefault(num, []).append((i, tail, is_toc))

    starts: list[tuple[int, int, str]] = []
    for num in sorted(candidates):
        opts = candidates[num]
        body = [o for o in opts if not o[2]]
        pick = body[0] if body else opts[0]
        starts.append((num, pick[0], pick[1]))

    out_dir.mkdir(parents=True, exist_ok=True)
    results: list[tuple[int, str, Path]] = []

    for idx, (num, start_i, tail) in enumerate(starts):
        end_i = starts[idx + 1][1] if idx + 1 < len(starts) else len(lines)
        chunk = lines[start_i:end_i]
        title = re.sub(r"\s*\(\d{4}-\d{2}-\d{2}.*\)\s*$", "", tail).strip()
        title = re.sub(r"\s+", " ", title)
        fname = f"lesson-{num:03d}.md"
        dest = out_dir / fname
        header = f"# 教你炒股票{num}：{title}\n\n"
        body = "\n".join(chunk)
        dest.write_text(header + body + "\n", encoding="utf-8")
        results.append((num, title, dest))

    return results


def write_index(
    index_path: Path,
    results: list[tuple[int, str, Path]],
    part_path: Path,
) -> None:
    rows = [
        "---",
        "type: source-lesson-index",
        f"corpus: {part_path.name}",
        "---",
        "",
        "# 教你炒股票 — lesson index",
        "",
        "Per-lesson files extracted from monolithic blog corpus. Prefer these for Evidence links.",
        "",
        "| 课 | File | 标题 |",
        "|----|------|------|",
    ]
    for num, title, dest in sorted(results, key=lambda x: x[0]):
        rel = f"lessons/{dest.name}"
        safe_title = title.replace("|", "/")[:80]
        rows.append(f"| {num} | [[md/{rel}\\|lesson-{num:03d}]] | {safe_title} |")
    missing = [n for n in range(1, 109) if n not in {r[0] for r in results}]
    rows.extend(
        [
            "",
            f"**Extracted:** {len(results)} / 108 lessons.",
        ]
    )
    if missing:
        rows.append(f"**Missing:** {missing[:20]}{'…' if len(missing) > 20 else ''}")
    rows.append("")
    index_path.write_text("\n".join(rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("part_md", type=Path, help="Monolithic part-001.md")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output lessons dir (default: part_md.parent/lessons)",
    )
    args = parser.parse_args()
    out_dir = args.out or (args.part_md.parent / "lessons")
    if out_dir.exists():
        for f in out_dir.glob("lesson-*.md"):
            f.unlink()
    results = split_lessons(args.part_md, out_dir)
    write_index(args.part_md.parent / "stock-lessons-index.md", results, args.part_md)
    print(f"Extracted {len(results)} lessons to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
