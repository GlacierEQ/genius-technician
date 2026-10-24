"""STONE VI: CYBERNETICS (The Stone of Power, Feedback & Substrate Force).

A deep hierarchical collection of 4 cognitive cybernetic collections:
  1. make -j Heavy Swarm Orchestration Engine (Multi-manager parallel execution & memory fabric)
  2. Substrate Telemetry & Resource Governor Engine (Physics & storage safety)
  3. Auto-Healing & Self-Correcting Control Loop Engine (Resilient circuit breakers)
  4. Hardware & Multi-Protocol Execution Bridges (Device telemetry & RPC)
"""
from __future__ import annotations

import hashlib
import logging
from typing import Any, Dict

from .swarm import (
    HeavySwarmOrchestrator,
    SwarmTask,
    DualLayerMemoryBridge,
    ComprehensiveDisposableWorker,
    RobustStoreManager,
    HolographicVPAgent,
)
from .substrate_governor import SubstrateGovernor, SubstrateHealth
from .feedback import SelfCorrectingFeedbackLoop, CircuitBreakerState
from .bridges import HardwareBridgeEngine, DeviceTelemetrySnapshot

logger = logging.getLogger(__name__)


class CyberneticsStone:
    """The Mega-Cognitive Stone of Execution Power, Substrate Governance, and Self-Healing Feedback."""

    def __init__(self, target_path: str = "/root", max_workers: int = 4) -> None:
        # WHY: Cybernetics is Stone VI because power without substrate feedback leads to host crash or burnout
        self.swarm: HeavySwarmOrchestrator = HeavySwarmOrchestrator(max_workers=max_workers)
        self.memory_bridge: DualLayerMemoryBridge = DualLayerMemoryBridge()
        self.holographic_vp: HolographicVPAgent = HolographicVPAgent(memory_bridge=self.memory_bridge)
        self.governor: SubstrateGovernor = SubstrateGovernor(target_path=target_path)
        self.feedback: SelfCorrectingFeedbackLoop = SelfCorrectingFeedbackLoop()
        self.bridges: HardwareBridgeEngine = HardwareBridgeEngine()

    def audit(self) -> Dict[str, Any]:
        """Audit Cybernetics Stone status with cryptographic digest and provenance.
        
        # WHY: Auditing cybernetics verifies that physical headroom, feedback breakers, and bridges are live.
        """
        try:
            sub_rep = self.governor.audit()
            feed_rep = self.feedback.audit()
            telem_rep = self.bridges.audit()
        except Exception as e:
            err_msg = str(e)
            logger.warning("Error auditing CyberneticsStone: %s", err_msg)
            sub_rep, feed_rep, telem_rep = {}, {}, {}

        raw = f"CYBERNETICS:{sub_rep.get('free_gb', 0)}:{self.swarm.max_workers}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        return {
            "stone": "CYBERNETICS",
            "symbol": "STONE_OF_POWER",
            "digest": digest_str,
            "provenance": "stone://cybernetics/audit",
            "substrate_health": sub_rep,
            "feedback_status": feed_rep,
            "hardware_telemetry": telem_rep,
            "vp_status": self.holographic_vp.get_vp_statistics(),
        }


__all__ = [
    "CyberneticsStone",
    "HeavySwarmOrchestrator",
    "SwarmTask",
    "DualLayerMemoryBridge",
    "ComprehensiveDisposableWorker",
    "RobustStoreManager",
    "HolographicVPAgent",
    "SubstrateGovernor",
    "SubstrateHealth",
    "SelfCorrectingFeedbackLoop",
    "CircuitBreakerState",
    "HardwareBridgeEngine",
    "DeviceTelemetrySnapshot",
]
