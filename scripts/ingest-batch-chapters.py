#!/usr/bin/env python3
"""Ingest continue — chapter-batch wrapper (model-agnostic).

Groups a source page Topic map by chapter/section, tracks progress in
`next_sections` frontmatter, and prints the next batch for agent deepen.

Usage:
  python3 ingest-batch-chapters.py <vault>/wiki --source <slug>           # plan + next batch
  python3 ingest-batch-chapters.py <vault>/wiki --source <slug> --init    # seed next_sections
  python3 ingest-batch-chapters.py <vault>/wiki --source <slug> --mark-done "Ch3"
  python3 ingest-batch-chapters.py <vault>/wiki --source <slug> --chapters 2
  python3 ingest-batch-chapters.py <vault>/wiki --source <slug> --json
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
TOPIC_MAP_HEADING = re.compile(r"^## Topic map\b", re.M | re.I)
TABLE_ROW = re.compile(r"^\|(.+)\|\s*$")
CHAPTER_KEY = re.compile(
    r"^(?:"
    r"(Ch(?:apter)?\s*\d+[a-z]?)"
    r"|(Part\s*\d+)"
    r"|(Appendix(?:\s+[A-Z0-9]+)?)"
    r"|(§\s*[\d.]+)"
    r")",
    re.I,
)
PART_EVIDENCE = re.compile(r"\bpart-(\d+)\b", re.I)
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


@dataclass
class TopicRow:
    chapter_key: str
    topic: str
    evidence: str
    existing: str
    action: str
    concept_slugs: list[str] = field(default_factory=list)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm, text[m.end() :]


def dump_frontmatter(fm: dict[str, str]) -> str:
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def chapter_key_from_row(topic: str, evidence: str) -> str:
    topic = topic.strip()
    if topic.lower().startswith("appendix"):
        return "Appendix"
    m = CHAPTER_KEY.match(topic)
    if m:
        return next(g for g in m.groups() if g).replace("  ", " ").strip()
    pm = PART_EVIDENCE.search(evidence)
    if pm:
        return f"part-{pm.group(1)}"
    return topic.split("—")[0].split("-")[0].strip()[:48] or "misc"


def extract_concept_slugs(cells: list[str]) -> list[str]:
    slugs: list[str] = []
    for cell in cells[2:]:
        for m in WIKILINK.finditer(cell):
            slug = m.group(1).strip()
            if slug.startswith("sources/") or slug.startswith("domains/"):
                continue
            if slug not in slugs:
                slugs.append(slug)
    return slugs


def parse_topic_map(body: str) -> list[TopicRow]:
    m = TOPIC_MAP_HEADING.search(body)
    if not m:
        return []
    tail = body[m.end() :]
    rows: list[TopicRow] = []
    for line in tail.splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*[-—]", line):
            continue
        tm = TABLE_ROW.match(line)
        if not tm:
            continue
        cells = [c.strip() for c in tm.group(1).split("|")]
        if len(cells) < 4:
            continue
        if cells[0].lower() in {"topic", "…", "..."}:
            continue
        topic, evidence, existing, action = cells[0], cells[1], cells[2], cells[3]
        key = chapter_key_from_row(topic, evidence)
        rows.append(
            TopicRow(
                chapter_key=key,
                topic=topic,
                evidence=evidence,
                existing=existing,
                action=action,
                concept_slugs=extract_concept_slugs(cells),
            )
        )
    return rows


def parse_next_sections(raw: str) -> list[str]:
    raw = (raw or "[]").strip()
    if not raw or raw == "[]":
        return []
    try:
        val = ast.literal_eval(raw)
        if isinstance(val, list):
            return [str(x) for x in val]
    except (SyntaxError, ValueError):
        pass
    return [s.strip() for s in raw.split(",") if s.strip()]


def format_next_sections(keys: list[str]) -> str:
    return json.dumps(keys, ensure_ascii=False)


def group_by_chapter(rows: list[TopicRow]) -> dict[str, list[TopicRow]]:
    groups: dict[str, list[TopicRow]] = {}
    for r in rows:
        groups.setdefault(r.chapter_key, []).append(r)
    return groups


def find_batch_script(slug: str) -> Path | None:
    scripts = Path(__file__).resolve().parent
    candidate = scripts / f"batch-ingest-{slug}.py"
    return candidate if candidate.is_file() else None


def md_paths_for_evidence(wiki: Path, source_slug: str, evidence: str) -> list[str]:
    paths: list[str] = []
    for pm in PART_EVIDENCE.finditer(evidence):
        rel = f"sources/{source_slug}/md/part-{pm.group(1)}.md"
        if (wiki / rel).is_file():
            paths.append(rel)
    for m in WIKILINK.finditer(evidence):
        link = m.group(1)
        p = wiki / link if link.startswith("sources/") else wiki / link
        if not p.suffix:
            p = p.with_suffix(".md")
        if p.is_file():
            paths.append(str(p.relative_to(wiki)))
    return paths


def render_batch_markdown(
    source_slug: str,
    batch_keys: list[str],
    groups: dict[str, list[TopicRow]],
    wiki: Path,
    batch_script: Path | None,
) -> str:
    lines = [f"## Ingest batch — sources/{source_slug}", ""]
    for key in batch_keys:
        lines.append(f"### {key}")
        for row in groups.get(key, []):
            lines.append(f"- **Topic:** {row.topic}")
            lines.append(f"  - Evidence: {row.evidence}")
            if row.concept_slugs:
                lines.append(f"  - Concepts: {', '.join('[[%s]]' % s for s in row.concept_slugs)}")
            else:
                lines.append(f"  - Action: {row.action}")
            md_files = md_paths_for_evidence(wiki, source_slug, row.evidence)
            if md_files:
                lines.append(f"  - Read MD: {', '.join(f'[[{p}]]' for p in md_files)}")
        lines.append("")
    lines.extend(
        [
            "**Agent checklist (one batch per turn):**",
            "1. Read MD anchors above only — not whole book",
            "2. Write/update `wiki/concepts/` per `concept-claim-rubric.md`",
            "3. `patch-claim-two-layers.py --apply --slug` on new concepts",
            "4. `lint_explain_back_coverage.py` on touched slugs",
            f"5. Mark done: `ingest-batch-chapters.py <wiki> --source {source_slug} --mark-done \"{batch_keys[0]}\"`",
            "",
        ]
    )
    if batch_script:
        lines.append(f"**Optional one-shot script:** `{batch_script.name}` (if re-ingesting entire source)")
    return "\n".join(lines)


def update_source_page(
    path: Path,
    fm: dict[str, str],
    body: str,
    next_sections: list[str],
    concepts_added: int = 0,
    today: str | None = None,
) -> None:
    today = today or date.today().isoformat()
    fm["ingest_status"] = "complete" if not next_sections else "partial"
    fm["next_sections"] = format_next_sections(next_sections)
    fm["last_ingest"] = today
    if concepts_added:
        try:
            prev = int(fm.get("concepts_deepened", "0") or "0")
        except ValueError:
            prev = 0
        fm["concepts_deepened"] = str(prev + concepts_added)
    fm.setdefault("type", "source")
    path.write_text(f"{dump_frontmatter(fm)}\n\n{body.lstrip()}", encoding="utf-8")


def init_next_sections(rows: list[TopicRow]) -> list[str]:
    seen: list[str] = []
    for r in rows:
        if r.chapter_key not in seen:
            seen.append(r.chapter_key)
    return seen


def cmd_plan(
    source_slug: str,
    rows: list[TopicRow],
    fm: dict[str, str],
    pending: list[str],
    as_json: bool,
) -> int:
    groups = group_by_chapter(rows)
    all_keys = init_next_sections(rows)
    done = [k for k in all_keys if k not in pending]
    payload = {
        "source": source_slug,
        "ingest_status": fm.get("ingest_status", "(unset)"),
        "chapters_total": len(all_keys),
        "chapters_done": len(done),
        "chapters_pending": pending,
        "chapters": [
            {
                "key": k,
                "status": "pending" if k in pending else "done",
                "topics": [r.topic for r in groups[k]],
                "concepts": [s for r in groups[k] for s in r.concept_slugs],
            }
            for k in all_keys
        ],
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"INGEST BATCH — sources/{source_slug}")
    print(f"  status={payload['ingest_status']}  done={payload['chapters_done']}/{payload['chapters_total']}")
    for ch in payload["chapters"]:
        mark = "TODO" if ch["status"] == "pending" else "DONE"
        print(f"  [{mark}] {ch['key']}: {len(ch['topics'])} topic(s)")
    if pending:
        print(f"\nNext pending: {pending[0]}")
    else:
        print("\nAll chapters marked done.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wiki", type=Path, help="Path to vault wiki/")
    ap.add_argument("--source", required=True, help="Source slug (sources/<slug>.md)")
    ap.add_argument("--init", action="store_true", help="Seed next_sections from topic map")
    ap.add_argument("--mark-done", metavar="CHAPTER", help="Mark chapter key done")
    ap.add_argument("--chapters", type=int, default=1, help="Chapters per batch output (default 1)")
    ap.add_argument("--concepts-added", type=int, default=0, help="With --mark-done, increment concepts_deepened")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    wiki = args.wiki.resolve()
    source_slug = args.source.strip().removesuffix(".md")
    source_path = wiki / "sources" / f"{source_slug}.md"
    if not source_path.is_file():
        print(f"Missing {source_path}", file=sys.stderr)
        return 2

    text = source_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    rows = parse_topic_map(body)
    if not rows:
        print(f"No topic map rows in {source_path}", file=sys.stderr)
        return 2

    groups = group_by_chapter(rows)
    all_keys = init_next_sections(rows)
    pending = parse_next_sections(fm.get("next_sections", "[]"))
    if not pending and fm.get("ingest_status") != "complete":
        pending = list(all_keys)

    if args.init:
        pending = list(all_keys)
        fm["ingest_status"] = "partial"
        fm["next_sections"] = format_next_sections(pending)
        fm.setdefault("concepts_deepened", "0")
        if not args.dry_run:
            update_source_page(source_path, fm, body, pending, concepts_added=0)
        print(f"{'Would init' if args.dry_run else 'Initialized'} {len(pending)} chapters in next_sections")
        return 0

    if args.mark_done:
        key = args.mark_done.strip()
        # fuzzy match
        match = next((k for k in pending if k.lower() == key.lower()), None)
        if not match:
            match = next((k for k in pending if key.lower() in k.lower()), None)
        if not match:
            print(f"Chapter not in pending list: {key!r} — pending={pending}", file=sys.stderr)
            return 1
        pending = [k for k in pending if k != match]
        if not args.dry_run:
            update_source_page(
                source_path,
                fm,
                body,
                pending,
                concepts_added=args.concepts_added,
            )
        print(f"{'Would mark' if args.dry_run else 'Marked'} done: {match} — {len(pending)} chapter(s) left")
        return 0

    if args.json and not pending:
        return cmd_plan(source_slug, rows, fm, pending, True)

    if not pending:
        return cmd_plan(source_slug, rows, fm, pending, args.json)

    batch_keys = pending[: max(1, args.chapters)]
    batch_script = find_batch_script(source_slug)

    if args.json:
        out = {
            "source": source_slug,
            "batch": batch_keys,
            "rows": [
                {
                    "chapter": k,
                    "topic": r.topic,
                    "evidence": r.evidence,
                    "concepts": r.concept_slugs,
                }
                for k in batch_keys
                for r in groups.get(k, [])
            ],
            "batch_script": str(batch_script) if batch_script else None,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print(render_batch_markdown(source_slug, batch_keys, groups, wiki, batch_script))
    print(
        f"Progress: {len(all_keys) - len(pending)}/{len(all_keys)} chapters done · "
        f"pending={format_next_sections(pending)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
