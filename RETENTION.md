# Retention (Zhuomo)

**Review, explain-back, mastery, epistemic tags, applied journal.**

Primary guide: [REVIEW.md](REVIEW.md). This file keeps **truth confidence** and **applied** policy.

---

## Review & explain-back

See [REVIEW.md](REVIEW.md) for:

- `Review` vs `Explain-back` operations
- Concept frontmatter (`reviewed`, `explain_back`, `mastery`, `wiki_revised`)
- `## Explain-back` section on concept pages
- Rubric, Weekly checklist, lint review queue

---

## Epistemic status (concept pages)

```yaml
---
epistemic: tentative    # tentative | established | contested | deprecated
sources: 2
applied_count: 0
---
```

| Value | Meaning |
|-------|---------|
| `tentative` | One source or untested |
| `established` | Multi-source and/or applied |
| `contested` | Sources disagree |
| `deprecated` | Superseded — link forward |

Promote `tentative` → `established` when multi-source or applied supports claims (separate from **mastery** `solid`).

---

## Mastery (`mastery` / overview 掌握度)

| Level | Criteria |
|-------|----------|
| **learning** | Deepened; `## Evidence` present |
| **solid** | **Explain-back passed** ([REVIEW.md](REVIEW.md)) |
| **gap** | Stub or not ingested |

Agent updates overview table on Promote / successful Explain-back.

---

## Applied journal (optional, not required)

Path: `wiki/learn/applied/YYYY-MM-DD-slug.md`

```markdown
# Applied — BGP communities at work

- **Concepts:** [[bgp-communities]], [[route-maps]]
- **Context:** Production prefix leak mitigation
- **Decision:** …
- **Outcome:** …
- **Wiki revise?** no / yes → [[log]]
```

- **Not required** for ingest, Weekly, or `solid`.
- **Cannot** promote to `solid` on applied alone — still need explain-back passed.
- Useful evidence for `epistemic: established` and real-world anchors.

---

## Progressive summarization layers

| Layer | Location | Owner |
|-------|----------|-------|
| L0 | `raw/` snapshot | Immutable |
| L1 | `wiki/sources/` | Agent ingest |
| L2 | `wiki/learn/digests/` | Learn |
| L2b | `wiki/learn/fables/` | Learn (Askell fable) |
| L3 | `domains/<slug>/overview.md` | Framework |
| L4 | Concept `## Explain-back` | Review |

---

## Prerequisite graph

On concept pages when useful:

```markdown
## Prerequisites
- [[aci-fabric-underlay]]

## Enables
- [[aci-border-leaf-l3out]]
```

---

## Readwise → raw/inbox

1. Readwise export → `~/zhuomo-data/raw/inbox/readwise-YYYY-MM.md`
2. `/zhuomo Process inbox — ingest highlights to wiki` (no flashcard generation)

See [REFERENCE.md](REFERENCE.md#readwise--highlights-pipeline).
