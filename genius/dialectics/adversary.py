"""Adversarial Red-Team Simulator & Refutation Verdict Engine.

Simulates the fiercest possible opposing counsel and skeptical bench:
  - Subjecting every estate motion and proposition to adversarial attack.
  - Identifying unaddressed vulnerabilities, missing predicate proofs, and potential defenses.
  - Generating concrete AdversaryVerdict objects with factual refutation metrics rather than feelings.
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from .deduction import LogicProposition

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AdversaryVerdict:
    target_claim_id: str
    refuted: bool
    challengers: List[str]
    vulnerabilities: List[str]
    survival_confidence: float  # 0.0 to 1.0 (1.0 = survived all attacks)
    verdict_note: str
    digest: str = ""
    provenance: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_claim_id": self.target_claim_id,
            "refuted": self.refuted,
            "challengers": self.challengers,
            "vulnerabilities": self.vulnerabilities,
            "survival_confidence": self.survival_confidence,
            "verdict_note": self.verdict_note,
            "digest": self.digest,
            "provenance": self.provenance,
        }


class AdversarySimulator:
    """Stress-tests legal and tactical claims against adversarial refutation."""

    def test_claim(
        self,
        claim: LogicProposition,
        belief_set: Dict[str, LogicProposition],
        known_opposing_arguments: List[str] = None,
    ) -> AdversaryVerdict:
        """Subject claim to red-team attack and generate AdversaryVerdict.
        
        # WHY: Simulating hostile counsel before filing identifies structural vulnerabilities
        # in the legal theory while they can still be reinforced with additional exhibits.
        """
        try:
            challengers: List[str] = []
            for pid, prop in belief_set.items():
                if claim.id in prop.contradicts or pid in claim.contradicts:
                    challengers.append(pid)

            challengers = list(dict.fromkeys(challengers))
            refuted = any(belief_set[c].truth == "true" for c in challengers if c in belief_set)

            vulns = known_opposing_arguments or []
            if not claim.supports:
                vulns.append("Claim lacks supporting L0 evidence anchors.")

            confidence = 0.0 if refuted else max(0.1, 1.0 - (len(vulns) * 0.15))
            note = (
                "CLAIM REFUTED: Incompatible with established ground truth."
                if refuted
                else (
                    "SURVIVED ATTACK: Impervious to known adversarial challenges."
                    if not vulns
                    else f"SURVIVED WITH WARNINGS: {len(vulns)} vulnerability points noted."
                )
            )
        except Exception as e:
            err_msg = str(e)
            logger.error("Adversary simulation error: %s", err_msg)
            refuted, challengers, vulns, confidence, note = False, [], [f"Error: {err_msg}"], 0.5, "ERROR"

        raw = f"{claim.id}:{refuted}:{confidence}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        return AdversaryVerdict(
            target_claim_id=claim.id,
            refuted=refuted,
            challengers=challengers,
            vulnerabilities=vulns,
            survival_confidence=round(confidence, 2),
            verdict_note=note,
            digest=digest_str,
            provenance=f"adversary://verdict/{claim.id}",
        )
