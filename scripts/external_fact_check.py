"""Shared scan for External (YYYY) rows on corpus concept pages."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
EXTERNAL_RE = re.compile(r"External\s*\((\d{4})\)", re.I)
EVIDENCE_RE = re.compile(r"^## Evidence\s*$", re.M)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Default age for opportunistic 外搜 (Query / Study follow-on).
DEFAULT_EXTERNAL_MAX_AGE_DAYS = 180


def fm_val(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    return v or None


def parse_iso_date(value: str | None) -> date | None:
    if not value or not DATE_RE.match(value):
        return None
    y, mo, d = (int(x) for x in value.split("-"))
    return date(y, mo, d)


def external_years(body: str) -> list[int]:
    return [int(y) for y in EXTERNAL_RE.findall(body)]


def classify_concept_external(
    fm: str,
    body: str,
    *,
    expected_year: int,
    max_age_days: int = DEFAULT_EXTERNAL_MAX_AGE_DAYS,
    today: date | None = None,
) -> str:
    """Return ok | missing | stale."""
    if not EVIDENCE_RE.search(body):
        return "ok"

    years = external_years(body)
    if not years:
        return "missing"

    latest_year = max(years)
    if latest_year < expected_year:
        return "stale"

    if max_age_days <= 0:
        return "ok"

    ref = today or date.today()
    checked = parse_iso_date(fm_val(fm, "external_checked"))
    if checked is None:
        # Current-year External but never stamped — treat as stale for age-based refresh.
        return "stale"

    if checked < ref - timedelta(days=max_age_days):
        return "stale"

    return "ok"


def stale_reason(
    fm: str,
    body: str,
    *,
    expected_year: int,
    max_age_days: int = DEFAULT_EXTERNAL_MAX_AGE_DAYS,
    today: date | None = None,
) -> str:
    years = external_years(body)
    if not years:
        return f"no External ({expected_year})"
    latest = max(years)
    if latest < expected_year:
        return f"latest External ({latest})"
    checked = fm_val(fm, "external_checked")
    if not checked:
        return "missing external_checked"
    return f"external_checked {checked} (>{max_age_days}d)"


@dataclass
class ExternalScanResult:
    year: int
    max_age_days: int = DEFAULT_EXTERNAL_MAX_AGE_DAYS
    missing: list[tuple[str, str | None]] = field(default_factory=list)
    stale: list[tuple[str, str, str | None]] = field(default_factory=list)
    ok: int = 0

    @property
    def issue_count(self) -> int:
        return len(self.missing) + len(self.stale)

    def stale_slugs(self) -> set[str]:
        return {slug for slug, _reason, _dom in self.stale}

    def issue_slugs(self) -> set[str]:
        return {slug for slug, _ in self.missing} | self.stale_slugs()


def scan_wiki_external(
    wiki_dir: Path,
    *,
    domain: str | None = None,
    year: int | None = None,
    max_age_days: int = DEFAULT_EXTERNAL_MAX_AGE_DAYS,
    slugs: set[str] | None = None,
    concepts_glob: str = "concepts/*.md",
    today: date | None = None,
) -> ExternalScanResult:
    wiki = wiki_dir.resolve()
    expected_year = year if year is not None else date.today().year
    result = ExternalScanResult(year=expected_year, max_age_days=max_age_days)

    for path in sorted(wiki.glob(concepts_glob)):
        slug = path.stem
        if slugs is not None and slug not in slugs:
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        m = FM_RE.match(text)
        fm = m.group(1) if m else ""
        body = text[m.end() :] if m else text

        page_domain = fm_val(fm, "domain")
        if domain and page_domain != domain:
            continue

        status = classify_concept_external(
            fm,
            body,
            expected_year=expected_year,
            max_age_days=max_age_days,
            today=today,
        )
        if status == "missing":
            result.missing.append((slug, page_domain))
        elif status == "stale":
            result.stale.append(
                (
                    slug,
                    stale_reason(
                        fm,
                        body,
                        expected_year=expected_year,
                        max_age_days=max_age_days,
                        today=today,
                    ),
                    page_domain,
                )
            )
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
    age_note = (
        f"; external_checked >{result.max_age_days}d"
        if result.max_age_days > 0
        else ""
    )
    if not result.issue_count and result.ok:
        lines.append(
            f"OK ({result.ok}) — External ({result.year}) fresh{age_note}"
        )
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
            f"STALE_EXTERNAL ({len(result.stale)}) — "
            f"External year < {result.year}{age_note}:"
        )
        for slug, reason, _dom in result.stale:
            lines.append(f"  - {slug} ({reason})")

    if result.ok:
        lines.append(f"OK ({result.ok}) — External ({result.year}) fresh{age_note}")

    if result.issue_count:
        scope = domain or "<domain>"
        lines.append("")
        lines.append(f"Suggested: 外搜 {scope} (or 外搜 [[concept]] for single page)")

    return lines, result.issue_count
