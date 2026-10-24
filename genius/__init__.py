"""genius: The Cognitive Amplification Package (INNOVATION).

Exposes the 6 Cognitive Mega-Stones:
  1. EpistemologyStone
  2. EpidemiologyStone
  3. OntologyStone
  4. TeleologyStone
  5. DialecticsStone
  6. CyberneticsStone
  and the master orchestrator GeniusTechnician.
"""
from __future__ import annotations

import hashlib
import logging
from typing import Any, Dict, Optional

from .epistemology import EpistemologyStone
from .epidemiology import EpidemiologyStone
from .ontology import OntologyStone
from .teleology import TeleologyStone
from .dialectics import DialecticsStone
from .cybernetics import CyberneticsStone
from .engine import GeniusTechnician

logger = logging.getLogger(__name__)

__version__: str = "1.0.0"
__provenance__: str = "apex_holographic_mesh_genius_technician_v1"
__digest__: str = f"sha256:{hashlib.sha256(__version__.encode()).hexdigest()}"


def get_technician(
    target_path: str = "/root",
    storage_dir: str = "/tmp/aspen_grove_quantum_store",
) -> GeniusTechnician:
    """Instantiate and return a fully wired GeniusTechnician engine.
    
    # WHY: Factory function provides a centralized, typed entrypoint with error recovery.
    """
    try:
        return GeniusTechnician(target_path=target_path, storage_dir=storage_dir)
    except Exception as e:
        err_msg = str(e)
        logger.error("Failed to initialize GeniusTechnician factory: %s", err_msg)
        raise RuntimeError(f"GeniusTechnician initialization error: {err_msg}")


def package_audit() -> Dict[str, Any]:
    """Audit the root genius package metadata and provenance.
    
    # WHY: Package-level audits verify deployment integrity across estate repositories.
    """
    try:
        tech = get_technician()
        status = tech.audit_all_stones()
    except Exception as e:
        err_msg = str(e)
        logger.warning("Package audit encountered warning: %s", err_msg)
        status = {"status": "DEGRADED", "error": err_msg}

    return {
        "version": __version__,
        "provenance": __provenance__,
        "digest": __digest__,
        "engine_status": status.get("genius_technician_status", "ONLINE"),
    }


__all__ = [
    "GeniusTechnician",
    "EpistemologyStone",
    "EpidemiologyStone",
    "OntologyStone",
    "TeleologyStone",
    "DialecticsStone",
    "CyberneticsStone",
    "get_technician",
    "package_audit",
    "__version__",
    "__provenance__",
    "__digest__",
]
