# Zhuomo — simplified mode

**Six verbs:** Bootstrap · Ingest · Query · Revise · Study · Lint. Everything else is optional.

## Minimum viable Zhuomo

```
Raw  →  Bootstrap + Ingest  →  concepts + Evidence  →  Query
```

**Daily cheatsheet:** Obsidian `wiki/help.md`.

| Keep | Drop (until needed) |
|------|---------------------|
| `~/zhuomo-data/raw/` inbox | Domain skills |
| `wiki/concepts/` + Explain-back | Weekly ritual (use Lint + Study ad hoc) |
| `wiki/overview.md` + domain overviews | 10+ repo docs — read `help.md` + [REVIEW.md](REVIEW.md) |
| `wiki/sources/` + md corpus | Digests, applied journal, review logs |
| Chat with agent | — |

## Default: reference depth at bootstrap

Bootstrap + first ingest **deepen all** concepts unless you say `overview only` / `lite`.

## Lite mode (opt-in)

| Phase | Trigger | Output |
|-------|---------|--------|
| Map | `Ingest overview only: book.epub` | Stubs + topic map |
| Deepen | `Deepen all` or `Deepen tenant` | Full concepts + Evidence |
| Study | `Explain-back [[concept]]` | Interactive prompts → grade per turn → frontmatter ([REVIEW.md](REVIEW.md#interactive-explain-back-default)) |

## Ingest depth

| Mode | Say |
|------|-----|
| Default | `Ingest: …` |
| Lite map | `Ingest overview only: …` |
| Storage only | `archive only` |

## Obsidian layout

| View | Path |
|------|------|
| Vault hub | `wiki/overview.md` |
| Domain entry + **Dataview progress** | `domains/<domain>/overview.md` |
| Concept index (not full digest) | `domains/<domain>/guide.md` |
| Truth + Explain-back | `wiki/concepts/` |

Install **Dataview** plugin to see progress tables on domain overviews.

## Repo docs

| Read | Skip |
|------|------|
| `wiki/help.md` | FRAMEWORK, KNOWLEDGE-BASE (agent) |
| [REVIEW.md](REVIEW.md) | RETENTION (merged into REVIEW) |
| [USER-GUIDE.md](USER-GUIDE.md) if stuck | — |

## One-line prompts

```
/zhuomo Bootstrap + ingest: ~/zhuomo-data/raw/books/my-book.epub

/zhuomo Ingest: ~/zhuomo-data/raw/inbox/book.epub

/zhuomo Query think: Multi-Pod vs Multi-Site?

Explain-back [[aci-border-leaf-l3out]]

/zhuomo Lint

/zhuomo Learn fable: [[aci-tenant-epg-contract]]
```

Optional: `Weekly` = Lint + suggest one Explain-back (~15 min).
