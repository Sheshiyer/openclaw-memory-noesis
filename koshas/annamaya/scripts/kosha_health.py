#!/usr/bin/env python3
"""
Kosha Health Dashboard
━━━━━━━━━━━━━━━━━━━━━━

System health monitoring for the Tryambakam Noesis architecture.
Checks integrity, structure, connections, and detects drift.

Usage:
    python3 kosha_health.py --report          # Full health report
    python3 kosha_health.py --json            # JSON output
    python3 kosha_health.py --check brahmasthana  # Check specific kosha
    python3 kosha_health.py --quick           # Quick status only
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

KOSHAS_ROOT = Path(__file__).parent.parent.parent  # Up from scripts → annamaya → koshas
BRAHMASTHANA = KOSHAS_ROOT / "brahmasthana"

KOSHA_NAMES = ["anandamaya", "vijnanamaya", "manomaya", "pranamaya", "annamaya"]

# Required files in brahmasthana
CORE_FILES = [
    "SOUL.md", "IDENTITY.md", "USER.md", "PANCHA-KOSHA.md",
    "KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md", "SELEMENE-ENGINE.md"
]

# Required agent files
AGENT_REQUIRED = ["SOUL.md", "IDENTITY.md"]
AGENT_OPTIONAL = ["TOOLS.md", "MEMORY.md", "MANIFEST.yaml"]

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def compute_checksum(filepath: Path) -> str:
    """Compute SHA256 checksum."""
    if not filepath.exists():
        return "MISSING"
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

def file_age_days(filepath: Path) -> int:
    """Return file age in days."""
    if not filepath.exists():
        return -1
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime, tz=timezone.utc)
    return (datetime.now(timezone.utc) - mtime).days

def count_lines(filepath: Path) -> int:
    """Count lines in a file."""
    if not filepath.exists():
        return 0
    return len(filepath.read_text().splitlines())

def status_emoji(status: str) -> str:
    """Return emoji for status."""
    return {"healthy": "✅", "warning": "⚠️", "critical": "❌", "unknown": "❓"}[status]

# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def check_brahmasthana_integrity() -> Dict[str, Any]:
    """Check core kernel files exist and haven't been corrupted."""
    result = {
        "status": "healthy",
        "files": {},
        "issues": [],
        "checksums": {}
    }
    
    for filename in CORE_FILES:
        filepath = BRAHMASTHANA / filename
        if filepath.exists():
            checksum = compute_checksum(filepath)
            size = filepath.stat().st_size
            age = file_age_days(filepath)
            result["files"][filename] = {
                "exists": True,
                "size": size,
                "age_days": age,
                "checksum": checksum
            }
            result["checksums"][filename] = checksum
            
            # Check for stale files
            if age > 30 and filename in ["SOUL.md", "IDENTITY.md"]:
                result["issues"].append(f"{filename} is {age} days old (consider refresh)")
                result["status"] = "warning"
        else:
            result["files"][filename] = {"exists": False}
            result["issues"].append(f"MISSING: {filename}")
            result["status"] = "critical"
    
    return result

def check_kosha_structure() -> Dict[str, Any]:
    """Validate all 5 koshas + brahmasthana directories exist."""
    result = {
        "status": "healthy",
        "koshas": {},
        "issues": []
    }
    
    # Check brahmasthana
    if BRAHMASTHANA.exists():
        result["koshas"]["brahmasthana"] = {"exists": True, "type": "center"}
    else:
        result["koshas"]["brahmasthana"] = {"exists": False}
        result["issues"].append("CRITICAL: brahmasthana missing")
        result["status"] = "critical"
    
    # Check each kosha
    for kosha in KOSHA_NAMES:
        kosha_path = KOSHAS_ROOT / kosha
        if kosha_path.exists():
            file_count = len(list(kosha_path.rglob("*.md")))
            result["koshas"][kosha] = {
                "exists": True,
                "file_count": file_count
            }
        else:
            result["koshas"][kosha] = {"exists": False}
            result["issues"].append(f"MISSING: {kosha} kosha")
            result["status"] = "critical"
    
    return result

def check_agent_bindings() -> Dict[str, Any]:
    """Check all agents have required files."""
    result = {
        "status": "healthy",
        "agents": {},
        "issues": []
    }
    
    # Scan all agent directories
    agent_locations = [
        KOSHAS_ROOT / "vijnanamaya" / "agents",
        KOSHAS_ROOT / "manomaya" / "agents",
        KOSHAS_ROOT / "pranamaya" / "agents",
        KOSHAS_ROOT / "annamaya" / "agents",
    ]
    
    for agent_root in agent_locations:
        if not agent_root.exists():
            continue
        
        for agent_dir in agent_root.iterdir():
            if not agent_dir.is_dir() or agent_dir.name.startswith((".", "_")):
                continue
            
            agent_name = agent_dir.name
            kosha = agent_root.parent.name
            
            agent_info = {
                "kosha": kosha,
                "path": str(agent_dir.relative_to(KOSHAS_ROOT)),
                "has_soul": (agent_dir / "SOUL.md").exists(),
                "has_identity": (agent_dir / "IDENTITY.md").exists(),
                "has_manifest": (agent_dir / "MANIFEST.yaml").exists(),
                "has_memory": (agent_dir / "MEMORY.md").exists(),
            }
            
            result["agents"][agent_name] = agent_info
            
            # Check required files
            if not agent_info["has_soul"]:
                result["issues"].append(f"{agent_name}: MISSING SOUL.md")
                result["status"] = "critical"
            if not agent_info["has_identity"]:
                result["issues"].append(f"{agent_name}: MISSING IDENTITY.md")
                result["status"] = "critical" if result["status"] != "critical" else result["status"]
            if not agent_info["has_manifest"]:
                result["issues"].append(f"{agent_name}: missing MANIFEST.yaml")
                if result["status"] == "healthy":
                    result["status"] = "warning"
    
    return result

def check_selemene_connection() -> Dict[str, Any]:
    """Test Selemene API connectivity."""
    result = {
        "status": "healthy",
        "api_key_set": False,
        "health_response": None,
        "latency_ms": None,
        "issues": []
    }
    
    api_key = os.getenv("NOESIS_API_KEY")
    if api_key and api_key.startswith("nk_"):
        result["api_key_set"] = True
    else:
        result["api_key_set"] = False
        result["issues"].append("NOESIS_API_KEY not configured")
        result["status"] = "warning"
        return result
    
    # Try to connect to Selemene
    try:
        import urllib.request
        import time
        
        url = "https://selemene.tryambakam.space/health/live"
        req = urllib.request.Request(url, headers={"User-Agent": "KoshaHealth/1.0"})
        
        start = time.time()
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            latency = (time.time() - start) * 1000
            
            result["health_response"] = data
            result["latency_ms"] = round(latency, 2)
            
            if data.get("status") != "ok":
                result["issues"].append("Selemene health check returned non-ok status")
                result["status"] = "warning"
    except Exception as e:
        result["issues"].append(f"Selemene connection failed: {str(e)}")
        result["status"] = "critical"
    
    return result

def check_memory_health() -> Dict[str, Any]:
    """Check MEMORY.md files aren't too large or stale."""
    result = {
        "status": "healthy",
        "memories": {},
        "issues": []
    }
    
    # Find all MEMORY.md files
    for memory_file in KOSHAS_ROOT.rglob("MEMORY.md"):
        rel_path = str(memory_file.relative_to(KOSHAS_ROOT))
        lines = count_lines(memory_file)
        age = file_age_days(memory_file)
        
        mem_status = "healthy"
        if lines > 500:
            mem_status = "warning"
            result["issues"].append(f"{rel_path}: {lines} lines (consider pruning)")
        if age > 30:
            if mem_status == "healthy":
                mem_status = "warning"
            result["issues"].append(f"{rel_path}: {age} days old (may be stale)")
        
        result["memories"][rel_path] = {
            "lines": lines,
            "age_days": age,
            "status": mem_status
        }
        
        if mem_status == "warning" and result["status"] == "healthy":
            result["status"] = "warning"
    
    return result

def check_log_health() -> Dict[str, Any]:
    """Check logging system is working."""
    result = {
        "status": "healthy",
        "log_dirs": {},
        "recent_logs": 0,
        "issues": []
    }
    
    log_root = KOSHAS_ROOT / "pranamaya" / "logs"
    
    if not log_root.exists():
        result["issues"].append("Log directory does not exist")
        result["status"] = "warning"
        return result
    
    # Check subdirectories
    for subdir in ["samskara"]:
        subdir_path = log_root / subdir
        if subdir_path.exists():
            files = list(subdir_path.glob("*"))
            result["log_dirs"][subdir] = len(files)
            result["recent_logs"] += len(files)
        else:
            result["log_dirs"][subdir] = 0
    
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN REPORT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def full_health_report() -> Dict[str, Any]:
    """Run all checks and compile full report."""
    checks = {
        "brahmasthana": check_brahmasthana_integrity(),
        "kosha_structure": check_kosha_structure(),
        "agent_bindings": check_agent_bindings(),
        "selemene": check_selemene_connection(),
        "memory": check_memory_health(),
        "logging": check_log_health(),
    }
    
    # Calculate overall status
    statuses = [c["status"] for c in checks.values()]
    if "critical" in statuses:
        overall = "critical"
    elif "warning" in statuses:
        overall = "warning"
    else:
        overall = "healthy"
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall,
        "checks": checks,
        "summary": {
            "total_checks": len(checks),
            "passed": sum(1 for s in statuses if s == "healthy"),
            "warnings": sum(1 for s in statuses if s == "warning"),
            "critical": sum(1 for s in statuses if s == "critical"),
        }
    }

def print_report(report: Dict[str, Any]) -> None:
    """Pretty print the health report."""
    print()
    print("═" * 60)
    print("  🏥 KOSHA HEALTH DASHBOARD")
    print("═" * 60)
    print(f"  Timestamp: {report['timestamp']}")
    print(f"  Overall: {status_emoji(report['overall_status'])} {report['overall_status'].upper()}")
    print("═" * 60)
    print()
    
    # Summary
    s = report["summary"]
    print(f"  📊 Summary: {s['passed']}/{s['total_checks']} passed, "
          f"{s['warnings']} warnings, {s['critical']} critical")
    print()
    
    # Individual checks
    for check_name, check_data in report["checks"].items():
        emoji = status_emoji(check_data["status"])
        print(f"  {emoji} {check_name}: {check_data['status']}")
        
        if check_data.get("issues"):
            for issue in check_data["issues"][:3]:  # Show first 3 issues
                print(f"      → {issue}")
    
    print()
    print("─" * 60)
    
    # Quick stats
    checks = report["checks"]
    if "agent_bindings" in checks:
        agent_count = len(checks["agent_bindings"].get("agents", {}))
        print(f"  🤖 Agents: {agent_count}")
    
    if "kosha_structure" in checks:
        kosha_data = checks["kosha_structure"].get("koshas", {})
        total_files = sum(k.get("file_count", 0) for k in kosha_data.values() if isinstance(k, dict))
        print(f"  📁 Total MD files: {total_files}")
    
    if "selemene" in checks:
        sel = checks["selemene"]
        if sel.get("latency_ms"):
            print(f"  🔮 Selemene latency: {sel['latency_ms']}ms")
    
    print()

def quick_status() -> None:
    """Print quick one-line status."""
    report = full_health_report()
    status = report["overall_status"]
    s = report["summary"]
    emoji = status_emoji(status)
    print(f"{emoji} Kosha Health: {status.upper()} ({s['passed']}/{s['total_checks']} checks passed)")

# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Kosha Health Dashboard - System monitoring for Tryambakam Noesis",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--report", action="store_true", help="Full health report (default)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quick", action="store_true", help="Quick one-line status")
    parser.add_argument("--check", type=str, help="Run specific check (brahmasthana, agents, selemene, etc.)")
    
    args = parser.parse_args()
    
    if args.quick:
        quick_status()
        return
    
    if args.check:
        check_map = {
            "brahmasthana": check_brahmasthana_integrity,
            "structure": check_kosha_structure,
            "agents": check_agent_bindings,
            "selemene": check_selemene_connection,
            "memory": check_memory_health,
            "logging": check_log_health,
        }
        if args.check in check_map:
            result = check_map[args.check]()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n{status_emoji(result['status'])} {args.check}: {result['status']}")
                for issue in result.get("issues", []):
                    print(f"  → {issue}")
        else:
            print(f"Unknown check: {args.check}")
            print(f"Available: {', '.join(check_map.keys())}")
        return
    
    # Default: full report
    report = full_health_report()
    
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)

if __name__ == "__main__":
    main()
