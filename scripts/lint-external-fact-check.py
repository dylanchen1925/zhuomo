#!/usr/bin/env python3
"""Report corpus concept pages missing or stale External (YYYY) Evidence rows."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from external_fact_check import format_external_report, scan_wiki_external


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path)
    p.add_argument("--domain", default=None, help="Filter by domain slug")
    p.add_argument(
        "--year",
        type=int,
        default=date.today().year,
        help="Expected External (YYYY) year (default: current year)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = scan_wiki_external(args.wiki_dir, domain=args.domain, year=args.year)
    lines, issues = format_external_report(
        result, domain=args.domain, group_by_domain=not args.domain
    )
    for line in lines:
        print(line)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
