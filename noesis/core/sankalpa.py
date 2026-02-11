"""
Sankalpa - Initialization Phase
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sankalpa = Intention, Resolution, Initial Vow

This module handles the initialization phase of the Noesis kernel,
validating the environment and loading core identity files.
"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from noesis.config import Config


def validate_environment(config: "Config") -> list[str]:
    """Validate that required files and directories exist."""
    errors = []
    
    # Check koshas root
    if not config.koshas_root.exists():
        errors.append(f"Koshas root not found: {config.koshas_root}")
    
    # Check brahmasthana
    if not config.brahmasthana.exists():
        errors.append(f"Brahmasthana not found: {config.brahmasthana}")
    
    # Check core identity files
    core_files = ["SOUL.md", "IDENTITY.md", "USER.md"]
    for filename in core_files:
        filepath = config.brahmasthana / filename
        if not filepath.exists():
            errors.append(f"Core file missing: {filename}")
    
    return errors


def load_core_identity(config: "Config") -> dict:
    """Load core identity files (SOUL.md, IDENTITY.md)."""
    identity = {}
    
    soul_path = config.brahmasthana / "SOUL.md"
    if soul_path.exists():
        identity["soul"] = soul_path.read_text()
        identity["soul_path"] = str(soul_path)
    
    identity_path = config.brahmasthana / "IDENTITY.md"
    if identity_path.exists():
        identity["identity"] = identity_path.read_text()
        identity["identity_path"] = str(identity_path)
    
    return identity


def run_sankalpa(config: "Config", verbose: bool = False) -> int:
    """
    Run the Sankalpa (initialization) phase.
    
    Returns:
        0 on success, 1 on error
    """
    print("━" * 50)
    print("SANKALPA - Initialization Phase")
    print("━" * 50)
    print()
    
    # Step 1: Validate environment
    if verbose:
        print(f"Koshas root: {config.koshas_root}")
        print(f"Brahmasthana: {config.brahmasthana}")
        print()
    
    print("Validating environment...")
    errors = validate_environment(config)
    
    if errors:
        print("\n❌ Validation failed:")
        for error in errors:
            print(f"  • {error}")
        return 1
    
    print("✓ Environment validated")
    
    # Step 2: Load core identity
    print("\nLoading core identity...")
    identity = load_core_identity(config)
    
    if "soul" in identity:
        # Extract first meaningful line from SOUL.md
        lines = identity["soul"].strip().split("\n")
        title = next((l for l in lines if l.startswith("# ")), "SOUL.md loaded")
        print(f"✓ {title}")
    
    if "identity" in identity:
        print("✓ IDENTITY.md loaded")
    
    # Step 3: Check Selemene connection (optional)
    if config.selemene.api_key:
        print("\n✓ Selemene API key configured")
    else:
        print("\n⚠ Selemene API key not set (set NOESIS_API_KEY)")
    
    print("\n" + "━" * 50)
    print("SANKALPA COMPLETE")
    print("━" * 50)
    print("\nRun 'noesis install' for full Samskara installation")
    
    return 0
