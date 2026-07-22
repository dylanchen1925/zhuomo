---
type: help
updated: 2026-07-05
---

# Zhuomo 怎么用

**日常只看这一页。** 仓库：`SIMPLE.md`、`REVIEW.md`（Study 详规 + Dataview）。

---

## 学习链（Path → Test → Repeat）

```mermaid
flowchart TD
  A[新主题 / Tier A 概念] --> B["Explain-back cold 先测"]
  B --> C{passed?}
  C -->|否| D["读 Evidence 缺口 → feynman"]
  D --> B
  C -->|是| E[Promote solid]
  E --> F["Lint RETEST 30d → cold 复测"]
```

| 学习要素 | 琢磨动词 | 产出 |
|----------|----------|------|
| **Path** | `domains/<学科>/overview` · `study` | Tier A/B 顺序 + 进度表 |
| **Test（首次）** | `Explain-back [[概念]] cold` | 先答后看 Claim |
| **Test（复习）** | `Explain-back [[概念]]` | 已读过 concept 时用 |
| **深测** | `Explain-back [[概念]] feynman` | 小孩式追问 |
| **Repeat** | `Lint` · RETEST 桶 | solid 超 30 天 cold 复测 |

**15 分钟块：** cold → Evidence 补缺 → feynman → Promote。

---

## 今日 Study：顺序 + 进度

打开 `domains/<学科>/study` — **下一步** 列：

| 标记 | 你做什么 |
|------|----------|
| `① Promote` | `Promote [[概念]] to solid` |
| `② Explain-back` | `Explain-back [[概念]]` 或 `cold` |
| `③ Cold` | 未读或 wiki 更新后 → `Explain-back [[概念]] cold` |
| `—` | 暂无需动作 |

`reviewed` 由 Explain-back 会话自动写入，无需单独「标记已读」。

详规：`~/zhuomo/REVIEW.md`

---

## 七个动词

| 动词 | 说 | 产出 |
|------|-----|------|
| **Bootstrap** | `Bootstrap + ingest: 书.epub` | 建库 + 第一本书 |
| **Ingest** | `Ingest: …` | concepts + Evidence + Explain-back |
| **Query** | `Query: …` | 答案 + Gaps + Next step |
| **外搜** | `外搜 cisco-sdwan` / `外搜 [[概念]]` | Evidence 加 `External (YYYY)`；过时 Claim 修正 |
| **Revise** | `Revise [[页]] — …` | 改 corpus；`我的想法` → `notes/on-concept/` |
| **Study** | `cold` / `Explain-back` / `feynman` / `Promote` | 掌握度 |
| **Lint** | `Lint` | 健康 + Review 分桶 + External 扫描（默认一体） |

**Connect（个人模型）：** `Connect: … — 记入 synthesis` → `notes/synthesis/`（见下）

---

## Connect 是什么

聊透几个概念的关系后，把**你自己的**对照/模型记下来：

```
Connect: Cilium native routing 和 ACI L3Out 的相似点 — 记入 synthesis
```

→ Agent 写入 `wiki/notes/synthesis/<主题>.md`（`origin: personal`），链到相关 `[[concepts]]`。

**不是**改 corpus Claim；**不是** Ingest 自动写的 `wiki/synthesis/`（那是编译层）。

单概念想法用：`Revise [[概念]] — 我的想法：…` → `notes/on-concept/`。

---

## Study 指令速查

| 我想… | 说 |
|-------|-----|
| 第一次学（先测后读） | `Explain-back [[概念]] cold` |
| 复习已学概念 | `Explain-back [[概念]]` |
| 讲不清楚 | `Explain-back [[概念]] feynman` |
| 升掌握度 | `Promote [[概念]] to solid` |
| 下一项 | `domains/<学科>/study` **下一步** 列 |
| 跨概念个人模型 | `Connect: … — 记入 synthesis` |

---

## 常用指令

```
Ingest: ~/zhuomo-data/raw/inbox/book.epub
Query think: Multi-Pod vs Multi-Site?
外搜 cisco-aci
外搜 [[sdwan-architecture-planes]]
Explain-back [[cilium-network-policy-identity]] cold
Explain-back [[cilium-kube-proxy-replacement]] feynman
Promote [[k8s-network-visibility-gap]] to solid
Review queue: kubernetes-cilium
Lint
Connect: overlay vs native 选型 — 记入 synthesis
```

---

## 看哪里

| 问题 | 打开 |
|------|------|
| 学科列表 | [[domain-map]] · [[overview]] |
| 学习顺序 / 进度 | `domains/<学科>/overview` · `study` |
| 编译概念 | `concepts/` |
| 个人笔记 | `notes/` |
| 日志 | [[log]] |

---

## 原始资料

`~/zhuomo-data/raw/inbox/` — 手机丢 inbox，笔记本 ingest。
