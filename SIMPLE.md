# Zhuomo — simplified mode

The full system has 9 operations, 10+ repo docs, and optional learn/run/retention loops. **You don't need all of that to start.**

## Minimum viable Zhuomo

```
Raw file  →  Ingest  →  concept pages  →  Query when you need answers
```

That's it for phase 1.

| Keep | Drop (until you want them) |
|------|----------------------------|
| `~/zhuomo-data/raw/` inbox | Domain skills |
| Obsidian `wiki/concepts/` | Run (roguelike) |
| `wiki/overview.md` | Weekly ritual |
| `wiki/sources/` one-line summary | 10 repo markdown files — read only USER-GUIDE + this file |
| Natural-language chat with agent | Mandatory Evidence tables (use in *deepen* pass only) |

## Three phases

| Phase | Trigger | Agent does |
|-------|---------|------------|
| **1 — Map** | `Ingest overview only: book.epub` | Source page + topic map + **stub** concept pages (5–10 bullets each) + `wiki/overview.md` update |
| **2 — Deepen** | `Deepen tenant` or `Deepen all` | Expand chosen concepts + Evidence links |
| **3 — Remember** | `Learn recap` | Digest + recall cards only |

Skip phase 2 until you actually need reference depth on a topic.

## Single-domain shortcut

One subject (e.g. only Cisco ACI)?

- Use `wiki/overview.md` instead of juggling `index` + `domain-map` + `framework`
- `domain-map.md` — add when you have a **second** domain
- Flat `wiki/concepts/` — fine; no need for `wiki/domains/*/` until pillars multiply

## Ingest depth (say this explicitly)

| Mode | When | Output size |
|------|------|-------------|
| `overview only` | First pass on big book | ~10 pages, topic map, stubs |
| `deepen [topic]` | You care about one chapter | 1–3 full concept pages |
| `reference depth` / `deepen all` | Exam / design reference | Full tables + Evidence (what you did for ACI) |

**Default recommendation:** start `overview only`; deepen on demand. Avoid `deepen all` unless you need a design reference wiki.

## EPUB workflow (lite)

Full workflow: convert entire EPUB → `md/` corpus → Evidence on every page.

**Lite:**

1. Ingest overview from EPUB directly (no md corpus)
2. When you deepen one chapter → run `scripts/epub-to-wiki-md.py` once; add Evidence only on pages you deepen

## Obsidian: three levels, two pages per domain

| View | Where | Answers |
|------|-------|---------|
| **Vault overview** | `wiki/overview.md` | Which domains exist; where to put new sources (**stays short**) |
| **Domain overview** | `wiki/domains/<domain>/overview.md` | Why learn, pillars, progress, glossary |
| **Domain guide** | `wiki/domains/<domain>/guide.md` | Technical one-page digest (optional) |

No separate `framework.md` or `mega-overview.md` — merged into overview + guide.

Set Obsidian **Settings → Files → Default open file** to `wiki/overview.md` if you want it on every launch.

## Repo docs — what to read

| Read | Skip until needed |
|------|-------------------|
| [USER-GUIDE.md](USER-GUIDE.md) § Quick start | RUN.md, RETENTION.md, WIKI-BACKED-SKILLS.md |
| This file (SIMPLE.md) | FRAMEWORK.md (same ideas, longer) |
| [SKILL.md](SKILL.md) — only if customizing agent | KNOWLEDGE-BASE.md, REFERENCE.md (agent reference) |

## One-line prompts

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, vault ~/Obsidian/zhuomo-vault

/zhuomo Ingest overview only: ~/zhuomo-data/raw/inbox/book.epub

/zhuomo Deepen: tenant model from book.epub

/zhuomo Query: how does contract direction work? cite wiki

/zhuomo Revise: aci-tenant-epg-contract — ESG Multi-Site note is wrong
```

## What made your ACI vault feel complex

You ran **reference-depth deepen all** on a 6000-line design guide → 13 concept pages + md corpus + learn artifacts. That's the **maximal** path.

For the next book, try:

```
/zhuomo Ingest overview only: next-book.epub
```

Open `wiki/overview.md` — if the topic map looks right, deepen one cluster at a time.
