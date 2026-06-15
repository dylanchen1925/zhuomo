# Review & Explain-back (Zhuomo)

Learning loop: **read concept → Review (read) → Explain-back (teach) → mastery**. No flashcards, no Roguelike runs.

**Related:** [LEARNING.md](LEARNING.md) (digests, fable) · [RETENTION.md](RETENTION.md) (epistemic, applied) · [SKILL.md](SKILL.md) (operations)

---

## Operations

| Op | User says | Agent does |
|----|-----------|------------|
| **Review** | `Review [[concept]]` | Mark `reviewed:` today; optional session note |
| **Explain-back** | `Explain-back [[concept]]` | Prompts from `## Explain-back` → score → update fields |
| **Review queue** | `Review queue: cisco-aci` | List `wiki_revised > reviewed` and never reviewed |
| **Promote** | `Promote [[concept]] to solid` | Only if `explain_back: passed` |

---

## Concept frontmatter (review progress)

```yaml
---
domain: cisco-aci
epistemic: tentative
sources: 2
mastery: learning              # learning | solid
reviewed:                      # YYYY-MM-DD — you read and accept current page
explain_back: not_started      # not_started | attempted | passed
explain_back_date:             # YYYY-MM-DD when passed/last attempt
wiki_revised: 2026-06-14       # agent last edited (ingest/revise)
---
```

| Field | Who sets | Meaning |
|-------|----------|---------|
| `reviewed` | You confirm / Review op | You've read this version |
| `explain_back` | Explain-back op | Can you teach it back? |
| `mastery` | Promote / passed explain-back | `learning` vs `solid` |
| `wiki_revised` | Agent on Revise/Ingest | Triggers re-read if `> reviewed` |

**Do not confuse:** `wiki_revised` (agent changed wiki) ≠ `reviewed` (you studied it).

---

## `## Explain-back` on every concept page

Place **before** `## Evidence`. Ingest/deepen must add 3–4 prompts per concept.

```markdown
## Explain-back

1. *"…open question referencing Claim/mechanism…"*
2. *"…trap or contrast…"*
3. *"…procedure or object model…"*

**Rubric:** Claim correct · mechanism without major errors · at least one constraint/trap · aligns with Evidence.
```

Agent uses these prompts in chat; scores **passed** / **partial** / **fail** (see below).

---

## Explain-back rubric

| Result | Criteria | Updates |
|--------|----------|---------|
| **passed** | Claim OK; mechanism OK; ≥1 trap/constraint; follow-up OK; matches Evidence | `explain_back: passed`, `explain_back_date`, optional `mastery: solid` + overview row |
| **partial** | Framework OK, missing detail | `explain_back: attempted`; suggest re-read or fable |
| **fail** | Wrong mechanism or contradicts wiki | `explain_back: attempted`; suggest **Revise** |

**Promote to `solid`:** `explain_back: passed` required. Second source or applied entry **recommended** but not required for single-source books.

---

## Session log (optional history)

`wiki/learn/reviews/YYYY-MM-DD.md`:

```markdown
## [[aci-border-leaf-l3out]]
- **type:** explain-back
- **result:** passed
- **missed:** —
- **action:** —
```

---

## Domain overview progress table

Add columns **Review** and **Explain-back** (or sync from concept frontmatter on Weekly).

| 掌握度 | Meaning |
|--------|---------|
| **learning** | Deepened; has Evidence |
| **solid** | Explain-back passed |
| **gap** | Stub / no Evidence |

---

## Lint: review queue

Run `scripts/lint-review-queue.py <vault>/wiki` or **Lint** / **Weekly**:

- `wiki_revised > reviewed` → agent changed page; you should re-read
- No `reviewed` + has Evidence → never reviewed
- `reviewed` set but `explain_back` not `passed` → read but not tested

---

## Weekly checklist (~15 min)

```
- [ ] 1. Review queue — re-read concepts where wiki_revised > reviewed
- [ ] 2. One Explain-back on a weak or new concept
- [ ] 3. Lint — links, Evidence, review queue, progress sync
- [ ] 4. Framework — sync overview progress columns
- [ ] 5. Applied (optional) — scan learn/applied/; Revise if needed
```

Append `wiki/log.md`: `## [YYYY-MM-DD] weekly | …`

---

## Example prompts

```
Explain-back [[aci-border-leaf-l3out]]

Review [[aci-spine-leaf-topology]] — read and revised in chat today

Review queue: cisco-aci

Promote [[aci-spine-leaf-topology]] to solid — explain-back passed

Applied: border leaf incident — [[aci-border-leaf-l3out]]

Weekly
```
