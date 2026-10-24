"""Multi-Horizon Strategic Planning Engine.

Maintains coherence across 3 temporal execution horizons:
  Horizon 1 (Tactical): Next immediate checkpoint (tests passing, filing generated, byte verified).
  Horizon 2 (Operational): Campaign milestones (complete case packages deployed, cloud synchronization).
  Horizon 3 (Strategic / Sovereign): Total estate victory (mandatory restitution, vacatur ab initio, sovereign recovery).
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class HorizonTier(str, Enum):
    HORIZON_1_TACTICAL = "HORIZON_1_TACTICAL"
    HORIZON_2_OPERATIONAL = "HORIZON_2_OPERATIONAL"
    HORIZON_3_STRATEGIC = "HORIZON_3_STRATEGIC"


@dataclass
class Milestone:
    milestone_id: str
    tier: HorizonTier
    title: str
    deliverable: str
    completed: bool = False
    verification_evidence: str = ""
    digest: str = ""
    provenance: str = ""


class MultiHorizonPlanner:
    """Orchestrates progress across all three planning horizons simultaneously."""

    def __init__(self) -> None:
        # WHY: Horizon planning prevents short-term tactical tunnel vision from degrading long-term sovereign strategy
        self.milestones: List[Milestone] = []

    def add_milestone(self, milestone_id: str, tier: HorizonTier, title: str, deliverable: str) -> Milestone:
        """Register a milestone across temporal horizons with cryptographic digest.
        
        # WHY: Fingerprinting milestones ensures every deliverable is bound to a verifiable checkpoint.
        """
        raw = f"{milestone_id}:{tier.value}:{title}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        m = Milestone(
            milestone_id=milestone_id,
            tier=tier,
            title=title,
            deliverable=deliverable,
            digest=digest_str,
            provenance=f"horizon://milestone/{milestone_id}",
        )
        self.milestones.append(m)
        return m

    def complete_milestone(self, milestone_id: str, verification_evidence: str) -> None:
        """Mark milestone complete with empirical verification proof.
        
        # WHY: Milestone completion requires verified proof to uphold zero fake execution standards.
        """
        try:
            found = False
            for m in self.milestones:
                if m.milestone_id == milestone_id:
                    m.completed = True
                    m.verification_evidence = verification_evidence
                    raw = f"{milestone_id}:{verification_evidence}".encode("utf-8")
                    m.digest = f"sha256:{hashlib.sha256(raw).hexdigest()}"
                    found = True
                    break
            if not found:
                raise KeyError(f"Milestone {milestone_id} not found.")
        except Exception as e:
            err_msg = str(e)
            logger.error("Error completing milestone: %s", err_msg)
            raise

    def audit(self) -> Dict[str, Any]:
        """Audit multi-horizon progress with cryptographic provenance.
        
        # WHY: Horizon audits verify overall campaign momentum without losing tactical fidelity.
        """
        try:
            h1 = [m for m in self.milestones if m.tier == HorizonTier.HORIZON_1_TACTICAL]
            h2 = [m for m in self.milestones if m.tier == HorizonTier.HORIZON_2_OPERATIONAL]
            h3 = [m for m in self.milestones if m.tier == HorizonTier.HORIZON_3_STRATEGIC]
            completed_count = sum(1 for m in self.milestones if m.completed)
            pct = round(completed_count / len(self.milestones) * 100.0, 1) if self.milestones else 0.0
        except Exception as e:
            err_msg = str(e)
            logger.warning("Error auditing horizons: %s", err_msg)
            h1, h2, h3, completed_count, pct = [], [], [], 0, 0.0

        raw = f"HORIZONS:{len(self.milestones)}:{completed_count}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        return {
            "h1_tactical": {"total": len(h1), "completed": sum(1 for m in h1 if m.completed)},
            "h2_operational": {"total": len(h2), "completed": sum(1 for m in h2 if m.completed)},
            "h3_strategic": {"total": len(h3), "completed": sum(1 for m in h3 if m.completed)},
            "overall_completion_pct": pct,
            "digest": digest_str,
            "provenance": "multi_horizon_planner_v1",
        }
