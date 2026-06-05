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
| **Framework** | After ingest or on request | `domain-map`, per-domain `framework.md`, progress |
| **Weekly** | ~15 min ritual | Review + Connect/Run + Lint + progress → `log.md` |
| **Query** | Question | Answer (+ file back to wiki) |
| **Revise** | Wrong, stale, duplicate | Corrected pages/skills + log |
| **Lint** | Periodic health | Issues → often Revise |

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

## Learn & framework (for you, not agents)

| Goal | Ask for |
|------|---------|
| Learn faster | **Learn** — preview, digest, quiz, explain-back |
| Cross-domain under pressure | **Run** — roguelike scenario fused from 2+ domains — [RUN.md](RUN.md) |
| See the big picture | **Framework** — pillars, mental model, progress table |
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
- [ ] 2c. Framework — update domain framework + epistemic/progress
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
| Fix only in chat | Revise wiki/skill + log.md |
| New source contradicts old | Revise affected pages, don't append both as true |
| Duplicate concept pages | Merge on lint/revise; one canonical page |
| One topic per resource assumed | Multi-topic normal — topic map first, one concept page each |
| User must name topic upfront | Optional — agent infers; user topic = priority lens only |
| Summary dump, no framework | Digest + link to pillars; update framework.md |
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
