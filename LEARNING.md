# Learning & domain overviews (Zhuomo)

Help the user **learn from concepts** and **maintain domain overviews** — not duplicate content in digests.

**Study loop:** [REVIEW.md](REVIEW.md) — `Explain-back` (cold / default / feynman) + Promote.

---

## Architecture (optional)

**North star:** Turn raw sources into durable wiki you can study from; agents query corpus, not re-read EPUBs.

| Layer | Location | Role |
|-------|----------|------|
| **Raw** | `~/zhuomo-data/raw/` | Immutable snapshots — never edited by agent |
| **Wiki** | Obsidian `wiki/` | Concepts, Evidence, domains, synthesis |
| **Personal** | `wiki/notes/` | Your models and takes — not ingest output |

**RAG rediscovers every question. A wiki accumulates.** Ingest compiles once; Query and Revise keep it current.

**Cursor skills:** Not part of zhuomo verbs. To build a skill from wiki content, chat with the agent and point at `[[concepts]]` — no `Extract skill` workflow in this repo.

---

## Explain-back at ingest (required quality)

Every deepened concept gets `## Explain-back` with **3–4 prompts**:

| Rule | Detail |
|------|--------|
| **Ban** | Pure definition recall ("What is X?") |
| **Require ≥1** | Contrast, scenario/decision, remove-premise, or failure/troubleshooting |
| **Prefer** | Synthesis across Claim — not copying one bullet |
| **Rubric line** | `Claim correct · mechanism OK · ≥1 constraint/trap · aligns with Evidence` |

**Tier A first pass:** `Explain-back [[slug]] cold` — [REVIEW.md](REVIEW.md#cold-explain-back-first-learn).

### Learning outputs

| Artifact | Path | When |
|----------|------|------|
| **Explain-back prompts** | `wiki/concepts/*.md` `## Explain-back` | Every deepen (default) |
| **Gap list** | `domains/<slug>/overview.md` §尚未覆盖 | After ingest |
| **Synthesis (compiled L1)** | `wiki/synthesis/*.md` | Ingest / Query file-back (`origin: zhuomo`) |
| **Personal take (L2)** | `wiki/notes/on-concept/<slug>.md` | `Revise [[x]] — 我的想法：…` |
| **Personal synthesis (L1)** | `wiki/notes/synthesis/*.md` | `Connect: … — 记入 synthesis` |

### Model layers

| Layer | Location | Content |
|-------|----------|---------|
| **L0** | `domains/<slug>/overview.md` | Domain map — pillars, gaps, Dataview progress |
| **L1 compiled** | `wiki/synthesis/` | Cross-book themes (`origin: zhuomo`) |
| **L1 personal** | `wiki/notes/synthesis/` | Your cross-concept models (`origin: personal`) |
| **L2 personal** | `wiki/notes/on-concept/` | Your judgment on one concept |

---

## Connect

**What it is:** Save a **personal** cross-concept insight from chat — comparison, mental model, checklist — into `wiki/notes/synthesis/`.

**When to use:** You connected two or more `[[concepts]]` (or domains) in conversation and want it filed for later — not merged into corpus Claim.

**Say:** `Connect: <your insight> — 记入 synthesis`

**Agent does:**

1. Copy `templates/wiki/synthesis.md` → `wiki/notes/synthesis/<kebab>.md`
2. Set `origin: personal`, `kind: chat-summary`
3. Fill `## Model` / `## My take`; wikilink related concepts
4. Append `log.md`: `## [date] connect | notes/synthesis/<slug>`

**Not Connect:** Ingest/Query writing compiled themes to `wiki/synthesis/` (`origin: zhuomo`) — that is corpus file-back, not personal Connect.

**Single-concept opinion:** `Revise [[concept]] — 我的想法：…` → `notes/on-concept/<slug>.md` instead.

---

## Domain overview maintenance

**`domains/<slug>/overview.md`** — pillars, **Dataview progress**, glossary, gaps, **建议学习顺序** (Tier **A** / **B**).

**`guide.md`** — concept index only (concept-first).

Progress: Obsidian Dataview on concept frontmatter — [REVIEW.md](REVIEW.md#progress-in-obsidian-dataview).

**After ingest (agent checklist):**

- [ ] Concepts: `## Evidence` + `## Explain-back` (quality rules above)
- [ ] Frontmatter: `domain`, `mastery`, `explain_back`, `updated`
- [ ] Domain `overview.md` pillars + gaps
- [ ] Run `sync-domain-study-paths.py` (or `--tiers-only`)

```bash
python3 ~/zhuomo/scripts/sync-domain-study-paths.py <vault>/wiki
python3 ~/zhuomo/scripts/sync-domain-study-paths.py <vault>/wiki --tiers-only
```

### Example prompts

```
Connect: native routing vs overlay in Cilium and ACI L3Out — 记入 synthesis

Explain-back [[aci-border-leaf-l3out]] cold
Explain-back [[aci-border-leaf-l3out]] feynman
```
