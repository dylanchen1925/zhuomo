#!/usr/bin/env python3
"""Lint wiki concepts for review queue: stale reads, missing explain-back sections."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path)
    p.add_argument("--concepts-glob", default="concepts/*.md")
    return p.parse_args()


def fm_val(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    return v or None


def has_evidence(body: str) -> bool:
    return bool(re.search(r"^## Evidence\s*$", body, re.M))


def has_explain_back_section(body: str) -> bool:
    return bool(re.search(r"^## Explain-back\s*$", body, re.M))


def main() -> int:
    args = parse_args()
    wiki = args.wiki_dir.resolve()
    issues = 0

    for path in sorted(wiki.glob(args.concepts_glob)):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = FM_RE.match(text)
        fm = m.group(1) if m else ""
        body = text[m.end() :] if m else text

        if not has_evidence(body):
            continue

        name = path.stem
        reviewed = fm_val(fm, "reviewed")
        wiki_revised = fm_val(fm, "wiki_revised") or fm_val(fm, "revised")
        explain_back = fm_val(fm, "explain_back") or "not_started"
        mastery = fm_val(fm, "mastery") or fm_val(fm, "status")

        rel = path.relative_to(wiki)
        page_issues: list[str] = []

        if wiki_revised and DATE_RE.match(wiki_revised):
            if not reviewed or wiki_revised > reviewed:
                page_issues.append(f"wiki_revised {wiki_revised} > reviewed {reviewed or '—'}")
        elif not reviewed:
            page_issues.append("never reviewed")

        if not has_explain_back_section(body):
            page_issues.append("missing ## Explain-back section")

        if reviewed and explain_back not in ("passed",):
            page_issues.append(f"reviewed but explain_back={explain_back}")

        if page_issues:
            issues += 1
            print(f"{rel}")
            for i in page_issues:
                print(f"  - {i}")

    if issues:
        print(f"\n{issues} concept(s) in review queue")
        return 1
    print("Review queue empty")
    return 0


if __name__ == "__main__":
    sys.exit(main())
