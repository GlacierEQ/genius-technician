"""Unit tests for the Genius Technician 6-Mega-Stone Cognitive Suite and Swarm Memory Fabric.

Verifies end-to-end operational rigor across:
  - Stone I: Epistemic Ladder (L0 to L5 provenance)
  - Stone II: Epidemiology Contagion & Structural Collapse
  - Stone III: Quantum Memory (Aspen Grove Pointer Indexing)
  - Stone IV: Teleology High Council & Mission Advance Score
  - Stone V: Dialectics Deduction & Perjury Trapping
  - Stone VI: Cybernetics Substrate Governor, Dual-Layer Memory Bridge & Holographic VP
"""
from __future__ import annotations

import hashlib
import logging
import math
from typing import Any, Dict

import pytest
from genius.engine import GeniusTechnician
from genius.epistemology.ladder import EpistemicLevel
from genius.epidemiology.pathogen import PathogenSeverity
from genius.dialectics.deduction import LogicProposition
from genius.teleology.mission import MissionAdvanceMetrics
from genius.cybernetics.swarm import (
    DualLayerMemoryBridge,
    ComprehensiveDisposableWorker,
    RobustStoreManager,
    HolographicVPAgent,
)

logger = logging.getLogger(__name__)


def test_epistemology_ladder() -> None:
    """Verify Epistemology Stone L0 ground truth and L1 ladder soundness.
    
    # WHY: L0 ground-truth guarantees immutable SHA-256 evidence provenance before inference.
    """
    tech: GeniusTechnician = GeniusTechnician()
    try:
        att0 = tech.epistemology.ladder.attest_l0(b"test_payload", "TEST-EVID", "Test L0 Ground Truth")
        assert att0.level == EpistemicLevel.L0_GROUND_TRUTH
        assert att0.verified is True
        assert "sha256:" in att0.provenance_hash

        att1 = tech.epistemology.ladder.attest_level(
            EpistemicLevel.L1_COMPONENT,
            "Test L1 Component",
            "TEST-EVID",
            supporting_l0_hash=att0.provenance_hash,
        )
        assert att1.level == EpistemicLevel.L1_COMPONENT
        ladder_report = tech.epistemology.ladder.verify_ladder()
        assert ladder_report["is_sound"] is True
        assert ladder_report["total_attestations"] == 2
    except Exception as e:
        err_msg = str(e)
        logger.error("Epistemology test failed: %s", err_msg)
        raise


def test_epidemiology_contagion_and_collapse() -> None:
    """Verify Epidemiology Stone pathogen vector propagation and structural order collapse.
    
    # WHY: Models systematic contamination from fraudulent ex parte filings across institutional nodes.
    """
    tech: GeniusTechnician = GeniusTechnician()
    try:
        c = tech.epidemiology.contagion
        c.add_node("N1", "Source Node", "COURT")
        c.add_node("N2", "Target Node", "AGENCY")
        c.add_vector("V1", "N1", "N2", "PATH-TRO-PREMED", 1.0, "Vector 1")
        c.infect_patient_zero("N1", "PATH-TRO-PREMED")

        spread = c.propagate(steps=2)
        assert spread["infected_nodes"] == 2
        assert spread["infection_rate_pct"] == 100.0

        tech.epidemiology.collapse.register_order("ORD-1", "Dkt. 98", "Family Court", "2024-08-23", "PATH-TRO-PREMED")
        res = tech.epidemiology.collapse.execute_collapse("PATH-TRO-PREMED")
        assert res["total_orders_collapsed"] == 1
        assert res["collapsed_orders"][0]["is_void"] is True
        assert "digest" in res
    except Exception as e:
        err_msg = str(e)
        logger.error("Epidemiology test failed: %s", err_msg)
        raise


def test_ontology_quantum_memory() -> None:
    """Verify Aspen Grove pointer-indexed quantum memory retrieval.
    
    # WHY: Direct pointer dereferencing bypasses expensive recursive scans and protects context budget.
    """
    tech: GeniusTechnician = GeniusTechnician()
    try:
        ptr = tech.ontology.aspen_grove.store("TEST_TYPE", {"test_key": "test_val"})
        assert ptr.id.startswith("ptr_")
        assert ptr.digest != ""
        recalled = tech.ontology.aspen_grove.recall(ptr.id)
        assert recalled["test_key"] == "test_val"
    except Exception as e:
        err_msg = str(e)
        logger.error("Ontology test failed: %s", err_msg)
        raise


def test_teleology_high_council_and_mission() -> None:
    """Verify High Council multi-VP adjudication and Maximum Coherent Advance scoring.
    
    # WHY: Authority-weighted voting resolves tactical dilemmas without compromising to a consensus average.
    """
    tech: GeniusTechnician = GeniusTechnician()
    try:
        directive = tech.teleology.council.deliberate("Should emergency vacatur be sought?")
        assert len(directive.positions) == 3
        assert "Stafford v. Dickison" in directive.effective_directive
        assert directive.digest != ""

        metrics = MissionAdvanceMetrics(
            capability_gained=2.0,
            intelligence_gained=2.0,
            integration_gained=2.0,
            verified_progress=2.0,
            preserved_prior_value=1.0,
        )
        res = tech.teleology.mission.evaluate_task("TEST_TASK", metrics)
        assert res["approved"] is True
        assert res["maximum_coherent_advance_score"] == 9.0
        assert "digest" in res
    except Exception as e:
        err_msg = str(e)
        logger.error("Teleology test failed: %s", err_msg)
        raise


def test_dialectics_deduction_and_adversary() -> None:
    """Verify Formal Deductive fixpoint derivation and contradiction hunting.
    
    # WHY: Proves that void orders without notice fail as a matter of controlling law.
    """
    tech: GeniusTechnician = GeniusTechnician()
    try:
        p1 = LogicProposition("P1", "Notice required", "true")
        p2 = LogicProposition("P2", "Order void without notice", "unknown")
        tech.dialectics.deduction.add_proposition(p1)
        tech.dialectics.deduction.add_proposition(p2)
        tech.dialectics.deduction.add_rule("P1", "P2")
        derivations = tech.dialectics.deduction.derive_fixpoint()
        assert derivations == 1
        assert tech.dialectics.deduction.props["P2"].truth == "true"
    except Exception as e:
        err_msg = str(e)
        logger.error("Dialectics test failed: %s", err_msg)
        raise


def test_cybernetics_substrate_and_feedback() -> None:
    """Verify Substrate Governor physical headroom limits and self-correcting feedback loops.
    
    # WHY: Physical headroom guarantees prevent out-of-memory or out-of-disk crashes on the substrate.
    """
    tech: GeniusTechnician = GeniusTechnician()
    try:
        health = tech.cybernetics.governor.check_health()
        assert health.free_gb > 0.5
        assert health.disk_safe is True
        assert "digest" in tech.cybernetics.governor.audit()

        def safe_op() -> str:
            return "SUCCESS_VALUE"

        val = tech.cybernetics.feedback.execute_resilient("SAFE_OP", safe_op)
        assert val == "SUCCESS_VALUE"
    except Exception as e:
        err_msg = str(e)
        logger.error("Cybernetics test failed: %s", err_msg)
        raise


def test_cybernetics_swarm_memory_fabric_and_vp() -> None:
    """Verify DualLayerMemoryBridge, RobustStoreManager, and HolographicVPAgent.
    
    # WHY: Validates high-intensity worker dispatch, memory bus broadcast, and holographic coordination.
    """
    try:
        bridge: DualLayerMemoryBridge = DualLayerMemoryBridge()
        msg_hash = bridge.broadcast_worker_message("W1", "analyst", "Test message", {"key": "val"})
        assert msg_hash.startswith("sha256:")
        assert len(bridge.worker_bus) == 1

        milestone_hash = bridge.log_project_milestone("Goal 1", "Milestone details")
        assert milestone_hash.startswith("sha256:")
        assert len(bridge.project_memory["completed_milestones"]) == 1

        worker: ComprehensiveDisposableWorker = ComprehensiveDisposableWorker(
            worker_id="test-w1",
            specialty="syntax_lint",
            task="Verify syntax on test module",
            memory_bridge=bridge,
            verification_depth=2,
        )
        res = worker.execute()
        assert res["status"] == "COMPLETED"
        assert res["success_path_verified"] is True
        assert res["digest"].startswith("sha256:")

        mgr: RobustStoreManager = RobustStoreManager("mgr-test", "engineering", bridge)
        batch = mgr.dispatch_worker_swarm("Refactor critical loop", ["syntax_lint"])
        assert len(batch) == 1
        assert batch[0]["status"] == "COMPLETED"
        stats = mgr.get_dispatch_statistics()
        assert stats["total_dispatched"] == 1

        vp: HolographicVPAgent = HolographicVPAgent("VP-HOLO", bridge)
        goal_res = vp.execute_enterprise_goal("Verify system integrity", ["syntax_lint"])
        assert goal_res["status"] == "SUCCESS"
        assert goal_res["digest"].startswith("sha256:")
        vp_stats = vp.get_vp_statistics()
        assert vp_stats["vp_id"] == "VP-HOLO"
    except Exception as e:
        err_msg = str(e)
        logger.error("Swarm memory fabric test failed: %s", err_msg)
        raise


def test_full_cognitive_cascade() -> None:
    """Verify end-to-end cascade across all 6 cognitive stones.
    
    # WHY: Ensures full pipeline execution generates cryptographic audit trail across all cognitive layers.
    """
    tech: GeniusTechnician = GeniusTechnician()
    try:
        res = tech.execute_full_cognitive_cascade("Execute emergency mandate to vacate void ex parte orders")
        assert res["status"] == "COGNITIVE_CASCADE_COMPLETE"
        assert "sha256:" in res["epistemic_l0_hash"]
        assert res["quantum_memory_pointer"].startswith("ptr_")
        assert res["substrate_safe"] is True
    except Exception as e:
        err_msg = str(e)
        logger.error("Cascade test failed: %s", err_msg)
        raise


def test_bayesian_epistemic_stability() -> None:
    """Verify BayesianEpistemicUpdater numerical stability and zero-NaN degradation."""
    tech: GeniusTechnician = GeniusTechnician()
    b = tech.epistemology.bayesian
    assert b.prior == 0.5
    assert b.prior_odds == 1.0

    # Normal evidence accumulation
    b.add_evidence("E-01", "Contemporaneous audio recording", likelihood_ratio=10.0, weight=1.0)
    audit = b.audit()
    assert audit["posterior_probability"] > 0.9
    assert audit["win_confidence_pct"] > 90.0
    assert not math.isnan(audit["posterior_probability"])

    # Massive evidence updates (previously triggered float overflow and NaN degradation)
    for i in range(150):
        b.add_evidence(f"E-BULK-{i}", "Corroborated exhibit", likelihood_ratio=50.0, weight=1.0)

    extreme_audit = b.audit()
    assert extreme_audit["posterior_probability"] == 1.0
    assert extreme_audit["win_confidence_pct"] == 100.0
    assert extreme_audit["posterior_odds"] > 1e100
    assert not math.isnan(extreme_audit["posterior_probability"])
    assert extreme_audit["digest"].startswith("sha256:")

    # Add evidence that pushes log-odds past 700.0 limit
    for i in range(100):
        b.add_evidence(f"E-INFINITE-{i}", "Decisive proof", likelihood_ratio=100.0, weight=1.0)
    inf_audit = b.audit()
    assert inf_audit["posterior_odds"] == float("inf")
    assert inf_audit["posterior_probability"] == 1.0
    assert not math.isnan(inf_audit["posterior_probability"])

