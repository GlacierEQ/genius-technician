"""DiGraph Contagion Modeling Engine.

Simulates transmission of forensic and institutional pathogens across a network graph:
  - Directed edges represent transmission vectors (e.g. fraudulent filings, tainted orders, administrative referrals)
  - Nodes represent institutional actors, court divisions, dockets, and bank accounts
  - Calculates cumulative infection probability and epidemic blast radius
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


@dataclass
class NetworkNode:
    node_id: str
    name: str
    node_type: str  # "COURT", "AGENCY", "ATTORNEY", "FINANCIAL", "EVIDENTIARY"
    infected: bool = False
    active_pathogens: Set[str] = field(default_factory=set)
    taint_score: float = 0.0  # 0.0 (clean) to 1.0 (fully tainted)
    digest: str = ""
    provenance: str = ""


@dataclass
class TransmissionVector:
    vector_id: str
    source_node: str
    target_node: str
    pathogen_id: str
    transmission_prob: float
    vector_name: str
    digest: str = ""
    provenance: str = ""


class ContagionNetworkEngine:
    """Directed graph contagion simulator for forensic epidemiology."""

    def __init__(self) -> None:
        self.nodes: Dict[str, NetworkNode] = {}
        self.vectors: List[TransmissionVector] = []

    def add_node(self, node_id: str, name: str, node_type: str) -> NetworkNode:
        """Add an institutional node to the epidemiological graph.
        
        # WHY: Institutional nodes represent distinct legal boundaries;
        # mapping them individually allows computing discrete transmission blast radiuses.
        """
        raw = f"{node_id}:{name}:{node_type}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        node = NetworkNode(
            node_id=node_id,
            name=name,
            node_type=node_type,
            digest=digest_str,
            provenance=f"contagion://node/{node_id}",
        )
        self.nodes[node_id] = node
        return node

    def add_vector(
        self,
        vector_id: str,
        source_node: str,
        target_node: str,
        pathogen_id: str,
        transmission_prob: float,
        vector_name: str,
    ) -> TransmissionVector:
        """Add a directed transmission vector between nodes.
        
        # WHY: Transmission vectors reflect legal causal conduits such as ex parte filings,
        # administrative cross-referrals, and court minutes.
        """
        if source_node not in self.nodes or target_node not in self.nodes:
            raise KeyError(f"Both nodes ({source_node}, {target_node}) must exist in graph.")
        raw = f"{vector_id}:{source_node}->{target_node}:{pathogen_id}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        vec = TransmissionVector(
            vector_id=vector_id,
            source_node=source_node,
            target_node=target_node,
            pathogen_id=pathogen_id,
            transmission_prob=transmission_prob,
            vector_name=vector_name,
            digest=digest_str,
            provenance=f"contagion://vector/{vector_id}",
        )
        self.vectors.append(vec)
        return vec

    def infect_patient_zero(self, node_id: str, pathogen_id: str, initial_taint: float = 1.0) -> None:
        """Seed patient zero with a primary pathogen.
        
        # WHY: Seeding patient zero models the primary fraudulent filing that starts the systemic contamination.
        """
        node = self.nodes[node_id]
        node.infected = True
        node.active_pathogens.add(pathogen_id)
        node.taint_score = min(1.0, node.taint_score + initial_taint)

    def propagate(self, steps: int = 3) -> Dict[str, Any]:
        """Simulate discrete-step epidemic contagion propagation.
        
        # WHY: Step-wise propagation models the timeline latency between initial fraudulent pleading
        # and downstream administrative agency execution (e.g. CSEA bank levy).
        """
        try:
            for step in range(steps):
                new_infections: List[tuple] = []
                for vec in self.vectors:
                    src = self.nodes[vec.source_node]
                    tgt = self.nodes[vec.target_node]
                    if src.infected and vec.pathogen_id in src.active_pathogens:
                        if not tgt.infected or vec.pathogen_id not in tgt.active_pathogens:
                            new_infections.append((tgt, vec.pathogen_id, vec.transmission_prob))
                for tgt, pathogen_id, prob in new_infections:
                    tgt.infected = True
                    tgt.active_pathogens.add(pathogen_id)
                    tgt.taint_score = min(1.0, tgt.taint_score + prob)
        except Exception as e:
            err_msg = str(e)
            logger.error("Contagion propagation encountered error: %s", err_msg)

        total_nodes = len(self.nodes)
        infected_nodes = sum(1 for n in self.nodes.values() if n.infected)
        avg_taint = sum(n.taint_score for n in self.nodes.values()) / total_nodes if total_nodes > 0 else 0.0
        digest_str = f"sha256:{hashlib.sha256(f'{infected_nodes}/{total_nodes}'.encode()).hexdigest()}"

        return {
            "total_nodes": total_nodes,
            "infected_nodes": infected_nodes,
            "infection_rate_pct": round((infected_nodes / total_nodes * 100.0) if total_nodes > 0 else 0.0, 2),
            "average_network_taint": round(avg_taint, 4),
            "digest": digest_str,
            "provenance": "contagion_network_simulation_v1",
            "node_states": [
                {
                    "node_id": n.node_id,
                    "name": n.name,
                    "type": n.node_type,
                    "infected": n.infected,
                    "pathogens": list(n.active_pathogens),
                    "taint_score": round(n.taint_score, 3),
                    "digest": n.digest,
                }
                for n in self.nodes.values()
            ],
        }
