# Zhuomo vault — agent conventions

Bootstrapped: {{BOOTSTRAP_DATE}}

**Procedures:** `~/zhuomo/SKILL.md` (self-contained — ingest, query, revise, study, lint).  
**Human cheatsheet:** `wiki/help.md` (from repo `templates/wiki/help.md`).

---

## Ingest depth (default)

**Default:** `reference depth` for **Study-type** books (technical, analytic, craft) — see `~/zhuomo/SKILL.md` § Source types.

**Opt-out / literary:** `overview only`, `lite`, `archive only`, `selective deepen`, `精读` — fiction/poetry appreciation defaults to overview/archive unless user says 精读.

**Archive only:** Ingest source + concept stubs only; skip Explain-back unless asked.

**No default digests:** Do not create `learn/digests/`, `learn/reviews/`, or `learn/applied/`.

---

## Reference depth workflow

1. **Topic map** on `wiki/sources/[slug].md`
2. **EPUB/PDF** → `wiki/sources/[slug]/md/` via `~/zhuomo/scripts/epub-to-wiki-md.py` or `pdf-to-wiki-md.py` (images → `md/assets/`)
3. **Deepen all** topic-map concepts unless user opted out
4. **Domain overview** — `domains/<slug>/overview.md` pillars, Dataview, gaps; optional `guide.md`
5. **Explain-back** — 3–4 prompts per deepened concept: **no pure definitions**; ≥1 contrast/scenario/trap
6. **Study paths** — run `sync-domain-study-paths.py` after ingest

---

## Concept page contract

Frontmatter (keep minimal):

```yaml
domain: <slug>
origin: zhuomo
mastery: learning              # learning | solid
reviewed:                      # YYYY-MM-DD — set by Explain-back
explain_back: not_started      # not_started | attempted | passed
updated: YYYY-MM-DD            # last agent or study edit
```

Body order: **`## Claim`** → optional **`## Personal notes`** (link to `notes/on-concept/<slug>.md` only) → **`## Explain-back`** → **`## Evidence`** → **`## Sources`**

| Rule | Detail |
|------|--------|
| **Personal prose** | `wiki/notes/` only — not long text in `## Claim` / `## Evidence` |
| Re-read | `updated > reviewed` → `Explain-back [[slug]] cold` |
| **solid** | Only after `explain_back: passed` |
| Progress tables | **Dataview on concepts** — never hand-maintain 100-row tables |
| Figures | Inline image or mermaid at first mention of Figure N |

Repo: `~/zhuomo/REVIEW.md` (Study), `~/zhuomo/REFERENCE.md` (figures, EPUB).

---

## Wiki layout

| Page | Path |
|------|------|
| Vault hub | `wiki/overview.md` |
| Domain entry | `wiki/domains/<slug>/overview.md` |
| Concepts | `wiki/concepts/*.md` |
| Synthesis (compiled) | `wiki/synthesis/*.md` |
| Personal notes | `wiki/notes/` |
| Log | `wiki/log.md` |

---

## User verbs (6) + Connect

| Verb | Notes |
|------|-------|
| Bootstrap · Ingest · Query · Revise · Study · Lint | See `~/zhuomo/SKILL.md` |
| **Connect** | `Connect: … — 记入 synthesis` → `wiki/notes/synthesis/` — `~/zhuomo/LEARNING.md` |

---

## Study / Explain-back

- `Explain-back [[concept]] cold` — first learn; hide Claim until session ends
- `Explain-back [[concept]]` — revision path; one prompt per turn
- `Explain-back [[concept]] feynman` — child-persona teach-back
- `Promote [[concept]] to solid` — only if `explain_back: passed`

---

## Log format

```markdown
## [YYYY-MM-DD] ingest | Title | N concepts
## [YYYY-MM-DD] explain-back | [[slug]] — passed (3/3)
## [YYYY-MM-DD] connect | notes/synthesis/<slug>
```

Co-evolve with `~/zhuomo/templates/AGENTS.md`.
