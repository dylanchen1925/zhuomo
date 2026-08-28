#!/usr/bin/env python3
"""Add ### Formal: definitions & parameters to concept Claim sections (two-layer rubric).

Heuristic migration: keeps existing opening + ### Q&A as 可理解层; appends 正式层
synthesized from bold terms, paths, and key phrases in existing Claim bodies.

Skips: pages that already have Formal; craft-narrative / study-analytic optional domains
(set formal_layer: n/a in frontmatter instead).

Usage:
  python3 patch-claim-two-layers.py <vault>/wiki              # dry-run stats
  python3 patch-claim-two-layers.py <vault>/wiki --apply
  python3 patch-claim-two-layers.py <vault>/wiki --apply --domain kubernetes-cilium
  python3 patch-claim-two-layers.py <vault>/wiki --apply --slug cilium-cni-overview
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
FORMAL_RE = re.compile(r"^### Formal:", re.M)
H3_RE = re.compile(r"^(### .+)$", re.M)

# formal_layer optional per concept-claim-rubric.md
FORMAL_OPTIONAL_DOMAINS = frozenset({
    "craft-writing",
    "chinese-history-culture",
    "games-people-play-berne",
})

KNOWN_SECTIONS = frozenset({
    "claim",
    "personal notes",
    "explain-back",
    "evidence",
    "sources",
    "related",
    "prerequisites",
    "prerequisite",
    "mechanics",
    "my take",
})


def parse_frontmatter(text: str) -> tuple[str, str]:
    m = FM_RE.match(text)
    if not m:
        return "", text
    return m.group(1).strip(), text[m.end() :]


def set_frontmatter_field(fm: str, key: str, value: str) -> str:
    if re.search(rf"^{key}:", fm, re.M):
        return re.sub(rf"^{key}:\s*.+$", f"{key}: {value}", fm, count=1, flags=re.M)
    return fm.rstrip() + f"\n{key}: {value}"


def is_real_section_header(line: str) -> bool:
    m = re.match(r"^## (.+?)\s*$", line.strip())
    if not m:
        return False
    title = m.group(1).strip()
    if "{#" in title or title.startswith("hosts:") or title.startswith("Figure "):
        return False
    return title.lower() in KNOWN_SECTIONS


def claim_region(body: str) -> tuple[int, int] | None:
    lines = body.splitlines()
    start = end = None
    for i, line in enumerate(lines):
        m = re.match(r"^## (.+?)\s*$", line.strip())
        if m and m.group(1).strip().lower() == "claim":
            start = i + 1
            continue
        if start is not None and is_real_section_header(line):
            end = i
            break
    if start is None:
        return None
    return start, end if end is not None else len(lines)


def split_claim_parts(claim: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (opening, [(h3_title, body), ...])."""
    chunks = H3_RE.split(claim.strip())
    if not chunks:
        return "", []
    opening = chunks[0].strip()
    subs: list[tuple[str, str]] = []
    i = 1
    while i + 1 < len(chunks):
        title = chunks[i].strip()
        body = chunks[i + 1].strip()
        if not title.startswith("### Formal:"):
            subs.append((title, body))
        i += 2
    return opening, subs


GENERIC_TERMS = frozenset({
    "add", "del", "check", "get", "api", "cli", "dns", "tcp", "udp", "agent", "note", "trap",
})


def ref_label(title: str | None) -> str:
    if title:
        clean = title.removeprefix("### ").strip()
        if len(clean) > 64:
            clean = clean[:61].rsplit(" ", 1)[0] + "…"
        return f"对应上文「{clean}」"
    return "对应开篇例子"


def first_sentence(text: str, max_len: int = 140) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    parts = re.split(r"(?<=[.!?])\s+", text)
    sent = parts[0] if parts else text
    if len(sent) > max_len:
        sent = sent[: max_len - 1].rsplit(" ", 1)[0] + "…"
    return sent


def extract_bullets(opening: str, subs: list[tuple[str, str]], max_items: int = 12) -> list[str]:
    bullets: list[str] = []
    seen_terms: set[str] = set()
    seen_lines: set[str] = set()

    def add(line: str) -> None:
        key = re.sub(r"\*\*|`|—.*", "", line).strip().lower()[:72]
        if key in seen_lines or len(bullets) >= max_items:
            return
        seen_lines.add(key)
        bullets.append(line)

    def add_term(term: str, gloss: str, ref: str) -> None:
        key = term.strip().lower()
        if key in seen_terms or key in GENERIC_TERMS or len(key) < 3:
            return
        seen_terms.add(key)
        add(f"- **{term.strip()}** — {gloss} ({ref})")

    open_text = opening.strip()
    if open_text:
        for path in re.findall(r"(/(?:etc|var|usr|opt|sys|dev)[^\s`,.;)]+)", open_text):
            add(f"- `{path}` — 安装/配置路径 ({ref_label(None)})")
        for term in re.findall(r"\*\*([^*]+)\*\*", open_text):
            if len(term) >= 5:
                add_term(term, "开篇定义", ref_label(None))

    for title, body in subs:
        ref = ref_label(title)
        text = body.strip()
        if not text:
            continue
        add(f"- {first_sentence(text)} — {ref}")

        for path in re.findall(r"(/(?:etc|usr|var|opt)[^\s`,.;)]+)", text):
            add(f"- `{path}` — 路径/对象 ({ref})")

        bold_terms = [t.strip() for t in re.findall(r"\*\*([^*]+)\*\*", text)]
        for term in bold_terms:
            if len(term) >= 5 and not term.endswith("?"):
                add_term(term, "正式用语", ref)
            if len(bullets) >= max_items:
                break

    if not bullets and opening.strip():
        add(f"- （待 Revise 补全精确定义）— 见 Evidence 锚点 ({ref_label(None)})")

    return bullets


def build_formal_block(opening: str, subs: list[tuple[str, str]]) -> str:
    bullets = extract_bullets(opening, subs)
    lines = ["### Formal: definitions & parameters", ""]
    lines.extend(bullets)
    return "\n".join(lines).strip() + "\n"


def strip_formal(claim: str) -> str:
    return re.sub(r"\n### Formal:.*?(?=\n## |\Z)", "\n", claim, flags=re.S).rstrip() + "\n"


def patch_claim_body(body: str, force: bool = False) -> tuple[str, bool]:
    region = claim_region(body)
    if region is None:
        return body, False
    start, end = region
    lines = body.splitlines(keepends=True)
    claim_text = "".join(lines[start:end])
    has_formal = bool(FORMAL_RE.search(claim_text))
    if has_formal and not force:
        return body, False
    if has_formal and force:
        claim_text = strip_formal(claim_text)

    opening, subs = split_claim_parts(claim_text)
    formal = build_formal_block(opening, subs)
    spacer = "\n" if claim_text.rstrip() else ""
    new_claim = claim_text.rstrip() + spacer + "\n" + formal + "\n"
    new_lines = lines[:start] + [new_claim] + lines[end:]
    return "".join(new_lines), True


def domain_from_fm(fm: str) -> str | None:
    m = re.search(r"^domain:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else None


def patch_file(path: Path, today: str, dry_run: bool, force: bool = False) -> tuple[str, str]:
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    domain = domain_from_fm(fm)

    if FORMAL_RE.search(body) and not force:
        return "skip_has_formal", domain or ""

    if domain in FORMAL_OPTIONAL_DOMAINS:
        if dry_run:
            return "skip_optional_domain", domain
        new_fm = set_frontmatter_field(fm, "formal_layer", "n/a") if fm else ""
        if "formal_layer:" not in fm:
            out = f"---\n{new_fm}\n---\n\n{body}" if fm else raw
            path.write_text(out, encoding="utf-8")
            return "marked_n/a", domain
        return "skip_optional_domain", domain

    new_body, changed = patch_claim_body(body, force=force)
    if not changed:
        return "skip_no_claim", domain or ""

    new_fm = set_frontmatter_field(fm, "updated", today) if fm else ""
    out = f"---\n{new_fm}\n---\n\n{new_body}" if fm else raw

    if not dry_run:
        path.write_text(out, encoding="utf-8")
    return "patched", domain or ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wiki", type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--domain", help="Only concepts in domain")
    ap.add_argument("--slug", help="Single concept slug")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true", help="Replace existing ### Formal: block")
    args = ap.parse_args()

    wiki = args.wiki.resolve()
    concepts_dir = wiki / "concepts"
    if not concepts_dir.is_dir():
        print(f"Missing {concepts_dir}", file=sys.stderr)
        return 1

    paths = sorted(concepts_dir.glob("*.md"))
    if args.slug:
        paths = [concepts_dir / f"{args.slug}.md"]

    today = date.today().isoformat()
    stats: dict[str, int] = {}
    patched = 0

    for p in paths:
        if not p.is_file():
            continue
        if args.domain:
            head = p.read_text(encoding="utf-8")[:600]
            if f"domain: {args.domain}" not in head:
                continue

        status, _ = patch_file(p, today, dry_run=not args.apply, force=args.force)
        stats[status] = stats.get(status, 0) + 1
        if status == "patched":
            patched += 1
            print(f"{'PATCH' if args.apply else 'WOULD'} [[{p.stem}]]")
        if args.limit and patched >= args.limit:
            break

    print(f"\n{'Applied' if args.apply else 'Dry-run'}: {patched} patched")
    for k in sorted(stats):
        print(f"  {k}: {stats[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
