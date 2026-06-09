# Learning & Frameworks (Zhuomo)

Help the user **learn faster** from resources and **build a mental framework** of what they know — across **many domains** in one wiki.

## Learn operation

Run during or right after ingest. Goal: understanding and retention, not just storage.

### Learning outputs (file to wiki)

| Artifact | Path | Purpose |
|----------|------|---------|
| **Study digest** | `wiki/learn/digests/[source-slug].md` | 5-min re-read: core ideas, analogies, "so what" |
| **Preread questions** | same or separate | Questions to read *for* (before deep read) |
| **Recall cards** | `wiki/learn/recall/[domain]/` | Q → A; `#flashcards/domain` for **Spaced Repetition** |
| **Explain-it-back** | chat + optional wiki | Feynman prompt; agent checks against source + wiki |
| **Concept fable** | `wiki/learn/fables/[domain]/` | Narrative that embodies a concept; reveal at end — Askell fable mode |
| **Mini quiz** | digest or `wiki/learn/quizzes/` | 5–10 questions + answers; user self-tests |
| **Gap list** | domain `framework.md` | What this source didn't cover; what to read next |
| **Applied journal** | `wiki/learn/applied/` | Real-world use of concepts — see [RETENTION.md](RETENTION.md) |
| **Pretest** | digest `## Pretest` section | Questions *before* read — testing effect |

**Retention loop (Review, Weekly, epistemic tags, mastery):** [RETENTION.md](RETENTION.md)

### Learn modes (user picks or agent suggests)

| Mode | When | What agent does |
|------|------|-----------------|
| **Preview** | Before reading | Topic map + **pretest questions** + link to existing framework |
| **Companion** | While reading (chapter by chapter) | Digest per chunk + tie to framework pillars |
| **Recap** | After ingest | Quiz + recall cards + update framework progress |
| **Connect** | Any time | "How does this relate to [[other concept]] in other domain?" |
| **Fable** | Hard or abstract concept; before/after read | Story embodies concept without naming it; reveal + map beats → terms — see below |
| **Run** | Multi-domain integration | Fictional scenario + floors + debrief — [RUN.md](RUN.md) |

### Fable mode (Amanda Askell)

**Why:** Definitions are easy to nod at and forget. A fable lets you *feel* the mechanism first; naming it afterward locks intuition. Technique from Anthropic researcher **Amanda Askell** — indirect narrative, reveal near the end, then explicit articulation.

**When:** Abstract jargon (CAP, Nash equilibrium, contract model); pillar still `learning` on domain `overview`; user says "I don't get [[concept]]"; optional **Preview** hook before reading or **Recap** after ingest.

**Agent does:**

1. Read target `[[concept]]` + source/wiki — fable must match trusted claims (no fiction-as-fact).
2. Write a short fable (≈300–800 words) that **embodies** the concept without naming it; reader should guess only near the end.
3. **Reveal** — name the concept in one clear sentence.
4. **Explanation** — map 3–6 story beats → technical points; wikilink to concept page.
5. Optional: 1–2 recall hooks (`Question::Answer`) tying fable imagery to terms.
6. File to `wiki/learn/fables/[domain]/[concept-slug].md`; link from concept page `## Learn` or digest; append `log.md` if first fable for domain.

**Output template:**

```markdown
---
domain: networking
concept: "[[bgp-path-selection]]"
technique: askell-fable
tags: [learn, fable]
---

# Fable — BGP path selection

## Story
…narrative; do not name BGP or path attributes until the reveal…

## Reveal
The concept is **BGP path selection** (simplified attribute order).

## Explanation
| Story beat | Technical point |
|------------|-----------------|
| … | Weight → local pref → … |

→ [[concepts/bgp-path-selection]]

## Recall hook (optional)
#flashcards/networking
What did the three merchants argue about first?::…
```

**Prompt seeds (user or agent):**

```
Learn fable: [[aci-contract]] — village metaphor, reveal at end.

Learn fable mode for ch.5 topics I keep missing — pick weakest pillar from overview.

I want to understand [[event-sourcing]]. Write a fable that embodies it completely without naming it until the end; then explain and map story beats to the wiki.
```

**Not a substitute for:** Evidence on concept pages, recall cards for lists/procedures, or **Run** (multi-domain fiction quiz). **Run** tests wiki under pressure; **Fable** builds single-concept intuition.

### Rules

- **Short beats long** — digest ≤ 1 screen; expand via links to concept pages.
- **Link everything** — every learning artifact wikilinks to `wiki/concepts/` or domain concepts.
- **Use what they already know** — compare new material to existing wiki pages in same or other domains.
- **No skill substitute** — learning artifacts teach *you*; skills teach *agents*.

### Example prompts

```
/zhuomo Learn mode: preview raw/new-book.epub ch.1 before I read it.

/zhuomo I finished ch.3 — recap quiz + update my distributed-systems framework.

/zhuomo Explain event sourcing back to me; correct me using the wiki.

/zhuomo Learn fable: [[event-sourcing]] — story first, name it at the end.

/zhuomo Run: fuse distributed-systems + finance — 3 floors, easy
```

---

## Framework operation

A **framework** is the user's evolving map of a domain — pillars, progress, gaps, mental model — not a book summary.

### Framework page template

Path: `wiki/domains/[domain-slug]/framework.md`

```markdown
# Framework — [Domain display name]

One-sentence north star: what this domain is *for* in your life/work.

## Pillars (big ideas)

1. **[[pillar-a]]** — one line
2. **[[pillar-b]]** — one line
3. …

## Mental model

[Diagram, analogy, or 3–5 bullet "how the pieces fit"]

## Progress

| Pillar / topic | Strength | Sources ingested | Gaps |
|----------------|----------|------------------|------|
| Replication | solid | DDIA ch.5, paper X | multi-leader edge cases |
| … | learning | ch.1 only | … |

Strength rules: **learning** → **solid** — see [RETENTION.md](RETENTION.md#mastery-criteria-framework-strength).

Concept pages use `epistemic: tentative | established | contested | deprecated` in frontmatter.

## Cross-domain links

- Related to [[domains/psychology/habit-formation]] via feedback loops
- Related to [[domains/finance/risk]] via tail events

## Study path (optional)

Suggested order for remaining gaps → links to raw/ or external.
```

Rebuild framework when: new ingest touches domain; user asks; lint finds orphan concepts in domain.

### Framework levels

| Level | Content |
|-------|---------|
| **L0** | `wiki/domain-map.md` — all domains at a glance |
| **L1** | `wiki/domains/*/framework.md` — pillars + mental model per domain |
| **L2** | Concept pages — detailed nodes |
| **L3** | Source pages — evidence trail |

User climbs L0 → L3 as needed; learning digests sit between L2 and reading raw.

---

## Multi-domain wiki

**One vault, many domains.** Domains are independent; concepts may appear in more than one.

### Directory layout (multi-domain)

```
wiki/
├── domain-map.md              # required when 2+ domains
├── domains/
│   ├── distributed-systems/
│   │   ├── framework.md
│   │   └── index.md           # pages in this domain
│   ├── psychology/
│   │   ├── framework.md
│   │   └── index.md
│   └── finance/
│       └── framework.md
├── concepts/                  # flat OK — use frontmatter domain:
├── sources/
├── synthesis/                 # cross-domain synthesis lives here
├── learn/
│   ├── digests/
│   ├── fables/                  # Askell narrative → reveal → beat map
│   ├── recall/                # Obsidian FSRS targets this folder
│   ├── quizzes/
│   ├── runs/                  # roguelike multi-domain sessions
│   ├── applied/
│   └── reviews/               # optional session notes
└── index.md                   # global catalog OR pointer to domain-map
```

### domain-map.md template

```markdown
# Domain map

| Domain | Framework | Topics (count) | Last updated |
|--------|-----------|----------------|--------------|
| [[domains/distributed-systems/framework\|Distributed systems]] | 5 pillars | 42 | 2026-05-30 |
| [[domains/psychology/framework\|Psychology]] | 3 pillars | 18 | 2026-05-28 |
```

### Assigning domain on ingest

1. **Auto-detect** from source (TOC, title, topic map).
2. **Ask** only if source clearly spans domains with no primary home.
3. Tag concept pages:

```yaml
---
domain: distributed-systems
domains: [distributed-systems, finance]   # when cross-cutting
---
```

4. **Cross-domain concept** — one canonical concept page; link from each domain's framework under "Cross-domain links". Avoid duplicate pages per domain unless definitions genuinely differ.

### Cross-domain synthesis

Put in `wiki/synthesis/` when user has ingested across domains:

- "How CAP theorem shows up in product tradeoffs"
- "Habit loops ↔ feedback control (psychology ↔ systems)"

---

## Integrated workflow (ingest + learn + framework)

```
Topic map → assign domain(s)
    → Ingest (wiki pages)
    → Learn: pretest → digest → recall cards (Spaced Repetition)
    → Update domain framework + domain-map + epistemic tags
    → Extract technique skills OR domain skill (WIKI-SCOPE) if requested
```

Progressive layers L0 (raw) → L4 (recall): [RETENTION.md](RETENTION.md#progressive-summarization-layers).

Domain skills (wiki backend): [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md).

After every chapter ingest (default when user is learning, not just archiving):

- [ ] Digest in `wiki/learn/digests/` (include Pretest section if Preview ran)
- [ ] Bump progress + epistemic tags in `framework.md` / concept pages
- [ ] Add 3–7 recall cards in `wiki/learn/recall/` (`#flashcards/[domain]`) for Spaced Repetition

User says **"archive only"** to skip learn artifacts.

---

## Example: first domain + second domain

**First book (creates domain):**
```
/zhuomo Ingest DDIA ch.1–2. Create domain distributed-systems with framework.
Learn: preview + recap quiz.
```

**Unrelated book (new domain):**
```
/zhuomo Ingest raw/atomic-habits.epub. New domain psychology.
Update domain-map. Connect to existing domains only if real overlap.
```

**Cross-domain later:**
```
/zhuomo Synthesis page: feedback loops in systems vs habit psychology.
```
