#!/usr/bin/env python3
"""Run zhuomo lint scripts in fixed order; emit tiered report (model-agnostic Lint).

Usage:
  python3 zhuomo-doctor.py <vault>/wiki
  python3 zhuomo-doctor.py <vault>/wiki --domain slug
  python3 zhuomo-doctor.py <vault>/wiki --json
  python3 zhuomo-doctor.py <vault>/wiki --skip-external
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent


def run_script(name: str, wiki: Path, extra: list[str] | None = None) -> tuple[int, str]:
    cmd = [sys.executable, str(SCRIPTS_DIR / name), str(wiki), *(extra or [])]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def parse_review_queue(text: str) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        m = re.match(r"^=== (.+?) \(\d+\) ===$", line.strip())
        if m:
            current = m.group(1).strip()
            buckets.setdefault(current, [])
            continue
        if current and line.strip() and not line.startswith("  -"):
            if line.endswith(".md") or "/concepts/" in line:
                buckets[current].append(line.strip())
        if current and line.strip().startswith("- "):
            buckets[current].append(line.strip())
    return buckets


def parse_explain_back_coverage(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        if line.strip().startswith("- [[") or "COVERAGE" in line.upper():
            items.append(line.strip())
    return items


def parse_claim_layers(text: str) -> list[str]:
    items: list[str] = []
    in_missing = False
    for line in text.splitlines():
        if line.startswith("MISSING_FORMAL"):
            in_missing = True
            continue
        if in_missing and (line.strip().startswith("[[") or line.strip().startswith("- [[")):
            items.append(line.strip())
        if in_missing and line.startswith("formal_layer"):
            break
    return items


def parse_ingest_resume(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        if "partial" in line.lower() or line.strip().startswith("- sources/"):
            items.append(line.strip())
    return items


def parse_figure_visuals(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip().startswith("- [[") or "missing" in ln.lower()]


def tier_for_bucket(name: str) -> int:
    n = name.upper()
    if "BROKEN" in n or "ORPHAN" in n or "WIKILINK" in n:
        return 1
    if "COVERAGE" in n or "THIN" in n or "EXTERNAL" in n or "STALE_EXTERNAL" in n or "MISSING_EXTERNAL" in n:
        return 2
    if "NEVER" in n or "STALE" in n or "RETEST" in n or "UNTESTED" in n or "PARTIAL" in n:
        return 3
    return 4


def build_report(wiki: Path, domain: str | None, sections: dict) -> dict:
    tier_items: dict[int, list[str]] = {1: [], 2: [], 3: [], 4: []}

    rq = sections.get("review_queue", {})
    for bucket, lines in rq.items():
        t = tier_for_bucket(bucket)
        for ln in lines[:50]:
            tier_items[t].append(f"{bucket}: {ln}")

    for ln in sections.get("explain_back", [])[:30]:
        tier_items[2].append(f"EXPLAIN-BACK: {ln}")

    for ln in sections.get("formal", [])[:20]:
        tier_items[2].append(f"MISSING_FORMAL: {ln}")

    for ln in sections.get("ingest", [])[:20]:
        tier_items[3].append(f"INGEST_RESUME: {ln}")

    for ln in sections.get("figures", [])[:20]:
        tier_items[4].append(f"FIGURE: {ln}")

    return {
        "vault": str(wiki),
        "domain_filter": domain,
        "tiers": {str(k): v for k, v in tier_items.items()},
        "counts": {str(k): len(v) for k, v in tier_items.items()},
    }


def format_markdown(report: dict) -> str:
    lines = [f"## Lint — {report['vault']}", ""]
    if report.get("domain_filter"):
        lines.append(f"**Domain filter:** `{report['domain_filter']}`")
        lines.append("")
    for tier in (1, 2, 3, 4):
        items = report["tiers"].get(str(tier), [])
        labels = {1: "阻断", 2: "失真风险", 3: "待消化", 4: "维护便利"}
        lines.append(f"### {tier} {labels[tier]} ({len(items)})")
        if items:
            lines.extend(items[:40])
            if len(items) > 40:
                lines.append(f"… +{len(items) - 40} more")
        else:
            lines.append("—")
        lines.append("")
    lines.append("**Agent:** follow [model-agnostic-playbook.md](../references/model-agnostic-playbook.md) bucket → action; Revise ladder before hand edit.")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wiki", type=Path)
    ap.add_argument("--domain", help="Pass --domain to sub-scripts where supported")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--skip-external", action="store_true")
    args = ap.parse_args()

    wiki = args.wiki.resolve()
    if not (wiki / "concepts").is_dir():
        print(f"Not a wiki dir: {wiki}", file=sys.stderr)
        return 2

    rq_extra: list[str] = []
    if args.domain:
        rq_extra.extend(["--domain", args.domain])
    if args.skip_external:
        rq_extra.append("--skip-external")

    sections: dict = {}

    _, rq_out = run_script("lint-review-queue.py", wiki, rq_extra)
    sections["review_queue"] = parse_review_queue(rq_out)

    _, eb_out = run_script("lint_explain_back_coverage.py", wiki, ["--domain", args.domain] if args.domain else None)
    sections["explain_back"] = parse_explain_back_coverage(eb_out)

    _, cl_out = run_script("lint-claim-layers.py", wiki, ["--domain", args.domain] if args.domain else None)
    sections["formal"] = parse_claim_layers(cl_out)

    _, ir_out = run_script("lint-ingest-resume.py", wiki)
    sections["ingest"] = parse_ingest_resume(ir_out)

    _, fig_out = run_script("lint-figure-visuals.py", wiki)
    sections["figures"] = parse_figure_visuals(fig_out)

    report = build_report(wiki, args.domain, sections)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(report))

    return 1 if report["counts"].get("1", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
