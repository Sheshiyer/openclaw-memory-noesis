"""
Prana Stream - Query Interface
प्राण पृच्छा — Inquiring into the vital stream

SQL query helpers for telemetry data analysis.
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json

from .schema import (
    PranaEvent, Session,
    get_connection, get_db_path, get_khaloree_balance
)


def get_recent_events(
    limit: int = 50,
    event_type: Optional[str] = None,
    agent_id: Optional[str] = None,
    kosha_layer: Optional[str] = None,
    db_path: Optional[Path] = None
) -> List[PranaEvent]:
    """Get recent events with optional filters."""
    conn = get_connection(db_path)
    
    query = "SELECT * FROM events WHERE 1=1"
    params: List[Any] = []
    
    if event_type:
        query += " AND event_type = ?"
        params.append(event_type)
    
    if agent_id:
        query += " AND agent_id = ?"
        params.append(agent_id)
    
    if kosha_layer:
        query += " AND kosha_layer = ?"
        params.append(kosha_layer)
    
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    events = [PranaEvent.from_dict(dict(row)) for row in cursor.fetchall()]
    conn.close()
    
    return events


def get_session_events(
    session_id: str,
    db_path: Optional[Path] = None
) -> List[PranaEvent]:
    """Get all events for a specific session."""
    conn = get_connection(db_path)
    
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM events WHERE session_id = ? ORDER BY timestamp ASC",
        (session_id,)
    )
    
    events = [PranaEvent.from_dict(dict(row)) for row in cursor.fetchall()]
    conn.close()
    
    return events


def get_sessions(
    limit: int = 20,
    agent_id: Optional[str] = None,
    db_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """Get recent sessions."""
    conn = get_connection(db_path)
    
    query = "SELECT * FROM sessions WHERE 1=1"
    params: List[Any] = []
    
    if agent_id:
        query += " AND agent_id = ?"
        params.append(agent_id)
    
    query += " ORDER BY started_at DESC LIMIT ?"
    params.append(limit)
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    sessions = []
    for row in cursor.fetchall():
        d = dict(row)
        if d.get('metadata'):
            try:
                d['metadata'] = json.loads(d['metadata'])
            except json.JSONDecodeError:
                pass
        sessions.append(d)
    
    conn.close()
    return sessions


def get_khaloree_history(
    limit: int = 50,
    session_id: Optional[str] = None,
    db_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """Get khalorēē ledger history."""
    conn = get_connection(db_path)
    
    query = "SELECT * FROM khaloree_ledger WHERE 1=1"
    params: List[Any] = []
    
    if session_id:
        query += " AND session_id = ?"
        params.append(session_id)
    
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    history = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return history


def get_current_khaloree(db_path: Optional[Path] = None) -> int:
    """Get current khalorēē balance."""
    conn = get_connection(db_path)
    balance = get_khaloree_balance(conn)
    conn.close()
    return balance


def search_events(
    query_text: str,
    since: Optional[str] = None,
    until: Optional[str] = None,
    limit: int = 100,
    db_path: Optional[Path] = None
) -> List[PranaEvent]:
    """
    Search events by text in payload.
    
    Args:
        query_text: Text to search for in payload
        since: ISO timestamp or relative time (e.g., "1 hour ago")
        until: ISO timestamp or relative time
        limit: Maximum results
    """
    conn = get_connection(db_path)
    
    query = "SELECT * FROM events WHERE payload LIKE ?"
    params: List[Any] = [f"%{query_text}%"]
    
    if since:
        since_ts = _parse_time(since)
        query += " AND timestamp >= ?"
        params.append(since_ts)
    
    if until:
        until_ts = _parse_time(until)
        query += " AND timestamp <= ?"
        params.append(until_ts)
    
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    events = [PranaEvent.from_dict(dict(row)) for row in cursor.fetchall()]
    conn.close()
    
    return events


def get_event_stats(
    since: Optional[str] = None,
    db_path: Optional[Path] = None
) -> Dict[str, Any]:
    """Get aggregate statistics about events."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    since_clause = ""
    params: List[Any] = []
    if since:
        since_ts = _parse_time(since)
        since_clause = " WHERE timestamp >= ?"
        params.append(since_ts)
    
    # Total events
    cursor.execute(f"SELECT COUNT(*) as count FROM events{since_clause}", params)
    total_events = cursor.fetchone()['count']
    
    # Events by type
    cursor.execute(f"""
        SELECT event_type, COUNT(*) as count 
        FROM events{since_clause}
        GROUP BY event_type
        ORDER BY count DESC
    """, params)
    by_type = {row['event_type']: row['count'] for row in cursor.fetchall()}
    
    # Events by kosha
    cursor.execute(f"""
        SELECT kosha_layer, COUNT(*) as count 
        FROM events{since_clause}
        GROUP BY kosha_layer
        ORDER BY count DESC
    """, params)
    by_kosha = {row['kosha_layer']: row['count'] for row in cursor.fetchall()}
    
    # Events by guna
    cursor.execute(f"""
        SELECT guna_state, COUNT(*) as count 
        FROM events{since_clause}
        GROUP BY guna_state
        ORDER BY count DESC
    """, params)
    by_guna = {row['guna_state']: row['count'] for row in cursor.fetchall()}
    
    # Khalorēē total delta
    cursor.execute(f"""
        SELECT COALESCE(SUM(khalorēē_delta), 0) as total_delta 
        FROM events{since_clause}
    """, params)
    khaloree_delta = cursor.fetchone()['total_delta']
    
    conn.close()
    
    return {
        "total_events": total_events,
        "by_type": by_type,
        "by_kosha": by_kosha,
        "by_guna": by_guna,
        "khaloree_delta": khaloree_delta,
        "current_khaloree": get_current_khaloree(db_path)
    }


def export_events(
    format: str = "json",
    limit: int = 1000,
    since: Optional[str] = None,
    db_path: Optional[Path] = None
) -> str:
    """Export events as JSON or CSV."""
    events = get_recent_events(limit=limit, db_path=db_path)
    
    if since:
        since_ts = _parse_time(since)
        events = [e for e in events if e.timestamp >= since_ts]
    
    if format == "json":
        return json.dumps([e.to_dict() for e in events], indent=2)
    
    elif format == "csv":
        if not events:
            return "id,timestamp,session_id,agent_id,event_type,kosha_layer,guna_state,khalorēē_delta,payload\n"
        
        lines = ["id,timestamp,session_id,agent_id,event_type,kosha_layer,guna_state,khalorēē_delta,payload"]
        for e in events:
            payload_str = json.dumps(e.payload).replace('"', '""')
            lines.append(
                f'{e.id},{e.timestamp},{e.session_id or ""},{e.agent_id or ""},'
                f'{e.event_type},{e.kosha_layer},{e.guna_state},{e.khalorēē_delta},"{payload_str}"'
            )
        return "\n".join(lines)
    
    else:
        raise ValueError(f"Unknown format: {format}")


def _parse_time(time_str: str) -> str:
    """Parse time string to ISO format."""
    # Already ISO format
    if "T" in time_str:
        return time_str
    
    # Relative time parsing
    now = datetime.utcnow()
    
    parts = time_str.lower().split()
    if len(parts) >= 2 and parts[-1] == "ago":
        amount = int(parts[0])
        unit = parts[1].rstrip('s')  # Remove trailing 's'
        
        if unit == "minute":
            delta = timedelta(minutes=amount)
        elif unit == "hour":
            delta = timedelta(hours=amount)
        elif unit == "day":
            delta = timedelta(days=amount)
        elif unit == "week":
            delta = timedelta(weeks=amount)
        else:
            raise ValueError(f"Unknown time unit: {unit}")
        
        return (now - delta).isoformat() + "Z"
    
    raise ValueError(f"Cannot parse time: {time_str}")


if __name__ == "__main__":
    # Test queries
    print("Testing Prana Query...")
    
    # These will work if there's data in the DB
    events = get_recent_events(limit=5)
    print(f"Recent events: {len(events)}")
    
    stats = get_event_stats()
    print(f"Stats: {stats}")
    
    balance = get_current_khaloree()
    print(f"Khalorēē balance: {balance}")
    
    print("✓ Query test passed")
