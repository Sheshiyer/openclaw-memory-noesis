"""
Noesis Core Modules
━━━━━━━━━━━━━━━━━━━

Core functionality for the Noesis kernel:
- sankalpa: Initialization
- samskara: Full installation
- vikara: Drift detection
- context: Context generation
- guru: Teaching mode
- health: System health checks
- agents: Agent management
"""

from noesis.core.sankalpa import run_sankalpa
from noesis.core.samskara import run_samskara
from noesis.core.health import run_health_check
from noesis.core.vikara import run_drift_detection
from noesis.core.context import run_context_generation
from noesis.core.guru import run_teaching
from noesis.core.agents import list_agents

__all__ = [
    "run_sankalpa",
    "run_samskara",
    "run_health_check",
    "run_drift_detection",
    "run_context_generation",
    "run_teaching",
    "list_agents",
]
