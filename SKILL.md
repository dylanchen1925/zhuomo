---
name: zhuomo
description: Turn books, EPUBs, blogs, videos, or notes into a personal Obsidian wiki and agent skills; ingest with Evidence, query brain-first, Study via Explain-back, 外搜 external fact-check, Lint health. Use when user says zhuomo, ingest, bootstrap, query wiki, revise concept, 外搜, external fact-check, explain-back, lint, weekly, or wants to build/learn from a knowledge base across domains.
disable-model-invocation: true
---

# 琢磨 (Zhuomo)

**琢磨** — polish raw sources into a **personal wiki** + optional **agent skills**. This file is **self-contained**: follow it without loading other Cursor skills. Extended detail: [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md), [REFERENCE.md](REFERENCE.md), [REVIEW.md](REVIEW.md).

**Human docs:** [USER-GUIDE.md](USER-GUIDE.md) · [SIMPLE.md](SIMPLE.md) · [LEARNING.md](LEARNING.md)

---

## Step 0 — Intent router (match first, then act)

Scan the user message **top to bottom**. First matching row wins. If two verbs apply, run in order: **Lint → 外搜 → Revise → Ingest → Study → Query**.

| If message contains… | Verb | First action |
|----------------------|------|--------------|
| `Bootstrap`, `建库`, first-time setup | **Bootstrap** | § Bootstrap |
| `Ingest`, `ingest:`, `Process raw`, book/EPUB/PDF path + import intent | **Ingest** | § Ingest — step 1 topic map |
| `Query search:` or "list wiki pages" | **Query (search)** | § Query — search template only |
| `Query`, `Query think:`, question about existing wiki | **Query (think)** | § Query — read wiki brain-first |
| `外搜`, `external fact-check`, `external search:` + domain/concept scope | **外搜** | § 外搜 — brain-first then web |
| `Revise`, `修正`, user reports wiki error | **Revise** | § Revise |
| `Explain-back`, `explain-back`, `Explain-back … cold`, `先测后读`, `Explain-back … feynman`, `feynman`, `Promote [[`, `Review queue` | **Study** | § Study |
| `Lint`, `doctor`, health check | **Lint** | Run scripts § Scripts |
| `Connect` | **Connect** | § Connect — [LEARNING.md](LEARNING.md) |
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

1. **Brain-first:** Read wiki (`overview` → `domain-map` → domain `overview`/`guide` → `index` → `concepts/` + `sources/`) **before** `notes/` or web/raw EPUB.
2. **Never silent overwrite:** Revise in place or supersede with link; append `log.md`; set `updated:` on changed concept pages.
3. **No hand-maintained progress tables:** Domain progress = Dataview on concept frontmatter only.
4. **No default digests:** Do not create `learn/digests/` unless user explicitly asks.
5. **Explain-back:** One prompt per turn — always interactive default.
6. **Figure N cited:** Inline image or mermaid at first mention — never bare "see Figure N".
7. **Closing block:** After Bootstrap / Ingest / Revise / 外搜 / Lint / major Query file-back — use exact 3-line shape in § Output templates.
8. **Promote to `solid`:** Only when `explain_back: passed` (never on Review alone).
9. **Skills ≠ wiki:** Wiki holds facts/synthesis. To create a Cursor skill from wiki content, ask the agent in chat (no zhuomo verb). Do not paste corpus facts into SKILL.md.
10. **Corpus vs personal:** Skill writes **corpus** only (`concepts/`, `sources/`, ingest `synthesis/`). User personal notes live under **`wiki/notes/`** — never Ingest into `notes/`; never paste user judgment into corpus `## Claim` / `## Evidence`.

---

## User verbs (7)

| Verb | Bundled ops | Primary output |
|------|-------------|----------------|
| **Bootstrap** | setup + optional first ingest | Folders, `AGENTS.md`, wiki skeleton |
| **Ingest** | topic map, md corpus, deepen, framework | Concepts + Evidence + `## Explain-back` |
| **Query** | search / think | Answer + Gaps; optional file to `synthesis/` |
| **外搜** | web fact-check + propagate | `External (YYYY)` rows; Claim fixes **after user confirms**; domain overview |
| **Revise** | propagate fix | Corrected pages; `updated:`; log |
| **Study** | Review, Explain-back (cold / feynman), Promote, queue | Frontmatter mastery fields |
| **Lint** | doctor-lite + review queue + external gap scan | Issue list → 外搜 / Revise |


## Wiki layout (do not invent other shapes)

| Page | Path | Holds |
|------|------|-------|
| Vault hub | `wiki/overview.md` | Domain table + ingest rules — **no domain prose** |
| Domain map | `wiki/domain-map.md` | All domains — table links **without** `\|alias` in cells |
| Domain entry | `wiki/domains/<slug>/overview.md` | Why learn, pillars, **Dataview progress**, glossary, gaps |
| Domain guide | `wiki/domains/<slug>/guide.md` | Concept index + mental model only (concept-first) |
| Concepts | `wiki/concepts/*.md` | Claim, `## Explain-back`, `## Evidence` |
| Synthesis | `wiki/synthesis/*.md` | Cross-concept answers, comparisons |
| Sources | `wiki/sources/<slug>.md` + `md/` | Topic map, raw path, md corpus |
| Log | `wiki/log.md` | Append-only audit |
| Help | `wiki/help.md` | Human cheatsheet (from `templates/wiki/help.md`) |
| **Personal notes** | `wiki/notes/` | User-authored; skill touches only on explicit Revise/Note |

**Do not create:** `framework.md`, `mega-overview.md`, `learn/digests/`, `learn/reviews/`, `learn/applied/` (unless user explicitly requests).

### Corpus vs personal notes (two zones)

| Zone | Paths | Written by | Content |
|------|-------|------------|---------|
| **Corpus（琢磨编译）** | `concepts/`, `sources/`, `domains/`, ingest `synthesis/`, `log.md`, `index.md` | Zhuomo skill (Ingest / fact Revise) | Claim + Evidence + Explain-back; book-derived |
| **Personal（个人笔记）** | `notes/` | **You** (Obsidian); agent only when asked | 想法、听课、实验、清单；链到 corpus `[[wikilinks]]` |

```
wiki/notes/
  README.md              # 入口与约定
  inbox/                 # 随手记（手机 / 快捕）
  synthesis/             # 对话总结、跨概念个人模型（主路径）
  by-domain/<slug>/      # 按学科整理（可选）
  on-concept/<slug>.md   # 单概念短评
```

| Rule | Detail |
|------|--------|
| **对话总结** | 聊完让 Agent 整理 → `notes/synthesis/<kebab>.md`，`kind: chat-summary`；例：[[notes/synthesis/cisco-sdn-policy-abstraction-by-scope]] |
| **Ingest** | 只写 corpus；**禁止**在 `notes/` 下建概念页或 Evidence |
| **我的想法** | `Revise [[concept]] — 我的想法：…` → 写/更新 `notes/on-concept/<slug>.md`（`origin: personal`）；corpus 概念页最多留一行 `## Personal notes` → 链到该文件 |
| **Connect（个人）** | `Connect: … — 记入 synthesis` 或「聊完总结成笔记」→ `notes/synthesis/<kebab>.md`（`origin: personal`, `kind: chat-summary`） |
| **Connect（编译）** | Ingest / Query 产出的跨书主题 → `wiki/synthesis/` + `origin: zhuomo` |
| **Overwrite** | Agent **不得**静默改 `notes/`；用户改 corpus 用 `Revise`；用户改个人笔记直接在 Obsidian 编辑 |
| **Lint** | `notes/` 不参与 Explain-back / Promote / Dataview 掌握度（除非页面前置 `study: true` 且用户明确要求） |

**Frontmatter `origin`:** corpus 页 `origin: zhuomo`；`notes/` 页 `origin: personal`。旧页无 `origin` 视为 corpus。

**Legacy:** concept 内 `## My take` 仍有效，但**新内容优先** `notes/on-concept/`；迁移时把 My take 剪切到 `notes/on-concept/<slug>.md` 并在 concept 留链接。

**New domain:** Add row to `wiki/overview.md` + `domain-map.md`; create `domains/<slug>/overview.md`.

**Reference depth (default for Study-type books only):** Deepen **all** topic-map concepts with full pages + Evidence + Explain-back. See § Source types — do **not** apply reference depth to literary appreciation or lookup-only sources unless user opts in.

---

## Source types & ingest depth

**Before deepening**, classify the source. User override beats inference. If class is ambiguous (especially fiction/poetry), use § Confirm menu and **stop**.

### Classes

| Class | Typical sources | Default depth | Topic-map grain | Explain-back / Promote |
|-------|-----------------|---------------|-----------------|------------------------|
| **study-technical** | IT, cert guides, RFCs, engineering, ops | **reference depth** | mechanism, object model, procedure, design tradeoff | Yes — mechanism traps; Tier A → solid |
| **study-analytic** | 政经史, 社科, 方法论, 投资框架专著 | **reference depth** (or **selective deepen** if huge) | reusable **解释单元**（机制、学派争论、时期框架）— **not** one concept per chapter/year | Yes — compare schools, causal chain; use `epistemic: contested` |
| **craft-narrative** | 写作技法, 叙事/编剧, 文学批评方法 | **reference depth** | technique, structure, principle | Yes — apply method to novel situation |
| **literary-appreciation** | 小说、诗歌、散文（欣赏/消遣，非 craft） | **overview only** or **archive only** | book-level themes only if user says **精读** / **selective deepen** | **Skip** unless user asks; **no** Promote pressure |
| **reference-lookup** | 年鉴, 辞典, 手册查阅型 | **archive only** | index rows in topic map; deepen on demand via Query | Skip |

### User keywords (override class default)

| Keyword | Effect |
|---------|--------|
| `reference depth` / `study depth` / `继续` | Full deepen all topic-map rows |
| `selective deepen` / `精读` / `只 deepen [[x]]` | Deepen named themes only + optional `wiki/synthesis/<book>.md` |
| `overview only` / `lite` | Topic map + stubs; no full Evidence pass |
| `archive only` | Source page + md corpus; no concept deepen |
| `literary` | Treat as **literary-appreciation** unless title is clearly craft (→ **craft-narrative**) |

### Classifier (agent — step 1 of Ingest)

```
1. If user message names a keyword row above → use that depth
2. Else if domain is IT/network/k8s/security/performance → study-technical
3. Else if domain is macro-cycle-investing, research-methods, technical-analysis → study-analytic or craft per title
4. Else if EPUB fiction/poetry collection OR user says 小说/诗歌/读一读 → literary-appreciation
5. Else if 通史/政论/经济史/传记论点型 → study-analytic
6. Else if 写作/叙事/批评理论 → craft-narrative
7. Else ambiguous large book → Confirm menu with recommended class + depth
```

### Outputs by class

| Class | Primary wiki artifacts |
|-------|------------------------|
| study-technical / craft-narrative | `concepts/*` + domain overview pillars |
| study-analytic | `concepts/*` + **`wiki/synthesis/`** for cross-book models; contested claims in Evidence |
| literary-appreciation | `sources/<slug>.md` + md corpus; optional **one** `wiki/synthesis/<book>.md`; **avoid** concept sprawl |
| reference-lookup | `sources/<slug>.md` + md corpus + topic index table |

### Query answer framing (by domain class)

| Class | Answer shape |
|-------|----------------|
| study-technical | business constraint → design lever → technical object |
| study-analytic | question → mechanism / school debate → Evidence anchor → testable implication |
| craft-narrative | principle → example from source → application to new scene |
| literary-appreciation | close reading + `## My take`; **Next step** usually **够用** or **File** — rarely push Explain-back |

---

## Concept page contract

Every deepened concept **must** include these sections **in order**:

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
One paragraph — current trusted statement.

## Personal notes
> Optional one-liner + link only, e.g. [[notes/on-concept/<slug>]] — **do not** paste long personal prose here.

## Explain-back
1. *"Open question testing mechanism…"*
2. *"Trap or contrast…"*
3. *"Procedure, scenario, or migration…"*

**Ingest quality (required):** See § Explain-back at ingest — no pure-definition prompts; ≥1 application/contrast/trap per concept.

## Evidence
| 要点 | 原文 |
|------|------|
| … | [[sources/<slug>/md/part-NNN#anchor]] |

## Sources
- **Raw:** `~/zhuomo-data/raw/…`

```

**Optional frontmatter:** `epistemic: contested` when sources disagree. **Do not** use `epistemic: personal` on corpus pages — personal content belongs in `notes/`.

**Personal note page** (`wiki/notes/on-concept/<slug>.md` or `notes/inbox/…`):

```markdown
---
origin: personal
domain: <slug>          # optional — for grouping
related: "[[concept-slug]]"
updated: YYYY-MM-DD
---

# My take — <title>

（自由书写；可链 [[concepts]]、[[notes/synthesis/…]]）
```

**Chat summary** (`wiki/notes/synthesis/<kebab>.md`) — 对话后整理的跨概念笔记：

```markdown
---
origin: personal
type: personal-synthesis
kind: chat-summary
domain: <slug>
updated: YYYY-MM-DD
---

# <title>

> 个人笔记（对话总结）。链到 [[concepts]] / [[sources]]；事实以 corpus Evidence 为准。

## Model
…

## My take
…
```

**Frontmatter rules:**

| Field | Who sets | Values |
|-------|----------|--------|
| `domain` | Agent on create | slug matching `domains/<slug>/` |
| `origin` | Agent on corpus create | `zhuomo` (corpus only) |
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
   domain-map.md (copy ~/zhuomo/templates/wiki/domain-map.md),
   notes/ tree (copy ~/zhuomo/templates/wiki/notes-README.md → notes/README.md;
     mkdir notes/inbox notes/by-domain notes/on-concept notes/synthesis)
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
| Book/large EPUB AND user did NOT name depth keyword AND not already confirmed | Post § Confirm menu (include **source class** + recommended depth); **stop** |
| User said `overview only` / `lite` / `archive only` / `selective deepen` / `精读` | Proceed with § Source types keyword |
| User said `Ingest: path` (explicit) for article/small source | Classify § Source types; proceed |
| `raw/inbox/` non-empty | Process inbox files first |
| Class = **literary-appreciation** AND user did not say `精读` / `selective deepen` | Default **overview only** or **archive only** — do not reference-depth |

### Procedure (numbered — complete in order)

```
0. Classify source § Source types; record class + depth in source page frontmatter comment or Topics line
1. Read source structure: TOC, headings, timestamps (video), intro/conclusion
2. Search existing wiki for related [[concepts]] before creating duplicates
3. Write topic map on wiki/sources/<slug>.md (table: Topic | Evidence location | Existing page? | Action)
4. EPUB/PDF → convert full md corpus:
   python3 ~/zhuomo/scripts/epub-to-wiki-md.py <epub> <vault>/wiki/sources/<slug>/md/
   (or pdf-to-wiki-md.py / pdf-ocr-to-wiki-md.py / markitdown-to-wiki-md.py per REFERENCE.md)
5. Deepen per class + depth (§ Source types):
   - reference depth → every topic-map row → full concept pages
   - selective deepen → only listed rows + optional wiki/synthesis/<book>.md
   - overview only → stubs or pillar links only; no full Evidence pass
   - archive only → skip step 5 concept writes
   For each deepened row:
   a. Create/update wiki/concepts/<slug>.md per § Concept page contract
   b. study-analytic: prefer `epistemic: contested` when sources disagree
   c. literary-appreciation + 精读: prefer synthesis over per-chapter concepts
   d. Add/update wikilinks in domain overview pillars + slim guide.md
   e. Embed figures per § Figure rule (study-technical / craft only when figures exist)
6. Update wiki/index.md; domain overview gaps if needed
6b. **Synthesis gate** — required offer for study-analytic & literary 精读; optional for study-technical:
    `⚙ 是否更新 synthesis / 域心智模型？回复 domain + 要点` (do not auto-write synthesis)
6c. **Auto 外搜 (study-technical only)** — when class = **study-technical** AND depth is **reference** or **selective deepen** (skip **overview only** / **archive only**):
    - Resolve domain from new/updated concepts' `domain:` frontmatter (majority wins; tie → source page Topics domain)
    - Immediately run § 外搜 for that `<domain-slug>` (same session; do not wait for user to say `外搜`)
    - Write `External (YYYY)` + overview + log as usual; **Claim patches → § 外搜 Claim confirmation gate** (stop for approval before editing Claim)
    - If ingest touched multiple domains → run 外搜 once per affected domain (batch if large; offer `外搜 batch N continue`)
7. log.md: ## [date] ingest | <title> | N concepts deepened
8. Optional: run lint-figure-visuals.py, lint-review-queue.py
9. Closing block — if step 6c ran, mention 外搜 scope + pending Claim confirmations in **→ 下一步**
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

1. Insert `![Figure N](/corpus/<slug>/assets/…)` immediately after mentioning paragraph
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
→ wiki/concepts/*.md + wiki/sources/*.md + wiki/synthesis/*.md (origin zhuomo)
→ wiki/notes/ (personal — if query needs user model or 我的想法)
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

**Answer framing:** See § Source types → Query answer framing (by domain class). Default for IT/network domains: business constraint → design lever → technical object.

**File back when:** comparison, cross-concept synthesis, or durable Q&A → `wiki/synthesis/<slug>.md` or extend concept; append `log.md` if substantial.

---

## Revise

**Trigger:** user error report, lint finding, or new source contradicts wiki.

```
1. Locate: target page, backlinks (grep wiki), related skills
2. Fill revision card (mental or chat):
   - Old claim | New claim | Evidence | Pages to propagate
3. **User idea** (`Revise [[x]] — 我的想法：…`):
   - Create or update `wiki/notes/on-concept/<slug>.md` (`origin: personal`); on corpus concept add/update `## Personal notes` → link only
   - If cross-concept personal model → `wiki/notes/synthesis/<slug>.md` from `templates/wiki/synthesis.md` with `origin: personal`
   - Never overwrite corpus `## Claim` or `## Evidence`; if user disagrees with book → note in personal file + optional `epistemic: contested` on corpus Claim footnote via Revise card
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

**Personal / cross-concept notes:** see § Connect and `Revise [[x]] — 我的想法：…` → `notes/on-concept/`.

---

## 外搜 (External fact-check)

**Trigger:** `外搜`, `外搜 <domain>`, `外搜 [[concept]]`, `external fact-check`, `/zhuomo 外搜 cisco-aci`.

**Purpose:** Proactively validate **corpus** claims against **current external sources** (vendor matrices, exam catalogs, CVE advisories, renames/EOL). Book Evidence stays; add **`External (YYYY)`** rows and fix Claims only when external facts supersede stale book baseline.

**Not:** personal notes (`notes/`), one-off Query answers, or replacing `## Evidence` book anchors.

### Scope (pick one)

| User says | Scope |
|-----------|--------|
| `外搜 [[slug]]` | Single concept page |
| `外搜 <domain-slug>` | All `domain: <slug>` concept pages + `domains/<slug>/overview.md` |
| `外搜` (no scope) | Run `lint-external-fact-check.py`; list domains with `MISSING_EXTERNAL`; ask user OR pick domain from message context |
| `外搜 batch N continue` | Resume partial domain run (same domain, next chunk) |

**Skip by default:** `literary-appreciation` domains unless user explicitly names scope. **Cross-domain** full vault → confirm once.

### Read order (mandatory — before any web search)

```
wiki/overview.md → domain-map → domains/<slug>/overview (+ guide)
→ Tier A concept slugs from overview
→ sample 3–5 concept Claims + Evidence in scope
→ grep scope for legacy names / version numbers in Claims
```

Then web search for **domain-relevant fact categories** (not page-by-page random search).

### Fact categories (study-technical default)

| Category | Look for | Typical Claim impact |
|----------|----------|----------------------|
| **Recommended release** | Vendor software matrix, EM/LTS trains | Deployment / ops concepts |
| **Rename / rebrand** | Product name changes | Architecture / component pages |
| **Exam / cert** | Active exam version, EOL, blueprint % | Use-case / design methodology |
| **CVE / security** | Critical advisories, fixed trains | Control deployment, firewall, troubleshooting |
| **Feature gate** | "From version X" availability | Multi-site, new object models |
| **EOL / migration** | Deprecated products, replacement | Architecture, integration pages |

**study-analytic:** add contested primary sources, revised dates, school debate — prefer `epistemic: contested` footnote over hard Claim swap unless consensus shifted.

Record search URLs in chat revision card; wiki Evidence row summarizes facts (no bare URL dumps in Claim).

### Procedure (numbered)

```
1. Resolve scope § above; record YYYY = current year for External (YYYY) label
2. Web research: 2–4 authoritative sources per category (vendor docs > exam page > CVE > community)
3. Build revision card (mental or chat table):
   Theme | Old wiki signal | New external fact | Pages to touch
4. For each page in scope:
   a. If no External (YYYY) row → add to ## Evidence (table row preferred):
      | External (YYYY) | <concise facts; page-specific override when needed> |
   b. **Claim confirmation gate (mandatory):** If Claim contradicts external (version gate, "not supported", wrong name) → **do NOT edit Claim yet**. Collect in revision card:
      | Page | Old Claim (excerpt) | Proposed Claim | External fact |
      Post **Claim 修正待确认** block in chat; **stop** until user replies **确认 Claim** / **确认全部 Claim** / per-row approve or reject.
      Only after approval → edit Claim in place + propagate (step 4c).
   c. Propagate approved Claim fixes to every page citing old name/version (grep wiki)
   d. Set updated: today on pages where External row and/or approved Claim changed; wiki_revised: today if field exists
   e. Do NOT change explain_back / mastery unless user asks
5. domains/<slug>/overview.md:
   - updated: today
   - Ensure ## 外搜 fact-check table (create if missing):
     | Batch | 状态 |
     | 全域 YYYY-MM-DD | 完成 — <1-line key themes>; see log.md |
   - Refresh ## 尚未覆盖 / gaps rows that referenced stale baselines
6. log.md append:
   ## [YYYY-MM-DD] external-fact-check | <domain or [[slug]]> | N pages | <key themes>
7. Optional: re-run `lint-review-queue.py` (includes external section)
8. Closing block § Output templates
```

### Per-page contract

| Field | Rule |
|-------|------|
| `External (YYYY)` | One row per pass; newer year supersedes — do not delete old External rows |
| `## Claim` | Edit only when external fact **changes** design truth (not "nice to know") — **always user-confirmed first** (§ Claim confirmation gate) |
| Book Evidence rows | Keep; External supplements time-sensitive facts |
| `notes/` | Never write |

**After 外搜:** `updated > reviewed` on touched pages → suggest `Explain-back [[tier-a-slug]] cold` in closing block.

### Lint integration

Included in default `lint-review-queue.py` output. Standalone:

```bash
python3 ~/zhuomo/scripts/lint-external-fact-check.py <vault>/wiki --domain <slug>
```

| Bucket | Action |
|--------|--------|
| `MISSING_EXTERNAL` | Run `外搜 <domain>` or `外搜 [[slug]]` |
| `STALE_EXTERNAL` | Re-run 外搜 for that scope |

### 外搜 vs Revise vs Query

| | **外搜** | **Revise** | **Query** |
|---|----------|------------|-----------|
| **Trigger** | Stale domain / scheduled refresh | User error / contradiction | Question |
| **Web** | Yes — systematic | Only if new evidence cited | After wiki insufficient |
| **Scope** | Domain or concept batch | Targeted pages + backlinks | Answer in chat |
| **Evidence** | Adds `External (YYYY)` | Edits Claim + book Evidence | Cites existing pages |
| **log** | `external-fact-check` | `revise` | optional file-back |

User-reported mistake mid-外搜 → finish external row, then **Revise** card for that page.

### Output (chat summary — optional before closing block)

```markdown
## 外搜摘要 — <domain>
| 主题 | 旧信号 | 更新 |
|------|--------|------|
| … | book ≤20.6 | Recommended 20.15.x |
**触及：** N 概念页 · External (YYYY) 已写入 · Claim 待确认：[[slug]] …

## Claim 修正待确认
| Page | 现 Claim（摘录） | 建议 Claim | 依据 |
|------|------------------|------------|------|
| [[slug]] | … | … | External (YYYY) + source |
回复 **确认 Claim** / **确认全部 Claim** / 逐条改意见；未确认前不得改 wiki Claim。
```

---

## Study

### Operations

| User says | Agent does |
|-----------|------------|
| `Explain-back [[concept]]` | § Explain-back protocol (default) |
| `Explain-back [[concept]] cold` / `先测后读` | § Cold explain-back — test before revealing Claim |
| `Explain-back [[concept]] feynman` / `feynman` | § Feynman explain-back protocol |
| `Review queue: <domain>` | List concepts where `reviewed = null` OR `updated > reviewed` |
| `Promote [[concept]] to solid` | If `explain_back: passed` → `mastery: solid`; else refuse |

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

### Cold explain-back protocol (first learn — recommended)

**Trigger:** `Explain-back [[concept]] cold` or `… 先测后读` on same line.

**Goal:** Retrieval practice before reading Claim — avoid fluency illusion from pre-reading summaries.

```
START:
  1. Read wiki/concepts/<slug>.md internally (Claim, Explain-back, Evidence) — DO NOT quote Claim/body to user yet
  2. Post intro: "先凭记忆答，不看笔记。答完再对照 wiki。"
  3. Post ONLY prompt 1 from ## Explain-back

EACH USER REPLY:
  4. Grade THIS prompt: ✅ / ⚠️ / ❌ (same table as default)
  5. Brief feedback — cite gaps only; still NO full Claim paste
  6. Post ONLY next prompt

END (after last prompt):
  7. Session verdict + frontmatter (same table as default)
  8. THEN reveal: Claim one-liner + bullet list of what user missed vs Evidence
  9. Suggest: read missed Evidence rows OR `Explain-back [[slug]] feynman` if core mechanism weak
 10. Offer Promote if passed
```

**Rules:** Never show Claim, body, or Evidence anchors before user finishes the prompt. **Tier A first pass:** prefer `cold` over `Review` then default Explain-back.

**Retest:** For `mastery: solid` with stale `reviewed`, Lint RETEST bucket → run `cold` again.

### Feynman explain-back protocol

**Trigger:** `Explain-back [[concept]] feynman` or `… feynman` on same line.

Same **frontmatter** as default Explain-back (`explain_back: passed` → eligible for Promote). Differs in interaction shape:

```
START:
  1. Read wiki/concepts/<slug>.md (Claim, Explain-back, Evidence)
  2. Post intro: one-line domain context only (NOT full Claim) + "用你自己的话讲清楚，像教一个好奇的 12 岁小孩"
  3. Persona: curious child — ask "为什么？" "能举个具体例子吗？" "如果去掉 X 会怎样？"

EACH USER EXPLANATION:
  3. Grade holistically: ✅ / ⚠️ / ❌ vs Claim + Evidence
  4. List: what was right · exact gaps/mistakes · one trap if missed
  5. Child follow-ups on gaps only (1–2 probes max per round) — not a lecture
  6. Optional: "这和 [[prerequisite]] 怎么连？" if concept has ## Prerequisite links
  7. Re-teach ONLY missed parts (short; cite Evidence anchor)
  8. Ask user to explain again — simpler and more complete
  9. Do NOT advance until core mechanism is ✅ (⚠️ on minor detail OK after 2 rounds)

END:
  8. Session verdict: passed | partial | fail (same table as default)
  9. Update frontmatter per verdict
 10. Offer Promote if passed
 11. Optional: append clean 5–8 sentence summary to notes/on-concept/<slug>.md
     (origin: personal) — user says `保存 feynman 笔记` or offer once at end
 12. log.md: ## [date] explain-back-feynman | [[slug]] — passed
```

**Rules:** One turn = one user explanation + one agent feedback block. No lecture before first attempt. No dumping full Claim rewrite. Feynman does **not** skip the numbered `## Explain-back` bullets — if passed via Feynman, those prompts are considered covered for Promote.

### Explain-back at ingest (prompt quality)

When deepening concepts, every `## Explain-back` section must follow:

| Required | Detail |
|----------|--------|
| **Ban** | Pure definition recall ("What is X?") |
| **Include ≥1** | Contrast (X vs Y), scenario/decision, remove-premise ("if we drop …"), or failure/troubleshooting |
| **Prefer** | Synthesis across Claim sections — not a single bullet copy-paste answer |
| **Count** | 3–4 prompts per deepened concept |

Rubric line on page: `Claim correct · mechanism OK · ≥1 constraint/trap · aligns with Evidence`.

---

## Lint

**Trigger:** `Lint`, after large ingest.

Run (replace `<vault>`):

```bash
python3 ~/zhuomo/scripts/lint-review-queue.py <vault>/wiki
python3 ~/zhuomo/scripts/lint-review-queue.py <vault>/wiki --domain kubernetes-cilium
python3 ~/zhuomo/scripts/lint-figure-visuals.py <vault>/wiki
```

`lint-review-queue.py` **includes External (YYYY) fact-check by default** (section `EXTERNAL FACT-CHECK`). Skip with `--skip-external`. Standalone scan: `lint-external-fact-check.py`.

**Review queue buckets (script output — act in order):**

| Bucket | Action |
|--------|--------|
| `SOLID_CANDIDATE` | `Promote [[slug]] to solid` |
| `RETEST` | `Explain-back [[slug]] cold` — solid but `reviewed` >30d (default; `--retest-days`) |
| `READ_UNTESTED` | `Explain-back [[slug]]` or `cold` — reviewed but not passed |
| `STALE` | Re-read + Review |
| `NEVER_REVIEWED` | `Explain-back [[slug]] cold` (Tier A) or Review |
| `MISSING_EXPLAIN_BACK_SECTION` | Add `## Explain-back` |
| `MISSING_EXTERNAL` / `STALE_EXTERNAL` (lint-external-fact-check.py) | `外搜 <domain>` |

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

## Connect

**Trigger:** `Connect: …` or `Connect: … — 记入 synthesis` or user asks to save a cross-concept insight from chat.

**Purpose:** File **personal** cross-concept models to `wiki/notes/synthesis/` — not corpus `concepts/`.

```
1. User states link/comparison/model across [[concepts]] or domains
2. If user says 记入 synthesis (or clear intent to save):
   - Copy templates/wiki/synthesis.md → wiki/notes/synthesis/<kebab>.md
   - origin: personal, kind: chat-summary
   - Fill ## Model / ## My take; wikilink concepts
3. Do NOT merge into corpus Claim/Evidence unless user says Revise
```

**Compiled** cross-book themes from Ingest/Query still go to `wiki/synthesis/` (`origin: zhuomo`) — that is not Connect; it is ingest/query file-back.

---

## Output templates

### Confirm menu (ambiguous large ingest)

```markdown
**类型判断：** [study-technical | study-analytic | craft-narrative | literary-appreciation | reference-lookup]
**推荐档位：** [reference depth | selective deepen | overview only | archive only] — [1 句理由]
**Ingest 计划：** [书名] → topic map → md 全文 → [deepen 约 N 概念 | 仅 synthesis | 仅语料]
回复 **继续**（reference depth）/ **overview only** / **archive only** / **selective deepen [[主题]]** / **精读**
```

### Closing block (required after major ops)

```markdown
**✓ 完成：** [操作] — [1 句结果，如 12 concepts + Evidence]
**→ 下一步：** [1–2 个具体建议，链到 [[wikilinks]] 或指令]
**⚙ 可选：** `overview only` · `Lint` · `Connect: … — 记入 synthesis` · `更新 synthesis？`
```

### log.md lines

```markdown
## [YYYY-MM-DD] bootstrap | vault created
## [YYYY-MM-DD] ingest | Book Title | 12 concepts deepened
## [YYYY-MM-DD] revise | [[aci-foo]] | corrected FD_VNID claim
## [YYYY-MM-DD] external-fact-check | cisco-sdwan | 48 pages | Manager rebrand, 20.15 EM, CVE-2026-20127
## [YYYY-MM-DD] lint | 3 broken links
## [YYYY-MM-DD] explain-back | [[aci-foo]] — passed (3/3)
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
| `markitdown-to-wiki-md.py` | PPTX / DOCX / YouTube → `sources/<slug>/md/` |
| `embed-figure-visuals.py` | Inline figures at mentions |
| `lint-figure-visuals.py` | Find missing figure embeds |
| `lint-review-queue.py` | Review queue + **External (YYYY)** scan (default) |
| `lint-external-fact-check.py` | External scan only (same logic as lint-review-queue) |
| `add-evidence-sections.py` | Backfill Evidence blocks |
| `sync-domain-study-paths.py` | Study paths + inline **A**/**B** tiers + Dataview queues on overviews |
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

- [ ] Source class + depth chosen per § Source types (record on source page)
- [ ] Topic map on source page
- [ ] EPUB/PDF has md corpus under `sources/<slug>/md/` (unless overview only)
- [ ] Every deepened concept has Claim, Explain-back (3+), Evidence table (skip if archive/overview only per class)
- [ ] `index.md` updated; `log.md` appended
- [ ] No dangling `[[wikilinks]]` on touched pages
- [ ] Closing block posted
- [ ] If domain mental model may change: offer synthesis update in `⚙ 可选`
- [ ] **study-technical** + reference/selective deepen: § 外搜 auto-run for ingest domain(s); Claim patches gated per § Claim confirmation gate

### Query (think)

- [ ] Brain-first read order followed
- [ ] Output has `## Answer`, `## Sources`, `## Gaps`, `## Next step`
- [ ] Gaps table non-empty if any stub/contradiction exists
- [ ] Next step follows deterministic table (够用 / Study / File / Revise)

### Explain-back

- [ ] One prompt per turn
- [ ] Frontmatter updated only at session end
- [ ] `passed` not set if core mechanism contradicts wiki

### Revise

- [ ] Old claim propagated fix on all citing pages
- [ ] `updated:` set; `log.md` appended

### 外搜

- [ ] Brain-first read before web search
- [ ] Every in-scope deepened concept has `External (YYYY)` row
- [ ] **No Claim edit without user `确认 Claim` / `确认全部 Claim`**
- [ ] If Claim patches proposed → **Claim 修正待确认** block posted; wiki Claim unchanged until approved
- [ ] Approved Claim fixes propagated via grep
- [ ] `domains/<slug>/overview` **外搜 fact-check** row + gaps refreshed
- [ ] `log.md`: `external-fact-check | …` (note pending Claim count if any)
- [ ] Closing block posted; offer Tier A `Explain-back cold` if `updated > reviewed`

### Lint

- [ ] Scripts run or manual equivalent checks listed
- [ ] Each issue maps to Revise or deepen action

---

## Good vs bad (calibrate output)

| Bad | Good |
|-----|------|
| Chapter summary pasted as concept Claim | One-sentence Claim + Evidence row per fact |
| Novel/poem → 50 chapter concepts + Explain-back | overview only or 精读 → synthesis + few theme concepts |
| History book → one concept per year | study-analytic units: mechanism, school, period framework |
| Mix personal essay into concept Claim | Personal → `notes/on-concept/`; corpus keeps Claim + Evidence |
| Ingest writes into `notes/` | Ingest → corpus only |
| Reference depth on 诗歌消遣读 | archive only; Query + personal notes when needed |
| All Explain-back Q&A in one message | One prompt → wait → grade → next |
| Progress table edited by hand in overview | Dataview reads concept frontmatter |
| Web search before reading wiki | overview → concepts → then web (外搜: read scope first, then web) |
| 外搜 only in chat, no wiki write | Every fact → Evidence `External (YYYY)` + log.md |
| 外搜 silently edits Claim | Post **Claim 修正待确认**; apply only after user confirms |
| study-technical ingest ends without 外搜 | Auto § 外搜 step 6c (unless overview only / archive only) |
| Replace book Evidence with External | External **supplements**; Revise if book Claim wrong |
| Skill file full of BGP facts | Domain skill + wiki backend; Revise wiki when facts change |
| "See Figure 5" with no image | Inline `![Figure 5](…)` + source link |
| `[[path|alias]]` inside markdown table cell | `[[path]]` only — pipe splits table columns |
| `mastery: solid` after Review only | solid only after `explain_back: passed` |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| RAG-only, no wiki | Ingest compiles once; wiki stays current |
| User must name topic | Infer from TOC; user topic = priority lens only |
| One concept per whole book | Topic map → many concept pages |
| Skip confirm on ambiguous huge ingest | § Confirm menu + § Source types class |
| IT defaults applied to fiction | Classify literary-appreciation; overview/archive default |
| Fix only in chat | Revise wiki + log.md; time-sensitive → **外搜** |
| New source contradicts old | Revise affected pages; don't keep both as true |
| Stale release/CVE in Claims | `外搜 <domain>` not one-off Query |
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
| [LEARNING.md](LEARNING.md) | Connect, domain overviews, ingest study-path sync |
| [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md) | Domain skills with WIKI-SCOPE |
| [USER-GUIDE.md](USER-GUIDE.md) | Full user manual |
