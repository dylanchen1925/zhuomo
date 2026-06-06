---
name: zhuomo
description: Use when turning books, EPUBs, blogs, videos, or notes into a personal wiki or agent skills; when learning from resources quickly, building domain frameworks, running roguelike multi-domain learning scenarios, or mapping progress across varied domains; when discovering topics or correcting existing wiki/skills.
disable-model-invocation: true
---

# 琢磨 (Zhuomo)

**琢磨** — to polish, refine, and chew over raw material until it becomes clear and usable. Turn sources into a **personal wiki** and **agent skills** — help **you learn faster**, **build frameworks** of what you know, and keep knowledge correct across **many domains**.

## Overview

**Skills are proven techniques with triggers — not book summaries.**

Give future agents: *when* to act, *what* to do, *how* to decide, *what mistakes* to avoid. Drop narrative, anecdotes, repetition.

**Knowledge is never write-once.** Ingest adds; **revise** corrects, updates, merges, and supersedes. See [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md#revise-correct--update) and [REFERENCE.md](REFERENCE.md#correcting--updating-existing-knowledge).

**Two compounding outputs:**

| Output | Holds | Agent use |
|--------|-------|-----------|
| **Wiki** | Synthesis, entities, links, contradictions | Query, browse, **domain skill backend** |
| **Skill** | Triggers + workflows (+ WIKI-SCOPE for domain skills) | Auto-invoke under symptoms |

**REQUIRED:** **superpowers:writing-skills**, **write-a-skill**  
**User:** [USER-GUIDE.md](USER-GUIDE.md) · **Framework:** [FRAMEWORK.md](FRAMEWORK.md)  
**Wiki:** [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md) · **Learn:** [LEARNING.md](LEARNING.md) · **Run:** [RUN.md](RUN.md) · **Retention:** [RETENTION.md](RETENTION.md) · **Domain skills:** [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md)

## When to Use / NOT

**Use:** sources → wiki and/or skill; **learn** from resources (digests, quizzes, recall); **run** roguelike multi-domain scenarios; **build/update domain frameworks**; multi-domain vault; correct or update existing pages.

**Don't:** one-off answers without filing; silent overwrite; delete history instead of supersede/archive; wall-of-text summaries instead of linked learning artifacts.

## Nine operations

| Op | When | Output |
|----|------|--------|
| **Ingest** | New source | Wiki pages (multi-topic, multi-domain) |
| **Learn** | User studying | Digests, pretest, recall cards → `wiki/learn/` |
| **Run** | Multi-domain practice | Fictional scenario + floors + debrief → `wiki/learn/runs/` — [RUN.md](RUN.md) |
| **Review** | Due cards / study session | SR review + explain-back → [RETENTION.md](RETENTION.md) |
| **Framework** | After ingest or on request | `domain-map`, per-domain `overview.md` (pillars + progress), optional `guide.md` |
| **Weekly** | ~15 min ritual | Review + Connect/Run + Lint + progress → `log.md` |
| **Query** | Question | **search** (page list) or **think** (synthesis + gaps + file back) |
| **Revise** | Wrong, stale, duplicate | Corrected pages/skills + log |
| **Lint** | Periodic health | Doctor-lite checklist → issues → often Revise |

Details: [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md), [LEARNING.md](LEARNING.md), [RUN.md](RUN.md), [RETENTION.md](RETENTION.md)

## Wiki vs Skill

| Put in **wiki** | **Zhuomo** into skill |
|-------------------------|------------------------|
| Entity pages, themes, synthesis | Named technique with clear trigger |
| Cross-source contradictions | Iron law / discipline rule |
| Research thesis evolving over weeks | "When X symptom, do Y" |
| Comparison tables, cited answers | Agent must comply under pressure |

Often: **topic map → ingest → wiki first → zhuomo extraction card → skill** when actionable + non-default.

## Domain skills (wiki as backend)

**Technique skill** = one workflow. **Domain skill** = expert persona + **WIKI-SCOPE.md** manifest — agent loads your wiki (e.g. BGP concepts) at invoke time; facts stay in wiki, not in SKILL.md.

Example: `network-expert` + `wiki/domains/networking/` + `[[concepts/bgp]]`. Full pattern: [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md).

```
/zhuomo Domain skill: network-expert — wiki backend wiki/domains/networking/
```

## Topics (optional from you)

**You do not need to name the topic.** Provide a source; the agent reads structure (TOC, headings, skim) and **discovers topics** — often several per book, paper, or video.

| You provide | Agent does |
|-------------|------------|
| Nothing | Infer all major topics; present topic map; proceed unless you narrow |
| Topic / lens ("focus on ch. 5–7") | Prioritize those; still note other topics for later |
| Goal ("wiki only" / "one skill") | Filter extraction toward that output |

One resource → **one source summary** + **many concept pages** across **one or more domains**. Details: [REFERENCE.md](REFERENCE.md#topic-discovery-multi-topic-resources), [LEARNING.md](LEARNING.md).

## Wiki page layout (per domain)

**Two pages per domain — do not create `framework.md` or `mega-overview.md`.**

| Page | Path | Holds |
|------|------|-------|
| **Vault hub** | `wiki/overview.md` | Domain table + ingest rules only — **no domain prose** |
| **Domain entry** | `wiki/domains/<slug>/overview.md` | Why learn, architect lens, pillars, progress, glossary, study order, gaps |
| **Domain guide** (optional) | `wiki/domains/<slug>/guide.md` | One-page technical digest (merge of concept pages) |
| **Concepts** | `wiki/concepts/*.md` | Full depth + `## Evidence` when deepened |

New domain ingest: add a row to vault `overview.md` + `domain-map.md`; create `domains/<slug>/overview.md`. Add `guide.md` only when user wants one-scroll reference depth.

Lite mode default: [SIMPLE.md](SIMPLE.md). Vault `AGENTS.md` must mirror this block.

**Concept pages (compiled truth):** body = current trusted claims; optional `## Changelog` or frontmatter records when ingest/revise changed what (never silent overwrite).

## Query — brain-first, search vs think

**Brain-first (always):** read wiki before web or raw EPUB.

1. `wiki/overview.md` → `domain-map.md` → `domains/<domain>/overview.md` / `guide.md`
2. `wiki/index.md` → relevant `concepts/` + `sources/`
3. Only if insufficient: raw `~/zhuomo-data/raw/` or external search

| Mode | User says | Agent returns |
|------|-----------|---------------|
| **search** | `Query search: …` or "list wiki pages about …" | Ranked page list + one-line why each matters — user reads pages |
| **think** (default) | `Query: …` or `Query think: …` | Synthesized answer + citations + **## Gaps** |

**Think output template (required sections):**

```markdown
## Answer
…synthesis with [[wikilinks]] and Evidence anchors where deepened…

## Sources
- [[concept-or-page]] — what you used

## Gaps
| Gap | Why it matters | Suggested next step |
|-----|----------------|---------------------|
| … | stub / no Evidence / stale source / contradiction | deepen X / Revise Y / new source |
```

**Network/IT:** lead Answer with business constraint → design lever → technical object (see domain `overview` architect lens).

**File back:** comparisons, cross-concept synthesis, or durable Q&A → `wiki/synthesis/` or strengthen an existing concept; append `log.md` if substantial.

## Lint — doctor-lite

Run on request, after large ingest, or as part of **Weekly**.

| Check | Action if failed |
|-------|------------------|
| Broken `[[wikilinks]]` | Fix path or create stub concept linked from domain `overview` pillar |
| Orphan concept pages (no inbound links) | Link from `overview`, `guide`, or related concepts |
| Concept mentioned in text but no page | Create stub or merge duplicate |
| `overview` progress ≠ concept `status` / depth | Revise overview or concept |
| Deepened book concept missing `## Evidence` | Add Evidence or downgrade progress note |
| Contradictions between pages | Revise; supersede stale claim |
| Stale source (newer guide/version exists) | Note in Gaps; flag in `overview` |
| Duplicate concept pages same topic | Merge; one canonical page |
| Domain `overview` gaps list outdated | Refresh after ingest |

Append `## [date] lint | …` to `wiki/log.md`. Turn each row into **Revise** or **deepen** follow-up.

**Auto-stub (on ingest/lint):** when a pillar or guide links `[[aci-foo]]` and page missing, create minimal stub with `domain:` frontmatter and link back to pillar — do not leave dangling wikilinks.

## Weekly — mini dream cycle

~15 min ritual ([RETENTION.md](RETENTION.md)): **Review** due cards → **Lint** (doctor-lite) → merge duplicates → bump `overview` progress → optional one `wiki/synthesis/` cross-concept note → `log.md`.

## Learn & framework (for you, not agents)

| Goal | Ask for |
|------|---------|
| Learn faster | **Learn** — preview, digest, quiz, explain-back |
| Cross-domain under pressure | **Run** — roguelike scenario fused from 2+ domains — [RUN.md](RUN.md) |
| See the big picture | **Framework** — update `domains/<slug>/overview.md` (pillars, progress) |
| Many unrelated subjects | **Multi-domain** — `wiki/domain-map.md` + `wiki/domains/*/` |

Default after chapter ingest (unless you say **archive only**): digest + update domain framework. Full guide: [LEARNING.md](LEARNING.md).

## Workflow Checklist

**New source:**
```
- [ ] 0. Wiki setup — bootstrap if needed; multi-domain → domain-map (LEARNING.md)
- [ ] 1. Intake — source; discover topics; assign domain(s)
- [ ] 1b. EPUB/PDF — convert full text to wiki/sources/[slug]/md/; Evidence links on every concept page (REFERENCE.md)
- [ ] 2. Ingest — wiki pages; flag contradictions
- [ ] 2b. Learn — pretest + digest + recall for Spaced Repetition (skip if "archive only")
- [ ] 2c. Framework — update `domains/<slug>/overview.md` (pillars, progress, gaps)
- [ ] 3–10. Extract → skill pipeline if actionable
```

**Correct or update existing knowledge:**
```
- [ ] 1. Locate — index.md, backlinks, related skills
- [ ] 2. Revision card — what was wrong, evidence, new claim (REFERENCE.md)
- [ ] 3. Propagate — fix all pages that cite the old claim
- [ ] 4. Wiki — edit in place or supersede; never silent delete
- [ ] 5. Skill — merge correction; re-run RED if discipline changed
- [ ] 6. Log — append wiki/log.md: revise | target | reason
```

Full ingest checklist:

```
- [ ] 3. Extract — extraction card per candidate idea
- [ ] 4. Filter — actionable AND non-default
- [ ] 5. Classify — technique / pattern / reference / discipline
- [ ] 6. Decide — new vs enhance vs split; run Revise if source contradicts wiki
- [ ] 7. RED — baseline WITHOUT draft skill
- [ ] 8. GREEN — minimal SKILL.md
- [ ] 9. REFACTOR — counters; re-test
- [ ] 10. Update SOURCES.md (+ wiki log.md)
```

### Extraction card

| Field | Capture |
|-------|---------|
| Trigger | Situation/symptoms (not chapter title) |
| Core move | One non-obvious action |
| Steps | Workflow or decision tree |
| Anti-pattern | Common failure |
| Example | One adapted before/after |
| Type | technique / pattern / reference / discipline |

### Validate (TDD)

**No SKILL.md until RED completes.** See **superpowers:writing-skills**.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Chapter summary as skill | Wiki for synthesis; skill for triggers only |
| RAG-only (no wiki) | Ingest compiles once; wiki stays current |
| Wiki without schema | AGENTS.md/CLAUDE.md defines ingest/query/lint |
| Skip RED | Test skill first |
| Query answers lost in chat | File good answers back to wiki |
| Web search before wiki | Brain-first: overview → guide → concepts |
| Query without Gaps section | Think mode must end with ## Gaps |
| Lint only when user complains | Run doctor-lite after big ingest + Weekly |
| Fix only in chat | Revise wiki/skill + log.md |
| New source contradicts old | Revise affected pages, don't append both as true |
| Duplicate concept pages | Merge on lint/revise; one canonical page |
| One topic per resource assumed | Multi-topic normal — topic map first, one concept page each |
| User must name topic upfront | Optional — agent infers; user topic = priority lens only |
| Summary dump, no framework | Digest + link to pillars; update `domains/<slug>/overview.md` |
| `framework.md` / `mega-overview.md` | Use `overview.md` + optional `guide.md` only — see Wiki page layout |
| Single-domain assumed | Use domain-map + wiki/domains/* for varied subjects |
| BGP facts pasted into skill | Domain skill + WIKI-SCOPE; Revise wiki only when facts change |
| Recall cards never reviewed | Obsidian Spaced Repetition + Weekly Review — [RETENTION.md](RETENTION.md) |
| Scenario fiction filed as facts | Run artifacts use `type: fictional-scenario`; Revise only for wiki errors — [RUN.md](RUN.md) |
| Cross-domain only in chat | **Run** — fuse domains, file debrief to `wiki/learn/runs/` |

## Deployment

- [ ] Skill: name, description, SOURCES.md, RED/GREEN/REFACTOR
- [ ] Raw: local path (e.g. `~/zhuomo-data/raw/`), `inbox/` for phone captures, immutable snapshots
- [ ] Wiki: Obsidian vault — `wiki/`, index.md, log.md, schema in AGENTS.md; sync to phone for read
- [ ] Retention: Spaced Repetition plugin on `wiki/learn/recall/` (`#flashcards/domain`); optional Readwise → inbox

Details: [REFERENCE.md](REFERENCE.md), [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md), [LEARNING.md](LEARNING.md), [RETENTION.md](RETENTION.md), [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md)
