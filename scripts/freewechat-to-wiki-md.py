#!/usr/bin/env python3
"""Batch-fetch WeChat public-account articles from FreeWeChat into raw/web markdown.

Uses the profile ``?articles.json`` API for the article list and fetches each
article page with a WeChat in-app User-Agent (required by freewechat.com).

Example:
  python3 scripts/freewechat-to-wiki-md.py --limit 5
  python3 scripts/freewechat-to-wiki-md.py --profile MzUxNzQ5MTExNw== --slug zartbot
  python3 scripts/freewechat-to-wiki-md.py --html-dir ~/Downloads/zartbot-html
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

from corpus_assets import (
    DEFAULT_CORPUS_ROOT,
    asset_vault_path,
    corpus_root_from_arg,
    slug_assets_dir,
)

FREEWECHAT_BASE = "https://freewechat.com"
ZARTBOT_PROFILE = "MzUxNzQ5MTExNw=="
WECHAT_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
    "MicroMessenger/8.0.43(0x18002b2d) NetType/WIFI Language/zh_CN"
)
DEFAULT_RAW_OUT = Path.home() / "zhuomo-data" / "raw" / "web" / "zartbot"


@dataclass
class ArticleMeta:
    title: str
    url_path: str
    preview: str
    published: str
    article_id: str  # freewechat /a/{biz}/{id}/{idx}
    img_src: str = ""
    classification: str = ""


def slugify(text: str, max_len: int = 80) -> str:
    text = html.unescape(text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text or "article")[:max_len]


def parse_chinese_date(text: str) -> str:
    """``2025年10月27日`` → ``2025-10-27``; fallback to slug-safe prefix."""
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", text or "")
    if m:
        y, mo, d = m.groups()
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    return "unknown-date"


def article_id_from_path(url_path: str) -> str:
    parts = [p for p in url_path.split("/") if p]
    # /a/{biz}/{id}/{idx}
    if len(parts) >= 3 and parts[0] == "a":
        return parts[2]
    return slugify(url_path)


def filename_for(meta: ArticleMeta) -> str:
    date = parse_chinese_date(meta.published)
    slug = slugify(meta.title)
    return f"{date}-{slug}.md"


def http_get(url: str, *, referer: str | None = None, timeout: float = 30.0) -> bytes:
    headers = {
        "User-Agent": WECHAT_UA,
        "Accept": "text/html,application/xhtml+xml,application/json",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def list_articles(profile_id: str) -> list[ArticleMeta]:
    profile_url = f"{FREEWECHAT_BASE}/profile/{profile_id}"
    api_url = f"{profile_url}?articles.json"
    seen: set[str] = set()
    items: list[ArticleMeta] = []
    next_url: str | None = api_url

    while next_url:
        raw = http_get(next_url, referer=profile_url)
        data = json.loads(raw.decode("utf-8"))
        for row in data.get("items", []):
            path = row.get("url", "")
            if not path or path in seen:
                continue
            seen.add(path)
            items.append(
                ArticleMeta(
                    title=(row.get("title") or "untitled").strip(),
                    url_path=path,
                    preview=(row.get("preview") or "").strip(),
                    published=(row.get("ct") or "").strip(),
                    article_id=article_id_from_path(path),
                    img_src=(row.get("img_src") or "").strip(),
                    classification=(row.get("classification") or "").strip(),
                )
            )
        more = (data.get("load-more-src") or "").strip()
        if not more:
            break
        next_url = more if more.startswith("http") else f"{FREEWECHAT_BASE}{more}"

    return items


def fetch_article_html(url_path: str, profile_id: str) -> str | None:
    url = url_path if url_path.startswith("http") else f"{FREEWECHAT_BASE}{url_path}"
    referer = f"{FREEWECHAT_BASE}/profile/{profile_id}"
    try:
        body = http_get(url, referer=referer)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        print(f"  fetch failed: {exc}", file=sys.stderr)
        return None
    text = body.decode("utf-8", errors="replace")
    if "Attention Required" in text and "Cloudflare" in text:
        print("  fetch blocked by Cloudflare", file=sys.stderr)
        return None
    return text


def inline_to_md(node: Tag | NavigableString) -> str:
    if isinstance(node, NavigableString):
        return html.unescape(str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name in {"script", "style"}:
        return ""
    if name in {"b", "strong"}:
        inner = "".join(inline_to_md(c) for c in node.children).strip()
        return f"**{inner}**" if inner else ""
    if name in {"i", "em"}:
        inner = "".join(inline_to_md(c) for c in node.children).strip()
        return f"*{inner}*" if inner else ""
    if name == "br":
        return "\n"
    if name == "code":
        return f"`{node.get_text()}`"
    if name == "a":
        href = node.get("href", "")
        text = node.get_text(strip=True)
        if href and text:
            return f"[{text}]({href})"
        return text
    return "".join(inline_to_md(c) for c in node.children)


def image_url(tag: Tag) -> str | None:
    for attr in ("data-src", "src", "data-original"):
        val = (tag.get(attr) or "").strip()
        if val and not val.startswith("data:"):
            return val
    return None


def block_to_md(
    node: Tag | NavigableString,
    lines: list[str],
    image_map: dict[str, str],
) -> None:
    if isinstance(node, NavigableString):
        return
    if not isinstance(node, Tag):
        return

    name = node.name.lower()
    if name in {"script", "style"}:
        return

    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        text = node.get_text(" ", strip=True)
        if text:
            level = min(int(name[1]) + 1, 6)
            lines.append("")
            lines.append(f"{'#' * level} {text}")
            lines.append("")
        return

    if name == "pre":
        text = node.get_text("\n", strip=False).rstrip()
        if text:
            lines.append("")
            lines.append("```")
            lines.append(text)
            lines.append("```")
            lines.append("")
        return

    if name == "p":
        text = inline_to_md(node).strip()
        if text:
            lines.append(text)
            lines.append("")
        return

    if name in {"ul", "ol"}:
        ordered = name == "ol"
        for i, li in enumerate(node.find_all("li", recursive=False), start=1):
            text = li.get_text(" ", strip=True)
            if text:
                prefix = f"{i}." if ordered else "-"
                lines.append(f"{prefix} {text}")
        lines.append("")
        return

    if name == "table":
        rows: list[list[str]] = []
        for tr in node.find_all("tr"):
            cells = [
                c.get_text(" ", strip=True).replace("|", "\\|")
                for c in tr.find_all(["th", "td"])
            ]
            if cells:
                rows.append(cells)
        if rows:
            lines.append("")
            lines.append("| " + " | ".join(rows[0]) + " |")
            lines.append("| " + " | ".join(["---"] * len(rows[0])) + " |")
            for row in rows[1:]:
                padded = row + [""] * (len(rows[0]) - len(row))
                lines.append("| " + " | ".join(padded[: len(rows[0])]) + " |")
            lines.append("")
        return

    if name == "img":
        src = image_url(node)
        if src:
            ref = image_map.get(src, src)
            lines.append("")
            lines.append(f"![image]({ref})")
            lines.append("")
        return

    if name in {"section", "div", "figure", "blockquote"}:
        if name == "section":
            strong = node.find(["strong", "b"])
            text = node.get_text(" ", strip=True)
            if strong and text and len(text) < 120 and text == strong.get_text(" ", strip=True):
                lines.append("")
                lines.append(f"## {text}")
                lines.append("")
                return
        for child in node.children:
            block_to_md(child, lines, image_map)
        return

    for child in node.children:
        block_to_md(child, lines, image_map)


def download_image(url: str, dest: Path, referer: str) -> bool:
    headers = {
        "User-Agent": WECHAT_UA,
        "Referer": referer,
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return False
    if not data:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return True


def collect_images(content: Tag) -> list[str]:
    urls: list[str] = []
    for img in content.find_all("img"):
        src = image_url(img)
        if src:
            urls.append(src)
    return urls


def html_to_markdown(
    page_html: str,
    *,
    slug: str,
    corpus_root: Path,
    download_images: bool,
    referer: str,
) -> tuple[str, str, str, str]:
    soup = BeautifulSoup(page_html, "html.parser")
    title_el = soup.select_one("#activity-name, h1.rich_media_title, h1")
    time_el = soup.select_one("#publish_time, em#publish_time")
    author_el = soup.select_one("#js_name, .rich_media_meta_nickname")

    title = title_el.get_text(strip=True) if title_el else ""
    published = time_el.get_text(strip=True) if time_el else ""
    author = author_el.get_text(strip=True) if author_el else ""

    content = soup.select_one("#js_content, .rich_media_content")
    if not content:
        raise ValueError("No #js_content found in HTML")

    image_map: dict[str, str] = {}
    if download_images:
        assets_dir = slug_assets_dir(corpus_root, slug)
        for idx, src in enumerate(collect_images(content), start=1):
            parsed = urllib.parse.urlparse(src)
            ext = Path(parsed.path).suffix or ".jpg"
            if "wx_fmt=" in src:
                fmt = re.search(r"wx_fmt=(\w+)", src)
                if fmt:
                    ext = f".{fmt.group(1)}"
            fname = f"{slugify(title or 'article')}-{idx}{ext}"
            dest = assets_dir / fname
            if download_image(src, dest, referer) or dest.exists():
                image_map[src] = asset_vault_path(slug, dest.name)

    lines: list[str] = []
    block_to_md(content, lines, image_map)
    body = "\n".join(lines)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return title or "untitled", published or "", author or "", body


def build_markdown(
    meta: ArticleMeta,
    *,
    profile_id: str,
    slug: str,
    body: str,
    fetch_status: str,
    author: str = "zartbot",
) -> str:
    canonical = f"{FREEWECHAT_BASE}{meta.url_path}"
    date_iso = parse_chinese_date(meta.published)
    front = f"""---
type: raw-web-article
source: freewechat
account: {slug}
profile_id: {profile_id}
article_id: {meta.article_id}
title: {json.dumps(meta.title, ensure_ascii=False)}
published: {json.dumps(meta.published, ensure_ascii=False)}
date: {date_iso}
author: {author}
fetch_status: {fetch_status}
url: {canonical}
classification: {meta.classification or "其他"}
---

# {meta.title}

- **公众号:** {slug}
- **发布:** {meta.published or "unknown"}
- **原文:** {canonical}
- **抓取:** {fetch_status}

"""
    if fetch_status != "full" and meta.preview:
        front += f"> 摘要（FreeWeChat 预览）: {meta.preview}\n\n"
    return front + body + "\n"


def write_manifest(out_dir: Path, articles: list[ArticleMeta], results: list[dict]) -> None:
    manifest = {
        "source": "freewechat",
        "count": len(articles),
        "articles": results,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    rows = [
        "| Date | Title | File | Status |",
        "|------|-------|------|--------|",
    ]
    for row in results:
        rows.append(
            f"| {row['date']} | {row['title']} | `{row['file']}` | {row['status']} |"
        )
    index_md = f"""---
type: source-index
source: freewechat-zartbot
---

# zartbot — FreeWeChat article index

Total: **{len(results)}** articles.

{chr(10).join(rows)}
"""
    (out_dir / "index.md").write_text(index_md, encoding="utf-8")


def find_html_for_article(html_dir: Path, article_id: str) -> Path | None:
    patterns = [f"*{article_id}*", f"*{article_id}*.html", f"*{article_id}*.htm"]
    for pattern in patterns:
        matches = sorted(html_dir.glob(pattern))
        if matches:
            return matches[0]
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch WeChat articles from FreeWeChat → raw/web markdown"
    )
    parser.add_argument(
        "--profile",
        default=ZARTBOT_PROFILE,
        help=f"FreeWeChat profile id (default: zartbot {ZARTBOT_PROFILE})",
    )
    parser.add_argument("--slug", default="zartbot", help="Source slug / account name")
    parser.add_argument(
        "--raw-out",
        type=Path,
        default=DEFAULT_RAW_OUT,
        help=f"Output directory (default: {DEFAULT_RAW_OUT})",
    )
    parser.add_argument(
        "--corpus-root",
        type=Path,
        default=None,
        help=f"Corpus root for images (default: {DEFAULT_CORPUS_ROOT})",
    )
    parser.add_argument("--limit", type=int, default=0, help="Max articles (0 = all)")
    parser.add_argument("--delay", type=float, default=1.2, help="Seconds between fetches")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if output md exists")
    parser.add_argument("--no-images", action="store_true", help="Do not download images")
    parser.add_argument(
        "--html-dir",
        type=Path,
        help="Import full HTML saved from browser (matched by article id in filename)",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Only write manifest.json + index.md from article list",
    )
    args = parser.parse_args()

    raw_out = args.raw_out.expanduser().resolve()
    raw_out.mkdir(parents=True, exist_ok=True)
    corpus_root = corpus_root_from_arg(args.corpus_root)

    print(f"Listing articles for profile {args.profile} …")
    articles = list_articles(args.profile)
    if args.limit:
        articles = articles[: args.limit]
    print(f"Found {len(articles)} articles")

    referer = f"{FREEWECHAT_BASE}/profile/{args.profile}"
    results: list[dict] = []

    for i, meta in enumerate(articles, start=1):
        out_file = raw_out / filename_for(meta)
        print(f"[{i}/{len(articles)}] {meta.title}")

        if args.skip_existing and out_file.exists():
            print("  skip existing")
            results.append(
                {
                    "title": meta.title,
                    "date": parse_chinese_date(meta.published),
                    "file": out_file.name,
                    "status": "skipped",
                    "url": f"{FREEWECHAT_BASE}{meta.url_path}",
                    "article_id": meta.article_id,
                }
            )
            continue

        if args.manifest_only:
            results.append(
                {
                    "title": meta.title,
                    "date": parse_chinese_date(meta.published),
                    "file": out_file.name,
                    "status": "listed",
                    "url": f"{FREEWECHAT_BASE}{meta.url_path}",
                    "article_id": meta.article_id,
                }
            )
            continue

        body = ""
        fetch_status = "preview-only"
        author = args.slug
        title = meta.title
        published = meta.published
        html_page: str | None = None
        if args.html_dir:
            html_path = find_html_for_article(args.html_dir.expanduser(), meta.article_id)
            if html_path:
                html_page = html_path.read_text(encoding="utf-8", errors="replace")
                print(f"  using local HTML {html_path.name}")

        if html_page is None:
            html_page = fetch_article_html(meta.url_path, args.profile)
            if html_page and args.delay:
                time.sleep(args.delay)

        if html_page:
            try:
                parsed_title, parsed_published, parsed_author, body = html_to_markdown(
                    html_page,
                    slug=args.slug,
                    corpus_root=corpus_root,
                    download_images=not args.no_images,
                    referer=referer,
                )
                title = parsed_title or meta.title
                if re.search(r"\d{4}年\d", parsed_published):
                    published = parsed_published
                else:
                    published = meta.published
                author = parsed_author or args.slug
                fetch_status = "full"
            except ValueError as exc:
                print(f"  parse warning: {exc}", file=sys.stderr)
                body = meta.preview
                fetch_status = "preview-only"
        else:
            body = meta.preview

        meta_for_file = ArticleMeta(
            title=title or meta.title,
            url_path=meta.url_path,
            preview=meta.preview,
            published=published or meta.published,
            article_id=meta.article_id,
            img_src=meta.img_src,
            classification=meta.classification,
        )
        out_file = raw_out / filename_for(meta_for_file)
        out_file.write_text(
            build_markdown(
                meta_for_file,
                profile_id=args.profile,
                slug=args.slug,
                body=body,
                fetch_status=fetch_status,
                author=author,
            ),
            encoding="utf-8",
        )
        print(f"  wrote {out_file.name} ({fetch_status})")
        results.append(
            {
                "title": meta_for_file.title,
                "date": parse_chinese_date(meta_for_file.published),
                "file": out_file.name,
                "status": fetch_status,
                "url": f"{FREEWECHAT_BASE}{meta.url_path}",
                "article_id": meta.article_id,
            }
        )

    write_manifest(raw_out, articles, results)
    full = sum(1 for r in results if r["status"] == "full")
    preview = sum(1 for r in results if r["status"] == "preview-only")
    print(f"Done: {len(results)} listed, {full} full, {preview} preview-only → {raw_out}")


if __name__ == "__main__":
    main()
