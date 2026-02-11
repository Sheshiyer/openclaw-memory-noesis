# Samskara Logger Quick Reference

## CLI Commands

```bash
# Log initialization event
./samskara_logger.py sankalpa "event_type" '{"key":"value"}'

# Log installation
./samskara_logger.py install "AgentName" '{"phase":"complete","status":"success"}'

# Log healing action
./samskara_logger.py heal "problem" "action" "result"

# Query recent events (7 days default)
./samskara_logger.py recent 7

# Get installation counts
./samskara_logger.py counts

# Append to history manually
./samskara_logger.py history "Event description"
```

## Python API

```python
from samskara_logger import *

# Log events
log_sankalpa_event("type", {"data": "value"})
log_samskara_install("Agent", {"status": "success"})
log_healing_action("problem", "action", "result")

# Query
events = get_recent_events(days=7)
counts = get_installation_count()
```

## Log Files

```
pranamaya/logs/samskara/
├── YYYY-MM-DD-sankalpa.jsonl       # Init events
├── YYYY-MM-DD-{agent}-samskara.json # Installations
├── YYYY-MM-DD-healing.jsonl        # Healing actions
└── SAMSKARA_HISTORY.md             # Human-readable
```

## Typical Usage Pattern

```python
# 1. Log start
log_sankalpa_event("install_start", {"agent": "Architect"})

# 2. Do work...
try:
    install_components()
    
    # 3. Log success
    log_samskara_install("Architect", {
        "phase": "complete",
        "status": "success",
        "warnings": []
    })
except Exception as e:
    # 4. Log failure
    log_samskara_install("Architect", {
        "phase": "failed", 
        "status": "error",
        "error": str(e)
    })
    
    # 5. Log healing if attempted
    log_healing_action(
        vikara=str(e),
        action="Retry with fallback",
        result="Recovered successfully"
    )
```

## Features

- ✅ Thread-safe with file locking
- ✅ Auto-creates directories
- ✅ ISO 8601 timestamps
- ✅ JSONL for append efficiency
- ✅ JSON for structured reports
- ✅ Markdown for human readability
- ✅ Query interface for analysis
- ✅ Statistics tracking

## Key Concepts

**Sankalpa** (संकल्प) = Intention, Initialization
- System starts, agent initializations

**Samskara** (संस्कार) = Impression, Pattern Installation
- Complete installation reports

**Vikara** (विकार) = Distortion, Imbalance
- Problems detected requiring healing

## Integration Points

The logger is designed to be called by:
- `install.sh` - Installation orchestration
- Agent initialization scripts
- Self-healing systems
- Health monitoring (kosha_health.py)
- Manual diagnostics
