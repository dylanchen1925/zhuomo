# Run — Roguelike Multi-Domain Learning (Zhuomo)

**Run** fuses concepts from **multiple wiki domains** into a **fictional scenario**, then tests you floor-by-floor with questions grounded in **your wiki** — not the story.

Scenario = fiction. Answers = wiki-cited truth. Permadeath of the **run**, not of knowledge.

For daily use: [USER-GUIDE.md](USER-GUIDE.md#17-roguelike-runs). Conceptual fit: [FRAMEWORK.md](FRAMEWORK.md).

---

## Why Run exists

| Artifact | What it tests |
|----------|----------------|
| Recall cards | Atomic facts |
| Quizzes | Single-source comprehension |
| Applied journal | Real-world use |
| **Run** | **Cross-domain transfer under narrative pressure** |

Roguelike structure adds **escalating difficulty**, **low-stakes failure**, and **meta-progress** across sessions.

---

## Roguelike mapping

| Game term | Zhuomo meaning |
|-----------|----------------|
| **Run** | One session: fuse domains → scenario → N floors |
| **Seed** | Domain combo + difficulty + date (reproducible) |
| **Floor** | One scene beat; 1–3 questions; harder each floor |
| **Death** | Failed explain-back or can't cite wiki → run ends |
| **Loot** | Recall cards, synthesis stubs, framework progress notes |
| **Boss** | Final synthesis question across all fused domains |
| **Meta-progress** | `solid` pillars, unlocked domain pairs, rematch seeds |

---

## When to Run

**Use:**

- You have **2+ domains** with enough concept pages to fuse
- You want **integration**, not another chapter quiz
- Weekly ritual step — one 10-min run on a weak domain pair
- After ingest — cement new concepts against an existing domain

**Don't:**

- Run before minimal wiki exists (ingest first)
- Treat scenario fiction as wiki facts
- Skip debrief / loot (run without filing wastes the session)

---

## Agent workflow

### 1. Select fusion

Read `wiki/domain-map.md` and chosen `wiki/domains/*/framework.md`.

| Mode | How |
|------|-----|
| **User pick** | `fuse networking + psychology` |
| **Random fuse** | Agent picks 2 domains from domain-map |
| **Themed fuse** | User theme: "incident response", "negotiation under uncertainty" |
| **Boss rematch** | Re-run prior seed after Revise/ingest |

Prefer concepts tagged `epistemic: established`; use `tentative` on early floors; use `contested` as **trap floors** (must acknowledge both sides).

### 2. Build scenario bible (fiction)

Short document in chat + filed in run artifact:

- Setting, stakes, cast (all fictional)
- **Constraint sheet** — list of wiki pages the run must exercise
- No claims that contradict wiki without marking as story-only

### 3. Floors

Default: **5 floors** + **1 boss**. Adjust by user (`3 floors`, `hard`).

Each floor:

1. **Scene twist** — advances fiction
2. **Question(s)** — decision, explain-why, or tradeoff
3. **GM note** (optional) — concepts tested this floor
4. User answers
5. **Grade** — against wiki only; cite `[[pages]]`; note gaps

**Death condition:** user can't explain with wiki support after one nudge → run ends; still debrief.

### 4. Boss

Cross-domain synthesis: one hard tradeoff requiring concepts from **every** fused domain.

Pass: coherent answer citing multiple domains.  
Partial: file gaps as loot recall cards.

### 5. Debrief + loot

Always file `wiki/learn/runs/YYYY-MM-DD-[seed-slug].md`:

- Scenario summary (fiction)
- Floors cleared / death floor
- Weak concepts → 2–5 new recall cards in `wiki/learn/recall/[domain]/`
- Optional synthesis stub in `wiki/synthesis/` if a cross-domain insight emerged
- Update `framework.md` progress if user passed boss (bump toward `solid` per [RETENTION.md](RETENTION.md))
- Append `wiki/log.md`: `run | domains | outcome | seed`

If user answer reveals **wiki error** (not story error) → offer **Revise**, don't patch via fiction.

---

## Grounding rules (required)

1. **Scenario ≠ claim** — frontmatter `type: fictional-scenario`; never ingest plot as fact
2. **Answers cite wiki** — good answers name `[[concept]]` pages; reject hand-wavy lore
3. **Contested stays contested** — trap floors present both sides; grading honors `epistemic: contested`
4. **Revise on real conflict only** — fiction doesn't force wiki changes
5. **Fuse from wiki, not imagination** — agent reads concept pages before writing questions

---

## Run artifact template

Path: `wiki/learn/runs/YYYY-MM-DD-[seed-slug].md`

```markdown
---
type: fictional-scenario
seed: 2026-06-01-net-psych-7
domains: [networking, psychology]
difficulty: medium
floors_total: 5
floors_cleared: 4
outcome: death-floor-5
concepts_tested: ["[[bgp]]", "[[amygdala-hijack]]"]
---

# Run — The Friday Outage

## Scenario (fiction)

Regional bank, 4pm, alerts flooding. You are lead SRE. The CFO is in the war room…

## Constraint sheet (wiki)

Must exercise: [[bgp]], [[bgp-graceful-restart]], [[amygdala-hijack]], [[decision-fatigue]]

## Floor 3

**Scene:** Team wants to hard-restart all edge routers…

**Question:** What's wrong with that plan? What do you propose instead?

**GM note:** Tests graceful restart vs panic; team dynamics.

### Your answer

(user text or summary)

### Grade

Missed [[bgp-graceful-restart]]. Strong cite of [[amygdala-hijack]] for de-escalation.

## Boss (floor 5)

**Question:** …

### Grade

Death — couldn't tie finance SLA to routing policy without hand-waving.

## Loot

- [ ] Recall card added: `wiki/learn/recall/networking/bgp-gr-restart.md`
- [ ] Synthesis stub: [[synthesis/outage-culture]]
- Framework bump: networking pillar "incident response" → learning → (solid if boss passed)

## Rematch

`/zhuomo Run rematch seed:2026-06-01-net-psych-7`
```

---

## Meta-progress (optional)

Track on `wiki/learn/runs/index.md` or domain `framework.md`:

| Field | Meaning |
|-------|---------|
| Runs completed | Count per domain pair |
| Bosses cleared | Unlocks harder difficulty |
| Favorite seeds | Links to rematch |
| Weakest fuse pair | Suggested next run |

---

## Example prompts

```
/zhuomo Run: fuse networking + psychology — roguelike, 5 floors, medium

/zhuomo Run random — 2 domains from domain-map, easy, 3 floors

/zhuomo Run themed "incident response" — use my weakest domains from framework progress

/zhuomo Run rematch seed:2026-06-01-net-psych-7

/zhuomo Run boss only — finance + distributed-systems, hard
```

---

## Relation to other operations

| Operation | Link |
|-----------|------|
| **Learn → Connect** | Single cross-domain prompt; Run is full scenario arc |
| **Review** | Run debrief may spawn explain-back on weak pillars |
| **Weekly** | Optional step 2b: one short Run instead of Connect |
| **Revise** | If run exposes wiki error, not scenario error |
| **Framework** | Loot updates progress / gaps |
| **Synthesis** | Boss insights → `wiki/synthesis/` |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Story facts filed to wiki | Mark `fictional-scenario`; only debrief/loot in wiki |
| Questions not from wiki | Read concept pages before generating floors |
| Single domain only | Run requires 2+ domains or explicit "solo domain drill" mode |
| No artifact filed | Always write `wiki/learn/runs/` + log |
| Flatten contested topics | Trap floor must show both sides |
| Run before ingest | Need L2 concept pages to fuse |

---

## Bootstrap directory

On wiki bootstrap, include:

```
wiki/learn/runs/
wiki/learn/runs/index.md   # optional meta-progress table
```
