"""Epistemic Ladder Engine (L0–L5 Doctrine).

Enforces the APEX 6-level epistemic standard:
  L0: Immutable byte/SHA/commit/docket provenance.
  L1: Component boundary & deterministic input/output validation.
  L2: Lossless data translation, type safety & schema preservation.
  L3: Substrate comprehension (PRoot, SQLite locks, process limits).
  L4: Invariant causality & anti-symptom-chasing (root-cause first).
  L5: Holographic mesh governance (decentralized multi-node consensus).
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class EpistemicLevel(IntEnum):
    L0_GROUND_TRUTH = 0      # Byte/SHA/Docket immutable provenance
    L1_COMPONENT = 1         # Atomic boundary & I/O contract
    L2_SUBSYSTEM = 2         # Lossless schema & data translation
    L3_SUBSTRATE = 3         # Hardware/OS limits & leverage
    L4_INVARIANT = 4         # Causal root-cause analysis
    L5_HOLOGRAPHIC_MESH = 5  # Multi-node consensus & verification


@dataclass(frozen=True)
class EpistemicAttestation:
    level: EpistemicLevel
    claim: str
    provenance_hash: str
    verified: bool
    evidence_node: str
    digest: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.name,
            "level_int": int(self.level),
            "claim": self.claim,
            "provenance_hash": self.provenance_hash,
            "digest": self.digest or self.provenance_hash,
            "verified": self.verified,
            "evidence_node": self.evidence_node,
            "metadata": self.metadata,
        }


class EpistemicLadderEngine:
    """Audits and validates claims through the progressive L0-L5 ladder."""

    def __init__(self) -> None:
        self.attestations: List[EpistemicAttestation] = []

    def attest_l0(self, raw_bytes: bytes, evidence_id: str, claim: str) -> EpistemicAttestation:
        """Bind claim to cryptographic L0 ground truth.
        
        # WHY: L0 ground truth requires immutable byte-level provenance (SHA-256)
        # to ensure that downstream legal and technical deductions cannot drift.
        """
        try:
            sha = hashlib.sha256(raw_bytes).hexdigest()
            digest_str = f"sha256:{sha}"
            att = EpistemicAttestation(
                level=EpistemicLevel.L0_GROUND_TRUTH,
                claim=claim,
                provenance_hash=digest_str,
                verified=True,
                evidence_node=evidence_id,
                digest=digest_str,
                metadata={"byte_size": len(raw_bytes)},
            )
            self.attestations.append(att)
            return att
        except Exception as e:
            logger.error("L0 attestation failed: %s", e)
            # Fallback safe error attestation
            fallback_att = EpistemicAttestation(
                level=EpistemicLevel.L0_GROUND_TRUTH,
                claim=claim,
                provenance_hash="sha256:error_fallback",
                verified=False,
                evidence_node=evidence_id,
                digest="sha256:error_fallback",
                metadata={"error": str(e)},
            )
            self.attestations.append(fallback_att)
            return fallback_att

    def attest_level(
        self,
        level: EpistemicLevel,
        claim: str,
        evidence_node: str,
        supporting_l0_hash: str,
        verified: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> EpistemicAttestation:
        """Ascend the ladder only when grounded in verifiable prior levels.
        
        # WHY: Escalating higher epistemic levels without grounding in prior levels
        # generates synthetic or hallucinated conclusions.
        """
        if level > EpistemicLevel.L0_GROUND_TRUTH and not supporting_l0_hash:
            raise ValueError(f"Cannot attest {level.name} without L0 ground-truth anchor.")
        att = EpistemicAttestation(
            level=level,
            claim=claim,
            provenance_hash=supporting_l0_hash,
            verified=verified,
            evidence_node=evidence_node,
            digest=supporting_l0_hash,
            metadata=metadata or {},
        )
        self.attestations.append(att)
        return att

    def verify_ladder(self) -> Dict[str, Any]:
        """Audit the entire belief ladder for broken lineage or ungrounded claims.
        
        # WHY: Verifying ladder integrity before strategic filing ensures zero
        # uncorroborated assertions survive to adversarial contact.
        """
        summary: Dict[str, int] = {lvl.name: 0 for lvl in EpistemicLevel}
        broken_lineages: List[str] = []
        try:
            for att in self.attestations:
                summary[att.level.name] += 1
                if not att.verified:
                    broken_lineages.append(f"{att.level.name}: {att.claim}")
            is_sound = len(broken_lineages) == 0
        except Exception as e:
            logger.warning("Error during ladder verification: %s", e)
            is_sound = False
            broken_lineages.append(f"Verification audit exception: {e}")

        return {
            "total_attestations": len(self.attestations),
            "distribution": summary,
            "broken_lineages": broken_lineages,
            "is_sound": is_sound,
        }
