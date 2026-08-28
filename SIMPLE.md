# Zhuomo — simplified mode

**Seven verbs:** Bootstrap · Ingest · Query · **外搜** · Revise · Study · Lint. **Connect** for personal notes. **Adopt vault** · **Ingest continue** · **Study continue** when resuming.

**Agent refs:** `~/zhuomo/references/` (Claim rubric, Apply, diagnosis, Lint tiers).

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

**Learn from `concepts/` Claim（知识笔记）— not the book.** Evidence → source = 按需深挖。

| Step | Say |
|------|-----|
| First learn | `Explain-back [[concept]] cold` |
| Stuck explaining | `Explain-back [[concept]] feynman` |
| Promote | `Promote [[concept]] to solid` |
| Health | `Lint` |
| Stale releases/CVE | `外搜 <domain>` |

## 外搜 (lite)

| Scope | Say |
|-------|-----|
| Whole domain | `外搜 cisco-sdwan` |
| One concept | `外搜 [[sdwan-omp-routing]]` |
| Check gaps | `Lint`（含 External 扫描；或 `lint-external-fact-check.py` 单独跑） |

Adds `External (YYYY)` to Evidence; **Claim 修正需你确认**（`确认 Claim`）后才写入 wiki。

**自动外搜：** study-technical ingest 后；Query/Study 引用页 **>180 天未 external_checked** 或缺 External 时跟进（可说 `no 外搜` 跳过）。

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
/zhuomo 外搜 cisco-sdwan
/zhuomo Explain-back [[cilium-datapath-modes]] cold
/zhuomo Connect: Cilium overlay vs ACI — 记入 synthesis
/zhuomo Lint
```
