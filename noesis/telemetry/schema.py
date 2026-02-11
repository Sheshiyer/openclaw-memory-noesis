"""
Prana Stream - SQLite Schema
प्राण धारा — The vital current that carries consciousness through the system

SQLite schema for telemetry events, sessions, and khalorēē tracking.
Auto-migrates on first connection.
"""

import sqlite3
import os
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime
import json
import uuid


# Default database location
DEFAULT_DB_PATH = Path.home() / ".noesis" / "prana.db"
DEFAULT_FIFO_PATH = Path.home() / ".noesis" / "prana.fifo"
DEFAULT_PID_PATH = Path.home() / ".noesis" / "prana.pid"


SCHEMA_VERSION = 1

SCHEMA_SQL = """
-- Events table: Every telemetry event
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    session_id TEXT NOT NULL,
    agent_id TEXT,
    event_type TEXT NOT NULL,
    payload TEXT,
    kosha_layer TEXT,
    guna_state TEXT,
    khalorēē_delta INTEGER DEFAULT 0
);

-- Sessions table: Track agent sessions
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    agent_id TEXT,
    total_khalorēē INTEGER DEFAULT 0,
    metadata TEXT
);

-- Khalorēē ledger: Running balance of metabolic reserve
CREATE TABLE IF NOT EXISTS khaloree_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    session_id TEXT,
    delta INTEGER NOT NULL,
    reason TEXT,
    balance INTEGER NOT NULL
);

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_agent ON events(agent_id);
CREATE INDEX IF NOT EXISTS idx_events_kosha ON events(kosha_layer);
CREATE INDEX IF NOT EXISTS idx_sessions_agent ON sessions(agent_id);
CREATE INDEX IF NOT EXISTS idx_ledger_session ON khaloree_ledger(session_id);
"""


@dataclass
class PranaEvent:
    """A single telemetry event in the Prana Stream."""
    event_type: str
    payload: dict = field(default_factory=dict)
    kosha_layer: str = "annamaya"
    guna_state: str = "sattvic"
    khalorēē_delta: int = 0
    agent_id: Optional[str] = None
    session_id: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage/transmission."""
        d = asdict(self)
        if isinstance(d.get('payload'), dict):
            d['payload'] = json.dumps(d['payload'])
        return d
    
    @classmethod
    def from_dict(cls, d: dict) -> 'PranaEvent':
        """Create from dictionary."""
        if isinstance(d.get('payload'), str):
            try:
                d['payload'] = json.loads(d['payload'])
            except json.JSONDecodeError:
                d['payload'] = {'raw': d['payload']}
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        d = asdict(self)
        return json.dumps(d)
    
    @classmethod
    def from_json(cls, s: str) -> 'PranaEvent':
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(s))


@dataclass
class Session:
    """A telemetry session."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    ended_at: Optional[str] = None
    agent_id: Optional[str] = None
    total_khalorēē: int = 0
    metadata: dict = field(default_factory=dict)


def get_db_path() -> Path:
    """Get database path, creating directory if needed."""
    db_path = Path(os.environ.get("NOESIS_DB_PATH", DEFAULT_DB_PATH))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_fifo_path() -> Path:
    """Get FIFO path."""
    return Path(os.environ.get("NOESIS_FIFO_PATH", DEFAULT_FIFO_PATH))


def get_pid_path() -> Path:
    """Get PID file path."""
    return Path(os.environ.get("NOESIS_PID_PATH", DEFAULT_PID_PATH))


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Get a database connection, initializing schema if needed."""
    if db_path is None:
        db_path = get_db_path()
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    
    # Check if schema needs initialization
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'")
    if cursor.fetchone() is None:
        # Initialize schema
        conn.executescript(SCHEMA_SQL)
        conn.execute(
            "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)",
            (SCHEMA_VERSION, datetime.utcnow().isoformat() + "Z")
        )
        conn.commit()
    
    return conn


def insert_event(conn: sqlite3.Connection, event: PranaEvent) -> None:
    """Insert an event into the database."""
    d = event.to_dict()
    conn.execute("""
        INSERT INTO events (id, timestamp, session_id, agent_id, event_type, 
                           payload, kosha_layer, guna_state, khalorēē_delta)
        VALUES (:id, :timestamp, :session_id, :agent_id, :event_type,
                :payload, :kosha_layer, :guna_state, :khalorēē_delta)
    """, d)
    conn.commit()


def insert_session(conn: sqlite3.Connection, session: Session) -> None:
    """Insert or update a session."""
    conn.execute("""
        INSERT OR REPLACE INTO sessions (id, started_at, ended_at, agent_id, total_khalorēē, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session.id,
        session.started_at,
        session.ended_at,
        session.agent_id,
        session.total_khalorēē,
        json.dumps(session.metadata)
    ))
    conn.commit()


def update_khaloree(conn: sqlite3.Connection, delta: int, reason: str, 
                    session_id: Optional[str] = None) -> int:
    """Update khalorēē balance and return new balance."""
    cursor = conn.cursor()
    
    # Get current balance
    cursor.execute("SELECT balance FROM khaloree_ledger ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    current_balance = row['balance'] if row else 100  # Default starting balance
    
    new_balance = max(0, min(100, current_balance + delta))  # Clamp 0-100
    
    cursor.execute("""
        INSERT INTO khaloree_ledger (timestamp, session_id, delta, reason, balance)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.utcnow().isoformat() + "Z", session_id, delta, reason, new_balance))
    conn.commit()
    
    return new_balance


def get_khaloree_balance(conn: sqlite3.Connection) -> int:
    """Get current khalorēē balance."""
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM khaloree_ledger ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    return row['balance'] if row else 100


if __name__ == "__main__":
    # Test schema creation
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        test_db = Path(f.name)
    
    conn = get_connection(test_db)
    
    # Test event insertion
    event = PranaEvent(
        event_type="test",
        payload={"message": "Hello Prana"},
        kosha_layer="manomaya",
        guna_state="sattvic",
        session_id="test-session"
    )
    insert_event(conn, event)
    
    # Test khalorēē
    balance = update_khaloree(conn, -5, "test deduction", "test-session")
    print(f"Balance after -5: {balance}")
    
    balance = update_khaloree(conn, 10, "test addition", "test-session")
    print(f"Balance after +10: {balance}")
    
    # Query events
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    for row in cursor.fetchall():
        print(dict(row))
    
    conn.close()
    test_db.unlink()
    print("✓ Schema test passed")
