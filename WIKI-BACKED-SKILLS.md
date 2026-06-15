# Wiki-Backed Domain Skills

A **domain skill** makes an agent *think and act* like an expert. The **wiki** is the knowledge backend — facts, synthesis, contradictions, frameworks. The skill holds **triggers, workflow, and scope** — not a copy of the wiki.

Example: `network-expert` skill + your BGP/Ospf wiki pages → agent loads wiki at invoke time, reasons with citations, follows expert workflow.

## Two skill types (both from zhuomo)

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
- [[domains/networking/index.md]]

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
4. After solving a novel case, offer to **Revise** the concept or file synthesis in `wiki/synthesis/`.
```

### SOURCES.md

```markdown
| Backend | Path | Role |
|---------|------|------|
| Wiki domain | `wiki/domains/networking/` | Framework + index |
| Wiki concepts | `wiki/concepts/bgp.md`, … | Facts + synthesis |
| Raw evidence | `~/zhuomo-data/raw/books/…` | Provenance only — don't load unless verifying |
```

## Invoke workflow

```
Trigger matches domain skill
    → Read WIKI-SCOPE.md
    → Load domain overview + relevant concept pages (don't load entire vault)
    → Apply SKILL.md reasoning workflow
    → Answer citing wiki; flag gaps/contested/stale
    → Optional: propose Revise or applied/ journal entry
```

Domain skills **must not** cache wiki text inside SKILL.md — wiki Revise updates backend without redeploying skill unless workflow changes.

## Creating a domain skill from wiki (zhuomo)

After ingesting a domain (e.g. networking / BGP):

```
/zhuomo Domain skill: network-expert — wiki backend wiki/domains/networking/ + BGP concepts. WIKI-SCOPE manifest only; no fact dump in SKILL.md.
```

Checklist:

- [ ] Domain overview exists (`wiki/domains/[slug]/overview.md`)
- [ ] Key concept pages exist and linked from overview
- [ ] WIKI-SCOPE.md lists always-read + topic routing table
- [ ] SKILL.md: triggers (symptoms), persona, workflow, anti-patterns
- [ ] SOURCES.md lists wiki paths
- [ ] RED: ask network question **without** skill — note generic/wrong patterns
- [ ] GREEN: skill + wiki scope — agent must cite wiki, respect epistemic tags

## Wiki concept page hooks for domain skills

On concept pages, optional backlink:

```markdown
Related domain skill: `~/.cursor/skills/network-expert`
```

On `overview.md`:

```markdown
## Domain skill
Agent persona: [[~/.cursor/skills/network-expert]] — loads this overview first.
```

## When to Revise vs update skill

| Change | Action |
|--------|--------|
| BGP fact wrong | **Revise** wiki only |
| New BGP concept ingested | Wiki + update WIKI-SCOPE table row |
| Expert workflow changed (new debug order) | Update SKILL.md; RED if discipline |
| Wiki domain split (BGP vs DC) | Update WIKI-SCOPE routing; skill name may stay |

## Example prompts

```
/zhuomo Create domain skill network-expert backed by my networking wiki.

/zhuomo Update WIKI-SCOPE for network-expert — I added [[concepts/bgp-communities]].

/zhuomo Debug this BGP flap — use network-expert skill (load wiki first).
```
