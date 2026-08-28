# Query think + Apply (practice-led)

**Trigger:** `Query: …`, `Query think: …`

Default: brain-first answer. When user gives a **real scenario**, add **Apply** block.

Full read order: SKILL.md § Query (summary) — same as before.

---

## Required sections (think mode)

```markdown
## Answer
…synthesis with [[wikilinks]]…

## Sources
- [[page]] — what you used

## Gaps
| Gap | Type | Why it matters | Suggested next step |
|-----|------|----------------|---------------------|
| … | fact / judgment / unknown | … | Revise / 外搜 / deepen |

## Next step
**Study** — `Explain-back [[slug]]`  (pick one primary: 够用 / Study / File / Revise/deepen)
```

**Gap Type column:** fact = verifiable; judgment = conditional conclusion; unknown = needs research/外搜.

---

## Apply block (when user gave real scenario)

Add after **Next step** when message includes现场/场景/我的环境/故障/选型:

```markdown
## Apply
- **断点：** 预期 … · 实际 … · 差异 …
- **用的 wiki 概念：** [[…]]
- **判断：** … (judgment — state conditions)
- **下一次验证：** one concrete check or experiment
- **写入 wiki：** 默认否；用户说 Revise/Connect 才落盘
```

### Practice contract (internal — merge into Apply)

| Field | Content |
|-------|---------|
| 成功标准 | What “done” looks like for this scenario |
| 边界 | Budget, risk, permissions, must-not-change |
| 观察指标 | What feedback distinguishes explanations |

Do **not** paste practice contract into corpus Claim.

---

## Next step table (deterministic)

| Condition | Primary line |
|-----------|--------------|
| One-off fact; no Tier A in Answer | `**够用** — 无需 Study` |
| Tier A with `explain_back` not `passed` | `**Study** — \`Explain-back [[slug]]\`` |
| Personal model / cross-domain comparison | `**File** — Connect / Revise 我的想法` |
| Gaps non-empty | `**Revise/deepen** — 见 Gaps 首行` |
| Apply + judgment needs verification | `**Study** or 外搜` per Gap type |

---

## Answer framing by domain class

| Class | Shape |
|-------|-------|
| study-technical | business constraint → design lever → technical object |
| study-analytic | question → mechanism / debate → Evidence → implication |
| craft-narrative | principle → example → apply to new scene |
| literary-appreciation | close reading; Next step usually **够用** |

---

## Opportunistic 外搜

After Answer posted: if cited study-technical slugs stale → § [external-fact-check.md](external-fact-check.md).  
Cap: 2 domain 外搜 per Query turn. Opt out: `no 外搜`.

---

## File back

Comparison / durable Q&A → `wiki/synthesis/` (`origin: zhuomo`); append `log.md` if substantial.

Personal cross-concept → **Connect**, not Query file-back.
