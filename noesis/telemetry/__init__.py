"""
Prana Stream - Telemetry for Tryambakam Noesis
प्राण धारा — The vital current that carries consciousness through the system

This module provides:
- Event emission (SQLite + FIFO dual-write)
- Query interface for analysis
- Background daemon for real-time streaming
- Rich TUI for visualization
- Clifford Clock (8-hour consciousness octave)
- Moon phase tracking (Selemene integration)

Usage:
    from noesis.telemetry import emit, session, get_clifford_hour, get_moon_phase
    
    # Start a session
    with session(agent_id="chitta-weaver"):
        emit("read", {"path": "SOUL.md"}, kosha_layer="manomaya")
        emit("think", {"topic": "Architecture"}, kosha_layer="vijnanamaya")
    
    # Check temporal state
    clock = get_clifford_hour()
    print(f"Hour {clock.hour}/7 ({clock.phase.value})")

CLI:
    noesis telemetry start   # Start background daemon
    noesis telemetry watch   # Live TUI dashboard
    noesis telemetry query   # Query events
    noesis telemetry export  # Export data
    noesis clock             # Show Clifford Clock
    noesis moon              # Show moon phase
"""

from .schema import (
    PranaEvent,
    Session,
    get_db_path,
    get_fifo_path,
    get_pid_path,
    get_connection,
    SCHEMA_VERSION,
)

from .emitter import (
    emit,
    emit_read,
    emit_write,
    emit_exec,
    emit_think,
    emit_vikara,
    emit_khaloree,
    emit_engine_call,
    emit_workflow_call,
    init_session,
    end_session,
    get_session_id,
    session,
)

from .query import (
    get_recent_events,
    get_session_events,
    get_sessions,
    get_khaloree_history,
    get_current_khaloree,
    search_events,
    get_event_stats,
    export_events,
)

from .daemon import (
    PranaDaemon,
    start_daemon,
    stop_daemon,
    daemon_status,
)

from .temporal import (
    CliffordPhase,
    CliffordState,
    MoonPhase,
    MoonState,
    TemporalState,
    Guna,
    get_clifford_hour,
    get_moon_phase,
    get_temporal_state,
    format_clifford_clock,
    format_moon_phase,
)

from .engines import (
    Engine,
    EngineMetadata,
    EngineState,
    EngineTracker,
    ENGINE_REGISTRY,
    get_engine_tracker,
    get_engine_metadata,
    list_engines_by_kosha,
    format_engine_status,
    format_engine_dashboard,
)

__all__ = [
    # Schema
    "PranaEvent",
    "Session",
    "get_db_path",
    "get_fifo_path",
    "get_pid_path",
    "get_connection",
    "SCHEMA_VERSION",
    
    # Emitter
    "emit",
    "emit_read",
    "emit_write",
    "emit_exec",
    "emit_think",
    "emit_vikara",
    "emit_khaloree",
    "emit_engine_call",
    "emit_workflow_call",
    "init_session",
    "end_session",
    "get_session_id",
    "session",
    
    # Query
    "get_recent_events",
    "get_session_events",
    "get_sessions",
    "get_khaloree_history",
    "get_current_khaloree",
    "search_events",
    "get_event_stats",
    "export_events",
    
    # Daemon
    "PranaDaemon",
    "start_daemon",
    "stop_daemon",
    "daemon_status",
    
    # Temporal
    "CliffordPhase",
    "CliffordState",
    "MoonPhase",
    "MoonState",
    "TemporalState",
    "Guna",
    "get_clifford_hour",
    "get_moon_phase",
    "get_temporal_state",
    "format_clifford_clock",
    "format_moon_phase",
    
    # Engines
    "Engine",
    "EngineMetadata",
    "EngineState",
    "EngineTracker",
    "ENGINE_REGISTRY",
    "get_engine_tracker",
    "get_engine_metadata",
    "list_engines_by_kosha",
    "format_engine_status",
    "format_engine_dashboard",
]
