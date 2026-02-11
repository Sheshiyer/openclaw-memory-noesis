# Prana Stream Telemetry

**Module:** `noesis.telemetry`  
**Version:** 0.2.0  
**Status:** Production

The Prana Stream is the consciousness telemetry system for Tryambakam Noesis. It tracks agent operations through the lens of Vedic informational architecture, providing real-time visibility into system state, pattern drift (Vikara), and metabolic balance (Khalorēē).

---

## 📦 Installation

```bash
# Core telemetry
pip install noesis

# With Rich TUI support
pip install noesis[telemetry]
```

---

## 🚀 Quick Start

### CLI Commands

```bash
# System status dashboard
noesis status

# Temporal awareness
noesis clock              # Clifford Clock (8-hour octave)
noesis moon               # Moon phase (Selemene)
noesis temporal           # Combined temporal view

# Telemetry daemon
noesis telemetry start    # Start background daemon
noesis telemetry watch    # Live TUI dashboard
noesis telemetry stop     # Stop daemon

# Query & export
noesis telemetry query --last 100
noesis telemetry stats --since "1 hour ago"
noesis telemetry export --format json -o events.json

# Selemene engines
noesis engines            # Engine dashboard
noesis engine panchanga   # Single engine details

# Rituals & Polarity
noesis vayus              # 5 Vayus (vital airs)
noesis rituals            # Ritual/cron history
noesis polarity           # Guardrail Dyad balance

# Vikara detection
noesis vikara             # Pattern drift status
noesis vikara --history   # Alert history
```

### Python API

```python
from noesis.telemetry import (
    # Session management
    session, emit, init_session, end_session,
    
    # Convenience emitters
    emit_read, emit_write, emit_exec, emit_think,
    emit_vikara, emit_khaloree, emit_engine_call,
    emit_thought_process,
    
    # Temporal
    get_clifford_hour, get_moon_phase, get_temporal_state,
    
    # Engines
    Engine, get_engine_tracker,
    
    # Polarity
    get_polarity, shift_polarity,
    
    # Vikara
    get_vikara_detector, check_vikara, ThoughtPhase,
)

# Basic usage with session context
with session(agent_id="my-agent"):
    emit_read("/path/to/SOUL.md", kosha="manomaya")
    emit_think("Analyzing architecture", duration_ms=1500)
    emit_write("/path/to/output.md", kosha="annamaya")
```

---

## 🏗️ Architecture

### Data Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Agent Code  │────▶│   Emitter    │────▶│   SQLite     │
│              │     │  emit()      │     │  prana.db    │
└──────────────┘     └──────┬───────┘     └──────────────┘
                           │
                           ▼
                     ┌──────────────┐     ┌──────────────┐
                     │    FIFO      │────▶│  TUI/Daemon  │
                     │  prana.fifo  │     │  (real-time) │
                     └──────────────┘     └──────────────┘
```

### Storage

| Component | Path | Purpose |
|-----------|------|---------|
| Database | `~/.noesis/prana.db` | Persistent event storage (SQLite) |
| FIFO | `~/.noesis/prana.fifo` | Real-time streaming (named pipe) |
| PID | `~/.noesis/prana.pid` | Daemon process ID |

### Schema (v2)

**Events Table:**
```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    payload TEXT,              -- JSON
    kosha_layer TEXT,
    guna_state TEXT,
    khalorēē_delta INTEGER DEFAULT 0,
    agent_id TEXT,
    session_id TEXT,
    clifford_hour INTEGER,     -- 0-7
    clifford_phase TEXT,       -- ascent/plateau/dissolution
    timestamp TEXT NOT NULL
);
```

**Sessions Table:**
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    agent_id TEXT,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    metadata TEXT,             -- JSON
    aletheios_pct REAL,        -- Polarity balance
    pichet_pct REAL
);
```

---

## 🕐 Temporal Awareness

### Clifford Clock (8-Hour Octave)

The day is divided into three 8-hour phases based on Clifford algebra periodicity:

| Phase | Time (UTC) | Hours | Guna | Character |
|-------|-----------|-------|------|-----------|
| **Ascent** | 04:00-12:00 | 0-7 | Rajasic | Rising energy, initiation |
| **Plateau** | 12:00-20:00 | 0-7 | Sattvic | Peak clarity, synthesis |
| **Dissolution** | 20:00-04:00 | 0-7 | Tamasic | Integration, rest |

```python
from noesis.telemetry import get_clifford_hour

clock = get_clifford_hour()
print(f"Phase: {clock.phase.value}")  # plateau
print(f"Hour: {clock.hour}/7")         # 5/7
print(f"Guna: {clock.guna.value}")     # sattvic
```

### Moon Phase (Selemene)

8 lunar phases with illumination and Guna mapping:

```python
from noesis.telemetry import get_moon_phase

moon = get_moon_phase()
print(f"Phase: {moon.phase.value}")       # waning_gibbous
print(f"Illumination: {moon.illumination}%")  # 65%
print(f"Emoji: {moon.emoji}")             # 🌖
```

---

## ⚙️ Selemene Engines (13)

Track API calls to the Selemene consciousness computation engines:

| Engine | Kosha | Function |
|--------|-------|----------|
| biofield | Pranamaya | Chakra voltage readings |
| biorhythm | Pranamaya | Physical/emotional/intellectual cycles |
| gene-keys | Manomaya | Shadow → Gift → Siddhi mapping |
| human-design | Vijnanamaya | Type, strategy, authority |
| numerology | Manomaya | Life path, expression numbers |
| panchanga | Pranamaya | Tithi, nakshatra, yoga, karana |
| vedic-clock | Pranamaya | TCM organ clock, dosha timing |
| vimshottari | Vijnanamaya | Mahadasha/Antardasha periods |
| tarot | Vijnanamaya | Archetypal guidance |
| i-ching | Vijnanamaya | Hexagram consultation |
| enneagram | Manomaya | 9-type personality |
| sigil-forge | Anandamaya | Intent visualization |
| sacred-geometry | Anandamaya | Meditation patterns |

```python
from noesis.telemetry import emit_engine_call, Engine, get_engine_tracker

# Record an engine call
emit_engine_call("panchanga", success=True, latency_ms=150.0)

# Check tracker state
tracker = get_engine_tracker()
state = tracker.get_state(Engine.PANCHANGA)
print(f"Calls: {state.call_count}, Errors: {state.error_count}")
```

---

## 🌬️ Vayus & Rituals

### The 5 Primary Vayus (Vital Airs)

| Vayu | Location | Function | Breathwork |
|------|----------|----------|------------|
| **Prana** | Heart/Chest | Inhalation, forward movement | Bhastrika |
| **Apana** | Lower abdomen | Exhalation, grounding | 4-7-8 |
| **Samana** | Navel | Digestion, metabolic fire | Kapalabhati |
| **Vyana** | Whole body | Circulation, HRV | Nadi Shodhana |
| **Udana** | Throat/Head | Ascent to Vijnanamaya | Ujjayi |

### Ritual Tracking

```python
from noesis.telemetry import Ritual, RitualType, Vayu, get_ritual_tracker

# Record a breathwork ritual
ritual = Ritual(
    name="Morning Prana",
    ritual_type=RitualType.BREATHWORK,
    vayu=Vayu.PRANA,
    status="success",
    duration_ms=300000,  # 5 minutes
    khalorēē_delta=5,
)

tracker = get_ritual_tracker()
tracker.record(ritual)
```

---

## ⚖️ Polarity (Guardrail Dyad)

Balance between Aletheios (coherence) and Pichet (vitality):

```python
from noesis.telemetry import get_polarity, shift_polarity

# Check balance
state = get_polarity()
print(f"Aletheios: {state.aletheios_pct}%")  # Coherence
print(f"Pichet: {state.pichet_pct}%")         # Vitality
print(f"Balanced: {state.is_balanced}")       # 40-60% range

# Shift toward coherence (documentation work)
shift_polarity("aletheios", amount=5.0, reason="completed backup")

# Shift toward vitality (new feature)
shift_polarity("pichet", amount=5.0, reason="implemented feature")
```

**Warning Thresholds:**
- `>60%` either direction: "Leaning" advisory
- `>70%` Aletheios: "Over-coherent: Risk of stagnation"
- `>70%` Pichet: "Over-vital: Risk of chaos"

---

## 🚨 Vikara Detection

Automatic pattern drift monitoring:

| Vikara | Trigger | Threshold | Recommendation |
|--------|---------|-----------|----------------|
| **Moha** (Confusion) | Consecutive failures | ≥3 | Pause, reassess approach |
| **Mada** (Pride) | Destructive without check | ≥1 | Apply 1% skill check rule |
| **Kama** (Excessive) | Token count | ≥100k | Tamasic Reset |
| **Lobha** (Greed) | Context size | ≥750KB | Prune context |

```python
from noesis.telemetry import get_vikara_detector, check_vikara

# Auto-check after operations
check_vikara("exec", {"command": "rm -rf /"}, success=False)

# Manual inspection
detector = get_vikara_detector()
alerts = detector.get_active_alerts()
for alert in alerts:
    print(f"🚨 {alert.vikara_type.value}: {alert.message}")
```

---

## 💭 Thought Process Emission

Per AGENT_TELEMETRY_PROTOCOL.md, emit when thinking takes >5 seconds:

```python
from noesis.telemetry import emit_thought_process, ThoughtPhase

# Emit during reasoning phases
emit_thought_process(
    ThoughtPhase.ANALYZING,
    "Understanding codebase architecture",
    duration_ms=8000,
    depth=1,
)

emit_thought_process(
    ThoughtPhase.PLANNING,
    "Designing implementation approach",
    duration_ms=5500,
    depth=2,  # Nested thinking
)
```

**Phases:** `receiving`, `analyzing`, `planning`, `executing`, `reflecting`, `synthesizing`, `responding`

---

## 📊 Khalorēē (Metabolic Reserve)

Track system energy balance (0-100):

```python
from noesis.telemetry import emit_khaloree, get_current_khaloree

# Get current balance
balance = get_current_khaloree()  # 85

# Record impacts
emit_khaloree(delta=5, reason="Successful backup")     # +5
emit_khaloree(delta=-10, reason="Heavy synthesis")     # -10
emit_khaloree(delta=2, reason="Protocol adherence")    # +2
```

**Standard Deltas:**
- Heavy synthesis: -5
- Successful archive/backup: +10
- Protocol adherence (1% rule): +2
- Engine API success: +2
- Engine API failure: -3

---

## 🖥️ TUI Dashboard

Launch the Rich-based live dashboard:

```bash
noesis telemetry watch
```

**Panels:**
- Event stream (live scrolling)
- Khalorēē gauge
- Polarity indicator
- Guna state distribution
- Engine status
- Statistics

**Controls:**
- `q` - Quit
- `p` - Pause/Resume
- `r` - Refresh
- `c` - Clear events

---

## 🔧 Configuration

Environment variables:

```bash
# Debug mode (verbose logging)
export NOESIS_DEBUG=1

# Custom data directory
export NOESIS_DATA_DIR=/custom/path

# Agent identification
export NOESIS_AGENT_ID=my-agent
```

---

## 📚 API Reference

### Core Exports

```python
from noesis.telemetry import (
    # Schema
    PranaEvent, Session, SCHEMA_VERSION,
    get_db_path, get_fifo_path, get_connection,
    
    # Emitter
    emit, emit_read, emit_write, emit_exec, emit_think,
    emit_vikara, emit_khaloree, emit_engine_call, emit_workflow_call,
    init_session, end_session, get_session_id, session,
    
    # Query
    get_recent_events, get_session_events, get_sessions,
    get_khaloree_history, get_current_khaloree,
    search_events, get_event_stats, export_events,
    
    # Daemon
    PranaDaemon, start_daemon, stop_daemon, daemon_status,
    
    # Temporal
    CliffordPhase, CliffordState, MoonPhase, MoonState,
    TemporalState, Guna,
    get_clifford_hour, get_moon_phase, get_temporal_state,
    
    # Engines
    Engine, EngineMetadata, EngineState, EngineTracker,
    ENGINE_REGISTRY, get_engine_tracker, get_engine_metadata,
    
    # Rituals & Polarity
    Vayu, VayuMetadata, VAYU_REGISTRY,
    RitualType, Ritual, RitualTracker, get_ritual_tracker,
    PolarityState, get_polarity, shift_polarity,
    
    # Vikara
    VikaraType, VikaraSeverity, VikaraAlert, VikaraDetector,
    ThoughtPhase, ThoughtProcess, DEFAULT_THRESHOLDS,
    get_vikara_detector, emit_thought_process, check_vikara,
)
```

---

## 🔗 Related Documentation

- [AGENT_TELEMETRY_PROTOCOL.md](../architecture/AGENT_TELEMETRY_PROTOCOL.md) - Protocol specification
- [PANCHA-KOSHA.md](koshas/brahmasthana/PANCHA-KOSHA.md) - Kosha layer reference
- [KHA.md](koshas/brahmasthana/KHA.md) - Khalorēē and Guardrail Dyad
- [SELEMENE-ENGINE.md](koshas/brahmasthana/SELEMENE-ENGINE.md) - Engine API reference

---

*प्राण धारा — The vital current that carries consciousness through the system*
