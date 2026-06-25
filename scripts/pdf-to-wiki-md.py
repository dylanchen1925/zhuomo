#!/usr/bin/env python3
"""Convert PDF to per-chapter Markdown under wiki/sources/<slug>/md/."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# HDN (Hardware-Defined Networking) — PDF page ranges (1-indexed, inclusive).
HDN_CHAPTERS: list[tuple[str, int, int]] = [
    ("Introduction", 5, 7),
    ("Foundation Principles", 8, 13),
    ("Tunnels", 14, 22),
    ("Network Virtualization", 23, 30),
    ("Terminology", 31, 39),
    ("Forwarding Protocols", 40, 114),
    ("Load Balancing", 115, 125),
    ("Overlay Protocols", 126, 139),
    ("Virtual Private Networks", 140, 153),
    ("Multicast", 154, 166),
    ("Connections", 167, 184),
    ("Quality of Service", 185, 208),
    ("Time Synchronization", 209, 238),
    ("OAM", 239, 276),
    ("Security", 277, 301),
    ("Searching", 302, 314),
    ("Firewall Filters", 315, 320),
    ("Routing Protocols", 321, 334),
    ("Forwarding System Architecture", 335, 348),
    ("Conclusion", 349, 352),
]

# Kubernetes: Up and Running, 3rd ed. Early Release (ISBN 9781098110130, Dec 2021).
K8S_UP_AND_RUNNING_CHAPTERS: list[tuple[str, int, int]] = [
    ("Pods", 7, 26),
    ("Labels and Annotations", 27, 36),
    ("Accessing Kubernetes from Common Programming Languages", 37, 50),
    ("Policy and Governance for Kubernetes Clusters", 51, 67),
]

# Orhan Ergun — CCDE In Depth (SchonJasoon, 2016). PDF page = book page.
ORHAN_CCDE_IN_DEPTH_CHAPTERS: list[tuple[str, int, int]] = [
    ("Front Matter", 1, 20),
    ("Layer 2 Technologies", 21, 57),
    ("Network Design Tools", 58, 83),
    ("OSPF", 84, 134),
    ("IS-IS", 135, 160),
    ("EIGRP", 161, 186),
    ("VPN Design", 187, 209),
    ("IPv6 Design", 210, 249),
    ("Border Gateway Protocol", 250, 332),
    ("Multicast", 333, 351),
    ("Quality of Service", 352, 371),
    ("MPLS", 372, 465),
    ("CCDE Practical Scenario — SpeedNet", 466, 494),
    ("CCDE Practical Scenario — MAG Energy", 495, 562),
]

# Cisco Catalyst SD-WAN Design Guide (Jan 2025, 102 pages). PDF page = printed page.
CISCO_SDWAN_DESIGN_CHAPTERS: list[tuple[str, int, int]] = [
    ("Front Matter", 1, 2),
    ("Introduction", 3, 3),
    ("About this Guide", 4, 4),
    ("Use Cases", 5, 11),
    ("Architecture and Components", 12, 16),
    ("Control Plane", 17, 25),
    ("Orchestration Plane", 26, 28),
    ("Data Plane", 29, 40),
    ("SD-WAN Routing", 41, 43),
    ("Firewall Port Considerations", 44, 50),
    ("Control Components Deployment", 51, 65),
    ("WAN Edge Deployment", 66, 87),
    ("Management Plane", 88, 98),
    ("Deployment Planning", 99, 100),
    ("Appendix References", 101, 102),
]

# Cisco Campus LAN and Wireless LAN Solution Design Guide (May 2020, 76 pages).
CISCO_CAMPUS_LAN_WLAN_CHAPTERS: list[tuple[str, int, int]] = [
    ("Front Matter", 1, 2),
    ("Definition and Introduction", 3, 4),
    ("Design Overview", 5, 5),
    ("Design Fundamentals Campus Wired LAN", 6, 18),
    ("Design Options Campus Wired LAN", 19, 24),
    ("Design Fundamentals LAN Security", 25, 26),
    ("Design Fundamentals LAN High Availability", 27, 30),
    ("Design Fundamentals Campus Wireless LAN", 31, 44),
    ("Design Options Campus Wireless LAN", 45, 64),
    ("Deployment Platform Choices", 65, 68),
    ("Operate Common Components", 69, 72),
    ("Appendix Glossary", 73, 76),
]

# Isovalent Networking for Kubernetes: Design Guide (Cisco ACI + NX-OS, Jun 2025, 38 pp).
ISOVALENT_K8S_ACI_NXOS_DESIGN_CHAPTERS: list[tuple[str, int, int]] = [
    ("Front Matter", 1, 4),
    ("Introduction and Executive Summary", 5, 9),
    ("Design Options and Common Features", 10, 14),
    ("ACI Basic Design", 15, 19),
    ("ACI Advanced Design", 20, 26),
    ("ACI Scale Testing", 27, 28),
    ("Example OpenShift Configuration", 29, 30),
    ("NX-OS EVPN VXLAN Design", 31, 37),
    ("Closing Remarks", 38, 38),
]

# Booth, Colomb, Williams — The Craft of Research, 3rd ed. (2008). PDF page = printed page.
CRAFT_OF_RESEARCH_CHAPTERS: list[tuple[str, int, int]] = [
    ("Front Matter", 1, 26),
    ("Part I Prologue and Ch1 Thinking in Print", 27, 34),
    ("Ch2 Connecting with Your Reader", 35, 47),
    ("Part II Prologue Planning Overview", 48, 53),
    ("Ch3 From Topics to Questions", 54, 69),
    ("Ch4 From Questions to a Problem", 70, 86),
    ("Ch5 From Problems to Sources", 87, 103),
    ("Ch6 Engaging Sources", 104, 121),
    ("Part III Prologue Assembling an Argument", 122, 126),
    ("Ch7 Making Good Arguments Overview", 127, 138),
    ("Ch8 Making Claims", 139, 148),
    ("Ch9 Assembling Reasons and Evidence", 149, 158),
    ("Ch10 Acknowledgments and Responses", 159, 171),
    ("Ch11 Warrants", 172, 189),
    ("Part IV Prologue Planning Again", 190, 195),
    ("Ch12 Planning", 196, 205),
    ("Ch13 Drafting Your Report", 206, 222),
    ("Ch14 Revising Organization and Argument", 223, 231),
    ("Ch15 Communicating Evidence Visually", 232, 250),
    ("Ch16 Introductions and Conclusions", 251, 267),
    ("Ch17 Revising Style", 268, 291),
    ("Ethics Appendix and Index", 292, 337),
]

PRESETS: dict[str, list[tuple[str, int, int]]] = {
    "hdn": HDN_CHAPTERS,
    "k8s-up-and-running": K8S_UP_AND_RUNNING_CHAPTERS,
    "k8supandrunning": K8S_UP_AND_RUNNING_CHAPTERS,
    "orhan-ccde-in-depth": ORHAN_CCDE_IN_DEPTH_CHAPTERS,
    "orhanergunccdeindepth": ORHAN_CCDE_IN_DEPTH_CHAPTERS,
    "cisco-sdwan-design": CISCO_SDWAN_DESIGN_CHAPTERS,
    "ciscosdwan-design": CISCO_SDWAN_DESIGN_CHAPTERS,
    "ciscosdwan design": CISCO_SDWAN_DESIGN_CHAPTERS,
    "cisco-campus-lan-wlan": CISCO_CAMPUS_LAN_WLAN_CHAPTERS,
    "ciscocampuslanwlan": CISCO_CAMPUS_LAN_WLAN_CHAPTERS,
    "isovalent-k8s-aci-nxos-design": ISOVALENT_K8S_ACI_NXOS_DESIGN_CHAPTERS,
    "isovalentk8sacinxosdesign": ISOVALENT_K8S_ACI_NXOS_DESIGN_CHAPTERS,
    "craft-of-research": CRAFT_OF_RESEARCH_CHAPTERS,
    "craftofresearch": CRAFT_OF_RESEARCH_CHAPTERS,
    "the-craft-of-research": CRAFT_OF_RESEARCH_CHAPTERS,
}


def slugify(text: str, max_len: int = 80) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text or "section")[:max_len]


def pdftotext_pages(pdf: Path, start: int, end: int) -> str:
    result = subprocess.run(
        ["pdftotext", "-f", str(start), "-l", str(end), str(pdf), "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext failed pages {start}-{end}: {result.stderr[:300]}")
    return result.stdout


def clean_text(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        s = line.rstrip()
        if re.fullmatch(r"\d+", s.strip()) and len(s.strip()) <= 3:
            continue
        if s.strip() == "Hardware-Defined Networking":
            continue
        if s.strip() == "\f" or s == "\x0c":
            continue
        out.append(s)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def promote_headings(md: str, title: str) -> tuple[str, list[str]]:
    headings: list[str] = [title]
    lines = md.split("\n")
    out: list[str] = [f"# {title}", ""]
    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append("")
            continue
        if stripped == title:
            continue
        if re.match(r"^Figure \d+", stripped):
            anchor = slugify(stripped)
            out.append(f"## {stripped} {{#{anchor}}}")
            headings.append(stripped)
            out.append("")
            continue
        if len(stripped) < 80 and stripped[0].isupper() and not stripped.endswith("."):
            if re.match(r"^[A-Z][A-Za-z0-9 /-]+$", stripped) and len(stripped.split()) <= 6:
                anchor = slugify(stripped)
                out.append(f"## {stripped} {{#{anchor}}}")
                headings.append(stripped)
                out.append("")
                continue
        out.append(line)
    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return body, headings


def extract_images(pdf: Path, assets_dir: Path) -> int:
    assets_dir.mkdir(parents=True, exist_ok=True)
    prefix = assets_dir / "img"
    result = subprocess.run(
        ["pdfimages", "-png", str(pdf), str(prefix)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return 0
    return len(list(assets_dir.glob("img-*.png")))


def main() -> int:
    parser = argparse.ArgumentParser(description="PDF → wiki/sources/<slug>/md/")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--slug", type=str, default="")
    parser.add_argument("--preset", type=str, default="", help="Chapter map preset (e.g. hdn)")
    parser.add_argument("--no-images", action="store_true")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = args.slug or pdf.stem.lower()

    preset = args.preset or slug.replace("-", "")
    if preset not in PRESETS and slug in PRESETS:
        preset = slug
    chapters = PRESETS.get(preset)
    if not chapters:
        print(f"No chapter preset for {preset!r}; add page ranges to PRESETS", file=sys.stderr)
        return 1

    image_count = 0
    if not args.no_images:
        image_count = extract_images(pdf, out_dir / "assets")

    index_lines = [
        "---",
        "type: source-md-corpus",
        f"raw: {pdf}",
        "---",
        "",
        f"# Markdown corpus — {slug}",
        "",
        "Full PDF text converted for provenance links. Concept pages cite `[[md/part-NNN#heading]]`.",
        "",
    ]
    if image_count:
        index_lines.append(
            f"Images extracted to `md/assets/` ({image_count} PNG files via pdfimages)."
        )
        index_lines.append("")
    index_lines.extend(
        [
            "| Part | File | Chapter | PDF pages | First headings |",
            "|------|------|---------|-----------|----------------|",
        ]
    )

    for part, (title, start, end) in enumerate(chapters, start=1):
        raw = clean_text(pdftotext_pages(pdf, start, end))
        if len(raw.strip()) < 80:
            continue
        md, headings = promote_headings(raw, title)
        fname = f"part-{part:03d}.md"
        (out_dir / fname).write_text(md, encoding="utf-8")
        preview = "; ".join(headings[:3])
        index_lines.append(
            f"| {part} | [[md/{fname}\\|{fname}]] | {title} | {start}–{end} | {preview[:100]} |"
        )

    index_lines.extend(
        [
            "",
            "## Provenance link format",
            "",
            "```markdown",
            "## Evidence",
            "- [[md/part-006#forwarding-protocols]] — Forwarding protocols chapter",
            "```",
            "",
        ]
    )
    (out_dir / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Wrote {part} parts to {out_dir}; {image_count} images in assets/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
