# Continuous study — Study continue

**Trigger:** `Study continue: <domain-slug>`, `连续学习 <domain>`.

One **lesson per turn** — do not expand into multi-day plan unless user asks.

---

## Procedure

```
1. Read domains/<slug>/study.md — 下一步 column (priority ① → ② → ③)
2. Read log.md — last 5 explain-back / ingest lines for domain
3. Pick ONE concept:
   - First ① Promote row, else ② Explain-back, else ③ Cold
   - If all —, pick next Tier A from overview 建议学习顺序
4. If lint-external stale on target (study-technical Tier A):
   → 外搜 [[slug]] first (External only until Claim confirmed)
5. Run one Study session (interactive Explain-back OR cold per REVIEW)
6. If partial/fail → references/study-diagnosis.md
7. Closing block:
   → 下一步: next study.md row OR Revise/外搜 if diagnosed
```

---

## Stop rules

- One concept session complete (passed / partial with clear Revise path)
- User says stop
- Do **not** auto-ingest next book chapter unless user says `Ingest continue`

---

## Log

Optional: `## [date] study-continue | <domain> | [[slug]] — passed (2/3)`
