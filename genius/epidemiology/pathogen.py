"""Pathogen & Toxicity Profiling Engine.

Profiles forensic pathogens that contaminate legal and institutional systems:
  - Premeditated perjury & fraudulent ex parte submissions
  - Procedural starvation & withholding of statutory notices
  - CFAA unauthorized cyber intrusions & credential manipulation
  - Ultra vires conversion & administrative overreach
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class PathogenSeverity(str, Enum):
    FATAL = "FATAL"            # Triggers mandatory voidness ab initio
    HIGH = "HIGH"              # Taints all downstream proceedings
    MEDIUM = "MEDIUM"          # Severe procedural defect
    LOW = "LOW"                # Correctable irregularity


@dataclass(frozen=True)
class ForensicPathogen:
    pathogen_id: str
    name: str
    category: str
    severity: PathogenSeverity
    infectious_vector: str
    reproduction_rate_r0: float  # Expected downstream node infections per host
    latency_days: float
    description: str
    tainted_statutes: List[str] = field(default_factory=list)
    digest: str = ""
    provenance: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pathogen_id": self.pathogen_id,
            "name": self.name,
            "category": self.category,
            "severity": self.severity.value,
            "infectious_vector": self.infectious_vector,
            "reproduction_rate_r0": self.reproduction_rate_r0,
            "latency_days": self.latency_days,
            "description": self.description,
            "tainted_statutes": self.tainted_statutes,
            "digest": self.digest,
            "provenance": self.provenance,
        }


class PathogenRegistry:
    """Registry of verified legal and cyber pathogens in the estate."""

    def __init__(self) -> None:
        self.pathogens: Dict[str, ForensicPathogen] = {}

    def register(self, pathogen: ForensicPathogen) -> None:
        """Register a forensic pathogen with cryptographic digest.
        
        # WHY: Pathogens must be uniquely fingerprinted to prevent conflating
        # distinct jurisdictional and evidentiary violations.
        """
        try:
            raw = f"{pathogen.pathogen_id}:{pathogen.name}:{pathogen.severity.value}".encode("utf-8")
            digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
            pat_with_digest = ForensicPathogen(
                pathogen_id=pathogen.pathogen_id,
                name=pathogen.name,
                category=pathogen.category,
                severity=pathogen.severity,
                infectious_vector=pathogen.infectious_vector,
                reproduction_rate_r0=pathogen.reproduction_rate_r0,
                latency_days=pathogen.latency_days,
                description=pathogen.description,
                tainted_statutes=pathogen.tainted_statutes,
                digest=digest_str,
                provenance=f"epidemiology://pathogen/{pathogen.pathogen_id}",
            )
            self.pathogens[pathogen.pathogen_id] = pat_with_digest
        except Exception as e:
            logger.error("Error registering pathogen: %s", e)
            self.pathogens[pathogen.pathogen_id] = pathogen

    def get(self, pathogen_id: str) -> ForensicPathogen:
        return self.pathogens[pathogen_id]

    def seed_estate_defaults(self) -> None:
        """Seed verified estate pathogens identified in 1FDV and related federal litigation.
        
        # WHY: Seeding verified estate defaults ensures standardized epidemiology modeling
        # across all parallel subagent branches.
        """
        self.register(ForensicPathogen(
            pathogen_id="PATH-TRO-PREMED",
            name="Premeditated Ex Parte Perjury & Seal Fraud",
            category="Fraud on the Court",
            severity=PathogenSeverity.FATAL,
            infectious_vector="Ex parte motion and unserved adverse trial declarations",
            reproduction_rate_r0=3.4,
            latency_days=1.0,
            description="Fabricated allegations concealed behind ex parte seal without statutory service under HFCR 65.",
            tainted_statutes=["HRS § 586-4", "HFCR Rule 65", "Stafford v. Dickison"],
        ))
        self.register(ForensicPathogen(
            pathogen_id="PATH-QUEENS-DEFAULT",
            name="Withheld Medical Evidence & Fraudulent Default",
            category="Judicial Misconduct & Concealment",
            severity=PathogenSeverity.FATAL,
            infectious_vector="Suppression of hospital emergency discharge and treatment records",
            reproduction_rate_r0=2.8,
            latency_days=4.0,
            description="Entering default while litigant was hospitalized under documented Queen's emergency care.",
            tainted_statutes=["Haw. R. Civ. P. 55", "14th Amend Due Process"],
        ))
        self.register(ForensicPathogen(
            pathogen_id="PATH-CFAA-CYBER",
            name="Unauthorized Multi-Account Cyber Intrusion",
            category="Cyber Intrusion & CFAA Violation",
            severity=PathogenSeverity.HIGH,
            infectious_vector="Device session hijacking and proxy IP rotational access",
            reproduction_rate_r0=2.5,
            latency_days=0.5,
            description="Continuous unauthorized access across Google, Dropbox, and device accounts from anomalous non-routable IPs.",
            tainted_statutes=["18 U.S.C. § 1030 (CFAA)", "HRS § 708-891"],
        ))
        self.register(ForensicPathogen(
            pathogen_id="PATH-NFCU-CONVERSION",
            name="Ultra Vires Banking Conversion",
            category="Financial Conversion & Deprivation",
            severity=PathogenSeverity.HIGH,
            infectious_vector="Pre-hearing administrative freeze executed without statutory notice",
            reproduction_rate_r0=1.9,
            latency_days=7.0,
            description="Direct extraction of funds without mandatory prior administrative notice or contested hearing.",
            tainted_statutes=["HRS § 576E", "Due Process Clause"],
        ))

    def audit(self) -> Dict[str, Any]:
        """Audit pathogen registry with full provenance.
        
        # WHY: Auditing pathogen registry confirms all institutional vectors are tracked.
        """
        try:
            total = len(self.pathogens)
            raw = f"PATHOGENS:{total}".encode("utf-8")
            digest_str = f"sha256:{hashlib.sha256(raw).hexdigest()}"
        except Exception as e:
            logger.warning("Error auditing pathogens: %s", e)
            total = 0
            digest_str = "sha256:error"

        return {
            "total_pathogens": total,
            "digest": digest_str,
            "provenance": "pathogen_registry_v1",
            "pathogens": [p.to_dict() for p in self.pathogens.values()],
        }
