#!/usr/bin/env python3
"""Lint wiki concept pages for missing inline Figure visuals."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FIGURE_NUM = re.compile(r"(?<![\w-])Figure\s+([\d\-\.]+)\b", re.I)
ANCHOR_FIGURE = re.compile(r"#figure-([\d\-\.]+)\b", re.I)
LEGACY_FIGURES = re.compile(r"^## Figures\s*$", re.M)
INLINE_IMG = re.compile(r"!\[Figure\s+([\d\-\.]+)\]", re.I)
MERMAID = re.compile(r"^```mermaid\s*$", re.M)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path, help="Path to vault wiki/ folder")
    p.add_argument(
        "--concepts-glob",
        default="concepts/*.md",
        help="Glob under wiki_dir for concept pages",
    )
    return p.parse_args()


def norm_fig(fig: str) -> str:
    return fig.strip().replace("_", "-").rstrip("-")


def split_body_evidence(text: str) -> tuple[str, str]:
    m = re.search(r"^## Evidence\s*$", text, re.M)
    if not m:
        return text, ""
    return text[: m.start()], text[m.start() :]


def collect_cited(text: str) -> set[str]:
    out: set[str] = set()
    for m in FIGURE_NUM.finditer(text):
        out.add(norm_fig(m.group(1)))
    for m in ANCHOR_FIGURE.finditer(text):
        out.add(norm_fig(m.group(1)))
    return out


def has_named_visual(text: str, fig: str) -> bool:
    f = re.escape(fig)
    if INLINE_IMG.search(text) and re.search(rf"!\[Figure\s+{f}\]", text, re.I):
        return True
    if re.search(rf"#figure-{fig.replace('.', '-')}\]\]", text, re.I):
        return True
    return False


def has_mermaid_in_body(body: str) -> bool:
    return bool(MERMAID.search(body))


def lint_page(path: Path, text: str) -> list[str]:
    issues: list[str] = []
    if LEGACY_FIGURES.search(text):
        issues.append("legacy ## Figures section (use inline embeds)")

    body, tail = split_body_evidence(text)
    cited = collect_cited(text)
    if not cited:
        return issues

    body_cited = collect_cited(body)
    for fig in sorted(cited):
        if not has_named_visual(text, fig):
            if fig in body_cited and has_mermaid_in_body(body):
                continue
            issues.append(f"Figure {fig}: no ![Figure {fig}] or source anchor link")

    for fig in sorted(collect_cited(tail) - body_cited):
        if has_named_visual(text, fig) and not has_named_visual(body, fig):
            if has_mermaid_in_body(body):
                continue
            issues.append(f"Figure {fig}: visual only under Evidence (move inline to body)")

    return issues


def main() -> int:
    args = parse_args()
    wiki_dir = args.wiki_dir.resolve()
    failures = 0

    for path in sorted(wiki_dir.glob(args.concepts_glob)):
        text = path.read_text(encoding="utf-8", errors="replace")
        if not collect_cited(text) and not LEGACY_FIGURES.search(text):
            continue
        issues = lint_page(path, text)
        if issues:
            failures += 1
            print(f"{path.relative_to(wiki_dir)}")
            for issue in issues:
                print(f"  - {issue}")

    if failures:
        print(f"\n{failures} concept page(s) with figure visual issues")
        return 1

    print("All cited figures have inline visuals")
    return 0


if __name__ == "__main__":
    sys.exit(main())
