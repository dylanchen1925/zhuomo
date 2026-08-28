# Lint — script candidates vs agent judgment

**Trigger:** `Lint`, after large ingest.

Scripts report **candidates**; agent **opens pages** before delete/merge/Claim edit.

---

## Run order

```bash
python3 ~/zhuomo/scripts/lint-review-queue.py <vault>/wiki
python3 ~/zhuomo/scripts/lint-figure-visuals.py <vault>/wiki
python3 ~/zhuomo/scripts/lint_explain_back_coverage.py <vault>/wiki
python3 ~/zhuomo/scripts/lint-ingest-resume.py <vault>/wiki   # partial sources
```

`lint-review-queue.py` includes External scan + Explain-back coverage by default.  
Skip external: `--skip-external`. Standalone: `lint-external-fact-check.py`.

**Never:** `enrich-explain-back-coverage.py --apply` as default Lint fix.

---

## Severity tiers (report in this order)

| Tier | Meaning | Examples |
|------|---------|----------|
| **1 — 阻断** | Broken read path | Broken wikilinks, orphan with no pillar link |
| **2 — 失真风险** | Wrong/stale/contradictory knowledge | Thin 导读 Claim, contradiction, missing External on study-technical Tier A |
| **3 — 待消化** | Structure OK, study backlog | NEVER_REVIEWED, partial ingest, MISSING_EXPLAIN_BACK |
| **4 — 维护便利** | Cosmetic / optional | Figure embed, duplicate title wording |

**Rule:** Zero script alerts ≠ “content all correct”. Agent spot-checks tier-2 candidates.

---

## Bucket → action

| Bucket | Agent action |
|--------|----------------|
| `SOLID_CANDIDATE` | Suggest `Promote [[slug]] to solid` |
| `RETEST` | `Explain-back [[slug]] cold` |
| `READ_UNTESTED` | `Explain-back [[slug]]` or `cold` |
| `STALE` | Re-read Claim (not full book) |
| `NEVER_REVIEWED` | Claim → `Explain-back [[slug]] cold` (Tier A) |
| `MISSING_EXPLAIN_BACK_SECTION` | Add `## Explain-back` |
| `EXPLAIN-BACK COVERAGE` | **Revise** — expand Claim; enrich dry-run only |
| `MISSING_EXTERNAL` / `STALE_EXTERNAL` | Suggest **外搜** — do **not** auto-edit Claim |
| Duplicate topic (manual) | Read both; merge/supersede — **no script auto-delete** |
| `ingest_status: partial` | Offer `Ingest continue: <slug>` |

---

## Auto-fix vs ask user

| Issue | Auto-fix OK? |
|-------|----------------|
| Broken link with known target | Yes |
| Auto-stub for pillar `[[missing-slug]]` | Yes (minimal concept + backlink) |
| Claim text / External content | **No** — 外搜 confirmation gate |
| Merge two concepts | **No** — read both first |
| Delete page | **No** — supersede + forward link |
| `notes/` | **Never** touch in Lint |

---

## Chat report shape

```markdown
## Lint — <vault>

### 1 阻断 (N)
…

### 2 失真风险 (N)
… evidence path …

### 3 待消化 (N)
…

### 4 维护便利 (N)
…
```

Append `log.md`: `## [date] lint | N issues`. Closing block.
