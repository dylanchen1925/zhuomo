# Transcript ingest (SRT / VTT / ASR)

**Trigger:** `Ingest: *.srt`, `*.vtt`, 字幕, 转写稿.

**Class:** `transcript` (may also be study-technical content if user says deepen).

---

## Default (no extra keywords)

1. **Clean:** remove clear ads / off-topic inserts; keep recoverable timestamps optional in metadata block
2. **Correct:** fix obvious ASR errors when context confirms; restore paragraphs
3. **Write:** full text → `sources/<slug>/md/` (article-style sections)
4. **Source page:** `source_class: transcript`, `ingest_status: archive-only` or `complete` if only archiving
5. **Do NOT** auto-generate concept 知识笔记 or Explain-back
6. log.md: `ingest-transcript | title | md corpus`

User says **沉淀知识** / **deepen** / **提炼概念** → run normal topic map + Claim deepen on cleaned text.

---

## Pipeline

```bash
# Optional deterministic prep
python3 ~/zhuomo/scripts/transcript-to-wiki-md.py <input.srt> <vault>/wiki/sources/<slug>/md/
```

Agent still: topic map, classification, deepen if requested.

---

## vs video URL

- **Has SRT/VTT body** → this reference (not source-ingestion web fetch first)
- **URL only** → `markitdown-to-wiki-md.py` or manual fetch per REFERENCE.md

---

## Figure / speaker labels

Preserve `[Speaker]` / `[00:12:34]` when useful for Evidence anchors; strip for readable prose sections.
