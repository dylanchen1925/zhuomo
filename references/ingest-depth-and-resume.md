# Ingest depth, resume, and source types

**Trigger:** `Ingest: <path>`, `Ingest continue: <slug>`, ingest after Bootstrap.

---

## Source classes

| Class | Typical | Default depth |
|-------|---------|---------------|
| **study-technical** | IT, cert, RFC, ops | reference depth |
| **study-analytic** | 政经史, 社科 | reference or selective |
| **craft-narrative** | 写作/叙事技法 | reference depth |
| **literary-appreciation** | 小说诗歌消遣 | overview or archive only |
| **reference-lookup** | 手册/年鉴 | archive only |
| **transcript** | SRT/VTT/ASR 稿 | archive + transcript pipeline — see [transcript-ingest.md](transcript-ingest.md) |

### User keywords

| Keyword | Effect |
|---------|--------|
| `reference depth` / `继续` | Full deepen all topic-map rows |
| `selective deepen` / `精读` | Named themes only |
| `overview only` / `lite` | Topic map + stubs |
| `archive only` | Source + md corpus; no deepen |
| `Ingest continue: <slug>` | Resume from source `next_sections` |

---

## Decision gate

| Condition | Action |
|-----------|--------|
| Large book, no depth keyword, not confirmed | § Confirm menu — **stop** |
| Keyword or explicit small source | Proceed |
| `raw/inbox/` non-empty | Process inbox first |
| literary + no 精读 | overview/archive only |

---

## Source page frontmatter

Use [templates/wiki/source-page.md](../templates/wiki/source-page.md):

```yaml
source_class: study-technical
ingest_depth: reference
ingest_status: partial | complete | archive-only
next_sections: []
last_ingest: YYYY-MM-DD
concepts_deepened: 0
```

---

## Procedure (numbered)

```
0. Classify; write/update source page frontmatter
1. Read TOC/structure; brain-first duplicate search
2. Topic map table on sources/<slug>.md
3. Convert corpus (epub/pdf/markitdown/transcript per type)
4. Deepen per depth → `wiki/concepts/` only (Claim per [concept-claim-rubric.md](concept-claim-rubric.md); **never** `wiki/notes/`)
5. Update index, overview gaps, map.md pillars
6b. Synthesis gate offer (study-analytic / 精读 required offer)
6c. Auto 外搜 (study-technical + reference/selective) — external-fact-check.md
7. Set ingest_status:
   - all topic-map rows done → complete; clear next_sections
   - partial → partial; set next_sections + concepts_deepened count
8. log.md: ingest | title | N concepts  OR  ingest-resume | slug | sections | +N
9. Lint optional; closing block
```

### Ingest continue

```
1. Read sources/<slug>.md — ingest_status, next_sections, topic map
2. If complete → tell user; offer new selective deepen
3. Process only next_sections rows + update frontmatter
4. Same 6c 外搜 rules if study-technical deepen
```

---

## Topic map template

```markdown
## Topic map — [title]

| Topic | Evidence | Existing wiki? | Action |
|-------|----------|----------------|--------|
| … | ch./§/time | [[…]] or — | Create / Update / Merge |
```

---

## Confirm menu

```markdown
**类型：** [class] · **推荐档位：** [depth] — [理由]
**计划：** topic map → md → [deepen N | synthesis | 语料 only]
回复 **继续** / **overview only** / **archive only** / **selective deepen [[x]]** / **精读**
```

---

## Figure rule

Inline `![Figure N](…)` at first mention + source link. Never bare "see Figure N".  
Backfill: `embed-figure-visuals.py`.
