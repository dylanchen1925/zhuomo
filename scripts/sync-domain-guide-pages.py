#!/usr/bin/env python3
"""Create missing domains/<slug>/guide.md from overview.md (Domain 四页 — guide 补全)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from domain_study_tiers import VIRTUAL_DOMAIN_PARENT  # noqa: E402

SECTION_RE = re.compile(r"^(## .+)$", re.M)
CAREER_TRACKS = frozenset({"ai-platform-career-track", "hft-network-career-track"})


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, parts[2]


def domain_title(text: str, slug: str) -> str:
    m = re.search(r"^# (.+?) —", text, re.M)
    if m:
        return m.group(1).strip()
    return slug.replace("-", " ").title()


def extract_section(body: str, headings: list[str]) -> str:
    for h in headings:
        pat = re.compile(rf"({re.escape(h)}\n.*?)(?=\n## |\Z)", re.S)
        m = pat.search(body)
        if m:
            return m.group(1).strip()
    return ""


def build_career_guide(slug: str, title: str, body: str, updated: str) -> str:
    hub = extract_section(body, ["## 父域 Hub（知识从哪来）", "## 父域 Hub"])
    time_block = extract_section(body, ["## 时间分配", "## 与 AI Platform 轨的关系"])
    lines = [
        "---",
        f"domain: {slug}",
        "type: domain-guide",
        f"updated: {updated}",
        "---",
        "",
        f"# {title} — 一页通",
        "",
        f"> 跨域职业轨。进度 → [[domains/{slug}/study]] · 周计划 → [[domains/{slug}/phases]] · 发表 → [[domains/{slug}/publish-plan]]",
        "",
        "## 入口",
        "",
        "| 页 | 用途 |",
        "|----|------|",
        f"| [[domains/{slug}/overview]] | 战略与资源 |",
        f"| [[domains/{slug}/map]] | 纲领 / whole picture |",
        f"| [[domains/{slug}/study]] | 进度 + milestones |",
        f"| [[domains/{slug}/phases]] | Phase 周计划 |",
        "",
    ]
    if time_block:
        lines.extend([time_block, ""])
    if hub:
        lines.extend([hub, ""])
    lines.extend(
        [
            "## 建议学习顺序",
            "",
            f"见 [[domains/{slug}/phases]]；概念 mastery 按父域 **study** 表推进（Cilium / 安全 / AI fabric 等）。",
            "",
            "## 相关",
            "",
            f"- **进度：** [[domains/{slug}/study]]",
            f"- **总览：** [[domains/{slug}/overview]]",
            "",
        ]
    )
    return "\n".join(lines)


def build_standard_guide(slug: str, title: str, body: str, fm: dict[str, str], updated: str) -> str:
    parent = fm.get("parent") or VIRTUAL_DOMAIN_PARENT.get(slug, "")
    prefix = extract_section(body, ["## Slug 前缀规则"])
    pillars = extract_section(body, ["## 支柱地图", "## 支柱"])
    study_path = extract_section(
        body, ["## 建议学习顺序（草案）", "## 建议学习顺序", "## Study path"]
    )
    architect = extract_section(body, ["## 架构师视角"])
    related = extract_section(body, ["## 相关虚拟域", "## 相关"])

    lines = [
        "---",
        f"domain: {slug}",
        "type: domain-guide",
        f"updated: {updated}",
        "---",
        "",
        f"# {title} — 一页通",
        "",
        f"> Vault 入口：[[domains/{slug}/overview]] · 纲领 [[domains/{slug}/map]] · 进度 [[domains/{slug}/study]]",
        "",
    ]
    if parent:
        lines.extend(
            [
                f"> **虚拟域**（parent: `{parent}`）。concept 的 `domain:` 仍写在原归属；本页按 slug 前缀 / 主题聚合。",
                f"> Hub：[[domains/{parent}/overview]]",
                "",
            ]
        )
    if prefix:
        lines.extend([prefix, ""])
    if pillars:
        lines.extend([pillars, ""])
    if study_path:
        lines.extend([study_path, ""])
    elif architect:
        lines.extend([architect, ""])
    else:
        lines.extend(
            [
                "## 建议学习顺序",
                "",
                f"与 [[domains/{slug}/overview#建议学习顺序]] 同步；日常从 [[domains/{slug}/study]] **下一步** 列开始。",
                "",
            ]
        )
    if related:
        lines.extend([related, ""])
    lines.extend(
        [
            "## 相关",
            "",
            f"- **进度：** [[domains/{slug}/study]]",
            f"- **总览：** [[domains/{slug}/overview]]",
            f"- **纲领：** [[domains/{slug}/map]]",
            "",
        ]
    )
    return "\n".join(lines)


def build_guide(slug: str, overview_text: str, updated: str) -> str:
    fm, body = parse_frontmatter(overview_text)
    title = domain_title(body, slug)
    if slug in CAREER_TRACKS or fm.get("type") == "virtual-collection":
        return build_career_guide(slug, title, body, updated)
    return build_standard_guide(slug, title, body, fm, updated)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("vault_wiki", type=Path, help="Path to vault wiki/")
    ap.add_argument("--date", default="2026-08-28")
    ap.add_argument("--force", action="store_true", help="Overwrite existing guide.md")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    domains_dir = args.vault_wiki.resolve() / "domains"
    n = 0
    for dom in sorted(domains_dir.iterdir()):
        if not dom.is_dir():
            continue
        slug = dom.name
        ov = dom / "overview.md"
        gd = dom / "guide.md"
        if not ov.is_file():
            continue
        if gd.is_file() and not args.force:
            continue
        content = build_guide(slug, ov.read_text(encoding="utf-8"), args.date)
        n += 1
        print(f"guide: {gd}")
        if not args.dry_run:
            gd.write_text(content, encoding="utf-8")
    print(f"guide pages written: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
