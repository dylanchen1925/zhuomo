# Zhuomo User Guide

How to set up **琢磨 (Zhuomo)**, learn from sources **one concept at a time**, and keep a personal wiki + optional agent skills.

**You read this guide.** The agent reads [SKILL.md](SKILL.md) and loads detail from `~/zhuomo/references/` when needed.

**Quick links:** [REVIEW.md](REVIEW.md) · [LEARNING.md](LEARNING.md) · Obsidian `wiki/help.md` · [SIMPLE.md](SIMPLE.md)

---

## 先说你想要什么（意图 → 指令）

| 你想… | 说… | 停在哪 |
|--------|-----|--------|
| 新建知识库 | `Bootstrap: raw …, vault …` | 文件夹 + AGENTS + config |
| **接入已有 Obsidian** | `Adopt vault: …` | 只补 help/AGENTS，**不改**你的 concepts |
| 导入一本书 | `Ingest: …/book.epub` | concepts + topic map |
| 书太大、分批 | `Ingest continue: <source-slug>` | partial → 续 deepen |
| 导入字幕/转写 | `Ingest: …/lecture.srt` | 默认只 md 语料；要概念加 `deepen` |
| 搞懂一个概念 | `Explain-back [[slug]] cold` | Promote solid |
| 用知识分析现场 | `Query think: 场景 …` | Answer + 可选 **Apply** |
| 查版本/CVE | `外搜 <domain>` | Evidence；Claim **需你确认** |
| 库健康 | `Lint` | 四级报告（阻断→维护） |
| 连续学一域 | `Study continue: kubernetes-cilium` | 一课 Explain-back |
| 记个人模型 | `Connect: … — 记入 synthesis` | `wiki/notes/synthesis/` |

---

## Table of contents

0. [功能地图（一张总图）](#0-功能地图一张总图)
1. [功能图式说明](#1-功能图式说明)
2. [What Zhuomo is](#2-what-zhuomo-is)
3. [Prerequisites](#3-prerequisites)
4. [First-time setup（Bootstrap / Adopt）](#4-first-time-setupbootstrap--adopt)
5. [Learn by concept (Study)](#5-learn-by-concept-study)
6. [Lint vs Revise vs 外搜](#6-lint-vs-revise-vs-外搜)
7. [Daily habits](#7-daily-habits)
8. [Operations reference](#8-operations-reference)
9. [Prompt cookbook](#9-prompt-cookbook)
10. [Domain frameworks and progress](#10-domain-frameworks-and-progress)
11. [Optional Cursor skills](#11-optional-cursor-skills)
12. [Multi-device workflow](#12-multi-device-workflow)
13. [Source types](#13-source-types)
14. [Troubleshooting](#14-troubleshooting)
15. [FAQ](#15-faq)

---

## 0. 功能地图（一张总图）

琢磨把 **原始资料** 编译成 **Obsidian wiki**，你用 **Claim 知识笔记 + Explain-back** 掌握，必要时 **外搜** 保鲜；**Query** 用来问已有知识、**Apply** 分析现场。

> **手绘风图**在 `assets/diagrams/`（Excalidraw Pastel + 抖线滤镜）。改图：`python3 scripts/generate-sketch-diagrams.py`

![琢磨功能总览 — 手绘风](assets/diagrams/00-overview.svg)

**Corpus（编译层）** = `concepts/` · `sources/` · `domains/` · `wiki/synthesis/`  
**Personal（个人层）** = `wiki/notes/` — Connect / 「我的想法」写这里，Ingest **不会**自动写进去。

---

## 1. 功能图式说明（手绘风）

下面每张 **SVG 手绘图** 对应一组功能；文字表补充细节。规则见 [SKILL.md](SKILL.md) 与 `references/`。

| 图文件 | 内容 |
|--------|------|
| [00-overview.svg](assets/diagrams/00-overview.svg) | 总览：raw → 动词 → wiki |
| [01-ingest.svg](assets/diagrams/01-ingest.svg) | Ingest + partial continue + 外搜确认 |
| [02-study.svg](assets/diagrams/02-study.svg) | Study 链 + 卡住三分支 |
| [03-query-waishou.svg](assets/diagrams/03-query-waishou.svg) | Query / Apply / 外搜 |
| [04-domain-four-pages.svg](assets/diagrams/04-domain-four-pages.svg) | map · overview · guide · study |
| [05-lint-connect.svg](assets/diagrams/05-lint-connect.svg) | Lint 四级 + Connect |

---

### 1.1 Bootstrap — 从零建库

```
  你                          Agent                    磁盘
  ───                         ─────                    ────
  Bootstrap: raw… vault…  →   建 inbox/ books/    →   ~/zhuomo-data/raw/
                              建 wiki/            →   vault/wiki/
                              zhuomo_config set   →   ~/.zhuomo/config.json
```

---

### 1.2 Adopt — 接入已有 Obsidian（不覆盖）

已有大量笔记时 **不要 Bootstrap 覆盖**，用 Adopt：

**原则：** `vault-adopt-check.py` → 只加 help / AGENTS / `.zhuomo-adopted`，**不批量改** 已有 `concepts/` Claim。

---

### 1.3 Ingest — 书 → 知识笔记

![Ingest 流程 — 手绘风](assets/diagrams/01-ingest.svg)

**Claim 两层（技术书）：** 可理解层（问题 + 例子 + 机制）→ 正式层（定义/CLI/公式，指回例子）。

**大书分批：** `ingest_status: partial` + `Ingest continue: <slug>`，见 source 页 `next_sections`。

---

### 1.4 Transcript — 字幕 / 转写（默认只存档）

默认：**清洗 → md 语料 → 不生成 concepts**；要说 `deepen` / `沉淀知识` 才走 Ingest  deepen。

可选：`python3 ~/zhuomo/scripts/transcript-to-wiki-md.py input.srt out/md/`

---

### 1.5 Study — 学会一个概念

![Study 流程 — 手绘风](assets/diagrams/02-study.svg)

**Study continue：** `Study continue: <domain>` — 只从 `study.md` **下一步** 挑一课。

**卡住诊断（不必死磕 feynman）：**

| 现象 | 下一步 |
|------|--------|
| Claim 像目录、太短 | **Revise** |
| 术语/公式不懂 | Claim **正式层** + Evidence |
| 会背不会选型 | Revise 加 scenario |
| 和书/外搜矛盾 | **外搜** 或 Revise |
| 15 分钟做不完 | study 表 **一行** |

---

### 1.6 Query think + 1.7 外搜

![Query 与外搜 — 手绘风](assets/diagrams/03-query-waishou.svg)

**Apply 示例：**

```
Query think: 生产里 BGP 经常 flap，wiki 里的 [[bgp-hold-timer]] 怎么排查？场景：双 ISP，一侧在抖。
```

**外搜：** 事实 / 判断 / 未知 三分法；改 Claim 前必须 **确认 Claim**。自动外搜见 §6。

---

### 1.8 Revise — 改错 / 加厚 Claim

定位 → 修订卡 → 改 Claim / merge → 传播 → `log.md`。个人想法：`Revise [[x]] — 我的想法：…` → `notes/on-concept/`。

---

### 1.9 Lint + 1.10 Connect

![Lint 与 Connect — 手绘风](assets/diagrams/05-lint-connect.svg)

**Lint：** 1阻断 → 2失真 → 3待消化 → 4维护；脚本只报**候选**，合并前须读正文。

| 写哪 | 谁写 |
|------|------|
| `wiki/synthesis/` | Ingest / Query 编译 |
| `wiki/notes/synthesis/` | **Connect** 个人 |

---

### 1.11 Domain 四页 — 两种读法

![Domain 四页 — 手绘风](assets/diagrams/04-domain-four-pages.svg)

| 页 | 回答 |
|----|------|
| **map** | 整体怎么叠？Tier A 在哪层？ |
| **overview** | 为什么学？外搜？gaps？ |
| **guide** | 某概念在哪？ |
| **study** | 学到哪？下一步 Promote/cold？ |

---

## 2. What Zhuomo is

**琢磨** — polish raw material until it is clear, linked, and usable.

| You provide | Zhuomo helps produce |
|-------------|----------------------|
| EPUB, PDF, articles, **SRT/VTT**, notes | **Wiki** — concepts (Claim), Evidence, domains |
| Repeatable agent behavior (optional) | **Cursor skills** — separate chat; §11 |
| Your study time | **Explain-back** (cold / feynman) + **Study continue** |

**North star:** Ingest once → study from **Claim** → open book only when Claim thin or you want primary text.

**Agent 细节** 在 `~/zhuomo/references/`（Claim rubric、Apply、外搜、Lint 等）；**SKILL.md** 是路由入口。

---

## 3. Prerequisites

| Tool | Purpose |
|------|---------|
| **Cursor** | Run Zhuomo (`/zhuomo` or natural language) |
| **Obsidian** | Read wiki, graph, Dataview for study 进度 |
| **Git** (optional) | Version wiki or zhuomo repo |

```bash
ln -sf /path/to/zhuomo ~/.cursor/skills/zhuomo
```

Config（仅路径）：`python3 ~/zhuomo/scripts/zhuomo_config.py show`

---

## 4. First-time setup（Bootstrap / Adopt）

### 新建库 — Bootstrap

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, Obsidian vault ~/…/Dylan Chen
```

或一行带第一本书：

```
/zhuomo Bootstrap + ingest: ~/zhuomo-data/raw/books/my-first-book.epub
```

**Default:** reference depth — topic map, md corpus, concepts deepened + Explain-back + Evidence.

**Lite:** `overview only` / `Bootstrap lite`.

### 已有 Obsidian — Adopt

```
/zhuomo Adopt vault: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen
```

Agent 跑 `vault-adopt-check.py`；**不会**覆盖已有 concepts。只补 `help.md`、`AGENTS.md`、`.zhuomo-adopted`。

### Folder layout

```
~/zhuomo-data/raw/
├── inbox/          # phone captures
├── web/ · video/ · books/ · assets/
└── processed/

vault/
├── AGENTS.md
├── .zhuomo-adopted   # Adopt 后可选标记
└── wiki/
    ├── overview.md · index.md · log.md · domain-map.md · help.md
    ├── domains/<slug>/map · overview · guide · study
    ├── concepts/*.md
    ├── sources/<slug>.md + md/    # 含 ingest_status / next_sections
    ├── synthesis/                 # 编译层
    └── notes/                     # 个人层
```

### First ingest

```
/zhuomo Ingest: ~/zhuomo-data/raw/books/my-first-book.epub
```

大书续作：

```
/zhuomo Ingest continue: my-book-slug
```

Map only：

```
/zhuomo Ingest overview only: raw/web/article.md
```

---

## 5. Learn by concept (Study)

**主教材 = `## Claim` 知识笔记**，不是整本书。见 §1.5 图。

| Step | You say |
|------|---------|
| **Cold** | `Explain-back [[concept]] cold` |
| **Read** | Open concept — Claim（可理解层 + 正式层） |
| **Explain-back** | `Explain-back [[concept]]` — 一轮一题 |
| **Feynman** | `Explain-back [[concept]] feynman` |
| **Promote** | `Promote [[concept]] to solid` — 仅 after **passed** |
| **Continue** | `Study continue: <domain>` |
| **Evidence** | 按需 — 核对原文 |

Full spec: [REVIEW.md](REVIEW.md) · 卡住: [references/study-diagnosis.md](references/study-diagnosis.md)

### Frontmatter

| Field | Meaning |
|-------|---------|
| `reviewed` | Explain-back 结束时自动写 |
| `explain_back` | `not_started` · `attempted` · `passed` |
| `mastery` | `learning` · `solid` |
| `updated` | 页被改 — 若 **>** `reviewed` → 建议 cold 重测 |
| `external_checked` | 外搜确认 External 的日期 |

### Review queue

```
Review queue: cisco-aci
```

或：`python3 ~/zhuomo/scripts/lint-review-queue.py <vault>/wiki`

---

## 6. Lint vs Revise vs 外搜

见 §1.7–1.9 图。

| | **Lint** | **外搜** | **Revise** |
|---|----------|----------|------------|
| **Purpose** | 分级体检 | 保鲜时效事实 | 改具体错/加厚 Claim |
| **Trigger** | `Lint` | 过时 domain/概念 | 你发现错；Study gap |
| **Claim** | 只建议 | **待确认** 才改 | 直接改 corpus |
| **Web** | No | Yes | 仅当你给新来源 |

```
Lint → MISSING_EXTERNAL → 外搜 cisco-sdwan → 确认 Claim → Explain-back cold
```

---

## 7. Daily habits

- `raw/inbox/` 丢 capture
- `domains/<slug>/study` 看 **下一步** — 一行 concept
- `Explain-back cold` 或 `Study continue: <domain>`
- 每周或 ingest 后：`Lint`

---

## 8. Operations reference

**Verbs:** Bootstrap · **Adopt** · Ingest · **Ingest continue** · Query · 外搜 · Revise · Study · **Study continue** · Lint · Connect

| Verb | Examples | Output |
|------|----------|--------|
| **Bootstrap** | `Bootstrap: raw …, vault …` | Skeleton + config |
| **Adopt** | `Adopt vault: …` | Non-destructive merge |
| **Ingest** | `Ingest: book.epub` | Concepts + source status |
| **Ingest continue** | `Ingest continue: slug` | Resume `next_sections` |
| **Query** | `Query think: …` | Answer + Gaps + optional Apply |
| **外搜** | `外搜 cisco-aci` | External + 确认 Claim |
| **Study** | cold / feynman / Promote / continue | Mastery |
| **Revise** | `Revise [[page]] — …` | Fixed corpus |
| **Lint** | `Lint` | Tiered report |
| **Connect** | `Connect: … — 记入 synthesis` | `notes/synthesis/` |

---

## 9. Prompt cookbook

### Bootstrap / Adopt / maintenance

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, Obsidian vault ~/path/to/vault
/zhuomo Adopt vault: ~/path/to/existing/vault
/zhuomo Process everything in ~/zhuomo-data/raw/inbox/
/zhuomo Lint
```

### Study

```
Explain-back [[aci-border-leaf-l3out]] cold
Explain-back [[aci-border-leaf-l3out]] feynman
Study continue: kubernetes-cilium
Promote [[aci-spine-leaf-topology]] to solid
Review queue: cisco-aci
```

### Ingest

```
/zhuomo Ingest raw/ddia.epub
/zhuomo Ingest continue: ddia
/zhuomo Ingest overview only: huge-book.epub
/zhuomo Ingest: ~/raw/video/lecture.srt
/zhuomo Ingest: lecture.srt — deepen 前 3 章主题
```

### Query + Apply

```
/zhuomo Query think: Multi-Pod vs Multi-Site?
/zhuomo Query think: 现场 vManage 和 OMP 对不上，wiki 里 [[sdwan-omp-routing]] 怎么用？双 ISP 只有一侧 flap。
```

### 外搜 / Connect / Revise

```
/zhuomo 外搜 cisco-sdwan
/zhuomo 外搜 [[sdwan-architecture-planes]]
/zhuomo Connect: Cilium overlay vs ACI — 记入 synthesis
/zhuomo Revise [[bgp]] — 我的想法：…
```

---

## 10. Domain frameworks and progress

四页模型见 §1.11。

**Grasped** = Tier A 全 `explain_back: passed`。进度在 `study.md` Dataview **下一步** 列 — 不要手改大表。

```
/zhuomo Promote [[aci-spine-leaf-topology]] to solid
```

Detail: [LEARNING.md](LEARNING.md) · [REVIEW.md](REVIEW.md#progress-in-obsidian-dataview)

---

## 11. Optional Cursor skills

**Not a zhuomo verb.** Wiki first; skill in separate chat:

```
根据 wiki/domains/cisco-aci/overview.md 建 network-expert skill，
WIKI-SCOPE 写读哪些页；事实留在 wiki。
```

[WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md)

---

## 12. Multi-device workflow

| Device | Do | Don't |
|--------|-----|--------|
| **Phone** | `raw/inbox/`; read wiki | Heavy ingest |
| **Laptop** | Ingest, Revise, Adopt, Lint | — |

```
/zhuomo Process raw/inbox/
```

---

## 13. Source types

| Source | Raw | Ingest 默认 |
|--------|-----|-------------|
| EPUB / PDF | `raw/books/` | md corpus + deepen concepts |
| Web / article | `raw/web/` | 按大小 reference 或 overview |
| **SRT / VTT** | `raw/video/` | **语料 only**；deepen 需明说 |
| Readwise | `raw/inbox/` | → concepts |
| 年鉴/手册 | `raw/books/` | `archive only` 常见 |

Classes: study-technical · study-analytic · craft-narrative · literary-appreciation · reference-lookup · **transcript** — 见 [references/ingest-depth-and-resume.md](references/ingest-depth-and-resume.md)

---

## 14. Troubleshooting

| Problem | Fix |
|---------|-----|
| Claim 像导读 | `Revise [[slug]]` — 可理解层+正式层 |
| Explain-back 反复不过 | [study-diagnosis](references/study-diagnosis.md) — 别只会 feynman |
| 外搜改了 Claim 但你没同意 | 应出现「待确认」— 回复 `确认 Claim` |
| Adopt 覆盖了笔记 | 应用 Adopt 而非 Bootstrap；检查 adopt-check |
| 大书一次做不完 | `Ingest continue: <slug>` + source 页 `next_sections` |
| 字幕变成 50 个 concept | 默认 transcript 只语料；deepen 需你指定 |
| Lint 叫删页 | **不要**自动删 — 读两页再 merge |
| `solid` too early | 仅 **Promote** after passed |

---

## 15. FAQ

**Bootstrap 和 Adopt 区别？**  
Bootstrap = 空库新建。Adopt = 已有 vault 只加琢磨模板与 config，不改 corpus。

**Ingest continue 怎么知道续哪？**  
看 `wiki/sources/<slug>.md` 的 `ingest_status` / `next_sections`；或 `Lint` / `lint-ingest-resume.py`。

**Query 和 Apply？**  
Query 答 wiki；消息里带 **真实场景** 时多一块 **Apply**（判断+验证），默认不写回 wiki。

**手绘图在哪？**  
`assets/diagrams/*.svg`（Pastel 色 + 抖线滤镜，类似 Excalidraw）。GitHub / Obsidian 预览 `USER-GUIDE.md` 即可见。改布局：编辑 `scripts/generate-sketch-diagrams.py` 后运行 `python3 scripts/generate-sketch-diagrams.py`。

**Agent 读哪份 spec？**  
[SKILL.md](SKILL.md) 路由 + `references/` 细节。

---

## Document index

| File | Use when |
|------|----------|
| [USER-GUIDE.md](USER-GUIDE.md) | **This guide** — 图式 + 全流程 |
| [REVIEW.md](REVIEW.md) | Study, Explain-back, Dataview |
| [LEARNING.md](LEARNING.md) | Connect, domain 四页 |
| [SKILL.md](SKILL.md) | Agent 路由 |
| [references/](references/) | Agent 专项方法 |
| [SIMPLE.md](SIMPLE.md) | 最小路径 |
| Obsidian `wiki/help.md` | 日常 cheatsheet |
