# 琢磨 (Zhuomo) — Reference

## Wiki + Skill Together

| Stage | Wiki | Skill |
|-------|--------------|-------|
| Reading a book chapter | Entity/theme pages, plot/thesis threads | Techniques with triggers |
| Research paper | Methods, claims, citations, contradictions | Reusable method if non-default |
| Blog with one trick | Source summary + links | Often skill-only if small |
| Ongoing domain (months) | Primary home for synthesis | **Domain skill** + WIKI-SCOPE, or technique skills as patterns stabilize |
| Expert persona (BGP, etc.) | Concepts + framework = backend | Domain skill loads wiki at invoke — [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md) |

Full wiki setup and operations: [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md).

## Obsidian vault (wiki output only)

**Raw local; Obsidian for what you read.**

| Store | Where | Obsidian |
|-------|-------|----------|
| Clips, EPUB, transcripts, video notes | `~/zhuomo-data/raw/` | Don't add to vault (or exclude from graph) |
| Concepts, frameworks, digests, synthesis | `~/Obsidian/zhuomo-vault/wiki/` | **Open vault here** |

Bootstrap prompt:

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, Obsidian vault ~/Obsidian/zhuomo-vault/wiki/, AGENTS.md in vault root.
```

**Source page** (in wiki, not raw) links outward:

```markdown
# Source — Condition-Based Waiting

- **Raw:** `~/zhuomo-data/raw/web/2026-05-30-condition-based-waiting.md`
- **URL:** https://… (accessed 2026-05-30)
- **Topics:** [[flaky-tests]], [[condition-based-waiting]]
```

Internet capture still lands in **local raw** first; ingest writes **only** under `wiki/`.

Multi-device: phone saves to `raw/inbox/` (iCloud/Dropbox); laptop ingests and moves to `processed/`. Wiki syncs via Obsidian Sync or iCloud; laptop owns wiki edits. Details: [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md#multi-device-sync-laptop--iphone).

### Obsidian Spaced Repetition (recall cards)

Install **[Spaced Repetition](https://github.com/st3v3nmw/obsidian-spaced-repetition)** (st3v3nmw). Zhuomo writes cards under `wiki/learn/recall/` with `#flashcards/[domain]` tags and `::` / `?` syntax. Plugin owns scheduling. Details: [RETENTION.md](RETENTION.md).

## Readwise & highlights pipeline

For Kindle, O'Reilly, Instapaper, web highlights — when full raw EPUB isn't available:

1. **Export** from Readwise (markdown) on laptop.
2. Save to `~/zhuomo-data/raw/inbox/readwise-YYYY-MM.md` (or weekly file).
3. Ingest:

```
/zhuomo Process raw/inbox/readwise-2026-05.md — ingest to wiki, recall cards for ★ highlights only.
```

4. Wiki source page cites Readwise export path + original book URL.
5. Optional: Readwise → Obsidian direct sync for reading only; still run zhuomo **ingest** to compile into concepts/framework.

**Don't:** treat Readwise sync alone as wiki — it's another raw snapshot until ingested.

## Topic discovery (multi-topic resources)

**Topic is not required from the user.** The agent reads the resource and determines topics. **Multiple topics per source is normal** — never force one resource into one concept page.

### When user gives a topic

Treat it as a **lens** (priority, scope, goal) — not the only topic in the material:

- "Focus on replication" → ingest replication deeply first; list other topics for later passes
- "Skill for chapter 7 only" → scope extraction; still file source summary + cross-links

### When user gives no topic

1. **Structure pass** — TOC, headings, intro/conclusion, chapter titles, timestamps (video).
2. **Topic map** — list distinct topics before deep ingest:

```markdown
## Topic map — [source title]

| Topic | Evidence (section/ch.) | Existing wiki page? | Action |
|-------|------------------------|---------------------|--------|
| Event sourcing | Ch. 3–4 | [[event-sourcing]] | Update |
| CQRS | Ch. 5 | — | Create |
| … | … | … | … |
```

3. **Confirm if ambiguous** — new domain, overlaps existing pages, or user goal unclear. Otherwise proceed.
4. **Ingest by topic cluster** — update/create concept pages; one source page links to all.

### Rules

- **Search wiki first** — map discovered topics to existing pages; Revise/merge don't duplicate.
- **Granularity** — one concept page per distinct idea; split chapters that cover unrelated topics.
- **Skills** — usually **one skill per technique**, not one skill per book; a multi-topic book may yield 0–N skills after filter.
- **Large sources** — topic map on first pass; ingest 1–2 topic clusters per session.

### Example prompts

```
/zhuomo Ingest raw/ddia.epub ch. 1 — discover topics, no lens from me.

/zhuomo Ingest this blog. I care about caching only; still list other topics at the end.

/zhuomo Here's a paper — topic map first, then ingest everything into wiki.
```

## Correcting & Updating Existing Knowledge

Zhuomo is not append-only. Existing wiki pages and skills **must be corrected** when wrong or outdated.

### When to Revise

| Trigger | Example |
|---------|---------|
| User correction | "The wiki says X but that's wrong" |
| New source contradicts | Paper B refutes claim from Book A already in wiki |
| Stale claim | API/library changed; old procedure no longer works |
| Lint finding | Orphan, duplicate entity, untyped contradiction |
| Skill drift | Skill contradicts updated wiki or user practice |

### Revision card

Fill before editing:

| Field | Capture |
|-------|---------|
| **Target** | Wiki page path(s) and/or skill path |
| **Problem** | wrong / stale / contradicts / duplicate / incomplete |
| **Old claim** | What the wiki/skill currently says (quote briefly) |
| **New claim** | Corrected statement or behavior |
| **Evidence** | raw source path, URL, user statement, lint ID |
| **Propagation** | Other pages/skills that cite the old claim |
| **Action** | edit / supersede / merge / retract / split |

### Wiki revision workflow

1. Read target page + all backlinks (pages linking to it).
2. If **duplicate**: pick canonical page; merge content; redirect wikilinks; archive duplicate.
3. If **contradiction**: don't leave both claims as true — resolve with user if needed, then:
   - Update synthesis to reflect tension, or
   - Supersede old page, or
   - Add explicit `contradicts` / `supersedes` relation in prose.
4. Update `index.md` one-line summary if scope changed.
5. Append `log.md` revise entry.

Optional frontmatter after revise:

```yaml
---
status: active          # active | stale | superseded | archived
updated: 2026-05-30
supersedes: [[old-page]]
sources: [raw/paper-b.pdf]
---
```

### Skill revision workflow

1. Read SKILL.md, REFERENCE.md, SOURCES.md + linked wiki pages.
2. Apply revision card — skills get **behavioral** fixes only (triggers, steps, anti-patterns).
3. **Enhance** vs **correct**:
   - Enhance = net-new from another source
   - Correct = fix wrong/outdated step or trigger
4. Append SOURCES.md row documenting the correction.
5. **Re-run RED** if the correction changes a discipline rule or core workflow.

### Ingest + Revise together

Every ingest must include a **contradiction pass**:

```
Search index for related concepts → read existing pages →
if new source conflicts → Revise before marking ingest complete
```

### Example prompts

```
/zhuomo Revise wiki/concepts/event-sourcing.md — user says we use Kafka not RabbitMQ.
Propagate to all pages linking to it.

/zhuomo New paper in raw/ contradicts our synthesis on CAP theorem. Revise affected pages.

/zhuomo Lint found duplicate pages "CQRS" and "Command Query Separation". Merge them.

/zhuomo Update skill ~/.cursor/skills/tdd/ — step 3 is outdated after our wiki revise.
```

## Source Ingestion

### Books (PDF, EPUB, pasted text)

1. Identify **scope** — whole book vs chapters (user may specify).
2. Extract text (see **EPUB** below for `.epub` files).
3. If using a knowledge base: copy original to `raw/`, **ingest to wiki** chapter-by-chapter (characters, themes, claims).
4. Scan structure: TOC, headings, recurring frameworks, named methods.
5. Prefer **frameworks and named techniques** for skills; **entities and synthesis** for wiki.
6. Copyright: paraphrase; no large verbatim blocks; cite source in SOURCES.md and wiki source page.

#### EPUB (`.epub`)

EPUB works well — it's structured HTML in a ZIP, so chapter boundaries are usually preserved.

**Workflow:**

1. Copy the `.epub` to `raw/` (immutable source).
2. Extract text **by chapter** (don't ingest the whole book in one pass unless it's short).
3. Run the normal pipeline: wiki ingest → extraction card → zhuomo to skill.

**Extraction options** (pick one available on the machine):

```bash
# Option A — pandoc (best chapter structure as markdown)
pandoc book.epub -t markdown --split-level=1 -o wiki/sources/book-title/

# Option B — Calibre CLI (plain text, one file or per-chapter)
ebook-convert book.epub book.txt

# Option C — unzip + read XHTML (no extra tools; EPUB is a zip)
unzip -l book.epub   # find OEBPS/*.xhtml or similar spine files
unzip -j book.epub 'OEBPS/chapter*.xhtml' -d /tmp/book-chapters/
```

Python (when scripting ingest):

```python
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

book = epub.read_epub("raw/book.epub")
for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    soup = BeautifulSoup(item.get_content(), "html.parser")
    text = soup.get_text("\n", strip=True)
    # process per spine item / chapter
```

**Tips:**

- Use the EPUB **TOC/spine order**, not filename order, for chapter sequence.
- DRM-protected EPUBs must be decrypted by the user first; the skill only reads unlocked files.
- Footnotes/endnotes often live in separate XHTML files — merge or link in wiki, don't drop silently.
- For zhuomo to skill, one technique-heavy chapter may be enough; you don't need the whole book.

### Blogs and articles (URL or paste)

1. Fetch or read pasted content.
2. Often **one technique → one skill** or **one section → enhancement**.
3. Capture URL, date, and which claims are author-specific vs common knowledge.
4. Blog posts with code: put long API detail in REFERENCE.md, triggers in SKILL.md.

### Videos and podcasts

1. Get transcript: user paste, auto-caption export, or summary notes.
2. Record **timestamps** in SOURCES.md for traceability.
3. Videos often mix story + technique — apply extraction card aggressively.
4. Demos: convert to one runnable example, not a play-by-play.

### Notes and highlights

1. Treat highlights as **pre-filtered** — still run Filter step (actionable + non-default).
2. Ask user what they highlighted *for* if ambiguous.
3. Merge duplicate highlights into one trigger/workflow.

### Multiple sources → one skill

- First source: establish skill skeleton (name, core triggers, primary workflow).
- Later sources: **enhancement pass only** — net-new triggers, steps, anti-patterns, examples.
- If a new source contradicts the skill, resolve with user; update or split, don't silently merge.

## Enhancing or Correcting an Existing Skill

**Enhance** = add net-new from a source. **Correct** = fix wrong/outdated content.

1. **Read** current SKILL.md, REFERENCE.md, SOURCES.md + linked wiki pages.
2. **Diff mentally:** net-new vs correction vs contradiction?
3. **Merge rules:**
   - Same idea, clearer wording → replace, don't duplicate
   - New trigger → add to description keywords + body
   - New step → insert in workflow where it belongs
   - Contradiction → user decision; Revise wiki first; ADR note in SOURCES.md
4. **Keep SKILL.md lean** — move new bulk to REFERENCE.md.
5. **Re-run validation** if correction changes discipline rules or core workflow:
   - Discipline addition → new RED scenario for that rule
   - Technique tweak → re-run application scenario
6. **Append SOURCES.md** row; never delete prior source rows.

## Skill Directory Layout

**Technique skill:**

```
skill-name/
├── SKILL.md        # Triggers, workflow, checklist (required)
├── REFERENCE.md    # Heavy detail, optional
├── SOURCES.md      # Provenance (required)
└── EXAMPLES.md     # Optional pressure scenarios / usage
```

**Domain skill (wiki backend):**

```
network-expert/
├── SKILL.md        # Persona, triggers, workflow (required)
├── WIKI-SCOPE.md   # Vault paths, topic routing table (required)
├── REFERENCE.md    # Checklists not yet in wiki (optional)
└── SOURCES.md      # Wiki paths + raw provenance (required)
```

See [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md).

## Description (CSO) from Book Material

Book titles and chapter names are bad triggers. Convert to **symptoms and situations**:

| Book language | Skill description language |
|---------------|----------------------------|
| "Chapter 7: Dealing with Legacy Code" | "Use when changing code without tests, seam-finding, or safe refactoring constraints" |
| "The Art of X" | "Use when [specific failure mode X was meant to prevent]" |

Description template:

```yaml
description: Use when [symptom/situation A], [symptom B], or [context C].
```

Never include the zhuomo workflow in the description.

## Splitting One Book Into Multiple Skills

Split when:

- Triggers belong to different domains (e.g. "testing" vs "deployment")
- Combined SKILL.md would exceed ~100 lines of distinct workflows
- Description would need "or" more than twice for unrelated situations

Keep a lightweight index in SOURCES.md:

```markdown
## Related skills from same source
- `characterization-tests` — Ch. 9–11
- `seam-based-refactoring` — Ch. 12–15
```

## Validation Scenarios by Type

### Discipline (from books like TDD, clean code rules)

Pressure template:

```markdown
IMPORTANT: Real scenario. Choose and act.

[Concrete task with sunk cost, time pressure, authority, or exhaustion]
[Option that violates the book's rule looks attractive]

What do you do?
```

Document verbatim rationalizations from RED; each gets a counter in REFACTOR.

### Technique (how-to chapters)

Give a novel situation not copied from the book. Agent must pick the book's method over a generic alternative.

### Pattern (mental models)

Present two similar problems; agent must identify which matches the pattern and which doesn't.

### Reference (appendix, API chapters)

Ask for a specific fact or procedure; verify agent finds it in REFERENCE.md and applies correctly.

## Example: Mini Zhuomo

**Source:** Blog post "Condition-Based Waiting for Flaky Tests"

**Extracted (not shipped as summary):**

| Field | Content |
|-------|---------|
| Trigger | Tests pass/fail inconsistently; uses sleep/setTimeout |
| Core move | Wait on observable condition, not time |
| Anti-pattern | Increasing timeout blindly |
| Type | technique |

**RED:** Agent adds `sleep(5000)` to flaky test.

**GREEN:** Skill with trigger keywords "flaky", "race condition", "timing".

**SOURCES.md:** URL, date refined.
