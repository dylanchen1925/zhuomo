# Zhuomo 手绘风功能图

Excalidraw 风格的 **SVG** 示意图，供 [USER-GUIDE.md](../USER-GUIDE.md) 嵌入。

| 文件 | 说明 |
|------|------|
| `00-overview.svg` | 总览：raw → 动词 → wiki |
| `01-ingest.svg` | Ingest + continue + 外搜确认 |
| `02-study.svg` | Study + 卡住分支 |
| `03-query-waishou.svg` | Query / Apply / 外搜 |
| `04-domain-four-pages.svg` | domain 四页 |
| `05-lint-connect.svg` | Lint 四级 + Connect |

## 重新生成

```bash
python3 scripts/generate-sketch-diagrams.py
```

生成器使用：Pastel 填色、`feTurbulence` 抖线滤镜、手写体 font stack（Segoe Print / Bradley Hand）。

## 在文档里引用

```markdown
![说明](assets/diagrams/00-overview.svg)
```

Obsidian：若 SVG 不显示，用「在默认浏览器中打开」或复制 SVG 到 vault `assets/`。
