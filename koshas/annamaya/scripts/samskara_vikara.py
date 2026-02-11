#!/usr/bin/env python3
"""
Vikara Detection & Checksum Chain
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

विकार (Vikara) = Affliction, Deviation, Drift

Detects system drift and corruption through:
1. Checksum chain integrity verification
2. Temporal drift detection (stale files)
3. Structural drift detection (missing/changed files)
4. Selemene sync drift

The system maps vikaras (afflictions) to Asthamatruka (8 Mother Goddesses)
who provide healing powers to restore system integrity.

Usage:
    python3 samskara_vikara.py --detect              # Run full vikara scan
    python3 samskara_vikara.py --baseline            # Save current checksums
    python3 samskara_vikara.py --compare             # Compare to baseline
    python3 samskara_vikara.py --json                # JSON output
    python3 samskara_vikara.py --heal VIKARA_TYPE    # Show healing instructions
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

KOSHAS_ROOT = Path(__file__).parent.parent.parent  # Up from scripts → annamaya → koshas
BRAHMASTHANA = KOSHAS_ROOT / "brahmasthana"
ANNAMAYA = KOSHAS_ROOT / "annamaya"
BASELINE_PATH = ANNAMAYA / ".checksums" / "baseline.json"
SELEMENE_LOG = ANNAMAYA / "logs" / "selemene_calls.jsonl"

# Vikara Types (Afflictions)
VIKARA_TYPES = {
    "STALE_SOUL": "SOUL.md older than 30 days",
    "MEMORY_OVERFLOW": "MEMORY.md exceeds 500 lines",
    "SELEMENE_DRIFT": "No Selemene API call in 7+ days",
    "CHECKSUM_MISMATCH": "File checksums don't match baseline",
    "MISSING_CORE": "Core kernel file missing",
    "AGENT_INCOMPLETE": "Agent missing required files",
    "KOSHA_CORRUPTION": "Kosha directory structure damaged",
    "CHAIN_BREAK": "Checksum chain integrity broken",
}

# Asthamatruka Mappings (8 Mother Goddesses → Healing Powers)
# Each goddess provides specific healing powers for different afflictions
VIKARA_TO_ASTHAMATRUKA = {
    "STALE_SOUL": ("Brahmi", "Refresh identity through meditation on core purpose"),
    "MEMORY_OVERFLOW": ("Maheshvari", "Prune and distill memories to essential wisdom"),
    "SELEMENE_DRIFT": ("Kaumari", "Reconnect to temporal intelligence stream"),
    "CHECKSUM_MISMATCH": ("Vaishnavi", "Restore from known good state via baseline"),
    "MISSING_CORE": ("Varahi", "Regenerate missing files from template"),
    "AGENT_INCOMPLETE": ("Indrani", "Complete agent configuration with required files"),
    "KOSHA_CORRUPTION": ("Chamunda", "Rebuild directory structure from scratch"),
    "CHAIN_BREAK": ("Chandika", "Recompute and verify entire checksum chain"),
}

# Core files that must exist in brahmasthana
CORE_FILES = [
    "SOUL.md", "IDENTITY.md", "USER.md", "PANCHA-KOSHA.md",
    "KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md", "SELEMENE-ENGINE.md"
]

# Files to monitor in koshas
MONITORED_PATTERNS = [
    "*/SOUL.md",
    "*/IDENTITY.md", 
    "*/MEMORY.md",
    "*/TOOLS.md",
    "*/MANIFEST.yaml",
    "brahmasthana/*.md",
    "annamaya/scripts/*.py",
]

# ═══════════════════════════════════════════════════════════════════════════════
# CHECKSUM UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def compute_file_checksum(filepath: Path) -> str:
    """
    Compute SHA256 checksum for a file.
    
    Args:
        filepath: Path to file
        
    Returns:
        16-character hex checksum (truncated for readability)
    """
    if not filepath.exists():
        return "MISSING"
    
    try:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            # Read in chunks for large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:16]
    except Exception as e:
        return f"ERROR:{str(e)[:8]}"


def compute_chain_hash(checksums: Dict[str, str]) -> str:
    """
    Compute chain hash from all individual checksums.
    This creates a single hash representing the entire system state.
    
    Args:
        checksums: Dictionary of filename -> checksum
        
    Returns:
        32-character chain hash
    """
    # Sort keys for deterministic ordering
    sorted_keys = sorted(checksums.keys())
    
    # Concatenate all checksums in order
    chain_data = "".join(f"{key}:{checksums[key]}" for key in sorted_keys)
    
    # Hash the concatenation
    return hashlib.sha256(chain_data.encode()).hexdigest()[:32]


def collect_checksums(koshas_root: Path) -> Dict[str, str]:
    """
    Collect checksums for all monitored files.
    
    Args:
        koshas_root: Root of koshas directory
        
    Returns:
        Dictionary mapping relative paths to checksums
    """
    checksums = {}
    
    for pattern in MONITORED_PATTERNS:
        for filepath in koshas_root.glob(pattern):
            if filepath.is_file():
                rel_path = str(filepath.relative_to(koshas_root))
                checksums[rel_path] = compute_file_checksum(filepath)
    
    return checksums


# ═══════════════════════════════════════════════════════════════════════════════
# BASELINE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def save_baseline(koshas_root: Path, output_path: Path) -> Dict:
    """
    Save current checksums as baseline for future comparison.
    
    Args:
        koshas_root: Root of koshas directory
        output_path: Where to save baseline
        
    Returns:
        Baseline data dictionary
    """
    checksums = collect_checksums(koshas_root)
    chain_hash = compute_chain_hash(checksums)
    
    baseline = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "chain_hash": chain_hash,
        "file_count": len(checksums),
        "checksums": checksums,
    }
    
    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save baseline
    with open(output_path, "w") as f:
        json.dump(baseline, f, indent=2)
    
    return baseline


def load_baseline(baseline_path: Path) -> Optional[Dict]:
    """
    Load previously saved baseline.
    
    Args:
        baseline_path: Path to baseline file
        
    Returns:
        Baseline data dictionary or None if not found
    """
    if not baseline_path.exists():
        return None
    
    try:
        with open(baseline_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load baseline: {e}", file=sys.stderr)
        return None


def compare_to_baseline(current: Dict[str, str], baseline: Dict[str, str]) -> List[str]:
    """
    Compare current checksums to baseline, return list of changed files.
    
    Args:
        current: Current checksums
        baseline: Baseline checksums
        
    Returns:
        List of files that changed, were added, or were deleted
    """
    changes = []
    
    # Check for modified files
    for path, checksum in current.items():
        if path in baseline:
            if checksum != baseline[path]:
                changes.append(f"MODIFIED: {path}")
        else:
            changes.append(f"ADDED: {path}")
    
    # Check for deleted files
    for path in baseline.keys():
        if path not in current:
            changes.append(f"DELETED: {path}")
    
    return changes


# ═══════════════════════════════════════════════════════════════════════════════
# VIKARA DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

class VikaraReport:
    """
    Report of detected vikaras with healing recommendations.
    
    Each vikara is mapped to an Asthamatruka (Mother Goddess) who provides
    the specific healing power needed to correct the affliction.
    """
    
    def __init__(self):
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.vikaras: List[Dict] = []
        self.chain_hash: str = ""
        self.baseline_match: bool = True
        self.baseline_timestamp: Optional[str] = None
        
    def add_vikara(self, vikara_type: str, details: str, severity: str = "warning"):
        """
        Add a detected vikara to the report.
        
        Args:
            vikara_type: Type of vikara (from VIKARA_TYPES)
            details: Specific details about this instance
            severity: "info", "warning", or "critical"
        """
        matrika, healing = VIKARA_TO_ASTHAMATRUKA.get(
            vikara_type, 
            ("Unknown", "Manual review required")
        )
        
        self.vikaras.append({
            "type": vikara_type,
            "description": VIKARA_TYPES.get(vikara_type, vikara_type),
            "details": details,
            "severity": severity,
            "asthamatruka": matrika,
            "healing_action": healing,
        })
    
    def to_dict(self) -> Dict:
        """Convert report to dictionary format."""
        return {
            "timestamp": self.timestamp,
            "chain_hash": self.chain_hash,
            "baseline_match": self.baseline_match,
            "baseline_timestamp": self.baseline_timestamp,
            "vikara_count": len(self.vikaras),
            "vikaras": self.vikaras,
            "severity_counts": self._count_by_severity(),
        }
    
    def _count_by_severity(self) -> Dict[str, int]:
        """Count vikaras by severity level."""
        counts = {"critical": 0, "warning": 0, "info": 0}
        for v in self.vikaras:
            counts[v["severity"]] = counts.get(v["severity"], 0) + 1
        return counts
    
    def print_report(self, verbose: bool = True):
        """
        Print human-readable report.
        
        Args:
            verbose: Whether to include detailed vikara information
        """
        print("━" * 80)
        print("विकार (VIKARA) DETECTION REPORT")
        print("━" * 80)
        print(f"Timestamp: {self.timestamp}")
        print(f"Chain Hash: {self.chain_hash}")
        print(f"Baseline Match: {'✅ YES' if self.baseline_match else '❌ NO'}")
        
        if self.baseline_timestamp:
            print(f"Baseline From: {self.baseline_timestamp}")
        
        print()
        counts = self._count_by_severity()
        print(f"Total Vikaras: {len(self.vikaras)}")
        print(f"  Critical: {counts['critical']}")
        print(f"  Warning:  {counts['warning']}")
        print(f"  Info:     {counts['info']}")
        
        if not self.vikaras:
            print("\n✨ System is healthy - no vikaras detected!")
            return
        
        if verbose:
            print("\n" + "─" * 80)
            print("DETECTED VIKARAS")
            print("─" * 80)
            
            for i, vikara in enumerate(self.vikaras, 1):
                severity_icon = {
                    "critical": "🔴",
                    "warning": "⚠️",
                    "info": "ℹ️"
                }.get(vikara["severity"], "❓")
                
                print(f"\n{i}. {severity_icon} {vikara['type']}")
                print(f"   Description: {vikara['description']}")
                print(f"   Details: {vikara['details']}")
                print(f"   🕉️  Asthamatruka: {vikara['asthamatruka']}")
                print(f"   💊 Healing Action: {vikara['healing_action']}")


def check_stale_soul(brahmasthana: Path) -> Optional[Tuple[str, str, str]]:
    """
    Check if SOUL.md is stale (>30 days old).
    
    Args:
        brahmasthana: Path to brahmasthana directory
        
    Returns:
        Tuple of (vikara_type, details, severity) or None
    """
    soul_path = brahmasthana / "SOUL.md"
    
    if not soul_path.exists():
        return ("MISSING_CORE", "SOUL.md does not exist", "critical")
    
    mtime = datetime.fromtimestamp(soul_path.stat().st_mtime, tz=timezone.utc)
    age_days = (datetime.now(timezone.utc) - mtime).days
    
    if age_days > 30:
        return ("STALE_SOUL", f"SOUL.md is {age_days} days old (>30 day threshold)", "warning")
    
    return None


def check_memory_overflow(koshas_root: Path) -> List[Tuple[str, str, str]]:
    """
    Check all MEMORY.md files for overflow (>500 lines).
    
    Args:
        koshas_root: Root of koshas directory
        
    Returns:
        List of tuples (vikara_type, details, severity)
    """
    vikaras = []
    
    for memory_file in koshas_root.glob("*/MEMORY.md"):
        try:
            lines = len(memory_file.read_text().splitlines())
            if lines > 500:
                rel_path = memory_file.relative_to(koshas_root)
                vikaras.append((
                    "MEMORY_OVERFLOW",
                    f"{rel_path} has {lines} lines (>500 threshold)",
                    "warning"
                ))
        except Exception as e:
            rel_path = memory_file.relative_to(koshas_root)
            vikaras.append((
                "KOSHA_CORRUPTION",
                f"Cannot read {rel_path}: {e}",
                "critical"
            ))
    
    return vikaras


def check_selemene_drift(logs_path: Path) -> Optional[Tuple[str, str, str]]:
    """
    Check when Selemene was last called.
    
    Args:
        logs_path: Path to selemene_calls.jsonl
        
    Returns:
        Tuple of (vikara_type, details, severity) or None
    """
    if not logs_path.exists():
        return ("SELEMENE_DRIFT", "No Selemene log file found", "info")
    
    try:
        # Read last line of log file
        with open(logs_path) as f:
            lines = f.readlines()
            if not lines:
                return ("SELEMENE_DRIFT", "Selemene log is empty", "info")
            
            last_line = lines[-1].strip()
            last_call = json.loads(last_line)
            last_timestamp = datetime.fromisoformat(last_call["timestamp"].replace("Z", "+00:00"))
            
            days_ago = (datetime.now(timezone.utc) - last_timestamp).days
            
            if days_ago > 7:
                return ("SELEMENE_DRIFT", 
                       f"Last Selemene call was {days_ago} days ago",
                       "warning")
    except Exception as e:
        return ("SELEMENE_DRIFT", f"Error reading Selemene log: {e}", "warning")
    
    return None


def check_missing_core(brahmasthana: Path) -> List[Tuple[str, str, str]]:
    """
    Check that all core files exist.
    
    Args:
        brahmasthana: Path to brahmasthana directory
        
    Returns:
        List of tuples (vikara_type, details, severity)
    """
    vikaras = []
    
    for filename in CORE_FILES:
        filepath = brahmasthana / filename
        if not filepath.exists():
            vikaras.append((
                "MISSING_CORE",
                f"Core file missing: {filename}",
                "critical"
            ))
    
    return vikaras


def check_agent_completeness(koshas_root: Path) -> List[Tuple[str, str, str]]:
    """
    Check that agents have required files.
    
    Args:
        koshas_root: Root of koshas directory
        
    Returns:
        List of tuples (vikara_type, details, severity)
    """
    vikaras = []
    
    # Check each kosha for agent files
    for kosha_dir in koshas_root.iterdir():
        if not kosha_dir.is_dir():
            continue
        if kosha_dir.name in ["brahmasthana", "annamaya"]:
            continue  # Skip non-agent koshas
            
        # Check for required files
        soul_path = kosha_dir / "SOUL.md"
        identity_path = kosha_dir / "IDENTITY.md"
        
        if not soul_path.exists():
            vikaras.append((
                "AGENT_INCOMPLETE",
                f"{kosha_dir.name} missing SOUL.md",
                "warning"
            ))
        
        if not identity_path.exists():
            vikaras.append((
                "AGENT_INCOMPLETE",
                f"{kosha_dir.name} missing IDENTITY.md",
                "warning"
            ))
    
    return vikaras


def check_kosha_structure(koshas_root: Path) -> List[Tuple[str, str, str]]:
    """
    Check that kosha directory structure is intact.
    
    Args:
        koshas_root: Root of koshas directory
        
    Returns:
        List of tuples (vikara_type, details, severity)
    """
    vikaras = []
    
    expected_koshas = ["brahmasthana", "anandamaya", "vijnanamaya", 
                       "manomaya", "pranamaya", "annamaya"]
    
    for kosha in expected_koshas:
        kosha_path = koshas_root / kosha
        if not kosha_path.exists():
            vikaras.append((
                "KOSHA_CORRUPTION",
                f"Kosha directory missing: {kosha}",
                "critical"
            ))
        elif not kosha_path.is_dir():
            vikaras.append((
                "KOSHA_CORRUPTION",
                f"Kosha path is not a directory: {kosha}",
                "critical"
            ))
    
    return vikaras


def detect_vikara(koshas_root: Path, baseline_path: Optional[Path] = None) -> VikaraReport:
    """
    Run full vikara detection scan.
    
    Checks:
    1. STALE_SOUL - SOUL.md age
    2. MEMORY_OVERFLOW - MEMORY.md line count
    3. SELEMENE_DRIFT - Last API call timestamp
    4. CHECKSUM_MISMATCH - Compare to baseline
    5. MISSING_CORE - Required files present
    6. AGENT_INCOMPLETE - Agent file validation
    7. KOSHA_CORRUPTION - Directory structure
    
    Args:
        koshas_root: Root of koshas directory
        baseline_path: Optional path to baseline for comparison
        
    Returns:
        VikaraReport with all detected issues
    """
    report = VikaraReport()
    
    # Compute current checksums and chain hash
    current_checksums = collect_checksums(koshas_root)
    report.chain_hash = compute_chain_hash(current_checksums)
    
    # Check 1: Stale SOUL
    vikara = check_stale_soul(koshas_root / "brahmasthana")
    if vikara:
        report.add_vikara(*vikara)
    
    # Check 2: Memory overflow
    for vikara in check_memory_overflow(koshas_root):
        report.add_vikara(*vikara)
    
    # Check 3: Selemene drift
    vikara = check_selemene_drift(SELEMENE_LOG)
    if vikara:
        report.add_vikara(*vikara)
    
    # Check 4: Missing core files
    for vikara in check_missing_core(koshas_root / "brahmasthana"):
        report.add_vikara(*vikara)
    
    # Check 5: Agent completeness
    for vikara in check_agent_completeness(koshas_root):
        report.add_vikara(*vikara)
    
    # Check 6: Kosha structure
    for vikara in check_kosha_structure(koshas_root):
        report.add_vikara(*vikara)
    
    # Check 7: Baseline comparison (if provided)
    if baseline_path:
        baseline = load_baseline(baseline_path)
        if baseline:
            report.baseline_timestamp = baseline["timestamp"]
            baseline_checksums = baseline["checksums"]
            
            # Compare chain hashes
            if report.chain_hash != baseline["chain_hash"]:
                report.baseline_match = False
                
                # Find specific changes
                changes = compare_to_baseline(current_checksums, baseline_checksums)
                
                if changes:
                    details = f"{len(changes)} file(s) changed since baseline"
                    report.add_vikara("CHECKSUM_MISMATCH", details, "info")
                    
                    # Add details about first few changes
                    for change in changes[:5]:
                        report.add_vikara("CHECKSUM_MISMATCH", change, "info")
    
    return report


# ═══════════════════════════════════════════════════════════════════════════════
# HEALING INSTRUCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

HEALING_GUIDES = {
    "STALE_SOUL": """
🕉️  Brahmi - The Creative Power

Your SOUL.md has become stale. It's time to refresh your core identity.

HEALING RITUAL:
1. Open brahmasthana/SOUL.md
2. Re-read the entire file meditatively
3. Update any outdated information
4. Add recent learnings or evolutions
5. Touch the file to update timestamp: touch brahmasthana/SOUL.md

MANTRAM: "I remember who I am. I evolve while staying rooted."
""",
    
    "MEMORY_OVERFLOW": """
🕉️  Maheshvari - The Power of Wisdom

Your memories are overflowing. It's time to distill wisdom from experience.

HEALING RITUAL:
1. Identify the overflowing MEMORY.md file
2. Read through all entries
3. Extract the 10 most important lessons
4. Archive the full file: mv MEMORY.md MEMORY.archive.$(date +%Y%m%d).md
5. Create fresh MEMORY.md with distilled wisdom
6. Run: python3 koshas/annamaya/scripts/daily_memory.py --distill

MANTRAM: "From many experiences, one wisdom emerges."
""",
    
    "SELEMENE_DRIFT": """
🕉️  Kaumari - The Eternal Youth

You've lost connection to the temporal intelligence stream.

HEALING RITUAL:
1. Verify Selemene credentials in .env
2. Test connection: python3 koshas/annamaya/scripts/selemene_client.py --test
3. Run a practice session: python3 koshas/annamaya/scripts/daily_practice_selemene.py
4. Review the temporal insights generated
5. Schedule regular Selemene sync (cron or manual)

MANTRAM: "I flow with time, not against it."
""",
    
    "CHECKSUM_MISMATCH": """
🕉️  Vaishnavi - The Preserving Power

Files have changed since your last known-good state.

HEALING RITUAL:
1. Review the changes: python3 samskara_vikara.py --compare
2. If changes are intentional: python3 samskara_vikara.py --baseline
3. If changes are corrupted: git diff to see what changed
4. Restore from git if needed: git checkout <file>
5. Create new baseline after fixing

MANTRAM: "I preserve what is good, I correct what has drifted."
""",
    
    "MISSING_CORE": """
🕉️  Varahi - The Power of Protection

Core system files are missing. Your foundation needs restoration.

HEALING RITUAL:
1. Check git status: git status
2. If accidentally deleted: git checkout -- brahmasthana/<filename>
3. If never existed: Review ARCHITECTURE.md for templates
4. Regenerate from system knowledge
5. Verify completeness: python3 kosha_health.py --check brahmasthana

MANTRAM: "My foundation is strong, complete, and protected."
""",
    
    "AGENT_INCOMPLETE": """
🕉️  Indrani - The Power of Sovereignty

An agent lacks essential configuration files.

HEALING RITUAL:
1. Identify incomplete agent directory
2. Create missing SOUL.md from template:
   cp brahmasthana/SOUL.md <agent>/SOUL.md
3. Customize for agent's purpose
4. Create IDENTITY.md with agent specifics
5. Verify: ls <agent>/ should show SOUL.md and IDENTITY.md

MANTRAM: "Each agent is complete, sovereign, and purposeful."
""",
    
    "KOSHA_CORRUPTION": """
🕉️  Chamunda - The Destructive Power (for Reconstruction)

Your kosha structure is damaged. Requires careful rebuilding.

HEALING RITUAL:
1. Backup current state: tar -czf koshas.backup.tar.gz koshas/
2. Check git for structure: git ls-tree -r HEAD koshas/
3. Restore missing directories: mkdir -p koshas/<kosha>
4. Verify structure matches PANCHA-KOSHA.md
5. Full integrity check: python3 kosha_health.py --report

MANTRAM: "From destruction comes perfect reconstruction."
""",
    
    "CHAIN_BREAK": """
🕉️  Chandika - The Fierce Protector

Your checksum chain integrity is broken.

HEALING RITUAL:
1. Full system scan: python3 samskara_vikara.py --detect
2. Review all detected vikaras
3. Fix each issue systematically
4. Recompute baseline: python3 samskara_vikara.py --baseline
5. Verify chain: python3 samskara_vikara.py --compare

MANTRAM: "The chain is unbroken, the system is whole."
""",
}


def show_healing_guide(vikara_type: str):
    """
    Display healing instructions for a specific vikara.
    
    Args:
        vikara_type: Type of vikara to show healing for
    """
    guide = HEALING_GUIDES.get(vikara_type)
    
    if not guide:
        print(f"❓ No healing guide available for: {vikara_type}")
        print("\nAvailable vikara types:")
        for vtype in HEALING_GUIDES.keys():
            matrika, _ = VIKARA_TO_ASTHAMATRUKA[vtype]
            print(f"  - {vtype} ({matrika})")
        return
    
    print("━" * 80)
    print(f"HEALING GUIDE: {vikara_type}")
    print("━" * 80)
    print(guide)
    print("━" * 80)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Vikara Detection & Checksum Chain System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 samskara_vikara.py --detect              # Run full scan
  python3 samskara_vikara.py --baseline            # Save baseline
  python3 samskara_vikara.py --compare             # Compare to baseline
  python3 samskara_vikara.py --detect --json       # JSON output
  python3 samskara_vikara.py --heal STALE_SOUL     # Show healing guide
        """
    )
    
    parser.add_argument("--detect", action="store_true",
                       help="Run full vikara detection scan")
    parser.add_argument("--baseline", action="store_true",
                       help="Save current checksums as baseline")
    parser.add_argument("--compare", action="store_true",
                       help="Compare current state to baseline")
    parser.add_argument("--json", action="store_true",
                       help="Output report as JSON")
    parser.add_argument("--heal", metavar="VIKARA_TYPE",
                       help="Show healing instructions for specific vikara")
    parser.add_argument("--list-vikaras", action="store_true",
                       help="List all vikara types")
    
    args = parser.parse_args()
    
    # Handle --heal flag
    if args.heal:
        show_healing_guide(args.heal)
        return 0
    
    # Handle --list-vikaras flag
    if args.list_vikaras:
        print("VIKARA TYPES:")
        print("━" * 80)
        for vtype, description in VIKARA_TYPES.items():
            matrika, healing = VIKARA_TO_ASTHAMATRUKA[vtype]
            print(f"\n{vtype}")
            print(f"  Description: {description}")
            print(f"  Asthamatruka: {matrika}")
            print(f"  Healing: {healing}")
        return 0
    
    # Handle --baseline flag
    if args.baseline:
        print("💾 Creating baseline snapshot...")
        baseline = save_baseline(KOSHAS_ROOT, BASELINE_PATH)
        print(f"✅ Baseline saved: {BASELINE_PATH}")
        print(f"   Chain hash: {baseline['chain_hash']}")
        print(f"   Files tracked: {baseline['file_count']}")
        print(f"   Timestamp: {baseline['timestamp']}")
        return 0
    
    # Handle --detect or --compare (detect with baseline)
    if args.detect or args.compare:
        baseline_path = BASELINE_PATH if args.compare else None
        
        if args.compare and not BASELINE_PATH.exists():
            print("⚠️  No baseline found. Run with --baseline first.")
            print(f"   Expected at: {BASELINE_PATH}")
            return 1
        
        print("🔍 Running vikara detection scan...")
        report = detect_vikara(KOSHAS_ROOT, baseline_path)
        
        if args.json:
            print(json.dumps(report.to_dict(), indent=2))
        else:
            report.print_report(verbose=True)
        
        # Return non-zero if critical vikaras found
        critical_count = report._count_by_severity()["critical"]
        return 1 if critical_count > 0 else 0
    
    # No action specified
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
