# 外搜 (External fact-check)

**Trigger:** `外搜`, `外搜 <domain>`, `外搜 [[concept]]`, `external fact-check`.

**Purpose:** Validate corpus against current external sources. Book Evidence stays; add **`External (YYYY)`** rows.

**Claim edits:** user must confirm — never silent overwrite.

---

## Read order (before web)

```
overview → domain-map → domains/<slug>/map → overview (+ guide)
→ Tier A sample Claims + Evidence → grep legacy names/versions
```

---

## Scope

| User says | Scope |
|-----------|--------|
| `外搜 [[slug]]` | Single concept |
| `外搜 <domain>` | All `domain:` pages + overview |
| `外搜 batch N continue` | Resume partial domain run |
| `外搜` alone | Run `lint-external-fact-check.py`; ask or infer domain |

Skip: literary-appreciation unless explicit. Full vault → confirm once.

---

## Fact categories (study-technical)

Recommended release · Rename/rebrand · Exam/cert · CVE/security · Feature gate · EOL/migration.

**study-analytic:** contested sources, revised dates — prefer `epistemic: contested` footnote.

---

## Procedure

```
1. Resolve scope; YYYY = current year
2. Web: 2–4 authoritative sources per category
3. Revision card: Theme | Old signal | New fact | Pages
4. Per page:
   a. Add External (YYYY) row to Evidence
   b. Claim change → **Claim 修正待确认** — STOP until 确认 Claim
   c. After approval → propagate + updated: today + external_checked: today
5. overview.md 外搜 fact-check table + gaps refresh
6. log.md: external-fact-check | scope | N pages | themes
7. Closing block; offer cold Explain-back if updated > reviewed
```

---

## Summary template (三分法)

```markdown
## 外搜摘要 — <domain>

### 事实（有来源）
- …

### 判断（含适用条件）
- …

### 未知 / 待确认
- …

| 主题 | 旧信号 | 更新 |
|------|--------|------|
| … | … | … |

**触及：** N 页 · External (YYYY) 已写入 · Claim 待确认：[[slug]] …

## Claim 修正待确认
| Page | 现 Claim（摘录） | 建议 Claim | 依据 |
|------|------------------|------------|------|
| [[slug]] | … | … | External (YYYY) |

回复 **确认 Claim** / **确认全部 Claim** / 逐条意见；未确认前不得改 wiki Claim。
```

---

## Opportunistic 外搜

| Workflow | When |
|----------|------|
| Ingest 6c | study-technical + reference/selective deepen |
| Query | After Answer; cited slugs stale |
| Study cold | Target slug stale before session |
| Lint | Lists only — does **not** auto-run |

Opt out: `no 外搜` in same message.

---

## vs Revise vs Query

| | 外搜 | Revise | Query |
|---|------|--------|-------|
| Trigger | Stale/time-sensitive | User error | Question |
| Web | Systematic | If new evidence | After wiki insufficient |
| Claim | Confirm gate | Direct fix | Cite only |
