#!/usr/bin/env python3
"""Generate hand-drawn style SVG diagrams for USER-GUIDE."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams"

HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Segoe Print, Bradley Hand, Comic Sans MS, cursive">
  <defs>
    <filter id="sketch" x="-4%" y="-4%" width="108%" height="108%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="3" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="1.5"/>
    </filter>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <path d="M0,0 L10,3.5 L0,7 Z" fill="#1e1e1e"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fffef9"/>
'''

FOOTER = "</svg>\n"


def box(x, y, w, h, fill, label, fs=18):
    return f'''
  <g filter="url(#sketch)">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#1e1e1e" stroke-width="2.2"/>
    <text x="{x + w/2}" y="{y + h/2 + fs*0.35}" text-anchor="middle" font-size="{fs}" fill="#1e1e1e">{label}</text>
  </g>'''


def arrow(x1, y1, x2, y2, label=""):
    mid = ""
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
        mid = f'<text x="{mx}" y="{my}" text-anchor="middle" font-size="14" fill="#555">{label}</text>'
    return f'''
  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1e1e1e" stroke-width="2" marker-end="url(#arr)" filter="url(#sketch)"/>
  {mid}'''


def title(text, y=36):
    return f'<text x="400" y="{y}" text-anchor="middle" font-size="26" font-weight="bold" fill="#1e1e1e">{text}</text>'


def overview():
    w, h = 800, 420
    body = title("琢磨 · 功能总览")
    body += box(40, 80, 140, 70, "#ffd8a8", "raw 资料", 16)
    body += box(220, 80, 120, 70, "#d0bfff", "Ingest", 18)
    body += box(380, 60, 160, 90, "#b2f2bb", "concepts\nClaim", 17)
    body += box(580, 80, 120, 70, "#a5d8ff", "Study", 18)
    body += box(380, 200, 160, 70, "#fff3bf", "Query + Apply", 16)
    body += box(580, 200, 120, 70, "#ffc9c9", "外搜", 18)
    body += box(40, 200, 140, 70, "#c3fae8", "Bootstrap\nAdopt", 15)
    body += box(220, 200, 120, 70, "#eebefa", "Lint", 18)
    body += box(380, 310, 160, 60, "#e5dbff", "notes 个人", 16)
    body += arrow(180, 115, 220, 115)
    body += arrow(340, 115, 380, 115)
    body += arrow(540, 115, 580, 115)
    body += arrow(460, 150, 460, 200)
    body += arrow(540, 235, 580, 235)
    body += arrow(110, 150, 110, 200)
    body += arrow(110, 235, 220, 235)
    body += arrow(340, 235, 380, 235)
    body += arrow(460, 270, 460, 310)
    return HEADER.format(w=w, h=h) + body + FOOTER


def ingest():
    w, h = 800, 380
    body = title("Ingest · 书 → 知识笔记", 34)
    body += box(30, 90, 110, 55, "#ffd8a8", "EPUB/PDF", 15)
    body += box(170, 90, 100, 55, "#fff3bf", "Topic map", 15)
    body += box(300, 90, 100, 55, "#c3fae8", "md 语料", 15)
    body += box(430, 75, 130, 85, "#b2f2bb", "Claim\n可理解+正式", 14)
    body += box(590, 90, 100, 55, "#a5d8ff", "Explain-back", 14)
    body += box(720, 90, 60, 55, "#d0bfff", "Evidence", 13)
    body += arrow(140, 118, 170, 118)
    body += arrow(270, 118, 300, 118)
    body += arrow(400, 118, 430, 118)
    body += arrow(560, 118, 590, 118)
    body += arrow(690, 118, 720, 118)
    body += box(170, 220, 200, 55, "#ffd8a8", "partial → continue", 15)
    body += box(430, 220, 200, 55, "#ffc9c9", "外搜 → 确认 Claim", 15)
    body += arrow(270, 145, 270, 220)
    body += arrow(495, 160, 495, 220)
    return HEADER.format(w=w, h=h) + body + FOOTER


def study():
    w, h = 800, 400
    body = title("Study · 学会一个概念", 34)
    body += box(40, 100, 120, 60, "#d0bfff", "map 纲领", 16)
    body += box(200, 100, 120, 60, "#fff3bf", "study 下一步", 14)
    body += box(360, 100, 130, 60, "#a5d8ff", "cold 先测", 16)
    body += box(530, 100, 120, 60, "#b2f2bb", "读 Claim", 16)
    body += box(690, 100, 90, 60, "#22c55e", "Promote", 14)
    body += arrow(160, 130, 200, 130)
    body += arrow(320, 130, 360, 130)
    body += arrow(490, 130, 530, 130)
    body += arrow(650, 130, 690, 130)
    body += box(200, 240, 140, 55, "#ffc9c9", "卡住?", 18)
    body += box(380, 220, 110, 55, "#ffd8a8", "Revise", 16)
    body += box(520, 220, 110, 55, "#eebefa", "feynman", 16)
    body += box(660, 220, 100, 55, "#ffc9c9", "外搜", 16)
    body += arrow(270, 160, 270, 240)
    body += arrow(340, 267, 380, 247)
    body += arrow(340, 267, 520, 247)
    body += arrow(340, 267, 660, 247)
    return HEADER.format(w=w, h=h) + body + FOOTER


def query_waishou():
    w, h = 800, 360
    body = title("Query · 外搜", 34)
    body += box(40, 100, 150, 65, "#a5d8ff", "Query think\nbrain-first", 14)
    body += box(230, 100, 120, 65, "#b2f2bb", "Answer", 16)
    body += box(390, 100, 120, 65, "#fff3bf", "Gaps", 16)
    body += box(550, 100, 130, 65, "#d0bfff", "Apply 现场", 15)
    body += arrow(190, 132, 230, 132)
    body += arrow(350, 132, 390, 132)
    body += arrow(510, 132, 550, 132)
    body += box(120, 230, 200, 55, "#ffc9c9", "外搜 三分法", 16)
    body += box(360, 230, 180, 55, "#ffd8a8", "External YYYY", 14)
    body += box(580, 230, 170, 55, "#ffc9c9", "确认 Claim", 15)
    body += arrow(400, 165, 220, 230)
    body += arrow(450, 165, 450, 230)
    body += arrow(615, 165, 615, 230)
    return HEADER.format(w=w, h=h) + body + FOOTER


def domain():
    w, h = 800, 340
    body = title("Domain · 四页两种读法", 34)
    body += box(80, 100, 140, 70, "#d0bfff", "map\n自顶向下", 16)
    body += box(260, 100, 140, 70, "#fff3bf", "overview\n入口", 15)
    body += box(440, 100, 140, 70, "#c3fae8", "guide\n索引", 16)
    body += box(620, 100, 140, 70, "#b2f2bb", "study\n进度", 16)
    body += arrow(220, 135, 260, 135)
    body += arrow(400, 135, 440, 135)
    body += arrow(580, 135, 620, 135)
    body += box(260, 220, 280, 55, "#a5d8ff", "concepts Claim", 17)
    body += arrow(330, 170, 330, 220)
    body += arrow(690, 170, 400, 220)
    return HEADER.format(w=w, h=h) + body + FOOTER


def lint_connect():
    w, h = 800, 360
    body = title("Lint · Connect", 34)
    body += box(40, 100, 90, 50, "#ffc9c9", "1阻断", 16)
    body += box(150, 100, 90, 50, "#ffd8a8", "2失真", 16)
    body += box(260, 100, 90, 50, "#fff3bf", "3待消化", 14)
    body += box(370, 100, 90, 50, "#d3f9d8", "4维护", 16)
    body += arrow(130, 125, 150, 125)
    body += arrow(240, 125, 260, 125)
    body += arrow(350, 125, 370, 125)
    body += box(500, 90, 120, 60, "#ffc9c9", "Revise", 16)
    body += box(640, 90, 120, 60, "#ffd8a8", "外搜", 16)
    body += arrow(460, 125, 500, 125)
    body += arrow(460, 125, 640, 125)
    body += box(120, 220, 200, 55, "#eebefa", "Connect", 16)
    body += box(380, 220, 220, 55, "#e5dbff", "notes/synthesis", 14)
    body += box(640, 220, 120, 55, "#d0bfff", "个人", 16)
    body += arrow(320, 247, 380, 247)
    body += arrow(600, 247, 640, 247)
    return HEADER.format(w=w, h=h) + body + FOOTER


DIAGRAMS = {
    "00-overview.svg": overview,
    "01-ingest.svg": ingest,
    "02-study.svg": study,
    "03-query-waishou.svg": query_waishou,
    "04-domain-four-pages.svg": domain,
    "05-lint-connect.svg": lint_connect,
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        path = OUT / name
        path.write_text(fn(), encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
