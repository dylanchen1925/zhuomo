# 琢磨 (Zhuomo) — Reference

Extended ingest, EPUB, Readwise, and revision detail. **Agent entry point:** [SKILL.md](SKILL.md). **Study:** [REVIEW.md](REVIEW.md).

## Optional Cursor skills (not zhuomo verbs)

Zhuomo verbs compile **wiki** only (`Ingest`, `Revise`, `Query`, `Study`, `Lint`, `Connect`). Turning wiki into repeatable agent behavior is a **separate Cursor chat** step — cite `[[concepts]]` or a domain overview and ask for triggers + workflow.

| You want | Where it lives |
|----------|----------------|
| Facts, Evidence, study progress | `wiki/concepts/`, `wiki/domains/` |
| Triggers, persona, read order | `~/.cursor/skills/<name>/` (optional) |

When facts change: **Revise wiki** first. Edit skill files only if triggers or workflow changed. Optional layouts: [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md).

Full wiki setup: [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md).

## Obsidian vault (wiki output only)

**Raw local; Obsidian for what you read.**

| Store | Where | Obsidian |
|-------|-------|----------|
| Clips, EPUB, transcripts, video notes | `~/zhuomo-data/raw/` | Don't add to vault (or exclude from graph) |
| Concepts, frameworks, digests, synthesis | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen/wiki/` | **Open vault here** |

Bootstrap prompt:

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, Obsidian vault ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen
```

With first source (deepen all in one session):

```
/zhuomo Bootstrap + ingest: raw ~/zhuomo-data/raw/, vault ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen, book ~/zhuomo-data/raw/books/my-book.epub
```

**Default:** reference depth — topic map → md corpus → deepen every concept + Evidence. Opt-out: `bootstrap lite` or `overview only`.

**Source page** (in wiki, not raw) links outward:

```markdown
# Source — Condition-Based Waiting

- **Raw:** `~/zhuomo-data/raw/web/2026-05-30-condition-based-waiting.md`
- **URL:** https://… (accessed 2026-05-30)
- **Topics:** [[flaky-tests]], [[condition-based-waiting]]
```

Internet capture still lands in **local raw** first; ingest writes **only** under `wiki/`.

Multi-device: phone saves to `raw/inbox/` (iCloud/Dropbox); laptop ingests and moves to `processed/`. Wiki syncs via Obsidian Sync or iCloud; laptop owns wiki edits. Details: [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md#multi-device-sync-laptop--iphone).

### Review & Explain-back

Per-concept teach-back on `wiki/concepts/*.md` using `## Explain-back` prompts. **Default:** interactive — one question per turn, brief feedback, frontmatter at end. Spec: [REVIEW.md § Interactive explain-back](REVIEW.md#interactive-explain-back-default).

## Readwise & highlights pipeline

For Kindle, O'Reilly, Instapaper, web highlights — when full raw EPUB isn't available:

1. **Export** from Readwise (markdown) on laptop.
2. Save to `~/zhuomo-data/raw/inbox/readwise-YYYY-MM.md` (or weekly file).
3. Ingest:

```
/zhuomo Process raw/inbox/readwise-2026-05.md — ingest highlights to wiki.
```

4. Wiki source page cites Readwise export path + original book URL.
5. Optional: Readwise → Obsidian direct sync for reading only; still run zhuomo **ingest** to compile into concepts/framework.

**Don't:** treat Readwise sync alone as wiki — it's another raw snapshot until ingested.

## Topic discovery (multi-topic resources)

**Topic is not required from the user.** The agent reads the resource and determines topics. **Multiple topics per source is normal** — never force one resource into one concept page.

### When user gives a topic

Treat it as a **lens** (priority, scope, goal) — not the only topic in the material:

- "Focus on replication" → ingest replication deeply first; list other topics for later passes
- "Chapter 7 only" → deepen that cluster first; still file source summary + cross-links

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
- **Large sources** — topic map on first pass; ingest 1–2 topic clusters per session.

### Example prompts

```
/zhuomo Ingest raw/ddia.epub ch. 1 — discover topics, no lens from me.

/zhuomo Ingest this blog. I care about caching only; still list other topics at the end.

/zhuomo Here's a paper — topic map first, then ingest everything into wiki.
```

## Correcting & Updating Existing Knowledge

Zhuomo is not append-only. Existing wiki pages **must be corrected** when wrong or outdated.

### When to Revise

| Trigger | Example |
|---------|---------|
| User correction | "The wiki says X but that's wrong" |
| New source contradicts | Paper B refutes claim from Book A already in wiki |
| Stale claim | API/library changed; old procedure no longer works |
| Lint finding | Orphan, duplicate entity, untyped contradiction |

### Revision card

Fill before editing:

| Field | Capture |
|-------|---------|
| **Target** | Wiki page path(s) |
| **Problem** | wrong / stale / contradicts / duplicate / incomplete |
| **Old claim** | What the wiki currently says (quote briefly) |
| **New claim** | Corrected statement |
| **Evidence** | raw source path, URL, user statement, lint ID |
| **Propagation** | Other pages that cite the old claim |
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
```

## Source Ingestion

### Books (PDF, EPUB, pasted text)

1. Identify **scope** — whole book vs chapters (user may specify).
2. Extract text (see **EPUB** below for `.epub` files).
3. If using a knowledge base: copy original to `raw/`, **ingest to wiki** chapter-by-chapter (characters, themes, claims).
4. Scan structure: TOC, headings, recurring frameworks, named methods.
5. Copyright: paraphrase; no large verbatim blocks; cite source on wiki source page.

#### EPUB (`.epub`)

EPUB works well — it's structured HTML in a ZIP, so chapter boundaries are usually preserved.

**Workflow (required steps):**

1. Copy the `.epub` to `raw/books/` (immutable source).
2. **Convert full text to Markdown** under `wiki/sources/[slug]/md/` — one file per spine item/chapter, with heading anchors. **Images** go to `~/zhuomo-data/corpus/<slug>/assets/` (not in the vault); embed as `![alt](/corpus/<slug>/assets/…)` in part files. Requires **`{vault_root}/corpus`** → `~/zhuomo-data/corpus` symlink (Obsidian `/corpus/…` is vault root, not `wiki/`). This is the **provenance corpus**; concept pages link here, not only to the EPUB path.
3. Write `wiki/sources/[slug].md` index (topic map + link to `md/index`).
4. **Deepen all** topic-map concepts — full pages + **`## Evidence`** on each (default). Use stub-only pass only when user says `overview only`.
5. On every deepened concept page: **`## Evidence`** table — each claim row links `[[sources/slug/md/part-NNN#heading-anchor]]`.
6. Then: Study (`Explain-back`) and domain overview updates as needed.

**Convert script (repo):**

```bash
python3 scripts/epub-to-wiki-md.py raw/books/my-book.epub \
  --out ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Dylan\ Chen/wiki/sources/my-book/md \
  --slug my-book
```

Requires: `pip install ebooklib beautifulsoup4`

**PDF (`.pdf`) — chapter presets:**

```bash
python3 scripts/pdf-to-wiki-md.py raw/books/HDN.pdf \
  --preset hdn \
  --out ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Dylan\ Chen/wiki/sources/hardware-defined-networking/md \
  --slug hardware-defined-networking
```

Requires: `pdftotext` (poppler); optional `pdfimages` for PNG extraction. Add page-range presets in `scripts/pdf-to-wiki-md.py` for new books.

#### PPTX, DOCX, YouTube (MarkItDown)

Use for training decks, whitepapers, and video transcripts when EPUB/PDF presets do not apply.

**Workflow:**

1. Copy source to `raw/ppt/`, `raw/web/`, or `raw/video/` (or pass a YouTube URL / `.url` sidecar).
2. Convert to md corpus:

```bash
python3 -m pip install 'markitdown[pptx,docx]' youtube-transcript-api

python3 scripts/markitdown-to-wiki-md.py raw/ppt/cwna-deck.pptx \
  --out wiki/sources/cwna-deck/md \
  --slug cwna-deck

python3 scripts/markitdown-to-wiki-md.py 'https://www.youtube.com/watch?v=…' \
  --out wiki/sources/my-talk/md \
  --slug my-talk \
  --youtube-chunk-sec 300
```

3. Write `wiki/sources/<slug>.md` topic map; **selective deepen** concepts (same as EPUB).
4. Evidence links: `[[sources/<slug>/md/part-012#slide-title]]` or `[[…#t-0012-34]]` for YouTube timestamps.

**Split rules:**

| Input | Parts |
|-------|--------|
| **PPTX** | One part per slide (`<!-- Slide number: N -->`) |
| **DOCX** | Split on `#` headings or short title lines |
| **YouTube** | Metadata part + transcript chunks (default 300s); needs `youtube-transcript-api` for timestamps |

PPTX images extract to `/corpus/<slug>/assets/` unless `--no-images`.

**Alternative extraction options:**

```bash
# pandoc (single file or split — publisher-dependent)
pandoc book.epub -t markdown --split-level=1 -o wiki/sources/book-title/md/

# Calibre CLI (plain text fallback)
ebook-convert book.epub book.txt
```

**Concept page evidence block (required):**

```markdown
## Evidence

| 要点 | 原文 |
|------|------|
| FD_VNID mismatch F3274 | [[sources/my-book/md/part-003#vpc-consistency-checks]] |

## Sources

- **Raw EPUB:** `~/zhuomo-data/raw/books/my-book.epub`
- **MD 全文:** [[sources/my-book/md/index]]
```

### Figure visuals on wiki pages

When ingest, deepen, or revise mentions **Figure N** (or `#figure-*` anchors), embed the visual **where the figure is discussed** — not in a consolidated `## Figures` block at the end.

**Placement:**

1. **Body mention** — insert image/mermaid **immediately after** the paragraph or bullet that cites Figure N (prefer prose lines over `##` headings when both mention the same figure).
2. **Evidence-only cite** — insert under the matching thematic section (e.g. `#figure-3-4` under `## Mechanics`, scheduler figures under `## Concept`); Evidence bullet keeps the wikilink only.
3. **Never** append all figures before `## Evidence`.

**Priority (what to embed):**

1. **Source asset** — `![Figure N](/corpus/<slug>/assets/…)` from EPUB MD corpus (same image as `part-NNN.md`; files live under `~/zhuomo-data/corpus/`).
2. **Mermaid schematic** — when no asset exists or book figure is unreadable; topology/flow only; must match wiki claims.
3. **Link only** — never alone; always pair `→ [[sources/.../md/part-NNN#figure-x-y]]` with (1) or (2).

**Inline template:**

```markdown
Guide **Figure 91** = …

![Figure 91](/corpus/my-book/assets/…)

→ [[sources/…/md/part-NNN#figure-91]]
```

**Migrate existing vault assets (one-time):**

```bash
python3 ~/zhuomo/scripts/migrate-corpus-assets-out.py ~/path/to/vault/wiki --dry-run
python3 ~/zhuomo/scripts/migrate-corpus-assets-out.py ~/path/to/vault/wiki
```

**Backfill existing vault:**

```bash
python3 scripts/embed-figure-visuals.py ~/path/to/vault/wiki
```

Removes legacy `## Figures` sections and re-inlines at mention sites.

**Lint:**

```bash
python3 scripts/lint-figure-visuals.py ~/path/to/vault/wiki
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
- One technique-heavy chapter may be enough for a first ingest pass; deepen the rest later.

### Blogs and articles (URL or paste)

1. Fetch or read pasted content.
2. Capture URL, date, and which claims are author-specific vs common knowledge.
3. Ingest to wiki concepts + Evidence; optional personal notes via **Connect**.

### Videos and podcasts

1. **Preferred:** convert with MarkItDown + transcript API:

```bash
python3 scripts/markitdown-to-wiki-md.py 'https://www.youtube.com/watch?v=…' \
  --out wiki/sources/<slug>/md --slug <slug>
```

2. Or get transcript manually: user paste, auto-caption export, or summary notes.
3. Record **timestamps** in Evidence (`#t-MM-SS` anchors) and `wiki/log.md` for traceability.
4. Demos: convert to one runnable example in synthesis or concept Mechanics, not a play-by-play.

### Notes and highlights

1. Treat highlights as **pre-filtered** — still map topics before deep ingest.
2. Ask user what they highlighted *for* if ambiguous.
3. Merge duplicate highlights into one concept update where they repeat the same claim.

---
