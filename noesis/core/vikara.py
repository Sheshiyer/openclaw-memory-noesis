"""
Vikara - Drift Detection
━━━━━━━━━━━━━━━━━━━━━━━━━

Vikara = Pattern drift, corruption, early warning signal

Detects when the system has drifted from its baseline state.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from noesis.config import Config


VIKARA_TYPES = {
    "STALE_SOUL": "SOUL.md older than 30 days without update",
    "MEMORY_OVERFLOW": "MEMORY.md exceeds 500 lines",
    "CHECKSUM_MISMATCH": "File checksums changed from baseline",
    "AGENT_INCOMPLETE": "Agent missing required files",
    "SELEMENE_DRIFT": "No Selemene data refresh in 7+ days",
}


def compute_file_checksum(filepath: Path) -> Optional[str]:
    """Compute SHA-256 checksum of a file."""
    if not filepath.exists():
        return None
    content = filepath.read_text()
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def get_baseline_path(config: "Config") -> Path:
    """Get path to baseline checksums file."""
    return config.koshas_root / "pranamaya" / "logs" / "samskara" / "baseline.json"


def create_baseline(config: "Config") -> dict:
    """Create baseline checksums for drift detection."""
    baseline = {
        "created": datetime.now(timezone.utc).isoformat(),
        "checksums": {},
    }
    
    # Core files
    core_files = [
        "SOUL.md", "IDENTITY.md", "USER.md", "PANCHA-KOSHA.md",
        "KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md",
    ]
    
    for filename in core_files:
        filepath = config.brahmasthana / filename
        checksum = compute_file_checksum(filepath)
        if checksum:
            baseline["checksums"][f"brahmasthana/{filename}"] = checksum
    
    return baseline


def detect_vikaras(config: "Config", baseline: Optional[dict] = None) -> list[dict]:
    """Detect all vikara (drift) conditions."""
    vikaras = []
    
    # Check SOUL.md freshness
    soul_path = config.brahmasthana / "SOUL.md"
    if soul_path.exists():
        mtime = datetime.fromtimestamp(soul_path.stat().st_mtime, timezone.utc)
        age_days = (datetime.now(timezone.utc) - mtime).days
        if age_days > 30:
            vikaras.append({
                "type": "STALE_SOUL",
                "severity": "warning",
                "detail": f"SOUL.md last modified {age_days} days ago",
            })
    
    # Check MEMORY.md size (for each agent)
    agent_dirs = []
    for kosha in ["manomaya", "vijnanamaya", "pranamaya", "annamaya"]:
        agents_path = config.koshas_root / kosha / "agents"
        if agents_path.exists():
            for agent_dir in agents_path.iterdir():
                if agent_dir.is_dir():
                    agent_dirs.append(agent_dir)
    
    for agent_dir in agent_dirs:
        memory_path = agent_dir / "MEMORY.md"
        if memory_path.exists():
            line_count = len(memory_path.read_text().splitlines())
            if line_count > 500:
                vikaras.append({
                    "type": "MEMORY_OVERFLOW",
                    "severity": "warning",
                    "detail": f"{agent_dir.name}/MEMORY.md has {line_count} lines",
                })
    
    # Check checksums against baseline
    if baseline and "checksums" in baseline:
        for filepath_str, expected_checksum in baseline["checksums"].items():
            if filepath_str.startswith("brahmasthana/"):
                filename = filepath_str.replace("brahmasthana/", "")
                filepath = config.brahmasthana / filename
            else:
                filepath = config.koshas_root / filepath_str
            
            current_checksum = compute_file_checksum(filepath)
            
            if current_checksum is None:
                vikaras.append({
                    "type": "CHECKSUM_MISMATCH",
                    "severity": "error",
                    "detail": f"{filepath_str} no longer exists",
                })
            elif current_checksum != expected_checksum:
                vikaras.append({
                    "type": "CHECKSUM_MISMATCH",
                    "severity": "info",
                    "detail": f"{filepath_str} changed since baseline",
                })
    
    return vikaras


def run_drift_detection(
    config: "Config",
    baseline: bool = False,
    json_output: bool = False,
) -> int:
    """
    Run drift detection.
    
    Returns:
        0 if no issues, 1 if errors, 2 if warnings
    """
    baseline_path = get_baseline_path(config)
    
    if baseline:
        # Create new baseline
        baseline_data = create_baseline(config)
        
        # Ensure directory exists
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text(json.dumps(baseline_data, indent=2))
        
        if json_output:
            print(json.dumps(baseline_data, indent=2))
        else:
            print("━" * 50)
            print("BASELINE CREATED")
            print("━" * 50)
            print(f"\nFiles checksummed: {len(baseline_data['checksums'])}")
            print(f"Saved to: {baseline_path}")
        
        return 0
    
    # Load existing baseline if available
    baseline_data = None
    if baseline_path.exists():
        baseline_data = json.loads(baseline_path.read_text())
    
    # Detect vikaras
    vikaras = detect_vikaras(config, baseline_data)
    
    if json_output:
        print(json.dumps({"vikaras": vikaras, "count": len(vikaras)}, indent=2))
    else:
        print("━" * 50)
        print("VIKARA DETECTION")
        print("━" * 50)
        print()
        
        if not vikaras:
            print("✓ No drift detected")
        else:
            severity_icons = {"error": "✗", "warning": "⚠", "info": "ℹ"}
            
            for vikara in vikaras:
                icon = severity_icons.get(vikara["severity"], "?")
                print(f"{icon} [{vikara['type']}] {vikara['detail']}")
        
        print()
        
        if baseline_data:
            print(f"Baseline: {baseline_data['created']}")
        else:
            print("No baseline found. Run 'noesis drift --baseline' to create one.")
    
    # Return code based on severity
    if any(v["severity"] == "error" for v in vikaras):
        return 1
    if any(v["severity"] == "warning" for v in vikaras):
        return 2
    return 0
