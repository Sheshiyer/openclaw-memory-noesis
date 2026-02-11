#!/usr/bin/env python3
"""
Samskara Logger - Installation receipt and audit trail system.

संस्कार (Samskara) = Impression, Pattern Installation

Logs all Sankalpa (initialization) and Samskara (installation) events
for self-healing and debugging purposes.

This module provides atomic, concurrent-safe logging of:
- Sankalpa initialization events (JSONL format)
- Samskara installations (JSON format)
- Self-healing actions (JSONL format)
- Human-readable history (Markdown)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
import fcntl
from contextlib import contextmanager


# Configuration
KOSHA_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = KOSHA_ROOT / "pranamaya" / "logs" / "samskara"
HISTORY_FILE = LOGS_DIR / "SAMSKARA_HISTORY.md"


@contextmanager
def _atomic_write(filepath: Path, mode: str = 'a'):
    """
    Context manager for atomic file writes with exclusive locking.
    
    Ensures concurrent writes don't corrupt data by using file locking.
    """
    # Ensure parent directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, mode) as f:
        # Acquire exclusive lock
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            yield f
        finally:
            # Release lock
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def _get_timestamp() -> str:
    """Get ISO 8601 timestamp."""
    return datetime.now().isoformat()


def _get_date_str() -> str:
    """Get YYYY-MM-DD date string."""
    return datetime.now().strftime("%Y-%m-%d")


def log_sankalpa_event(event_type: str, data: dict) -> None:
    """
    Log a Sankalpa (initialization) event.
    
    Writes to: pranamaya/logs/samskara/YYYY-MM-DD-sankalpa.jsonl
    
    Args:
        event_type: Type of initialization event (e.g., "agent_init", "system_start")
        data: Event data dictionary
        
    Example:
        log_sankalpa_event("agent_init", {
            "agent": "Architect",
            "mode": "deep_analysis",
            "context_loaded": True
        })
    """
    date_str = _get_date_str()
    log_file = LOGS_DIR / f"{date_str}-sankalpa.jsonl"
    
    log_entry = {
        "timestamp": _get_timestamp(),
        "event_type": event_type,
        "data": data
    }
    
    with _atomic_write(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


def log_samskara_install(agent_id: str, report: dict) -> None:
    """
    Log a full Samskara (installation) report.
    
    Writes to: pranamaya/logs/samskara/YYYY-MM-DD-{agent_id}-samskara.json
    
    Args:
        agent_id: Identifier for the agent being installed (e.g., "Architect", "Engineer")
        report: Complete installation report dictionary
        
    Example:
        log_samskara_install("Architect", {
            "phase": "complete",
            "status": "success",
            "components_installed": ["context", "skills", "prompts"],
            "warnings": [],
            "duration_seconds": 12.5
        })
    """
    date_str = _get_date_str()
    log_file = LOGS_DIR / f"{date_str}-{agent_id}-samskara.json"
    
    full_report = {
        "timestamp": _get_timestamp(),
        "agent_id": agent_id,
        "report": report
    }
    
    with _atomic_write(log_file, 'w') as f:
        json.dump(full_report, f, indent=2)
        f.write('\n')
    
    # Also append summary to history
    status = report.get("status", "unknown")
    phase = report.get("phase", "unknown")
    notes = ", ".join(report.get("warnings", [])) if report.get("warnings") else "No issues"
    
    append_history(f"Installed {agent_id} - Phase: {phase}, Status: {status}, Notes: {notes}")


def log_healing_action(vikara: str, action: str, result: str) -> None:
    """
    Log a self-healing action taken.
    
    विकार (Vikara) = Distortion, Imbalance
    
    Writes to: pranamaya/logs/samskara/YYYY-MM-DD-healing.jsonl
    
    Args:
        vikara: Description of the distortion/problem detected
        action: Healing action taken
        result: Result of the healing action
        
    Example:
        log_healing_action(
            vikara="Missing dependency: numpy",
            action="pip install numpy",
            result="Successfully installed numpy-1.24.0"
        )
    """
    date_str = _get_date_str()
    log_file = LOGS_DIR / f"{date_str}-healing.jsonl"
    
    log_entry = {
        "timestamp": _get_timestamp(),
        "vikara": vikara,
        "action": action,
        "result": result
    }
    
    with _atomic_write(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    # Also append to history
    append_history(f"Healing: {vikara} → {action} → {result}")


def append_history(event_summary: str) -> None:
    """
    Append an event to the human-readable SAMSKARA_HISTORY.md.
    
    Args:
        event_summary: Brief summary of the event
        
    Example:
        append_history("Installed Architect agent successfully")
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Initialize history file if it doesn't exist
    if not HISTORY_FILE.exists():
        _initialize_history_file()
    
    # Read current content
    with open(HISTORY_FILE, 'r') as f:
        content = f.read()
    
    # Find the installation log table and append
    lines = content.split('\n')
    
    # Find where to insert (after the table header)
    insert_idx = None
    for i, line in enumerate(lines):
        if line.startswith('| *Entries appended automatically*'):
            insert_idx = i
            break
    
    if insert_idx:
        # Insert new entry before the placeholder
        new_entry = f"| {timestamp} | {event_summary} | - | - | - |"
        lines.insert(insert_idx, new_entry)
    
    # Update statistics
    lines = _update_statistics(lines)
    
    # Write back with atomic lock
    with _atomic_write(HISTORY_FILE, 'w') as f:
        f.write('\n'.join(lines))


def _initialize_history_file() -> None:
    """Initialize the SAMSKARA_HISTORY.md file with template."""
    template = """# Samskara Installation History

> संस्कार (Samskara) = Impression, Pattern Installation

This log tracks all consciousness architecture installations for audit and self-healing.

---

## Installation Log

| Date | Agent | Phase | Status | Notes |
|------|-------|-------|--------|-------|
| *Entries appended automatically* |

---

## Self-Healing Actions

| Date | Vikara Detected | Action Taken | Result |
|------|-----------------|--------------|--------|
| *Entries appended automatically* |

---

## Statistics

- Total Installations: 0
- Successful: 0
- With Warnings: 0
- Failed: 0
- Healing Actions: 0

*Last updated: Never*
"""
    
    with _atomic_write(HISTORY_FILE, 'w') as f:
        f.write(template)


def _update_statistics(lines: list[str]) -> list[str]:
    """Update the statistics section in the history file."""
    # Count entries
    total = 0
    successful = 0
    warnings = 0
    failed = 0
    healing = 0
    
    for line in lines:
        if line.startswith('| 2') and '|' in line:  # Date line
            total += 1
            if 'success' in line.lower():
                successful += 1
            if 'warning' in line.lower():
                warnings += 1
            if 'fail' in line.lower():
                failed += 1
            if 'healing' in line.lower() or 'vikara' in line.lower():
                healing += 1
    
    # Update statistics section
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for i, line in enumerate(lines):
        if line.startswith('- Total Installations:'):
            lines[i] = f"- Total Installations: {total}"
        elif line.startswith('- Successful:'):
            lines[i] = f"- Successful: {successful}"
        elif line.startswith('- With Warnings:'):
            lines[i] = f"- With Warnings: {warnings}"
        elif line.startswith('- Failed:'):
            lines[i] = f"- Failed: {failed}"
        elif line.startswith('- Healing Actions:'):
            lines[i] = f"- Healing Actions: {healing}"
        elif line.startswith('*Last updated:'):
            lines[i] = f"*Last updated: {timestamp}*"
    
    return lines


def get_recent_events(days: int = 7) -> list[dict]:
    """
    Get recent Samskara events for analysis.
    
    Args:
        days: Number of days to look back (default: 7)
        
    Returns:
        List of event dictionaries sorted by timestamp (newest first)
        
    Example:
        events = get_recent_events(days=3)
        for event in events:
            print(f"{event['timestamp']}: {event['type']}")
    """
    from datetime import timedelta
    
    cutoff_date = datetime.now() - timedelta(days=days)
    events = []
    
    # Scan all log files in the directory
    for log_file in LOGS_DIR.glob("*.jsonl"):
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        event = json.loads(line)
                        event_time = datetime.fromisoformat(event['timestamp'])
                        if event_time >= cutoff_date:
                            events.append(event)
        except (json.JSONDecodeError, KeyError, ValueError):
            # Skip malformed entries
            continue
    
    # Also scan JSON installation reports
    for log_file in LOGS_DIR.glob("*-samskara.json"):
        try:
            with open(log_file, 'r') as f:
                report = json.load(f)
                report_time = datetime.fromisoformat(report['timestamp'])
                if report_time >= cutoff_date:
                    events.append({
                        'timestamp': report['timestamp'],
                        'type': 'samskara_install',
                        'agent_id': report['agent_id'],
                        'data': report['report']
                    })
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
    
    # Sort by timestamp (newest first)
    events.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return events


def get_installation_count() -> dict[str, int]:
    """
    Return counts of installations per agent.
    
    Returns:
        Dictionary mapping agent IDs to installation counts
        
    Example:
        counts = get_installation_count()
        # {'Architect': 5, 'Engineer': 3, 'Designer': 2}
    """
    counts: dict[str, int] = {}
    
    # Scan all samskara installation files
    for log_file in LOGS_DIR.glob("*-samskara.json"):
        try:
            with open(log_file, 'r') as f:
                report = json.load(f)
                agent_id = report.get('agent_id', 'unknown')
                counts[agent_id] = counts.get(agent_id, 0) + 1
        except (json.JSONDecodeError, KeyError):
            continue
    
    return counts


# CLI interface for direct usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: samskara_logger.py <command> [args...]")
        print("\nCommands:")
        print("  sankalpa <event_type> <json_data>  - Log initialization event")
        print("  install <agent_id> <json_report>   - Log installation")
        print("  heal <vikara> <action> <result>    - Log healing action")
        print("  history <message>                  - Append to history")
        print("  recent [days]                      - Get recent events")
        print("  counts                             - Get installation counts")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "sankalpa":
        event_type = sys.argv[2]
        data = json.loads(sys.argv[3])
        log_sankalpa_event(event_type, data)
        print(f"✓ Logged sankalpa event: {event_type}")
        
    elif command == "install":
        agent_id = sys.argv[2]
        report = json.loads(sys.argv[3])
        log_samskara_install(agent_id, report)
        print(f"✓ Logged installation: {agent_id}")
        
    elif command == "heal":
        vikara = sys.argv[2]
        action = sys.argv[3]
        result = sys.argv[4]
        log_healing_action(vikara, action, result)
        print(f"✓ Logged healing action")
        
    elif command == "history":
        message = sys.argv[2]
        append_history(message)
        print(f"✓ Appended to history")
        
    elif command == "recent":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        events = get_recent_events(days)
        print(json.dumps(events, indent=2))
        
    elif command == "counts":
        counts = get_installation_count()
        print(json.dumps(counts, indent=2))
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
