# Wiki-Backed Domain Skills

> **Not a zhuomo verb.** Zhuomo `Ingest` / `Revise` / `Query` / `Study` / `Lint` / `Connect` compile **wiki** only. To add agent behavior, open a **separate Cursor chat**, cite `[[concepts]]` or a domain overview, and ask for files under `~/.cursor/skills/`. This doc is an optional layout reference.

A **domain skill** makes an agent *think and act* like an expert. The **wiki** is the knowledge backend. The skill holds **triggers, workflow, and scope** — not a copy of the wiki.

Example: `network-expert` skill + your BGP/OSPF wiki pages → agent reads wiki at invoke time, reasons with citations, follows an expert workflow.

## Two skill types (optional)

| Type | Holds | Wiki role |
|------|-------|-----------|
| **Technique skill** | One trigger + workflow (TDD, condition-based waiting) | Optional link to concept page |
| **Domain skill** | Persona + reasoning mode + scope manifest | **Primary backend** — read on every invoke |

Technique skills distill *behavior*. Domain skills *consult* wiki *then* behave.

## Domain skill layout

```
~/.cursor/skills/network-expert/
├── SKILL.md           # triggers, persona, workflow (required)
├── WIKI-SCOPE.md      # which wiki to load, how (required for domain skills)
├── REFERENCE.md       # decision trees / checklists not yet in wiki (optional)
└── SOURCES.md         # wiki paths + raw provenance (required)
```

### SKILL.md (domain)

Keep lean. No BGP textbook in the skill.

```yaml
---
name: network-expert
description: Use when designing, debugging, or reviewing network architecture, routing, BGP, datacenter fabric, or when the user asks to think like a senior network engineer.
---
```

Body: persona constraints, reasoning steps, anti-patterns, **pointer to WIKI-SCOPE.md**. Never paste wiki content wholesale.

### WIKI-SCOPE.md (manifest)

Tells the agent **what to read** from the vault before answering.

```markdown
# Wiki scope — network-expert

Vault: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen/wiki/`

## Always read first
- [[domains/networking/overview.md]]
- [[domains/networking/guide.md]]

## Load by topic (open if question touches)
| Topic signal | Wiki pages |
|--------------|------------|
| BGP, peering, AS path | [[concepts/bgp]], [[concepts/bgp-path-selection]] |
| OSPF, IGP | [[concepts/ospf]], [[concepts/area-design]] |
| Datacenter Clos | [[concepts/clos-fabric]], [[synthesis/dc-routing]] |

## Tags (grep frontmatter if many pages)
`domain: networking`

## Rules
1. Prefer **established** claims over **tentative** (see concept frontmatter).
2. If wiki **contested**, present both sides; don't flatten.
3. Cite wiki page names in reasoning; if wiki gap, say so and suggest ingest.
4. After solving a novel case, offer to **Revise** the concept or **Connect** a personal synthesis note.
```

### SOURCES.md

```markdown
| Backend | Path | Role |
|---------|------|------|
| Wiki domain | `wiki/domains/networking/` | Framework + index |
| Wiki concepts | `wiki/concepts/bgp.md`, … | Facts + Evidence |
| Raw evidence | `~/zhuomo-data/raw/books/…` | Provenance only — don't load unless verifying |
```

## Invoke workflow

```
Trigger matches domain skill
    → Read WIKI-SCOPE.md
    → Load domain overview + relevant concept pages (don't load entire vault)
    → Apply SKILL.md reasoning workflow
    → Answer citing wiki; flag gaps/contested/stale
    → Optional: propose Revise or Connect
```

Domain skills **must not** cache wiki text inside SKILL.md — wiki **Revise** updates facts without redeploying the skill unless triggers or workflow changed.

## Creating via chat (after wiki ingest)

Prerequisites: domain overview + key concept pages exist.

**Example prompt:**

```
根据 wiki/domains/networking/overview.md 和其中 BGP 相关 [[concepts]]，
在 ~/.cursor/skills/network-expert/ 创建 domain skill：
- SKILL.md：触发词、persona、推理步骤、反模式
- WIKI-SCOPE.md：always-read 列表 + 按话题路由表
- SOURCES.md：wiki 路径与 raw 出处
不要把 wiki Claim/Evidence 全文复制进 skill。
```

**Checklist:**

- [ ] Domain overview exists (`wiki/domains/<slug>/overview.md`)
- [ ] Key concept pages linked from overview
- [ ] WIKI-SCOPE.md lists always-read + topic routing table
- [ ] SKILL.md: triggers (symptoms), persona, workflow, anti-patterns
- [ ] SOURCES.md lists wiki paths
- [ ] Smoke test: ask a domain question with skill enabled — agent cites wiki, respects `epistemic` tags

## Optional wiki hooks

On concept pages:

```markdown
Related skill (optional): `~/.cursor/skills/network-expert`
```

On `overview.md`:

```markdown
## Optional agent skill
`~/.cursor/skills/network-expert` — see WIKI-SCOPE.md for read order.
```

## When to Revise wiki vs edit skill

| Change | Action |
|--------|--------|
| Fact wrong on concept page | **Revise** wiki only |
| New concept ingested | Wiki + add row to WIKI-SCOPE routing table |
| Expert workflow changed (new debug order) | Edit skill `SKILL.md` |
| Wiki domain split (BGP vs DC) | Update WIKI-SCOPE routing; skill name may stay |

## Example prompts

```
根据 [[cilium-datapath-modes]] 写 technique skill，触发词「Cilium 路由模式」。

我加了 [[concepts/bgp-communities]]，请更新 ~/.cursor/skills/network-expert/WIKI-SCOPE.md 路由表。

用 network-expert skill 分析这个 BGP flap（先读 wiki 再回答）。
```
