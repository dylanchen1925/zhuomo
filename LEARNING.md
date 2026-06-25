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

### Learn modes

| Mode | When | What agent does |
|------|------|-----------------|
| **Fable** | User says "I don't get [[concept]]" | Askell-style story → `wiki/learn/fables/` |
| **Connect** | Cross-domain question | Relate concepts across domains in chat |

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

**Study path:** numbered list with `[[concept-slug]]` wikilinks on `overview.md` (and short mirror on `guide.md`). After ingest with new concepts, run `python3 ~/zhuomo/scripts/sync-domain-study-paths.py <vault>/wiki` or say `Framework: <domain>` to refresh paths.

### After ingest checklist (agent)

- [ ] Concepts: `## Evidence` + `## Explain-back`
- [ ] Frontmatter: `domain`, `mastery`, `explain_back`, `updated` on deepen/revise
- [ ] Domain `overview.md` pillars + gaps (no hand-maintained progress table)
- [ ] Optional slim `guide.md` index
- [ ] **Study path:** if new concepts or new domain → run `python3 ~/zhuomo/scripts/sync-domain-study-paths.py <vault>/wiki` or edit paths in script + run
