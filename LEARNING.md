# Learning & Frameworks (Zhuomo)

Help the user **learn from concepts** and **maintain domain overviews** — not duplicate content in digests.

**Study loop:** [REVIEW.md](REVIEW.md) — per-concept `## Explain-back`; on demand, **interactive explain-back** (one prompt per turn).

---

## Learn operation

Runs **during ingest** (Explain-back prompts on concepts) or **on demand** (fable). Default ingest does **not** write `learn/digests/`.

### Learning outputs

| Artifact | Path | When |
|----------|------|------|
| **Explain-back prompts** | `wiki/concepts/*.md` `## Explain-back` | Every deepen (default) |
| **Concept fable** | `wiki/learn/fables/[domain]/` | User asks; hard abstract concept |
| **Gap list** | `domains/<slug>/overview.md` §尚未覆盖 | After ingest |
| **Synthesis (compiled L1)** | `wiki/synthesis/*.md` | Ingest / Query file-back (`origin: zhuomo`) |
| **Personal take (L2)** | `wiki/notes/on-concept/<slug>.md` | `Revise [[x]] — 我的想法：…` |
| **Personal synthesis (L1)** | `wiki/notes/synthesis/*.md` | `Connect: … — 记入 synthesis` |

### Model layers (where your thinking lives)

| Layer | Location | Content |
|-------|----------|---------|
| **L0** | `domains/<slug>/overview.md` 心智模型 | One domain map — agent/user Revise on corpus |
| **L1 compiled** | `wiki/synthesis/` | Cross-book themes from ingest (`origin: zhuomo`) |
| **L1 personal** | `wiki/notes/synthesis/` | Your cross-concept models (`origin: personal`) |
| **L2 personal** | `wiki/notes/on-concept/` | Your judgment on one concept — not `## Evidence` |

### Learn modes

| Mode | When | What agent does |
|------|------|-----------------|
| **Fable** | User says "I don't get [[concept]]" | Askell-style story → `wiki/learn/fables/` |
| **Connect** | Cross-domain or personal model | Chat + **file** to `wiki/notes/synthesis/` if user says 记入 synthesis |

### Fable mode (Amanda Askell)

1. Read `[[concept]]` + Evidence — fable must match wiki.
2. Short story (≈300–800 words); reveal at end.
3. File to `wiki/learn/fables/[domain]/[slug].md`; link from concept.

**Not a substitute for** Evidence or Explain-back.

### Example prompts

```
/zhuomo Learn fable: [[aci-tenant-epg-contract]] — story first, reveal at end

Explain-back [[aci-border-leaf-l3out]]
```

---

## Framework operation

**`domains/<slug>/overview.md`** — north star, pillars, **Dataview progress**, glossary, gaps.

**`guide.md`** — concept index + mental model only (concept-first). No merged technical digest.

Progress: Obsidian Dataview on concept frontmatter — see [REVIEW.md](REVIEW.md#progress-in-obsidian-dataview).

**Study path:** numbered list with `[[concept-slug]]` wikilinks on `overview.md` (and short mirror on `guide.md`).

**Mastery tiers (A/B/C/D):** inline on **建议学习顺序** (**A** / **B** markers); synced from `scripts/domain_study_tiers.py`.

```bash
# Paths + tiers + Dataview solid/read queues
python3 ~/zhuomo/scripts/sync-domain-study-paths.py <vault>/wiki

# After ingest — tiers/queues only
python3 ~/zhuomo/scripts/sync-domain-study-paths.py <vault>/wiki --tiers-only
```

### After ingest checklist (agent)

- [ ] Concepts: `## Evidence` + `## Explain-back`
- [ ] Frontmatter: `domain`, `mastery`, `explain_back`, `updated` on deepen/revise
- [ ] Domain `overview.md` pillars + gaps (no hand-maintained progress table)
- [ ] Optional slim `guide.md` index
- [ ] **Study path / tiers:** run `sync-domain-study-paths.py` (or `--tiers-only` if paths unchanged)
- [ ] **Synthesis gate:** closing block asks if user wants domain model / synthesis update
