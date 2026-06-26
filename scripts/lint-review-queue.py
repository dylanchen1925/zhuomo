#!/usr/bin/env python3
"""Lint wiki concepts: review queue, solid candidates, read-but-untested."""

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
    p.add_argument("--domain", default=None, help="Filter by domain slug")
    return p.parse_args()


def fm_val(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    if not v or v.startswith("explain_back:"):
        return None
    return v


def has_evidence(body: str) -> bool:
    return bool(re.search(r"^## Evidence\s*$", body, re.M))


def has_explain_back_section(body: str) -> bool:
    return bool(re.search(r"^## Explain-back\s*$", body, re.M))


def main() -> int:
    args = parse_args()
    wiki = args.wiki_dir.resolve()
    buckets: dict[str, list[tuple[str, list[str]]]] = {
        "solid_candidate": [],
        "read_untested": [],
        "stale": [],
        "never_reviewed": [],
        "missing_explain_back": [],
    }

    for path in sorted(wiki.glob(args.concepts_glob)):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = FM_RE.match(text)
        fm = m.group(1) if m else ""
        body = text[m.end() :] if m else text

        if not has_evidence(body):
            continue

        domain = fm_val(fm, "domain")
        if args.domain and domain != args.domain:
            continue

        reviewed = fm_val(fm, "reviewed")
        page_updated = fm_val(fm, "updated") or fm_val(fm, "wiki_revised") or fm_val(fm, "revised")
        explain_back = fm_val(fm, "explain_back") or "not_started"
        mastery = fm_val(fm, "mastery") or fm_val(fm, "status") or "learning"

        rel = str(path.relative_to(wiki))

        if explain_back == "passed" and mastery != "solid":
            buckets["solid_candidate"].append((rel, ["Promote to solid"]))
            continue

        if reviewed and explain_back != "passed":
            buckets["read_untested"].append(
                (rel, [f"reviewed={reviewed}, explain_back={explain_back}"])
            )

        if not has_explain_back_section(body):
            buckets["missing_explain_back"].append((rel, ["missing ## Explain-back section"]))

        if page_updated and DATE_RE.match(page_updated):
            if not reviewed or page_updated > reviewed:
                buckets["stale"].append(
                    (rel, [f"updated {page_updated} > reviewed {reviewed or '—'}"])
                )
        elif not reviewed:
            buckets["never_reviewed"].append((rel, ["never reviewed"]))

    total = 0
    labels = {
        "solid_candidate": "SOLID_CANDIDATE (explain_back passed, not solid)",
        "read_untested": "READ_UNTESTED (reviewed, explain_back not passed)",
        "stale": "STALE (updated > reviewed)",
        "never_reviewed": "NEVER_REVIEWED",
        "missing_explain_back": "MISSING_EXPLAIN_BACK_SECTION",
    }
    for key in labels:
        items = buckets[key]
        if not items:
            continue
        print(f"\n=== {labels[key]} ({len(items)}) ===")
        for rel, notes in items:
            print(rel)
            for n in notes:
                print(f"  - {n}")
        total += len(items)

    if total:
        print(f"\n{total} concept(s) flagged")
        return 1
    print("Review queue empty")
    return 0


if __name__ == "__main__":
    sys.exit(main())
