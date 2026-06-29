---
type: help
updated: 2026-06-27
---

# Zhuomo 怎么用

**日常只看这一页。** 仓库：`SIMPLE.md`、`REVIEW.md`（Study 详规 + Dataview）。

---

## 今日 Study：顺序 + 待巩固

### 1. 打开学科 **study** 页（进度 + 待巩固）

`domains/<学科>/study` — **按 Tier A / B / 其余分表**：

| 区块 | 作用 |
|------|------|
| **待巩固** | 每 Tier：Solid 候选 · 读过未测 · 待复习 |
| **学习进度** | 每 Tier 全表（掌握度 / Review / Explain-back） |

`domains/<学科>/overview` — **建议学习顺序**（行内 **A** / **B** 标记）

Vault 总表：[[domain-map]] · [[overview]]

### 2. 待巩固（consolidate）— 按优先级做

| 优先级 | 列表在哪 | 你做什么 |
|--------|----------|----------|
| 1 | overview **Solid 候选** | `Promote [[概念]] to solid` |
| 2 | **读过未测** | `Explain-back [[概念]]`（读过 concept 但没 passed） |
| 3 | **待复习** | 重读 concept → `Review [[概念]]`（wiki 更新后） |
| 4 | 路径中下一个 **A** 仍未 solid | overview **建议学习顺序** → `study` 页对照 |

Lint 脚本同样分桶：`SOLID_CANDIDATE` / `READ_UNTESTED` / `STALE` — 说 `Lint` 或 `Review queue: <domain>`。

### 3. 怎么读 concept 页（Explain-back 考点从哪来）

concept 页 = **地图 + 结论**，不是全书。Explain-back 常考「连起来用」，不一定有单独一行答案。

**第一次学（标 A 的概念 / 新 ingest）：**

1. 先读 **Explain-back** 三题（当自测大纲）
2. **Claim** + 正文 + **Prerequisites** 链
3. 闭卷答不上 → 只点开对应 **Evidence** 一行（进 `sources/.../md/`）
4. `Review [[概念]]` → `Explain-back [[概念]]` → passed 再 `Promote`

**复习（已学过）：** 多数时候 **Claim + 正文** 够用；卡壳再开 Evidence。

**只查事实：** `Query: …` — 不必通读 concept；Next step 写 **够用** 即可。

| 情况 | 怎么办 |
|------|--------|
| 答案在正文，要自己推导 | 正常；Explain-back 就在测这个 |
| 答案在 Evidence 原文 | 点 Evidence 读对应段 |
| 页内 + Evidence 都没有 | wiki 质量问题 → `Revise [[概念]] — Explain-back 第 N 题缺依据` |

**不必**为学习回读 Raw EPUB；**不必**全库 solid — 路径里 **A** 即可。

### 4. 15 分钟一块（习惯）

1. overview **待巩固** 里选 1 个概念  
2. 读 Explain-back → Claim/正文（5–8 分钟）  
3. 闭卷答 → 卡壳开 1 条 Evidence  
4. `Explain-back [[概念]]` 或先 `Review`  

详规：`~/zhuomo/REVIEW.md` § How to read a concept page

---

## 六个动词

| 动词 | 说 | 产出 |
|------|-----|------|
| **Bootstrap** | `Bootstrap + ingest: 书.epub` | 建库 + 第一本书 |
| **Ingest** | `Ingest: …` | 按书类型选深度 — 见下表 |
| **Query** | `Query: …` | 答案 + Gaps + **Next step** |
| **Revise** | `Revise [[页]] — …` | 改 corpus；`我的想法` → `notes/on-concept/` |
| **Study** | `Review` / `Explain-back` / `Promote` | 掌握度 — 见上 §今日 Study |
| **Lint** | `Lint` | 健康问题 + 待巩固分桶 |

**Weekly（可选）：** `Lint` + 建议一次 Explain-back。

**Framework：** `sync-domain-study-paths.py` 更新学习路径、待巩固区块、Tier。

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

## Study 指令速查

| 我想… | 说 |
|-------|-----|
| 标记读过了 | `Review [[概念]]` |
| 讲回来测掌握 | `Explain-back [[概念]]` |
| 待巩固列表 | 看 overview **待巩固** 或 `Review queue: <domain>` |
| 升掌握度 | `Promote [[概念]] to solid`（须 `explain_back: passed`） |
| 我的想法 | `Revise [[概念]] — 我的想法：…` → `notes/on-concept/` |

**Explain-back：** 每次 1 题 → 反馈 → 下一题。

---

## 常用指令

```
Ingest: ~/zhuomo-data/raw/inbox/book.epub
Query think: Multi-Pod vs Multi-Site?
Explain-back [[cilium-network-policy-identity]]
Promote [[k8s-network-visibility-gap]] to solid
Review queue: kubernetes-cilium
Lint
Framework: kubernetes-cilium — tiers only
```

---

## 看哪里

| 问题 | 打开 |
|------|------|
| 学科列表 | [[overview]] · [[domain-map]] |
| **学习顺序** | `domains/<学科>/overview` |
| **进度 + 待巩固（Tier 分表）** | `domains/<学科>/study` |
| 编译：跨书主题 | `wiki/synthesis/` |
| 编译：概念 + Evidence | `concepts/` |
| 个人笔记 | `notes/` |
| 日志 | [[log]] |

---

## 原始资料

`~/zhuomo-data/raw/inbox/` — 手机丢 inbox，笔记本 ingest。
