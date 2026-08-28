#!/usr/bin/env python3
"""Batch Revise: rebuild concept Claim as 知识笔记 from Evidence-linked source MD.

Heuristic synthesis (no LLM): multi-sentence ### per Explain-back prompt from best
source paragraphs; strips enrich paste patterns. Skips pages that already pass quality.

Usage:
  python3 batch-revise-knowledge-notes.py <vault>/wiki              # dry-run
  python3 batch-revise-knowledge-notes.py <vault>/wiki --apply
  python3 batch-revise-knowledge-notes.py <vault>/wiki --apply --limit 50
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
prompt_keywords = _lint.prompt_keywords

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|[^\]]+)?\]\]")
ENRICH_TITLE = re.compile(r"^### .+[…\.]{1,3}\s*$", re.M)
SNIPPET_LINE = re.compile(r"^## [^{].*\{#", re.M)
TOC_BULLET = re.compile(r"^-\s+[A-Z][a-z]+.*-\s+[A-Z]", re.M)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
TECH_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_/-]*|[一-龥]{2,}")


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
    for base in ("concepts", "sources"):
        p = wiki / base / f"{link}.md"
        if p.is_file():
            return p
    return None


def evidence_links(evidence: str, wiki: Path) -> list[tuple[str, str | None, Path | None]]:
    out: list[tuple[str, str | None, Path | None]] = []
    seen: set[str] = set()
    for line in evidence.splitlines():
        if not line.startswith("|") or "要点" in line or re.match(r"^\|\s*[-—]", line):
            continue
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if len(cells) < 2 or cells[0].startswith("External"):
            continue
        label = cells[0]
        for m in WIKILINK_RE.finditer(cells[1]):
            key = m.group(1)
            if key in seen:
                continue
            seen.add(key)
            anchor = m.group(2)
            p = resolve_wikilink(wiki, key)
            out.append((label, anchor, p))
    return out


def slugify_anchor(anchor: str) -> str:
    return anchor.lower().strip()


def extract_anchor_section(text: str, anchor: str) -> str:
    if not anchor:
        return ""
    pat = re.compile(
        rf"^#{{1,6}}\s+.*\{{#{re.escape(anchor)}\}}\s*$",
        re.M | re.I,
    )
    m = pat.search(text)
    if not m:
        pat2 = re.compile(rf"\{{#{re.escape(anchor)}\}}", re.I)
        m2 = pat2.search(text)
        if not m2:
            return ""
        start = m2.start()
    else:
        start = m.start()
    rest = text[start:]
    nxt = re.search(r"^#{1,6}\s+\S", rest[1:], re.M)
    chunk = rest[: nxt.start() + 1 if nxt else len(rest)]
    return chunk


def clean_prose(s: str, max_chars: int = 900) -> str:
    s = re.sub(r"^##\s+[^\n]+", "", s, flags=re.M)
    s = re.sub(r"\{#([^}]+)\}", "", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", s)
    s = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > max_chars:
        s = s[: max_chars - 1].rsplit(" ", 1)[0] + "…"
    return s


def score_paragraph(para: str, terms: list[str]) -> int:
    if para.startswith("|") or para.startswith("![") or len(para.strip()) < 40:
        return 0
    if re.match(r"^##\s+\S", para.strip()):
        return 0
    if TOC_BULLET.search(para):
        return 0
    if para.strip().startswith("- ") and para.count(".") < 2:
        return 2
    low = para.lower()
    hits = sum(2 for t in terms if t in low)
    return hits * 10 + min(len(para), 300) // 30


def best_paragraphs(text: str, terms: list[str], limit: int = 2) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) > 40]
    scored = [(score_paragraph(p, terms), p) for p in paras]
    scored = [(s, p) for s, p in scored if s > 0]
    scored.sort(key=lambda x: -x[0])
    out: list[str] = []
    seen: set[str] = set()
    for _, p in scored:
        key = p[:80].lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
        if len(out) >= limit:
            break
    return out


def sentences_from_paras(paras: list[str], max_sentences: int = 4) -> str:
    sentences: list[str] = []
    for para in paras:
        for sent in SENT_SPLIT.split(re.sub(r"\s+", " ", para)):
            sent = sent.strip()
            if len(sent) < 25:
                continue
            if sent not in sentences:
                sentences.append(sent)
            if len(sentences) >= max_sentences:
                break
        if len(sentences) >= max_sentences:
            break
    return " ".join(sentences)


def subsection_title(prompt: str) -> str:
    p = prompt.strip().strip('"').strip("*").rstrip("?").strip()
    p = re.sub(r"\s*[—–-]\s*", " — ", p)
    if len(p) > 72:
        p = p[:69].rsplit(" ", 1)[0] + "…"
    return p


def opening_paragraph(existing: str, title: str, source_text: str, terms: list[str]) -> str:
    first = existing.strip().split("\n\n")[0].strip()
    first = re.sub(r"^#+\s.*", "", first).strip()
    # Drop accidental markdown-heading paste from enrich
    if re.match(r"^##\s+\S", first):
        first = ""
    bad = (
        not first
        or len(first.split()) < 15
        or ENRICH_TITLE.match(first)
        or TOC_BULLET.search(first)
        or SNIPPET_LINE.search(first)
        or first.startswith("- ")
    )
    if not bad:
        return clean_prose(first, max_chars=600)
    paras = best_paragraphs(source_text, terms or TECH_TOKEN.findall(title)[:5], limit=1)
    if paras:
        intro = sentences_from_paras(paras, max_sentences=3)
        if intro:
            return intro
    return first if first else f"**{title}** — compiled concept note (see ### sections for mechanisms and traps)."


def claim_quality(claim: str, prompt_count: int) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    subs = len(re.findall(r"^### ", claim, re.M))
    words = len(re.findall(r"\S+", claim))
    if subs < prompt_count:
        reasons.append("missing_subsections")
    if words < 100 and prompt_count >= 2:
        reasons.append("thin_claim")
    if ENRICH_TITLE.search(claim):
        reasons.append("enrich_title")
    bodies = re.split(r"^### .+$", claim, flags=re.M)[1:]
    for b in bodies:
        b = b.strip()
        if SNIPPET_LINE.search(b) or (b.startswith("- ") and len(b) > 180):
            reasons.append("snippet_paste")
            break
        if b.startswith("- ") and b.count(" - ") >= 3:
            reasons.append("toc_paste")
            break
    if len(set(b.strip()[:120] for b in bodies if b.strip())) < len([b for b in bodies if b.strip()]):
        reasons.append("duplicate_subsections")
    return (len(reasons) == 0, reasons)


def source_for_prompt(
    prompt: str,
    ev_links: list[tuple[str, str | None, Path | None]],
    combined: str,
) -> str:
    keys = prompt_keywords(prompt) or [
        t.lower() for t in TECH_TOKEN.findall(prompt) if len(t) >= 3
    ][:6]
    best: tuple[int, str] | None = None
    for label, anchor, path in ev_links:
        if not path or not path.is_file():
            continue
        lab_low = label.lower()
        score = sum(3 for k in keys if k in lab_low)
        text = path.read_text(encoding="utf-8", errors="replace")
        chunk = text
        if anchor:
            sec = extract_anchor_section(text, slugify_anchor(anchor))
            if sec:
                chunk = sec
                score += 5
        if score > 0:
            if best is None or score > best[0]:
                best = (score, chunk)
    if best:
        return best[1]
    return combined


def build_claim(
    title: str,
    existing_claim: str,
    prompts: list[str],
    ev_links: list[tuple[str, str | None, Path | None]],
    combined: str,
) -> str:
    opening_existing = existing_claim.split("^###")[0] if False else existing_claim
    opening_existing = re.split(r"^### ", existing_claim, maxsplit=1, flags=re.M)[0].strip()
    all_terms = []
    for p in prompts:
        all_terms.extend(prompt_keywords(p))
    opener = opening_paragraph(opening_existing, title, combined, list(dict.fromkeys(all_terms))[:8])

    blocks = [opener, ""]
    used_snippets: set[str] = set()

    for prompt in prompts:
        terms = prompt_keywords(prompt)
        src = source_for_prompt(prompt, ev_links, combined)
        paras = best_paragraphs(src, terms, limit=3)
        body = sentences_from_paras(paras, max_sentences=5)
        if not body or body[:100] in used_snippets:
            paras = best_paragraphs(combined, terms, limit=3)
            body = sentences_from_paras(paras, max_sentences=5)
        body = clean_prose(body)
        if not body or body[:80] in used_snippets:
            body = (
                f"Decision context: {prompt.rstrip('?')}. "
                "See Evidence anchors for source detail; expand via Revise if mechanism is still thin."
            )
        used_snippets.add(body[:80])
        blocks.append(f"### {subsection_title(prompt)}")
        blocks.append(body)
        blocks.append("")

    return append_formal_layer("\n".join(blocks).strip() + "\n")


def append_formal_layer(claim: str) -> str:
    """Append ### Formal: if missing (shared with patch-claim-two-layers)."""
    if re.search(r"^### Formal:", claim, re.M):
        return claim
    import importlib.util

    patch_path = Path(__file__).resolve().parent / "patch-claim-two-layers.py"
    spec = importlib.util.spec_from_file_location("patch_claim_two_layers", patch_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    opening, subs = mod.split_claim_parts(claim)
    formal = mod.build_formal_block(opening, subs)
    return claim.rstrip() + "\n\n" + formal + "\n"


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


def is_real_section_header(line: str) -> bool:
    m = re.match(r"^## (.+?)\s*$", line.strip())
    if not m:
        return False
    title = m.group(1).strip()
    if "{#" in title or title.startswith("hosts:") or title.startswith("Figure "):
        return False
    low = title.lower()
    if low in KNOWN_SECTIONS:
        return True
    # Unknown ## inside Claim paste — not a section boundary
    return False


def replace_section(body: str, name_key: str, content: str) -> str:
    lines = body.splitlines(keepends=True)
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if start_idx is None:
            m = re.match(r"^## (.+?)\s*$", line.strip())
            if m and m.group(1).strip().lower() == name_key.lower():
                start_idx = i
            continue
        if is_real_section_header(line.rstrip("\n")):
            end_idx = i
            break
    if start_idx is None:
        return body
    if end_idx is None:
        end_idx = len(lines)
    header = lines[start_idx]
    new_lines = lines[: start_idx + 1] + [content.rstrip() + "\n", "\n"] + lines[end_idx:]
    return "".join(new_lines)


def claim_region(body: str) -> str:
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
        return ""
    return "\n".join(lines[start:end] if end else lines[start:])


def claim_section_corrupt(body: str) -> bool:
    region = claim_region(body)
    if re.search(r"^## hosts:", region, re.M):
        return True
    titles = re.findall(r"^### (.+)$", region, re.M)
    if len(titles) != len(set(t.strip().lower() for t in titles)):
        return True
    return False


def revise_concept(path: Path, wiki: Path, today: str, dry_run: bool, force: bool = False) -> tuple[bool, str]:
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    if "## Explain-back" not in body:
        return False, "no_explain_back"

    sections = split_sections(body)
    claim = claim_region(body) or sections.get("claim", "")
    evidence = sections.get("evidence", "")
    explain = sections.get("explain-back", "")
    prompts = extract_prompts(explain)
    if not prompts:
        return False, "no_prompts"

    ok, reasons = claim_quality(claim, len(prompts))
    lint = audit_file(path)
    corrupt = claim_section_corrupt(body)
    if ok and not lint and not corrupt and not force:
        return False, "ok"

    ev_links = evidence_links(evidence, wiki)
    paths = [p for _, _, p in ev_links if p and p.is_file()]
    if corrupt:
        reasons = reasons + ["corrupt_section"]
    if not paths and not evidence:
        return False, "no_evidence"

    combined = "\n\n".join(
        p.read_text(encoding="utf-8", errors="replace") for p in paths
    ) if paths else ""

    title_m = re.search(r"^# (.+)$", body, re.M)
    title = title_m.group(1).strip() if title_m else path.stem

    new_claim = build_claim(title, claim, prompts, ev_links, combined)
    new_body = replace_section(body, "claim", new_claim)
    new_fm = set_frontmatter_field(fm, "updated", today) if fm else f"updated: {today}"
    out = f"---\n{new_fm}\n---\n\n{new_body}" if fm else raw

    if dry_run:
        return True, ",".join(reasons) or (lint["issues"][0] if lint else "revise")

    path.write_text(out, encoding="utf-8")
    return True, ",".join(reasons) or (lint["issues"][0] if lint else "revise")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wiki", type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--domain", help="Only domain: slug")
    ap.add_argument("--slug", help="Single concept")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true", help="Revise even if quality OK")
    args = ap.parse_args()
    wiki = args.wiki.resolve()
    today = date.today().isoformat()
    concepts = sorted((wiki / "concepts").glob("*.md"))
    if args.slug:
        concepts = [wiki / "concepts" / f"{args.slug}.md"]

    changed = 0
    skipped_ok = 0
    for p in concepts:
        if args.domain:
            head = p.read_text(encoding="utf-8")[:800]
            if f"domain: {args.domain}" not in head:
                continue
        if args.force:
            # Temporarily treat as needs revise
            pass
        ok, reason = revise_concept(p, wiki, today, dry_run=not args.apply, force=args.force)
        if ok:
            changed += 1
            print(f"{'WOULD' if not args.apply else 'REVISED'} [[{p.stem}]] — {reason}")
        elif reason == "ok":
            skipped_ok += 1
        if args.limit and changed >= args.limit:
            break

    print(
        f"\n{'Applied' if args.apply else 'Would revise'}: {changed} | skipped_ok: {skipped_ok}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
