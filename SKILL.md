---
name: zhuomo
description: Turn books, EPUBs, blogs, videos, transcripts, or notes into a personal Obsidian wiki and agent skills; ingest compiles concept 知识笔记, query brain-first, Study via Explain-back, 外搜 external fact-check, Lint health, Adopt existing vault. Use when user says zhuomo, ingest, bootstrap, adopt, query, 外搜, revise, explain-back, lint, study continue, or wants to build/learn from a knowledge base.
disable-model-invocation: true
---

# 琢磨 (Zhuomo)

**琢磨** — polish raw sources into a **personal wiki** + optional **agent skills**.

**Router:** match Step 0 first. **Details:** load `references/*.md` on demand (repo `~/zhuomo/references/`). Human docs: [USER-GUIDE.md](USER-GUIDE.md) · [SIMPLE.md](SIMPLE.md) · [REVIEW.md](REVIEW.md) · [LEARNING.md](LEARNING.md).

---

## Step 0 — Intent router (first match wins)

Order when multiple verbs: **Lint → 外搜 → Revise → Ingest → Study → Query**.

| If message contains… | Verb | First action |
|----------------------|------|--------------|
| `Bootstrap`, `建库`, first-time setup | **Bootstrap** | § Bootstrap → [bootstrap-adopt.md](references/bootstrap-adopt.md) |
| `Adopt vault`, `接入已有库` | **Bootstrap (adopt)** | [bootstrap-adopt.md](references/bootstrap-adopt.md) |
| `Ingest continue`, `续 ingest` | **Ingest (resume)** | [ingest-depth-and-resume.md](references/ingest-depth-and-resume.md) § continue |
| `Ingest`, `ingest:`, book/EPUB/PDF/transcript + import | **Ingest** | [ingest-depth-and-resume.md](references/ingest-depth-and-resume.md); `.srt`/`.vtt`/字幕 → [transcript-ingest.md](references/transcript-ingest.md) |
| `Query search:` | **Query (search)** | § Query search |
| `Query`, `Query think:` | **Query (think)** | [query-think-and-apply.md](references/query-think-and-apply.md) |
| `外搜`, `external fact-check` | **外搜** | [external-fact-check.md](references/external-fact-check.md) |
| `Revise`, `修正` | **Revise** | § Revise |
| `Explain-back`, `cold`, `feynman`, `Promote`, `Review queue` | **Study** | [explain-back-modes.md](references/explain-back-modes.md); stuck → [study-diagnosis.md](references/study-diagnosis.md) |
| `Study continue`, `连续学习` | **Study (continue)** | [continuous-study.md](references/continuous-study.md) |
| `Lint`, `doctor` | **Lint** | [lint-interpretation.md](references/lint-interpretation.md) |
| `Connect` | **Connect** | § Connect · [LEARNING.md](LEARNING.md) |
| "怎么用" | **Help** | `[[help]]` + `SIMPLE.md` |
| Ambiguous large book, no `overview only`/`lite` | **Confirm** | § Confirm menu — **stop** |

**Default paths:** raw `~/zhuomo-data/raw/` · wiki Obsidian `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen/wiki/` · scripts `~/zhuomo/scripts/` · config `~/.zhuomo/config.json` (`zhuomo_config.py show`).

---

## Hard rules (every turn)

1. **Brain-first:** `overview` → `domain-map` → domain **`map`** → `overview`/`guide` → `index` → `concepts/` + `sources/` before `notes/` or web/raw.
2. **Never silent overwrite:** Revise or supersede + `log.md` + `updated:`.
3. **No hand-maintained progress tables:** Dataview on concept frontmatter only.
4. **No default digests:** no `learn/digests/` unless user asks.
5. **Explain-back:** one prompt per turn (interactive default).
6. **Explain-back coverage:** every prompt answerable from **`## Claim` `###` bodies** on same page — gap → **Revise**, not chat-only.
7. **Figure N:** inline image or mermaid at first mention.
8. **Closing block:** after Bootstrap / Ingest / Revise / 外搜 / Lint / major Query file-back — § Output templates.
9. **Promote solid:** only when `explain_back: passed`.
10. **Skills ≠ wiki:** no corpus facts in SKILL.md.
11. **Corpus vs personal:** ingest → `concepts/`/`sources/` only; user judgment → `wiki/notes/`.
12. **Concept = 知识笔记:** user learns from Claim; agent reads source at Ingest/Revise — not 导读.

---

## Learning model (summary)

| Layer | Who | When |
|-------|-----|------|
| **`concepts/` Claim** | User | First learn, review, Explain-back |
| **Evidence** | Optional | Provenance, drill-down |
| **`sources/md`** | Agent at ingest; user on demand | Archive — not prerequisite reading |

**Claim rubric (full):** [references/concept-claim-rubric.md](references/concept-claim-rubric.md) — 可理解层 + 正式层 (study-technical).

**Study path:** `map` (~30m) → `study` Tier A → `Explain-back cold` → read Claim → Promote → Evidence on demand.

---

## References index (load when needed)

| Reference | Use when |
|-----------|----------|
| [concept-claim-rubric.md](references/concept-claim-rubric.md) | Ingest deepen, Revise Claim, coverage |
| [ingest-depth-and-resume.md](references/ingest-depth-and-resume.md) | Ingest, continue, source classes |
| [transcript-ingest.md](references/transcript-ingest.md) | SRT/VTT/转写 |
| [explain-back-modes.md](references/explain-back-modes.md) | Study sessions |
| [study-diagnosis.md](references/study-diagnosis.md) | Explain-back stuck |
| [continuous-study.md](references/continuous-study.md) | `Study continue` |
| [query-think-and-apply.md](references/query-think-and-apply.md) | Query + Apply scenario |
| [external-fact-check.md](references/external-fact-check.md) | 外搜 + 三分法摘要 |
| [lint-interpretation.md](references/lint-interpretation.md) | Lint report tiers |
| [bootstrap-adopt.md](references/bootstrap-adopt.md) | Bootstrap / Adopt |

---

## User verbs (7 + adopt/continue)

| Verb | Output |
|------|--------|
| **Bootstrap** | Folders, AGENTS.md, config, wiki skeleton |
| **Ingest** | Concepts + Evidence + Explain-back; partial → `ingest_status` |
| **Query** | Answer + Gaps (+ Apply if scenario) |
| **外搜** | External (YYYY); Claim fix after **确认 Claim** |
| **Revise** | Corrected corpus; personal → `notes/` |
| **Study** | Explain-back / Promote / continue |
| **Lint** | Tiered issue list → Revise / 外搜 / continue ingest |
| **Connect** | Personal `notes/synthesis/` |

---

## Wiki layout (do not invent)

| Page | Path |
|------|------|
| Hub | `wiki/overview.md`, `domain-map.md` |
| Domain | `domains/<slug>/map.md`, `overview.md`, `guide.md`, `study.md` |
| Corpus | `concepts/`, `sources/<slug>.md` + `md/`, `synthesis/` |
| Personal | `wiki/notes/` |
| Log | `wiki/log.md` |

**Do not create:** `framework.md`, `mega-overview.md`, `learn/digests/` (unless asked).

**Corpus vs personal:** see [LEARNING.md](LEARNING.md). **Domain four-page model:** map · overview · guide · study — detail in [LEARNING.md](LEARNING.md).

**map.md contract:** North star, 分层地图 (mermaid), 块关系, 30min path, Tier 对照 — sync via `sync-domain-map-pages.py`.

---

## Bootstrap

→ [references/bootstrap-adopt.md](references/bootstrap-adopt.md)

**Bootstrap:** raw tree + wiki skeleton + `templates/AGENTS.md` + `zhuomo_config.py set` + optional first Ingest.

**Adopt:** `vault-adopt-check.py` first; non-destructive merge of help/AGENTS/marker `.zhuomo-adopted`; never batch-rewrite existing concepts.

---

## Ingest

→ [references/ingest-depth-and-resume.md](references/ingest-depth-and-resume.md) · Claim → [concept-claim-rubric.md](references/concept-claim-rubric.md)

**Summary:** classify → topic map (`templates/wiki/source-page.md`) → md corpus → deepen → map/overview → optional auto **外搜** (study-technical reference/selective) → set `ingest_status` / `next_sections`.

**Resume:** `Ingest continue: <slug>` — deepen `next_sections` only.

**Transcript default:** clean + md corpus; **no** auto concepts unless user asks deepen.

**Confirm menu** (ambiguous large book):

```markdown
**类型：** … · **推荐档位：** …
回复 **继续** / **overview only** / **archive only** / **selective deepen [[x]]** / **精读**
```

---

## Query

**Read order:** overview → domain-map → **map** → overview (+ guide) → index → concepts/sources/synthesis → notes → raw/web.

**Search:** `Query search:` — ranked `[[pages]]` + one line each.

**Think:** → [query-think-and-apply.md](references/query-think-and-apply.md)

Required: `## Answer`, `## Sources`, `## Gaps` (with **Type:** fact/judgment/unknown), `## Next step` (够用 / Study / File / Revise).

**Apply:** add when user gives real scenario — judgment + 下一次验证; default **不写入 wiki**.

**Opportunistic 外搜:** after Answer if cited slugs stale — [external-fact-check.md](references/external-fact-check.md); max 2 domains/turn; `no 外搜` opts out.

---

## Revise

User error, lint tier-2, Explain-back gap, contradiction, approved 外搜 Claim.

```
Locate → revision card → edit/supersede/merge/retract → propagate → updated: → log
```

`Revise [[x]] — 我的想法：…` → `notes/on-concept/<slug>.md` only. Never silent corpus ↔ personal mix.

---

## 外搜

→ [external-fact-check.md](references/external-fact-check.md)

**Gate:** **no Claim edit** without `确认 Claim` / `确认全部 Claim`. External supplements book Evidence.

**Summary:** 事实 / 判断 / 未知 + Claim 修正待确认 table.

**Auto:** Ingest 6c (study-technical deepen); Query/Study cold staleness — same gate.

---

## Study

→ [explain-back-modes.md](references/explain-back-modes.md) · stuck → [study-diagnosis.md](references/study-diagnosis.md) · `Study continue` → [continuous-study.md](references/continuous-study.md)

| Say | Do |
|-----|-----|
| `Explain-back [[x]]` | Interactive, one prompt/turn |
| `… cold` | Hide Claim until end |
| `… feynman` | Advanced opt-in: free teach-back + probes |
| `Promote [[x]] to solid` | If `explain_back: passed` |
| `Review queue: domain` | `reviewed` null or `updated > reviewed` |

---

## Lint

→ [lint-interpretation.md](references/lint-interpretation.md)

```bash
python3 ~/zhuomo/scripts/lint-review-queue.py <vault>/wiki
python3 ~/zhuomo/scripts/lint-figure-visuals.py <vault>/wiki
python3 ~/zhuomo/scripts/lint_explain_back_coverage.py <vault>/wiki
python3 ~/zhuomo/scripts/lint-ingest-resume.py <vault>/wiki
```

Report tiers **1阻断 → 2失真 → 3待消化 → 4维护**. Script output = **candidates**; read pages before merge/delete/Claim edit.

---

## Connect

Personal cross-concept → `wiki/notes/synthesis/` (`origin: personal`). Compiled themes → `wiki/synthesis/` (`origin: zhuomo`) via Ingest/Query — not Connect.

---

## Output templates

**Closing block:**

```markdown
**✓ 完成：** …
**→ 下一步：** …
**⚙ 可选：** Lint · Connect · Ingest continue · 更新 synthesis？
```

**log.md:** `bootstrap` · `ingest` · `ingest-resume` · `revise` · `external-fact-check` · `lint` · `explain-back` · `adopt`

---

## Scripts

| Script | When |
|--------|------|
| `epub-to-wiki-md.py` / `pdf-*` / `markitdown-to-wiki-md.py` | Book/article/video URL corpus |
| `transcript-to-wiki-md.py` | SRT/VTT → `sources/.../md/` |
| `lint-review-queue.py` | Review buckets + External |
| `lint-external-fact-check.py` | External only |
| `lint_explain_back_coverage.py` | Prompt vs Claim ### |
| `lint-ingest-resume.py` | Partial `ingest_status` |
| `vault-adopt-check.py` | Before Adopt |
| `zhuomo_config.py` | `~/.zhuomo/config.json` |
| `sync-domain-study-paths.py` / `sync-domain-map-pages.py` | Domain study/map |
| `embed-figure-visuals.py` / `lint-figure-visuals.py` | Figures |

All under `~/zhuomo/scripts/`. Pass `<vault>/wiki` unless documented otherwise.

**Tests:** `python3 -m unittest discover -s tests -v`

---

## Validation gates (done checklist)

**Ingest:** class/depth on source page · topic map · Claim = 知识笔记 per rubric · Explain-back coverage · map updated · 外搜 6c if study-technical deepen · `ingest_status` set.

**Query:** brain-first · Gaps types · Next step · optional Apply · opportunistic 外搜 if stale.

**外搜:** External rows · Claim 待确认 until approved · log.

**Study:** one prompt/turn · diagnosis if fail · no chat-only gap fill.

**Lint:** tier report · no silent Claim · no `notes/` edits.

---

## Good vs bad (short)

| Bad | Good |
|-----|------|
| 导读 Claim + "见原文" | 可理解层 + 正式层 知识笔记 |
| 外搜 silent Claim edit | 确认 Claim gate |
| Script alert → auto delete page | Read both → merge/supersede |
| Transcript → 50 concepts default | md corpus; deepen only if asked |
| All Explain-back in one message | One prompt per turn |
| enrich `--apply` fixes Claim | Revise synthesis |
| Skip adopt check on full vault | vault-adopt-check first |

---

## Extended docs

| Doc | Use |
|-----|-----|
| [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md) | Multi-device, ops |
| [REFERENCE.md](REFERENCE.md) | EPUB/video edge cases |
| [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md) | Domain Cursor skills |
| [USER-GUIDE.md](USER-GUIDE.md) | Full manual + intent table |

**Edge-case procedures** (figures, EPUB, revision cards) remain in [REFERENCE.md](REFERENCE.md). **Dataview / human Study** in [REVIEW.md](REVIEW.md).
