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


def _prefix_scope(*prefixes: str) -> str:
    parts: list[str] = []
    for p in prefixes:
        if p.endswith("*"):
            parts.append(f'startswith(file.name, "{p[:-1]}")')
        elif p.endswith("-"):
            parts.append(f'startswith(file.name, "{p}")')
        else:
            parts.append(f'(file.name = "{p}" OR startswith(file.name, "{p}-"))')
    return "(" + " OR ".join(parts) + ")"


# Virtual domains: study/Dataview scope by filename prefix; frontmatter domain: unchanged.
VIRTUAL_DOMAIN_PARENT: dict[str, str] = {
    "campus-wireless": "network-architecture",
    "network-automation": "network-architecture",
    "campus-enterprise-design": "network-architecture",
    "cloud-network-architecture": "network-architecture",
    "dc-fabric-evpn": "network-architecture",
    "collaboration-uc": "network-architecture",
    "network-storage": "network-architecture",
    "platform-api-engineering": "network-architecture",
    "network-architecture-extended": "network-architecture",
    "security-perimeter-ngfw": "network-security",
    "security-identity-nac": "network-security",
    "security-vpn-remote": "network-security",
    "security-zero-trust": "network-security",
    "security-soc-ops": "network-security",
    "security-cloud-workload": "network-security",
    "security-textbooks": "network-security",
    "kubernetes-fundamentals": "kubernetes-cilium",
    "cilium-networking": "kubernetes-cilium",
    "cloud-native-infrastructure": "kubernetes-cilium",
    "container-security-devops": "kubernetes-cilium",
    "kubernetes-cisco-integration": "kubernetes-cilium",
    "kubernetes-genai-agents": "kubernetes-cilium",
    "kubernetes-distributed-patterns": "kubernetes-cilium",
}

VIRTUAL_DOMAIN_SCOPE: dict[str, str] = {
    "campus-wireless": _prefix_scope(
        "cwna-",
        "cwdp-",
        "enwl-",
        "wng802-",
        "campus-wlan",
        "mrki-mr-wireless-design",
        "ccde-wireless-enterprise-design",
        "encor-enterprise-wireless",
    ),
    "network-automation": _prefix_scope(
        "iac3-",
        "tfur3e-",
        "ausr-",
        "pyats-",
        "devcor-",
        "ndops-",
        "name-",
        "lcij-",
        "cdwj-",
        "lcook-",
        "elcl-",
        "lfnp-",
        "lmlx-",
        "mvim2e-",
        "pvim2e-",
        "lvvim8e-",
        "modvim-",
        "grpc-",
        "network-programmability",
        "network-automation",
        "anops-",
        "ansible-",
    ),
    "campus-enterprise-design": _prefix_scope(
        "sda-",
        "campus-",
        "ensld-",
        "encor-",
        "tcibn-",
        "cdna-",
        "lan-switch-",
        "switch-fund",
        "icns-",
        "cnda-campus",
        "netplus6e-",
    ),
    "cloud-network-architecture": _prefix_scope(
        "acnmap-",
        "sdaws-",
        "awssa-",
        "aznet-",
        "cc2e-",
        "carpat-",
        "caap-",
        "foss-",
        "bcan-",
        "cci-",
        "sahand-",
        "saint-",
    ),
    "dc-fabric-evpn": _prefix_scope(
        "jdevpn-",
        "bdve-",
        "vxlan-",
        "cisco-msdc",
        "sdn2e-",
        "sdn-",
        "tinet2e-",
        "nalg2e-",
        "cnps-",
        "lisnet-",
        "lisdep-",
    ),
    "collaboration-uc": _prefix_scope("clcor-", "claccm-", "clcei-", "usbc-", "pucs-"),
    "network-storage": _prefix_scope("nstor-", "sanf-"),
    "platform-api-engineering": _prefix_scope("pefa-", "epe-", "maapi-"),
    "network-architecture-extended": _prefix_scope(
        "e2eqos-",
        "nag5g-",
        "nxns-",
        "hidhci-",
        "mrki-",
        "fcan3e-",
        "saasf-",
        "stevens-",
        "tcpip-",
    ),
    "security-perimeter-ngfw": _prefix_scope(
        "scor-",
        "sfips-",
        "ftd-",
        "cish4e-",
        "sninf-",
        "mlsh3e-",
        "istv1-",
        "cnsts-",
    ),
    "security-identity-nac": _prefix_scope("sise-", "sisas-", "cise-", "pise-", "istv2-"),
    "security-vpn-remote": _prefix_scope("svpn-"),
    "security-zero-trust": _prefix_scope("zta-", "ztn2-", "ztrc-", "tsb-", "dsbf-", "sse-"),
    "security-soc-ops": _prefix_scope(
        "cbrops-",
        "icb-",
        "nss-",
        "daitn-",
        "aidlp-",
        "uklb3e-",
        "anp-",
        "lbh-",
    ),
    "security-cloud-workload": _prefix_scope("csah-", "sdsi-", "saizt-", "oias-"),
    "security-textbooks": _prefix_scope("sic6-", "cwsp-", "sahc-", "npsp-", "mrkis-"),
    "kubernetes-fundamentals": _prefix_scope(
        "k8s-",
        "kia-",
        "k8pat-",
        "kur3-",
        "pk8s-",
        "pek8s-",
        "ck8i-",
        "hoka-",
        "k8sbp-",
        "nk8s-",
    ),
    "cilium-networking": _prefix_scope("cilium-", "isovalent-", "lobpf-", "ebpf-", "linux-ebpf-"),
    "cloud-native-infrastructure": _prefix_scope("cninfra-", "cndc-", "cnp-", "cn-"),
    "container-security-devops": _prefix_scope("udcb-", "ddb-", "csec2e-", "nvk8ss-"),
    "kubernetes-cisco-integration": _prefix_scope(
        "cilium-aci",
        "cilium-nxos",
        "cilium-cisco",
        "calico-",
        "fs-ocp",
        "flashstack-",
    ),
    "kubernetes-genai-agents": _prefix_scope("k8s-llm", "k8s-ai", "kgais-", "a30ag-", "bm-"),
    "kubernetes-distributed-patterns": _prefix_scope("msa-", "pdds-", "dds-"),
}


def concept_scope(domain: str) -> str:
    if domain in VIRTUAL_DOMAIN_SCOPE:
        prefix = VIRTUAL_DOMAIN_SCOPE[domain]
        parent = VIRTUAL_DOMAIN_PARENT.get(domain)
        if parent:
            return f'domain = "{parent}" AND {prefix}'
        return prefix
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
        "c_note": "扩展：`cilium-cluster-mesh`、`cilium-service-mesh`、GenAI — 见 [[domains/kubernetes-genai-agents/overview]]；K8s 实操 — [[domains/kubernetes-fundamentals/overview]]；企业集成 — [[domains/kubernetes-cisco-integration/overview]] — **learning + Query**",
        "d_note": "索引：`msa-*`/`pdds-*`/`dds-*` — 见 [[domains/kubernetes-distributed-patterns/overview]]，**不必 solid**",
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
        "a_label": "AI survey 主线（建议 solid）",
        "a": [
            "ai-age-and-llm-foundations",
            "ai-in-computer-networking",
            "ai-in-cybersecurity",
            "ai-cloud-computing",
            "ai-collaboration-technologies",
            "ai-iot-aiot",
            "ai-emerging-technologies-frontier",
        ],
        "c_note": "`llm-*`/`gaai-*`/`ml-*`/`nlp-*`/`vllm-*` 等 ingest 子页 — **learning + Query**；深度见各来源",
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
        "c_note": "垂直子域见 [[domains/virtual-domains-registry]]；园区/DC/云/自动化等 — 各 virtual overview；无线 → [[domains/campus-wireless/overview]] — **learning + Query**",
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
        "c_note": "证书/运维/教材见各 `security-*` 虚拟域（[[domains/virtual-domains-registry]]）；本 hub 仅 `ns-*` — 其余 **learning + Query**",
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
    "meta-skills": {
        "a_label": "人类判断与元能力（建议 solid）",
        "a": [
            "ms-system1-system2",
            "ms-heuer-competing-hypotheses",
            "ms-tetlock-calibration",
            "ms-problem-vs-solution",
            "ms-polya-four-phases",
            "ms-deliberate-practice",
            "ms-retrieval-practice",
            "ms-pearl-causal-ladder",
            "ms-system-feedback-loops",
            "ms-meadows-leverage-points",
            "ms-simon-satisficing",
            "ms-rumelt-strategy-kernel",
            "ms-minto-pyramid-principle",
            "ms-cialdini-influence-defense",
            "ms-forward-fog",
            "ms-cloud-boundaries",
            "ms-getting-to-yes-interests-not-positions",
            "ms-patterson-dialogue-safety",
            "ms-axelrod-tit-for-tat",
        ],
        "b": [
            "ms-popper-falsification",
            "ms-range-late-specialization",
            "ms-klein-naturalistic-decision",
            "ms-dalio-believability-weighting",
            "ms-dalio-issue-log",
            "ms-perrow-normal-accidents",
            "ms-grant-giver-trap",
            "ms-stone-three-conversations",
            "ms-debecker-pre-incident-indicators",
        ],
        "b_label": "深化 / 可选专题 / 对话补丁",
        "c_note": "ingest 后其余 `ms-*` 概念 — learning + Query；延展 Sterman/Popper/Goffman — overview only",
        "d_note": "—",
    },
    "chinese-history-culture": {
        "a_label": "政制与文化核心（建议 solid）",
        "a": [
            "qmc-how-to-read-political-history",
            "qmc-imperial-minister-power",
            "qmc-scholar-government",
            "qmc-han-political-system",
            "qmc-ming-political-system",
            "qmc-qing-political-system",
            "qmc-political-history-summary",
            "qmc-wenzhi-government",
            "qmc-cultural-spirit-twelve-lectures",
            "qmc-cultural-history-framework",
            "qmc-cheng-zhu-vs-lu-wang",
        ],
        "b": [
            "qmc-tang-political-system",
            "qmc-song-political-system",
            "qmc-chinese-history-spirit",
            "qmc-song-learning-rise",
            "qmc-zhu-xi-lixue",
            "qmc-wang-yangming-xinxue",
            "qmc-chinese-vs-western-comparison",
        ],
        "b_label": "思想史与比较深化",
        "c_note": "经学史、史学方法、考据、人生论 — learning + Query",
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
    "enterprise-architecture": {
        "a_label": "TOGAF ADM + FOSA 核心（建议 solid）",
        "a": [
            "togaf-framework-overview",
            "togaf-core-concepts",
            "togaf-adm-overview",
            "togaf-preliminary-phase",
            "togaf-phase-a-architecture-vision",
            "togaf-phase-b-business-architecture",
            "togaf-phase-d-technology-architecture",
            "togaf-phase-f-migration-planning",
            "togaf-adm-requirements-management",
            "togaf-architecture-principles",
            "togaf-gap-analysis",
            "togaf-building-blocks",
            "togaf-enterprise-continuum",
            "togaf-architecture-repository",
            "togaf-architecture-governance",
            "fosa-software-architect-role",
            "fosa-architectural-thinking",
            "fosa-architecture-characteristics-defined",
            "fosa-choosing-architecture-style",
            "fosa-architecture-decisions",
        ],
        "b_label": "Phase C / 内容框架深化",
        "b": [
            "togaf-phase-c-information-systems",
            "togaf-phase-c-data-architecture",
            "togaf-phase-c-application-architecture",
            "fosa-microservices-architecture-style",
        ],
        "c_note": "其余 TOGAF Phase E–H / 能力框架 — **learning + Query**",
        "d_note": "—",
    },
    "algorithms": {
        "a_label": "Jeff Erickson 核心（建议 solid）",
        "a": [
            "jeffe-algorithm-definition",
            "jeffe-asymptotic-analysis",
            "jeffe-recursion-reductions",
            "jeffe-divide-and-conquer-sorting",
            "jeffe-recursion-trees",
            "jeffe-backtracking-general-pattern",
            "jeffe-dp-memoization-tabulation",
            "jeffe-dp-edit-distance",
            "jeffe-greedy-structure",
            "jeffe-graph-representations",
            "jeffe-graph-traversal",
            "jeffe-dfs-classification",
            "jeffe-minimum-spanning-trees",
            "jeffe-sssp-framework",
            "jeffe-dijkstra-algorithm",
            "jeffe-bellman-ford",
            "jeffe-maxflow-mincut",
            "jeffe-p-vs-np",
            "jeffe-np-completeness",
            "jeffe-np-reduction-sat",
        ],
        "b_label": "专题深化（场景 solid）",
        "b": ["jeffe-huffman-codes", "jeffe-edmonds-karp-flow", "jeffe-dp-longest-increasing-subsequence"],
        "c_note": "其余 `jeffe-*` / `ga2e-*` — **learning + Query**",
        "d_note": "—",
    },
    "computer-architecture": {
        "a_label": "CAQA 核心（建议 solid）",
        "a": [
            "caqa-computer-classes",
            "caqa-performance-measurement",
            "caqa-quantitative-design-principles",
            "caqa-amdahl-law",
            "caqa-cache-hierarchy-basics",
            "caqa-virtual-memory",
            "caqa-ilp-fundamentals",
            "caqa-dynamic-scheduling",
            "caqa-ilp-limitations",
            "caqa-gpu-architecture",
            "caqa-smp-cache-coherence",
            "caqa-memory-consistency",
            "caqa-wsc-architecture",
        ],
        "b_label": "进阶优化（场景 solid）",
        "b": ["caqa-branch-prediction", "caqa-cache-advanced-optimizations", "caqa-directory-coherence"],
        "c_note": "向量/SIMD/仓库级案例 — **learning + Query**",
        "d_note": "—",
    },
    "craft-writing": {
        "a_label": "文风机制（建议 solid · 小域全覆盖）",
        "a": [
            "te-shi-absurd-vocabulary-diction",
            "te-shi-oral-fragment-rhythm",
            "te-shi-bait-switch-mindfuck-narrative",
            "te-shi-middle-class-satire-target",
            "te-shi-zoo-animal-persona",
            "te-shi-ironic-title-paratext",
            "te-shi-poetry-rhythm",
        ],
        "c_note": "—",
        "d_note": "—",
    },
    "network-automation": {
        "a_label": "自动化脊骨（建议 solid）",
        "a": ["network-automation-architecture", "iac3-what-is-infrastructure-as-code"],
        "b_label": "NetDevOps / 测试（场景 solid）",
        "b": ["ndops-netdevops-culture-stages", "pyats-cicd-pipelines"],
        "c_note": "其余 IaC/Ansible/DEVCOR/Vim — **learning + Query**",
        "d_note": "—",
    },
    "campus-enterprise-design": {
        "a_label": "园区 / SD-Access 核心（建议 solid）",
        "a": ["sda-campus-fabric-fundamentals", "ensld-enterprise-lan-design"],
        "b_label": "ENCOR / 跨域（场景 solid）",
        "b": ["encor-enterprise-architecture-fabric", "mdn-sda-campus-integration"],
        "c_note": "其余 `sda-*`/`ensld-*`/`icns-*` — **learning + Query**",
        "d_note": "—",
    },
    "cloud-network-architecture": {
        "a_label": "多云网络核心（建议 solid）",
        "a": ["acnmap-aks-networking", "sdaws-aws-orchestration-monitoring-iam"],
        "b_label": "设计 / 运维深化",
        "b": ["cc2e-cloud-ecosystem-providers", "awssa-aws-devops-cloudops"],
        "c_note": "其余 `acnmap-*`/`aznet-*`/`sahand-*` — **learning + Query**",
        "d_note": "—",
    },
    "dc-fabric-evpn": {
        "a_label": "EVPN / VXLAN 核心（建议 solid）",
        "a": ["jdevpn-apstra-foundation", "bdve-bgp-evpn-route-types", "vxlan-evpn-multisite-vpc-bgw-dci"],
        "b_label": "MSDC / SDN",
        "b": ["cisco-msdc-fabric-topology", "sdn2e-openflow-specification"],
        "c_note": "其余 fabric/SDN 专著 — **learning + Query**",
        "d_note": "—",
    },
    "collaboration-uc": {
        "a_label": "协作 UC 核心（建议 solid）",
        "a": ["clcor-converged-collaboration-solution", "claccm-cucm-call-routing"],
        "c_note": "其余 `clcor-*`/`clcei-*`/`pucs-*` — **learning + Query**",
        "d_note": "—",
    },
    "network-storage": {
        "a_label": "存储网络核心（建议 solid）",
        "a": ["sanf-fibre-channel-basics", "nstor-data-security-governance"],
        "c_note": "其余 — **learning + Query**",
        "d_note": "—",
    },
    "platform-api-engineering": {
        "a_label": "API / 平台工程（建议 solid）",
        "a": ["pefa-platform-architecture-product", "epe-control-plane-foundations"],
        "c_note": "其余 `maapi-*` — **learning + Query**",
        "d_note": "—",
    },
    "network-architecture-extended": {
        "c_note": "杂项专著 / 5G / QoS / MRKI 等 — **learning + Query**；未归入其他 virtual 的 NA 页",
        "d_note": "索引 — 按需查阅",
    },
    "security-perimeter-ngfw": {
        "a_label": "边界 / NGFW 核心（建议 solid）",
        "a": ["scor-secure-firewall", "sfips-ngfw-architecture"],
        "b_label": "SCOR / FTD 深化",
        "b": ["scor-cybersecurity-fundamentals", "ftd-firepower-platform-overview"],
        "c_note": "其余 `scor-*`/`sfips-*`/`ftd-*` — **learning + Query**；hub 先修 [[ns-firewalls-zero-trust]]",
        "d_note": "—",
    },
    "security-identity-nac": {
        "a_label": "身份 / NAC 核心（建议 solid）",
        "a": ["sise-ise-architecture", "cise-nac-policy-framework"],
        "b_label": "SISE / PISE 深化",
        "b": ["sise-authn-authz-policies", "pise-authentication-policies"],
        "c_note": "其余 `sise-*`/`sisas-*` — **learning + Query**",
        "d_note": "—",
    },
    "security-vpn-remote": {
        "a_label": "远程接入（建议 solid）",
        "a": ["svpn-anyconnect-vpn"],
        "c_note": "其余 `svpn-*` — **learning + Query**",
        "d_note": "—",
    },
    "security-zero-trust": {
        "a_label": "零信任核心（建议 solid）",
        "a": ["zta-reference-architecture", "zta-enforcement"],
        "b_label": "框架 / 专著",
        "b": ["zta-five-pillar-capabilities", "ztn2-managing-trust"],
        "c_note": "其余 `zta-*`/`sse-*` — **learning + Query**；hub [[ns-firewalls-zero-trust]]",
        "d_note": "—",
    },
    "security-soc-ops": {
        "a_label": "SOC / 运维核心（建议 solid）",
        "a": ["cbrops-cybersecurity-fundamentals", "icb-digital-forensics-fundamentals"],
        "c_note": "其余 `cbrops-*`/`daitn-*`/`aidlp-*` — **learning + Query**",
        "d_note": "—",
    },
    "security-cloud-workload": {
        "a_label": "云工作负载安全（建议 solid）",
        "a": ["csah-architect-responsibilities", "sdsi-core-security-principles"],
        "c_note": "其余 `saizt-*`/`oias-*` — **learning + Query**",
        "d_note": "—",
    },
    "security-textbooks": {
        "a_label": "教材主线（建议 solid）",
        "a": ["sic6-access-control-reference-monitor", "cwsp-encryption-ciphers"],
        "b_label": "专著深化",
        "b": ["sahc-architecture-concepts", "npsp-enterprise-network-architecture"],
        "c_note": "其余 `sic6-*`/`mrkis-*` — **learning + Query**",
        "d_note": "—",
    },
    "kubernetes-fundamentals": {
        "a_label": "K8s 核心（建议 solid）",
        "a": [
            "k8s-network-visibility-gap",
            "k8s-pod-model",
            "k8sbp-pod-security-standards-enforcement",
        ],
        "b_label": "模式 / 平台工程",
        "b": ["k8pat-sidecar", "pk8s-admission-control", "pek8s-platform-apis-architecture"],
        "c_note": "其余 `kia-*`/`pk8s-*`/`hoka-*` — **learning + Query**",
        "d_note": "—",
    },
    "cilium-networking": {
        "a_label": "Cilium / eBPF 核心（建议 solid）",
        "a": [
            "linux-ebpf-fundamentals",
            "ebpf-program-anatomy",
            "cilium-cni-overview",
            "cilium-architecture",
            "cilium-ebpf-dataplane",
            "cilium-datapath-modes",
            "cilium-network-policy-identity",
            "cilium-network-policies-segmentation",
            "cilium-hubble-observability",
            "cilium-hubble-policy-workflow",
        ],
        "b_label": "IPAM / 企业版",
        "b": ["cilium-ipam", "cilium-kube-proxy-replacement", "isovalent-network-bridge"],
        "c_note": "Mesh / Cluster Mesh / L7 — **learning + Query**",
        "d_note": "—",
    },
    "cloud-native-infrastructure": {
        "a_label": "云原生基础设施（建议 solid）",
        "a": ["cninfra-app-lifecycle", "cndc-clos-topology"],
        "b_label": "模式 / 平台",
        "b": ["cnp-cloud-native-definition", "cn-api-gateway-patterns"],
        "c_note": "其余 `cn-*`/`cninfra-*` — **learning + Query**",
        "d_note": "—",
    },
    "container-security-devops": {
        "a_label": "容器安全 / DevOps（建议 solid）",
        "a": ["udcb-container-hardening-runtime", "csec2e-hardening-isolation"],
        "c_note": "其余 `ddb-*`/`nvk8ss-*` — **learning + Query**",
        "d_note": "—",
    },
    "kubernetes-cisco-integration": {
        "a_label": "Cisco 集成（场景 solid）",
        "a": [
            "cilium-aci-basic-design",
            "cilium-nxos-evpn-vxlan-k8s-design",
            "cilium-cisco-hybrid-integration",
        ],
        "b_label": "Calico / FlashStack",
        "b": ["calico-ebpf-dataplane", "fs-ocp-baremetal-openshift"],
        "c_note": "其余集成 SKU — **learning + Query**",
        "d_note": "—",
    },
    "kubernetes-genai-agents": {
        "a_label": "K8s + GenAI（建议 solid）",
        "a": ["k8s-llm-inference-fundamentals", "k8s-ai-job-scheduling"],
        "b_label": "Agent / 推理",
        "b": ["kgais-eks-cloud-setup", "a30ag-agent-engineering-foundations"],
        "c_note": "其余 `k8s-llm-*`/`k8s-ai-*`/`bm-*` — **learning + Query**",
        "d_note": "—",
    },
    "kubernetes-distributed-patterns": {
        "c_note": "全书 **Query 串联**，不必 solid — 见 overview 三书索引",
        "d_note": "`msa-*`/`pdds-*`/`dds-*` — **Tier D 索引**",
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
    'choice(reviewed = null OR (updated != null AND reviewed != null AND updated > reviewed), "③ Cold", "—"))) AS "下一步", '
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
        "`① Promote` → `② Explain-back` → `③ Cold`（`Explain-back [[概念]] cold`）；`—` 表示暂无需动作。"
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
