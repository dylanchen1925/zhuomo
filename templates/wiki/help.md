---
type: help
updated: 2026-06-14
---

# Zhuomo 怎么用

**日常只看这一页。** 仓库：`SIMPLE.md`、`REVIEW.md`（Study + Dataview 进度）。

---

## 六个动词

| 动词 | 说 | 产出 |
|------|-----|------|
| **Bootstrap** | `Bootstrap + ingest: 书.epub` | 建库 + 第一本书 |
| **Ingest** | `Ingest: …` | concepts + Evidence + Explain-back |
| **Query** | `Query: …` | 答案 + Gaps |
| **Revise** | `Revise [[页]] — …` | 改 wiki |
| **Study** | 见下表 | 掌握度 |
| **Lint** | `Lint` | 健康问题 + 待复习列表 |

**Weekly（可选）：** 约 15 分钟的 `Lint` + 建议做一次 Explain-back。不必固定每周；随时 `Lint` / `Study` 即可。

**默认 Ingest：** deepen 全书。轻量：`Ingest overview only: …`

---

## Study（按 concept 学习）

| 我想… | 说 |
|-------|-----|
| 标记读过了 | `Review [[概念]]` |
| 讲回来测掌握 | `Explain-back [[概念]]` |
| 待复习列表 | `Review queue: cisco-aci` |
| 升掌握度 | `Promote [[概念]] to solid` |

Agent 改页会更新 `updated`；你读完打 `reviewed`。`updated > reviewed` → 该再读。

---

## Obsidian 进度（Dataview）

打开 `domains/<学科>/overview` → **学习进度** 表自动列出该学科所有 concept 的 `mastery` / `reviewed` / `explain_back`。

需要安装 **Dataview** 插件。勿手改大表；改 concept 页 frontmatter 即可。

---

## 常用指令

```
Ingest: ~/zhuomo-data/raw/inbox/book.epub
Query think: Multi-Pod vs Multi-Site?
Explain-back [[aci-border-leaf-l3out]]
Lint
Learn fable: [[aci-tenant-epg-contract]]
```

---

## 看哪里

| 问题 | 打开 |
|------|------|
| 学科列表 | [[overview]] |
| 进度 + 术语 | `domains/<学科>/overview` |
| 概念索引（非全文） | `domains/<学科>/guide` |
| 概念正文 + Explain-back | `concepts/` |
| 听不懂时的故事 | `learn/fables/`（可选） |
| 日志 | [[log]] |

---

## 原始资料

`~/zhuomo-data/raw/inbox/` — 手机丢 inbox，笔记本 ingest。
