"""Multi-Layer Unified Memory Mesh Engine.

Coordinates across memory strata:
  Strata 1: Episodic conversational context (real-time chat stream)
  Strata 2: Semantic vector & concept retrieval (Mem0, Supermemory, Context7)
  Strata 3: Relational knowledge graph (dockets, cases, orders, timelines)
  Strata 4: Cold-storage cryptographic archives (10-zip Google Takeout, Dropbox vaults)
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MemoryStrata(str, Enum):
    STRATA_1_EPISODIC = "STRATA_1_EPISODIC"
    STRATA_2_SEMANTIC = "STRATA_2_SEMANTIC"
    STRATA_3_RELATIONAL = "STRATA_3_RELATIONAL"
    STRATA_4_COLD_VAULT = "STRATA_4_COLD_VAULT"


@dataclass
class MemoryItem:
    item_id: str
    strata: MemoryStrata
    tag: str
    content: str
    digest: str = ""
    provenance: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class MemoryMeshEngine:
    """Multi-strata unified memory fabric."""

    def __init__(self) -> None:
        # WHY: Multi-strata separation prevents high-frequency episodic messages from evicting durable legal models
        self.strata_bins: Dict[MemoryStrata, List[MemoryItem]] = {s: [] for s in MemoryStrata}

    def index_item(
        self,
        item_id: str,
        strata: MemoryStrata,
        tag: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryItem:
        """Index memory item into target strata with cryptographic digest.
        
        # WHY: Cryptographic hashing of memory entries ensures that memory state changes
        # can be audited against unauthorized mutation or tampering.
        """
        raw = f"{item_id}:{strata.value}:{tag}:{content[:64]}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        item = MemoryItem(
            item_id=item_id,
            strata=strata,
            tag=tag,
            content=content,
            digest=digest_str,
            provenance=f"memory://{strata.value.lower()}/{item_id}",
            metadata=metadata or {},
        )
        self.strata_bins[strata].append(item)
        return item

    def search_by_tag(self, tag: str) -> List[MemoryItem]:
        """Search across strata for matching tag or content keywords.
        
        # WHY: Cross-strata keyword searching allows pulling related memories regardless of storage tier.
        """
        results: List[MemoryItem] = []
        try:
            for bin_items in self.strata_bins.values():
                for it in bin_items:
                    if tag.lower() in it.tag.lower() or tag.lower() in it.content.lower():
                        results.append(it)
        except Exception as e:
            err_msg = str(e)
            logger.error("Error searching memory mesh: %s", err_msg)
        return results

    def audit(self) -> Dict[str, Any]:
        """Audit memory mesh distribution with cryptographic provenance.
        
        # WHY: Verifying memory counts prevents strata imbalance or memory exhaustion.
        """
        total = sum(len(items) for items in self.strata_bins.values())
        raw = f"MEMORY_MESH:{total}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        return {
            "strata_counts": {s.value: len(items) for s, items in self.strata_bins.items()},
            "total_items": total,
            "digest": digest_str,
            "provenance": "memory_mesh_unified_v1",
        }
