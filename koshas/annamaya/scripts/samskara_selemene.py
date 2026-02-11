"""
Selemene Engine Bindings for Samskara
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Auto-connects agents to their relevant Selemene engines
and fetches personalized data during Samskara installation.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Agent → Engine bindings
AGENT_ENGINE_BINDINGS = {
    "chitta-weaver": {
        "engines": ["vimshottari", "numerology"],
        "purpose": "Memory consolidation needs temporal context (dasha) and numeric patterns",
    },
    "kosha-regulator": {
        "engines": ["biorhythm", "biofield"],
        "purpose": "System oversight needs energy cycle and field coherence data",
    },
    "nadi-mapper": {
        "engines": ["human-design", "gene-keys"],
        "purpose": "Pathway discovery needs design type and transformation sequences",
    },
    "noesis-vishwakarma": {
        "engines": ["vedic-clock", "panchanga"],
        "purpose": "Build timing needs auspicious moments and daily rhythms",
    },
}

# Shesh's birth data (from USER.md)
SHESH_BIRTH_DATA = {
    "name": "Shesh Iyer",
    "date": "1991-08-13",
    "time": "13:31",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "timezone": "Asia/Kolkata",
}

def get_agent_engines(agent_id: str) -> List[str]:
    """Get list of Selemene engines for an agent."""
    binding = AGENT_ENGINE_BINDINGS.get(agent_id, {})
    return binding.get("engines", [])

def fetch_engine_data(engine_id: str, birth_data: Dict = None) -> Dict:
    """Fetch data from a Selemene engine."""
    import urllib.request
    
    api_key = os.getenv("NOESIS_API_KEY")
    if not api_key:
        return {"error": "NOESIS_API_KEY not set"}
    
    birth_data = birth_data or SHESH_BIRTH_DATA
    
    url = f"https://selemene.tryambakam.space/api/v1/engines/{engine_id}/calculate"
    
    payload = json.dumps({
        "birth_data": birth_data,
        "precision": "Standard",
    }).encode()
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "SamskaraSelemene/1.0",
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": str(e)}

def fetch_agent_context(agent_id: str) -> Dict[str, Any]:
    """Fetch all Selemene engine data for an agent."""
    engines = get_agent_engines(agent_id)
    results = {
        "agent_id": agent_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engines": {},
        "summary": "",
    }
    
    for engine in engines:
        data = fetch_engine_data(engine)
        results["engines"][engine] = data
    
    # Generate summary based on fetched data
    results["summary"] = generate_context_summary(agent_id, results["engines"])
    
    return results

def generate_context_summary(agent_id: str, engine_data: Dict) -> str:
    """Generate a human-readable summary for context injection."""
    lines = [f"## Selemene Context for {agent_id}", ""]
    
    for engine, data in engine_data.items():
        if "error" in data:
            lines.append(f"- {engine}: Error - {data['error']}")
            continue
            
        result = data.get("result", {})
        
        if engine == "vimshottari":
            current = result.get("current_period", {})
            maha = current.get("maha_dasha", {})
            lines.append(f"- **Current Dasha:** {maha.get('planet', 'Unknown')} Mahadasha")
            
        elif engine == "numerology":
            life_path = result.get("life_path", {})
            lines.append(f"- **Life Path:** {life_path.get('value', '?')} - {life_path.get('meaning', '')}")
            
        elif engine == "biorhythm":
            lines.append(f"- **Physical:** {result.get('physical', {}).get('value', 0)}%")
            lines.append(f"- **Emotional:** {result.get('emotional', {}).get('value', 0)}%")
            
        elif engine == "vedic-clock":
            lines.append(f"- **Current Organ:** {result.get('organ', 'Unknown')}")
            lines.append(f"- **Dosha:** {result.get('dosha', 'Unknown')}")
            
        elif engine == "panchanga":
            lines.append(f"- **Tithi:** {result.get('tithi', {}).get('name', 'Unknown')}")
            lines.append(f"- **Nakshatra:** {result.get('nakshatra', {}).get('name', 'Unknown')}")
            
        elif engine == "human-design":
            lines.append(f"- **Type:** {result.get('type', 'Unknown')}")
            lines.append(f"- **Authority:** {result.get('authority', 'Unknown')}")
            
        elif engine == "gene-keys":
            activations = result.get("activations", [])
            if activations:
                first = activations[0]
                lines.append(f"- **Life's Work:** Gate {first.get('gate', '?')}")
    
    lines.append("")
    return "\n".join(lines)

def inject_selemene_context(base_context: str, agent_id: str, fetch: bool = True) -> str:
    """Inject Selemene engine data into context string."""
    if not fetch:
        return base_context
    
    selemene_data = fetch_agent_context(agent_id)
    injection = f"\n\n# SELEMENE LIVE DATA\n{selemene_data['summary']}\n"
    
    return base_context + injection

# CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=str, help="Agent ID to fetch context for")
    parser.add_argument("--engine", type=str, help="Specific engine to query")
    parser.add_argument("--list", action="store_true", help="List all agent bindings")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if args.list:
        for agent, binding in AGENT_ENGINE_BINDINGS.items():
            print(f"{agent}: {', '.join(binding['engines'])}")
            print(f"  Purpose: {binding['purpose']}")
            print()
    elif args.agent:
        data = fetch_agent_context(args.agent)
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(data["summary"])
    elif args.engine:
        data = fetch_engine_data(args.engine)
        print(json.dumps(data, indent=2))
