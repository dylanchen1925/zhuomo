---
name: zhuomo
description: Turn books, EPUBs, blogs, videos, or notes into a personal Obsidian wiki and agent skills; ingest with Evidence, query brain-first, Study via Explain-back, Lint health. Use when user says zhuomo, ingest, bootstrap, query wiki, revise concept, explain-back, lint, weekly, or wants to build/learn from a knowledge base across domains.
disable-model-invocation: true
---

# 琢磨 (Zhuomo)

**琢磨** — polish raw sources into a **personal wiki** + optional **agent skills**. This file is **self-contained**: follow it without loading other Cursor skills. Extended detail: [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md), [REFERENCE.md](REFERENCE.md), [REVIEW.md](REVIEW.md).

**Human docs:** [USER-GUIDE.md](USER-GUIDE.md) · [SIMPLE.md](SIMPLE.md) · [FRAMEWORK.md](FRAMEWORK.md)

---

## Step 0 — Intent router (match first, then act)

Scan the user message **top to bottom**. First matching row wins. If two verbs apply, run in order: **Lint → Revise → Ingest → Study → Query**.

| If message contains… | Verb | First action |
|----------------------|------|--------------|
| `Bootstrap`, `建库`, first-time setup | **Bootstrap** | § Bootstrap |
| `Ingest`, `ingest:`, `Process raw`, book/EPUB/PDF path + import intent | **Ingest** | § Ingest — step 1 topic map |
| `Query search:` or "list wiki pages" | **Query (search)** | § Query — search template only |
| `Query`, `Query think:`, question about existing wiki | **Query (think)** | § Query — read wiki brain-first |
| `Revise`, `修正`, user reports wiki error | **Revise** | § Revise |
| `Review [[`, `Explain-back`, `explain-back`, `Promote [[`, `Review queue` | **Study** | § Study |
| `Lint`, `Weekly`, `doctor`, health check | **Lint** (+ Weekly if said) | Run scripts § Scripts |
| `Learn fable`, `Framework`, `Connect` | **Learn** (subset) | [LEARNING.md](LEARNING.md); `Framework` → `sync-domain-study-paths.py` (`--tiers-only` = 只更新分层) |
| `Extract skill`, `RED`, skill from concept | **Skill extract** | § Skill extraction |
| "怎么用", "有哪些功能" | **Help** | Link vault `[[help]]` + `SIMPLE.md`; do not dump full spec |
| Ambiguous + large book/EPUB, no `overview only` / `lite` | **Confirm** | § Confirm menu — **stop** until user replies |

**Default paths** (override only if user gives paths):

| What | Path |
|------|------|
| Raw (read-only) | `~/zhuomo-data/raw/` |
| Wiki (Obsidian) | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen/wiki/` |
| Repo scripts | `~/zhuomo/scripts/` |

---

## Hard rules (every model, every turn)

1. **Brain-first:** Read wiki (`overview` → `domain-map` → domain `overview`/`guide` → `index` → `concepts/`) **before** web search or re-reading raw EPUB.
2. **Never silent overwrite:** Revise in place or supersede with link; append `log.md`; set `updated:` on changed concept pages.
3. **No hand-maintained progress tables:** Domain progress = Dataview on concept frontmatter only.
4. **No default digests:** Do not create `learn/digests/` unless user explicitly asks.
5. **Explain-back:** One prompt per turn unless user says `batch` / `一次出题`.
6. **Figure N cited:** Inline image or mermaid at first mention — never bare "see Figure N".
7. **Closing block:** After Bootstrap / Ingest / Revise / Lint / major Query file-back — use exact 3-line shape in § Output templates.
8. **Promote to `solid`:** Only when `explain_back: passed` (never on Review alone).
9. **Skills ≠ wiki:** Wiki holds facts/synthesis; skills hold triggers + workflows. Do not paste BGP facts into SKILL.md — use domain skill + WIKI-SCOPE ([WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md)).

---

## User verbs (6)

| Verb | Bundled ops | Primary output |
|------|-------------|----------------|
| **Bootstrap** | setup + optional first ingest | Folders, `AGENTS.md`, wiki skeleton |
| **Ingest** | topic map, md corpus, deepen, framework | Concepts + Evidence + `## Explain-back` |
| **Query** | search / think | Answer + Gaps; optional file to `synthesis/` |
| **Revise** | propagate fix | Corrected pages; `updated:`; log |
| **Study** | Review, Explain-back, Promote, queue | Frontmatter mastery fields |
| **Lint** | doctor-lite + review queue | Issue list → Revise |

**Weekly** = optional alias for Lint + suggest one Explain-back (~15 min). Not required.

---

## Wiki layout (do not invent other shapes)

| Page | Path | Holds |
|------|------|-------|
| Vault hub | `wiki/overview.md` | Domain table + ingest rules — **no domain prose** |
| Domain entry | `wiki/domains/<slug>/overview.md` | Why learn, pillars, **Dataview progress**, glossary, gaps |
| Domain guide | `wiki/domains/<slug>/guide.md` | Concept index + mental model only (concept-first) |
| Concepts | `wiki/concepts/*.md` | Claim, `## Explain-back`, `## Evidence` |
| Synthesis | `wiki/synthesis/*.md` | Cross-concept answers, comparisons |
| Sources | `wiki/sources/<slug>.md` + `md/` | Topic map, raw path, md corpus |
| Log | `wiki/log.md` | Append-only audit |
| Help | `wiki/help.md` | Human cheatsheet (from `templates/wiki/help.md`) |

**Do not create:** `framework.md`, `mega-overview.md`, `learn/digests/`, `learn/reviews/`, `learn/applied/` (unless user explicitly requests).

**New domain:** Add row to `wiki/overview.md` + `domain-map.md`; create `domains/<slug>/overview.md`.

**Reference depth (default):** Deepen **all** topic-map concepts with full pages + Evidence + Explain-back. Opt-out keywords: `overview only`, `lite`, `archive only`, `bootstrap lite`.

---

## Concept page contract

Every deepened concept **must** include these sections **in order**:

```markdown
---
domain: <slug>
mastery: learning
reviewed:
explain_back: not_started
updated: YYYY-MM-DD
---

# Title

## Claim
One paragraph — current trusted statement.

## Explain-back
1. *"Open question testing mechanism…"*
2. *"Trap or contrast…"*
3. *"Procedure or object model…"*

## Evidence
| 要点 | 原文 |
|------|------|
| … | [[sources/<slug>/md/part-NNN#anchor]] |

## Sources
- **Raw:** `~/zhuomo-data/raw/…`

## My take
> Optional. `epistemic: personal` — **your** judgment only; never replace Evidence. User adds via `Revise [[x]] — 我的想法：…`
```

**Optional frontmatter:** `epistemic: personal` on concept or synthesis when content is user-authored (not book Evidence).

**Frontmatter rules:**

| Field | Who sets | Values |
|-------|----------|--------|
| `domain` | Agent on create | slug matching `domains/<slug>/` |
| `mastery` | Promote or passed explain-back | `learning` \| `solid` |
| `reviewed` | Review / Explain-back end | `YYYY-MM-DD` or empty |
| `explain_back` | Explain-back session | `not_started` \| `attempted` \| `passed` |
| `updated` | Any agent edit or explain-back | `YYYY-MM-DD` |

**Re-read trigger:** `updated > reviewed` → user should Review again.

---

## Bootstrap

**Trigger:** `Bootstrap: raw …, vault …` optionally `+ ingest: …`

```
1. Create raw/ tree: inbox/, web/, video/, books/, assets/, processed/
2. Create wiki skeleton:
   index.md, log.md, overview.md, help.md (copy ~/zhuomo/templates/wiki/help.md),
   domain-map.md, learn/fables/ only
3. Copy AGENTS.md template — do NOT write from scratch:
   cp ~/zhuomo/templates/AGENTS.md → <vault>/AGENTS.md
   Replace placeholders only:
   | Placeholder | Value |
   |-------------|-------|
   | {{RAW_PATH}} | User raw path (e.g. ~/zhuomo-data/raw/) |
   | {{VAULT_PATH}} | Vault root with trailing / (e.g. ~/…/Dylan Chen/) |
   | {{BOOTSTRAP_DATE}} | Today YYYY-MM-DD |
4. If first source on same line → run Ingest § steps on that source
5. log.md: ## [date] bootstrap | …
6. Closing block § Output templates
```

---

## Ingest

**Trigger:** `Ingest: <path>` or ingest after Bootstrap.

### Decision gate (before writing files)

| Condition | Action |
|-----------|--------|
| Book/large EPUB AND user did NOT say `overview only`/`lite` AND not already confirmed | Post § Confirm menu; **stop** |
| User said `Ingest: path` (explicit) for article/small source | Proceed |
| `raw/inbox/` non-empty | Process inbox files first |

### Procedure (numbered — complete in order)

```
1. Read source structure: TOC, headings, timestamps (video), intro/conclusion
2. Search existing wiki for related [[concepts]] before creating duplicates
3. Write topic map on wiki/sources/<slug>.md (table: Topic | Evidence location | Existing page? | Action)
4. EPUB/PDF → convert full md corpus:
   python3 ~/zhuomo/scripts/epub-to-wiki-md.py <epub> <vault>/wiki/sources/<slug>/md/
   (or pdf-to-wiki-md.py / pdf-ocr-to-wiki-md.py per REFERENCE.md)
5. For each topic-map row (unless overview only):
   a. Create/update wiki/concepts/<slug>.md per § Concept page contract
   b. Add/update wikilinks in domain overview pillars + slim guide.md
   c. Embed figures per § Figure rule
6. Update wiki/index.md; domain overview gaps if needed
6b. **Synthesis gate** — if ingest touches domain mental model or user may have opinions, add to closing block:
    `⚙ 是否更新 synthesis / 域心智模型？回复 domain + 要点` (do not auto-write synthesis)
7. log.md: ## [date] ingest | <title> | N concepts deepened
8. Optional: run lint-figure-visuals.py, lint-review-queue.py
9. Closing block
```

### Topic map template

```markdown
## Topic map — [source title]

| Topic | Evidence (§/ch./time) | Existing wiki? | Action |
|-------|----------------------|----------------|--------|
| … | … | [[…]] or — | Create / Update / Merge |
```

### Figure rule

When prose cites **Figure N** or `#figure-*`:

1. Insert `![Figure N](sources/<slug>/md/assets/…)` immediately after mentioning paragraph
2. Next line: `→ [[sources/.../md/part-NNN#figure-n]]`
3. No asset → mermaid schematic at same spot (topology/flow only)
4. Never a consolidated `## Figures` appendix

Backfill: `python3 ~/zhuomo/scripts/embed-figure-visuals.py <vault>/wiki`

---

## Query

### Read order (mandatory)

```
wiki/overview.md
→ wiki/domain-map.md
→ wiki/domains/<domain>/overview.md (+ guide.md if exists)
→ wiki/index.md
→ wiki/concepts/*.md + wiki/sources/*.md relevant to question
→ only if insufficient: raw/ or external search
```

### Search mode

**Trigger:** `Query search: …`

Output: numbered list — `[[page]] — one line why relevant`. No synthesis essay.

### Think mode (default)

**Trigger:** `Query: …` or `Query think: …`

**Required sections (exact headings):**

```markdown
## Answer
…synthesis with [[wikilinks]]; cite Evidence anchors for deepened concepts…

## Sources
- [[concept-or-page]] — what you used

## Gaps
| Gap | Why it matters | Suggested next step |
|-----|----------------|---------------------|
| stub / no Evidence / stale / contradiction | … | deepen X / Revise Y / new source |
```

**Required — `## Next step` (deterministic; pick exactly one primary line):**

| Condition | Primary line |
|-----------|--------------|
| One-off fact; no Tier A concept in Answer | `**够用** — 无需 Study；下次同类问题可再 Query` |
| Answer used Tier A concept with `explain_back` not `passed` | `**Study** — \`Explain-back [[slug]]\`` (pick highest-signal Tier A slug from domain overview) |
| User stated personal model / checklist / cross-domain comparison | `**File** — \`Connect: … — 记入 synthesis\` 或 \`Revise [[x]] — 我的想法：…\`` |
| Gaps table non-empty with stub/contradiction | `**Revise/deepen** — 见 Gaps 首行` |

```markdown
## Next step
**Study** — `Explain-back [[cilium-network-policy-identity]]`（Tier A，尚未 passed）
```

**Network/IT domains:** Answer leads with business constraint → design lever → technical object.

**File back when:** comparison, cross-concept synthesis, or durable Q&A → `wiki/synthesis/<slug>.md` or extend concept; append `log.md` if substantial.

---

## Revise

**Trigger:** user error report, lint finding, or new source contradicts wiki.

```
1. Locate: target page, backlinks (grep wiki), related skills
2. Fill revision card (mental or chat):
   - Old claim | New claim | Evidence | Pages to propagate
3. **User idea** (`Revise [[x]] — 我的想法：…`):
   - Add or update `## My take` on concept; set `epistemic: personal` in frontmatter if not already
   - If cross-concept → create/update `wiki/synthesis/<slug>.md` from `templates/wiki/synthesis.md`
   - Never overwrite `## Evidence` rows; if contradicts Claim → `epistemic: contested` + note both views
4. Choose action:
   - Edit in place (minor)
   - Supersede (old wrong → status: superseded + forward link)
   - Merge (duplicates → one canonical)
   - Retract (archive + why)
5. Propagate: fix every page citing old claim
6. Set updated: today on all touched concept pages
7. log.md: ## [date] revise | [[page]] | reason
8. Closing block
```

**Connect → wiki (model layer L1):**

```
User: Connect: <cross-concept insight> — 记入 synthesis
```

1. Copy `templates/wiki/synthesis.md` → `wiki/synthesis/<kebab-slug>.md`
2. Fill `## Model`, `## My take`, link `[[concepts]]`
3. Link from domain `overview.md` 心智模型 or relevant concept `## My take`
4. log.md: `## [date] connect | synthesis/<slug>`

**Never:** paste user model into `## Claim` without `## My take` separation.

---

## Study

### Operations

| User says | Agent does |
|-----------|------------|
| `Review [[concept]]` | Set `reviewed: <today>` in frontmatter |
| `Explain-back [[concept]]` | § Explain-back protocol |
| `Review queue: <domain>` | List concepts where `reviewed = null` OR `updated > reviewed` |
| `Promote [[concept]] to solid` | If `explain_back: passed` → `mastery: solid`; else refuse and say run Explain-back |
| `Weekly` | Lint + review queue + suggest one Explain-back → log |

### Explain-back protocol (interactive — default)

**Do not** dump all questions, model answers, or final score in one message.

```
START:
  1. Read wiki/concepts/<slug>.md (Claim, Explain-back bullets, Evidence)
  2. Post intro: one-line Claim context
  3. Post ONLY prompt 1 from ## Explain-back — nothing else

EACH USER REPLY:
  4. Grade THIS prompt only: ✅ / ⚠️ / ❌ (see table below)
  5. 1–3 sentence correction if ⚠️ or ❌ — not full wiki rewrite
  6. Post ONLY next prompt (or go to END if done)

END (after last prompt):
  7. Session verdict: passed | partial | fail (see table below)
  8. Update frontmatter per verdict table
  9. Offer: Promote to solid (if passed) or retake weak prompts
  10. Optional log: ## [date] explain-back | [[slug]] — passed (3/3)
```

**Per-prompt grades:**

| Mark | Meaning |
|------|---------|
| ✅ | Mechanism correct; aligns with Evidence |
| ⚠️ | Framework OK; missing detail |
| ❌ | Wrong or contradicts wiki |

**Session → frontmatter:**

| Verdict | Criteria | Set |
|---------|----------|-----|
| **passed** | No ❌ on core mechanism; ≥1 trap shown across session | `explain_back: passed`, `reviewed: today`, `updated: today` |
| **partial** | Mix ⚠️/❌ but Claim salvageable | `explain_back: attempted`, `reviewed: today`, `updated: today` |
| **fail** | Wrong Claim or repeated ❌ on mechanism | `explain_back: attempted`; suggest Revise or re-read Evidence |

**Batch mode:** Only if user says `batch` or `一次出题`.

---

## Lint

**Trigger:** `Lint`, after large ingest, or part of Weekly.

Run (replace `<vault>`):

```bash
python3 ~/zhuomo/scripts/lint-review-queue.py <vault>/wiki
python3 ~/zhuomo/scripts/lint-review-queue.py <vault>/wiki --domain kubernetes-cilium
python3 ~/zhuomo/scripts/lint-figure-visuals.py <vault>/wiki
```

**Review queue buckets (script output — act in order):**

| Bucket | Action |
|--------|--------|
| `SOLID_CANDIDATE` | `Promote [[slug]] to solid` |
| `READ_UNTESTED` | `Explain-back [[slug]]` — reviewed but not passed |
| `STALE` | Re-read + Review |
| `NEVER_REVIEWED` | Review or deepen |
| `MISSING_EXPLAIN_BACK_SECTION` | Add `## Explain-back` |

| Check | If failed |
|-------|-----------|
| Broken `[[wikilinks]]` | Fix path or create stub with `domain:` |
| Orphan concept (no inbound link) | Link from overview / guide / peer concept |
| Text mentions concept, no page | Stub or merge duplicate |
| Deepened concept missing `## Evidence` | Add Evidence or note in overview gaps |
| Figure N without inline visual | embed-figure-visuals.py or manual inline |
| `updated > reviewed` | Report in review queue (user Study) |
| Missing `## Explain-back` on deepened concept | Add 3 prompts |
| Contradiction between pages | Revise |
| Duplicate topic pages | Merge to one canonical |

**Auto-stub:** Pillar links `[[missing-slug]]` → minimal concept page + link back to pillar.

Append `## [date] lint | N issues` to `log.md`. List each issue with suggested Revise/deepen. Closing block.

---

## Skill extraction (self-contained RED / GREEN / REFACTOR)

**No external skill required.** Use when user says `Extract skill from [[concept]]` or after ingest for actionable techniques.

### Extraction card (fill before writing SKILL.md)

| Field | Content |
|-------|---------|
| Trigger | Situation/symptoms — not chapter title |
| Core move | One non-obvious action |
| Steps | Numbered workflow or decision tree |
| Anti-pattern | Common failure |
| Example | One before/after |
| Type | technique / pattern / reference / discipline |

**Filter:** Keep only if **actionable AND non-default** (agent would not do this without the skill).

### RED (baseline — before SKILL.md exists)

1. Describe trigger scenario to agent **without** showing draft skill.
2. Record what agent actually does (especially wrong shortcuts).
3. For **discipline** type: add time pressure / authority / sunk cost; note verbatim rationalizations.

**Gate:** Do not write SKILL.md until RED shows a gap the skill must fix.

### GREEN (minimal skill)

Write SKILL.md with: name, description (CSO ≤1024 chars, third person, "Use when…"), trigger keywords, numbered steps, anti-pattern counter.

### REFACTOR

Add explicit counters for each RED rationalization. Re-run one RED scenario — agent must follow skill.

Update `SOURCES.md` + `log.md`: `## [date] skill | <name> | from [[concept]]`

---

## Output templates

### Confirm menu (ambiguous large ingest)

```markdown
**Ingest 计划：** [书名] → topic map → md 全文 → deepen **约 N 个概念** + Evidence。
继续默认 reference depth？回复 **继续** / **overview only** / **只 deepen [[某主题]]**
```

### Closing block (required after major ops)

```markdown
**✓ 完成：** [操作] — [1 句结果，如 12 concepts + Evidence]
**→ 下一步：** [1–2 个具体建议，链到 [[wikilinks]] 或指令]
**⚙ 可选：** `overview only` · `Learn fable [[stub]]` · `Weekly` · `Lint` · `更新 synthesis？`
```

### log.md lines

```markdown
## [YYYY-MM-DD] bootstrap | vault created
## [YYYY-MM-DD] ingest | Book Title | 12 concepts deepened
## [YYYY-MM-DD] revise | [[aci-foo]] | corrected FD_VNID claim
## [YYYY-MM-DD] lint | 3 broken links
## [YYYY-MM-DD] explain-back | [[aci-foo]] — passed (3/3)
## [YYYY-MM-DD] weekly | lint + suggested [[aci-bar]]
```

### Source page header

```markdown
# Source — [Title]

- **Raw:** `~/zhuomo-data/raw/…`
- **URL:** … (accessed YYYY-MM-DD)
- **Topics:** [[concept-a]], [[concept-b]]
```

---

## Scripts (deterministic — prefer over guessing)

| Script | When |
|--------|------|
| `epub-to-wiki-md.py` | EPUB → `sources/<slug>/md/` |
| `pdf-to-wiki-md.py` | Text PDF |
| `pdf-ocr-to-wiki-md.py` | Scanned PDF |
| `embed-figure-visuals.py` | Inline figures at mentions |
| `lint-figure-visuals.py` | Find missing figure embeds |
| `lint-review-queue.py` | `updated > reviewed`, missing Explain-back |
| `add-evidence-sections.py` | Backfill Evidence blocks |
| `sync-domain-study-paths.py` | Study paths + Tier A/B/C/D + Dataview queues on overviews |
| `simplify-vault.py` | One-shot vault migration (archive) |

All under `~/zhuomo/scripts/`. Pass `<vault>/wiki` as argument unless script docs say otherwise.

**Framework:**

```bash
# Full: paths + tiers + solid/read Dataview blocks
python3 ~/zhuomo/scripts/sync-domain-study-paths.py <vault>/wiki

# Tiers + queues only (after ingest, no path rewrite)
python3 ~/zhuomo/scripts/sync-domain-study-paths.py <vault>/wiki --tiers-only
```

Tier definitions: `scripts/domain_study_tiers.py` — edit then re-run sync.

---

## Validation gates (before saying "done")

### Ingest

- [ ] Topic map on source page
- [ ] EPUB/PDF has md corpus under `sources/<slug>/md/` (unless overview only)
- [ ] Every deepened concept has Claim, Explain-back (3+), Evidence table
- [ ] `index.md` updated; `log.md` appended
- [ ] No dangling `[[wikilinks]]` on touched pages
- [ ] Closing block posted
- [ ] If domain mental model may change: offer synthesis update in `⚙ 可选`

### Query (think)

- [ ] Brain-first read order followed
- [ ] Output has `## Answer`, `## Sources`, `## Gaps`, `## Next step`
- [ ] Gaps table non-empty if any stub/contradiction exists
- [ ] Next step follows deterministic table (够用 / Study / File / Revise)

### Explain-back

- [ ] One prompt per turn (unless batch)
- [ ] Frontmatter updated only at session end
- [ ] `passed` not set if core mechanism contradicts wiki

### Revise

- [ ] Old claim propagated fix on all citing pages
- [ ] `updated:` set; `log.md` appended

### Lint

- [ ] Scripts run or manual equivalent checks listed
- [ ] Each issue maps to Revise or deepen action

---

## Good vs bad (calibrate output)

| Bad | Good |
|-----|------|
| Chapter summary pasted as concept Claim | One-sentence Claim + Evidence row per fact |
| All Explain-back Q&A in one message | One prompt → wait → grade → next |
| Progress table edited by hand in overview | Dataview reads concept frontmatter |
| Web search before reading wiki | overview → concepts → then web |
| Skill file full of BGP facts | Domain skill + wiki backend; Revise wiki when facts change |
| "See Figure 5" with no image | Inline `![Figure 5](…)` + source link |
| Query answer with no Gaps section | Gaps table flags stubs and contradictions |
| `mastery: solid` after Review only | solid only after `explain_back: passed` |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| RAG-only, no wiki | Ingest compiles once; wiki stays current |
| User must name topic | Infer from TOC; user topic = priority lens only |
| One concept per whole book | Topic map → many concept pages |
| Skip confirm on ambiguous huge ingest | § Confirm menu |
| Fix only in chat | Revise wiki + log.md |
| New source contradicts old | Revise affected pages; don't keep both as true |
| `framework.md` / mega-overview | `overview.md` + optional `guide.md` only |
| Dump nine verbs in chat | Link `[[help]]` |

---

## Extended docs (optional depth)

| Doc | Use when |
|-----|----------|
| [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md) | Multi-device, operations detail, bridge to skills |
| [templates/AGENTS.md](templates/AGENTS.md) | Vault AGENTS.md — copy on Bootstrap |
| [REFERENCE.md](REFERENCE.md) | EPUB/video/Readwise edge cases, revision cards |
| [REVIEW.md](REVIEW.md) | Human-facing Study guide, Dataview examples |
| [LEARNING.md](LEARNING.md) | Fable, Connect, framework rituals |
| [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md) | Domain skills with WIKI-SCOPE |
| [USER-GUIDE.md](USER-GUIDE.md) | Full user manual |
