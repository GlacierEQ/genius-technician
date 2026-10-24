"""Systemic Collapse & Taint Engine.

Implements the legal mechanics of systemic institutional collapse:
  1. Falsus in Uno, Falsus in Omnibus: If testimony or declarations are proven intentionally false on a material element, the entirety is subject to total rejection.
  2. Fruit of the Poisonous Tree: Orders derived from tainted proceedings inherit fatal jurisdictional defect.
  3. Void Ab Initio (Stafford v. Dickison, 48 Haw. 462): A judgment or decree entered without notice and due process is void at its inception and cannot support downstream enforcement.
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TaintCascadeRule:
    rule_id: str
    doctrine_name: str
    trigger_condition: str
    legal_consequence: str
    controlling_precedent: str
    digest: str = ""
    provenance: str = ""


@dataclass
class CollapsibleOrder:
    order_id: str
    docket_ref: str
    issuing_body: str
    date_entered: str
    tainted_by_pathogen: str
    is_void_ab_initio: bool = False
    collapse_lineage: List[str] = field(default_factory=list)
    digest: str = ""
    provenance: str = ""


class SystemicCollapseEngine:
    """Calculates downstream legal voidness and systemic collapse from initial taint."""

    def __init__(self) -> None:
        self.orders: Dict[str, CollapsibleOrder] = {}
        self.rules: List[TaintCascadeRule] = []
        self._seed_doctrines()

    def _seed_doctrines(self) -> None:
        """Seed controlling constitutional and statutory voidness doctrines.
        
        # WHY: Binding explicit appellate precedents (Stafford v. Dickison, State v. Stoddard)
        # provides immutable legal authority that prevents arbitrary judicial dismissals.
        """
        self.rules.append(TaintCascadeRule(
            rule_id="RULE-STAFFORD-VOID",
            doctrine_name="Void Ab Initio for Due Process Starvation",
            trigger_condition="Entry of adverse order without mandatory statutory notice or service",
            legal_consequence="Order has no legal force from moment of entry; all contempt, warrants, or levies predicated thereon are nullities.",
            controlling_precedent="Stafford v. Dickison, 48 Haw. 462, 400 P.2d 249 (1965)",
            digest="sha256:stafford_48_haw_462",
            provenance="precedent://hawaii/stafford_v_dickison",
        ))
        self.rules.append(TaintCascadeRule(
            rule_id="RULE-FALSUS-IN-UNO",
            doctrine_name="Falsus in Uno, Falsus in Omnibus",
            trigger_condition="Material perjury demonstrated by unassailable contemporaneous audio/digital proof",
            legal_consequence="Complete impeachment and disqualification of declarant testimony across all consolidated dockets.",
            controlling_precedent="State v. Stoddard, 105 Hawaiʻi 274, 96 P.3d 603 (2004)",
            digest="sha256:stoddard_105_haw_274",
            provenance="precedent://hawaii/state_v_stoddard",
        ))
        self.rules.append(TaintCascadeRule(
            rule_id="RULE-POISON-FRUIT",
            doctrine_name="Fruit of the Poisonous Tree (Civil Due Process)",
            trigger_condition="Administrative or judicial action founded upon unconstitutional ex parte seizure",
            legal_consequence="Taint transmits to all subsequent agency actions, requiring restitution and vacatur.",
            controlling_precedent="Silverthorne Lumber Co. v. United States, 251 U.S. 385 (1920)",
            digest="sha256:silverthorne_251_us_385",
            provenance="precedent://scotus/silverthorne",
        ))

    def register_order(
        self,
        order_id: str,
        docket_ref: str,
        issuing_body: str,
        date_entered: str,
        tainted_by_pathogen: str,
    ) -> CollapsibleOrder:
        """Register an order subject to systemic voidness analysis.
        
        # WHY: Registering orders with cryptographic provenance establishes
        # the exact genealogical lineage for downstream vacatur.
        """
        raw = f"{order_id}:{docket_ref}:{issuing_body}:{date_entered}".encode("utf-8")
        digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        order = CollapsibleOrder(
            order_id=order_id,
            docket_ref=docket_ref,
            issuing_body=issuing_body,
            date_entered=date_entered,
            tainted_by_pathogen=tainted_by_pathogen,
            digest=digest_str,
            provenance=f"docket://{issuing_body}/{docket_ref}",
        )
        self.orders[order_id] = order
        return order

    def execute_collapse(self, root_taint_pathogen: str) -> Dict[str, Any]:
        """Trigger cascade of voidness across all orders linked to the pathogen.
        
        # WHY: Under Stafford v. Dickison, an order void for lack of notice is void ab initio;
        # this method maps the deterministic legal collapse of all downstream enforcement actions.
        """
        collapsed: List[CollapsibleOrder] = []
        try:
            for order in self.orders.values():
                if order.tainted_by_pathogen == root_taint_pathogen:
                    order.is_void_ab_initio = True
                    order.collapse_lineage.append(f"Triggered by root pathogen: {root_taint_pathogen}")
                    order.collapse_lineage.append("Mandatory vacatur under Stafford v. Dickison")
                    collapsed.append(order)
        except Exception as e:
            err_msg = str(e)
            logger.error("Error executing collapse cascade: %s", err_msg)

        total_orders = len(self.orders)
        collapse_rate = (len(collapsed) / total_orders * 100.0) if total_orders else 0.0
        digest_str = f"sha256:{hashlib.sha256(f'{len(collapsed)}/{total_orders}'.encode()).hexdigest()}"

        return {
            "root_pathogen": root_taint_pathogen,
            "total_orders_audited": total_orders,
            "total_orders_collapsed": len(collapsed),
            "systemic_collapse_rate_pct": round(collapse_rate, 2),
            "digest": digest_str,
            "provenance": "systemic_collapse_engine_v1",
            "collapsed_orders": [
                {
                    "order_id": o.order_id,
                    "docket_ref": o.docket_ref,
                    "issuing_body": o.issuing_body,
                    "is_void": o.is_void_ab_initio,
                    "digest": o.digest,
                    "lineage": o.collapse_lineage,
                }
                for o in collapsed
            ],
        }
