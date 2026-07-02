"""Per-domain mastery tiers (A/B/C/D). Imported by sync-domain-study-paths.py — no PyYAML."""

from __future__ import annotations

import re
from typing import TypedDict


class TierSpec(TypedDict, total=False):
    a: list[str]
    a_label: str
    b: list[str]
    b_label: str
    c_note: str
    d_note: str


# Virtual domains: study/Dataview scope by concept filename (frontmatter domain: unchanged).
VIRTUAL_DOMAIN_SCOPE: dict[str, str] = {
    "campus-wireless": (
        '(startswith(file.name, "cwna-") OR startswith(file.name, "cwdp-") OR '
        'startswith(file.name, "enwl-") OR startswith(file.name, "cwsp-") OR '
        'startswith(file.name, "wng802-") OR startswith(file.name, "campus-wlan") OR '
        'file.name = "mrki-mr-wireless-design" OR file.name = "ccde-wireless-enterprise-design" OR '
        'file.name = "encor-enterprise-wireless")'
    ),
}


def concept_scope(domain: str) -> str:
    if domain in VIRTUAL_DOMAIN_SCOPE:
        return VIRTUAL_DOMAIN_SCOPE[domain]
    return f'domain = "{domain}"'


TIERS: dict[str, TierSpec] = {
    "kubernetes-cilium": {
        "a_label": "核心脊骨（建议 solid）",
        "a": [
            "k8s-network-visibility-gap",
            "k8s-pod-model",
            "linux-ebpf-fundamentals",
            "ebpf-program-anatomy",
            "cilium-cni-overview",
            "cilium-architecture",
            "cilium-ebpf-dataplane",
            "cilium-datapath-modes",
            "cilium-kube-proxy-replacement",
            "cilium-network-policy-identity",
            "cilium-network-policies-segmentation",
            "cilium-hubble-observability",
            "cilium-hubble-policy-workflow",
            "cilium-ipam",
            "cilium-operations",
        ],
        "b_label": "Cisco / DC 集成（场景 solid）",
        "b": [
            "cilium-cisco-hybrid-integration",
            "cilium-aci-basic-design",
            "cilium-aci-bgp-fabric-peering",
            "cilium-nxos-evpn-vxlan-k8s-design",
            "isovalent-network-bridge",
        ],
        "c_note": "扩展：`cilium-cluster-mesh`、`cilium-service-mesh`、`k8s-*` 网络工程、GenAI（`k8s-llm-*`/`k8s-ai-*`）、企业 SKU — **learning + Query**",
        "d_note": "索引：`msa-*`/`bm-*`/`pdds-*`/`dds-*`/`cndc-*`/`fs-ocp-*` — **不必 solid**",
    },
    "cisco-aci": {
        "a_label": "核心脊骨（建议 solid）",
        "a": [
            "aci-sdn-value-proposition",
            "aci-spine-leaf-topology",
            "aci-apic",
            "aci-fabric-underlay",
            "aci-vlan-pools-aaep",
            "aci-vpc-design",
            "aci-tenant-epg-contract",
            "aci-endpoint-learning-controls",
            "aci-border-leaf-l3out",
            "aci-infra-mp-bgp",
            "aci-l3out-profiles",
        ],
        "b_label": "Multi-DC / 运维（场景 solid）",
        "b": [
            "aci-multi-pod",
            "aci-multi-site",
            "aci-nexus-dashboard-orchestrator",
            "aci-telemetry-nexus-insights",
        ],
        "c_note": "`aci-l3out-*` 子页、集成（VMM/Service Graph）、Exam 运维章 — **learning + Query**",
        "d_note": "`dccor-*` 考试支线 — 按需 solid",
    },
    "cisco-sdwan": {
        "a_label": "全书建议 solid（仅 15 概念）",
        "a": [
            "sdwan-use-cases",
            "sdwan-architecture-planes",
            "sdwan-control-plane",
            "sdwan-data-plane-tloc",
            "sdwan-omp-routing",
            "sdwan-deployment-planning",
            "sdwan-edge-deployment",
            "sdwan-policies-qos",
            "sdwan-operations-telemetry",
            "sdwan-troubleshooting",
        ],
        "b": ["sdwan-control-deployment", "sdwan-orchestration-onboarding", "sdwan-firewall-ports-nat"],
        "b_label": "部署 / 安全细节",
        "c_note": "Lab：`sdwan-eve-ng-lab-topology` — 动手前 Review",
        "d_note": "—",
    },
    "ai-dc-networking": {
        "a_label": "核心脊骨（建议 solid）",
        "a": [
            "ai-dc-workload-lifecycle",
            "ai-training-parallelism",
            "ai-jct-tail-latency",
            "ai-rdma-rocev2",
            "ai-infiniband-vs-ethernet",
            "ai-rail-optimized-design",
            "ai-dc-fabric-topologies",
            "ai-fabric-load-balancing",
            "ai-rocev2-congestion",
            "ai-fabric-ip-routing",
            "ai-dc-storage-networks",
            "ai-fabric-monitoring-ifa",
        ],
        "b_label": "Cisco 蓝图（场景 solid）",
        "b": [
            "cisco-nexus-ai-blueprint",
            "cisco-nexus-ai-era-architecture",
            "cisco-msdc-ai-rail-plane-fabric",
            "cisco-aiml-vxlan-evpn-gpuaas",
        ],
        "c_note": "物理层、UEC、Hyperfabric 细节、NVMe 子页 — **learning + Query**",
        "d_note": "—",
    },
    "ai-systems-performance": {
        "a_label": "建议 solid（小域全覆盖）",
        "a": [
            "ai-goodput-metric",
            "ai-gpu-platform-tuning",
            "ai-nccl-magnum-io",
            "ai-pytorch-distributed-performance",
            "ai-inference-serving-at-scale",
        ],
        "b": ["ai-grace-blackwell-superchip", "ai-gds-storage-pipeline", "ai-cuda-roofline-occupancy"],
        "b_label": "硬件 / 内核深化",
        "c_note": "其余 `ai-*` — learning + Query",
        "d_note": "—",
    },
    "systems-performance": {
        "a_label": "核心脊骨（建议 solid）",
        "a": [
            "sysperf-systems-performance-fundamentals",
            "sysperf-performance-methodologies",
            "sysperf-linux-perf",
            "sysperf-cpu-performance",
            "sysperf-memory-performance",
            "sysperf-network-performance",
        ],
        "b": ["sysperf-bpf-ebpf-tooling", "sysperf-ftrace-tracing", "sysperf-benchmarking"],
        "b_label": "工具链 / 基准",
        "c_note": "磁盘/文件系统/云/应用章 — learning + Query",
        "d_note": "—",
    },
    "ai-emerging-tech": {
        "a_label": "建议 solid（7 概念全覆盖）",
        "a": [
            "ai-age-and-llm-foundations",
            "ai-in-computer-networking",
            "ai-in-cybersecurity",
            "ai-cloud-computing",
            "ai-collaboration-technologies",
            "ai-iot-aiot",
            "ai-emerging-technologies-frontier",
        ],
        "c_note": "—",
        "d_note": "—",
    },
    "technical-analysis": {
        "a_label": "Murphy 主线（建议 solid）",
        "a": [
            "ding-yin-yang-ta-foundation",
            "ta-theory-foundation",
            "dow-theory",
            "trend-definition-peak-trough",
            "chart-construction",
            "major-reversal-patterns",
            "volume-open-interest",
            "moving-averages",
            "money-management-trading-tactics",
            "ta-synthesis-checklist",
        ],
        "b_label": "A 股 / 缠论（场景 solid）",
        "b": [
            "xuesong-trading-mindset",
            "xuesong-mode-a-breakout",
            "chan-theory-framework",
            "chan-three-buy-sell-points",
        ],
        "c_note": "波浪/周期/指标细节、其余 `chan-*`/`xuesong-*` — learning + Query",
        "d_note": "附录类（`market-profile` 等）— 索引",
    },
    "macro-cycle-investing": {
        "a_label": "建议 solid（11 概念全覆盖）",
        "a": [
            "zhou-cycle-human-nature",
            "zhou-kondratiev-life-wave",
            "zhou-three-cycle-nesting",
            "zhou-juglar-capacity-cycle",
            "zhou-inventory-cycle",
            "zhou-kuznets-property-cycle",
            "zhou-merrill-clock-revision",
            "zhou-asset-allocation-framework",
        ],
        "b": ["zhou-commodity-kondratiev", "zhou-gold-in-kondratiev", "zhou-destiny-and-resistance"],
        "b_label": "资产定价深化",
        "c_note": "—",
        "d_note": "—",
    },
    "ip-routing": {
        "a_label": "核心脊骨（建议 solid）",
        "a": [
            "dynamic-routing-protocols",
            "eigrp",
            "ospfv2",
            "ospfv3",
            "integrated-is-is",
            "route-redistribution",
            "route-filtering",
            "route-maps",
            "bgp-introduction",
            "bgp-routing-policies",
            "choosing-ospf-vs-is-is",
        ],
        "b_label": "进阶 / 认证（场景 solid）",
        "b": ["bgp-scaling", "mp-bgp", "enarsi-route-redistribution", "enarsi-bgp-advanced"],
        "c_note": "组播 `cipm*`、Stevens `tcpip-illustrated-*`、TCP CC `tcpcc-*`、CENG — **learning + Query**",
        "d_note": "—",
    },
    "campus-wireless": {
        "a_label": "核心脊骨（建议 solid）",
        "a": [
            "cwna-wireless-standards-fundamentals",
            "cwna-rf-fundamentals",
            "cwna-ieee-80211-standards",
            "campus-wlan-fundamentals",
            "enwl-design-requirements",
            "enwl-site-survey",
            "cwdp-requirements-planning",
            "cwdp-site-survey-rf-design",
            "cwdp-wlan-security-design",
        ],
        "b_label": "CWNA / Cisco 设计深化（场景 solid）",
        "b": [
            "cwna-wlan-architecture",
            "cwna-80211-security-architecture",
            "enwl-radio-management",
            "enwl-wireless-security",
            "ccde-wireless-enterprise-design",
        ],
        "c_note": "其余 cwna-* / cwdp-* / enwl-* / wng802-* — **learning + Query**",
        "d_note": "—",
    },
    "network-architecture": {
        "a_label": "架构师核心（建议 solid）",
        "a": [
            "network-architect-role",
            "network-design-principles",
            "dc-spine-leaf-design-fork",
            "ccde-design-requirements-process",
            "ccde-enterprise-wan-architecture",
        ],
        "b_label": "Multi-Domain 集成（场景 solid）",
        "b": [
            "mdn-multi-domain-fundamentals",
            "mdn-aci-datacenter-integration",
            "mdn-sdwan-wan-integration",
            "mdn-sda-campus-integration",
            "mdn-cross-domain-security",
            "mdn-cloud-hybrid",
            "ccde-practical-exam-methodology",
        ],
        "c_note": "园区/ENS/SDA/自动化/专著 — 见 overview **Track 分流**；无线 → [[domains/campus-wireless/overview]] — **learning + Query**",
        "d_note": "单书边角 concept — 索引",
    },
    "network-security": {
        "a_label": "NS 核心 9（建议 solid）",
        "a": [
            "ns-security-introduction",
            "ns-security-design-principles",
            "ns-cryptographic-primitives",
            "ns-key-distribution",
            "ns-authentication-protocols",
            "ns-transport-security-tls",
            "ns-infrastructure-security",
            "ns-subsystem-security",
            "ns-firewalls-zero-trust",
        ],
        "b_label": "SCOR / CISE（按工作场景）",
        "b": [
            "scor-cybersecurity-fundamentals",
            "scor-cryptography-pki",
            "cise-platform-architecture",
            "cise-nac-policy-framework",
        ],
        "c_note": "其余 `scor-*`/`cise-*` — learning + Query",
        "d_note": "—",
    },
    "design-thinking": {
        "a_label": "建议 solid（10 概念全覆盖）",
        "a": [
            "design-thinking-overview",
            "design-thinking-principles",
            "design-thinking-empathy",
            "design-thinking-observation",
            "design-thinking-problem-reframe",
            "design-thinking-ideation",
            "design-thinking-evaluation-prototyping",
            "design-thinking-testing-implementation",
        ],
        "c_note": "其余 — learning",
        "d_note": "—",
    },
    "research-methods": {
        "a_label": "建议 solid（核心论证链）",
        "a": [
            "cor-thinking-in-print",
            "cor-research-argument-model",
            "cor-topic-to-question",
            "cor-claims-reasons-evidence",
            "cor-planning-drafting-citation",
            "cor-revising-argument",
        ],
        "b": ["cor-research-ethics", "cor-visual-evidence", "cor-reader-writer-roles"],
        "b_label": "伦理 / 呈现",
        "c_note": "来源检索与写作风格章 — learning + Query",
        "d_note": "—",
    },
    "model-thinking": {
        "a_label": "框架与高频模型（建议 solid）",
        "a": [
            "mt-multi-model-thinker",
            "mt-seven-uses-of-models",
            "mt-multi-model-thinking",
            "mt-modeling-human-agents",
            "mt-normal-distribution",
            "mt-power-law-distribution",
            "mt-nonlinear-models",
            "mt-network-models",
            "mt-broadcast-diffusion-contagion",
            "mt-random-walk",
            "mt-markov-models",
            "mt-system-dynamics",
            "mt-threshold-models",
            "mt-game-theory-models",
            "mt-cooperation-models",
            "mt-collective-action",
            "mt-multi-armed-bandit",
            "mt-practical-multi-model",
        ],
        "b": [
            "mt-value-and-power-models",
            "mt-mechanism-design",
            "mt-rugged-landscape",
        ],
        "b_label": "权力 / 机制 / 创新搜索",
        "c_note": "其余 Part 2 工具章 — learning + Query",
        "d_note": "—",
    },
    "hardware-defined-networking": {
        "a_label": "核心脊骨（建议 solid）",
        "a": [
            "hdn-foundation-principles",
            "hdn-forwarding-system-architecture",
            "hdn-forwarding-protocols",
            "hdn-overlay-protocols",
            "hdn-routing-hardware",
        ],
        "b": ["hdn-network-virtualization", "hdn-vpn", "hdn-qos-hardware"],
        "b_label": "虚拟化 / VPN / QoS",
        "c_note": "组播、连接、OAM、安全查找 — learning + Query",
        "d_note": "—",
    },
}


def wikilinks(slugs: list[str]) -> str:
    return " · ".join(f"[[{s}]]" for s in slugs)


def wikilinks_tier(slugs: list[str], tier: str) -> str:
    return " · ".join(f"[[{s}]] **{tier}**" for s in slugs)


WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")


def strip_study_heading(md: str) -> str:
    md = md.strip()
    for prefix in ("## 建议学习顺序", "## Study path"):
        if md.startswith(prefix):
            return md[len(prefix) :].lstrip("\n")
    return md


def slug_from_wikilink(target: str) -> str:
    return target.split("/")[-1].strip()


def slugs_in_path(body: str) -> set[str]:
    return {slug_from_wikilink(m.group(1)) for m in WIKILINK_RE.finditer(body)}


def annotate_tiers_in_path(body: str, spec: TierSpec) -> str:
    a = set(spec.get("a") or [])
    b = set(spec.get("b") or [])

    def repl(m: re.Match[str]) -> str:
        slug = slug_from_wikilink(m.group(1))
        link = m.group(0)
        if slug in a:
            return f"{link} **A**"
        if slug in b:
            return f"{link} **B**"
        return link

    return WIKILINK_RE.sub(repl, body)


def format_unified_study_order(path_body: str, spec: TierSpec) -> str:
    """Study path with inline **A** / **B** mastery markers; replaces separate §掌握度分层."""
    body = strip_study_heading(path_body).strip()
    a_label = spec.get("a_label") or "建议 solid"
    b_label = spec.get("b_label") or "场景 solid"
    lines = [
        "## 建议学习顺序",
        "",
        f"> 行内标记：**A** = Tier A（{a_label}）· **B** = Tier B（{b_label}）· 无标记 = Tier C/D（learning / Query）",
        "",
        annotate_tiers_in_path(body, spec),
        "",
    ]
    path_slugs = slugs_in_path(body)
    a = spec.get("a") or []
    gaps_a = [s for s in a if s not in path_slugs]
    if gaps_a:
        lines.append("### Tier A 补充（路径外，同样建议 solid）")
        lines.append("")
        lines.append(wikilinks_tier(gaps_a, "A"))
        lines.append("")
    b = spec.get("b") or []
    gaps_b = [s for s in b if s not in path_slugs]
    if gaps_b:
        bl = spec.get("b_label") or "场景 solid"
        lines.append(f"### Tier B 补充（{bl}）")
        lines.append("")
        lines.append(wikilinks_tier(gaps_b, "B"))
        lines.append("")
    c = spec.get("c_note")
    if c and c != "—":
        lines.append(f"**Tier C：** {c}")
        lines.append("")
    d = spec.get("d_note")
    if d and d != "—":
        lines.append(f"**Tier D：** {d}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_tiers_block(slug: str, spec: TierSpec) -> str:
    lines = [
        "## 掌握度分层",
        "",
        "> **Tier A** = 建议 `solid` · **Tier B** = 场景 solid · **Tier C** = `learning` + Query · **Tier D** = 索引",
        "",
    ]
    a = spec.get("a") or []
    if a:
        label = spec.get("a_label") or "Tier A"
        lines.append(f"### Tier A — {label}")
        lines.append("")
        lines.append(wikilinks(a))
        lines.append("")
    b = spec.get("b") or []
    if b:
        label = spec.get("b_label") or "Tier B"
        lines.append(f"### Tier B — {label}")
        lines.append("")
        lines.append(wikilinks(b))
        lines.append("")
    c = spec.get("c_note")
    if c and c != "—":
        lines.append("### Tier C — learning + Query")
        lines.append("")
        lines.append(c)
        lines.append("")
    d = spec.get("d_note")
    if d and d != "—":
        lines.append("### Tier D — 索引")
        lines.append("")
        lines.append(d)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def dv_file_in(slugs: list[str]) -> str:
    if not slugs:
        return "false"
    return "(" + " OR ".join(f'file.name = "{s}"' for s in slugs) + ")"


def dv_file_not_in(slugs: list[str]) -> str:
    if not slugs:
        return "true"
    return "(" + " AND ".join(f'file.name != "{s}"' for s in slugs) + ")"


STUDY_TABLE_COLS = (
    'file.link AS "概念", '
    'choice(explain_back = "passed" AND mastery != "solid", "① Promote", '
    'choice(reviewed != null AND explain_back != "passed", "② Explain-back", '
    'choice(reviewed = null OR (updated != null AND reviewed != null AND updated > reviewed), "③ Review", "—"))) AS "下一步", '
    'mastery AS "掌握度", reviewed AS "Review", '
    'explain_back AS "Explain-back", updated AS "更新"'
)

STUDY_TABLE_SORT = (
    "choice(explain_back = \"passed\" AND mastery != \"solid\", 0, "
    "choice(reviewed != null AND explain_back != \"passed\", 1, "
    "choice(reviewed = null OR (updated != null AND reviewed != null AND updated > reviewed), 2, 3))) ASC, "
    "file.name ASC"
)


def dv_tier_group_expr(a: list[str], b: list[str]) -> str:
    """Dataview GROUP BY expression: Tier A / B / 其余 (or 全库)."""
    if not a and not b:
        return '"全库"'
    if a and b:
        return f'choice({dv_file_in(a)}, "Tier A", choice({dv_file_in(b)}, "Tier B", "其余"))'
    if a:
        return f'choice({dv_file_in(a)}, "Tier A", "其余")'
    return f'choice({dv_file_in(b)}, "Tier B", "其余")'


def _dv_progress_summary(domain: str, a: list[str], b: list[str]) -> str:
    tier_expr = dv_tier_group_expr(a, b)
    scope = concept_scope(domain)
    return f"""```dataview
TABLE WITHOUT ID
  tier AS "层级",
  length(filter(rows, (r) => r.mastery = "solid")) + " / " + length(rows) AS "solid",
  length(filter(rows, (r) => r.reviewed != null)) + " / " + length(rows) AS "Review",
  length(filter(rows, (r) => r.explain_back = "passed")) + " / " + length(rows) AS "Explain-back",
  choice(
    length(rows) > 0,
    round(100 * length(filter(rows, (r) => r.mastery = "solid")) / length(rows)) + "%",
    "—"
  ) AS "solid %"
FROM "wiki/concepts"
WHERE {scope}
GROUP BY {tier_expr} AS tier
SORT tier ASC
```"""


def _dv_table(
    domain: str,
    extra_where: str,
    slug_filter: str,
    sort: str,
    *,
    study: bool = False,
) -> str:
    if study:
        cols = STUDY_TABLE_COLS
        sort = STUDY_TABLE_SORT
    else:
        cols = (
            'file.link AS "概念", mastery AS "掌握度", reviewed AS "Review", '
            'explain_back AS "Explain-back", updated AS "更新"'
        )
    scope = concept_scope(domain)
    where = f"{scope} AND {extra_where}"
    if slug_filter not in ("true", "false"):
        where += f" AND {slug_filter}"
    elif slug_filter == "false":
        where += " AND false"
    return f"""```dataview
TABLE WITHOUT ID {cols}
FROM "wiki/concepts"
WHERE {where}
SORT {sort}
```"""


def format_study_page(slug: str, title: str, spec: TierSpec | None, updated: str) -> str:
    """Standalone domains/<slug>/study.md — 学习进度 only, split by Tier."""
    spec = spec or {}
    a = spec.get("a") or []
    b = spec.get("b") or []
    ab = a + b
    a_label = spec.get("a_label") or "建议 solid"
    b_label = spec.get("b_label") or "场景 solid"
    c_note = spec.get("c_note") or ""
    d_note = spec.get("d_note") or ""
    rest_label = "其余（Tier C/D）" if (a or b) else "全库"

    intro: list[str] = [
        f"← [[domains/{slug}/overview]] · 路径与 **A**/**B** 标记见 overview **建议学习顺序**",
    ]
    if slug in VIRTUAL_DOMAIN_SCOPE:
        intro.append(
            "> **虚拟域：** concept 的 `domain:` 仍写在原归属（如 `network-architecture`）；"
            "本页按 **文件名前缀** 聚合进度。"
        )
    intro.append(
        "> 需要 Obsidian **Dataview** 插件。日常 Study 从 **下一步** 列优先："
        "`① Promote` → `② Explain-back` → `③ Review`；`—` 表示暂无需动作。"
    )

    lines = [
        "---",
        f"domain: {slug}",
        "type: domain-study",
        f"updated: {updated}",
        "---",
        "",
        f"# {title} — 学习进度",
        "",
        *intro,
        "",
        "## 进度摘要",
        "",
        "> **主目标** 看 **Tier A** 的 `solid` 分数；**solid %** = solid 数 ÷ 该层概念总数。",
        "",
        _dv_progress_summary(slug, a, b),
        "",
        "## 学习进度",
        "",
    ]
    if a:
        lines.extend(
            [
                f"### Tier A — {a_label}",
                "",
                _dv_table(slug, "true", dv_file_in(a), STUDY_TABLE_SORT, study=True),
                "",
            ]
        )
    if b:
        lines.extend(
            [
                f"### Tier B — {b_label}",
                "",
                _dv_table(slug, "true", dv_file_in(b), STUDY_TABLE_SORT, study=True),
                "",
            ]
        )
    lines.extend([f"### {rest_label}", ""])
    if c_note and c_note != "—":
        lines.append(f"**Tier C：** {c_note}")
        lines.append("")
    if d_note and d_note != "—":
        lines.append(f"**Tier D：** {d_note}")
        lines.append("")
    lines.extend([_dv_table(slug, "true", dv_file_not_in(ab), STUDY_TABLE_SORT, study=True), ""])
    return "\n".join(lines).rstrip() + "\n"


def format_consolidate_block(domain: str) -> str:
    return f"""## 待巩固

> **Consolidate** = 把「测过 / 读过 / 版本变了」的概念收成掌握。下列 Dataview **按优先级** 自动更新；日常 Study 从这里开始，不必扫全库。

**处理顺序：** ① Solid 候选 → Promote · ② 读过未测 → Explain-back · ③ 待复习 → 重读 + Review

**Solid 候选**（`explain_back: passed` 且未 Promote）：

```dataview
TABLE WITHOUT ID file.link AS "概念", mastery, reviewed, explain_back, updated
FROM "wiki/concepts"
WHERE domain = "{domain}" AND explain_back = "passed" AND mastery != "solid"
SORT file.name ASC
```

**读过未测**（有 `reviewed` 但尚未 `passed`）：

```dataview
TABLE WITHOUT ID file.link AS "概念", mastery, reviewed, explain_back, updated
FROM "wiki/concepts"
WHERE domain = "{domain}" AND reviewed != null AND explain_back != "passed"
SORT updated DESC
```

**待复习**（`updated` 晚于 `reviewed` 或未读）：

```dataview
TABLE WITHOUT ID file.link AS "概念", reviewed, updated, explain_back
FROM "wiki/concepts"
WHERE domain = "{domain}" AND (reviewed = null OR (updated != null AND reviewed != null AND updated > reviewed))
SORT updated DESC
```

**新学顺序：** 见上方 **建议学习顺序**（**A** / **B** 行内标记）。
"""


def format_study_progress_block(domain: str) -> str:
    return f"""## 学习进度

> 需要 Obsidian **Dataview** 插件。全库 concept 清单（查阅用）；**日常从 §待巩固 开始**。

```dataview
TABLE WITHOUT ID file.link AS "概念", mastery AS "掌握度", reviewed AS "Review", explain_back AS "Explain-back", updated AS "更新"
FROM "wiki/concepts"
WHERE domain = "{domain}"
SORT file.name ASC
```
"""
