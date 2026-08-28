# Study diagnosis — when Explain-back stalls

Use when session is **partial/fail** or user says「卡住 / 不会用 / 背了不会讲」.

Do **not** default to feynman alone — pick action by bottleneck.

---

## Bottleneck → zhuomo action

| 卡点 | 常见表现 | 下一步 |
|------|----------|--------|
| **材料不足** | Claim <120 词、纯导读、无 `###` | **Revise** — agent re-reads source, expands Claim |
| **字面不懂** | 术语/符号/CLI 卡 | Read Claim **正式层** + Evidence anchor; not raw book yet |
| **关系没建立** | 会背定义，不会串机制 | **Revise** — add `### vs [[peer]]`, mechanism chain; optional **Connect** |
| **判断失真** | 与 Evidence / 外搜冲突 | **外搜** or **Revise**; do not Promote |
| **不会使用** | Scenario Explain-back ❌ | Revise add procedure + scenario prompt in Claim |
| **没有反馈** | 不确定对错 | **cold** → default Explain-back (interactive grades) |
| **难以行动** | 15 min block too big | Shrink to **one row** on `domains/<slug>/study.md` |

After action → retry Explain-back from appropriate mode (cold / default / feynman).

---

## Mode picker (after diagnosis)

| Situation | Mode |
|-----------|------|
| First learn Tier A | `Explain-back [[slug]] cold` |
| Revision | `Explain-back [[slug]]` |
| Mechanism weak but terms OK | **Revise** Claim first; optional `Explain-back [[slug]] feynman` if user asks |
| Passed | `Promote [[slug]] to solid` |
| solid + reviewed >30d | `Explain-back [[slug]] cold` (RETEST) |

---

## Wiki gap protocol

User: answer not on page / 「concept 里没有」

1. Acknowledge gap in session
2. End session with `explain_back: attempted` if needed
3. **Revise [[slug]]** — expand Claim (not chat-only teaching)
4. Do **not** rely on `enrich-explain-back-coverage.py --apply`

---

## Study continue (continuous learning)

**Trigger:** `Study continue: <domain>` — see [continuous-study.md](continuous-study.md).
