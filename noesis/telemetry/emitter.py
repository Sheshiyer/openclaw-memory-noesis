"""
Prana Stream - Event Emitter
प्राण प्रसारक — The broadcaster of vital signals

Emits telemetry events to SQLite (persistent) and FIFO (real-time).
Designed for agent-side use with graceful fallbacks.
"""

import os
import json
import stat
from pathlib import Path
from typing import Optional, Dict, Any
from contextlib import contextmanager
from datetime import datetime
import uuid

from .schema import (
    PranaEvent, Session,
    get_connection, get_fifo_path, get_db_path,
    insert_event, insert_session, update_khaloree
)


# Global session state
_current_session: Optional[Session] = None
_current_agent_id: Optional[str] = None


def init_session(agent_id: Optional[str] = None, metadata: Optional[Dict] = None) -> Session:
    """Initialize a new telemetry session."""
    global _current_session, _current_agent_id
    
    _current_agent_id = agent_id or os.environ.get("NOESIS_AGENT_ID")
    _current_session = Session(
        agent_id=_current_agent_id,
        metadata=metadata or {}
    )
    
    # Persist to database
    try:
        conn = get_connection()
        insert_session(conn, _current_session)
        conn.close()
    except Exception as e:
        # Non-fatal: continue without persistence
        pass
    
    # Emit session start event
    emit("session.start", {
        "session_id": _current_session.id,
        "agent_id": _current_agent_id
    })
    
    return _current_session


def end_session() -> None:
    """End the current telemetry session."""
    global _current_session
    
    if _current_session is None:
        return
    
    _current_session.ended_at = datetime.utcnow().isoformat() + "Z"
    
    # Emit session end event
    emit("session.end", {
        "session_id": _current_session.id,
        "duration_events": "calculated_at_query_time"
    })
    
    # Update session in database
    try:
        conn = get_connection()
        insert_session(conn, _current_session)
        conn.close()
    except Exception:
        pass
    
    _current_session = None


def get_session_id() -> Optional[str]:
    """Get current session ID."""
    return _current_session.id if _current_session else None


def emit(
    event_type: str,
    payload: Optional[Dict[str, Any]] = None,
    kosha_layer: str = "annamaya",
    guna_state: str = "sattvic",
    khalorēē_delta: int = 0,
    agent_id: Optional[str] = None
) -> PranaEvent:
    """
    Emit a telemetry event.
    
    Args:
        event_type: Type of event (read, write, exec, think, vikara, etc.)
        payload: Event-specific data
        kosha_layer: Which kosha this event relates to
        guna_state: Current guna (sattvic, rajasic, tamasic)
        khalorēē_delta: Points to add/subtract from balance
        agent_id: Override agent ID for this event
    
    Returns:
        The created PranaEvent
    """
    event = PranaEvent(
        event_type=event_type,
        payload=payload or {},
        kosha_layer=kosha_layer,
        guna_state=guna_state,
        khalorēē_delta=khalorēē_delta,
        agent_id=agent_id or _current_agent_id,
        session_id=get_session_id()
    )
    
    # Write to SQLite (persistent)
    _write_to_sqlite(event)
    
    # Write to FIFO (real-time)
    _write_to_fifo(event)
    
    # Update khalorēē if delta
    if khalorēē_delta != 0:
        _update_khaloree(khalorēē_delta, f"{event_type}: {payload.get('reason', 'auto')}")
    
    return event


def _write_to_sqlite(event: PranaEvent) -> bool:
    """Write event to SQLite database."""
    try:
        conn = get_connection()
        insert_event(conn, event)
        conn.close()
        return True
    except Exception as e:
        # Log but don't fail
        if os.environ.get("NOESIS_DEBUG"):
            print(f"[prana] SQLite write failed: {e}")
        return False


def _write_to_fifo(event: PranaEvent) -> bool:
    """Write event to named pipe for real-time streaming."""
    fifo_path = get_fifo_path()
    
    # Check if FIFO exists and is a pipe
    if not fifo_path.exists():
        return False
    
    try:
        if not stat.S_ISFIFO(fifo_path.stat().st_mode):
            return False
    except Exception:
        return False
    
    try:
        # Open in non-blocking mode to avoid hanging if no reader
        fd = os.open(str(fifo_path), os.O_WRONLY | os.O_NONBLOCK)
        try:
            data = event.to_json() + "\n"
            os.write(fd, data.encode('utf-8'))
            return True
        finally:
            os.close(fd)
    except (OSError, BrokenPipeError):
        # No reader connected - that's fine
        return False
    except Exception as e:
        if os.environ.get("NOESIS_DEBUG"):
            print(f"[prana] FIFO write failed: {e}")
        return False


def _update_khaloree(delta: int, reason: str) -> None:
    """Update khalorēē balance."""
    try:
        conn = get_connection()
        update_khaloree(conn, delta, reason, get_session_id())
        conn.close()
    except Exception:
        pass


# Convenience emitters for common event types

def emit_read(path: str, kosha: str = "manomaya") -> PranaEvent:
    """Emit a file read event."""
    return emit("read", {"path": path}, kosha_layer=kosha, guna_state="sattvic")


def emit_write(path: str, kosha: str = "annamaya") -> PranaEvent:
    """Emit a file write event."""
    return emit("write", {"path": path}, kosha_layer=kosha, guna_state="rajasic")


def emit_exec(command: str, exit_code: int = 0) -> PranaEvent:
    """Emit a command execution event."""
    guna = "sattvic" if exit_code == 0 else "tamasic"
    return emit("exec", {"command": command, "exit_code": exit_code}, 
                kosha_layer="annamaya", guna_state=guna)


def emit_think(topic: str, duration_ms: Optional[int] = None) -> PranaEvent:
    """Emit a thinking/reasoning event."""
    payload = {"topic": topic}
    if duration_ms:
        payload["duration_ms"] = duration_ms
    return emit("think", payload, kosha_layer="vijnanamaya", guna_state="sattvic")


def emit_vikara(vikara_type: str, details: Dict[str, Any]) -> PranaEvent:
    """Emit a drift/distortion detection event."""
    return emit("vikara", {"type": vikara_type, **details}, 
                kosha_layer="pranamaya", guna_state="tamasic", khalorēē_delta=-5)


def emit_khaloree(delta: int, reason: str) -> PranaEvent:
    """Emit a khalorēē adjustment event."""
    return emit("khalorēē", {"delta": delta, "reason": reason},
                kosha_layer="pranamaya", khalorēē_delta=delta)


@contextmanager
def session(agent_id: Optional[str] = None, metadata: Optional[Dict] = None):
    """Context manager for a telemetry session."""
    init_session(agent_id, metadata)
    try:
        yield _current_session
    finally:
        end_session()


if __name__ == "__main__":
    # Test emitter
    print("Testing Prana Emitter...")
    
    with session(agent_id="test-agent"):
        emit_read("/path/to/SOUL.md", kosha="manomaya")
        emit_write("/path/to/output.md", kosha="annamaya")
        emit_exec("git status", exit_code=0)
        emit_think("Analyzing architecture", duration_ms=1500)
        emit_vikara("MEMORY_OVERFLOW", {"lines": 600, "threshold": 500})
        emit_khaloree(5, "Completed health check")
    
    print("✓ Emitter test passed")
