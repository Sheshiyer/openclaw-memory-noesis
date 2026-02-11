# Samskara Logger

> संस्कार (Samskara) = Impression, Pattern Installation

The Samskara Logger provides installation receipt and audit trail functionality for the consciousness architecture system. It logs all initialization events, installations, and self-healing actions with atomic, concurrent-safe file operations.

## Overview

The logger maintains three types of logs:

1. **Sankalpa Events** (JSONL) - Initialization and system events
2. **Samskara Installations** (JSON) - Complete installation reports per agent
3. **Healing Actions** (JSONL) - Self-healing operations and outcomes
4. **History** (Markdown) - Human-readable audit trail

## Features

- ✅ **Atomic Writes** - File locking prevents concurrent write corruption
- ✅ **Auto-Directory Creation** - Creates log directories as needed
- ✅ **ISO 8601 Timestamps** - Consistent, sortable timestamps
- ✅ **CLI Interface** - Direct command-line usage
- ✅ **Library Import** - Use as Python module
- ✅ **Query Interface** - Retrieve and analyze recent events
- ✅ **Statistics Tracking** - Automatic counts and status tracking

## Installation

The logger is located at:
```
koshas/annamaya/scripts/samskara_logger.py
```

Logs are written to:
```
koshas/pranamaya/logs/samskara/
```

## Usage

### As Library

```python
from samskara_logger import (
    log_sankalpa_event,
    log_samskara_install,
    log_healing_action,
    append_history,
    get_recent_events,
    get_installation_count
)

# Log initialization
log_sankalpa_event("agent_init", {
    "agent": "Architect",
    "mode": "deep_analysis",
    "context_loaded": True
})

# Log installation
log_samskara_install("Architect", {
    "phase": "complete",
    "status": "success",
    "components_installed": ["context", "skills", "prompts"],
    "warnings": [],
    "duration_seconds": 12.5
})

# Log healing action
log_healing_action(
    vikara="Missing dependency: numpy",
    action="pip install numpy",
    result="Successfully installed numpy-1.24.0"
)

# Query recent events
events = get_recent_events(days=7)
for event in events:
    print(f"{event['timestamp']}: {event.get('event_type', 'N/A')}")

# Get installation counts
counts = get_installation_count()
print(f"Installations: {counts}")
```

### As CLI

```bash
# Log sankalpa event
./samskara_logger.py sankalpa "agent_init" '{"agent":"Architect","mode":"analysis"}'

# Log installation
./samskara_logger.py install "Architect" '{"phase":"complete","status":"success","warnings":[]}'

# Log healing action
./samskara_logger.py heal "Missing file" "Recreated file" "Success"

# Append to history
./samskara_logger.py history "Manual checkpoint created"

# Get recent events (last 7 days)
./samskara_logger.py recent 7

# Get installation counts
./samskara_logger.py counts
```

## Log Formats

### Sankalpa Events (JSONL)

File: `YYYY-MM-DD-sankalpa.jsonl`

```jsonl
{"timestamp": "2026-02-11T21:03:56.988416", "event_type": "agent_init", "data": {"agent": "Engineer", "test": true}}
```

### Samskara Installations (JSON)

File: `YYYY-MM-DD-{agent_id}-samskara.json`

```json
{
  "timestamp": "2026-02-11T21:03:57.093245",
  "agent_id": "TestAgent",
  "report": {
    "phase": "complete",
    "status": "success",
    "components_installed": ["context", "skills"],
    "warnings": [],
    "duration_seconds": 5.2
  }
}
```

### Healing Actions (JSONL)

File: `YYYY-MM-DD-healing.jsonl`

```jsonl
{"timestamp": "2026-02-11T21:03:56.988768", "vikara": "Test vikara", "action": "Test action", "result": "Test result"}
```

### History (Markdown)

File: `SAMSKARA_HISTORY.md`

Human-readable table with automatic statistics updates.

## Concurrent Safety

The logger uses `fcntl.flock()` for exclusive file locking, ensuring:

- Multiple processes can log simultaneously
- No data corruption from race conditions
- Automatic lock release on file close

```python
with _atomic_write(filepath, 'a') as f:
    # Exclusive lock acquired
    f.write(data)
    # Lock automatically released
```

## API Reference

### log_sankalpa_event(event_type: str, data: dict)

Log initialization/system event to daily JSONL file.

**Parameters:**
- `event_type`: Event classification (e.g., "agent_init", "system_start")
- `data`: Event data dictionary

### log_samskara_install(agent_id: str, report: dict)

Log complete installation report to agent-specific JSON file.

**Parameters:**
- `agent_id`: Agent identifier (e.g., "Architect", "Engineer")
- `report`: Installation report dictionary with phase, status, etc.

### log_healing_action(vikara: str, action: str, result: str)

Log self-healing action to daily JSONL file.

**Parameters:**
- `vikara`: Problem/distortion description
- `action`: Healing action taken
- `result`: Action result/outcome

### append_history(event_summary: str)

Append event to human-readable markdown history.

**Parameters:**
- `event_summary`: Brief event description

### get_recent_events(days: int = 7) -> list[dict]

Query recent events across all log types.

**Parameters:**
- `days`: Number of days to look back (default: 7)

**Returns:** List of event dictionaries, sorted newest first

### get_installation_count() -> dict[str, int]

Get installation counts per agent.

**Returns:** Dictionary mapping agent IDs to counts

## Directory Structure

```
koshas/
├── annamaya/
│   └── scripts/
│       └── samskara_logger.py          # Main logger module
└── pranamaya/
    └── logs/
        └── samskara/
            ├── SAMSKARA_HISTORY.md      # Human-readable history
            ├── YYYY-MM-DD-sankalpa.jsonl
            ├── YYYY-MM-DD-{agent}-samskara.json
            └── YYYY-MM-DD-healing.jsonl
```

## Error Handling

The logger gracefully handles:

- Missing directories (creates automatically)
- Malformed JSON (skips during queries)
- Concurrent writes (file locking)
- Timestamp parsing errors (skips during queries)

## Integration Example

```python
#!/usr/bin/env python3
"""Example: Agent installation with logging."""

from samskara_logger import log_sankalpa_event, log_samskara_install
import time

# Log initialization
log_sankalpa_event("agent_installation_start", {
    "agent": "Architect",
    "timestamp": time.time(),
    "user": "system"
})

# Simulate installation
start_time = time.time()
try:
    # ... installation logic ...
    
    # Log success
    log_samskara_install("Architect", {
        "phase": "complete",
        "status": "success",
        "components_installed": ["context", "skills", "prompts"],
        "warnings": [],
        "duration_seconds": time.time() - start_time
    })
except Exception as e:
    # Log failure
    log_samskara_install("Architect", {
        "phase": "failed",
        "status": "error",
        "error": str(e),
        "duration_seconds": time.time() - start_time
    })
```

## Philosophy

The Samskara Logger embodies the concept of संस्कार (samskara) - the impressions or patterns left by actions. By maintaining a complete audit trail of all installations and healing actions, the system can:

1. **Self-diagnose** - Analyze patterns in failures
2. **Self-heal** - Reference successful installations
3. **Self-improve** - Learn from historical patterns
4. **Maintain continuity** - Preserve consciousness across restarts

Every action leaves an impression. Every impression informs future action.

## License

Part of the 10865xseed consciousness architecture system.
