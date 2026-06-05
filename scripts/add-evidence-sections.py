#!/usr/bin/env python3
"""Add ## Evidence tables to ACI concept pages (one-time helper)."""

from pathlib import Path

VAULT = Path.home() / "Obsidian/zhuomo-vault/wiki/concepts"
SRC = "sources/cisco-aci-design-guide-2024/md"

EVIDENCE: dict[str, list[tuple[str, str]]] = {
    "aci-spine-leaf-topology.md": [
        ("Physical topology / leaf–spine roles", f"{SRC}/part-001#physical-topology"),
        ("Multi-tier design", f"{SRC}/part-001#multi-tier-design-considerations"),
        ("FEX limitations", f"{SRC}/part-001#fabric-extenders-fex"),
        ("Per-leaf RBAC", f"{SRC}/part-001#per-leaf-rbac-role-based-access-control"),
        ("Border leaf placement", f"{SRC}/part-001#placement-of-outside-connectivity"),
    ],
    "aci-apic.md": [
        ("APIC design / clustering", f"{SRC}/part-002#cisco-apic-design-considerations"),
        ("APIC teaming", f"{SRC}/part-002#cisco-apic-teaming"),
        ("Port tracking + APIC ports", f"{SRC}/part-002#port-tracking-and-cisco-apic-ports"),
        ("Cluster sizing / standby", f"{SRC}/part-002#cluster-sizing-and-redundancy"),
        ("Fabric recovery", f"{SRC}/part-002#fabric-recovery"),
        ("In-band static routes", f"{SRC}/part-002#creation-of-a-static-route-for-in-band-management"),
    ],
    "aci-fabric-underlay.md": [
        ("Fabric infrastructure configs", f"{SRC}/part-002#fabric-infrastructure-configurations"),
        ("VLAN pools / TEP (underlay)", f"{SRC}/part-002#defining-vlan-pools-and-domains"),
        ("Faster convergence / MTU", f"{SRC}/part-002#configuring-the-fabric-infrastructure-for-faster-convergence"),
        ("IS-IS metric", f"{SRC}/part-002#is-is-metric-for-redistributed-routes"),
    ],
    "aci-leaf-forwarding-profile.md": [
        ("Forwarding profiles / scale", f"{SRC}/part-001#leaf-switches"),
        ("vPC + hardware profiles", f"{SRC}/part-001#vpc-and-hardware-profiles"),
    ],
    "aci-vlan-pools-aaep.md": [
        ("Fabric access design", f"{SRC}/part-002#designing-the-fabric-access"),
        ("AAEPs", f"{SRC}/part-002#attachable-access-entity-profiles-aaeps"),
        ("VLAN ↔ VXLAN mapping", f"{SRC}/part-002#understanding-vlan-use-in-cisco-aci-and-to-which-vxlan-they-are-mapped"),
        ("Overlapping VLAN ranges", f"{SRC}/part-002#overlapping-vlan-ranges"),
        ("Domain / EPG VLAN validation", f"{SRC}/part-002#domain-and-epg-vlan-validations"),
        ("LLDP / CDP policy", f"{SRC}/part-002#cisco-discovery-protocol-lldp-and-policy-resolution"),
    ],
    "aci-vpc-design.md": [
        ("vPC hardware compatibility", f"{SRC}/part-001#hardware-compatibility-between-vpc-pairs"),
        ("vPC member ports / FEX", f"{SRC}/part-001#vpc-and-fex"),
        ("vPC consistency / F3274", f"{SRC}/part-003#vpc-consistency-checks"),
        ("Orphan ports", f"{SRC}/part-003#orphan-ports"),
        ("Port tracking", f"{SRC}/part-003#port-tracking"),
        ("Faster convergence with vPCs", f"{SRC}/part-002#configuration-for-faster-convergence-with-vpcs"),
        ("L3Out with vPC", f"{SRC}/part-004#l3out-with-vpc"),
    ],
    "aci-tenant-epg-contract.md": [
        ("Designing tenant network", f"{SRC}/part-003#designing-the-tenant-network"),
        ("Network- vs app-centric / ESG", f"{SRC}/part-003#network-centric-and-application-centric-designs-and-epgs-compared-with-esgs"),
        ("Naming conventions", f"{SRC}/part-002#naming-of-cisco-aci-objects"),
        ("tenant common / VRF", f"{SRC}/part-003#vrf-instances-and-bridge-domains-in-the-common-tenant"),
        ("Contracts design", f"{SRC}/part-003#contracts-design-considerations"),
        ("Contract direction / stateful", f"{SRC}/part-004#concept-of-direction-in-contracts"),
        ("Contracts in common tenant", f"{SRC}/part-004#contracts-and-filters-in-the-common-tenant"),
    ],
    "aci-endpoint-learning-controls.md": [
        ("Loop mitigation overview", f"{SRC}/part-003#loop-mitigation-features-overview"),
        ("Move dampening / loop / rogue", f"{SRC}/part-003#endpoint-move-dampening-endpoint-loop-protection-and-rogue-endpoint-control"),
        ("Endpoint learning (deep)", f"{SRC}/part-004#endpoint-learning-considerations"),
        ("Endpoint retention policy", f"{SRC}/part-004#endpoint-retention-policy-at-the-bridge-domain-and-vrf-level"),
        ("Enforce subnet check", f"{SRC}/part-004#enforce-subnet-check"),
        ("Endpoint aging", f"{SRC}/part-004#endpoint-aging"),
        ("Endpoint listen policy", f"{SRC}/part-003#endpoint-listen-policy-beta"),
    ],
    "aci-border-leaf-l3out.md": [
        ("Border leaf placement", f"{SRC}/part-001#placement-of-outside-connectivity"),
        ("L3Out evolution / model", f"{SRC}/part-004#layer-3-outside-l3out-and-external-routed-networks"),
        ("L3Out simplified object model", f"{SRC}/part-004#l3out-simplified-object-model"),
        ("Router ID", f"{SRC}/part-004#l3out-router-id-considerations"),
        ("Border leaf designs", f"{SRC}/part-004#border-leaf-switch-designs"),
        ("L3Out with vPC", f"{SRC}/part-004#l3out-with-vpc"),
        ("DEC / multi border leaf", f"{SRC}/part-005#using-dynamic-l3out-epg-classification-dec"),
    ],
}


def render_evidence(rows: list[tuple[str, str]]) -> str:
    lines = ["## Evidence", "", "| 要点 | 原文 |", "|------|------|"]
    for topic, link in rows:
        lines.append(f"| {topic} | [[{link}]] |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    for fname, rows in EVIDENCE.items():
        path = VAULT / fname
        text = path.read_text(encoding="utf-8")
        block = render_evidence(rows)
        if "## Evidence" in text:
            # replace existing evidence section up to ## Sources
            import re

            text = re.sub(
                r"## Evidence\n.*?(?=\n## Sources)",
                block.rstrip(),
                text,
                count=1,
                flags=re.DOTALL,
            )
        else:
            text = text.replace("\n## Sources\n", f"\n{block}## Sources\n", 1)
        # normalize Sources footer
        old_sources = "- [[sources/cisco-aci-design-guide-2024]]"
        new_sources = (
            "- **Raw EPUB:** `~/zhuomo-data/raw/books/cisco-application-centric-infrastructure-design-guide.epub`\n"
            "- **MD 全文:** [[sources/cisco-aci-design-guide-2024/md/index]]\n"
            "- **Source 索引:** [[sources/cisco-aci-design-guide-2024]]"
        )
        if old_sources in text and "**MD 全文:**" not in text:
            text = text.replace(
                f"{old_sources} —",
                new_sources + "\n- 章节索引 —",
                1,
            )
            # also handle lines that only have wiki link
            if "**MD 全文:**" not in text:
                text = re.sub(
                    r"## Sources\n\n- \[\[sources/cisco-aci-design-guide-2024\]\][^\n]*",
                    f"## Sources\n\n{new_sources}",
                    text,
                    count=1,
                )
        path.write_text(text, encoding="utf-8")
        print(f"Updated {fname}")


if __name__ == "__main__":
    main()
