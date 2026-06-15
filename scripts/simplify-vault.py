#!/usr/bin/env python3
"""One-shot vault simplification: frontmatter, overviews (Dataview), slim guides, delete digests."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

DATAVIEW_BLOCK = """## 学习进度

> 需要 Obsidian **Dataview** 插件。进度来自 `wiki/concepts/` frontmatter（`mastery` · `reviewed` · `explain_back` · `updated`），勿手改下表。

```dataview
TABLE WITHOUT ID file.link AS "概念", mastery AS "掌握度", reviewed AS "Review", explain_back AS "Explain-back", updated AS "更新"
FROM "wiki/concepts"
WHERE domain = "{domain}"
SORT file.name ASC
```

**待复习**（`updated` 晚于 `reviewed` 或未读）：

```dataview
TABLE WITHOUT ID file.link AS "概念", reviewed, updated, explain_back
FROM "wiki/concepts"
WHERE domain = "{domain}" AND (reviewed = null OR (updated != null AND reviewed != null AND updated > reviewed))
SORT updated DESC
```
"""

GUIDES: dict[str, str] = {
    "cisco-aci": """---
domain: cisco-aci
type: guide
updated: 2026-06-14
---

# Cisco ACI — 概念索引

**细节在 concept 页，不在本页。** 本页 = 心智模型 + 按支柱跳转。

- **为什么学、术语、Dataview 进度** → [[domains/cisco-aci/overview]]
- **Explain-back** → 各 `wiki/concepts/aci-*` 内 `## Explain-back`

---

## 心智模型

**Underlay 运包 → Tenant 策略定谁跟谁说话 → APIC 写配置 → Endpoint DB 决定包往哪走。**

```mermaid
flowchart LR
  U[Underlay] --> A[Access] --> T[Tenant] --> E[L3Out]
  U --> M[Multi-Pod / Multi-Site]
```

---

## 支柱 → 概念页

| 支柱 | 入口概念 |
|------|----------|
| Topology | [[aci-spine-leaf-topology]] · [[aci-border-leaf-l3out]] |
| Underlay | [[aci-fabric-underlay]] · [[aci-leaf-forwarding-profile]] |
| Access | [[aci-vlan-pools-aaep]] · [[aci-vpc-design]] |
| Tenant | [[aci-tenant-epg-contract]] |
| Endpoint | [[aci-endpoint-learning-controls]] · [[aci-ip-dataplane-learning]] |
| L3Out | [[aci-border-leaf-l3out]] · [[aci-l3out-profiles]] · [[aci-infra-mp-bgp]] |
| Multi-Pod | [[aci-multi-pod]] · [[aci-multi-pod-overlay]] |
| Multi-Site | [[aci-multi-site]] · [[aci-nexus-dashboard-orchestrator]] |
| Remote / Ops | [[aci-remote-leaf]] · [[aci-telemetry-nexus-insights]] · [[aci-apic]] |

L3Out 子页：`aci-l3out-*`（BGP/OSPF/合约/Route map 等）— 从 [[aci-border-leaf-l3out]] 展开。

---

## 推荐顺序

拓扑 + APIC → Underlay + Profile → Access + vPC → Tenant → Endpoint → L3Out → Multi-* → **Explain-back** 逐 concept

---

## 踩坑速查

| 症状 | 常见原因 |
|------|----------|
| vPC F3274 | 重叠 VLAN pool / FD_VNID |
| 外部学不到子网 | 缺合约或 scope |
| Multi-Pod 组播不通 | IPN 未配 PIM-Bidir |
| 迁 GW 后黑洞 | endpoint 学习/老化未调 |
""",
    "ai-dc-networking": """---
domain: ai-dc-networking
type: guide
updated: 2026-06-14
---

# AI DC Networking — 概念索引

**细节在 concept 页。** 入口与 Dataview 进度 → [[domains/ai-dc-networking/overview]]

---

## 心智模型

并行训练 job → east–west RDMA 大象流 → ROD/RUD + 无损 RoCEv2 + 负载均衡降 JCT/tail latency → 百万 GPU 走向 UEC。

---

## 支柱 → 概念页

| 支柱 | 概念 |
|------|------|
| Workload | [[ai-dc-workload-lifecycle]] · [[ai-training-parallelism]] · [[ai-jct-tail-latency]] |
| Transport | [[ai-rdma-rocev2]] · [[ai-infiniband-vs-ethernet]] |
| Topology | [[ai-rail-optimized-design]] · [[ai-rail-unified-design]] · [[ai-dc-fabric-topologies]] · [[ai-scheduled-fabric]] |
| Physical | [[ai-dc-optics-cabling]] · [[ai-dc-thermal-cooling]] |
| Fabric | [[ai-fabric-load-balancing]] · [[ai-rocev2-congestion]] · [[ai-fabric-ip-routing]] |
| Storage / Ops | [[ai-dc-storage-networks]] · [[ai-fabric-monitoring-ifa]] · [[ai-mlcommons-benchmarking]] |
| Next-gen | [[ai-ultra-ethernet-consortium]] · [[ai-scale-up-systems]] · [[ai-training-vs-inference-dc]] |

---

## 推荐顺序

workload/KPI → RDMA → topology (ROD/RUD) → LB + congestion → IP/storage → UEC
""",
    "technical-analysis": """---
domain: technical-analysis
type: guide
updated: 2026-06-14
---

# Technical Analysis — 概念索引

**细节在 concept 页。** 入口与 Dataview 进度 → [[domains/technical-analysis/overview]]

---

## 心智模型

市场行为包容一切 → 价格以趋势演变 → 历史会重演；先判趋势与价格水平，再用形态/量/指标确认，最后资金管理与执行。

---

## 分析层级（自上而下）

| 层级 | 概念 |
|------|------|
| 框架 | [[ding-yin-yang-ta-foundation]] · [[ideal-trend-evolution-pattern]] · [[ta-three-analysis-levels]] |
| 哲学 / 趋势 | [[ta-theory-foundation]] · [[dow-theory]] · [[trend-definition-peak-trough]] |
| 图表 | [[chart-construction]] · [[trendlines-channels]] · [[percentage-retracements]] |
| 形态 | [[major-reversal-patterns]] · [[head-and-shoulders]] · [[continuation-patterns]] |
| 量 / 情绪 | [[volume-open-interest]] · [[sentiment-option-indicators]] · [[contrary-opinion]] |
| 指标 | [[moving-averages]] · [[oscillator-analysis]] · [[rsi-stochastic-macd]] |
| 另类图 | [[point-and-figure]] · [[candlestick-charts]] · [[ding-candlestick-trend-framework]] |
| 结构 / 周期 | [[elliott-wave-theory]] · [[cycle-analysis]] |
| 宏观 / 广度 | [[intermarket-analysis]] · [[stock-market-breadth-indicators]] |
| 执行 | [[computer-trading-systems]] · [[money-management-trading-tactics]] · [[ta-synthesis-checklist]] |
| 附录 | [[market-profile]] · [[trading-system-design]] |

---

## 推荐顺序

丁氏框架 → 道氏/趋势 → 图表与形态 → 量与指标 → 波浪/周期 → 市场间 → 资金管理 → **Explain-back** 逐 concept
""",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wiki_dir", type=Path)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def fm_val(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip().strip('"').strip("'")
    return v or None


def pick_updated(fm: str) -> str | None:
    candidates = []
    for key in (
        "updated",
        "wiki_revised",
        "revised",
        "deepened",
        "lint_corrected",
        "explain_back_date",
    ):
        v = fm_val(fm, key)
        if v and DATE_RE.match(v):
            candidates.append(v)
    return max(candidates) if candidates else None


def simplify_concept(path: Path, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FM_RE.match(text)
    if not m:
        return False
    fm, body = m.group(1), text[m.end() :]
    domain = fm_val(fm, "domain")
    mastery = fm_val(fm, "mastery") or fm_val(fm, "status") or "learning"
    reviewed = fm_val(fm, "reviewed")
    explain_back = fm_val(fm, "explain_back") or "not_started"
    updated = pick_updated(fm)

    lines = ["---"]
    if domain:
        lines.append(f"domain: {domain}")
    lines.append(f"mastery: {mastery}")
    if reviewed:
        lines.append(f"reviewed: {reviewed}")
    lines.append(f"explain_back: {explain_back}")
    if updated:
        lines.append(f"updated: {updated}")
    lines.append("---")
    new_text = "\n".join(lines) + "\n" + body
    if new_text != text:
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")
        return True
    return False


def replace_progress_section(overview: Path, domain: str, dry_run: bool) -> None:
    text = overview.read_text(encoding="utf-8")
    block = DATAVIEW_BLOCK.format(domain=domain)
    pat = re.compile(r"## (?:学习进度|进度)\n.*?(?=\n## |\n---\n\n## |\Z)", re.S)
    if pat.search(text):
        new_text = pat.sub(block + "\n", text, count=1)
    else:
        # insert before 尚未覆盖 / 术语 / Gaps
        ins = re.search(r"\n## (?:尚未覆盖|术语|Gaps|建议学习)", text)
        if ins:
            new_text = text[: ins.start()] + "\n\n" + block + "\n" + text[ins.start() :]
        else:
            new_text = text.rstrip() + "\n\n" + block + "\n"
    if new_text != text and not dry_run:
        overview.write_text(new_text, encoding="utf-8")


def rm_tree(path: Path, dry_run: bool) -> None:
    if not path.exists():
        return
    if dry_run:
        print(f"would delete {path}")
        return
    if path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)


def main() -> int:
    args = parse_args()
    wiki = args.wiki_dir.resolve()
    dry = args.dry_run
    n = 0
    for p in sorted((wiki / "concepts").glob("*.md")):
        if simplify_concept(p, dry):
            n += 1
    print(f"concepts simplified: {n}")

    for domain, content in GUIDES.items():
        guide = wiki / "domains" / domain / "guide.md"
        if guide.parent.is_dir():
            if not dry:
                guide.write_text(content.strip() + "\n", encoding="utf-8")
            print(f"guide slim: {guide}")

    for domain in GUIDES:
        ov = wiki / "domains" / domain / "overview.md"
        if ov.is_file():
            replace_progress_section(ov, domain, dry)
            print(f"overview dataview: {ov}")

    for d in ("digests", "reviews", "applied"):
        rm_tree(wiki / "learn" / d, dry)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
