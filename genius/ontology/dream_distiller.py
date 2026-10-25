"""Dream & Hierarchical Distillation Engine (Ontology Stone IV-B).

Replaces naive, lossy prose context compression with a continuously maintained
4-Tier Hierarchical Bulletpoint Memory Tree (`DREAM_DISTILLED_HIERARCHY.md`):
  - Tier L0: Sovereign Teleology & Immutable Invariants (Never pruned)
  - Tier L1: Strategic Pillars & Active Workstreams
  - Tier L2: Verified Operational State & Cryptographic Receipts (Hashes, Byte Counts, Exit Codes)
  - Tier L3: Granular Technical Coordinates, Aspen-Grove Pointers (@pointer:<id>), & Proactive Queue
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class HierarchicalNode:
    """A node in the Dream-Distilled Hierarchical Bulletpoint Tree."""

    tier: str  # L0, L1, L2, L3
    title: str
    summary: str
    children: List["HierarchicalNode"] = field(default_factory=list)
    pointers: List[str] = field(default_factory=list)
    verification_hash: Optional[str] = None

    def to_markdown(self, indent: int = 0) -> List[str]:
        prefix = "  " * indent + "- "
        hash_tag = f" `[hash:{self.verification_hash[:12]}]`" if self.verification_hash else ""
        ptr_tag = f" `({' '.join(self.pointers)})`" if self.pointers else ""
        lines = [f"{prefix}**[{self.tier}] {self.title}**: {self.summary}{hash_tag}{ptr_tag}"]
        for child in self.children:
            lines.extend(child.to_markdown(indent + 1))
        return lines


class DreamDistiller:
    """Consolidates episodic session events into a persistent hierarchical bulletpoint structure."""

    def __init__(
        self,
        hierarchy_md_path: str = "/root/DREAM_DISTILLED_HIERARCHY.md",
        hierarchy_json_path: str = "/root/DREAM_DISTILLED_HIERARCHY.json",
    ) -> None:
        self.md_path = Path(hierarchy_md_path)
        self.json_path = Path(hierarchy_json_path)
        self.roots: List[HierarchicalNode] = []

    def add_root_pillar(self, node: HierarchicalNode) -> None:
        """Register or update a top-level L0/L1 hierarchical node."""
        self.roots = [r for r in self.roots if r.title != node.title]
        self.roots.append(node)

    def distill_and_persist(self, mission_lock_path: str = "/root/ACTIVE_MISSION_LOCK.json") -> Dict[str, Any]:
        """Dream and distill current mission state + registered nodes into hierarchical bulletpoints."""
        lock_file = Path(lock_path := mission_lock_path)
        lock_data: Dict[str, Any] = {
            "mission_id": "PIXEL_TABLET_PRE_RESET_EVACUATION",
            "operator": "Casey Barton",
            "device": "Google Pixel Tablet",
            "ultimate_objective": "COMPLETE ZERO-DATA-LOSS EVACUATION TO ONEDRIVE PRIOR TO HARDWARE FACTORY RESET",
            "cloud_root": "onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/",
            "proactive_improvement": "ENABLED_ALWAYS_ON",
        }
        if lock_file.exists():
            try:
                lock_data.update(json.loads(lock_file.read_text(encoding="utf-8")))
            except Exception:
                pass
        else:
            try:
                lock_file.write_text(json.dumps(lock_data, indent=2), encoding="utf-8")
                md_lock = lock_file.with_suffix(".md")
                if not md_lock.exists():
                    md_lock.write_text(
                        "# ACTIVE MISSION LOCK (COMPACTION-IMMUNE INVARIANT)\n"
                        f"- **[L0] Primary Mission**: `{lock_data['ultimate_objective']}`\n"
                        f"- **[L1] Operator & Device**: `{lock_data['operator']}` (`{lock_data['device']}`)\n"
                        f"- **[L2] Cloud Root**: `{lock_data['cloud_root']}`\n"
                        "- **[L3] Mandatory Rule**: Always read `/root/ACTIVE_MISSION_LOCK.md` and `/root/DREAM_DISTILLED_HIERARCHY.md` on wakeup.\n",
                        encoding="utf-8",
                    )
            except Exception:
                pass

        now_iso = datetime.now(timezone.utc).isoformat()
        md_lines = [
            "# DREAM-DISTILLED HIERARCHICAL MEMORY MATRIX",
            f"> **Last Dream Consolidation:** `{now_iso}` | **Policy:** `Compression != Deletion (Hierarchical Bulletpoint Preservation)`",
            "",
            "## 1. [L0] Sovereign Teleology & Immutable Invariants",
            f"- **[L0] Primary Mission**: `{lock_data.get('ultimate_objective', 'COMPLETE ZERO-DATA-LOSS EVACUATION TO ONEDRIVE PRIOR TO HARDWARE FACTORY RESET')}`",
            f"  - **[L0.1] Operator & Hardware**: `{lock_data.get('operator', 'Casey Barton')}` on `{lock_data.get('device', 'Google Pixel Tablet')}`",
            f"  - **[L0.2] Cloud Vault Root**: `{lock_data.get('cloud_root', 'onedrive:PIXEL_TABLET_PRE_RESET_EVACUATION/')}`",
            "  - **[L0.3] Anti-Amnesia Invariant**: Context compression must never drop L0–L3 structural coordinates; always read `/root/ACTIVE_MISSION_LOCK.md` and `/root/DREAM_DISTILLED_HIERARCHY.md` on wakeup.",
            "  - **[L0.4] Rule §0 Evidentiary Lock**: Never purge a local file prior to `rclone check --one-way` returning `0 differences` (`quickxor` / `sha256`).",
            "  - **[L0.5] Proactive Improvement Law**: Fix and improve discovered defects, test friction, and architectural gaps in flight while advancing the Operator's position.",
            "",
            "## 2. [L1–L3] Distilled Operational Hierarchy",
        ]

        for root in self.roots:
            md_lines.extend(root.to_markdown(indent=0))

        raw_md = "\n".join(md_lines) + "\n"
        digest = "sha256:" + hashlib.sha256(raw_md.encode("utf-8")).hexdigest()

        self.md_path.write_text(raw_md, encoding="utf-8")
        state_obj = {
            "schema": "apex.dream-distilled-hierarchy/v1.0",
            "updated_at": now_iso,
            "digest": digest,
            "mission_lock_ref": lock_path,
            "root_count": len(self.roots),
            "nodes": [
                {
                    "tier": r.tier,
                    "title": r.title,
                    "summary": r.summary,
                    "pointers": r.pointers,
                    "verification_hash": r.verification_hash,
                    "children_count": len(r.children),
                }
                for r in self.roots
            ],
        }
        self.json_path.write_text(json.dumps(state_obj, indent=2), encoding="utf-8")
        return {
            "status": "DREAM_DISTILLED",
            "md_path": str(self.md_path),
            "json_path": str(self.json_path),
            "digest": digest,
            "root_nodes": len(self.roots),
        }
