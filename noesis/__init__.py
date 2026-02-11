"""
Noesis - Tryambakam Consciousness Architecture Kernel
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A Python package that enables any AI model or agentic framework
to integrate the Tryambakam Noesis consciousness architecture.

Usage:
    noesis init              # Initialize (Sankalpa)
    noesis install           # Full installation (Samskara)
    noesis health            # System health check
    noesis drift             # Detect pattern drift (Vikara)
    noesis context --tier X  # Generate context for tier
    noesis teach FILE        # Teaching mode (Guru)
"""

__version__ = "0.1.0"
__author__ = "Shesh Iyer"
__email__ = "shesh@tryambakam.space"

from noesis.config import Config, load_config

__all__ = [
    "__version__",
    "Config",
    "load_config",
]
