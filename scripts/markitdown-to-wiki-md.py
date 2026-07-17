#!/usr/bin/env python3
"""Convert PPTX, DOCX, or YouTube sources to per-part Markdown under wiki/sources/<slug>/md/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from corpus_assets import DEFAULT_CORPUS_ROOT, corpus_root_from_arg

SLIDE_MARKER_RE = re.compile(r"<!--\s*Slide number:\s*(\d+)\s*-->", re.I)
YOUTUBE_WATCH_RE = re.compile(
    r"^https?://(www\.)?youtube\.com/watch\?",
    re.I,
)
YOUTUBE_SHORT_RE = re.compile(
    r"^https?://(www\.)?youtu\.be/[\w-]+",
    re.I,
)
HEADING_ANCHOR_RE = re.compile(r"^#{1,6}\s+(.+?)\s+\{#([\w-]+)\}\s*$")
MARKDOWN_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")


def slugify(text: str, max_len: int = 80) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text or "section")[:max_len]


def normalize_youtube_url(url: str) -> str:
    url = url.strip()
    if YOUTUBE_WATCH_RE.match(url):
        return url
    m = re.match(r"^https?://(?:www\.)?youtu\.be/([\w-]+)", url, re.I)
    if m:
        return f"https://www.youtube.com/watch?v={m.group(1)}"
    return url


def read_url_sidecar(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.upper().startswith("URL="):
            return line.split("=", 1)[1].strip()
        if line.startswith("http://") or line.startswith("https://"):
            return line
    return None


def resolve_source(raw: str) -> tuple[str, Path | None]:
    """Return (source_for_markitdown, optional local path for provenance)."""
    if YOUTUBE_WATCH_RE.match(raw) or YOUTUBE_SHORT_RE.match(raw):
        return normalize_youtube_url(raw), None

    path = Path(raw).expanduser()
    if path.is_file():
        if path.suffix.lower() == ".url":
            url = read_url_sidecar(path)
            if not url:
                raise ValueError(f"No URL found in sidecar file: {path}")
            return resolve_source(url)
        return str(path.resolve()), path.resolve()

    raise FileNotFoundError(f"Source not found: {raw}")


def detect_kind(source: str, local: Path | None) -> str:
    if YOUTUBE_WATCH_RE.match(source) or YOUTUBE_SHORT_RE.match(source):
        return "youtube"
    if local is not None:
        ext = local.suffix.lower()
        if ext == ".pptx":
            return "pptx"
        if ext == ".docx":
            return "docx"
    raise ValueError(f"Unsupported source type: {source}")


def convert_markdown(source: str, *, keep_data_uris: bool) -> tuple[str, str | None]:
    try:
        from markitdown import MarkItDown
    except ImportError as exc:
        raise SystemExit(
            "markitdown is required: python3 -m pip install 'markitdown[pptx,docx]'"
        ) from exc

    md_engine = MarkItDown()
    kwargs = {}
    if keep_data_uris:
        kwargs["keep_data_uris"] = True
    result = md_engine.convert(source, **kwargs)
    markdown = (result.markdown or result.text_content or "").strip()
    title = getattr(result, "title", None)
    return markdown, title


def add_heading_anchors(md: str) -> str:
    out: list[str] = []
    seen: dict[str, int] = {}
    for line in md.splitlines():
        if HEADING_ANCHOR_RE.match(line):
            out.append(line)
            continue
        m = MARKDOWN_HEADING_RE.match(line)
        if not m:
            out.append(line)
            continue
        hashes, title = m.group(1), m.group(2).strip()
        base = slugify(title)
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchor = base if count == 0 else f"{base}-{count + 1}"
        out.append(f"{hashes} {title} {{#{anchor}}}")
    return "\n".join(out)


def first_heading_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        m = HEADING_ANCHOR_RE.match(line.strip())
        if m:
            return m.group(1)
        m = MARKDOWN_HEADING_RE.match(line.strip())
        if m:
            return m.group(2).strip()
    return fallback


def split_pptx(md: str) -> list[tuple[str, str]]:
    markers = list(SLIDE_MARKER_RE.finditer(md))
    if not markers:
        return [("Document", md)]

    parts: list[tuple[str, str]] = []
    for i, match in enumerate(markers):
        slide_num = int(match.group(1))
        start = match.end()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(md)
        body = md[start:end].strip()
        if len(body) < 40:
            continue
        title = first_heading_title(body, f"Slide {slide_num}")
        parts.append((title, body))
    return parts or [("Document", md)]


def split_docx(md: str, *, min_part_chars: int) -> list[tuple[str, str]]:
    chunks = re.split(r"(?=\n# )", "\n" + md.strip())
    chunks = [c.strip() for c in chunks if c.strip()]
    if len(chunks) > 1:
        parts: list[tuple[str, str]] = []
        for chunk in chunks:
            title = first_heading_title(chunk, "Section")
            if len(chunk) >= min_part_chars:
                parts.append((title, chunk))
            elif parts:
                prev_title, prev_body = parts[-1]
                parts[-1] = (prev_title, prev_body + "\n\n" + chunk)
            else:
                parts.append((title, chunk))
        return parts

    # Fallback: short title lines followed by paragraphs (publisher-style).
    lines = md.splitlines()
    sections: list[tuple[str, list[str]]] = []
    current_title = "Document"
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines, current_title
        body = "\n".join(current_lines).strip()
        if len(body) >= min_part_chars:
            sections.append((current_title, body.splitlines()))
        elif sections:
            sections[-1][1].extend(["", body])
        elif body:
            sections.append((current_title, body.splitlines()))
        current_lines = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        next_line = lines[j].strip() if j < len(lines) else ""
        if (
            line
            and not line.startswith("#")
            and len(line) < 100
            and not line.endswith(".")
            and not line.endswith(":")
            and next_line
            and len(next_line) > 80
            and re.match(r"^[A-Za-z0-9]", line)
        ):
            flush()
            current_title = line
            i = j
            continue
        current_lines.append(lines[i])
        i += 1
    flush()

    if len(sections) > 1:
        return [(title, "\n".join(body_lines)) for title, body_lines in sections]

    return [("Document", md)]


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def youtube_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    if "youtu.be" in parsed.netloc:
        vid = parsed.path.lstrip("/").split("/")[0]
        return vid or None
    params = parse_qs(parsed.query)
    if "v" in params and params["v"]:
        return params["v"][0]
    return None


def fetch_youtube_transcript(url: str) -> list[tuple[float, str]] | None:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return None

    video_id = youtube_video_id(url)
    if not video_id:
        return None

    api = YouTubeTranscriptApi()
    try:
        transcript = api.fetch(video_id)
    except Exception:
        return None

    entries: list[tuple[float, str]] = []
    for item in transcript:
        if hasattr(item, "start"):
            start = float(item.start)
            text = str(item.text).strip()
        elif isinstance(item, dict):
            start = float(item.get("start", 0))
            text = str(item.get("text", "")).strip()
        else:
            continue
        if text:
            entries.append((start, text))
    return entries or None


def split_youtube_metadata(md: str) -> tuple[str, str]:
    """Return (metadata_md, remainder_md)."""
    transcript_idx = md.find("\n### Transcript")
    if transcript_idx >= 0:
        return md[:transcript_idx].strip(), md[transcript_idx:].strip()
    return md.strip(), ""


def transcript_to_parts(
    entries: list[tuple[float, str]],
    *,
    chunk_seconds: int,
) -> list[tuple[str, str]]:
    if not entries:
        return []

    parts: list[tuple[str, str]] = []
    chunk_start = entries[0][0]
    lines: list[str] = []
    part_index = 1

    def flush(end_time: float) -> None:
        nonlocal lines, chunk_start, part_index
        if not lines:
            return
        start_label = format_timestamp(chunk_start)
        end_label = format_timestamp(end_time)
        anchor = slugify(f"transcript-{start_label}-{end_label}")
        header = f"# Transcript {start_label}–{end_label} {{#{anchor}}}"
        parts.append((f"Transcript {start_label}–{end_label}", header + "\n\n" + "\n\n".join(lines)))
        lines = []
        part_index += 1

    last_end = chunk_start
    for start, text in entries:
        if start - chunk_start >= chunk_seconds and lines:
            flush(last_end)
            chunk_start = start
        ts = format_timestamp(start)
        anchor = slugify(f"t-{ts}")
        lines.append(f"### [{ts}] {{#{anchor}}}\n{text}")
        last_end = start

    flush(last_end)
    return parts


def split_youtube(
    md: str,
    url: str,
    *,
    chunk_seconds: int,
    min_part_chars: int,
) -> list[tuple[str, str]]:
    metadata, _legacy_transcript = split_youtube_metadata(md)
    parts: list[tuple[str, str]] = []

    if len(metadata.strip()) >= min_part_chars:
        title = first_heading_title(metadata, "Video metadata")
        parts.append((title, metadata))

    entries = fetch_youtube_transcript(url)
    if entries:
        parts.extend(transcript_to_parts(entries, chunk_seconds=chunk_seconds))
        return parts

    if _legacy_transcript and len(_legacy_transcript) >= min_part_chars:
        parts.append(("Transcript", _legacy_transcript))
    return parts or [("Video", md)]


def rewrite_data_uri_images(md: str, assets_dir: Path, slug: str) -> str:
    """Extract data: URIs to corpus assets; rewrite markdown image refs."""
    from corpus_assets import asset_vault_path

    assets_dir.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(
        r"!\[([^\]]*)\]\(data:([^;]+);base64,([^)]+)\)",
        re.DOTALL,
    )
    counter = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        import base64

        alt = match.group(1)
        mime = match.group(2)
        ext = ".png" if "png" in mime else ".jpg"
        fname = f"img-{counter:04d}{ext}"
        dest = assets_dir / fname
        dest.write_bytes(base64.b64decode(match.group(3)))
        return f"![{alt}]({asset_vault_path(slug, fname)})"

    return pattern.sub(repl, md)


def write_corpus(
    *,
    source_label: str,
    raw_path: Path | None,
    slug: str,
    kind: str,
    parts: list[tuple[str, str]],
    out_dir: Path,
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "---",
        "type: source-md-corpus",
        f"converter: markitdown-to-wiki-md.py",
        f"kind: {kind}",
        f"raw: {raw_path or source_label}",
        "---",
        "",
        f"# Markdown corpus — {slug}",
        "",
        "Converted for provenance links. Concept pages cite `[[md/part-NNN#heading]]`.",
        "",
        "| Part | File | Title | First headings |",
        "|------|------|-------|----------------|",
    ]

    written = 0
    for part_num, (title, body) in enumerate(parts, start=1):
        body = add_heading_anchors(body.strip())
        if not body.startswith("#"):
            body = f"# {title}\n\n{body}"
        fname = f"part-{part_num:03d}.md"
        (out_dir / fname).write_text(body + "\n", encoding="utf-8")
        written += 1
        headings = re.findall(r"^#{1,6}\s+(.+?)(?:\s+\{#|$)", body, flags=re.MULTILINE)
        preview = "; ".join(h.strip() for h in headings[:3])
        index_lines.append(
            f"| {part_num} | [[md/{fname}\\|{fname}]] | {title[:80]} | {preview[:120]} |"
        )

    index_lines.extend(
        [
            "",
            "## Provenance link format",
            "",
            "```markdown",
            "## Evidence",
            "| 要点 | 原文 |",
            "|------|------|",
            f"| Slide notes | [[md/part-001#notes]] |",
            "```",
            "",
        ]
    )
    (out_dir / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
    return written


def main() -> int:
    parser = argparse.ArgumentParser(
        description="PPTX / DOCX / YouTube → wiki/sources/<slug>/md/",
    )
    parser.add_argument(
        "source",
        help="Path to .pptx/.docx/.url, or YouTube watch URL",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory, e.g. wiki/sources/my-deck/md",
    )
    parser.add_argument("--slug", type=str, default="", help="Source slug for index and assets")
    parser.add_argument(
        "--corpus-root",
        type=Path,
        default=DEFAULT_CORPUS_ROOT,
        help=f"External corpus root (default: {DEFAULT_CORPUS_ROOT})",
    )
    parser.add_argument(
        "--youtube-chunk-sec",
        type=int,
        default=300,
        help="YouTube transcript chunk size in seconds (default: 300)",
    )
    parser.add_argument(
        "--min-part-chars",
        type=int,
        default=80,
        help="Skip or merge parts shorter than this (default: 80)",
    )
    parser.add_argument(
        "--keep-data-uris",
        action="store_true",
        help="Keep base64 images in markdown (default: extract to /corpus/ for PPTX)",
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Do not extract embedded images to corpus",
    )
    args = parser.parse_args()

    try:
        source, local_path = resolve_source(args.source)
    except (FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    kind = detect_kind(source, local_path)
    slug = args.slug or (local_path.stem if local_path else slugify(source.split("v=")[-1][:11]))
    corpus_root = corpus_root_from_arg(args.corpus_root)

    extract_images = kind == "pptx" and not args.no_images
    markdown, _title = convert_markdown(
        source,
        keep_data_uris=extract_images or args.keep_data_uris,
    )
    if not markdown.strip():
        print("MarkItDown returned empty markdown", file=sys.stderr)
        return 1

    if extract_images and not args.keep_data_uris:
        from corpus_assets import slug_assets_dir

        markdown = rewrite_data_uri_images(
            markdown,
            slug_assets_dir(corpus_root, slug),
            slug,
        )

    if kind == "pptx":
        parts = split_pptx(markdown)
    elif kind == "docx":
        parts = split_docx(markdown, min_part_chars=args.min_part_chars)
    else:
        parts = split_youtube(
            markdown,
            source,
            chunk_seconds=args.youtube_chunk_sec,
            min_part_chars=args.min_part_chars,
        )
        if kind == "youtube" and fetch_youtube_transcript(source) is None:
            print(
                "Note: install youtube-transcript-api for timestamped transcript parts: "
                "python3 -m pip install youtube-transcript-api",
                file=sys.stderr,
            )

    merged: list[tuple[str, str]] = []
    for title, body in parts:
        if len(body.strip()) < args.min_part_chars:
            if merged:
                prev_title, prev_body = merged[-1]
                merged[-1] = (prev_title, prev_body + "\n\n" + body.strip())
            elif body.strip():
                merged.append((title, body))
            continue
        merged.append((title, body))

    if not merged:
        print("No parts met min length after split", file=sys.stderr)
        return 1

    count = write_corpus(
        source_label=source,
        raw_path=local_path,
        slug=slug,
        kind=kind,
        parts=merged,
        out_dir=args.out,
    )
    print(f"Wrote {count} parts ({kind}) to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
