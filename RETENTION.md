# Retention & Review (Zhuomo + Obsidian)

Human memory needs **scheduled retrieval** and **real-world use**. This file defines Review, Weekly, epistemic tags, applied journal, and Obsidian SR integration.

## Obsidian SR plugin

**Use: [Spaced Repetition](https://github.com/st3v3nmw/obsidian-spaced-repetition)** (st3v3nmw) — `#flashcards` decks, `Question::Answer` / multiline `?` syntax, mobile-friendly, largest community.

Plugin owns scheduling — zhuomo writes card **content** only.

**Optional later:** [FSRS](https://obsidian.md/plugins?id=fsrs) plugin if you migrate algorithms; card paths stay the same.

### Plugin settings (suggested)

- **Folders:** include `wiki/learn/recall/` (or tag-based decks only)
- **Deck tags:** `#flashcards/networking`, `#flashcards/psychology` — match domain slugs
- **Multiline:** enable `multilineCardEndMarker` (e.g. `---`) if answers need blank lines

### Recall card path

`wiki/learn/recall/[domain]/[concept-slug].md`

One file per concept cluster; multiple cards per file OK.

### Card format (zhuomo output)

Tag the note as a sub-deck, then use multiline or single-line cards:

```markdown
---
domain: networking
concept: "[[bgp]]"
epistemic: established
tags: [recall, networking]
---

#flashcards/networking

# Recall — BGP

What are typical BGP path attributes in evaluation order (simplified)?

?

1. Weight → 2. Local pref → 3. Locally originated → 4. AS path length →
5. Origin → 6. MED → 7. eBGP over iBGP → 8. IGP metric → 9. Router ID

→ [[concepts/bgp-path-selection]]

---

BGP local preference: higher or lower preferred?

::Higher is preferred (among routes from same AS).
```

Single-line alternative: `Question::Answer` on one line.

After ingest, open Obsidian → **Spaced Repetition: Review flashcards** → phone or laptop.

### Readwise → raw/inbox

For Kindle, O'Reilly, web highlights:

1. Readwise export (markdown) → `~/zhuomo-data/raw/inbox/readwise-YYYY-MM.md`
2. Laptop: `/zhuomo Process inbox — ingest highlights to wiki, generate recall cards for marked items`

See [REFERENCE.md](REFERENCE.md#readwise--highlights-pipeline).

---

## Review operation

**When:** User asks to review; Spaced Repetition shows due cards; or Weekly ritual step 1.

**Agent does:**

1. User runs **Spaced Repetition** review UI in Obsidian (agent lists `wiki/learn/recall/` paths if helping plan a session)
2. Run **explain-it-back** on 1–3 weak pillars from `framework.md`
3. Update `last_reviewed` on concept frontmatter if manual tracking needed

**Output:** Optional session note in `wiki/learn/reviews/YYYY-MM-DD.md` — what was hard, links to revise.

---

## Weekly operation

**When:** User asks `/zhuomo Weekly review` or weekly calendar habit (~15 min).

```
- [ ] 1. Review — due SR cards (Obsidian Spaced Repetition) + one explain-back
- [ ] 2. Connect — one cross-domain prompt (LEARNING.md Connect mode) **or Run** — one short roguelike fuse ([RUN.md](RUN.md))
- [ ] 3. Lint — top 3 stale/contradicted/duplicate issues → Revise tasks
- [ ] 4. Progress — bump one gap on a domain study path
- [ ] 5. Applied — scan wiki/learn/applied/ since last week; any wiki revise needed?
```

Append `wiki/log.md`: `## [YYYY-MM-DD] weekly | domains touched`.

---

## Epistemic status (concept pages)

Add to concept frontmatter:

```yaml
---
epistemic: tentative    # tentative | established | contested | deprecated
sources: 2
applied_count: 0
prereqs: ["[[consistency]]"]
enables: ["[[multi-leader]]"]
---
```

| Value | Meaning | Domain skill behavior |
|-------|---------|------------------------|
| `tentative` | One source or untested | Mention uncertainty |
| `established` | Multi-source +/or applied | Default authority |
| `contested` | Sources disagree | Present tension |
| `deprecated` | Superseded | Link to replacement; don't assert |

Promote `tentative` → `established` when mastery criteria met (below).

---

## Mastery criteria (framework Strength)

In `framework.md` Progress table, use rules:

| Strength | Criteria |
|----------|----------|
| **learning** | Ingested; digest exists |
| **solid** | Explain-back pass + 2+ sources OR 1 source + applied entry |
| **gap** | Listed in study path; not yet ingested |

Agent updates Strength on Recap / Weekly / applied journal.

---

## Applied journal

Path: `wiki/learn/applied/YYYY-MM-DD-slug.md`

```markdown
# Applied — BGP communities at work

- **Concepts:** [[bgp-communities]], [[route-maps]]
- **Context:** Production prefix leak mitigation
- **Decision:** …
- **Outcome:** …
- **Wiki revise?** no / yes → [[log]]
```

Ingest of experience: bump `applied_count` on concepts; may promote epistemic → `established`.

---

## Preview pretest (before read)

Extend **Preview** mode in Learn:

1. Agent asks 3 questions from topic map + existing wiki (user may fail)
2. User reads raw/chapter
3. **Recap** compares pre-answers to digest; file gaps in framework

Log in digest: `## Pretest` / `## After read`.

---

## Progressive summarization layers

| Layer | Location | Owner |
|-------|----------|-------|
| L0 | `raw/` snapshot | Immutable |
| L1 | `wiki/sources/` | Agent ingest |
| L2 | `wiki/learn/digests/` bold claims | Learn |
| L3 | `framework.md` pillar one-liners | Framework |
| L4 | `wiki/learn/recall/` one-line cards | Learn + SR |

Don't skip layers — deep books need L2 before L4.

---

## Prerequisite graph

On concept pages:

```markdown
## Prerequisites
- [[consistency]]
- [[replication]]

## Enables
- [[multi-leader]]
```

Agent warns on ingest order; framework study path respects prereqs.

---

## Example prompts

```
/zhuomo Recap ch.5 — pretest first, then digest + 5 recall cards for FSRS.

/zhuomo Weekly review — networking + psychology domains.

/zhuomo Applied journal: used [[bgp-communities]] in incident today.

/zhuomo Promote [[bgp]] to established — explain-back passed, 2 sources.
```
