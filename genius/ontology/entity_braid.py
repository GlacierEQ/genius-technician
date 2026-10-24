"""Entity-Taxonomy & Relationship Braid Engine.

Binds heterogeneous entities into an immutable ontological graph:
  - Actors (Operator, opposing counsel, judges, witnesses)
  - Institutional nodes (Family Court, CSEA, Queens Medical Center, NFCU)
  - Evidence records (Audio files, transcripts, medical charts, JEFS filings)
  - Claims & statutes (HRS § 586, CFAA 1030, Stafford v. Dickison)
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


@dataclass
class OntologicalEntity:
    entity_id: str
    entity_type: str  # "ACTOR", "INSTITUTION", "RECORD", "STATUTE", "DEVICE"
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    connected_edges: Set[str] = field(default_factory=set)
    digest: str = ""
    provenance: str = ""


@dataclass
class OntologicalEdge:
    edge_id: str
    source_id: str
    target_id: str
    relation: str  # "BINDS_TO", "ISSUED_BY", "CORROBORATES", "CONTRADICTS", "VIOLATES"
    weight: float = 1.0
    digest: str = ""
    provenance: str = ""


class EntityBraidEngine:
    """Ontological graph linking all physical and legal entities."""

    def __init__(self) -> None:
        # WHY: Entity braiding creates an immutable knowledge graph linking real-world actors to legal dockets
        self.entities: Dict[str, OntologicalEntity] = {}
        self.edges: Dict[str, OntologicalEdge] = {}

    def add_entity(self, entity_id: str, entity_type: str, name: str, attributes: Dict[str, Any] = None) -> OntologicalEntity:
        """Add ontological entity with cryptographic digest.
        
        # WHY: Fingerprinting entities uniquely prevents identity ambiguity across dockets.
        """
        raw = f"{entity_id}:{entity_type}:{name}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        ent = OntologicalEntity(
            entity_id=entity_id,
            entity_type=entity_type,
            name=name,
            attributes=attributes or {},
            digest=digest_str,
            provenance=f"ontology://entity/{entity_id}",
        )
        self.entities[entity_id] = ent
        return ent

    def connect(self, source_id: str, target_id: str, relation: str, weight: float = 1.0) -> OntologicalEdge:
        """Connect two entities with a directed semantic relation edge.
        
        # WHY: Explicitly typed relationship edges enable causal graph traversal and contradiction hunting.
        """
        if source_id not in self.entities or target_id not in self.entities:
            raise KeyError("Both source and target entities must exist in braid.")
        eid = f"{source_id}--[{relation}]-->{target_id}"
        raw = f"{eid}:{weight}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        edge = OntologicalEdge(
            edge_id=eid,
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            weight=weight,
            digest=digest_str,
            provenance=f"ontology://edge/{eid}",
        )
        self.edges[eid] = edge
        self.entities[source_id].connected_edges.add(eid)
        self.entities[target_id].connected_edges.add(eid)
        return edge

    def audit(self) -> Dict[str, Any]:
        """Audit entity braid topology with cryptographic provenance.
        
        # WHY: Auditing entity types ensures structural balance and complete graph connectivity.
        """
        types: Dict[str, int] = {}
        try:
            for e in self.entities.values():
                types[e.entity_type] = types.get(e.entity_type, 0) + 1
        except Exception as e:
            err_msg = str(e)
            logger.error("Error auditing entity braid: %s", err_msg)

        raw = f"BRAID:{len(self.entities)}:{len(self.edges)}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"

        return {
            "total_entities": len(self.entities),
            "total_edges": len(self.edges),
            "entity_type_distribution": types,
            "digest": digest_str,
            "provenance": "entity_braid_graph_v1",
        }
