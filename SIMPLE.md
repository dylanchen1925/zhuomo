# Zhuomo — simplified mode

The full system has 9 operations, 10+ repo docs, and optional learn/run/retention loops. **You don't need all of that to start.**

## Minimum viable Zhuomo

```
Raw file  →  Bootstrap + Ingest  →  full concept pages (+ Evidence)  →  Query
```

That's it for phase 1. **Daily cheatsheet:** Obsidian `wiki/help.md` (created on bootstrap from `templates/wiki/help.md`).

| Keep | Drop (until you want them) |
|------|----------------------------|
| `~/zhuomo-data/raw/` inbox | Domain skills |
| Obsidian `wiki/concepts/` | Explain-back per concept |
| `wiki/overview.md` | Weekly ritual |
| `wiki/sources/` + md corpus | 10 repo markdown files — read only USER-GUIDE + this file |
| Natural-language chat with agent | — |

## Default: reference depth at bootstrap

**Bootstrap + first ingest** runs **deepen all** — not stubs:

| Step | Agent does |
|------|------------|
| **Bootstrap** | Folders + `AGENTS.md` (reference depth default) + wiki skeleton |
| **Ingest** | Topic map → EPUB md corpus → **every concept deepened** + Evidence + domain `overview.md` |

Say **`overview only`** or **`lite`** anytime to get the old stub-first path instead.

## Lite mode (opt-in)

| Phase | Trigger | Agent does |
|-------|---------|------------|
| **1 — Map** | `Ingest overview only: book.epub` | Topic map + **stub** concepts (5–10 bullets each) |
| **2 — Deepen** | `Deepen tenant` or `Deepen all` | Expand chosen concepts + Evidence links |
| **3 — Remember** | `Explain-back [[concept]]` or `Learn fable: [[concept]]` | Teach-back or narrative intuition |

Use lite for huge books when you only want a topic map first.

## Ingest depth (say this explicitly)

| Mode | When | Output size |
|------|------|-------------|
| **`reference depth`** (default) | Bootstrap, normal ingest | md corpus + all concepts deepened + Evidence |
| `overview only` / `lite` | Quick map only | ~10 stubs, topic map |
| `deepen [topic]` | One cluster after lite pass | 1–3 full concept pages |
| `archive only` | Storage, no learn | Wiki pages only |

## EPUB workflow (default)

1. Copy EPUB to `raw/books/`
2. Run `scripts/epub-to-wiki-md.py` → `wiki/sources/[slug]/md/` (+ images in `md/assets/`)
3. Ingest with **deepen all** — Evidence on every concept page

Lite EPUB: skip step 2 until you deepen; ingest `overview only` from EPUB directly.

## Obsidian: three levels, two pages per domain

| View | Where | Answers |
|------|-------|---------|
| **Vault overview** | `wiki/overview.md` | Which domains exist; where to put new sources (**stays short**) |
| **Domain overview** | `wiki/domains/<domain>/overview.md` | Why learn, pillars, progress, glossary |
| **Domain guide** | `wiki/domains/<domain>/guide.md` | Technical one-page digest (optional) |

Set Obsidian **Settings → Files → Default open file** to `wiki/overview.md` if you want it on every launch.

## Repo docs — what to read

| Read | Skip until needed |
|------|-------------------|
| Obsidian **`wiki/help.md`** | — |
| [USER-GUIDE.md](USER-GUIDE.md) | Full setup and daily use |
| [REVIEW.md](REVIEW.md) | Explain-back and review queue |
| This file (SIMPLE.md) | FRAMEWORK.md (same ideas, longer) |
| [SKILL.md](SKILL.md) — only if customizing agent | KNOWLEDGE-BASE.md, REFERENCE.md (agent reference) |

## One-line prompts

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, vault ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen

/zhuomo Bootstrap + ingest: ~/zhuomo-data/raw/books/my-book.epub

/zhuomo Ingest: ~/zhuomo-data/raw/inbox/book.epub

/zhuomo Ingest overview only: book.epub

/zhuomo Query think: Multi-Pod vs Multi-Site — when to use which?

/zhuomo Lint

/zhuomo Weekly

/zhuomo Learn fable: [[tenant-epg-contract]] — story first, reveal at end
```

## Bootstrap lite (opt-out)

```
/zhuomo Bootstrap lite: raw ~/zhuomo-data/raw/, vault ~/path/to/vault
/zhuomo Ingest overview only: next-book.epub
```
