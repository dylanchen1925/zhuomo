# Concept Claim rubric — 知识笔记

Agent reads at **Ingest / Revise**; user studies **`## Claim`** without the book.

See also: SKILL.md § Learning model · [REVIEW.md](../REVIEW.md)

---

## Two layers (study-technical default)

### 可理解层 (required)

| Block | Content |
|-------|---------|
| **Opening paragraph** | What it is, why it matters, one-line mental model (≥2 sentences; not a tagline) |
| **Mechanism chain** | Condition → process → result (and feedback if relevant) |
| **One complete example** | Walk through start → change → outcome in a concrete scenario |

Optional `###`: `When to use`, `vs [[peer]]`, `Failure modes`, numbered procedure.

### 正式层 (study-technical required)

Section **`### Formal: definitions & parameters`** (or split `### Formal: …` per object):

- Precise definitions, CLI/API params, formulas, version gates
- **Each item points back** to the example above (“对应例子中第 N 步”)
- If truly N/A (literary overview stub): set `formal_layer: n/a` in revision card with reason

**craft-narrative / study-analytic:** formal layer optional; emphasize mechanism + school debate instead.

---

## Concept page contract (section order)

```markdown
---
domain: <slug>
origin: zhuomo
mastery: learning
reviewed:
explain_back: not_started
updated: YYYY-MM-DD
---

# Title

## Claim
…可理解层 + 正式层…

## Personal notes
> Optional link → [[notes/on-concept/<slug>]]

## Explain-back
1. *"…"*
…

## Evidence
| 要点 | 原文 |
|------|------|
| … | [[sources/…]] |

## Sources
- **Raw:** …
```

---

## Explain-back coverage (required)

| Rule | Detail |
|------|--------|
| **Self-contained** | Every prompt answerable from Claim `###` bodies (cold included) |
| **Write order** | Read source → write Claim → Evidence anchors → Explain-back bullets |
| **Count** | 3–4 prompts; ban pure definition recall |
| **≥1 of** | Contrast, scenario, remove-premise, failure/troubleshooting |
| **Lint** | `lint_explain_back_coverage.py`; thin Claim → **Revise** even if ### count OK |

Rubric line: `Claim correct · mechanism OK · ≥1 constraint/trap · aligns with Evidence`.

---

## Pairwise concepts

When two adjacent concepts deepen in same ingest pass:

1. Each gets standalone “what + does what” in Claim opening
2. Same scenario run for both
3. `### vs [[peer]]` on at least one page

---

## Banned 导读 patterns

- “见 chapter …” / “详见原文” as substitute for Claim prose
- Evidence-only answers with stub Claim (<~120 words excluding `###`)
- Chapter paste, enrich snippet fill (`enrich-explain-back-coverage.py --apply` alone)
- Keyword-snippet without synthesis

**Gap signal:** user says「concept 里没有」→ **Revise** (agent re-reads source), not chat lecture.

---

## Frontmatter

| Field | Values |
|-------|--------|
| `mastery` | `learning` \| `solid` (solid only after `explain_back: passed`) |
| `explain_back` | `not_started` \| `attempted` \| `passed` |
| `external_checked` | Set on 外搜 when External row confirmed |
| `epistemic` | `contested` when sources disagree (corpus only) |

**Re-read:** `updated > reviewed` → suggest `Explain-back [[slug]] cold`.
