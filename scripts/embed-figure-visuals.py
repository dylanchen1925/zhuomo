#!/usr/bin/env python3
"""Embed figure visuals inline where Figure N is mentioned in wiki concept pages.

Prefers source MD corpus images (EPUB extract); falls back to mermaid schematics.
Removes consolidated ``## Figures`` sections (legacy).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from corpus_assets import DEFAULT_CORPUS_ROOT, asset_vault_path, corpus_root_from_arg, slug_assets_dir

IMG_LINE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
EVIDENCE_LINK = re.compile(
    r"\[\[sources/([^/\]]+)/md/([^#\|\]]+)(?:#[^\|\]]+)?(?:\|[^\]]*)?\]\]"
)
ANCHOR_IN_LINK = re.compile(r"#([^\|\]]+)")
FIGURE_NUM = re.compile(r"Figure\s+([\d\-\.]+)", re.I)
ANCHOR_FIGURE = re.compile(r"figure-([\d\-\.]+)", re.I)
INLINE_MARKER = re.compile(
    r"^!\[Figure\s+([\d\-\.]+)\]|^→ \[\[sources/.*#figure-([\d\-\.]+)\]\]"
)
MERMAID_MARKER = re.compile(r"^```mermaid\s*$")

MERMAID_FALLBACK: dict[str, dict[str, str]] = {
    "aci-vlan-pools-aaep": {
        "26": """flowchart TD
  SP[Switch profile] --> IP[Interface policy]
  IP --> PG[Policy group per vPC/PC]
  PG --> AAEP[AAEP]
  AAEP --> DOM[Domain]
  DOM --> VP[VLAN pool]""",
    },
    "aci-fabric-underlay": {
        "12": """flowchart LR
  SW[Leaf/Spine] -->|LLDP+DHCP| APIC[APIC]
  APIC -->|HTTP GET firmware| SW""",
    },
    "aci-l3out-transit-routing": {
        "88": """flowchart LR
  R10[Router 10/8] --> L3A[L3Out A]
  L3A --> FAB[ACI fabric]
  FAB --> L3B[L3Out B]
  L3B --> R20[Router 20/8]""",
    },
    "aci-multi-pod-migration": {
        "50": """flowchart TD
  SF[Stretched fabric Pod1] --> IPN[IPN]
  IPN --> P2[New Pod2]
  SF -->|Hard split| TEP[Shared TEP pool must divide]""",
    },
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path, help="Path to vault wiki/ folder")
    p.add_argument(
        "--corpus-root",
        type=Path,
        default=DEFAULT_CORPUS_ROOT,
        help=f"External corpus root (default: {DEFAULT_CORPUS_ROOT})",
    )
    p.add_argument(
        "--concepts-glob",
        default="concepts/*.md",
        help="Glob under wiki_dir for concept pages",
    )
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def load_corpus_index(wiki_dir: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for src in (wiki_dir / "sources").iterdir():
        md = src / "md"
        if md.is_dir():
            out[src.name] = md
    return out


def norm_fig(fig: str) -> str:
    return fig.strip().replace("_", "-")


def find_image_at_anchor(part_text: str, anchor: str) -> str | None:
    m = re.search(rf"^##[^\n]*\{{#{re.escape(anchor)}\}}", part_text, re.I | re.M)
    if not m:
        return None
    before = part_text[: m.start()]
    imgs = IMG_LINE.findall(before)
    if imgs:
        return imgs[-1]
    after = part_text[m.end() : m.end() + 800]
    post = IMG_LINE.findall(after)
    return post[0] if post else None


def _leading_digits(fig_num: str) -> int | None:
    m = re.match(r"(\d+)", fig_num.strip())
    return int(m.group(1)) if m else None


def find_image_for_figure_num(
    corpus_md: Path, fig_num: str, slug: str, corpus_root: Path
) -> tuple[str, str] | None:
    assets_on_disk = slug_assets_dir(corpus_root, slug)
    candidates_img: list[str] = []
    lead = _leading_digits(fig_num.split("-", 1)[0])
    if lead is not None:
        candidates_img.append(f"image{lead:03d}.jpg")
    candidates_img.append(f"image{fig_num.replace('.', '').replace('-', '')}.jpg")
    if "-" in fig_num:
        a, b = fig_num.split("-", 1)
        candidates_img.append(f"{a.zfill(2)}fig{b.zfill(2)}.jpg")
        candidates_img.append(f"{a}fig{b}.jpg")

    for part in sorted(corpus_md.glob("part-*.md")):
        text = part.read_text(encoding="utf-8", errors="replace")
        if not re.search(rf"Figure\s+{re.escape(fig_num)}\b", text, re.I):
            continue
        anchor = f"figure-{fig_num.replace('.', '-')}"
        img = find_image_at_anchor(text, anchor)
        if img:
            return part.name, img
        idx = text.lower().find(f"figure {fig_num.lower()}")
        if idx >= 0:
            window = text[max(0, idx - 400) : idx + 400]
            imgs = IMG_LINE.findall(window)
            if imgs:
                return part.name, imgs[-1]

    for name in candidates_img:
        if (assets_on_disk / name).is_file():
            return "part-000.md", asset_vault_path(slug, name)

    return None


def collect_figure_nums(text: str) -> set[str]:
    nums = {norm_fig(m) for m in FIGURE_NUM.findall(text)}
    for m in ANCHOR_FIGURE.finditer(text):
        nums.add(norm_fig(m.group(1)))
    return nums


def resolve_visual(
    fig_num: str,
    text: str,
    corpus: dict[str, Path],
    concept_slug: str,
    corpus_root: Path,
) -> tuple[str, str] | None:
    """Return (block_md, kind) where kind is image|mermaid."""
    label = f"Figure {fig_num}"
    search_slugs = [m.group(1) for m in EVIDENCE_LINK.finditer(text)] or list(corpus.keys())

    for src_slug in search_slugs:
        if src_slug not in corpus:
            continue
        hit = find_image_for_figure_num(corpus[src_slug], fig_num, src_slug, corpus_root)
        if not hit:
            continue
        part_name, img = hit
        if img.startswith("/corpus/"):
            vault_path = img
        elif img.startswith("assets/"):
            vault_path = asset_vault_path(src_slug, Path(img).name)
        else:
            vault_path = f"sources/{src_slug}/md/{img.lstrip('./')}"
        part_base = part_name.replace(".md", "")
        link = f"[[sources/{src_slug}/md/{part_base}#figure-{fig_num.replace('.', '-')}]]"
        block = f"\n![{label}]({vault_path})\n\n→ {link}\n"
        return block, "image"

    mmd = MERMAID_FALLBACK.get(concept_slug, {}).get(fig_num)
    if not mmd and "-" in fig_num:
        mmd = MERMAID_FALLBACK.get(concept_slug, {}).get(fig_num.split("-")[0])
    if mmd:
        block = f"\n```mermaid\n{mmd.strip()}\n```\n"
        return block, "mermaid"
    return None


def strip_figures_section(text: str) -> str:
    return re.sub(r"^## Figures\s*\n.*?(?=^## |\Z)", "", text, count=1, flags=re.M | re.S)


def split_body_tail(text: str) -> tuple[str, str]:
    m = re.search(r"^## Evidence\s*$", text, re.M)
    if not m:
        return text, ""
    return text[: m.start()], text[m.start() :]


def already_inline_after(lines: list[str], idx: int, fig_num: str) -> bool:
    """True if visual for fig_num already follows this line."""
    for j in range(idx + 1, min(idx + 8, len(lines))):
        line = lines[j].strip()
        if line.startswith("## "):
            break
        m = INLINE_MARKER.match(line)
        if m and norm_fig(m.group(1) or m.group(2) or "") == fig_num:
            return True
        if MERMAID_MARKER.match(line) and j == idx + 1:
            return True
    return False


def strip_existing_inline_figures(text: str) -> str:
    """Remove prior embed blocks (image + source link, or lone mermaid) for idempotent re-run."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = INLINE_MARKER.match(line.strip())
        if m:
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            if i < len(lines) and lines[i].strip().startswith("→ [[sources/"):
                i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        if MERMAID_MARKER.match(line.strip()):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            if i < len(lines):
                i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def evidence_bullets(tail: str) -> list[str]:
    return [ln for ln in tail.splitlines() if ln.lstrip().startswith("- ")]


def section_hint_for_figure(fig: str, bullets: list[str]) -> str | None:
    fig_pat = re.compile(rf"figure-{re.escape(fig.replace('.', '-'))}|Figure\s+{re.escape(fig)}\b", re.I)
    for bullet in bullets:
        if not fig_pat.search(bullet):
            continue
        if re.search(r"rail-unified|rud\b", bullet, re.I):
            return "vs rod"
        if re.search(r"dragonfly", bullet, re.I):
            return "dragonfly"
        if re.search(r"multi-planar|multi.?planar", bullet, re.I):
            return "multi-planar"
        if re.search(r"rail-only", bullet, re.I):
            return "rail-only"
        if re.search(r"rail-optimized|intra.?rail", bullet, re.I):
            return "mechanics"
        if re.search(r"jct\b|job.?completion", bullet, re.I):
            return "jct defined"
        if re.search(r"tail.?latency", bullet, re.I):
            return "tail latency"
        if re.search(r"transport|roce|rdma", bullet, re.I):
            return "transport"
        if re.search(r"scheduler|scheduled|fabric-controller", bullet, re.I):
            return "concept"
        if re.search(r"load.?balanc|traffic.?engineer", bullet, re.I):
            return "relation"
    return None


def insert_at_section_end(body: str, section_key: str, block: str) -> str:
    """Insert block after last non-empty line of first ## section whose title matches section_key."""
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and section_key in line.lower():
            start = i
            break
    if start is None:
        return body
    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    insert_at = end - 1
    while insert_at > start and not lines[insert_at].strip():
        insert_at -= 1
    lines[insert_at + 1 : insert_at + 1] = ["", block.rstrip("\n"), ""]
    return "\n".join(lines) + ("\n" if body.endswith("\n") else "")


def insert_inline_visuals(
    body: str,
    visuals: dict[str, tuple[str, str]],
) -> str:
    lines = body.splitlines()
    candidates: dict[str, tuple[int, int]] = {}

    for i, line in enumerate(lines):
        is_heading = line.startswith("## ")
        for m in FIGURE_NUM.finditer(line):
            fig = norm_fig(m.group(1))
            if fig not in visuals:
                continue
            pri = 1 if is_heading else 0
            cur = candidates.get(fig)
            if cur is None or pri < cur[0] or (pri == cur[0] and i < cur[1]):
                candidates[fig] = (pri, i)
        for m in ANCHOR_FIGURE.finditer(line):
            fig = norm_fig(m.group(1))
            if fig not in visuals:
                continue
            pri = 1 if is_heading else 0
            cur = candidates.get(fig)
            if cur is None or pri < cur[0] or (pri == cur[0] and i < cur[1]):
                candidates[fig] = (pri, i)

    insertions: list[tuple[int, str]] = []
    for fig, (_, idx) in sorted(candidates.items(), key=lambda x: x[1][1]):
        if already_inline_after(lines, idx, fig):
            continue
        insertions.append((idx, visuals[fig][0]))

    for idx, block in sorted(insertions, key=lambda x: x[0], reverse=True):
        lines[idx : idx + 1] = [lines[idx], block.rstrip("\n")]

    return "\n".join(lines) + ("\n" if body.endswith("\n") else "")


def promote_unplaced_to_body(
    body: str,
    tail: str,
    visuals: dict[str, tuple[str, str]],
    placed: set[str],
) -> str:
    bullets = evidence_bullets(tail)
    for fig in visuals:
        if fig in placed:
            continue
        hint = section_hint_for_figure(fig, bullets)
        if not hint:
            continue
        updated = insert_at_section_end(body, hint, visuals[fig][0])
        if updated != body:
            body = updated
            placed.add(fig)
    return body


def insert_evidence_inline(
    tail: str,
    visuals: dict[str, tuple[str, str]],
    placed: set[str],
) -> str:
    lines = tail.splitlines()
    insertions: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("- "):
            continue
        figs: set[str] = set()
        for m in ANCHOR_FIGURE.finditer(line):
            figs.add(norm_fig(m.group(1)))
        for m in FIGURE_NUM.finditer(line):
            figs.add(norm_fig(m.group(1)))
        for fig in figs:
            if fig in placed or fig not in visuals:
                continue
            if already_inline_after(lines, i, fig):
                placed.add(fig)
                continue
            insertions.append((i, visuals[fig][0]))
            placed.add(fig)
    for idx, block in sorted(insertions, key=lambda x: x[0], reverse=True):
        lines[idx : idx + 1] = [lines[idx], block.rstrip("\n")]
    return "\n".join(lines) + ("\n" if tail.endswith("\n") else "")


def figures_embedded(text: str) -> set[str]:
    embedded: set[str] = set()
    for m in INLINE_MARKER.finditer(text):
        embedded.add(norm_fig(m.group(1) or m.group(2) or ""))
    return embedded


def transform_concept(
    content: str, concept_slug: str, corpus: dict[str, Path], corpus_root: Path
) -> str | None:
    if not re.search(r"Figure\s+[\d\-]|#figure-", content, re.I):
        return None

    content = strip_figures_section(content)
    content = strip_existing_inline_figures(content)
    body, tail = split_body_tail(content)

    nums = collect_figure_nums(content)
    visuals: dict[str, tuple[str, str]] = {}
    for fig in nums:
        v = resolve_visual(fig, content, corpus, concept_slug, corpus_root)
        if v:
            visuals[fig] = v

    if not visuals:
        return None

    placed: set[str] = set()
    new_body = insert_inline_visuals(body, visuals)
    placed |= figures_embedded(new_body)
    new_body = promote_unplaced_to_body(new_body, tail, visuals, placed)
    placed |= figures_embedded(new_body)
    new_tail = insert_evidence_inline(tail, visuals, placed) if tail else ""

    new_content = new_body.rstrip() + "\n\n" + new_tail.lstrip() if new_tail else new_body
    if new_content != content:
        return new_content
    return None


def main() -> int:
    args = parse_args()
    wiki_dir = args.wiki_dir.resolve()
    corpus_root = corpus_root_from_arg(args.corpus_root)
    corpus = load_corpus_index(wiki_dir)
    updated = 0

    for path in sorted(wiki_dir.glob(args.concepts_glob)):
        old = path.read_text(encoding="utf-8", errors="replace")
        new = transform_concept(old, path.stem, corpus, corpus_root)
        if new is None:
            continue
        updated += 1
        print(path.relative_to(wiki_dir))
        if not args.dry_run:
            path.write_text(new, encoding="utf-8")

    print(f"Updated {updated} concept page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
