# 琢磨 (Zhuomo)

[English](README.md)

**把书、文章和笔记，变成你真正记得住的知识——以及 AI 代理能用的技能。**

> **琢磨** — 反复咀嚼、打磨材料，直到清晰可用。

---

## 从这里开始

| 你想… | 打开 |
|-------|------|
| **日常指令表（Obsidian）** | vault 里 `wiki/help.md` |
| **5 分钟入门** | [SIMPLE.md](SIMPLE.md) |
| **完整手册** | [USER-GUIDE.md](USER-GUIDE.md) |
| **Agent 规则** | [SKILL.md](SKILL.md) |

---

## 核心流程（4 + 1）

日常只需五个动词，其余都是加料。

| 步骤 | 怎么说 | 得到什么 |
|------|--------|----------|
| **Bootstrap** | `Bootstrap + ingest: book.epub` | 目录、`AGENTS.md`、首批 wiki |
| **Ingest** | `Ingest: 资料路径` | 概念页 + Evidence（默认 deepen 全部） |
| **Query** | `Query: 你的问题` | 合成答案 + Gaps |
| **Revise** | `Revise [[页]] — 错在哪` | 修正，不静默覆盖 |
| **Weekly**（可选） | `Weekly` | 约 15 分钟复习 + 巡检 |

**快速开始：**

```bash
ln -sf /path/to/zhuomo ~/.cursor/skills/zhuomo
```

```
/zhuomo Bootstrap + ingest: ~/zhuomo-data/raw/inbox/my-book.epub
/zhuomo Query: X 和 Y 什么关系？
/zhuomo Weekly
```

轻量模式：ingest 时加 `overview only`。完整 setup：[USER-GUIDE § 首次设置](USER-GUIDE.md#3-first-time-setup)

---

## 整体怎么运转

| 层级 | 位置 | 内容 |
|------|------|------|
| **Raw** | `~/zhuomo-data/raw/` | EPUB、摘录 — 不改 |
| **Wiki** | Obsidian `wiki/` | 概念、overview、摘要 |
| **Skills** | `~/.cursor/skills/` | 触发器 + 工作流（可选） |

**Wiki = 事实。Skill = 何时行动。** 先有 wiki，技法成熟再抽 skill。

---

## 进阶（需要时再开）

| 功能 | 怎么说 | 说明 |
|------|--------|------|
| **Learn** | `Learn fable: [[概念]]` | 寓言、摘要、闪卡 |
| **Lint** | `Lint` | wiki 健康检查（Weekly 已含） |
| **Review** | `Explain-back [[concept]]` | 按 concept 讲回来 — [REVIEW.md](REVIEW.md) |
| **Skill** | `Extract skill from [[概念]]` | Cursor 技能 |
| **Domain skill** | `Domain skill: xxx` | wiki 后端专家 |

---

## 目录结构

| 路径 | 作用 |
|------|------|
| 本仓库 | 技能文档 + `templates/AGENTS.md`、`templates/wiki/help.md` |
| Obsidian `wiki/help.md` | **日常指令表** |
| `~/zhuomo-data/raw/` | 原始资料 |
| Obsidian `wiki/` | 知识库 |

---

## 文档地图

| 文档 | 何时读 |
|------|--------|
| **`wiki/help.md`** | 每天在 Obsidian |
| [SIMPLE.md](SIMPLE.md) | 第一小时 |
| [USER-GUIDE.md](USER-GUIDE.md) | setup、习惯、排错 |
| [SKILL.md](SKILL.md) | 改 agent 行为 |
| [FRAMEWORK.md](FRAMEWORK.md) | 架构深读（可选） |

---

## 原则

1. **知识不是写一次就完** — 错了就 **Revise**。
2. **先 wiki 后 skill** — 技法验证过再固化。
3. **Query 先查 wiki** — 再查 web。
4. **一个 vault 多学科** — 每科 `domains/*/overview.md`。

---

## 许可与致谢

见 [SOURCES.md](SOURCES.md)。
