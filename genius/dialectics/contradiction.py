"""Contradiction Hunter & Inconsistency Isolation Engine.

Hunts and exposes structural contradictions across:
  - Witness testimony vs. contemporaneous audio/video recordings
  - Sworn court declarations vs. bank/medical timestamps
  - Ex parte representations vs. official JEFS filing metadata
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from .deduction import LogicProposition

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ContradictionCluster:
    cluster_id: str
    proposition_a: str
    statement_a: str
    proposition_b: str
    statement_b: str
    severity: str
    resolution_status: str
    digest: str = ""
    provenance: str = ""


class ContradictionHunter:
    """Detects mutually incompatible claims within a belief set."""

    def __init__(self) -> None:
        # WHY: Isolating contradictions early provides the highest-leverage attack vector in adversarial litigation
        self.clusters: List[ContradictionCluster] = []

    def hunt(self, propositions: Dict[str, LogicProposition]) -> List[ContradictionCluster]:
        """Hunt contradictions across all asserted propositions.
        
        # WHY: Contradictions between sworn statements and physical evidence
        # trigger Falsus in Uno disqualification of opposing declarants.
        """
        self.clusters.clear()
        try:
            for pid, prop in propositions.items():
                for other_id in prop.contradicts:
                    if other_id not in propositions:
                        continue
                    other = propositions[other_id]
                    if prop.truth != "unknown" and other.truth != "unknown":
                        cid = f"CONTRADICTION_{pid}_VS_{other_id}"
                        raw = f"{cid}:{prop.statement[:32]}:{other.statement[:32]}".encode("utf-8")
                        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
                        cluster = ContradictionCluster(
                            cluster_id=cid,
                            proposition_a=pid,
                            statement_a=prop.statement,
                            proposition_b=other_id,
                            statement_b=other.statement,
                            severity="FATAL" if prop.truth == "true" and other.truth == "true" else "HIGH",
                            resolution_status="SURFACED_FOR_ADJUDICATION",
                            digest=digest_str,
                            provenance=f"contradiction://cluster/{cid}",
                        )
                        self.clusters.append(cluster)
        except Exception as e:
            err_msg = str(e)
            logger.error("Error hunting contradictions: %s", err_msg)

        return list(self.clusters)

    def audit(self) -> Dict[str, Any]:
        """Audit contradiction isolation state with cryptographic provenance.
        
        # WHY: Auditing contradictions ensures no unresolved factual conflicts remain hidden.
        """
        raw = f"CONTRADICTIONS:{len(self.clusters)}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        return {
            "total_contradictions_isolated": len(self.clusters),
            "digest": digest_str,
            "provenance": "contradiction_hunter_v1",
            "clusters": [c.__dict__ for c in self.clusters],
        }
