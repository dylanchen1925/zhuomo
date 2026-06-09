# Zhuomo User Guide

Detailed guide for **you** (not the agent). How to set up 琢磨, run each operation, and build a personal wiki + skills over time.

**Quick links:** [FRAMEWORK.md](FRAMEWORK.md) (conceptual model) · [SKILL.md](SKILL.md) (agent entry) · [README.md](README.md) (repo index)

---

## Table of contents

1. [What Zhuomo is](#1-what-zhuomo-is)
2. [Prerequisites](#2-prerequisites)
3. [First-time setup](#3-first-time-setup)
4. [Daily and weekly habits](#4-daily-and-weekly-habits)
5. [Operations reference](#5-operations-reference)
6. [Prompt cookbook](#6-prompt-cookbook)
7. [Learning from sources](#7-learning-from-sources)
8. [Building domain frameworks](#8-building-domain-frameworks)
9. [Retention and review](#9-retention-and-review)
10. [Creating agent skills](#10-creating-agent-skills)
11. [Domain skills (wiki-backed experts)](#11-domain-skills-wiki-backed-experts)
12. [Correcting and updating knowledge](#12-correcting-and-updating-knowledge)
13. [Multi-device workflow](#13-multi-device-workflow)
14. [Source types](#14-source-types)
15. [Troubleshooting](#15-troubleshooting)
16. [Roguelike runs](#16-roguelike-runs)
17. [FAQ](#17-faq)

---

## 1. What Zhuomo is

**琢磨** means to polish and chew over material until it is clear and usable.

You give Zhuomo:

- Books (EPUB), articles, videos, notes, highlights

Zhuomo helps you produce:

| Output | What it is for |
|--------|----------------|
| **Personal wiki** (Obsidian) | Concepts, frameworks, digests — your long-term memory |
| **Agent skills** (Cursor) | When X happens, do Y — repeatable agent behavior |
| **Learning artifacts** | Digests, quizzes, flashcards, **roguelike runs** — faster human learning |

**You do not need to name topics upfront.** Drop a source; the agent discovers topics and proposes a topic map when useful.

---

## 2. Prerequisites

| Tool | Purpose |
|------|---------|
| **Cursor** | Agent runs Zhuomo skill (`/zhuomo` or natural language) |
| **Obsidian** | Read and review wiki (recommended) |
| **Git** (optional) | Version wiki and skill repos |
| **Spaced Repetition plugin** | Review recall cards — [Obsidian plugin](https://github.com/st3v3nmw/obsidian-spaced-repetition) |

Install the Zhuomo skill where Cursor discovers skills, e.g. symlink:

```bash
ln -sf /path/to/zhuomo ~/.cursor/skills/zhuomo
```

---

## 3. First-time setup

### Step 1: Bootstrap paths

In Cursor chat:

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, Obsidian vault ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen
```

The agent should create:

```
~/zhuomo-data/raw/
├── inbox/          # phone captures
├── web/
├── video/
├── books/
├── assets/
└── processed/

~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen/
├── AGENTS.md       # wiki schema for agents
└── wiki/
    ├── index.md
    ├── log.md
    ├── domain-map.md   # when you have 2+ domains
    ├── domains/
    ├── sources/
    ├── concepts/
    ├── synthesis/
    └── learn/
        ├── digests/
        ├── recall/
        ├── quizzes/
        ├── runs/
        └── applied/
```

### Step 2: Open Obsidian

Open the Obsidian vault folder **Dylan Chen** (iCloud); wiki lives under `wiki/`.

### Step 3: Install Spaced Repetition (recommended)

In Obsidian → Community plugins → **Spaced Repetition** (st3v3nmw).

Suggested settings:

- Include folder: `wiki/learn/recall/`
- Deck tags: `#flashcards/[domain]` matching your domain slugs

Details: [RETENTION.md](RETENTION.md).

### Step 4: Add AGENTS.md conventions

Ensure vault `AGENTS.md` includes raw path, wiki path, ingest/query/lint/revise/learn rules. Template in [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md#schema-agentsmd-section).

### Step 5: First ingest

Save one article or book chapter to `raw/`, then:

```
/zhuomo Ingest raw/web/my-first-article.md — discover topics, learn mode recap
```

Open Obsidian and browse new pages under `wiki/`.

---

## 4. Daily and weekly habits

### Light daily (5–10 min)

- Capture URLs or notes to `raw/inbox/` (phone or laptop)
- Read one digest in Obsidian
- Review due flashcards (Spaced Repetition)

### After reading a chapter (15–30 min)

```
/zhuomo I finished ch.3 of [book] — recap quiz + update [domain] framework
```

### Weekly ritual (~15 min)

```
/zhuomo Weekly review
```

Agent runs:

1. **Review** — SR cards + one explain-back
2. **Connect** — cross-domain link prompt
3. **Lint** — top issues → revise tasks
4. **Progress** — bump one gap on a study path
5. **Applied** — scan `wiki/learn/applied/` for wiki updates

You append to `wiki/log.md` via the agent.

---

## 5. Operations reference

| Operation | You say (examples) | You get |
|-----------|-------------------|---------|
| **Ingest** | `Ingest raw/books/ddia.epub ch.1` | Concept pages, source summary |
| **Learn** | `Learn mode: preview ch.2` / `Learn fable: [[concept]]` | Pretest, digest, recall; **fable** (Askell story → reveal) |
| **Run** | `Run: fuse networking + psychology, 5 floors` | Scenario, floors, debrief, loot |
| **Review** | `Review networking recall` | Session plan, explain-back |
| **Framework** | `Update my distributed-systems framework` | `framework.md` refresh |
| **Weekly** | `Weekly review` | Checklist + log entry |
| **Query** | `How does my wiki explain CAP?` | Cited answer; may file back |
| **Revise** | `Wiki says X but that's wrong` | Fixed pages + propagation |
| **Lint** | `Lint the networking domain` | Issue list |

**Archive only:** add `archive only` to skip learn/framework:

```
/zhuomo Ingest raw/paper.pdf — archive only
```

---

## 6. Prompt cookbook

### Bootstrap and maintenance

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, Obsidian vault ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen

/zhuomo Process everything in ~/zhuomo-data/raw/inbox/

/zhuomo Lint the whole wiki — top 10 issues

/zhuomo Weekly review
```

### Roguelike runs

```
/zhuomo Run: fuse networking + psychology — roguelike, 5 floors, medium

/zhuomo Run random — 2 domains from domain-map, easy, 3 floors

/zhuomo Run themed "incident response" — weakest domains from framework progress

/zhuomo Run rematch seed:2026-06-01-net-psych-7
```

### Ingest (no topic required)

```
/zhuomo Ingest raw/ddia.epub ch. 1 — discover topics, no lens from me.

/zhuomo Ingest this blog. I care about caching only; still list other topics at the end.

/zhuomo Here's a paper — topic map first, then ingest everything into wiki.
```

### Learn

```
/zhuomo Learn mode: preview raw/new-book.epub ch.1 before I read it.

/zhuomo I finished ch.3 — recap quiz + update my distributed-systems framework.

/zhuomo Explain event sourcing back to me; correct me using the wiki.

/zhuomo Learn fable: [[event-sourcing]] — don't name it until the end; then map story beats to the wiki.

/zhuomo Learn fable mode — pick the weakest pillar on my ACI overview.
```

### Skills

```
/zhuomo Extract a skill from [[concept-page]] — RED first.

/zhuomo Domain skill: network-expert — wiki backend wiki/domains/networking/
```

### Revise

```
/zhuomo Revise [[bgp]] — MED is lower preferred in my notes but wiki says higher wins locally. Source: [link].

/zhuomo Merge duplicate pages [[foo]] and [[foo-bar]].
```

---

## 7. Learning from sources

Zhuomo supports four **learn modes** (agent can suggest):

| Mode | When | Output |
|------|------|--------|
| **Preview** | Before reading | Topic map, pretest, links to framework |
| **Companion** | While reading | Per-chunk digest tied to pillars |
| **Recap** | After ingest | Quiz, recall cards, framework progress |
| **Connect** | Any time | Cross-domain relations |

### Artifacts (where to find them)

| Artifact | Path |
|----------|------|
| Study digest | `wiki/learn/digests/[source-slug].md` |
| Recall cards | `wiki/learn/recall/[domain]/` |
| Quizzes | `wiki/learn/quizzes/` |
| Applied journal | `wiki/learn/applied/` |
| Pretest | In digest `## Pretest` |

**Rules for you:**

- Digests should fit **one screen** — drill down via wikilinks
- Learning artifacts teach **you**; skills teach **agents**
- Default after ingest: digest + framework update (unless archive only)

Full detail: [LEARNING.md](LEARNING.md).

---

## 8. Building domain frameworks

### When to create a domain

- You have a sustained interest (networking, psychology, finance, …)
- Multiple sources map to the same pillar structure

### Start L0: domain map

File: `wiki/domain-map.md` — list domains, one-line description, link to each `framework.md`.

### Build L1: framework.md

Path: `wiki/domains/[slug]/framework.md`

Include:

1. North star (one sentence)
2. Pillars (wikilinked big ideas)
3. Mental model
4. Progress table (strength, sources, gaps)
5. Cross-domain links
6. Optional study path

### Progress strength

| Strength | Meaning |
|----------|---------|
| **learning** | Exposed, not yet teachable |
| **solid** | You can explain and apply — see mastery in [RETENTION.md](RETENTION.md) |

Ask the agent to update after each ingest touching that domain:

```
/zhuomo Update framework for domain networking after today's BGP ingest
```

Conceptual overview: [FRAMEWORK.md](FRAMEWORK.md#4-knowledge-framework-l0--l3).

---

## 9. Retention and review

### Flashcards

Zhuomo writes cards under `wiki/learn/recall/` with tags like `#flashcards/networking`.

**You review** in Obsidian: *Spaced Repetition: Review flashcards* (phone or laptop).

Example card shape:

```markdown
#flashcards/networking

What are typical BGP path attributes in evaluation order (simplified)?

?

1. Weight → 2. Local pref → …

→ [[concepts/bgp-path-selection]]
```

### Review operation

When you want agent help beyond the plugin:

```
/zhuomo Review — explain-back on weak pillars in networking framework
```

### Readwise pipeline

1. Export Readwise markdown on laptop
2. Save to `raw/inbox/readwise-2026-05.md`
3. `Process inbox — ingest highlights, recall cards for starred items only`

See [REFERENCE.md](REFERENCE.md#readwise--highlights-pipeline).

Full retention spec: [RETENTION.md](RETENTION.md).

---

## 10. Creating agent skills

### When to create a skill

Create a **technique skill** when:

- There is a clear **trigger** (symptom, situation)
- The move is **actionable** and **non-default** for the agent
- You want the agent to follow it under pressure

Do **not** create a skill for:

- Book plot or chapter summaries
- Facts that belong in wiki only
- Generic advice ("be careful", "think step by step")

### Workflow (TDD)

1. **Ingest to wiki first** — synthesis and contradictions stay in KB
2. **Extraction card** — trigger, core move, steps, anti-pattern, example, type
3. **Filter** — actionable AND non-default?
4. **RED** — verify baseline fails without skill
5. **GREEN** — minimal `SKILL.md`
6. **REFACTOR** — counters, edge cases, re-test
7. Update `SOURCES.md` and wiki links

```
/zhuomo Extract skill for condition-based waiting — RED then GREEN, link wiki [[flaky-tests]]
```

Requires agent skills: **writing-skills**, **write-a-skill** (Cursor superpowers).

### Skill types

| Type | Holds |
|------|--------|
| **Technique** | One workflow + trigger |
| **Domain** | Persona + WIKI-SCOPE (see next section) |

---

## 11. Domain skills (wiki-backed experts)

Use when you want an agent to **reason like an expert** in a field you have already built in the wiki (e.g. BGP, distributed systems).

**Facts stay in wiki.** Skill holds:

- `SKILL.md` — persona, workflow, anti-patterns (lean)
- `WIKI-SCOPE.md` — which pages to load at invoke time
- `SOURCES.md` — wiki paths + raw provenance

Example:

```
/zhuomo Domain skill: network-expert — wiki backend wiki/domains/networking/ + BGP concepts. WIKI-SCOPE manifest only; no fact dump in SKILL.md.
```

When facts change: **Revise wiki only** — redeploy skill only if workflow/discipline changed.

Full pattern: [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md).

---

## 12. Correcting and updating knowledge

### When to revise

- You spot an error
- New source contradicts old wiki claim
- Lint reports duplicate or stale pages
- Practice (applied journal) contradicts theory

### What to say

```
/zhuomo Revise [[page]] — [what was wrong], evidence: [source or reasoning], new claim: […]
```

Agent should:

1. Fill a **revision card** (see [REFERENCE.md](REFERENCE.md))
2. Edit, supersede, merge, or retract — **not** silent delete
3. **Propagate** to all pages and skills citing old claim
4. Append `wiki/log.md`: `revise | [[page]] | reason`

### Supersede pattern

Old page: `status: superseded` + link to canonical page.  
Git keeps history; `log.md` keeps intent.

---

## 13. Multi-device workflow

| Device | Do | Don't |
|--------|-----|--------|
| **iPhone** | Save to `raw/inbox/`; read wiki; SR review | Full EPUB ingest; paywalled fetch |
| **Laptop** | Ingest, learn, framework, revise, skills | Rely on phone for heavy processing |

### Sync suggestions

| Layer | Method |
|-------|--------|
| Wiki | Obsidian Sync, iCloud, or Git + Working Copy |
| Raw `inbox/` | iCloud Drive / Dropbox / Syncthing |
| Raw `books/` | Usually laptop-only |

### Inbox capture template (phone)

```markdown
---
url:
title:
captured: 2026-05-30
device: iphone
status: inbox
---

One line: why I saved this.
```

Laptop:

```
/zhuomo Process raw/inbox/ — ingest to wiki, move to processed/
```

Details: [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md#multi-device-sync-laptop--iphone).

---

## 14. Source types

| Source | Raw location | Notes |
|--------|--------------|-------|
| Web article | `raw/web/` | Clip or save markdown; URL alone is not enough |
| EPUB / PDF | `raw/books/` | Ingest by chapter for large books |
| Video | `raw/video/` | Transcript or notes |
| Readwise export | `raw/inbox/readwise-*.md` | Ingest to wiki; optional recall for ★ highlights |
| Phone note | `raw/inbox/` | Process on laptop |

EPUB, video, O'Reilly: see [REFERENCE.md](REFERENCE.md).

---

## 15. Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| Agent gives chat-only answers | Query not filed back | Ask to file answer to `wiki/synthesis/` |
| Duplicate concept pages | Skipped topic map / search | Lint + merge; search before ingest |
| Skill is a book summary | Skipped filter | Wiki for narrative; skill needs trigger |
| Wiki and skill disagree | No revise after correction | Revise wiki + update skill |
| Flashcards never reviewed | No SR plugin / habit | Install plugin; Weekly review |
| Phone can't find raw books | Books not synced | Keep `books/` laptop-only |
| Ingest twice same URL | No duplicate check | Agent checks `wiki/sources/` first |
| Overwhelming topic map | Large source | Ingest 1–2 clusters per session |
| Run questions not from my wiki | Agent skipped concept pages | Require wiki cites; see [RUN.md](RUN.md) |
| Story filed as wiki fact | Missing `fictional-scenario` tag | Revise if needed; runs go in `wiki/learn/runs/` only |
| Book ingest lost detail / no provenance | Pillar-only pass; no MD corpus | Run `scripts/epub-to-wiki-md.py`; deepen by chapter; add `## Evidence` per [REFERENCE.md](REFERENCE.md#epub-epub) |

---

## 16. Roguelike runs

**Run** turns your multi-domain wiki into a **roguelike learning game**: fictional scenario, escalating floors, wiki-grounded questions, debrief + loot.

| Piece | Meaning |
|-------|---------|
| **Scenario** | Made-up setting (bank outage, Mars colony, etc.) |
| **Floors** | Harder questions each floor; death = failed explain-back |
| **Fusion** | 2+ domains from `domain-map.md` combined in one story |
| **Loot** | New recall cards, synthesis stubs, framework progress |
| **Boss** | Final cross-domain tradeoff question |

**Rules:** fiction is allowed; **answers must cite your wiki**. Contested topics stay contested. If a run exposes a wiki error → **Revise**, don't patch via story.

### When to use

- After you have concept pages in 2+ domains
- Weekly ritual alternative to Connect (10 min)
- When quizzes feel too flat — you want **integration under pressure**

### Example

```
/zhuomo Run: fuse networking + psychology — 5 floors, medium
```

You play in chat; agent files `wiki/learn/runs/YYYY-MM-DD-seed.md` with grades and loot.

Full spec: [RUN.md](RUN.md).

---

## 17. FAQ

**Do I have to name the topic?**  
No. Optional lens only. Agent discovers from TOC/headings.

**Wiki only or skill only?**  
Say `wiki only` or `one skill` as your goal. Default is wiki + learn + framework; skills when actionable.

**One vault for unrelated subjects?**  
Yes. Use `domain-map.md` and `wiki/domains/*/`.

**Is Obsidian required?**  
No, but recommended for reading, graph, and spaced repetition.

**Where does the agent write?**  
Only under `wiki/`. Raw is read-only for the agent.

**Can I use RAG instead of a wiki?**  
Zhuomo assumes compile-once wiki. RAG-only loses revise, links, and frameworks.

**How is this different from Readwise → Obsidian sync?**  
Readwise sync is another raw snapshot until **ingest** compiles concepts and frameworks.

---

## Document index

| File | Use when |
|------|----------|
| [USER-GUIDE.md](USER-GUIDE.md) | This guide — setup and daily use |
| [FRAMEWORK.md](FRAMEWORK.md) | Understanding the system model |
| [RUN.md](RUN.md) | Roguelike multi-domain runs |
| [SKILL.md](SKILL.md) | What the agent reads first |
| [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md) | Wiki layout and operations |
| [LEARNING.md](LEARNING.md) | Learn modes and framework template |
| [RETENTION.md](RETENTION.md) | Flashcards and weekly ritual |
| [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md) | Domain expert skills |
| [REFERENCE.md](REFERENCE.md) | EPUB, video, revision cards |
