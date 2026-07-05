#!/usr/bin/env python3
"""Ingest zartbot FreeWeChat corpus into Obsidian wiki (source + selective deepen)."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

VAULT = Path(
    "/Users/xinjchen/Library/Mobile Documents/iCloud~md~obsidian/Documents/Dylan Chen/wiki"
)
RAW = Path.home() / "zhuomo-data/raw/web/zartbot"
SLUG = "zartbot"
TODAY = date.today().isoformat()

SERIES_RULES: list[tuple[str, str]] = [
    (r"^Tensor-\d", "Tensor / CUTLASS / CuTe 系列"),
    (r"DeepEP|deepep|3FS|3fs", "DeepEP · 3FS · DeepSeek 基础设施"),
    (r"DeepSeek|MoE|moe", "DeepSeek · MoE · 推理分析"),
    (r"Hopper|Blackwell|Rubin|GPU架构|TensorCore|GEMM", "GPU 微架构与算子"),
    (r"RDMA|NCCL|ScaleUP|ScaleOut|互联|UALink|ESUN|NVLink", "互联 · RDMA · Scale-up/out"),
    (r"Agent|Attention|Transformer|LLM|大模型", "LLM 架构与算法"),
    (r"推理|Prefill|KV", "推理与 serving"),
]

CONCEPTS: list[dict] = [
    {
        "slug": "ai-deepep-expert-parallelism",
        "domain": "ai-systems-performance",
        "title": "DeepEP expert parallelism",
        "claim": (
            "**DeepEP** 是 DeepSeek 为 MoE **expert parallelism (EP)** 定制的通信库："
            "dispatch/combine 走 GPU 发起的 RDMA（IBGDA / NVSHMEM），"
            "用 **all-to-all** 语义在节点间搬运 expert token，"
            "并与计算 overlap；设计取舍与通用 NCCL collectives 不同。"
        ),
        "explain": [
            "*DeepEP dispatch/combine 与 NCCL all-to-all 的分工差异？*",
            "*为什么 DeepEP 强调 IBGDA / AR，而不是纯 RC Verbs？*",
            "*EP 通信如何与 GEMM 做细粒度 overlap（对比 Comet）？*",
        ],
        "evidence": [
            ("DeepEP 与 RDMA 多路径", "2025-03-07-rdma这十年的反思4-从deepseek的3fs和deepep谈起.md", "从DeepSeek的3FS和DeepEP谈起"),
            ("eRDMA 视角 DeepEP", "2025-03-18-再以erdma的视角谈谈deepep和3fs.md", "关于DeepEP为什么要用AR和IBGDA"),
            ("MoE comm overlap", "2025-03-06-谈谈字节的comet-另一个细粒度的moe通信和计算overlap方案.md", "通信上和DeepSeek DeepEP一样"),
        ],
    },
    {
        "slug": "ai-deepseek-3fs-storage",
        "domain": "ai-systems-performance",
        "title": "DeepSeek 3FS distributed storage",
        "claim": (
            "**3FS** 是 DeepSeek 面向 AI 训练/推理的分布式文件系统："
            "客户端通过 RDMA 访问元数据与数据面，"
            "与 **DeepEP** 同属「训练数据面 + EP 通信面」基础设施；"
            "写路径与元数据服务是性能关键。"
        ),
        "explain": [
            "*3FS 数据面与元数据面如何分工？*",
            "*3FS 写性能优化的主要瓶颈是什么？*",
            "*3FS 与 GDS / 传统 NFS 在 AI 负载下的差异？*",
        ],
        "evidence": [
            ("3FS 概述", "2025-03-01-基于erdma实测deepseek开源的3fs.md", "DeepSeek 3FS分布式存储概述"),
            ("写性能难点", "2025-03-21-谈谈3fs的写性能优化的难点.md", "谈谈3FS的写性能优化的难点"),
            ("上云挑战", "2025-03-29-从3fs性能谈谈数据密集型应用上云的挑战和机会.md", "数据密集型应用上云"),
        ],
    },
    {
        "slug": "ai-hopper-gemm-persistent-kernel",
        "domain": "ai-systems-performance",
        "title": "Hopper GEMM and persistent kernels",
        "claim": (
            "Hopper 上高性能 GEMM 需同时处理 **Tile/Wave quantization**、"
            "**CTA swizzle（L2 局部性）** 与 **Persistent Kernel（跨 wave 任务调度）**；"
            "CuteDSL/CUTLASS 将 tile 调度参数与 kernel 生命周期解耦。"
        ),
        "explain": [
            "*Tile quantization 与 Wave quantization 分别浪费在哪一层？*",
            "*Persistent Kernel 如何解决尾 wave SM 空闲？*",
            "*CTA swizzle 提升 L2 命中率的条件？*",
        ],
        "evidence": [
            ("Hopper 架构 TMA", "2022-09-07-gpu架构演化史14-hopper架构详解.md", "TMA"),
            ("TensorCore 编程", "2024-08-10-tensor-004-tensorcore编程及优化.md", "TensorCore编程及优化"),
            ("Tensor Copy", "2024-09-14-tensor-010-tensor-copy.md", "Tensor Copy"),
        ],
    },
    {
        "slug": "ai-moe-dispatch-architecture",
        "domain": "ai-systems-performance",
        "title": "MoE dispatch and expert routing",
        "claim": (
            "MoE 训练/推理的性能瓶颈常在 **router → dispatch → expert GEMM → combine** 链路："
            "top-k 路由决定 all-to-all 流量形态；"
            "负载均衡、专家 prefetch 与通信-计算 overlap 是系统优化杠杆。"
        ),
        "explain": [
            "*MoE dispatch 与 combine 各解决什么问题？*",
            "*专家负载不均如何影响 EP 通信？*",
            "*Gate 预测下一层 top-k 以 prefetch 专家权重的可行性？*",
        ],
        "evidence": [
            ("MoE 数学基础", "2023-12-12-大模型时代的数学基础5-谈谈moe和mixtral-8x7b.md", "MoE概述"),
            ("专家 prefetch 脑洞", "2025-02-27-一个脑洞moe专家权重是否可以预测并prefetch.md", "Expert权重是否可以Prefetch"),
            ("DeepSeek MoE 负载均衡", "2025-02-12-详细谈谈deepseek-moe相关的技术发展.md", "MoE"),
        ],
    },
    {
        "slug": "ai-blackwell-tensorcore-arch",
        "domain": "ai-systems-performance",
        "title": "Blackwell Tensor Core architecture",
        "claim": (
            "**Blackwell** 延续 Tensor Core 代际演进："
            "微架构变更影响 GEMM tile 选择、FP8/FP4 路径与机架级 NVLink 拓扑；"
            "推理效率分析需把 **硬件峰值** 与 **MoE/EP 通信** 一并建模。"
        ),
        "explain": [
            "*Blackwell Tensor Core 相对 Hopper 的关键增量？*",
            "*DeepSeek V3/R1 在 Blackwell 上的瓶颈是算力还是通信？*",
            "*Rubin 机柜拓扑对 scale-up 意味着什么？*",
        ],
        "evidence": [
            ("Blackwell 概览", "2024-03-19-来谈谈英伟达的blackwell.md", "结论"),
            ("Blackwell TensorCore", "2025-01-25-blackwell-tensorcore架构.md", "Blackwell TensorCore架构"),
            ("Tensor-011", "2025-03-26-tensor-011-blackwell-tensorcore.md", "Blackwell TensorCore"),
        ],
    },
    {
        "slug": "ai-cute-cutlass-kernels",
        "domain": "ai-systems-performance",
        "title": "CuTe and CUTLASS kernel composition",
        "claim": (
            "**CUTLASS** 将 GEMM 抽象为 **Mainloop + Epilogue** 的可组合流水线；"
            "**CuTe** 用 layout 代数描述 thread/warp/block 级数据搬运；"
            "是 Tensor Core 手工调优与 CuteDSL 的高层接口基础。"
        ),
        "explain": [
            "*CUTLASS 中 Mainloop 与 Epilogue 各负责什么？*",
            "*CuTe layout 代数解决的核心问题？*",
            "*从 CUTLASS 到 CuteDSL 的抽象层次差异？*",
        ],
        "evidence": [
            ("CUTLASS 简介", "2024-08-20-tensor-005-cutlass简介.md", "CUTLASS计算流程抽象"),
            ("CuTe Layout", "2024-08-24-tensor-007-cute-layout简介.md", "Cute Layout简介"),
            ("可组合 Kernel", "2024-08-22-tensor-006-ai软硬件交互界面-可组合的kernel.md", "可组合的Kernel"),
        ],
    },
    {
        "slug": "ai-gpu-scaleup-interconnect",
        "domain": "ai-dc-networking",
        "title": "GPU scale-up interconnect (zartbot lens)",
        "claim": (
            "**Scale-up**（机架内内存语义互联）与 **scale-out**（RoCE/IB 训练 fabric）应协同设计："
            "UALink / ESUN / 以太网 scale-up 方案各有取舍；"
            "MoE EP 与 KV 传输对「先 scale-up 再 scale-out」假设提出挑战。"
        ),
        "explain": [
            "*Scale-up 与 scale-out 的边界在机架还是 pod？*",
            "*以太网 scale-up（如 EthZ 类方案）的协议层难点？*",
            "*GTC25 Rubin 互联与 UB-Mesh 类思路的异同？*",
        ],
        "evidence": [
            ("GTC25 GPU互联", "2025-03-30-从gtc25谈谈gpu互联.md", "Rubin"),
            ("以太网 ScaleUP", "2024-08-16-基于ethz的以太网scaleup互联方案.md", "EthernetZ协议规范"),
            ("GPU Scale-up 以太网", "2024-04-18-谈谈基于以太网的gpu-scale-up网络.md", "Scale-up"),
        ],
    },
    {
        "slug": "ai-deepseek-inference-efficiency",
        "domain": "ai-systems-performance",
        "title": "DeepSeek V3/R1 inference efficiency",
        "claim": (
            "DeepSeek V3/R1 **推理效率**需在 **prefill/decode 分离、MoE EP、"
            "KV cache 管理、量化路径** 上联合建模；"
            "版本迭代分析（v0.15→v0.17）显示瓶颈会随软件栈变化迁移。"
        ),
        "explain": [
            "*V3/R1 推理瓶颈如何在 prefill 与 decode 间切换？*",
            "*Blackwell 估计版本更新了哪些假设？*",
            "*满血版 R1 部署优化的关键配置项？*",
        ],
        "evidence": [
            ("推理分析 v1", "2025-03-14-deepseek-v3r1推理效率分析.md", "推理效率分析"),
            ("v0.17", "2025-03-16-deepseek-v3r1推理效率分析v017.md", "推理效率分析"),
            ("R1 部署", "2025-02-12-谈谈deepseek-r1满血版推理部署和优化.md", "推理部署和优化"),
        ],
    },
]

REVISE_CONCEPTS: list[dict] = [
    {
        "path": "concepts/ai-nccl-magnum-io.md",
        "evidence_rows": [
            ("DeepEP vs NCCL EP 路径", "[[sources/zartbot/md/2025-03-18-再以erdma的视角谈谈deepep和3fs.md#关于deepep为什么要用ar和ibgda]]"),
            ("RDMA RC 兼容与 EP", "[[sources/zartbot/md/2025-03-07-rdma这十年的反思4-从deepseek的3fs和deepep谈起.md#从deepseek的3fs和deepep谈起]]"),
        ],
    },
    {
        "path": "concepts/ai-training-parallelism.md",
        "evidence_rows": [
            ("MoE EP all-to-all", "[[sources/zartbot/md/2025-03-06-谈谈字节的comet-另一个细粒度的moe通信和计算overlap方案.md]]"),
            ("DeepEP dispatch", "[[ai-deepep-expert-parallelism]]"),
        ],
    },
    {
        "path": "concepts/ai-scale-up-systems.md",
        "evidence_rows": [
            ("GTC25 scale-up/out", "[[sources/zartbot/md/2025-03-30-从gtc25谈谈gpu互联.md]]"),
            ("以太网 GPU scale-up", "[[sources/zartbot/md/2024-04-18-谈谈基于以太网的gpu-scale-up网络.md]]"),
        ],
    },
]


def classify(title: str) -> str:
    for pat, label in SERIES_RULES:
        if re.search(pat, title, re.I):
            return label
    return "其他"


def symlink_corpus(md_dir: Path) -> list[dict]:
    md_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((RAW / "manifest.json").read_text(encoding="utf-8"))
    linked: list[dict] = []
    for row in manifest["articles"]:
        fname = row["file"]
        if fname in ("index.md", "manifest.json"):
            continue
        src = RAW / fname
        if not src.exists():
            continue
        dest = md_dir / fname
        if dest.exists() or dest.is_symlink():
            dest.unlink()
        dest.symlink_to(src.resolve())
        linked.append(row)
    return linked


def build_md_index(articles: list[dict]) -> str:
    by_series: dict[str, list[dict]] = {}
    for row in articles:
        by_series.setdefault(classify(row["title"]), []).append(row)

    lines = [
        "---",
        "type: source-md-corpus",
        f"source: {SLUG}",
        f"updated: {TODAY}",
        "---",
        "",
        f"# MD corpus — {SLUG}",
        "",
        f"**{len(articles)}** articles from zartbot 微信公众号 (FreeWeChat mirror).",
        "",
        "**Raw:** `~/zhuomo-data/raw/web/zartbot/`",
        "",
    ]
    for series in sorted(by_series, key=lambda s: (-len(by_series[s]), s)):
        lines.append(f"## {series}")
        lines.append("")
        lines.append("| Date | Title | File |")
        lines.append("|------|-------|------|")
        for row in sorted(by_series[series], key=lambda r: r.get("date", ""), reverse=True):
            lines.append(
                f"| {row.get('date', '')} | {row['title']} | [[{row['file']}]] |"
            )
        lines.append("")
    return "\n".join(lines)


def build_source_page(articles: list[dict]) -> str:
    topic_rows = [
        ("DeepEP · MoE EP 通信", "deepep / comet 文章", "—", "[[ai-deepep-expert-parallelism]]", "Create"),
        ("DeepSeek 3FS", "3fs 系列", "—", "[[ai-deepseek-3fs-storage]]", "Create"),
        ("Hopper GEMM / Persistent Kernel", "Tensor-103 / Hopper 系列", "—", "[[ai-hopper-gemm-persistent-kernel]]", "Create"),
        ("MoE dispatch / 路由", "MoE 基础 + prefetch", "—", "[[ai-moe-dispatch-architecture]]", "Create"),
        ("Blackwell / Rubin 架构", "Blackwell / GTC 文章", "—", "[[ai-blackwell-tensorcore-arch]]", "Create"),
        ("CuTe / CUTLASS", "Tensor-005–011", "—", "[[ai-cute-cutlass-kernels]]", "Create"),
        ("Scale-up / GPU 互联", "GTC / EthZ / scale-up", "[[ai-scale-up-systems]]", "[[ai-gpu-scaleup-interconnect]]", "Create + Revise"),
        ("DeepSeek 推理效率", "V3/R1 分析系列", "—", "[[ai-deepseek-inference-efficiency]]", "Create"),
        ("NCCL / RDMA 栈", "RDMA 反思 / NCCL", "[[ai-nccl-magnum-io]]", "—", "Revise"),
    ]
    table = "\n".join(
        f"| {t} | {e} | {ex} | {c} | {a} |" for t, e, ex, c, a in topic_rows
    )
    return f"""---
type: source
publisher: zartbot 微信公众号
ingested: {TODAY}
domain: ai-systems-performance
epistemic: practitioner-analysis
audience: ai-systems-performance-engineers
class: study-technical
depth: selective-deepen
---

# Source — zartbot 微信公众号

- **作者:** zartbot（渣B / 扎波特）
- **Raw:** `~/zhuomo-data/raw/web/zartbot/`
- **MD corpus:** [[sources/{SLUG}/md/index]] — {len(articles)} articles
- **Scope:** AI Infra 一线实践 — GPU 微架构、CUTLASS/CuTe、MoE/DeepEP、3FS、NCCL/RDMA、Scale-up/out、DeepSeek 推理分析
- **Complements:** [[sources/ai-systems-performance-engineering]] · [[sources/ai-data-center-network-design]]

## Summary

zartbot 是中文 AI 系统圈深度技术博客，偏 **NVIDIA 栈 + DeepSeek 开源栈** 的源码级分析。
本次 ingest：**archive 全量 md corpus** + **selective deepen 8 支柱概念**（MoE EP、3FS、Hopper GEMM、Blackwell、CuTe、互联、推理效率）。

## Topic map

| Topic | Evidence | Existing wiki? | Wiki concept | Action |
|-------|----------|----------------|--------------|--------|
{table}

## Deepen status

**{TODAY}:** selective deepen — 8 new concepts; revise [[ai-nccl-magnum-io]] · [[ai-training-parallelism]] · [[ai-scale-up-systems]].

## Related

- Domain: [[domains/ai-systems-performance/overview]] · [[domains/ai-dc-networking/overview]]
- 系列索引: [[sources/{SLUG}/md/index]]
"""


def concept_page(c: dict) -> str:
    explain = "\n".join(f"{i}. {q}" for i, q in enumerate(c["explain"], 1))
    evidence = "\n".join(
        f"| {label} | [[sources/{SLUG}/md/{fname}#{slugify(anchor)}]] |"
        for label, fname, anchor in c["evidence"]
    )
    return f"""---
domain: {c['domain']}
mastery: learning
reviewed:
explain_back: not_started
updated: {TODAY}
wiki_revised: {TODAY}
origin: zhuomo
---

# {c['title']}

## Claim

{c['claim']}

## Explain-back

{explain}

## Evidence

| 要点 | 原文 |
|------|------|
{evidence}

## Sources

- **zartbot corpus:** [[sources/{SLUG}/md/index]]
- **Raw:** `~/zhuomo-data/raw/web/zartbot/`
"""


def slugify_anchor(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text or "section"


# alias for evidence anchor helper
slugify = slugify_anchor


def append_evidence(concept_path: Path, rows: list[tuple[str, str]]) -> None:
    text = concept_path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    block = "\n".join(f"| {label} | {link} |" for label, link in rows)
    if "## Evidence" in text:
        text = text.replace(
            "## Evidence\n\n| 要点 | 原文 |\n|------|------|",
            f"## Evidence\n\n| 要点 | 原文 |\n|------|------|\n{block}",
            1,
        )
    else:
        text += f"\n## Evidence\n\n| 要点 | 原文 |\n|------|------|\n{block}\n"
    text = re.sub(
        r"^updated:.*$",
        f"updated: {TODAY}",
        text,
        count=1,
        flags=re.M,
    )
    concept_path.write_text(text, encoding="utf-8")


def patch_domain_overview() -> None:
    path = VAULT / "domains/ai-systems-performance/overview.md"
    text = path.read_text(encoding="utf-8")
    bullet = f"- [[sources/{SLUG}]] — zartbot 公众号（MoE/DeepEP/GPU 微架构）"
    if bullet not in text:
        text = text.replace(
            "- [[sources/ai-systems-performance-engineering]] — AI goodput / GPU 栈",
            "- [[sources/ai-systems-performance-engineering]] — AI goodput / GPU 栈\n" + bullet,
        )
        path.write_text(text, encoding="utf-8")


def append_log(n_concepts: int, n_articles: int) -> None:
    log = VAULT / "log.md"
    entry = f"""
## [{TODAY}] ingest | zartbot 微信公众号 | {n_concepts} concepts selective deepen

- **Raw:** `~/zhuomo-data/raw/web/zartbot/` — {n_articles} articles
- **Corpus:** [[sources/{SLUG}/md/index]]
- **Concepts:** `ai-deepep-expert-parallelism` · `ai-deepseek-3fs-storage` · `ai-hopper-gemm-persistent-kernel` · `ai-moe-dispatch-architecture` · `ai-blackwell-tensorcore-arch` · `ai-cute-cutlass-kernels` · `ai-gpu-scaleup-interconnect` · `ai-deepseek-inference-efficiency`
- **Revise:** [[ai-nccl-magnum-io]] · [[ai-training-parallelism]] · [[ai-scale-up-systems]]
"""
    content = log.read_text(encoding="utf-8")
    if f"ingest | zartbot" not in content:
        # insert after header
        parts = content.split("\n", 2)
        if len(parts) >= 2:
            new_content = parts[0] + "\n" + parts[1] + "\n" + entry + (parts[2] if len(parts) > 2 else "")
        else:
            new_content = content + entry
        log.write_text(new_content, encoding="utf-8")


def append_index() -> None:
    index = VAULT / "index.md"
    lines = [
        f"- [[sources/{SLUG}]] — zartbot 微信公众号",
    ]
    for c in CONCEPTS:
        lines.append(f"- [[{c['slug']}]] — {c['title']}")
    block = "\n".join(lines)
    text = index.read_text(encoding="utf-8")
    if f"[[sources/{SLUG}]]" not in text:
        marker = "## Sources"
        if marker in text:
            text = text.replace(marker, marker + "\n\n### zartbot\n\n" + block + "\n", 1)
        else:
            text += f"\n\n### zartbot\n\n{block}\n"
        index.write_text(text, encoding="utf-8")


def fix_evidence_filenames() -> None:
    """Map concept evidence to files that exist (fuzzy match)."""
    md_dir = VAULT / "sources" / SLUG / "md"
    existing = {p.name.lower(): p.name for p in md_dir.glob("*.md")}
    for c in CONCEPTS:
        fixed = []
        for label, fname, anchor in c["evidence"]:
            key = fname.lower()
            if key not in existing:
                # try partial match
                base = fname.replace(".md", "").lower()
                matches = [v for k, v in existing.items() if base[:20] in k]
                fname = matches[0] if matches else fname
            fixed.append((label, fname, anchor))
        c["evidence"] = fixed


def main() -> None:
    if not VAULT.is_dir():
        sys.exit(f"Vault not found: {VAULT}")
    if not (RAW / "manifest.json").is_file():
        sys.exit(f"Run freewechat-to-wiki-md.py first: {RAW}")

    md_dir = VAULT / "sources" / SLUG / "md"
    articles = symlink_corpus(md_dir)
    fix_evidence_filenames()

    (md_dir / "index.md").write_text(build_md_index(articles), encoding="utf-8")
    (VAULT / "sources" / f"{SLUG}.md").write_text(
        build_source_page(articles), encoding="utf-8"
    )

    concepts_dir = VAULT / "concepts"
    for c in CONCEPTS:
        (concepts_dir / f"{c['slug']}.md").write_text(
            concept_page(c), encoding="utf-8"
        )

    for rev in REVISE_CONCEPTS:
        path = VAULT / rev["path"]
        if path.is_file():
            append_evidence(path, rev["evidence_rows"])

    patch_domain_overview()
    append_log(len(CONCEPTS), len(articles))
    append_index()

    print(f"Ingested {len(articles)} articles → {md_dir}")
    print(f"Created {len(CONCEPTS)} concepts; revised {len(REVISE_CONCEPTS)} pages")


if __name__ == "__main__":
    main()
