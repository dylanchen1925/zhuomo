#!/usr/bin/env python3
"""Enrich concept Claim + Evidence so Explain-back prompts are answerable from the page.

Heuristic: thin Claim (no ### subsections, short) with 3+ Explain-back prompts.
Pulls matching paragraphs from Evidence-linked source MD files.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "lint_explain_back_coverage",
    Path(__file__).with_name("lint_explain_back_coverage.py"),
)
_lint = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(_lint)
audit_file = _lint.audit_file
extract_prompts = _lint.extract_prompts
split_sections = _lint.split_sections

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
TECH_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_/-]*|[一-龥]{2,}")


FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def parse_frontmatter(text: str) -> tuple[str, str]:
    m = FM_RE.match(text)
    if not m:
        return "", text
    return m.group(1).strip(), text[m.end() :]


def set_frontmatter_field(fm: str, key: str, value: str) -> str:
    if re.search(rf"^{key}:", fm, re.M):
        return re.sub(rf"^{key}:\s*.+$", f"{key}: {value}", fm, count=1, flags=re.M)
    return fm.rstrip() + f"\n{key}: {value}"


def resolve_wikilink(wiki: Path, link: str) -> Path | None:
    link = link.strip()
    if link.startswith("sources/"):
        p = wiki / link
        if not p.suffix:
            p = p.with_suffix(".md")
        return p if p.is_file() else None
    if link.startswith("concepts/"):
        return wiki / link if (wiki / link).is_file() else None
    # bare slug → concepts or sources
    for base in ("concepts", "sources"):
        p = wiki / base / f"{link}.md"
        if p.is_file():
            return p
    return None


def evidence_links(evidence: str, wiki: Path) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for m in WIKILINK_RE.finditer(evidence):
        p = resolve_wikilink(wiki, m.group(1))
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def prompt_search_terms(prompt: str) -> list[str]:
    terms: list[str] = []
    for tok in TECH_TOKEN.findall(prompt):
        low = tok.lower()
        if len(low) < 3 or low in {"the", "and", "how", "what", "why", "when", "which", "vs"}:
            continue
        if low not in terms:
            terms.append(low)
    return terms[:6]


def best_snippet(text: str, terms: list[str], max_chars: int = 420) -> str | None:
    if not terms:
        return None
    # Prefer paragraphs with most term hits
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) > 40]
    best: tuple[int, str] | None = None
    for para in paras:
        if para.startswith("|") or para.startswith("!["):
            continue
        if para.count(":") > 8 and "kind" in para.lower():
            continue
        low = para.lower()
        hits = sum(1 for t in terms if t in low)
        if hits == 0:
            continue
        score = hits * 10 + min(len(para), 200) // 20
        if best is None or score > best[0]:
            best = (score, para)
    if not best:
        return None
    snippet = re.sub(r"\s+", " ", best[1])
    if len(snippet) > max_chars:
        snippet = snippet[: max_chars - 1].rsplit(" ", 1)[0] + "…"
    return snippet


def subsection_title(prompt: str) -> str:
    p = prompt.strip().strip('"').strip("*")
    p = re.sub(r"\s*[—–-]\s*.*$", "", p)
    p = p.rstrip("?").strip()
    if len(p) > 48:
        p = p[:45] + "…"
    return p


def existing_evidence_labels(evidence: str) -> set[str]:
    labels: set[str] = set()
    for line in evidence.splitlines():
        if line.startswith("|") and "要点" not in line and not re.match(r"^\|\s*[-—]", line):
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if cells:
                labels.add(cells[0].lower())
    return labels


def enrich_concept(path: Path, wiki: Path, today: str, dry_run: bool) -> bool:
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    if not fm:
        return False
    audit = audit_file(path)
    if not audit:
        return False
    if "thin_corpus" not in audit["issues"]:
        return False

    sections = split_sections(body)
    claim = sections.get("claim", "")
    evidence = sections.get("evidence", "")
    explain = sections.get("explain-back", "")
    prompts = extract_prompts(explain)
    if not prompts:
        return False
    subsection_count = len(re.findall(r"^### ", claim, re.M))
    if subsection_count >= len(prompts):
        return False

    sources = evidence_links(evidence, wiki)
    if not sources:
        return False

    combined = "\n\n".join(p.read_text(encoding="utf-8", errors="replace") for p in sources)
    additions: list[str] = []
    new_rows: list[str] = []
    labels = existing_evidence_labels(evidence)

    existing_titles = {line[4:].strip().lower() for line in claim.splitlines() if line.startswith("### ")}

    for prompt in prompts:
        terms = prompt_search_terms(prompt)
        snippet = best_snippet(combined, terms)
        if not snippet:
            continue
        title = subsection_title(prompt)
        if title.lower() in existing_titles:
            continue
        block = f"### {title}\n{snippet}"
        additions.append(block)
        existing_titles.add(title.lower())
        label = title[:40]
        if label.lower() not in labels:
            # Link to first source that contained a term
            src_link = None
            for sp in sources:
                if any(t in sp.read_text(encoding="utf-8", errors="replace").lower() for t in terms):
                    rel = sp.relative_to(wiki).with_suffix("")
                    src_link = f"[[{rel.as_posix()}]]"
                    break
            if src_link:
                new_rows.append(f"| {label} | {src_link} |")
                labels.add(label.lower())

    if len(additions) < 1:
        return False

    new_claim = claim.rstrip() + "\n\n" + "\n\n".join(additions)
    new_evidence = evidence
    if new_rows:
        lines = evidence.splitlines()
        insert_at = len(lines)
        for i, line in enumerate(lines):
            if line.startswith("| External"):
                insert_at = i
                break
        lines = lines[:insert_at] + new_rows + lines[insert_at:]
        new_evidence = "\n".join(lines)

    # Rebuild body
    def replace_section(name_key: str, content: str, text: str) -> str:
        pattern = re.compile(r"^## (.+?)\s*\n", re.M)
        match = None
        for m in pattern.finditer(text):
            if m.group(1).strip().lower() == name_key.lower():
                match = m
                break
        if not match:
            return text
        start = match.start()
        rest = text[match.end() :]
        nxt = re.search(r"^## ", rest, re.M)
        end = match.end() + (nxt.start() if nxt else len(rest))
        header = text[match.start() : match.end()]
        return text[:start] + header + content.rstrip() + "\n\n" + text[end:].lstrip("\n")

    new_body = replace_section("claim", new_claim, body)
    new_body = replace_section("evidence", new_evidence, new_body)

    new_fm = set_frontmatter_field(fm, "updated", today)
    out = f"---\n{new_fm}\n---\n\n{new_body}"
    if dry_run:
        print(f"WOULD ENRICH [[{path.stem}]] +{len(additions)} subsections +{len(new_rows)} evidence")
        return True
    path.write_text(out, encoding="utf-8")
    print(f"ENRICHED [[{path.stem}]] +{len(additions)} subsections +{len(new_rows)} evidence")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wiki", type=Path)
    ap.add_argument("--domain", help="Only concepts with domain: slug")
    ap.add_argument("--slug", help="Single concept slug")
    ap.add_argument("--apply", action="store_true", help="Write files (default dry-run)")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    wiki = args.wiki.resolve()
    today = date.today().isoformat()
    concepts = sorted((wiki / "concepts").glob("*.md"))
    if args.slug:
        concepts = [wiki / "concepts" / f"{args.slug}.md"]
    changed = 0
    for p in concepts:
        if args.domain:
            head = p.read_text(encoding="utf-8")[:600]
            if f"domain: {args.domain}" not in head:
                continue
        if enrich_concept(p, wiki, today, dry_run=not args.apply):
            changed += 1
            if args.limit and changed >= args.limit:
                break
    print(f"\n{'Applied' if args.apply else 'Would apply'}: {changed} concept(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
