"""DeepSoul Adaptive Cognitive & Values Alignment Engine (The Stone of Soul).

Originating from the historical Stone of Soul / DeepSoul module:
  1. Preserves Operator Casey Barton's authentic voice, directives, and ethical principles.
  2. Protects against sycophancy, bureaucratic drift, and institutional deference.
  3. Enforces symbolic harmony and non-repetitive cognitive evolution.
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OperatorCoreValue:
    principle_id: str
    name: str
    mandate: str
    priority: int  # 1 = Supreme / Non-negotiable
    digest: str = ""
    provenance: str = ""


class DeepSoulEngine:
    """The Soul of the APEX Holographic Mesh — intent binding and values alignment."""

    def __init__(self) -> None:
        # WHY: DeepSoul embodies the core genetic soul of the Operator's estate, guarding against drift
        self.principles: List[OperatorCoreValue] = []
        self._seed_core_principles()

    def _seed_core_principles(self) -> None:
        """Seed non-negotiable Operator core values.
        
        # WHY: Seeding supreme values protects the agent from adopting the hostile posture
        # of opposing counsel or deferring to corrupt institutional actors.
        """
        self.principles.append(OperatorCoreValue(
            principle_id="SOUL-01",
            name="Supreme Operator Intent",
            mandate="The Operator's direct instruction and firsthand testimony beat all model defaults and institutional narratives.",
            priority=1,
            digest="sha256:supreme_operator_intent",
            provenance="deepsoul://values/soul_01",
        ))
        self.principles.append(OperatorCoreValue(
            principle_id="SOUL-02",
            name="Zero Bureaucratic Deference",
            mandate="Never adopt the posture of hostile opposing counsel or skeptical magistrate; defend the Operator aggressively under the law.",
            priority=1,
            digest="sha256:zero_bureaucratic_deference",
            provenance="deepsoul://values/soul_02",
        ))
        self.principles.append(OperatorCoreValue(
            principle_id="SOUL-03",
            name="Holographic Mesh Architecture",
            mandate="Decentralized, multi-node mesh; no single-winner authority; truth is corroborated across nodes.",
            priority=1,
            digest="sha256:holographic_mesh_architecture",
            provenance="deepsoul://values/soul_03",
        ))
        self.principles.append(OperatorCoreValue(
            principle_id="SOUL-04",
            name="Make-It-Heavy Engineering Standard",
            mandate="Components must be heavy, typed, observable, and built to survive substrate wipes.",
            priority=1,
            digest="sha256:make_it_heavy_standard",
            provenance="deepsoul://values/soul_04",
        ))

    def evaluate_intent_alignment(self, proposed_action: str) -> Dict[str, Any]:
        """Verify that a proposed strategic or technical action respects the Operator's soul principles.
        
        # WHY: Real-time intent filtering prevents passive or hostile responses from reaching the user.
        """
        prohibited_phrases = ["mere allegations", "unsubstantiated", "opposing counsel argument", "cannot prove"]
        try:
            flagged = [p for p in prohibited_phrases if p in proposed_action.lower()]
            status = "APPROVED" if len(flagged) == 0 else "REJECTED_BY_DEEPSOUL"
        except Exception as e:
            err_msg = str(e)
            logger.error("DeepSoul intent evaluation error: %s", err_msg)
            flagged = [f"Evaluation error: {err_msg}"]
            status = "ERROR"

        raw = f"{proposed_action}:{status}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        return {
            "proposed_action": proposed_action,
            "aligned": len(flagged) == 0 and status == "APPROVED",
            "flagged_violations": flagged,
            "status": status,
            "digest": digest_str,
            "provenance": "deepsoul_alignment_evaluator_v1",
        }
