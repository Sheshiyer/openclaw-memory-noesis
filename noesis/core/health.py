"""
Health - System Health Checks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Validates the integrity and completeness of the Noesis kernel.
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from noesis.config import Config


def check_brahmasthana(config: "Config") -> dict:
    """Check brahmasthana core files."""
    required = ["SOUL.md", "IDENTITY.md", "USER.md", "PANCHA-KOSHA.md"]
    optional = ["KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md", "SELEMENE-ENGINE.md"]
    
    result = {"status": "ok", "required": {}, "optional": {}}
    
    for filename in required:
        filepath = config.brahmasthana / filename
        result["required"][filename] = filepath.exists()
        if not filepath.exists():
            result["status"] = "error"
    
    for filename in optional:
        filepath = config.brahmasthana / filename
        result["optional"][filename] = filepath.exists()
    
    return result


def check_kosha_structure(config: "Config") -> dict:
    """Check kosha directory structure."""
    expected = ["annamaya", "pranamaya", "manomaya", "vijnanamaya", "anandamaya"]
    result = {"status": "ok", "koshas": {}}
    
    for kosha in expected:
        kosha_path = config.koshas_root / kosha
        result["koshas"][kosha] = kosha_path.exists()
        if not kosha_path.exists():
            result["status"] = "warning"
    
    return result


def check_agents(config: "Config") -> dict:
    """Check agent configurations."""
    result = {"status": "ok", "agents": []}
    
    agent_locations = [
        ("manomaya", config.koshas_root / "manomaya" / "agents"),
        ("vijnanamaya", config.koshas_root / "vijnanamaya" / "agents"),
        ("pranamaya", config.koshas_root / "pranamaya" / "agents"),
        ("annamaya", config.koshas_root / "annamaya" / "agents"),
    ]
    
    for kosha, agents_dir in agent_locations:
        if agents_dir.exists():
            for agent_dir in agents_dir.iterdir():
                if agent_dir.is_dir():
                    has_soul = (agent_dir / "SOUL.md").exists()
                    has_identity = (agent_dir / "IDENTITY.md").exists()
                    has_manifest = (agent_dir / "MANIFEST.yaml").exists()
                    
                    agent_info = {
                        "name": agent_dir.name,
                        "kosha": kosha,
                        "has_soul": has_soul,
                        "has_identity": has_identity,
                        "has_manifest": has_manifest,
                        "complete": has_soul and has_identity,
                    }
                    
                    if not agent_info["complete"]:
                        result["status"] = "warning"
                    
                    result["agents"].append(agent_info)
    
    return result


def check_selemene(config: "Config") -> dict:
    """Check Selemene connection (without making API call)."""
    result = {
        "status": "ok",
        "api_key_configured": config.selemene.api_key is not None,
        "base_url": config.selemene.base_url,
    }
    
    if not config.selemene.api_key:
        result["status"] = "warning"
        result["message"] = "API key not configured (set NOESIS_API_KEY)"
    
    return result


def run_health_check(
    config: "Config",
    check: Optional[str] = None,
    json_output: bool = False,
    quick: bool = False,
) -> int:
    """
    Run system health checks.
    
    Returns:
        0 if healthy, 1 if errors, 2 if warnings
    """
    checks = {
        "brahmasthana": check_brahmasthana,
        "structure": check_kosha_structure,
        "agents": check_agents,
        "selemene": check_selemene,
    }
    
    if quick:
        checks = {"brahmasthana": check_brahmasthana}
    
    if check and check in checks:
        checks = {check: checks[check]}
    
    results = {}
    overall_status = "ok"
    
    for name, check_fn in checks.items():
        results[name] = check_fn(config)
        
        if results[name]["status"] == "error":
            overall_status = "error"
        elif results[name]["status"] == "warning" and overall_status != "error":
            overall_status = "warning"
    
    results["overall"] = overall_status
    
    if json_output:
        print(json.dumps(results, indent=2))
    else:
        print("━" * 50)
        print("KOSHA HEALTH CHECK")
        print("━" * 50)
        print()
        
        status_icons = {"ok": "✓", "warning": "⚠", "error": "✗"}
        
        for name, result in results.items():
            if name == "overall":
                continue
            
            icon = status_icons.get(result["status"], "?")
            print(f"{icon} {name}: {result['status'].upper()}")
            
            # Show details for non-ok checks
            if result["status"] != "ok":
                if name == "brahmasthana":
                    missing = [f for f, exists in result["required"].items() if not exists]
                    if missing:
                        print(f"    Missing: {', '.join(missing)}")
                elif name == "agents":
                    incomplete = [a["name"] for a in result.get("agents", []) if not a["complete"]]
                    if incomplete:
                        print(f"    Incomplete: {', '.join(incomplete)}")
                elif name == "selemene" and "message" in result:
                    print(f"    {result['message']}")
        
        print()
        print(f"Overall: {overall_status.upper()}")
    
    return {"ok": 0, "warning": 2, "error": 1}.get(overall_status, 1)
