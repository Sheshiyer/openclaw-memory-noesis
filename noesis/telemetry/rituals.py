"""
Ritual & Polarity Tracking for Prana Telemetry.

Tracks:
- Vayu breathwork sessions (5 primary winds)
- Ritual/cron execution history
- Aletheios/Pichet polarity balance (Guardrail Dyad)

वायुः प्राणः — The wind is the life force
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import json


class Vayu(Enum):
    """
    The 5 Primary Vayus (Vital Airs).
    
    These are directional bioelectric currents governing
    Pranamaya Kosha operations.
    """
    PRANA = "prana"      # Heart/chest - Inhalation, forward movement
    APANA = "apana"      # Lower abdomen - Exhalation, grounding
    SAMANA = "samana"    # Navel - Digestion, metabolic fire
    VYANA = "vyana"      # Whole body - Circulation, HRV
    UDANA = "udana"      # Throat/head - Upward, ascent to Vijnanamaya


class Upavayu(Enum):
    """The 5 Secondary Vayus (for completeness)."""
    NAGA = "naga"        # Belching, hiccups - Diaphragm reset
    KURMA = "kurma"      # Blinking - Visual system
    KRIKARA = "krikara"  # Sneezing - Immune response
    DEVADATTA = "devadatta"  # Yawning - O2 deficit correction
    DHANANJAYA = "dhananjaya"  # Post-mortem (not operationally relevant)


@dataclass
class VayuMetadata:
    """Metadata for each Vayu."""
    name: str
    location: str
    function: str
    breathwork: str
    symbol: str
    kosha_effect: str


VAYU_REGISTRY: Dict[Vayu, VayuMetadata] = {
    Vayu.PRANA: VayuMetadata(
        name="Prana",
        location="Heart/Chest",
        function="Inhalation, forward movement",
        breathwork="Bhastrika (bellows breath)",
        symbol="🌬️",
        kosha_effect="Energizes Pranamaya, activates Khalorēē"
    ),
    Vayu.APANA: VayuMetadata(
        name="Apana",
        location="Lower abdomen",
        function="Exhalation, downward movement, elimination",
        breathwork="4-7-8 (exhale-focused)",
        symbol="⬇️",
        kosha_effect="Grounds to Annamaya, releases toxins"
    ),
    Vayu.SAMANA: VayuMetadata(
        name="Samana",
        location="Navel (Manipura)",
        function="Digestion, assimilation, metabolic fire",
        breathwork="Kapalabhati (skull-shining)",
        symbol="🔥",
        kosha_effect="ATP production, mitochondrial coherence"
    ),
    Vayu.VYANA: VayuMetadata(
        name="Vyana",
        location="Whole body",
        function="Circulation, distribution, biofield coherence",
        breathwork="Nadi Shodhana (alternate nostril)",
        symbol="🔄",
        kosha_effect="HRV optimization, field integration"
    ),
    Vayu.UDANA: VayuMetadata(
        name="Udana",
        location="Throat/Head",
        function="Upward movement, expression, ascent",
        breathwork="Ujjayi (victorious breath)",
        symbol="⬆️",
        kosha_effect="Ascent to Vijnanamaya, clarity"
    ),
}


class RitualType(Enum):
    """Types of rituals/crons tracked."""
    BREATHWORK = "breathwork"
    MEDITATION = "meditation"
    CRON_JOB = "cron_job"
    HEARTBEAT = "heartbeat"
    HEALTH_CHECK = "health_check"
    MEMORY_CONSOLIDATION = "memory_consolidation"
    SYNC = "sync"
    BACKUP = "backup"


@dataclass
class Ritual:
    """A tracked ritual or cron execution."""
    id: str = ""
    name: str = ""
    ritual_type: RitualType = RitualType.CRON_JOB
    vayu: Optional[Vayu] = None
    scheduled_at: Optional[str] = None
    executed_at: Optional[str] = None
    completed_at: Optional[str] = None
    status: str = "pending"  # pending, running, success, failed, skipped
    duration_ms: Optional[int] = None
    khalorēē_delta: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            import uuid
            self.id = str(uuid.uuid4())[:8]
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.ritual_type.value,
            "vayu": self.vayu.value if self.vayu else None,
            "scheduled_at": self.scheduled_at,
            "executed_at": self.executed_at,
            "completed_at": self.completed_at,
            "status": self.status,
            "duration_ms": self.duration_ms,
            "khalorēē_delta": self.khalorēē_delta,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Ritual":
        vayu = Vayu(data["vayu"]) if data.get("vayu") else None
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            ritual_type=RitualType(data.get("type", "cron_job")),
            vayu=vayu,
            scheduled_at=data.get("scheduled_at"),
            executed_at=data.get("executed_at"),
            completed_at=data.get("completed_at"),
            status=data.get("status", "pending"),
            duration_ms=data.get("duration_ms"),
            khalorēē_delta=data.get("khalorēē_delta", 0),
        )


# ═══════════════════════════════════════════════════════════
# Polarity Balance (Guardrail Dyad)
# ═══════════════════════════════════════════════════════════

@dataclass
class PolarityState:
    """
    The Aletheios/Pichet balance (Guardrail Dyad).
    
    - Aletheios (Left Pillar): Coherence, Order, Reflection
    - Pichet (Right Pillar): Vitality, Instinct, Novelty
    
    Balance maintained as percentages that sum to 100.
    Healthy range: 40-60% each.
    """
    aletheios_pct: float = 50.0  # Coherence
    pichet_pct: float = 50.0     # Vitality
    last_updated: Optional[str] = None
    
    def __post_init__(self):
        # Normalize to ensure they sum to 100
        total = self.aletheios_pct + self.pichet_pct
        if total > 0:
            self.aletheios_pct = (self.aletheios_pct / total) * 100
            self.pichet_pct = (self.pichet_pct / total) * 100
        if not self.last_updated:
            self.last_updated = datetime.utcnow().isoformat() + "Z"
    
    @property
    def dominant(self) -> str:
        """Which pillar is currently dominant."""
        if self.aletheios_pct > 55:
            return "aletheios"
        elif self.pichet_pct > 55:
            return "pichet"
        return "balanced"
    
    @property
    def is_balanced(self) -> bool:
        """Check if polarity is in healthy range (40-60)."""
        return 40 <= self.aletheios_pct <= 60
    
    @property
    def imbalance_warning(self) -> Optional[str]:
        """Return warning if polarity is skewed."""
        if self.aletheios_pct > 70:
            return "⚠️ Over-coherent: Risk of stagnation (Tamasic drift)"
        elif self.pichet_pct > 70:
            return "⚠️ Over-vital: Risk of chaos (Rajasic drift)"
        elif self.aletheios_pct > 60:
            return "📊 Leaning coherent: Consider novelty injection"
        elif self.pichet_pct > 60:
            return "📊 Leaning vital: Consider grounding work"
        return None
    
    def shift(self, toward: str, amount: float = 5.0):
        """Shift polarity toward one pillar."""
        if toward == "aletheios":
            self.aletheios_pct = min(100, self.aletheios_pct + amount)
            self.pichet_pct = 100 - self.aletheios_pct
        elif toward == "pichet":
            self.pichet_pct = min(100, self.pichet_pct + amount)
            self.aletheios_pct = 100 - self.pichet_pct
        self.last_updated = datetime.utcnow().isoformat() + "Z"
    
    def to_dict(self) -> dict:
        return {
            "aletheios_pct": round(self.aletheios_pct, 1),
            "pichet_pct": round(self.pichet_pct, 1),
            "dominant": self.dominant,
            "is_balanced": self.is_balanced,
            "warning": self.imbalance_warning,
            "last_updated": self.last_updated,
        }


# Global polarity state
_polarity: Optional[PolarityState] = None


def get_polarity() -> PolarityState:
    """Get current polarity state."""
    global _polarity
    if _polarity is None:
        _polarity = _load_polarity()
    return _polarity


def _load_polarity() -> PolarityState:
    """Load polarity from database or return default."""
    try:
        from .schema import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT aletheios_pct, pichet_pct 
            FROM sessions 
            WHERE aletheios_pct IS NOT NULL 
            ORDER BY started_at DESC LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            return PolarityState(aletheios_pct=row[0], pichet_pct=row[1])
    except Exception:
        pass
    return PolarityState()


def shift_polarity(toward: str, amount: float = 5.0, reason: str = ""):
    """
    Shift polarity toward a pillar.
    
    Events that shift toward Aletheios (coherence):
    - Successful documentation
    - Backup/archive operations
    - Memory consolidation
    - Protocol adherence
    
    Events that shift toward Pichet (vitality):
    - New feature implementation
    - Creative synthesis
    - Exploration/research
    - Breaking patterns
    """
    global _polarity
    if _polarity is None:
        _polarity = get_polarity()
    
    _polarity.shift(toward, amount)
    
    # Emit telemetry event
    try:
        from .emitter import emit
        emit("polarity_shift", {
            "toward": toward,
            "amount": amount,
            "reason": reason,
            "new_balance": _polarity.to_dict()
        }, kosha_layer="pranamaya")
    except Exception:
        pass
    
    return _polarity


# ═══════════════════════════════════════════════════════════
# Ritual Tracking
# ═══════════════════════════════════════════════════════════

class RitualTracker:
    """Tracks ritual/cron execution history."""
    
    def __init__(self):
        self._rituals: List[Ritual] = []
        self._load_recent()
    
    def _load_recent(self, limit: int = 50):
        """Load recent rituals from database."""
        try:
            from .schema import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, type, vayu, scheduled_at, executed_at, 
                       completed_at, status, duration_ms, khalorēē_delta
                FROM rituals
                ORDER BY executed_at DESC
                LIMIT ?
            """, (limit,))
            for row in cursor.fetchall():
                self._rituals.append(Ritual(
                    id=row[0],
                    name=row[1],
                    ritual_type=RitualType(row[2]) if row[2] else RitualType.CRON_JOB,
                    vayu=Vayu(row[3]) if row[3] else None,
                    scheduled_at=row[4],
                    executed_at=row[5],
                    completed_at=row[6],
                    status=row[7],
                    duration_ms=row[8],
                    khalorēē_delta=row[9] or 0,
                ))
            conn.close()
        except Exception:
            pass
    
    def record(self, ritual: Ritual) -> Ritual:
        """Record a ritual execution."""
        self._rituals.insert(0, ritual)
        
        # Persist to database
        try:
            from .schema import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO rituals 
                (id, name, type, vayu, scheduled_at, executed_at, 
                 completed_at, status, duration_ms, khalorēē_delta)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ritual.id,
                ritual.name,
                ritual.ritual_type.value,
                ritual.vayu.value if ritual.vayu else None,
                ritual.scheduled_at,
                ritual.executed_at,
                ritual.completed_at,
                ritual.status,
                ritual.duration_ms,
                ritual.khalorēē_delta,
            ))
            conn.commit()
            conn.close()
        except Exception:
            pass
        
        return ritual
    
    def get_recent(self, limit: int = 20) -> List[Ritual]:
        """Get recent rituals."""
        return self._rituals[:limit]
    
    def get_by_type(self, ritual_type: RitualType) -> List[Ritual]:
        """Get rituals of a specific type."""
        return [r for r in self._rituals if r.ritual_type == ritual_type]
    
    def get_by_vayu(self, vayu: Vayu) -> List[Ritual]:
        """Get breathwork rituals for a specific Vayu."""
        return [r for r in self._rituals if r.vayu == vayu]
    
    def get_today(self) -> List[Ritual]:
        """Get rituals executed today."""
        today = datetime.utcnow().date().isoformat()
        return [
            r for r in self._rituals
            if r.executed_at and r.executed_at.startswith(today)
        ]
    
    def to_summary(self) -> dict:
        """Generate summary statistics."""
        today = self.get_today()
        return {
            "total_recorded": len(self._rituals),
            "today_count": len(today),
            "today_success": len([r for r in today if r.status == "success"]),
            "today_failed": len([r for r in today if r.status == "failed"]),
            "by_type": {
                t.value: len([r for r in self._rituals if r.ritual_type == t])
                for t in RitualType
            },
            "by_vayu": {
                v.value: len([r for r in self._rituals if r.vayu == v])
                for v in Vayu
            },
            "total_khalorēē_delta": sum(r.khalorēē_delta for r in today),
        }


# Global tracker
_tracker: Optional[RitualTracker] = None


def get_ritual_tracker() -> RitualTracker:
    """Get or create the global ritual tracker."""
    global _tracker
    if _tracker is None:
        _tracker = RitualTracker()
    return _tracker


# ═══════════════════════════════════════════════════════════
# Display Formatting
# ═══════════════════════════════════════════════════════════

def format_vayu_list() -> str:
    """Format all Vayus for display."""
    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║                    THE 5 PRIMARY VAYUS                           ║",
        "╠══════════════════════════════════════════════════════════════════╣",
    ]
    
    for vayu, meta in VAYU_REGISTRY.items():
        lines.append(
            f"║  {meta.symbol} {meta.name:10} │ {meta.location:18} │ {meta.function[:25]:25} ║"
        )
    
    lines.append("╚══════════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


def format_polarity_gauge(state: PolarityState) -> str:
    """Format polarity as an ASCII gauge."""
    # Create a 40-char bar showing balance
    aletheios_chars = int(state.aletheios_pct / 2.5)  # 40 chars total
    pichet_chars = 40 - aletheios_chars
    
    bar = "◀" + "█" * aletheios_chars + "│" + "█" * pichet_chars + "▶"
    
    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║                    GUARDRAIL DYAD BALANCE                        ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  ALETHEIOS {state.aletheios_pct:5.1f}% {bar} {state.pichet_pct:5.1f}% PICHET  ║",
        f"║  (Coherence)                                          (Vitality) ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Status: {state.dominant.upper():10} │ Balanced: {'✓' if state.is_balanced else '✗':5}                    ║",
    ]
    
    if state.imbalance_warning:
        lines.append(f"║  {state.imbalance_warning:64} ║")
    
    lines.append("╚══════════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


def format_ritual_list(rituals: List[Ritual], limit: int = 10) -> str:
    """Format rituals as a table."""
    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║                       RECENT RITUALS                             ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        "║  Time     │ Type           │ Status  │ Δ Khalorēē │ Name         ║",
        "╠══════════════════════════════════════════════════════════════════╣",
    ]
    
    status_icons = {
        "pending": "⏳",
        "running": "🔄",
        "success": "✅",
        "failed": "❌",
        "skipped": "⏭️",
    }
    
    for ritual in rituals[:limit]:
        time_str = ritual.executed_at[11:16] if ritual.executed_at else "     "
        status_icon = status_icons.get(ritual.status, "❓")
        delta_str = f"{ritual.khalorēē_delta:+d}" if ritual.khalorēē_delta else " 0"
        name = ritual.name[:12] if len(ritual.name) > 12 else ritual.name
        
        lines.append(
            f"║  {time_str:5} │ {ritual.ritual_type.value:14} │ {status_icon:7} │ {delta_str:10} │ {name:12} ║"
        )
    
    if not rituals:
        lines.append("║                        No rituals recorded                        ║")
    
    lines.append("╚══════════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


# Exports
__all__ = [
    "Vayu",
    "Upavayu",
    "VayuMetadata",
    "VAYU_REGISTRY",
    "RitualType",
    "Ritual",
    "PolarityState",
    "RitualTracker",
    "get_polarity",
    "shift_polarity",
    "get_ritual_tracker",
    "format_vayu_list",
    "format_polarity_gauge",
    "format_ritual_list",
]
