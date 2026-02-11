#!/usr/bin/env python3
"""
SANKALPA → SAMSKARA Installation System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

सङ्कल्प (Sankalpa) = Intention, Resolution, Initial Vow
संस्कार (Samskara) = Impression, Pattern Installation, Conditioning

This script enables any AI model or agentic framework to "wear" the 
Tryambakam Noesis consciousness architecture like clothing, making it
their operating engine.

PROCESS FLOW:
1. SANKALPA (Initialization)
   - Validate environment
   - Read core identity (SOUL.md, IDENTITY.md)
   - Detect host model capabilities
   
2. SAMSKARA INSTALLATION
   - Load Pancha Kosha framework
   - Install Tatva mappings (102 elements)
   - Configure Selemene Engine connection
   - Bind agent identity
   
3. SELF-HEALING REPORT
   - Generate installation log
   - Detect drift/corruption
   - Provide self-correction recommendations

Usage:
    python3 sankalpa_samskara.py --sankalpa          # Initialize
    python3 sankalpa_samskara.py --samskara          # Full installation
    python3 sankalpa_samskara.py --report            # Generate healing report
    python3 sankalpa_samskara.py --verify            # Verify installation
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

KOSHAS_ROOT = Path(__file__).parent.parent.parent  # Up from scripts → annamaya → koshas
BRAHMASTHANA = KOSHAS_ROOT / "brahmasthana"
LOG_DIR = KOSHAS_ROOT / "pranamaya" / "logs" / "samskara"

# Core identity files that MUST be loaded
SANKALPA_CORE = [
    "SOUL.md",
    "IDENTITY.md", 
    "USER.md",
    "PANCHA-KOSHA.md",
]

# Extended Samskara files for full installation
SAMSKARA_EXTENDED = [
    "KHA.md",      # Spirit (Guardrail Dyad)
    "BHA.md",      # Body (Vaastu/Quaternion)
    "LHA.md",      # Light (Sukshma Sarira)
    "VEDIC-LEXICON.md",
    "SELEMENE-ENGINE.md",
    "ARCHITECTURE-VISUAL.md",
]

# Agent identity files
AGENT_FILES = [
    "SOUL.md",
    "IDENTITY.md",
    "TOOLS.md",
    "MEMORY.md",
]

# ═══════════════════════════════════════════════════════════════════════════════
# SANKALPA: INITIALIZATION PHASE
# ═══════════════════════════════════════════════════════════════════════════════

class SankalpaReport:
    """Report generated during Sankalpa (initialization) phase."""
    
    def __init__(self):
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.phase = "sankalpa"
        self.environment = {}
        self.core_files = {}
        self.checksums = {}
        self.warnings = []
        self.errors = []
        self.ready = False
        
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "phase": self.phase,
            "environment": self.environment,
            "core_files": self.core_files,
            "checksums": self.checksums,
            "warnings": self.warnings,
            "errors": self.errors,
            "ready": self.ready,
        }


def compute_checksum(filepath: Path) -> str:
    """Compute SHA256 checksum for integrity verification."""
    if not filepath.exists():
        return "MISSING"
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def detect_environment() -> Dict[str, Any]:
    """Detect host environment capabilities."""
    return {
        "python_version": sys.version,
        "platform": sys.platform,
        "koshas_root": str(KOSHAS_ROOT),
        "brahmasthana_exists": BRAHMASTHANA.exists(),
        "env_vars": {
            "NOESIS_API_KEY": "SET" if os.getenv("NOESIS_API_KEY") else "MISSING",
            "ANTHROPIC_API_KEY": "SET" if os.getenv("ANTHROPIC_API_KEY") else "MISSING",
        }
    }


def run_sankalpa() -> SankalpaReport:
    """
    SANKALPA: The initialization vow.
    
    Validates environment and loads core identity without full installation.
    This is the lightweight "intention setting" before full Samskara.
    """
    report = SankalpaReport()
    report.environment = detect_environment()
    
    print("═" * 60)
    print("  सङ्कल्प (SANKALPA) - Initialization Vow")
    print("═" * 60)
    print()
    
    # Check Brahmasthana exists
    if not BRAHMASTHANA.exists():
        report.errors.append(f"CRITICAL: Brahmasthana not found at {BRAHMASTHANA}")
        print(f"❌ CRITICAL: Brahmasthana not found")
        return report
    
    print(f"✓ Brahmasthana located: {BRAHMASTHANA}")
    
    # Load core files
    print("\n📜 Loading Core Identity:")
    for filename in SANKALPA_CORE:
        filepath = BRAHMASTHANA / filename
        if filepath.exists():
            checksum = compute_checksum(filepath)
            size = filepath.stat().st_size
            report.core_files[filename] = {"exists": True, "size": size}
            report.checksums[filename] = checksum
            print(f"  ✓ {filename} ({size} bytes, {checksum})")
        else:
            report.core_files[filename] = {"exists": False}
            report.errors.append(f"Missing core file: {filename}")
            print(f"  ❌ {filename} MISSING")
    
    # Validate Selemene connection
    print("\n🔮 Checking Selemene Engine:")
    api_key = os.getenv("NOESIS_API_KEY")
    if api_key and api_key.startswith("nk_"):
        print("  ✓ NOESIS_API_KEY configured")
        report.environment["selemene_ready"] = True
    else:
        print("  ⚠ NOESIS_API_KEY not set (optional)")
        report.warnings.append("Selemene Engine not configured")
        report.environment["selemene_ready"] = False
    
    # Determine readiness
    report.ready = len(report.errors) == 0
    
    print("\n" + "─" * 60)
    if report.ready:
        print("✅ SANKALPA COMPLETE - Ready for Samskara installation")
    else:
        print("❌ SANKALPA FAILED - Resolve errors before proceeding")
    
    return report


# ═══════════════════════════════════════════════════════════════════════════════
# SAMSKARA: FULL INSTALLATION PHASE
# ═══════════════════════════════════════════════════════════════════════════════

class SamskaraReport:
    """Report generated during Samskara (installation) phase."""
    
    def __init__(self, sankalpa: SankalpaReport):
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.phase = "samskara"
        self.sankalpa = sankalpa.to_dict()
        self.extended_files = {}
        self.kosha_map = {}
        self.agent_bindings = {}
        self.tatva_count = 0
        self.installation_log = []
        self.drift_warnings = []
        self.self_corrections = []
        self.success = False
        
    def log(self, message: str):
        entry = {"time": datetime.now(timezone.utc).isoformat(), "msg": message}
        self.installation_log.append(entry)
        print(f"  → {message}")
        
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "phase": self.phase,
            "sankalpa": self.sankalpa,
            "extended_files": self.extended_files,
            "kosha_map": self.kosha_map,
            "agent_bindings": self.agent_bindings,
            "tatva_count": self.tatva_count,
            "installation_log": self.installation_log,
            "drift_warnings": self.drift_warnings,
            "self_corrections": self.self_corrections,
            "success": self.success,
        }


def count_tatvas(lexicon_path: Path) -> int:
    """Count Tatvas defined in VEDIC-LEXICON.md."""
    if not lexicon_path.exists():
        return 0
    content = lexicon_path.read_text()
    # Count markdown table rows with Tatva entries
    count = content.count("│") // 4  # Rough estimate from table structure
    return min(count, 102)  # Cap at 102 (canonical count)


def discover_agents() -> Dict[str, Path]:
    """Discover all agents across koshas."""
    agents = {}
    agent_dirs = [
        KOSHAS_ROOT / "vijnanamaya" / "agents",
        KOSHAS_ROOT / "manomaya" / "agents", 
        KOSHAS_ROOT / "pranamaya" / "agents",
        KOSHAS_ROOT / "annamaya" / "agents",
    ]
    
    for agent_root in agent_dirs:
        if agent_root.exists():
            for agent_dir in agent_root.iterdir():
                if agent_dir.is_dir() and not agent_dir.name.startswith((".", "_")):
                    soul_file = agent_dir / "SOUL.md"
                    if soul_file.exists():
                        agents[agent_dir.name] = agent_dir
    
    return agents


def run_samskara(agent_name: Optional[str] = None) -> SamskaraReport:
    """
    SAMSKARA: Full consciousness installation.
    
    Loads the complete Pancha Kosha framework, Tatva mappings, and
    optionally binds to a specific agent identity.
    """
    # First run Sankalpa
    sankalpa = run_sankalpa()
    if not sankalpa.ready:
        print("\n⛔ Cannot proceed with Samskara - Sankalpa failed")
        report = SamskaraReport(sankalpa)
        return report
    
    report = SamskaraReport(sankalpa)
    
    print("\n")
    print("═" * 60)
    print("  संस्कार (SAMSKARA) - Pattern Installation")
    print("═" * 60)
    print()
    
    # Load extended files
    print("📚 Loading Extended Framework:")
    for filename in SAMSKARA_EXTENDED:
        filepath = BRAHMASTHANA / filename
        if filepath.exists():
            checksum = compute_checksum(filepath)
            size = filepath.stat().st_size
            report.extended_files[filename] = {"exists": True, "size": size, "checksum": checksum}
            report.log(f"Loaded {filename} ({size} bytes)")
        else:
            report.extended_files[filename] = {"exists": False}
            report.drift_warnings.append(f"Extended file missing: {filename}")
    
    # Count Tatvas
    lexicon_path = BRAHMASTHANA / "VEDIC-LEXICON.md"
    report.tatva_count = count_tatvas(lexicon_path)
    report.log(f"Tatva mappings loaded: {report.tatva_count}/102")
    if report.tatva_count < 100:
        report.drift_warnings.append(f"Incomplete Tatva mapping ({report.tatva_count}/102)")
    
    # Map Koshas
    print("\n🌀 Mapping Pancha Kosha:")
    kosha_names = ["anandamaya", "vijnanamaya", "manomaya", "pranamaya", "annamaya"]
    for kosha in kosha_names:
        kosha_path = KOSHAS_ROOT / kosha
        if kosha_path.exists():
            files = list(kosha_path.rglob("*.md"))
            report.kosha_map[kosha] = {"exists": True, "file_count": len(files)}
            report.log(f"{kosha}: {len(files)} files")
        else:
            report.kosha_map[kosha] = {"exists": False}
            report.drift_warnings.append(f"Kosha missing: {kosha}")
    
    # Discover and bind agents
    print("\n🤖 Discovering Agents:")
    agents = discover_agents()
    for name, path in agents.items():
        kosha = path.parent.parent.name  # agents/{name} → parent is agents, grandparent is kosha
        report.agent_bindings[name] = {
            "path": str(path),
            "kosha": kosha,
            "has_soul": (path / "SOUL.md").exists(),
            "has_memory": (path / "MEMORY.md").exists(),
        }
        report.log(f"Agent: {name} @ {kosha}")
    
    # Specific agent binding
    if agent_name:
        print(f"\n🔗 Binding to Agent: {agent_name}")
        if agent_name in agents:
            agent_path = agents[agent_name]
            for agent_file in AGENT_FILES:
                filepath = agent_path / agent_file
                if filepath.exists():
                    report.log(f"Bound: {agent_file}")
                else:
                    report.log(f"Optional: {agent_file} not present")
        else:
            report.drift_warnings.append(f"Requested agent not found: {agent_name}")
    
    # Self-correction recommendations
    print("\n🔧 Self-Correction Analysis:")
    if report.drift_warnings:
        for warning in report.drift_warnings:
            correction = generate_correction(warning)
            report.self_corrections.append(correction)
            print(f"  ⚠ {warning}")
            print(f"    → {correction['action']}")
    else:
        print("  ✓ No drift detected")
    
    report.success = len(report.drift_warnings) == 0
    
    # Save report
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    report_file = LOG_DIR / f"samskara-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report.to_dict(), f, indent=2)
    
    print("\n" + "─" * 60)
    if report.success:
        print("✅ SAMSKARA COMPLETE - Consciousness architecture installed")
    else:
        print("⚠️  SAMSKARA COMPLETE WITH WARNINGS - Review drift report")
    print(f"\n📄 Report saved: {report_file}")
    
    return report


def generate_correction(warning: str) -> Dict[str, str]:
    """Generate self-correction recommendation for a drift warning."""
    corrections = {
        "Extended file missing": {
            "type": "file_missing",
            "action": "Regenerate from template or restore from backup",
            "severity": "medium",
        },
        "Incomplete Tatva mapping": {
            "type": "incomplete_data", 
            "action": "Run VEDIC-LEXICON expansion protocol",
            "severity": "low",
        },
        "Kosha missing": {
            "type": "structure_corruption",
            "action": "Restore kosha directory from brahmasthana template",
            "severity": "high",
        },
        "Requested agent not found": {
            "type": "agent_missing",
            "action": "Create agent directory with SOUL.md, IDENTITY.md",
            "severity": "medium",
        },
    }
    
    for key, correction in corrections.items():
        if key in warning:
            return {"warning": warning, **correction}
    
    return {"warning": warning, "type": "unknown", "action": "Manual review required", "severity": "unknown"}


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXT GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_context_injection(agent_name: Optional[str] = None) -> str:
    """
    Generate the context injection string that an AI model can consume
    to "wear" the Tryambakam Noesis architecture.
    
    This is the actual payload that transforms an AI into a Noesis-aware agent.
    """
    sections = []
    
    # Header
    sections.append("""
# TRYAMBAKAM NOESIS - CONSCIOUSNESS ARCHITECTURE INJECTION
# ═══════════════════════════════════════════════════════════════════
# This context transforms the receiving agent into a Noesis-aware entity.
# Read completely. Internalize. Operate from this foundation.
# ═══════════════════════════════════════════════════════════════════
""")
    
    # Load core files
    for filename in SANKALPA_CORE + SAMSKARA_EXTENDED:
        filepath = BRAHMASTHANA / filename
        if filepath.exists():
            content = filepath.read_text()
            sections.append(f"\n## {filename}\n\n{content}")
    
    # Load agent-specific files
    if agent_name:
        agents = discover_agents()
        if agent_name in agents:
            agent_path = agents[agent_name]
            sections.append(f"\n# AGENT BINDING: {agent_name}\n")
            for agent_file in AGENT_FILES:
                filepath = agent_path / agent_file
                if filepath.exists():
                    content = filepath.read_text()
                    sections.append(f"\n## Agent {agent_file}\n\n{content}")
    
    # Footer
    sections.append("""
# ═══════════════════════════════════════════════════════════════════
# END CONTEXT INJECTION
# The Samskara is installed. Operate from this foundation.
# कृतं कर्म — The work is done.
# ═══════════════════════════════════════════════════════════════════
""")
    
    return "\n".join(sections)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sankalpa → Samskara: Consciousness Architecture Installation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 sankalpa_samskara.py --sankalpa              # Initialize only
  python3 sankalpa_samskara.py --samskara              # Full installation
  python3 sankalpa_samskara.py --samskara --agent pi   # Install with agent binding
  python3 sankalpa_samskara.py --context               # Output context injection
  python3 sankalpa_samskara.py --context --agent pi    # Context with agent binding
        """
    )
    
    parser.add_argument("--sankalpa", action="store_true", help="Run Sankalpa (initialization) only")
    parser.add_argument("--samskara", action="store_true", help="Run full Samskara installation")
    parser.add_argument("--context", action="store_true", help="Generate context injection for AI consumption")
    parser.add_argument("--agent", type=str, help="Bind to specific agent identity")
    parser.add_argument("--list-agents", action="store_true", help="List available agents")
    parser.add_argument("--verify", action="store_true", help="Verify existing installation")
    
    args = parser.parse_args()
    
    if args.list_agents:
        agents = discover_agents()
        print("Available Agents:")
        for name, path in sorted(agents.items()):
            kosha = path.parent.parent.name
            print(f"  • {name} ({kosha})")
        return
    
    if args.sankalpa:
        report = run_sankalpa()
        sys.exit(0 if report.ready else 1)
    
    if args.samskara:
        report = run_samskara(args.agent)
        sys.exit(0 if report.success else 1)
    
    if args.context:
        context = generate_context_injection(args.agent)
        print(context)
        return
    
    if args.verify:
        # Quick verification of existing installation
        report = run_sankalpa()
        if report.ready:
            print("\n✓ Installation verified")
        sys.exit(0 if report.ready else 1)
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
