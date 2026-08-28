#!/usr/bin/env python3
"""Convert SRT/VTT to sectioned markdown under sources/<slug>/md/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_srt(text: str) -> list[tuple[str, str]]:
    blocks = re.split(r"\n\s*\n", text.strip())
    out: list[tuple[str, str]] = []
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        # skip numeric index line if present
        idx = 0
        if lines[0].isdigit():
            idx = 1
        if idx >= len(lines):
            continue
        ts = lines[idx] if "-->" in lines[idx] else ""
        text_lines = lines[idx + 1 :] if "-->" in lines[idx] else lines[idx:]
        if not text_lines:
            continue
        body = " ".join(text_lines)
        out.append((ts, body))
    return out


def parse_vtt(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    out: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "-->" in line:
            ts = line
            i += 1
            parts: list[str] = []
            while i < len(lines) and lines[i].strip() and "-->" not in lines[i]:
                parts.append(lines[i].strip())
                i += 1
            if parts:
                out.append((ts, " ".join(parts)))
        else:
            i += 1
    return out


def to_markdown(cues: list[tuple[str, str]], include_timestamps: bool) -> str:
    paras: list[str] = []
    buf: list[str] = []
    for ts, body in cues:
        body = re.sub(r"\s+", " ", body).strip()
        if not body:
            continue
        if include_timestamps and ts:
            buf.append(f"[{ts.split('-->')[0].strip()}] {body}")
        else:
            buf.append(body)
        if len(" ".join(buf)) > 400:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    sections = ["# Transcript\n"]
    for i, p in enumerate(paras, 1):
        sections.append(f"\n## Part {i:03d}\n\n{p}\n")
    return "\n".join(sections)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("out_dir", type=Path, help="sources/<slug>/md/")
    ap.add_argument("--timestamps", action="store_true")
    args = ap.parse_args()
    text = args.input.read_text(encoding="utf-8", errors="replace")
    lower = args.input.suffix.lower()
    if lower == ".srt":
        cues = parse_srt(text)
    elif lower == ".vtt":
        cues = parse_vtt(text)
    else:
        # plain text — one part
        cues = [("", text)]
    md = to_markdown(cues, args.timestamps)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / "part-001-transcript.md"
    out.write_text(md, encoding="utf-8")
    print(f"Wrote {out} ({len(cues)} cues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
