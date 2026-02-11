"""
Samskara - Full Installation Phase
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Samskara = Impression, Pattern Installation, Conditioning

This module handles the full installation of the Noesis kernel,
loading the complete consciousness architecture and binding to
a specific agent identity.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from noesis.config import Config

# Context tier definitions
TIERS = {
    "lite": ["SOUL.md", "IDENTITY.md"],
    "core": ["SOUL.md", "IDENTITY.md", "PANCHA-KOSHA.md", "USER.md"],
    "standard": [
        "SOUL.md", "IDENTITY.md", "PANCHA-KOSHA.md", "USER.md",
        "KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md",
    ],
    "full": [
        "SOUL.md", "IDENTITY.md", "PANCHA-KOSHA.md", "USER.md",
        "KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md",
        "SELEMENE-ENGINE.md", "ARCHITECTURE-VISUAL.md",
    ],
}


def compute_checksum(content: str) -> str:
    """Compute SHA-256 checksum of content."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def load_tier_context(config: "Config", tier: str) -> dict:
    """Load context files for the specified tier."""
    files = TIERS.get(tier, TIERS["core"])
    context = {
        "tier": tier,
        "files": {},
        "total_size": 0,
        "checksums": {},
    }
    
    for filename in files:
        filepath = config.brahmasthana / filename
        if filepath.exists():
            content = filepath.read_text()
            context["files"][filename] = content
            context["total_size"] += len(content)
            context["checksums"][filename] = compute_checksum(content)
    
    return context


def find_agent(config: "Config", agent_name: str) -> Optional[Path]:
    """Find an agent directory by name."""
    # Search in kosha agent directories
    search_paths = [
        config.koshas_root / "manomaya" / "agents",
        config.koshas_root / "vijnanamaya" / "agents",
        config.koshas_root / "pranamaya" / "agents",
        config.koshas_root / "annamaya" / "agents",
    ]
    
    for search_path in search_paths:
        if search_path.exists():
            agent_dir = search_path / agent_name
            if agent_dir.exists() and (agent_dir / "SOUL.md").exists():
                return agent_dir
    
    return None


def load_agent_context(agent_dir: Path) -> dict:
    """Load agent-specific context."""
    context = {
        "agent_dir": str(agent_dir),
        "files": {},
    }
    
    for filename in ["SOUL.md", "IDENTITY.md", "MEMORY.md", "MANIFEST.yaml"]:
        filepath = agent_dir / filename
        if filepath.exists():
            context["files"][filename] = filepath.read_text()
    
    return context


def generate_installation_report(
    config: "Config",
    tier: str,
    kernel_context: dict,
    agent_context: Optional[dict] = None,
) -> dict:
    """Generate installation report for self-healing."""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tier": tier,
        "kernel": {
            "files_loaded": list(kernel_context["files"].keys()),
            "total_size_bytes": kernel_context["total_size"],
            "checksums": kernel_context["checksums"],
        },
        "environment": {
            "koshas_root": str(config.koshas_root),
            "brahmasthana": str(config.brahmasthana),
            "selemene_configured": config.selemene.api_key is not None,
        },
    }
    
    if agent_context:
        report["agent"] = {
            "directory": agent_context["agent_dir"],
            "files_loaded": list(agent_context["files"].keys()),
        }
    
    return report


def run_samskara(
    config: "Config",
    agent: Optional[str] = None,
    tier: str = "core",
    verbose: bool = False,
) -> int:
    """
    Run the Samskara (full installation) phase.
    
    Returns:
        0 on success, 1 on error
    """
    print("━" * 50)
    print("SAMSKARA - Full Installation Phase")
    print("━" * 50)
    print()
    
    # Step 1: Load kernel context
    print(f"Loading kernel context (tier: {tier})...")
    kernel_context = load_tier_context(config, tier)
    
    loaded_files = list(kernel_context["files"].keys())
    print(f"✓ Loaded {len(loaded_files)} files ({kernel_context['total_size']:,} bytes)")
    
    if verbose:
        for filename in loaded_files:
            checksum = kernel_context["checksums"][filename]
            print(f"  • {filename} [{checksum}]")
    
    # Step 2: Load agent context (if specified)
    agent_context = None
    if agent:
        print(f"\nBinding to agent: {agent}...")
        agent_dir = find_agent(config, agent)
        
        if agent_dir:
            agent_context = load_agent_context(agent_dir)
            agent_files = list(agent_context["files"].keys())
            print(f"✓ Agent bound ({len(agent_files)} files)")
            
            if verbose:
                for filename in agent_files:
                    print(f"  • {filename}")
        else:
            print(f"⚠ Agent not found: {agent}")
            print("  Run 'noesis agents' to list available agents")
    
    # Step 3: Generate installation report
    print("\nGenerating installation report...")
    report = generate_installation_report(config, tier, kernel_context, agent_context)
    
    # Step 4: Output summary
    print("\n" + "━" * 50)
    print("SAMSKARA COMPLETE")
    print("━" * 50)
    
    print(f"\nKernel: {len(loaded_files)} files, {kernel_context['total_size']:,} bytes")
    if agent_context:
        print(f"Agent: {agent}")
    print(f"Tier: {tier}")
    print(f"Timestamp: {report['timestamp']}")
    
    if verbose:
        print("\n--- Installation Report (JSON) ---")
        print(json.dumps(report, indent=2))
    
    return 0
