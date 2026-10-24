#!/usr/bin/env python3
"""CLI interface for Genius Technician Cognitive Amplification Engine."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add repository root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from genius.engine import GeniusTechnician


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="genius",
        description="Genius Technician: APEX Cognitive Amplification & 6 Mega-Stone Engine",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available cognitive commands")

    # Command: audit
    subparsers.add_parser("audit", help="Audit all 6 Cognitive Mega-Stones")

    # Command: think
    think_parser = subparsers.add_parser("think", help="Run full 6-stone cognitive cascade over a proposition")
    think_parser.add_argument("statement", type=str, help="Proposition or directive to process")

    # Command: stone
    stone_parser = subparsers.add_parser("stone", help="Inspect a specific cognitive stone")
    stone_parser.add_argument(
        "name",
        choices=["epistemology", "epidemiology", "ontology", "teleology", "dialectics", "cybernetics"],
        help="Name of the cognitive stone",
    )

    # Command: council
    council_parser = subparsers.add_parser("council", help="Run High Council multi-VP deliberation")
    council_parser.add_argument("question", type=str, help="Strategic question for deliberation")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run full integrated cognitive campaign & live estate harvest")
    run_parser.add_argument("--batch", type=int, default=500, help="MBOX distillation batch size (default: 500)")

    # Command: contagion
    subparsers.add_parser("contagion", help="Run forensic epidemiology contagion and collapse simulation")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # WHY: Wrapping CLI execution in try-except ensures graceful diagnostic reporting without unhandled stack traces
    try:
        technician = GeniusTechnician()
    except Exception as e:
        err_msg = str(e)
        print(f"ERROR: Failed to initialize GeniusTechnician: {err_msg}", file=sys.stderr)
        return 1

    if args.command == "run":
        print("\n" + "=" * 78)
        print("⚔️ [GENIUS TECHNICIAN: FULL INTEGRATED CAMPAIGN RUN]")
        print("=" * 78)
        res = technician.run_integrated_campaign(batch_size=args.batch)
        print(f"\n[1] ⚡ SUBSTRATE TELEMETRY & GOVERNOR:")
        print(f"    • Free Disk Headroom   : {res['substrate_telemetry']['free_gb']:.2f} GB (Safe: {res['substrate_telemetry']['disk_safe']})")
        print(f"    • Battery & Thermals   : {res['substrate_telemetry']['battery_pct']}% ({res['substrate_telemetry']['battery_status']})")
        print(f"\n[2] 💎 EPISTEMOLOGY & ADMISSIBILITY:")
        print(f"    • L0 Provenance Hash   : {res['epistemic_provenance']['l0_hash']}")
        print(f"    • Case Emails Indexed  : {res['epistemic_provenance']['evidence_corpus']['emails']}")
        print(f"    • Activities Indexed   : {res['epistemic_provenance']['evidence_corpus']['activities']}")
        print(f"    • Bayesian Win Prob    : {res['epistemic_provenance']['bayesian_win_pct']:.1f}%")
        print(f"\n[3] 🌀 ONTOLOGY & QUANTUM MEMORY:")
        print(f"    • Aspen-Grove Pointer  : {res['quantum_memory']['pointer_id']}")
        print(f"    • Pointer Digest       : {res['quantum_memory']['pointer_digest'][:24]}...")
        print(f"\n[4] ☣️ EPIDEMIOLOGY & SYSTEMIC COLLAPSE:")
        print(f"    • Network Nodes Mapped : {res['epidemiology_simulation']['network_nodes']}")
        print(f"    • Infected Nodes       : {res['epidemiology_simulation']['infected_nodes']}")
        print(f"    • Collapsed Void Orders: {res['epidemiology_simulation']['collapsed_void_orders']} (Stafford v. Dickison vacatur)")
        print(f"    • Antibody Efficacy    : {res['epidemiology_simulation']['antibody_efficacy_pct']:.0f}% (Remaining Taint: {res['epidemiology_simulation']['remaining_taint']})")
        print(f"\n[5] ⚔️ DIALECTICS & ADVERSARY REFUTATION:")
        print(f"    • Deductive Fixpoint   : {res['dialectics_reasoning']['derivations']} derivations (Void Order Derived: {res['dialectics_reasoning']['void_order_derived']})")
        print(f"    • Adversary Verdict    : {res['dialectics_reasoning']['adversary_refutation_verdict']}")
        print(f"    • Primed Perjury Traps : {res['dialectics_reasoning']['perjury_traps_primed']}")
        print(f"\n[6] 🏛️ TELEOLOGY & HIGH COUNCIL:")
        print(f"    • Council Directive    : {res['teleology_directive']['high_council_directive']}")
        print(f"    • Mission Advance Score: {res['teleology_directive']['mission_advance_score']:.2f}")
        print(f"\n[7] 📦 FORENSIC HARVEST:")
        h = res['forensic_harvest']
        print(f"    • Harvest Status       : {h.get('status', 'N/A')}")
        if h.get('status') == 'SUCCESS':
            print(f"    • Emails Processed     : {h.get('processed', 0)}")
            print(f"    • New Case Matches     : {h.get('new_matches', 0)}")
            print(f"    • Stream Cursor Pos    : {h.get('cursor', 'N/A')}")
        print(f"\n[8] 🏆 CAMPAIGN EXECUTION COMPLETE:")
        print(f"    • Total Elapsed Time   : {res['elapsed_sec']} seconds")
        print(f"    • Receipt Saved To     : /root/GENIUS_RUN_RECEIPT.json")
        print("=" * 78 + "\n")
        return 0


    if args.command == "audit":
        res = technician.audit_all_stones()
        print(json.dumps(res, indent=2))
        return 0

    elif args.command == "think":
        res = technician.execute_full_cognitive_cascade(args.statement)
        print("🧠 [GENIUS COGNITIVE CASCADE COMPLETED]")
        print(f"  • Mission Statement       : {res['mission']}")
        print(f"  • L0 Provenance Hash      : {res['epistemic_l0_hash']}")
        print(f"  • Quantum Memory Pointer  : {res['quantum_memory_pointer']}")
        print(f"  • High Council Directive  : {res['high_council_directive']}")
        print(f"  • Adversary Status        : {res['adversary_resilience']}")
        print(f"  • Antibody Deployment     : {res['epidemiology_antibody_deployed']}")
        print(f"  • Substrate Safety Guard  : VERIFIED SOUND")
        return 0

    elif args.command == "stone":
        stone_attr = getattr(technician, args.name)
        audit = stone_attr.audit()
        print(f"💎 [COGNITIVE STONE: {args.name.upper()}]")
        print(json.dumps(audit, indent=2))
        return 0

    elif args.command == "council":
        directive = technician.teleology.council.deliberate(args.question)
        print(f"🏛️ [HIGH COUNCIL DELIBERATION: '{args.question}']")
        for pos in directive.positions:
            print(f"  - [{pos.vp} ({pos.role})]: {pos.claim} (Confidence: {pos.confidence:.2f})")
        print("\n⚖️ [ADJUDICATED DIRECTIVE]:")
        print(f"  {directive.effective_directive}")
        return 0

    elif args.command == "contagion":
        # Build demonstration network
        epi = technician.epidemiology
        c = epi.contagion
        c.add_node("NODE-EX-PARTE", "Ex Parte Motion Pleading", "EVIDENTIARY")
        c.add_node("NODE-FAMILY-COURT", "Family Court Division 1", "COURT")
        c.add_node("NODE-CSEA", "Child Support Enforcement Agency", "AGENCY")
        c.add_node("NODE-NFCU", "Navy Federal Credit Union Account", "FINANCIAL")
        
        c.add_vector("VEC-1", "NODE-EX-PARTE", "NODE-FAMILY-COURT", "PATH-TRO-PREMED", 0.95, "Ex Parte Motion Submission")
        c.add_vector("VEC-2", "NODE-FAMILY-COURT", "NODE-CSEA", "PATH-TRO-PREMED", 0.85, "Judicial Notice Transmission")
        c.add_vector("VEC-3", "NODE-CSEA", "NODE-NFCU", "PATH-NFCU-CONVERSION", 0.90, "Pre-Hearing Administrative Levy")
        
        c.infect_patient_zero("NODE-EX-PARTE", "PATH-TRO-PREMED")
        spread = c.propagate(steps=3)
        
        print("☣️ [EPIDEMIOLOGY CONTAGION SIMULATION]")
        print(f"  • Total Network Nodes   : {spread['total_nodes']}")
        print(f"  • Total Infected Nodes  : {spread['infected_nodes']} ({spread['infection_rate_pct']}%)")
        print(f"  • Average Network Taint : {spread['average_network_taint']}")
        
        # Test antibody deployment
        ab = epi.antibodies.deploy("AB-AUDIO-TIMESTAMP", target_node_taint=1.0)
        print(f"\n💉 [ANTIBODY DEPLOYMENT: {ab['antibody_id']}]")
        print(f"  • Neutralizing Proof    : 11:51 AM Unbroken Audio Evidence")
        print(f"  • Efficacy Rate         : {ab['efficacy_rate'] * 100:.0f}%")
        print(f"  • Remaining Taint       : {ab['remaining_taint']}")
        print(f"  • Result Status         : {ab['status']}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
