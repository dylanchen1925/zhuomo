# Zhuomo vault — agent conventions

Bootstrapped: {{BOOTSTRAP_DATE}}

**Procedures:** `~/zhuomo/SKILL.md` (self-contained — ingest, query, revise, study, lint).  
**Human cheatsheet:** `wiki/help.md` (from repo `templates/wiki/help.md`).

---

## Ingest depth (default)

**Default:** `reference depth` for **Study-type** books (technical, analytic, craft) — see `~/zhuomo/SKILL.md` § Source types.

**Opt-out / literary:** `overview only`, `lite`, `archive only`, `selective deepen`, `精读` — fiction/poetry appreciation defaults to overview/archive unless user says 精读.

**Archive only:** Ingest source + concept stubs only; skip Explain-back / fable unless asked.

**No default digests:** Do not create `learn/digests/`, `learn/reviews/`, or `learn/applied/`.

---

## Reference depth workflow

1. **Topic map** on `wiki/sources/[slug].md`
2. **EPUB/PDF** → `wiki/sources/[slug]/md/` via `~/zhuomo/scripts/epub-to-wiki-md.py` or `pdf-to-wiki-md.py` (images → `md/assets/`)
3. **Deepen all** topic-map concepts unless user opted out
4. **Framework** — `domains/<slug>/overview.md` pillars, **Dataview progress**, gaps; optional concept-index `guide.md`
5. **Explain-back** — 3+ prompts under `## Explain-back` on each deepened concept; **fable** only if user asks

---

## Concept page contract

Frontmatter (keep minimal):

```yaml
domain: <slug>
origin: zhuomo
mastery: learning              # learning | solid
reviewed:                      # YYYY-MM-DD — user read this version
explain_back: not_started      # not_started | attempted | passed
updated: YYYY-MM-DD            # last agent or study edit
```

Body order: **`## Claim`** → optional **`## Personal notes`** (link to `notes/on-concept/<slug>.md` only) → **`## Explain-back`** → **`## Evidence`** → **`## Sources`**

| Rule | Detail |
|------|--------|
| **Personal prose** | `wiki/notes/` only — not long text in `## Claim` / `## Evidence` |
| Re-read | `updated > reviewed` → user should Review again |
| **solid** | Only after `explain_back: passed` (Promote or passed Explain-back session) |
| Progress tables | **Dataview on concepts** in domain `overview.md` — never hand-maintain 100-row tables |
| Figures | Inline image or mermaid at first mention of Figure N — never bare "see Figure N" |

Repo: `~/zhuomo/REVIEW.md` (Study), `~/zhuomo/REFERENCE.md` (figures, EPUB, revise cards).

---

## Wiki layout

| Page | Path |
|------|------|
| Vault hub | `wiki/overview.md` — domain table only; **no domain prose** |
| Domain entry | `wiki/domains/<slug>/overview.md` |
| Domain guide | `wiki/domains/<slug>/guide.md` — concept index only |
| Concepts | `wiki/concepts/*.md` |
| Synthesis | `wiki/synthesis/*.md` |
| Sources | `wiki/sources/<slug>.md` + `md/` text corpus; images in `~/zhuomo-data/corpus/<slug>/assets/` |
| Log | `wiki/log.md` — append-only |
| **Personal notes** | `wiki/notes/` — user-authored; see `templates/wiki/notes-README.md` |
| Fables (optional) | `wiki/learn/fables/` |

**New domain:** Add row to `wiki/overview.md` + `wiki/domain-map.md`; create `domains/<slug>/overview.md`.

**Do not create:** `framework.md`, `mega-overview.md`.

**Architect framing (network/IT):** Query Answer leads business constraint → design lever → technical object.

---

## Knowledge base paths

| Layer | Path |
|-------|------|
| **Raw** (read-only, never edit) | `{{RAW_PATH}}` |
| **Wiki** (corpus + personal) | `{{VAULT_PATH}}wiki/` |
| **Scripts** | `~/zhuomo/scripts/` |

**Multi-device:** Phone → `raw/inbox/` only. Laptop processes inbox first; move to `processed/` or typed folder after ingest. **Laptop owns wiki edits.**

---

## User verbs (6)

| Verb | When | Notes |
|------|------|-------|
| **Bootstrap** | Once | Copy this file from `~/zhuomo/templates/AGENTS.md`; replace `{{…}}` placeholders |
| **Ingest** | New source | Brain-first search wiki; topic map; reference depth default |
| **Query** | Questions | Brain-first read order; think mode → Answer + Sources + **Gaps** |
| **Revise** | Errors, contradictions | Propagate fix; set `updated:`; log |
| **Study** | Learning | Review, Explain-back (one prompt/turn), Promote, Review queue |
| **Lint** | Health | `lint-review-queue.py`, `lint-figure-visuals.py`; log issues |

**Weekly (optional):** Lint + review queue + suggest one Explain-back (~15 min). Not required.

---

## Query — brain-first order

```
wiki/overview.md → domain-map.md → domains/<slug>/overview.md (+ guide.md)
→ index.md → concepts/ + sources/ + synthesis/ (corpus) → notes/ if needed → only then raw or web
```

| Mode | Output |
|------|--------|
| `Query search:` | Ranked `[[pages]]` + one-line relevance |
| `Query think:` (default) | `## Answer` + `## Sources` + `## Gaps` + `## Next step` (够用 / Study / File — see SKILL.md table) |

**Model layer:** L0 overview 心智模型 · L1 compiled `wiki/synthesis/` (`origin: zhuomo`) · L1 personal `wiki/notes/synthesis/` · L2 `wiki/notes/on-concept/`. Template: `templates/wiki/synthesis.md`.

File durable synthesis to `wiki/synthesis/` or extend concepts; append `log.md` if substantial.

---

## Lint (doctor-lite)

Run on request, after large ingest, or optional Weekly:

```bash
python3 ~/zhuomo/scripts/lint-review-queue.py {{VAULT_PATH}}wiki
python3 ~/zhuomo/scripts/lint-figure-visuals.py {{VAULT_PATH}}wiki
```

Fix: broken wikilinks, orphans, missing Evidence / Explain-back, figure embeds, contradictions, duplicates. Lint buckets: `SOLID_CANDIDATE`, `READ_UNTESTED`, `STALE`, … — see SKILL.md § Lint.

---

## Revise

When wrong, stale, contradicted, or duplicated: revision card → edit / supersede / merge / retract → **propagate** → `updated:` → log.

**User idea:** `Revise [[x]] — 我的想法：…` → `wiki/notes/on-concept/<slug>.md`. **Connect** (personal) → `wiki/notes/synthesis/`; compiled cross-book → `wiki/synthesis/`.

---

## Study / Explain-back

- `Review [[concept]]` → set `reviewed: <today>`
- `Explain-back [[concept]]` → **one** `## Explain-back` prompt per turn; grade ✅/⚠️/❌; update frontmatter **after last prompt only**
- `Promote [[concept]] to solid` → only if `explain_back: passed`
- Domain **Tier A/B** in `overview.md` §建议学习顺序; progress in `domains/<slug>/study.md` — sync via `sync-domain-study-paths.py`
- Overview Dataview: **Solid 候选** · **读过未测** (see REVIEW.md)

Batch mode only if user says `batch` or `一次出题`.

---

## Log format

Append under `# Log` (newest first):

```markdown
## [YYYY-MM-DD] ingest | Title | N concepts
## [YYYY-MM-DD] revise | [[slug]] | reason
## [YYYY-MM-DD] lint | N issues
## [YYYY-MM-DD] explain-back | [[slug]] — passed (3/3)
## [YYYY-MM-DD] bootstrap | vault created
```

Use real dates — never placeholder years.

---

## User-facing UX

- **Before large book ingest:** Confirm once unless user said `overview only` / `lite` (see SKILL.md Confirm menu).
- **After major ops:** 3-line closing — `✓ 完成` / `→ 下一步` / `⚙ 可选` (see SKILL.md).
- **Ambiguous request:** Menu before multi-hour deepen.

---

## Co-evolve

Customize paths and domain rules here as the vault grows. When repo conventions change, diff against `~/zhuomo/templates/AGENTS.md` and merge updates.
