---
type: help
updated: 2026-06-01
---

# Zhuomo 怎么用

**日常只看这一页。** 仓库：`SIMPLE.md`、`REVIEW.md`（Study + Dataview 进度）。

---

## 六个动词

| 动词 | 说 | 产出 |
|------|-----|------|
| **Bootstrap** | `Bootstrap + ingest: 书.epub` | 建库 + 第一本书 |
| **Ingest** | `Ingest: …` | 按书类型选深度 — 见下表 |
| **Query** | `Query: …` | 答案 + Gaps + **Next step** |
| **Revise** | `Revise [[页]] — …` | 改 wiki；`我的想法` → `## My take` |
| **Study** | 见下表 | 掌握度 |
| **Lint** | `Lint` | 健康问题 + Solid 候选 + 读过未测 |

**Weekly（可选）：** `Lint` + 建议一次 Explain-back。

**Framework：** `sync-domain-study-paths.py` 更新学习路径与 Tier A/B/C/D。

---

## Ingest 按书类型（SKILL § Source types）

| 类型 | 例子 | 默认 |
|------|------|------|
| **IT / 工程** | 认证书、RFC | reference depth（全概念 + Evidence） |
| **政经史 / 社科** | 通史、政论、周期论 | reference depth 或 **selective deepen** |
| **写作技法** | 叙事、编剧 | reference depth |
| **小说 / 诗歌欣赏** | 消遣精读 | **overview only** 或 **archive only**；精读 → synthesis |
| **查阅型** | 年鉴、辞典 | **archive only** |

覆盖关键词：`继续` / `overview only` / `archive only` / `selective deepen` / `精读`

---

## Study（按 concept 学习）

| 我想… | 说 |
|-------|-----|
| 标记读过了 | `Review [[概念]]` |
| 讲回来测掌握 | `Explain-back [[概念]]` |
| 待复习列表 | `Review queue: cisco-aci` 或看 overview **待复习** Dataview |
| 升掌握度 | `Promote [[概念]] to solid`（须 `explain_back: passed`） |
| 我的想法写入 wiki | `Revise [[概念]] — 我的想法：…` 或 `Connect: … — 记入 synthesis` |

**Tier A**（overview §掌握度分层）= 建议 solid；不必全库 solid。

**Explain-back：** 每次 1 题 → 反馈 → 下一题。规范：`~/zhuomo/REVIEW.md`。

---

## Obsidian 进度（Dataview）

`domains/<学科>/overview` → **学习进度**：

- 全表 · **待复习** · **Solid 候选** · **读过未测** · **掌握度分层**

Lint 脚本也会打印：`SOLID_CANDIDATE` / `READ_UNTESTED` / …

---

## 常用指令

```
Ingest: ~/zhuomo-data/raw/inbox/book.epub
Query think: Multi-Pod vs Multi-Site?
Explain-back [[cilium-network-policy-identity]]
Promote [[k8s-network-visibility-gap]] to solid
Connect: Cilium 设计检查清单 — 记入 synthesis
Revise [[aci-tenant-epg-contract]] — 我的想法：…
Lint
Framework: kubernetes-cilium — tiers only
```

---

## 看哪里

| 问题 | 打开 |
|------|------|
| 学科列表 | [[overview]] |
| 进度 + Tier + 路径 | `domains/<学科>/overview` |
| 跨概念模型 | `wiki/synthesis/` |
| 概念 + My take | `concepts/` |
| 日志 | [[log]] |

---

## 原始资料

`~/zhuomo-data/raw/inbox/` — 手机丢 inbox，笔记本 ingest。
