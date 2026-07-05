# Zhuomo — simplified mode

**Six verbs:** Bootstrap · Ingest · Query · Revise · Study · Lint. **Connect** for personal cross-concept notes.

## Minimum viable Zhuomo

```
Raw  →  Bootstrap + Ingest  →  concepts + Evidence  →  Query
```

**Daily reference:** Obsidian `wiki/help.md`.

| Keep | Skip until needed |
|------|-------------------|
| `~/zhuomo-data/raw/` inbox | Domain-specific Cursor skills (ask agent in chat) |
| `wiki/concepts/` + Explain-back | Extra repo docs — `help.md` + REVIEW.md enough |
| `wiki/overview.md` + domain overviews | Extra repo docs |
| Chat with agent | — |

## Study (lite)

| Step | Say |
|------|-----|
| First learn | `Explain-back [[concept]] cold` |
| Stuck explaining | `Explain-back [[concept]] feynman` |
| Promote | `Promote [[concept]] to solid` |
| Health | `Lint` |

## Ingest depth

| Mode | Say |
|------|-----|
| Default | `Ingest: …` |
| Lite map | `Ingest overview only: …` |
| Storage only | `archive only` |

## Connect

`Connect: <insight across concepts> — 记入 synthesis` → `wiki/notes/synthesis/`

## Example session

```
/zhuomo Query think: when use native routing vs overlay?
/zhuomo Explain-back [[cilium-datapath-modes]] cold
/zhuomo Connect: Cilium overlay vs ACI — 记入 synthesis
/zhuomo Lint
```
