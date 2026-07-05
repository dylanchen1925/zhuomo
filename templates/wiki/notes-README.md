---
type: notes-hub
origin: personal
updated: 2026-06-22
---

# 个人笔记（Personal）

**与琢磨编译区分离。** Skill / Ingest 产出在 `concepts/`、`sources/`、`synthesis/`（`origin: zhuomo`）；**本目录由你书写**，Agent 仅在你说 `Revise … 我的想法`、**`Connect … 记入 synthesis`** 或 **「聊完总结成笔记」** 时协助。

## 放什么

| 子目录 | 用途 |
|--------|------|
| `inbox/` | 随手记、未整理片段 |
| `synthesis/` | **对话总结**（`Connect` / 聊完让 Agent 整理成文）— 跨概念模型、对标、类比 |
| `by-domain/<学科>/` | 按学科整理的笔记（可选） |
| `on-concept/<slug>.md` | 对单个 `[[concepts]]` 的补充想法（较短） |

**怎么选：** 聊完一整场、有多张表/图/竞品对比 → `synthesis/`；只评论一个概念 → `on-concept/`；还没想好放哪 → `inbox/`。

**示例：** [[notes/synthesis/cisco-sdn-policy-abstraction-by-scope]]

## 怎么链到编译区

- 在笔记里用 `[[concept-slug]]`、`[[sources/…]]`
- 编译区概念页可留一行：`## Personal notes` → `[[notes/on-concept/<slug>]]` 或相关 `[[notes/synthesis/…]]`

## 规范

- Frontmatter：`origin: personal`；对话总结加 `kind: chat-summary`
- **不要**把书单 Evidence 抄进个人笔记当事实；事实以 corpus 为准
- 琢磨 **不会** Ingest 进 `notes/`；你直接在 Obsidian 编辑即可

详见：`~/zhuomo/SKILL.md` § Corpus vs personal notes
