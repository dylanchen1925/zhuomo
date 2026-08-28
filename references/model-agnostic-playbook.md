# Model-agnostic playbook — 稳定跨模型表现

**Goal:** 弱模型也能可靠完成 **Lint / Study / Adopt / 结构化 Query / 单页 Revise**；强模型只用在 **新书 Ingest deepen、复杂 Apply、合并消歧**。

Load when: any verb; model seems weak; user asks「少用高阶模型 / 稳定表现」.

See also: [lint-interpretation.md](lint-interpretation.md) · [concept-claim-rubric.md](concept-claim-rubric.md)

---

## Principle: scripts first, model second

| Order | Do | Not |
|-------|-----|-----|
| 1 | Run documented **Python script** with `--dry-run` / default first | Guess file contents |
| 2 | Read **one** page the script flagged | Read whole domain |
| 3 | Apply **fixed template** (Claim rubric, Query sections, closing block) | Improvise report shape |
| 4 | **Stop** at confirm gates (外搜 Claim, merge, delete, large ingest) | Silent overwrite |

**Corollary:** If a task has a script row in SKILL § Scripts → **must run it** before hand-editing corpus.

---

## Capability map (pick path by model strength)

| Verb | Weak model OK | Script anchor | Human / strong model only |
|------|---------------|---------------|----------------------------|
| **Lint** | ✅ | `zhuomo-doctor.py` | Tier-2 spot-check **max 3** pages |
| **Study** | ✅ | frontmatter + Claim ### | Subjective nuance in feynman (opt-in) |
| **Promote** | ✅ | `explain_back: passed` check | — |
| **Bootstrap / Adopt** | ✅ | `vault-adopt-check.py`, templates | — |
| **Query search** | ✅ | brain-first read order | — |
| **Query think** | ⚠️ | fixed `## Answer/Sources/Gaps/Next step` | Apply 场景判断 |
| **Revise 单页** | ⚠️ | Revise ladder § below | Multi-source synthesis |
| **Ingest archive** | ✅ | epub/pdf/transcript scripts | — |
| **Ingest deepen** | ❌ | topic map + rubric checklist | Claim 知识笔记写作 |
| **外搜** | ⚠️ | External template + gate | Source selection |
| **Merge / delete** | ❌ | supersede template only | Always user confirm |

⚠️ = use **narrow scope** (one slug, one section, one prompt).

---

## One command: doctor

```bash
python3 ~/zhuomo/scripts/zhuomo-doctor.py <vault>/wiki
python3 ~/zhuomo/scripts/zhuomo-doctor.py <vault>/wiki --domain network-security
python3 ~/zhuomo/scripts/zhuomo-doctor.py <vault>/wiki --json   # machine-readable
```

Agent **Lint** default: run doctor → paste tier sections → **do not** re-run individual lints unless debugging.

---

## Revise ladder (single `[[slug]]`, always in order)

Stop at first step that fixes lint / Explain-back gap.

```bash
# 1 Heuristic rebuild from Evidence-linked source (no LLM)
python3 ~/zhuomo/scripts/batch-revise-knowledge-notes.py <vault>/wiki --slug <slug> --apply

# 2 Two-layer scaffold if missing Formal
python3 ~/zhuomo/scripts/patch-claim-two-layers.py <vault>/wiki --slug <slug> --apply

# 3 Agent read source MD anchors only — edit Claim + Evidence; no chat lecture
#    Use concept-claim-rubric.md checklist line-by-line
```

**Never** skip step 1–2 and jump to prose rewrite.  
**Never** `enrich-explain-back-coverage.py --apply` as default fix.

Domain-wide bulk: use existing `agent-revise-<domain>.py` if present; else batch by `--domain` with `--limit 50` per turn.

---

## Ingest ladder (reduce open-ended work)

| User intent | Weak model path | Strong model path |
|-------------|-----------------|-------------------|
| `archive only` | corpus scripts + stubs | — |
| `overview only` | topic map + stub Claim one-liner | — |
| `reference depth` | **Confirm menu** → stop until user says 继续 | deepen per rubric |
| `Ingest continue` | read `next_sections` only | same, one batch |

```bash
python3 ~/zhuomo/scripts/ingest-batch-chapters.py <vault>/wiki --source <slug>
python3 ~/zhuomo/scripts/ingest-batch-chapters.py <vault>/wiki --source <slug> --mark-done "<chapter>"
```

**Weak model default for ambiguous large book:** run corpus conversion → topic map → **Confirm menu → stop**. Do not deepen 50 concepts in one turn.

Checklist before marking ingest done (tick each):

- [ ] `source_class` + `ingest_status` on source page
- [ ] Each deepened concept: Claim opening ≥2 sentences + ≥1 `###` + `### Formal:` (study-technical)
- [ ] Explain-back 3–4 prompts; run `lint_explain_back_coverage.py` on new slugs
- [ ] `sync-domain-map-pages.py` / `sync-domain-study-paths.py` if domain touched

---

## Study / Explain-back (deterministic grading)

Grade each prompt **only** against Claim `###` bodies (+ Formal if prompt asks params):

| Result | Condition | Action |
|--------|-----------|--------|
| **pass** | Mechanism + ≥1 constraint/trap; aligns Evidence | `explain_back: passed`; offer Promote |
| **partial** | Missing trap or vague | One hint citing Claim heading; retry same prompt |
| **fail** | Wrong mechanism or not in Claim | → [study-diagnosis.md](study-diagnosis.md) row → Revise ladder |

**One prompt per turn.** Do not batch grade. Do not teach from raw book if Claim exists.

---

## Query (fixed sections — copy headings exactly)

Required headings: `## Answer` · `## Sources` · `## Gaps` · `## Next step`  
Optional: `## Apply` (only if user gave scenario)

**Next step** — pick **one** primary from [query-think-and-apply.md](query-think-and-apply.md) § Next step table (no custom categories).

---

## Lint (deterministic bucket → action)

| Bucket | Action (no debate) |
|--------|---------------------|
| `MISSING_EXPLAIN_BACK_SECTION` | Add section + numbered prompts from existing Claim ### titles |
| `EXPLAIN-BACK COVERAGE` | Revise ladder step 1–2 |
| `MISSING_FORMAL` | `patch-claim-two-layers.py --apply --slug` |
| `STALE` / `RETEST` | Tell user `Explain-back [[slug]] cold` |
| `NEVER_REVIEWED` (Tier A) | Same |
| `SOLID_CANDIDATE` | Tell user Promote line |
| `ingest_status: partial` | Quote `next_sections`; offer `Ingest continue` |
| Duplicate / merge | Report only; **no** auto-delete |

Tier **2** spot-check: open **at most 3** flagged pages; if script + ladder fixable → run ladder, do not rewrite by taste.

---

## Forbidden (all models)

- Silent Claim edit after 外搜 (without 确认 Claim)
- `enrich-explain-back-coverage.py --apply` as default
- Hand-maintained progress tables
- Merge/delete concept without user + log
- Ingest → `wiki/notes/`
- Chat-only gap fill when user says「concept 里没有」
- Skip `vault-adopt-check.py` on full vault adopt
- Invent wiki paths (`framework.md`, etc.)

---

## Closing block (always)

```markdown
**✓ 完成：** …
**→ 下一步：** …（one primary action）
**⚙ 可选：** …
```

---

## When to escalate (tell user)

- Merge two non-duplicate concepts
- Ingest deepen >30 concepts in one session without batch script
- Contradiction between two Tier A Claims in same domain
- Apply scenario needs site-specific data you don't have
