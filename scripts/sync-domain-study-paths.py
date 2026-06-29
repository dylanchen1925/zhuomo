#!/usr/bin/env python3
"""Sync domain overview.md + guide.md study paths and mastery tiers from repo templates."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from domain_study_tiers import (  # noqa: E402
    TIERS,
    format_study_page,
    format_unified_study_order,
    strip_study_heading,
)

# overview: full numbered path; guide: condensed (may link to overview)
PATHS: dict[str, dict[str, str]] = {
    "cisco-aci": {
        "overview": """## 建议学习顺序

1. **Why ACI + 拓扑** — [[aci-sdn-value-proposition]] → [[aci-spine-leaf-topology]] → [[aci-apic]]
2. **Fabric init + Underlay** — [[aci-fabric-initialization]] → [[aci-fabric-underlay]] → [[aci-leaf-forwarding-profile]]
3. **接入** — [[aci-vlan-pools-aaep]] → [[aci-vpc-design]] → [[aci-contract-subjects-filters]]
4. **Tenant** — [[aci-tenant-epg-contract]]
5. **Endpoint** — [[aci-endpoint-learning-controls]] → [[aci-ip-dataplane-learning]] → [[aci-endpoint-forwarding-scenarios]] → [[aci-l3out-endpoint-learning]] → [[aci-disable-remote-ep-learn]]
6. **L3Out 核心** — [[aci-border-leaf-l3out]] → [[aci-infra-mp-bgp]] → [[aci-l3out-profiles]]
7. **L3Out 协议/策略** — [[aci-l3out-bgp]] → [[aci-l3out-ospf]] → [[aci-l3out-eigrp]] → [[aci-l3out-static-routes]] → [[aci-l3out-route-maps]] → [[aci-l3out-contracts]] → [[aci-l3out-transit-routing]] → [[aci-l3out-vrf-route-leaking]] → [[aci-l3out-bd-subnet-advertisement]] → [[aci-l3out-bfd]] → [[aci-l4l7-virtual-ips-dsr]]
8. **L2Out / 迁移** — [[aci-l2out-network-centric-migration]]
9. **Multi-Pod** — [[aci-multi-pod]] → [[aci-multi-pod-overlay]] → [[aci-multi-pod-config-zones]] → [[aci-multi-pod-external-l3]] → [[aci-multi-pod-network-services]] → [[aci-multi-pod-migration]] → [[aci-multi-pod-workload-migration]]
10. **Multi-Site** — [[aci-multi-site]] → [[aci-nexus-dashboard-orchestrator]] → [[aci-multi-site-isn]] → [[aci-multi-site-overlay-control-plane]] → [[aci-multi-site-overlay-data-plane]] → [[aci-multi-site-best-practices]] → [[aci-remote-leaf]]
11. **集成 / 运维** — [[aci-vmm-vsphere-integration]] → [[aci-service-graph-integration]] → [[aci-telemetry-nexus-insights]] → [[aci-syslog-snmp-monitoring]] → [[aci-apic-fault-health-monitoring]] → [[aci-rbac-aaa]] → [[aci-inband-oob-management]]
12. **DCCOR 350-601**（按需）— [[dccor-dc-routing]] → [[dccor-dc-switching]] → [[dccor-dc-overlay-protocols]] → [[dccor-aci-fundamentals]] → [[dccor-ucs-compute]] → [[dccor-dc-automation]] → [[dccor-dc-security]]（完整 Ch 表见 [[domains/cisco-aci/guide]]）
13. 每步：**Review** + **Explain-back** 对应 concept
""",
        "guide": """## 建议学习顺序

与 [[domains/cisco-aci/overview#建议学习顺序]] 同步（2026-06-01 framework）。

**主线（8 步）：** 拓扑/APIC → Underlay → Access/vPC → Tenant → Endpoint → L3Out（含 `aci-l3out-*` 子页）→ Multi-Pod/Site → 运维/集成。

**DCCOR 支线：** 见本页 §0b CCNP/CCIE Data Center Core 表 — 从 [[dccor-dc-routing]] 按 Ch 顺序。

**DCACI 支线：** 见 §0 DCACI 300-620 速查表。
""",
    },
    "cisco-sdwan": {
        "overview": """## 建议学习顺序

1. **用例与架构** — [[sdwan-use-cases]] → [[sdwan-architecture-planes]]
2. **控制面** — [[sdwan-control-plane]] → [[sdwan-control-deployment]] → [[sdwan-orchestration-onboarding]]
3. **数据面与路由** — [[sdwan-data-plane-tloc]] → [[sdwan-omp-routing]]
4. **部署规划** — [[sdwan-deployment-planning]] → [[sdwan-edge-deployment]]
5. **策略 / 安全 / QoS** — [[sdwan-policies-qos]] → [[sdwan-firewall-ports-nat]]
6. **运维与排障** — [[sdwan-management-templates]] → [[sdwan-operations-telemetry]] → [[sdwan-troubleshooting]]
7. **实验** — [[sdwan-eve-ng-lab-topology]]
8. 每步：**Review** + **Explain-back**
""",
        "guide": """## 建议学习顺序

与 [[domains/cisco-sdwan/overview#建议学习顺序]] 相同：用例 → 平面 → 控制 → OMP/TLOC → 部署 → 策略/QoS → 运维 → Lab。
""",
    },
    "ai-dc-networking": {
        "overview": """## 建议学习顺序

1. **Workload / KPI** — [[ai-dc-workload-lifecycle]] → [[ai-training-parallelism]] → [[ai-jct-tail-latency]] → [[ai-training-vs-inference-dc]]
2. **传输** — [[ai-rdma-rocev2]] → [[ai-infiniband-vs-ethernet]] → [[ai-rocev2-congestion]]
3. **拓扑** — [[ai-rail-optimized-design]] → [[ai-rail-unified-design]] → [[ai-dc-fabric-topologies]] → [[ai-scheduled-fabric]]
4. **物理层** — [[ai-dc-optics-cabling]] → [[ai-dc-thermal-cooling]]
5. **Fabric 特性** — [[ai-fabric-load-balancing]] → [[nexus-intelligent-buffer-management]] → [[ai-fabric-ip-routing]]
6. **存储 / NVMe** — [[ai-dc-storage-networks]] → [[nvme-protocol-fundamentals]] → [[nvmeof-transport-selection]] → [[nvme-roce-host-target-config]] → [[roce-storage-vxlan-multi-site]] → [[nxos-roce-qos-vxlan-fabric]] → [[nexus9300-rocev2-qos-baseline]]
7. **可观测与验收** — [[ai-fabric-monitoring-ifa]] → [[ai-mlcommons-benchmarking]]
8. **下一代** — [[ai-ultra-ethernet-consortium]] → [[ai-scale-up-systems]]
9. **Cisco Nexus / MSDC / Hyperfabric** — [[cisco-ai-ml-network-challenges]] → [[cisco-nexus-ai-blueprint]] → [[cisco-nexus-ai-era-architecture]] → [[cisco-nexus-ai-spine-leaf-sizing]] → [[cisco-nexus-ai-clusters-design]] → [[cisco-nexus-ai-clusters-validation]] → [[cisco-msdc-fabric-topology]] → [[cisco-msdc-ai-rail-plane-fabric]] → [[cisco-hyperfabric-full-stack-ai]] → [[cisco-hyperfabric-hf6100-fabric]] → [[cisco-hyperfabric-controller]] → [[cisco-aiml-vxlan-evpn-gpuaas]]
10. 每步：**Review** + **Explain-back**
""",
        "guide": """## 建议学习顺序

与 [[domains/ai-dc-networking/overview#建议学习顺序]] 同步。主线 1–8；Cisco 蓝图见 overview 第 9 步。
""",
    },
    "ai-systems-performance": {
        "overview": """## 建议学习顺序

1. **KPI** — [[ai-goodput-metric]] → [[ai-disaggregated-prefill-decode]]
2. **硬件平台** — [[ai-grace-blackwell-superchip]] → [[ai-gpu-platform-tuning]]
3. **通信与 I/O** — [[ai-nccl-magnum-io]] → [[ai-gds-storage-pipeline]]
4. **GPU / 内核** — [[ai-cuda-roofline-occupancy]] → [[ai-pytorch-compiler-triton]]
5. **训练栈** — [[ai-pytorch-distributed-performance]]
6. **推理栈** — [[ai-inference-serving-at-scale]]
7. 每步：**Review** + **Explain-back**

**网络 fabric 设计** → [[domains/ai-dc-networking/overview]]
""",
        "guide": """## 建议学习顺序

与 [[domains/ai-systems-performance/overview#建议学习顺序]] 相同：goodput → 硬件 → NCCL/GDS → CUDA/Triton → 训练 → 推理。
""",
    },
    "systems-performance": {
        "overview": """## 建议学习顺序

详见 [[domains/systems-performance/guide#建议顺序]]。主线：

1. **方法论** — [[sysperf-systems-performance-fundamentals]] → [[sysperf-performance-methodologies]] → [[sysperf-benchmarking]]
2. **可观测** — [[sysperf-observability-tools]] → [[sysperf-linux-perf]] → [[sysperf-bpf-ebpf-tooling]] → [[sysperf-ftrace-tracing]]
3. **资源分析** — [[sysperf-operating-systems]] → [[sysperf-cpu-performance]] → [[sysperf-memory-performance]] → [[sysperf-filesystem-performance]] → [[sysperf-disk-io-performance]] → [[sysperf-network-performance]]
4. **应用与云** — [[sysperf-application-performance]] → [[sysperf-cloud-virtualization]]
5. 每步：**Review** + **Explain-back**
""",
        "guide": """## 建议顺序

1. **方法论** — [[sysperf-systems-performance-fundamentals]] → [[sysperf-performance-methodologies]] → [[sysperf-benchmarking]]
2. **可观测** — [[sysperf-observability-tools]] → [[sysperf-linux-perf]] → [[sysperf-bpf-ebpf-tooling]] → [[sysperf-ftrace-tracing]]
3. **CPU / 内存** — [[sysperf-operating-systems]] → [[sysperf-cpu-performance]] → [[sysperf-memory-performance]]
4. **存储 / 网络** — [[sysperf-filesystem-performance]] → [[sysperf-disk-io-performance]] → [[sysperf-network-performance]]
5. **应用与云** — [[sysperf-application-performance]] → [[sysperf-cloud-virtualization]]
6. 每步：**Review** + **Explain-back**
""",
    },
    "ai-emerging-tech": {
        "overview": """## 建议学习顺序

1. **AI 基础** — [[ai-age-and-llm-foundations]] → [[ai-emerging-technologies-frontier]]
2. **网络 / 安全 / 云** — [[ai-in-computer-networking]] → [[ai-in-cybersecurity]] → [[ai-cloud-computing]]
3. **协作与 IoT** — [[ai-collaboration-technologies]] → [[ai-iot-aiot]]
4. 每步：**Review** + **Explain-back**

**训练 fabric / goodput** → [[domains/ai-dc-networking/overview]] · [[domains/ai-systems-performance/overview]]
""",
        "guide": """## 建议顺序

与 [[domains/ai-emerging-tech/overview#建议学习顺序]] 相同（7 概念全覆盖）。
""",
    },
    "technical-analysis": {
        "overview": """## 建议学习顺序

1. **框架** — [[ding-yin-yang-ta-foundation]] → [[ta-theory-foundation]] → [[ta-three-analysis-levels]] → [[ideal-trend-evolution-pattern]]
2. **道氏 / 趋势** — [[dow-theory]] → [[trend-definition-peak-trough]] → [[trendlines-channels]] → [[trend-tracking-essentials]]
3. **图表** — [[chart-construction]] → [[percentage-retracements]] → [[candlestick-charts]] → [[ding-candlestick-trend-framework]]
4. **形态** — [[major-reversal-patterns]] → [[head-and-shoulders]] → [[continuation-patterns]] → [[price-gaps]] → [[measuring-techniques]]
5. **量 / 情绪** — [[volume-open-interest]] → [[sentiment-option-indicators]] → [[contrary-opinion]]
6. **指标** — [[moving-averages]] → [[oscillator-analysis]] → [[rsi-stochastic-macd]]
7. **另类图 / 高级** — [[point-and-figure]] → [[elliott-wave-theory]] → [[cycle-analysis]] → [[long-term-charts]] → [[monthly-candlestick-long-trend]]
8. **市场间 / 广度** — [[intermarket-analysis]] → [[stock-market-breadth-indicators]] → [[ta-market-state-logic]]
9. **执行** — [[money-management-trading-tactics]] → [[computer-trading-systems]] → [[trading-system-design]] → [[ta-synthesis-checklist]]
10. **A 股（雪松）** — [[xuesong-trading-mindset]] → [[xuesong-primary-pool-filters]] → [[xuesong-mode-a-breakout]] → [[xuesong-mode-b-deep-pullback]] → [[xuesong-volume-price-truth]] → [[xuesong-rsi-practical-application]] → [[xuesong-position-and-stop]] → [[xuesong-sell-and-take-profit]]
11. **缠论** — [[chan-theory-framework]] → [[chan-kline-inclusion]] → [[chan-bi-stroke]] → [[chan-line-segment]] → [[chan-central-pivot]] → [[chan-beichi-divergence]] → [[chan-three-buy-sell-points]] → [[chan-trading-execution]]
12. 每步：**Review** + **Explain-back**
""",
        "guide": """## 建议学习顺序

与 [[domains/technical-analysis/overview#建议学习顺序]] 同步。Murphy 主线 1–9；A 股 [[xuesong-*]]；缠论 [[chan-*]] 见 overview 10–11。
""",
    },
    "macro-cycle-investing": {
        "overview": """## 建议学习顺序

1. **人性与周期观** — [[zhou-cycle-human-nature]] → [[zhou-destiny-and-resistance]]
2. **康波** — [[zhou-kondratiev-life-wave]]
3. **三周期嵌套** — [[zhou-three-cycle-nesting]] → [[zhou-juglar-capacity-cycle]] → [[zhou-inventory-cycle]]
4. **资产定价** — [[zhou-kuznets-property-cycle]] → [[zhou-commodity-kondratiev]] → [[zhou-gold-in-kondratiev]]
5. **配置框架** — [[zhou-merrill-clock-revision]] → [[zhou-asset-allocation-framework]]
6. 每步：**Review** + **Explain-back**

**图表周期** → [[cycle-analysis]] · [[domains/technical-analysis/overview]]
""",
        "guide": """## 建议学习顺序

与 [[domains/macro-cycle-investing/overview#建议学习顺序]] 相同（11 概念全覆盖）。
""",
    },
    "kubernetes-cilium": {
        "overview": """## 建议学习顺序

**核心 Cilium 书路径（默认）：**

0. **先修** — [[k8s-enterprise-adoption]] → [[k8s-network-visibility-gap]] → [[k8s-pod-model]] → [[k8s-services-neteng-perspective]]
1. **eBPF 基础** — [[linux-ebpf-fundamentals]] → [[ebpf-program-anatomy]] → [[ebpf-bpf-syscall-maps]] → [[ebpf-networking-hooks]]
2. **Cilium 核心** — [[cilium-cni-overview]] → [[cilium-architecture]] → [[cilium-ebpf-dataplane]] → [[cilium-datapath-modes]] → [[cilium-kube-proxy-replacement]]
3. **策略与身份** — [[cilium-network-policy-identity]] → [[cilium-network-policies-segmentation]] → [[cilium-l7-fqdn-policy]] → [[k8s-network-policy-zero-trust-rollout]]
4. **可观测 / 运维** — [[cilium-hubble-observability]] → [[cilium-hubble-policy-workflow]] → [[cilium-operations]]
5. **企业平台** — [[isovalent-enterprise-platform]] → [[cilium-enterprise-value-pillars]] → [[isovalent-tetragon-runtime-security]]
6. **多云 / Mesh** — [[cilium-multi-cloud-networking]] → [[cilium-cluster-mesh]] → [[cilium-service-mesh]] → [[k8s-service-mesh-evolutionary-ladder]]

**扩展路径（按需）：**

7. **K8s 网络工程** — `k8s-*` 网络章：[[k8s-declarative-config-neteng]] → [[k8s-bgp-tor-integration]] → [[k8s-coredns-namespace-neteng]]
8. **Cisco 集成** — [[cilium-cisco-hybrid-integration]] → [[cilium-aci-basic-design]] → [[cilium-aci-bgp-fabric-peering]] → [[cilium-nxos-evpn-vxlan-k8s-design]]
9. **微服务 / 分布式** — [[msa-monolith-escape]] → [[msa-service-decomposition]] → [[msa-saga-transactions]] · [[pdds-leader-follower]] → [[pdds-quorum-commit]]
10. **GenAI on K8s** — [[k8s-ai-job-scheduling]] → [[k8s-rag-patterns]] → [[k8s-agentic-workflows]]
11. 每步：**Review** + **Explain-back**

完整书章索引 → [[domains/kubernetes-cilium/guide#推荐学习路径（书章顺序）]]
""",
        "guide": """## 推荐学习路径（书章顺序）

与 [[domains/kubernetes-cilium/overview#建议学习顺序]] 同步。

**Book 1 — Cilium（核心）：** eBPF → Cilium CNI/策略/Hubble → 企业 IEP/Tetragon → Cluster Mesh。

**Book 2 — K8s 网络（KUAR）：** Pod/Service/Ingress → NetPol → BGP/TOR → 运维。

**Book 3+ — 扩展：** Cisco ACI/NX-OS（`cilium-aci-*`）· CNDC（`cndc-*`）· FlashStack（`fs-ocp-*`）· MSA/BM · PDDS/DDS · GenAI（`k8s-llm-*` / `k8s-ai-*`）。

按 job 选支路；不必一次读完 199 页。
""",
    },
    "ip-routing": {
        "overview": """## 建议学习顺序

1. **基础** — [[tcpip-protocol-review]] → [[cn-foundation-systems-approach]] → [[dynamic-routing-protocols]]
2. **静态 / RIP** — [[static-routing]] → [[rip-routing]] → [[ripv2-ripng-classless]] → [[default-routes-odr]]
3. **EIGRP** — [[eigrp]] → [[enarsi-eigrp-advanced]] → [[enarsi-eigrp-troubleshooting]]
4. **OSPF** — [[ospfv2]] → [[ospfv3]] → [[enarsi-ospf-advanced]] → [[enarsi-ospf-troubleshooting]]
5. **IS-IS** — [[integrated-is-is]] → [[choosing-ospf-vs-is-is]] → [[igp-area-design]] → [[igp-scaling]]
6. **重分发与策略** — [[route-redistribution]] → [[route-filtering]] → [[route-maps]] → [[enarsi-route-redistribution]]
7. **BGP** — [[bgp-introduction]] → [[bgp-nlri]] → [[bgp-routing-policies]] → [[bgp-scaling]] → [[enarsi-bgp-advanced]] → [[enarsi-bgp-troubleshooting]] → [[mp-bgp]] → [[enarsi-mpls-l3vpn]]
8. **组播** — [[ip-multicast-routing]] → [[pim]] → [[cipm-multicast-introduction]] → [[cipm-multicast-design]] → [[cipm2-large-scale-multicast-design]]
9. **NAT / IPv6** — [[ipv6-overview]] → [[nat44]] → [[nat64]]
10. **TCP/IP 深入（Stevens）** — [[tcpip-illustrated-architecture]] → [[tcpip-illustrated-ip]] → [[tcpip-illustrated-tcp]] → [[tcpip-illustrated-multicast]]
11. **TCP 拥塞控制** — [[tcpcc-design-space]] → [[tcpcc-control-based-algorithms]] → [[tcpcc-active-queue-management]] → [[tcpcc-datacenter-transport]]
12. **ENCOR / CENG 速查** — [[encor-ip-routing-essentials]] · [[encor-bgp-enterprise]] · [[ceng-routing-fundamentals]]
13. 每步：**Review** + **Explain-back**
""",
        "guide": """## 建议学习顺序

与 [[domains/ip-routing/overview#建议学习顺序]] 同步。按 IGP → 策略 → BGP → 组播 → Stevens/TCP CC 分层；ENCOR/ENARSI 见各书表。
""",
    },
    "network-architecture": {
        "overview": """## 建议学习顺序

**Track A — 架构师角色（所有人先走）：**

1. [[network-architect-role]] → [[network-architect-in-organization]] → [[network-design-principles]] → [[network-architect-career-roadmap]]

**Track B — 基础与园区：**

2. [[network-architecture-routing-switching]] → [[switch-fundamentals-review]] → [[campus-network-design]] → [[campus-vlan-trunking]] → [[spanning-tree-protocol]] → [[first-hop-redundancy-protocols]]

**Track C — CCDE 设计：**

3. [[ccde-design-requirements-process]] → [[ccde-network-design-tradeoffs]] → [[ccde-enterprise-wan-architecture]] → [[ccde-evpn-vxlan-transport-design]] → [[ccde-practical-exam-methodology]]

**Track D — ENCOR / ENSLD 企业设计：**

4. [[encor-packet-forwarding-cef]] → [[encor-enterprise-architecture-fabric]] → [[ensld-ipv4-design]] → [[ensld-enterprise-lan-design]] → [[ensld-enterprise-wan-design]] → [[ensld-sd-access-design]] → [[ensld-sdwan-design]]

**Track E — 无线：**

5. [[campus-wlan-fundamentals]] → [[enwl-design-requirements]] → [[enwl-site-survey]] → [[cwdp-requirements-planning]] → [[cwdp-wlan-security-design]]

**Track F — SDN / SD-Access / 自动化：**

6. [[sdn-use-cases]] → [[sdn-software-stack]] → [[sda-campus-fabric-fundamentals]] → [[network-automation-architecture]] → [[ansible-network-automation]] → [[yang-netconf-restconf]]

**Track G — 专著 / 深度（按需）：**

7. [[pina-foundations-network-architecture]] → [[ana-business-driven-design]] → [[nnc-speed-state-surface]] → [[icns-enterprise-pin-architecture]] → [[cisco-msdc-fabric-topology]] → [[vxlan-evpn-multisite-vpc-bgw-dci]]

8. 每步：**Review** + **Explain-back** · 证书/书表细节 → [[domains/network-architecture/guide]]
""",
        "guide": """## 建议学习顺序

与 [[domains/network-architecture/overview#建议学习顺序]] 同步（Track A–G）。

**按目标选轨：** 职业/原则 → A；园区 L2/L3 → B；CCDE → C；ENCOR/ENSLD → D；无线 CWDP/ENWL → E；SD-Access/自动化 → F；PINA/ANA/NNC/MSDC → G。

各书概念索引见本页下方 ENCOR / ENSLD / CWDP / CCDE / SD-Access 等表格。
""",
    },
    "network-security": {
        "overview": """## 建议学习顺序

1. **安全基础（NS 核心 9）** — [[ns-security-introduction]] → [[ns-security-design-principles]] → [[ns-cryptographic-primitives]] → [[ns-key-distribution]] → [[ns-authentication-protocols]] → [[ns-transport-security-tls]] → [[ns-infrastructure-security]] → [[ns-subsystem-security]] → [[ns-firewalls-zero-trust]]
2. **SCOR 350-701** — [[scor-cybersecurity-fundamentals]] → [[scor-cryptography-pki]] → [[scor-aaa-identity]] → [[scor-secure-firewall]] → [[scor-vpn-security]] → [[scor-endpoint-protection]] → [[scor-network-visibility-segmentation]] → [[scor-infrastructure-security]] → [[scor-content-security]] → [[scor-cloud-security]] → [[scor-sdn-security-automation]]
3. **ISE / 准入（CISE）** — [[cise-platform-architecture]] → [[cise-identity-unified-access]] → [[cise-authn-authz-policies]] → [[cise-nac-policy-framework]] → [[cise-guest-cwa-lifecycle]] → [[cise-posture-supplicants-byod]] → [[cise-trustsec-pxgrid]] → [[cise-scale-vpn-phasing]]
4. **ENCOR 安全章** — [[encor-security-infrastructure]] · [[cnda-asa-security-acls]]
5. 每步：**Review** + **Explain-back**
""",
        "guide": """## 建议学习顺序

与 [[domains/network-security/overview#建议学习顺序]] 相同：NS 核心 → SCOR → CISE → ENCOR/ASA 速查。
""",
    },
    "design-thinking": {
        "overview": """## 建议学习顺序

详见 [[domains/design-thinking/guide#建议顺序]]：

1. [[design-thinking-overview]] → [[design-thinking-principles]]
2. [[design-thinking-empathy]] → [[design-thinking-observation]] → [[design-thinking-understand-task]]
3. [[design-thinking-problem-reframe]] → [[design-thinking-ideation]]
4. [[design-thinking-evaluation-prototyping]] → [[design-thinking-testing-implementation]] → [[design-thinking-project-setup]]
5. 每步：**Review** + **Explain-back**
""",
        "guide": """## 建议顺序

1. [[design-thinking-overview]] → [[design-thinking-principles]]
2. [[design-thinking-empathy]] → [[design-thinking-observation]] → [[design-thinking-understand-task]]
3. [[design-thinking-problem-reframe]] → [[design-thinking-ideation]]
4. [[design-thinking-evaluation-prototyping]] → [[design-thinking-testing-implementation]] → [[design-thinking-project-setup]]
5. 每步：**Review** + **Explain-back**
""",
    },
    "research-methods": {
        "overview": """## 建议学习顺序

详见 [[domains/research-methods/guide#建议顺序]]：

1. [[cor-thinking-in-print]] → [[cor-reader-writer-roles]] → [[cor-research-argument-model]]
2. [[cor-topic-to-question]] → [[cor-research-problem]] → [[cor-research-ethics]]
3. [[cor-finding-evaluating-sources]] → [[cor-engaging-sources]]
4. [[cor-claims-reasons-evidence]] → [[cor-acknowledgments-warrants]]
5. [[cor-planning-drafting-citation]] → [[cor-clear-writing-style]] → [[cor-introductions-conclusions]] → [[cor-visual-evidence]] → [[cor-revising-argument]]
6. 每步：**Review** + **Explain-back**
""",
        "guide": """## 建议顺序

1. [[cor-thinking-in-print]] → [[cor-reader-writer-roles]] → [[cor-research-argument-model]]
2. [[cor-topic-to-question]] → [[cor-research-problem]] → [[cor-research-ethics]]
3. [[cor-finding-evaluating-sources]] → [[cor-engaging-sources]]
4. [[cor-claims-reasons-evidence]] → [[cor-acknowledgments-warrants]]
5. [[cor-planning-drafting-citation]] → [[cor-clear-writing-style]] → [[cor-introductions-conclusions]] → [[cor-visual-evidence]] → [[cor-revising-argument]]
6. 每步：**Review** + **Explain-back**
""",
    },
    "hardware-defined-networking": {
        "overview": """## 建议学习顺序

详见 [[domains/hardware-defined-networking/guide#Study path]]：

1. [[hdn-foundation-principles]] → [[hdn-terminology]] → [[hdn-forwarding-system-architecture]]
2. [[hdn-forwarding-protocols]] → [[hdn-network-virtualization]] → [[hdn-overlay-protocols]] → [[hdn-tunnels]] → [[hdn-vpn]]
3. [[hdn-routing-hardware]] → [[hdn-load-balancing]] → [[hdn-multicast-hardware]] → [[hdn-connections]]
4. [[hdn-qos-hardware]] → [[hdn-time-sync-oam]] → [[hdn-security-searching-filters]]
5. 每步：**Review** + **Explain-back**
""",
        "guide": """## Study path

1. [[hdn-foundation-principles]] → [[hdn-terminology]] → [[hdn-forwarding-system-architecture]]
2. [[hdn-forwarding-protocols]] → [[hdn-network-virtualization]] → [[hdn-overlay-protocols]] → [[hdn-tunnels]] → [[hdn-vpn]]
3. [[hdn-routing-hardware]] → [[hdn-load-balancing]] → [[hdn-multicast-hardware]] → [[hdn-connections]]
4. [[hdn-qos-hardware]] → [[hdn-time-sync-oam]] → [[hdn-security-searching-filters]]
5. 每步：**Review** + **Explain-back**
""",
    },
}

# Headings to replace (first match per file type)
OVERVIEW_HEADINGS = [
    r"## 建议学习顺序",
    r"## Study path",
]
GUIDE_HEADINGS = [
    r"## 建议学习顺序",
    r"## 建议顺序",
    r"## Study path",
    r"## 推荐学习路径（书章顺序）",
]

INSERT_BEFORE = [
    r"## 尚未覆盖",
    r"## Gaps",
    r"## 缺口",
    r"## 术语",
    r"## 术语表",
    r"---\s*\n\n## 术语",
]

TIERS_HEADING = r"## 掌握度分层"
PROGRESS_HEADING = r"## 学习进度"
CONSOLIDATE_HEADING = r"## 待巩固"

STUDY_PATH_HEADINGS = frozenset({"## 建议学习顺序", "## Study path"})
STUDY_TOP_HEADINGS = STUDY_PATH_HEADINGS
STUDY_END_HEADINGS: frozenset[str] = frozenset()
REMOVED_FROM_OVERVIEW = frozenset({"## 待巩固", "## 学习进度", "## 掌握度分层"})


def is_defer_heading(h: str) -> bool:
    if h in {"## Gaps", "## 尚未覆盖", "## 缺口", "## 术语", "## 术语表"}:
        return True
    return h.startswith(("## Gaps", "## 尚未覆盖", "## 缺口", "## 术语"))

SECTION_SPLIT = re.compile(r"^(## .+)$", re.M)


def replace_or_insert(text: str, headings: list[str], new_block: str) -> str:
    new_block = new_block.strip() + "\n"
    for h in headings:
        pat = re.compile(rf"{h}\n.*?(?=\n## |\n---\n\n## |\Z)", re.S)
        if pat.search(text):
            return pat.sub(new_block + "\n", text, count=1)
    for before in INSERT_BEFORE:
        m = re.search(rf"\n({before})", text)
        if m:
            return text[: m.start()] + "\n\n" + new_block + "\n" + text[m.start() :]
    return text.rstrip() + "\n\n" + new_block + "\n"


def bump_updated(text: str, date: str) -> str:
    # Repair merged closing delimiter (breaks Obsidian frontmatter → red render)
    text = re.sub(
        r"^updated:\s*(\d{4}-\d{2}-\d{2})---\s*$",
        r"updated: \1\n---",
        text,
        count=1,
        flags=re.M,
    )
    if re.search(r"^updated:\s*", text, re.M):
        return re.sub(r"^updated:\s*.*$", f"updated: {date}", text, count=1, flags=re.M)
    return text


def replace_section(text: str, heading_pattern: str, new_block: str) -> str:
    new_block = new_block.strip() + "\n"
    pat = re.compile(rf"({heading_pattern}\n).*?(?=\n## |\n---\n\n## |\Z)", re.S)
    if pat.search(text):
        return pat.sub(new_block + "\n", text, count=1)
    return text


def split_h2_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    parts = SECTION_SPLIT.split(text)
    if len(parts) < 3:
        return text, []
    preamble = parts[0]
    sections: list[tuple[str, str]] = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((heading, f"{heading}\n{body}".rstrip() + "\n"))
    return preamble, sections


def reorder_overview_study_sections(text: str) -> str:
    """建议学习顺序 first; then body; Gaps/术语 last."""
    preamble, sections = split_h2_sections(text)
    if not sections:
        return text
    by_head = {h: block for h, block in sections}
    order = [h for h, _ in sections]

    def pick(headings: frozenset[str]) -> list[str]:
        return [by_head[h] for h in order if h in headings]

    first = pick(STUDY_PATH_HEADINGS)
    taken = STUDY_TOP_HEADINGS | STUDY_END_HEADINGS | REMOVED_FROM_OVERVIEW
    middle = [by_head[h] for h in order if h not in taken and not is_defer_heading(h)]
    tail = pick(STUDY_END_HEADINGS) + [by_head[h] for h in order if is_defer_heading(h)]

    blocks = [b.rstrip() for b in first + middle + tail if b.strip()]
    if not blocks:
        return text
    return preamble.rstrip() + "\n\n" + "\n\n".join(blocks) + "\n"


def remove_section_by_heading(text: str, heading: str) -> str:
    pat = re.compile(rf"\n{re.escape(heading)}\n.*?(?=\n## |\Z)", re.S)
    return pat.sub("\n", text)


def strip_progress_sections(text: str) -> str:
    for h in REMOVED_FROM_OVERVIEW:
        text = remove_section_by_heading(text, h)
    return text


def domain_title_from_overview(text: str, slug: str) -> str:
    m = re.search(r"^# (.+?) —", text, re.M)
    if m:
        return m.group(1).strip()
    return slug.replace("-", " ").title()


def inject_study_link(text: str, slug: str) -> str:
    link = f"[[domains/{slug}/study]]"
    if link in text:
        text = text.replace("见下方进度表", f"见 {link}")
        return text
    line = (
        f"\n> **学习进度与待巩固：** {link}"
        f"（按 Tier 分表：Solid 候选 / 读过未测 / 待复习 + 掌握度）\n"
    )
    m = re.search(r"\n---\n\n## (建议学习顺序|Study path)", text)
    if m:
        text = text[: m.start()] + line + text[m.start() :]
    else:
        text = text.rstrip() + line + "\n"
    return text.replace("见下方进度表", f"见 {link}")


def remove_tiers_section(text: str) -> str:
    return remove_section_by_heading(text, "## 掌握度分层")


def apply_study_path(text: str, slug: str, path_md: str) -> str:
    block = path_md
    if slug in TIERS:
        block = format_unified_study_order(strip_study_heading(path_md), TIERS[slug])
    return replace_or_insert(text, OVERVIEW_HEADINGS, block)


def sync_overview_extras(text: str, slug: str) -> str:
    """Strip embedded progress blocks; link to domains/<slug>/study.md."""
    text = strip_progress_sections(text)
    text = remove_tiers_section(text)
    text = inject_study_link(text, slug)
    return reorder_overview_study_sections(text)


def write_study_page(dom_dir: Path, slug: str, overview_text: str, updated: str) -> str:
    title = domain_title_from_overview(overview_text, slug)
    spec = TIERS.get(slug)
    return format_study_page(slug, title, spec, updated)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("vault_wiki", type=Path, help="Path to vault wiki/ directory")
    p.add_argument("--date", default="2026-06-01", help="Frontmatter updated date")
    p.add_argument(
        "--tiers-only",
        action="store_true",
        help="Update study.md + overview study link; re-annotate 建议学习顺序; skip PATHS text",
    )
    p.add_argument("--paths-only", action="store_true", help="Update study paths only; skip tiers")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if args.tiers_only and args.paths_only:
        p.error("use at most one of --tiers-only and --paths-only")
    wiki = args.vault_wiki.resolve()
    domains_dir = wiki / "domains"
    do_paths = not args.tiers_only
    do_tiers = not args.paths_only
    n = 0
    for dom in sorted(domains_dir.iterdir()):
        if not dom.is_dir():
            continue
        slug = dom.name
        ov = dom / "overview.md"
        if not ov.is_file():
            continue
        text = ov.read_text(encoding="utf-8")
        new_text = text
        if (do_paths or do_tiers) and slug in PATHS and "overview" in PATHS[slug]:
            new_text = apply_study_path(new_text, slug, PATHS[slug]["overview"])
        if do_tiers:
            new_text = sync_overview_extras(new_text, slug)
            study_md = dom / "study.md"
            study_content = write_study_page(dom, slug, new_text, args.date)
            old_study = study_md.read_text(encoding="utf-8") if study_md.is_file() else ""
            if study_content != old_study and not args.dry_run:
                study_md.write_text(study_content, encoding="utf-8")
            if study_content != old_study:
                n += 1
                print(f"study: {study_md}")
        new_text = bump_updated(new_text, args.date)
        if new_text != text:
            n += 1
            print(f"overview: {ov}")
            if not args.dry_run:
                ov.write_text(new_text, encoding="utf-8")
        if do_paths and slug in PATHS and "guide" in PATHS[slug]:
            gd = dom / "guide.md"
            if gd.is_file():
                gtext = gd.read_text(encoding="utf-8")
                gnew = replace_or_insert(gtext, GUIDE_HEADINGS, PATHS[slug]["guide"])
                gnew = bump_updated(gnew, args.date)
                if gnew != gtext:
                    n += 1
                    print(f"guide: {gd}")
                    if not args.dry_run:
                        gd.write_text(gnew, encoding="utf-8")
    print(f"updated {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
