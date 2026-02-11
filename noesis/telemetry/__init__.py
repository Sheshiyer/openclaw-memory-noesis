"""
Prana Stream - Telemetry for Tryambakam Noesis
प्राण धारा — The vital current that carries consciousness through the system

This module provides:
- Event emission (SQLite + FIFO dual-write)
- Query interface for analysis
- Background daemon for real-time streaming
- Rich TUI for visualization

Usage:
    from noesis.telemetry import emit, session, query
    
    # Start a session
    with session(agent_id="chitta-weaver"):
        emit("read", {"path": "SOUL.md"}, kosha_layer="manomaya")
        emit("think", {"topic": "Architecture"}, kosha_layer="vijnanamaya")

CLI:
    noesis telemetry start   # Start background daemon
    noesis telemetry watch   # Live TUI dashboard
    noesis telemetry query   # Query events
    noesis telemetry export  # Export data
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
]
