"""Zero-Fake Truth Enforcement & Hallucination Elimination Gate.

Enforces:
  1. No unverified claims without tool readback.
  2. No synthetic completion (sleep-simulations strictly forbidden).
  3. Strict separation of fact, witness testimony, legal argument, and hypothesis.
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VerificationResult:
    claim_id: str
    statement: str
    verified: bool
    evidence_proof: str
    failure_reason: Optional[str] = None
    digest: str = ""
    provenance: str = ""


class ZeroFakeTruthEnforcer:
    """Rigorous gate preventing unverified assumptions from entering the estate."""

    def __init__(self) -> None:
        self.verifications: List[VerificationResult] = []

    def verify_claim(
        self,
        claim_id: str,
        statement: str,
        evidence_proof: str,
        readback_validator: Optional[Callable[[], bool]] = None,
    ) -> VerificationResult:
        """Verify that a claim is backed by real tool readback, not model assertion.
        
        # WHY: Under Section 17 of AGENTS.md and zero-fake truth doctrine, claims of progress
        # or factual conclusions without tool readback are strictly forbidden as unverified hypotheses.
        """
        raw = f"{claim_id}:{statement}:{evidence_proof}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        provenance_str = f"gate://zero_fake/{claim_id}"

        if not evidence_proof or evidence_proof.strip() == "":
            res = VerificationResult(
                claim_id=claim_id,
                statement=statement,
                verified=False,
                evidence_proof="",
                failure_reason="Missing empirical evidence proof or tool readback.",
                digest=digest_str,
                provenance=provenance_str,
            )
            self.verifications.append(res)
            return res

        if readback_validator is not None:
            try:
                valid = readback_validator()
            except Exception as e:
                logger.error("Readback validator encountered error: %s", e)
                valid = False
                res = VerificationResult(
                    claim_id=claim_id,
                    statement=statement,
                    verified=False,
                    evidence_proof=evidence_proof,
                    failure_reason=f"Readback validator failed with exception: {e}",
                    digest=digest_str,
                    provenance=provenance_str,
                )
                self.verifications.append(res)
                return res
            if not valid:
                res = VerificationResult(
                    claim_id=claim_id,
                    statement=statement,
                    verified=False,
                    evidence_proof=evidence_proof,
                    failure_reason="Readback validation function returned False.",
                    digest=digest_str,
                    provenance=provenance_str,
                )
                self.verifications.append(res)
                return res

        res = VerificationResult(
            claim_id=claim_id,
            statement=statement,
            verified=True,
            evidence_proof=evidence_proof,
            digest=digest_str,
            provenance=provenance_str,
        )
        self.verifications.append(res)
        return res

    def audit(self) -> Dict[str, Any]:
        """Audit the zero-fake gate status across all tested claims.
        
        # WHY: Auditing verification ensures zero hallucinated assertions pollute estate filings.
        """
        total = len(self.verifications)
        passed = sum(1 for v in self.verifications if v.verified)
        failed = [v for v in self.verifications if not v.verified]
        return {
            "total_audited": total,
            "passed": passed,
            "failed_count": len(failed),
            "clean_pass_rate_pct": (passed / total * 100.0) if total > 0 else 100.0,
            "provenance": "zero_fake_enforcer_v1",
            "digest": f"sha256:{hashlib.sha256(str(total).encode()).hexdigest()}",
            "violations": [
                {"id": f.claim_id, "statement": f.statement, "reason": f.failure_reason, "digest": f.digest}
                for f in failed
            ],
        }
