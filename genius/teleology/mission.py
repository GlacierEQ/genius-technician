"""Mission Function Optimizer Engine.

Enforces Section 1.2 Mission Function of AGENTS.md:
  MAXIMUM COHERENT ADVANCE =
    (capability_gained + intelligence_gained + integration_gained + verified_progress + preserved_prior_value)
    - (avoidable_regression + unsupported_claims + unnecessary_friction)
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Dict

logger = logging.getLogger(__name__)


@dataclass
class MissionAdvanceMetrics:
    capability_gained: float = 0.0
    intelligence_gained: float = 0.0
    integration_gained: float = 0.0
    verified_progress: float = 0.0
    preserved_prior_value: float = 0.0
    avoidable_regression: float = 0.0
    unsupported_claims: float = 0.0
    unnecessary_friction: float = 0.0

    def compute_score(self) -> float:
        """Compute Maximum Coherent Advance mathematical score.
        
        # WHY: Quantifying advance ensures execution cycles compound intelligence
        # rather than indulging in process displacement or cosmetic polishing.
        """
        positive = (
            self.capability_gained
            + self.intelligence_gained
            + self.integration_gained
            + self.verified_progress
            + self.preserved_prior_value
        )
        negative = (
            self.avoidable_regression
            + self.unsupported_claims
            + self.unnecessary_friction
        )
        return round(positive - negative, 4)


class MissionOptimizerEngine:
    """Evaluates proposed executions against Maximum Coherent Advance."""

    def evaluate_task(self, task_name: str, metrics: MissionAdvanceMetrics) -> Dict[str, Any]:
        """Evaluate task yield and drag with cryptographic digest.
        
        # WHY: Mathematical gating ensures tasks with zero progress or high friction are rejected early.
        """
        try:
            score = metrics.compute_score()
            positive_yield = round(
                metrics.capability_gained
                + metrics.intelligence_gained
                + metrics.integration_gained
                + metrics.verified_progress
                + metrics.preserved_prior_value,
                4,
            )
            negative_drag = round(
                metrics.avoidable_regression
                + metrics.unsupported_claims
                + metrics.unnecessary_friction,
                4,
            )
            approved = score > 0 and metrics.unsupported_claims == 0.0
            recommendation = "EXECUTE" if score >= 2.0 else ("REVIEW_DRAG" if score > 0 else "ABORT_REGRESSIVE")
        except Exception as e:
            err_msg = str(e)
            logger.error("Mission evaluation error: %s", err_msg)
            score, positive_yield, negative_drag, approved, recommendation = 0.0, 0.0, 1.0, False, "ERROR"

        raw = f"{task_name}:{score}:{approved}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        return {
            "task_name": task_name,
            "maximum_coherent_advance_score": score,
            "positive_yield": positive_yield,
            "negative_drag": negative_drag,
            "approved": approved,
            "recommendation": recommendation,
            "digest": digest_str,
            "provenance": f"mission://task/{task_name}",
        }
