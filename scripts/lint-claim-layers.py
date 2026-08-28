#!/usr/bin/env python3
"""Flag concepts missing ### Formal: (two-layer Claim rubric)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FORMAL_RE = re.compile(r"^### Formal:", re.M)
OPTIONAL_DOMAINS = frozenset({"craft-writing", "chinese-history-culture", "games-people-play-berne"})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wiki", type=Path)
    ap.add_argument("--domain", help="Filter by domain slug")
    args = ap.parse_args()

    concepts = sorted((args.wiki.resolve() / "concepts").glob("*.md"))
    missing: list[str] = []
    optional: list[str] = []

    for p in concepts:
        text = p.read_text(encoding="utf-8")
        if args.domain and f"domain: {args.domain}" not in text[:800]:
            continue
        m = re.search(r"^domain:\s*(.+)$", text[:800], re.M)
        domain = m.group(1).strip() if m else ""
        if FORMAL_RE.search(text):
            continue
        if "formal_layer: n/a" in text[:500]:
            optional.append(p.stem)
            continue
        if re.search(r"^status:\s*superseded", text[:800], re.M):
            optional.append(p.stem)
            continue
        if domain in OPTIONAL_DOMAINS:
            optional.append(p.stem)
            continue
        missing.append(p.stem)

    print(f"MISSING_FORMAL ({len(missing)})")
    for slug in missing[:80]:
        print(f"  [[{slug}]]")
    if len(missing) > 80:
        print(f"  … +{len(missing) - 80} more")

    print(f"\nformal_layer n/a or optional domain ({len(optional)})")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
