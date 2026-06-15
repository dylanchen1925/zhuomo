# Learning & Frameworks (Zhuomo)

Help the user **learn faster** from resources and **build a mental framework** of what they know — across **many domains** in one wiki.

**Review loop:** [REVIEW.md](REVIEW.md) — per-concept `## Explain-back`, not flashcards.

## Learn operation

Run during or right after ingest. Goal: understanding and retention, not just storage.

### Learning outputs (file to wiki)

| Artifact | Path | Purpose |
|----------|------|---------|
| **Study digest** | `wiki/learn/digests/[source-slug].md` | 5-min re-read: core ideas, analogies, "so what" |
| **Preread questions** | same or separate | Questions to read *for* (before deep read) |
| **Explain-back prompts** | `wiki/concepts/*.md` `## Explain-back` | Per-concept teach-back questions |
| **Explain-back session** | chat + `wiki/learn/reviews/` | Agent scores rubric — [REVIEW.md](REVIEW.md) |
| **Concept fable** | `wiki/learn/fables/[domain]/` | Narrative that embodies a concept — Askell fable mode |
| **Mini quiz** | digest | 5–10 questions + answers; user self-tests |
| **Gap list** | domain `overview.md` | What this source didn't cover; what to read next |
| **Applied journal** | `wiki/learn/applied/` | Optional real-world use — [RETENTION.md](RETENTION.md) |
| **Pretest** | digest `## Pretest` section | Questions *before* read |

### Learn modes (user picks or agent suggests)

| Mode | When | What agent does |
|------|------|-----------------|
| **Preview** | Before reading | Topic map + **pretest questions** + link to domain `overview` |
| **Companion** | While reading (chapter by chapter) | Digest per chunk + tie to overview pillars |
| **Recap** | After ingest | Quiz + sync overview; ensure `## Explain-back` on concepts |
| **Connect** | Any time | "How does this relate to [[other concept]] in other domain?" |
| **Fable** | Hard or abstract concept | Story embodies concept without naming it — see below |

### Fable mode (Amanda Askell)

**When:** Abstract jargon; pillar still `learning`; user says "I don't get [[concept]]".

**Agent does:**

1. Read target `[[concept]]` + source/wiki — fable must match trusted claims.
2. Write a short fable (≈300–800 words) without naming the concept until the reveal.
3. **Reveal** + **Explanation** table mapping beats → technical points.
4. File to `wiki/learn/fables/[domain]/[concept-slug].md`; link from concept or digest.

**Not a substitute for:** Evidence, `## Explain-back`, or applied journal.

### Rules

- **Short beats long** — digest ≤ 1 screen; expand via links to concept pages.
- **Link everything** — every learning artifact wikilinks to `wiki/concepts/`.
- **No skill substitute** — learning artifacts teach *you*; skills teach *agents*.

### Example prompts

```
/zhuomo Learn mode: preview raw/new-book.epub ch.1 before I read it.

/zhuomo I finished ch.3 — recap quiz + update my distributed-systems overview.

Explain-back [[aci-border-leaf-l3out]]

/zhuomo Learn fable: [[event-sourcing]] — story first, name it at the end.
```

---

## Framework operation

A **framework** is the user's evolving map of a domain — pillars, progress, gaps — in **`domains/<slug>/overview.md`**. Optional **`guide.md`** = one-page technical digest.

### Domain overview template

See [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md) and existing `domains/*/overview.md`.

Progress table columns: **掌握度** · **Review** · **Explain-back** (sync from concept frontmatter on Weekly).

---

## Wiki learn folder layout

```
wiki/learn/
├── digests/
├── fables/
├── reviews/       # optional session logs
└── applied/       # optional; not required
```

Progressive layers: [RETENTION.md](RETENTION.md#progressive-summarization-layers).

### After ingest checklist (agent)

- [ ] Concept pages: `## Evidence` + `## Explain-back`
- [ ] Frontmatter: `mastery`, `explain_back`, `wiki_revised` on deepen/revise
- [ ] Digest under `wiki/learn/digests/` when user is studying (not archive-only)
- [ ] Update `domains/<slug>/overview.md` progress
