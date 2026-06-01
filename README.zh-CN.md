# 琢磨 (Zhuomo)

[English](README.md)

**把书、文章和笔记，变成你真正记得住的知识——以及 AI 代理能用的技能。**

丢进一份资料，得到 Obsidian 维基、闪卡、领域框架，以及（准备好时）Cursor 技能。把多个学科融进一个虚构场景时，学习甚至可以像 **Roguelike 游戏** 一样进行。

> **琢磨** — 反复咀嚼、打磨材料，直到清晰可用。

---

## 从这里开始

| 你想… | 打开 |
|-------|------|
| **日常 setup 和使用** | [USER-GUIDE.md](USER-GUIDE.md) |
| **理解整体架构** | [FRAMEWORK.md](FRAMEWORK.md) |
| **告诉 Agent 该做什么** | [SKILL.md](SKILL.md) |

---

## 快速开始（约 5 分钟）

**1. 安装技能** — 在本仓库路径处创建符号链接，让 Cursor 能发现：

```bash
ln -sf /path/to/zhuomo ~/.cursor/skills/zhuomo
```

**2. 初始化目录** — 在 Cursor 对话中：

```
/zhuomo Bootstrap: raw ~/zhuomo-data/raw/, Obsidian vault ~/Obsidian/zhuomo-vault
```

**3. 摄入第一份资料：**

```
/zhuomo Ingest: ~/zhuomo-data/raw/inbox/my-book.epub
```

Agent 会在 Obsidian 里创建维基页面。你阅读、学习、复习——发现错误时用 **Revise** 修正。

完整 setup：[USER-GUIDE § 首次设置](USER-GUIDE.md#3-first-time-setup)

---

## 整体怎么运转

原始资料保持不动。Zhuomo 把它们 **编译** 成可学习的维基，以及模式匹配时可调用的 Agent 技能。

![Zhuomo 系统概览 — 原始资料经 Zhuomo 流入 Obsidian 维基与 Cursor 技能](assets/framework-overview.png)

| 层级 | 位置 | 存放内容 |
|------|------|----------|
| **Raw（原始层）** | `~/zhuomo-data/raw/` | EPUB、摘录、转录 — 永不编辑 |
| **Wiki（维基层）** | Obsidian `wiki/` | 概念、框架、摘要、复习卡片 |
| **Skills（技能层）** | `~/.cursor/skills/` | 触发条件 + 工作流（可选领域专家） |

**Wiki = 事实与综合。Skill = 何时行动。** 常见路径：先有 wiki，技法成熟后再抽成 skill。

---

## 九大操作

你在 Zhuomo 里做的一切，都是下面这些「动词」之一。不必背——Agent 会从自然语言路由——但知道有哪些能力会很有帮助。

![Zhuomo 九大操作 — Ingest、Learn、Run、Review、Framework、Weekly、Query、Revise、Lint](assets/workflow-operations.png)

| 操作 | 你可以这样说… | 你会得到 |
|------|----------------|----------|
| **Ingest（摄入）** | 「摄入这本 EPUB」 | 维基概念页 |
| **Learn（学习）** | 「从这一章学习」 | 摘要、测验、复习卡片 |
| **Run（闯关）** | 「Run：融合 networking + psychology」 | Roguelike 场景 + 复盘 |
| **Review（复习）** | 「复习到期卡片」 | 间隔重复学习 session |
| **Framework（框架）** | 「更新我的 networking 框架」 | 支柱、缺口、进度 |
| **Weekly（周常）** | 「Weekly 仪式」 | 约 15 分钟复习 + 串联 |
| **Query（查询）** | 「X 和 Y 有什么关系？」 | 回答（可选写回 wiki） |
| **Revise（修订）** | 「这页错了」 | 修正后的页面，不静默覆盖 |
| **Lint（巡检）** | 「Lint 一下 wiki」 | 健康检查 → 待修清单 |

详情：[FRAMEWORK § 九大操作](FRAMEWORK.md#3-nine-operations) · Run 规范：[RUN.md](RUN.md)

---

## Roguelike 学习（Run）

当 flat 测验觉得无聊时，**Run** 把 2 个以上领域融进一个虚构场景。逐层爬楼、题目变难；解释不过关则「阵亡」结束本轮。虚构可以——**答案必须引用你的 wiki**。

![Roguelike 学习 Run — 楼层、融合领域、战利品即复习卡片](assets/roguelike-run.png)

```
/zhuomo Run: fuse networking + psychology — 5 floors, medium
```

产出写入 `wiki/learn/runs/`。完整指南：[USER-GUIDE § Roguelike 闯关](USER-GUIDE.md#16-roguelike-runs)

---

## 项目目录

| 路径 | 作用 |
|------|------|
| **本仓库**（你的 clone 路径） | 技能文档 + 可选配置 |
| `~/.cursor/skills/zhuomo` | 符号链接 → clone（Cursor 发现技能） |
| `~/zhuomo-data/raw/` | 资料 + `inbox/` *（bootstrap 时创建）* |
| `~/Obsidian/zhuomo-vault/wiki/` | 你的 wiki *（路径自定）* |

---

## 文档地图

**给你看**

| 文档 | 用途 |
|------|------|
| [USER-GUIDE.md](USER-GUIDE.md) | Setup、习惯、提示词手册、排错 |
| [FRAMEWORK.md](FRAMEWORK.md) | 概念模型 — 层级、操作、wiki vs skill |
| [RUN.md](RUN.md) | 多领域 Roguelike 闯关 |
| [RETENTION.md](RETENTION.md) | 间隔重复、周常仪式 |

**给你 + Agent**

| 文档 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | Agent 入口 — 工作流与规则 |
| [KNOWLEDGE-BASE.md](KNOWLEDGE-BASE.md) | Wiki 模式、Obsidian、多设备 |
| [LEARNING.md](LEARNING.md) | 学习模式、框架、多领域 |
| [WIKI-BACKED-SKILLS.md](WIKI-BACKED-SKILLS.md) | 以 wiki 为后端的领域专家 |
| [REFERENCE.md](REFERENCE.md) | EPUB、网页、视频、Readwise |

---

## 核心原则（简版）

1. **知识不是写一次就完** — 错了就 **Revise**，不要静默覆盖。
2. **Skill 不是读书笔记** — 而是触发器：*当 X 发生时，做 Y*。
3. **要学习，不要只归档** — 摘要、卡片、Run 胜过一大段文字堆砌。
4. **多领域、一个 vault** — 每域有框架，跨域做综合。

---

## 示例提示词

```
/zhuomo Ingest: ~/zhuomo-data/raw/inbox/article.md
/zhuomo Learn: digest + 10 recall cards for [[TCP congestion]]
/zhuomo Framework: update domains/networking after ingest
/zhuomo Run: random fuse, 3 floors, easy
/zhuomo Revise: [[old-page]] contradicts new source — merge and supersede
/zhuomo Weekly
```

更多：[USER-GUIDE § 提示词手册](USER-GUIDE.md#6-prompt-cookbook)

---

## 许可与致谢

设计参考个人 wiki 模式（Karpathy LLM Wiki）、间隔重复与 Agent 技能（Cursor）。详见 [SOURCES.md](SOURCES.md)。
