"""Shared scan for External (YYYY) rows on corpus concept pages."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
EXTERNAL_RE = re.compile(r"External\s*\((\d{4})\)", re.I)
EVIDENCE_RE = re.compile(r"^## Evidence\s*$", re.M)


def fm_val(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    return v or None


def external_years(body: str) -> list[int]:
    return [int(y) for y in EXTERNAL_RE.findall(body)]


@dataclass
class ExternalScanResult:
    year: int
    missing: list[tuple[str, str | None]] = field(default_factory=list)
    stale: list[tuple[str, int, str | None]] = field(default_factory=list)
    ok: int = 0

    @property
    def issue_count(self) -> int:
        return len(self.missing) + len(self.stale)


def scan_wiki_external(
    wiki_dir: Path,
    *,
    domain: str | None = None,
    year: int | None = None,
    concepts_glob: str = "concepts/*.md",
) -> ExternalScanResult:
    wiki = wiki_dir.resolve()
    expected_year = year if year is not None else date.today().year
    result = ExternalScanResult(year=expected_year)

    for path in sorted(wiki.glob(concepts_glob)):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = FM_RE.match(text)
        fm = m.group(1) if m else ""
        body = text[m.end() :] if m else text

        page_domain = fm_val(fm, "domain")
        if domain and page_domain != domain:
            continue
        if not EVIDENCE_RE.search(body):
            continue

        slug = path.stem
        years = external_years(body)
        if not years:
            result.missing.append((slug, page_domain))
            continue
        latest = max(years)
        if latest < expected_year:
            result.stale.append((slug, latest, page_domain))
        else:
            result.ok += 1

    return result


def format_external_report(
    result: ExternalScanResult,
    *,
    domain: str | None = None,
    group_by_domain: bool = False,
) -> tuple[list[str], int]:
    """Return printable lines and issue count."""
    lines: list[str] = []
    if not result.issue_count and result.ok:
        lines.append(f"OK ({result.ok}) — External ({result.year}) present")
        return lines, 0

    if result.missing:
        lines.append(
            f"MISSING_EXTERNAL ({len(result.missing)}) — no External ({result.year}) row:"
        )
        if group_by_domain and not domain:
            by_domain: dict[str, list[str]] = {}
            for slug, dom in result.missing:
                key = dom or "(no domain)"
                by_domain.setdefault(key, []).append(slug)
            for dom in sorted(by_domain):
                lines.append(f"  [{dom}] ({len(by_domain[dom])})")
                for slug in by_domain[dom][:20]:
                    lines.append(f"    - {slug}")
                extra = len(by_domain[dom]) - 20
                if extra > 0:
                    lines.append(f"    … +{extra} more")
        else:
            for slug, _dom in result.missing:
                lines.append(f"  - {slug}")

    if result.stale:
        lines.append(
            f"STALE_EXTERNAL ({len(result.stale)}) — External year < {result.year}:"
        )
        for slug, latest, _dom in result.stale:
            lines.append(f"  - {slug} (latest External ({latest}))")

    if result.ok:
        lines.append(f"OK ({result.ok}) — External ({result.year}) present")

    if result.issue_count:
        scope = domain or "<domain>"
        lines.append("")
        lines.append(f"Suggested: 外搜 {scope} (or 外搜 [[concept]] for single page)")

    return lines, result.issue_count
