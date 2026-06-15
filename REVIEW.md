# Study — Review & Explain-back (Zhuomo)

**Study** = read a concept, teach it back, promote mastery. One human doc for learning + retention.

**Related:** [LEARNING.md](LEARNING.md) (fable only) · [SKILL.md](SKILL.md) (agent ops)

---

## User verbs (6 total)

| Verb | Includes | When |
|------|----------|------|
| Bootstrap | — | Once |
| Ingest | deepen + Evidence + Explain-back | New source |
| Query | search / think | Questions |
| Revise | fix pages | Errors |
| **Study** | Review, Explain-back, Promote, Review queue | Learning |
| Lint | health + review queue | After big ingest, or when something feels stale |

**Weekly** is optional — a bundled alias for `Lint` + one suggested Explain-back (~15 min). **Not required** if you Study ad hoc. Skip Weekly entirely when you already run `Review queue` and `Lint` when needed.

---

## Study operations

| You say | Agent does |
|---------|------------|
| `Review [[concept]]` | Set `reviewed:` today |
| `Explain-back [[concept]]` | Prompts from `## Explain-back` → rubric → update fields |
| `Review queue: cisco-aci` | List `updated > reviewed` and never reviewed |
| `Promote [[concept]] to solid` | Only if `explain_back: passed` |
| `Weekly` | Optional: lint + review queue + suggest one Explain-back → `log.md` |

---

## Concept frontmatter (4 fields + domain)

```yaml
---
domain: cisco-aci
mastery: learning              # learning | solid
reviewed:                      # YYYY-MM-DD — you read this version
explain_back: not_started      # not_started | attempted | passed
updated: 2026-06-14            # last agent or study edit (replaces wiki_revised)
---
```

| Field | Who sets | Meaning |
|-------|----------|---------|
| `reviewed` | You / Review | You've read this version |
| `explain_back` | Explain-back | Can you teach it back? |
| `mastery` | Promote / passed explain-back | `learning` vs `solid` |
| `updated` | Agent on Revise/Ingest; agent on Explain-back | Triggers re-read if `> reviewed` |

**Do not confuse:** `updated` (page changed) ≠ `reviewed` (you studied it).

Add `epistemic: contested` only when sources disagree — not on every page.

---

## `## Explain-back` on every concept page

Place **before** `## Evidence`. Ingest/deepen adds 3–4 prompts per concept.

```markdown
## Explain-back

1. *"…open question…"*
2. *"…trap or contrast…"*
3. *"…procedure or object model…"*

**Rubric:** Claim correct · mechanism OK · ≥1 constraint/trap · aligns with Evidence.
```

---

## Explain-back rubric

| Result | Criteria | Updates |
|--------|----------|---------|
| **passed** | Claim OK; mechanism OK; ≥1 trap; matches Evidence | `explain_back: passed`, `updated`, optional `mastery: solid` |
| **partial** | Framework OK, missing detail | `explain_back: attempted` |
| **fail** | Wrong or contradicts wiki | `explain_back: attempted`; suggest **Revise** |

**Promote to `solid`:** `explain_back: passed` required.

---

## Progress in Obsidian (Dataview)

Domain `overview.md` **does not** duplicate a 100-row progress table. Progress lives on concept pages; overview embeds a Dataview query.

**Requires:** Obsidian [Dataview](https://github.com/blacksmithgu/obsidian-dataview) plugin.

**How to use:**

1. Open `domains/<学科>/overview.md` → scroll to **学习进度** — table auto-lists concepts for that domain.
2. Filter yourself: in any note, paste the query block below and change `domain`.
3. **Review queue in Dataview** — concepts where agent edited after you read:

```dataview
TABLE mastery, reviewed, explain_back, updated
FROM "wiki/concepts"
WHERE domain = "cisco-aci" AND (reviewed = null OR updated > reviewed)
SORT updated DESC
```

4. **Solid concepts:**

```dataview
LIST
FROM "wiki/concepts"
WHERE domain = "cisco-aci" AND mastery = "solid"
```

5. After **Explain-back** or **Revise**, refresh is automatic (Dataview reads frontmatter). No sync script.

| mastery | Meaning |
|---------|---------|
| `learning` | Deepened; has Evidence |
| `solid` | Explain-back passed |

---

## Lint: review queue

```bash
python3 scripts/lint-review-queue.py <vault>/wiki
```

Or say `Lint` / optional `Weekly`:

- `updated > reviewed` → re-read
- No `reviewed` + has Evidence → never reviewed
- `reviewed` but `explain_back` not `passed` → read but not tested
- Missing `## Explain-back`

---

## Optional Weekly (~15 min)

Only if you want a fixed ritual. Otherwise run **Lint** and **Study** when you feel like it.

```
- [ ] 1. Review queue — re-read where updated > reviewed
- [ ] 2. One Explain-back on a weak concept
- [ ] 3. Lint — links, Evidence, figures, review queue
```

Append `wiki/log.md`: `## [YYYY-MM-DD] weekly | …`

---

## Prerequisites (on concept pages when useful)

```markdown
## Prerequisites
- [[aci-fabric-underlay]]

## Enables
- [[aci-border-leaf-l3out]]
```

---

## Example prompts

```
Explain-back [[aci-border-leaf-l3out]]

Review [[aci-spine-leaf-topology]]

Review queue: cisco-aci

Promote [[aci-spine-leaf-topology]] to solid

Lint

Weekly
```

---

## Progressive layers

| Layer | Location |
|-------|----------|
| L0 | `raw/` |
| L1 | `wiki/sources/` |
| L2 | `wiki/concepts/` + `## Explain-back` |
| L3 | `domains/<slug>/overview.md` (pillars + Dataview) |
| Optional | `wiki/learn/fables/` |

No `learn/digests/`, `learn/reviews/`, or `learn/applied/` by default.
