"""Bayesian Probabilistic Epistemology Engine.

Updates belief states mathematically based on accumulating evidentiary weight:
  Odds(H|E) = Odds(H) * ( P(E|H) / P(E|~H) )
  Posterior = Odds / (1 + Odds)
"""
from __future__ import annotations

import hashlib
import logging
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EvidenceUpdate:
    evidence_id: str
    description: str
    likelihood_ratio: float  # P(E|H) / P(E|~H)
    weight: float = 1.0
    digest: str = ""
    provenance: str = ""


class BayesianEpistemicUpdater:
    """Rigorous Bayesian belief state updater over forensic propositions."""

    def __init__(self, prior: float = 0.5) -> None:
        # WHY: Default prior of 0.5 represents maximum initial uncertainty under Laplace rule
        if not (0.0 < prior < 1.0):
            raise ValueError("Prior probability must be strictly between 0 and 1.")
        self.prior = prior
        self.updates: List[EvidenceUpdate] = []

    @property
    def prior_odds(self) -> float:
        return self.prior / (1.0 - self.prior)

    def add_evidence(
        self,
        evidence_id: str,
        description: str,
        likelihood_ratio: float,
        weight: float = 1.0,
    ) -> None:
        """Incorporate a new item of verified evidence.
        
        # WHY: Bayesian likelihood ratios mathematically prevent arbitrary belief swings
        # by requiring each update factor to reflect the probability of the evidence under H vs ~H.
        """
        if likelihood_ratio <= 0:
            raise ValueError("Likelihood ratio must be strictly positive.")
        try:
            raw = f"{evidence_id}:{likelihood_ratio}:{weight}".encode("utf-8")
            digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
            self.updates.append(EvidenceUpdate(
                evidence_id=evidence_id,
                description=description,
                likelihood_ratio=likelihood_ratio,
                weight=weight,
                digest=digest_str,
                provenance=f"bayes://update/{evidence_id}",
            ))
        except Exception as e:
            logger.error("Failed to append Bayesian evidence: %s", e)
            self.updates.append(EvidenceUpdate(
                evidence_id=evidence_id,
                description=description,
                likelihood_ratio=1.0,
                weight=0.0,
                digest="sha256:error_digest",
                provenance="bayes://fallback",
            ))

    def log_posterior_odds(self) -> float:
        """Accumulated log-odds to prevent floating-point underflow/overflow."""
        log_odds = math.log(self.prior_odds)
        for u in self.updates:
            if u.likelihood_ratio > 0 and u.weight != 0:
                log_odds += u.weight * math.log(u.likelihood_ratio)
        return log_odds

    def posterior_odds(self) -> float:
        log_odds = self.log_posterior_odds()
        if log_odds >= 700.0:
            return float("inf")
        if log_odds <= -700.0:
            return 0.0
        return math.exp(log_odds)

    def posterior_probability(self) -> float:
        log_odds = self.log_posterior_odds()
        if log_odds >= 700.0:
            return 1.0
        if log_odds <= -700.0:
            return 0.0
        # Sigmoid: 1 / (1 + exp(-log_odds))
        return 1.0 / (1.0 + math.exp(-log_odds))

    def audit(self) -> Dict[str, Any]:
        """Audit Bayesian belief state with full mathematical provenance.
        
        # WHY: Audit outputs must carry full numerical provenance to prevent
        # claims of unsupported statistical certainty or NaN model degradation.
        """
        try:
            p = self.posterior_probability()
            p_odds = self.posterior_odds()
            display_odds = float("inf") if math.isinf(p_odds) else round(p_odds, 4)
        except Exception as e:
            logger.warning("Error calculating posterior: %s", e)
            p = self.prior
            p_odds = self.prior_odds
            display_odds = round(p_odds, 4)

        return {
            "prior_probability": self.prior,
            "total_evidence_updates": len(self.updates),
            "posterior_odds": display_odds,
            "posterior_probability": round(p, 6),
            "win_confidence_pct": round(p * 100.0, 2),
            "provenance": "bayesian_epistemic_engine_v1",
            "digest": f"sha256:{hashlib.sha256(str(round(p, 6)).encode()).hexdigest()}",
            "trajectory": [
                {
                    "evidence_id": u.evidence_id,
                    "lr": u.likelihood_ratio,
                    "weight": u.weight,
                    "digest": u.digest,
                }
                for u in self.updates
            ],
        }
