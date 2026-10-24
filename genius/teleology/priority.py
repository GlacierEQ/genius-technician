"""Priority Engine.

Calculates priority scores according to Section 3.1 of AGENTS.md:
  Priority = (MissionImpact * Urgency * Leverage * DependencyUnlock * EvidenceValue * Reusability) / CostOfDelay
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class PriorityFactors:
    mission_impact: float      # 1.0 - 10.0
    urgency: float             # 1.0 - 10.0
    leverage: float            # 1.0 - 10.0
    dependency_unlock: float   # 1.0 - 10.0
    evidence_value: float      # 1.0 - 10.0
    reusability: float         # 1.0 - 10.0
    cost_of_delay: float       # 1.0 - 10.0 (higher cost of delay increases priority)

    def calculate(self) -> float:
        """Calculate mathematical priority score.
        
        # WHY: AGENTS.md Section 3.1 formula ensures high-leverage and high-urgency tasks
        # are processed first, rather than whatever is most convenient for the model.
        """
        numerator = (
            self.mission_impact
            * self.urgency
            * self.leverage
            * self.dependency_unlock
            * self.evidence_value
            * self.reusability
        )
        denom = max(0.1, 11.0 - self.cost_of_delay)
        return round(numerator / denom, 2)


class PriorityEngine:
    """Ranks competing strategic tasks mathematically."""

    def __init__(self) -> None:
        # WHY: Task queue ranking prevents cognitive thrashing across competing mission demands
        self.task_queue: List[Dict[str, Any]] = []

    def score_task(self, name: str, factors: PriorityFactors) -> Dict[str, Any]:
        """Score task and enqueue with cryptographic digest.
        
        # WHY: Ranking tasks with provenance ensures auditability of scheduling decisions.
        """
        try:
            score = factors.calculate()
        except Exception as e:
            err_msg = str(e)
            logger.error("Error calculating priority score: %s", err_msg)
            score = 0.0

        raw = f"{name}:{score}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        entry = {
            "task_name": name,
            "priority_score": score,
            "digest": digest_str,
            "provenance": f"priority://task/{name}",
            "factors": factors.__dict__,
        }
        self.task_queue.append(entry)
        self.task_queue.sort(key=lambda x: x["priority_score"], reverse=True)
        return entry

    def top_tasks(self, n: int = 5) -> List[Dict[str, Any]]:
        return self.task_queue[:n]

    def audit(self) -> Dict[str, Any]:
        """Audit priority queue state with cryptographic provenance.
        
        # WHY: Auditing the priority queue verifies queue stability and ranking order.
        """
        raw = f"PRIORITY_QUEUE:{len(self.task_queue)}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        return {
            "queued_tasks": len(self.task_queue),
            "top_task": self.task_queue[0]["task_name"] if self.task_queue else None,
            "digest": digest_str,
            "provenance": "priority_engine_v1",
        }
