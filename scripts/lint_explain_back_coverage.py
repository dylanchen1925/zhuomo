#!/usr/bin/env python3
"""Flag concept pages where Explain-back prompts lack support in Claim + Evidence."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

STOPWORDS = {
    "a", "an", "the", "and", "or", "vs", "if", "how", "what", "when", "where", "why",
    "which", "who", "does", "do", "is", "are", "was", "were", "be", "to", "of", "in",
    "on", "at", "for", "with", "without", "from", "into", "not", "no", "by", "as",
    "this", "that", "these", "those", "it", "its", "you", "your", "we", "they",
    "trap", "scenario", "procedure", "migration", "impact", "effect", "order",
    "stuck", "unblock", "delete", "fix", "debug", "case", "example", "difference",
    "compare", "contrast", "between", "first", "last", "longest", "shortest",
    "applied", "applies", "apply", "behavior", "symptom", "symptoms", "fail",
    "fails", "failed", "failure", "wrong", "right", "true", "false", "same",
    "different", "two", "three", "one", "many", "most", "least", "still", "after",
    "before", "during", "while", "then", "than", "over", "under", "all", "any",
}


def split_sections(body: str) -> dict[str, str]:
    parts: dict[str, list[str]] = {}
    current = "_preamble"
    parts[current] = []
    for line in body.splitlines():
        m = re.match(r"^## (.+)$", line.strip())
        if m:
            current = m.group(1).strip().lower()
            parts.setdefault(current, [])
        else:
            parts.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in parts.items()}


def extract_prompts(explain_back: str) -> list[str]:
    prompts: list[str] = []
    for line in explain_back.splitlines():
        line = line.strip()
        if not line or line.startswith("Claim correct"):
            continue
        m = re.match(r"^\d+\.\s*\*?\"(.+?)\"?\*?$", line)
        if m:
            prompts.append(m.group(1))
        elif line.startswith("*") and line.endswith("*"):
            prompts.append(line.strip("*\" "))
    return prompts


def prompt_keywords(prompt: str) -> list[str]:
    raw = re.findall(r"[A-Za-z][A-Za-z0-9_-]*|[一-龥]{2,}", prompt)
    keys: list[str] = []
    for token in raw:
        low = token.lower()
        if low in STOPWORDS or len(low) < 3:
            continue
        if low not in keys:
            keys.append(low)
    return keys


def evidence_row_count(evidence: str) -> int:
    rows = 0
    for line in evidence.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*[-—]", line) and "要点" not in line:
            rows += 1
    return rows


def audit_file(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if "## Explain-back" not in text:
        return None
    if text.startswith("---"):
        _, _, body = text.partition("---")
        _, _, body = body.partition("---")
    else:
        body = text
    sections = split_sections(body)
    explain = sections.get("explain-back", "")
    claim = sections.get("claim", "")
    evidence = sections.get("evidence", "")
    if not explain or not claim:
        return None
    corpus = f"{claim}\n{evidence}".lower()
    prompts = extract_prompts(explain)
    if not prompts:
        return None

    subsection_count = len(re.findall(r"^### ", claim, re.M))
    if subsection_count >= len(prompts):
        return None

    ev_rows = evidence_row_count(evidence)
    issues: list[str] = []
    if subsection_count < len(prompts):
        issues.append("thin_corpus")
    if ev_rows == 0:
        issues.append("no_evidence")

    if not issues:
        return None

    missing_by_prompt: list[tuple[str, list[str]]] = []
    for p in prompts:
        missing = [k for k in prompt_keywords(p) if k not in corpus]
        if missing:
            missing_by_prompt.append((p, missing))

    return {
        "path": path,
        "slug": path.stem,
        "issues": issues,
        "prompts": len(prompts),
        "ev_rows": ev_rows,
        "claim_words": len(claim.split()),
        "missing_by_prompt": missing_by_prompt[:3],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wiki", type=Path, help="Path to wiki/ directory")
    ap.add_argument("--domain", help="Filter by domain: frontmatter")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    concepts = sorted((args.wiki / "concepts").glob("*.md"))
    hits: list[dict] = []
    for p in concepts:
        if args.domain:
            head = p.read_text(encoding="utf-8")[:800]
            if f"domain: {args.domain}" not in head:
                continue
        r = audit_file(p)
        if r:
            hits.append(r)
    hits.sort(key=lambda x: (-len(x["issues"]), -len(x["missing_by_prompt"]), x["slug"]))
    if args.limit:
        hits = hits[: args.limit]

    if args.json:
        import json

        print(json.dumps([{**h, "path": str(h["path"])} for h in hits], indent=2))
        return 0

    print(f"EXPLAIN-BACK COVERAGE — {len(hits)} flagged / {len(concepts)} concepts\n")
    for h in hits:
        miss = "; ".join(f'"{p[:50]}…" → {m}' for p, m in h["missing_by_prompt"][:2])
        print(
            f"- [[{h['slug']}]] | {','.join(h['issues'])} | "
            f"claim={h['claim_words']}w ev={h['ev_rows']} | {miss}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
