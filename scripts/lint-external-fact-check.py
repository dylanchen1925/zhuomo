#!/usr/bin/env python3
"""Report corpus concept pages missing or stale External (YYYY) Evidence rows."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from external_fact_check import (
    DEFAULT_EXTERNAL_MAX_AGE_DAYS,
    format_external_report,
    scan_wiki_external,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path)
    p.add_argument("--domain", default=None, help="Filter by domain slug")
    p.add_argument(
        "--slugs",
        default=None,
        help="Comma-separated concept slugs (Query/Study opportunistic scan)",
    )
    p.add_argument(
        "--year",
        type=int,
        default=date.today().year,
        help="Expected External (YYYY) year (default: current year)",
    )
    p.add_argument(
        "--max-age-days",
        type=int,
        default=DEFAULT_EXTERNAL_MAX_AGE_DAYS,
        help=(
            "Flag stale when external_checked older than N days "
            f"(default: {DEFAULT_EXTERNAL_MAX_AGE_DAYS}; 0 = year-only)"
        ),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    slugs = None
    if args.slugs:
        slugs = {s.strip() for s in args.slugs.split(",") if s.strip()}
    result = scan_wiki_external(
        args.wiki_dir,
        domain=args.domain,
        year=args.year,
        max_age_days=args.max_age_days,
        slugs=slugs,
    )
    lines, issues = format_external_report(
        result, domain=args.domain, group_by_domain=not args.domain
    )
    for line in lines:
        print(line)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
