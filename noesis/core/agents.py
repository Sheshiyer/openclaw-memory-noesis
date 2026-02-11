"""
Agents - Agent Management
━━━━━━━━━━━━━━━━━━━━━━━━━

Lists and manages agent configurations across koshas.
"""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from noesis.config import Config


def find_all_agents(config: "Config") -> list[dict]:
    """Find all agents across kosha directories."""
    agents = []
    
    kosha_agents = [
        ("manomaya", "Mind/Memory layer"),
        ("vijnanamaya", "Wisdom/Oversight layer"),
        ("pranamaya", "Energy/Flow layer"),
        ("annamaya", "Physical/Execution layer"),
    ]
    
    for kosha, description in kosha_agents:
        agents_dir = config.koshas_root / kosha / "agents"
        
        if not agents_dir.exists():
            continue
        
        for agent_dir in sorted(agents_dir.iterdir()):
            if not agent_dir.is_dir():
                continue
            
            agent_info = {
                "name": agent_dir.name,
                "kosha": kosha,
                "kosha_description": description,
                "path": str(agent_dir),
                "has_soul": (agent_dir / "SOUL.md").exists(),
                "has_identity": (agent_dir / "IDENTITY.md").exists(),
                "has_manifest": (agent_dir / "MANIFEST.yaml").exists(),
                "has_memory": (agent_dir / "MEMORY.md").exists(),
            }
            
            agent_info["complete"] = agent_info["has_soul"] and agent_info["has_identity"]
            
            agents.append(agent_info)
    
    return agents


def list_agents(config: "Config", verbose: bool = False) -> int:
    """
    List all available agents.
    
    Returns:
        0 on success
    """
    agents = find_all_agents(config)
    
    print("━" * 60)
    print("AVAILABLE AGENTS")
    print("━" * 60)
    print()
    
    if not agents:
        print("No agents found.")
        print()
        print("Agents should be located in:")
        print("  koshas/{kosha}/agents/{agent-name}/")
        return 0
    
    # Group by kosha
    by_kosha: dict[str, list] = {}
    for agent in agents:
        kosha = agent["kosha"]
        if kosha not in by_kosha:
            by_kosha[kosha] = []
        by_kosha[kosha].append(agent)
    
    for kosha, kosha_agents in by_kosha.items():
        description = kosha_agents[0]["kosha_description"] if kosha_agents else ""
        print(f"┌─ {kosha.upper()} ({description})")
        print("│")
        
        for agent in kosha_agents:
            status = "✓" if agent["complete"] else "⚠"
            print(f"│  {status} {agent['name']}")
            
            if verbose:
                parts = []
                if agent["has_soul"]:
                    parts.append("SOUL")
                if agent["has_identity"]:
                    parts.append("IDENTITY")
                if agent["has_manifest"]:
                    parts.append("MANIFEST")
                if agent["has_memory"]:
                    parts.append("MEMORY")
                
                print(f"│      Files: {', '.join(parts)}")
        
        print("│")
    
    print("└" + "─" * 59)
    print()
    print(f"Total: {len(agents)} agents")
    
    incomplete = [a for a in agents if not a["complete"]]
    if incomplete:
        print(f"Incomplete: {len(incomplete)} (missing SOUL.md or IDENTITY.md)")
    
    return 0
