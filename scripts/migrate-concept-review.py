#!/usr/bin/env python3
"""Migrate concept pages: review frontmatter + ## Explain-back before Evidence."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
EXPLAIN_BACK_HEADING = re.compile(r"^## Explain-back\s*$", re.M)
EVIDENCE_HEADING = re.compile(r"^## Evidence\s*$", re.M)
DIGEST_EXPLAIN = re.compile(
    r"^## Explain-it-back prompts\s*\n(.*?)(?=^## |\Z)",
    re.M | re.S,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path)
    p.add_argument("--concepts-glob", default="concepts/*.md")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def load_digest_prompts(wiki: Path, concept_slug: str) -> str | None:
    for digest in (wiki / "learn" / "digests").glob("*.md"):
        text = digest.read_text(encoding="utf-8", errors="replace")
        if f"[[{concept_slug}]]" not in text:
            continue
        m = DIGEST_EXPLAIN.search(text)
        if m:
            return m.group(1).strip()
    return None


def default_prompts(title: str, claim: str) -> str:
    claim_hint = claim.strip()[:120] if claim else title
    return (
        f"1. *State the **Claim** for {title} in one sentence.*\n"
        f"2. *Walk through the main mechanism — no reading. (Hint: {claim_hint}…)*\n"
        f"3. *Name one design trap, constraint, or common mistake for this topic.*\n"
        f"4. *How does this connect to one related concept you already know?*"
    )


def extract_claim(body: str) -> str:
    m = re.search(r"^## Claim\s*\n+(.*?)(?=^## |\Z)", body, re.M | re.S)
    if not m:
        return ""
    return re.sub(r"\[\[([^\]]+)\]\]", r"\1", m.group(1)).strip()


def ensure_fm_fields(fm: str, slug: str) -> str:
    lines = fm.splitlines()
    keys = {ln.split(":")[0].strip() for ln in lines if ":" in ln}

    if "revised" in keys and "wiki_revised" not in keys:
        for i, ln in enumerate(lines):
            if ln.startswith("revised:"):
                lines[i] = ln.replace("revised:", "wiki_revised:", 1)
                keys.add("wiki_revised")
                break

    additions = []
    if "mastery" not in keys and "status" not in keys:
        additions.append("mastery: learning")
    elif "status" in keys and "mastery" not in keys:
        for ln in lines:
            if ln.startswith("status:"):
                additions.append(f"mastery: {ln.split(':', 1)[1].strip()}")
                break
    if "explain_back" not in keys:
        additions.append("explain_back: not_started")
    if additions:
        lines.extend(additions)
    return "\n".join(lines)


def insert_explain_back(body: str, prompts: str) -> str:
    block = f"## Explain-back\n\n{prompts.strip()}\n\n"
    m = EVIDENCE_HEADING.search(body)
    if m:
        return body[: m.start()] + block + body[m.start() :]
    return body.rstrip() + "\n\n" + block


def transform(path: Path, wiki: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FM_RE.match(text)
    if not m:
        return None
    fm = ensure_fm_fields(m.group(1), path.stem)
    body = text[m.end() :]

    if not EVIDENCE_HEADING.search(body):
        return None

    new_body = body
    if not EXPLAIN_BACK_HEADING.search(body):
        title = path.stem.replace("-", " ")
        prompts = load_digest_prompts(wiki, path.stem)
        if not prompts:
            prompts = default_prompts(title, extract_claim(body))
        new_body = insert_explain_back(body, prompts)

    new_text = f"---\n{fm}\n---\n{new_body}"
    if new_text != text:
        return new_text
    return None


def main() -> int:
    args = parse_args()
    wiki = args.wiki_dir.resolve()
    updated = 0
    for path in sorted(wiki.glob(args.concepts_glob)):
        new = transform(path, wiki)
        if new is None:
            continue
        updated += 1
        print(path.relative_to(wiki))
        if not args.dry_run:
            path.write_text(new, encoding="utf-8")
    print(f"Updated {updated} concept page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
