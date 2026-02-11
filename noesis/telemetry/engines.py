"""
Selemene Engine State Tracking for Prana Telemetry.

The 13 engines of consciousness computation, each mapped to
a Kosha layer and operational domain.

कर्मणा मनसा वाचा — By action, mind, and speech
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List, Any
from datetime import datetime
import json


class Engine(Enum):
    """
    The 13 Selemene Engines.
    
    8 Primary (active on selemene.tryambakam.space):
    - biofield, biorhythm, gene-keys, human-design
    - numerology, panchanga, vedic-clock, vimshottari
    
    5 Extended (planned/internal):
    - tarot, i-ching, enneagram, sigil-forge, sacred-geometry
    """
    # Primary Engines (8)
    BIOFIELD = "biofield"
    BIORHYTHM = "biorhythm"
    GENE_KEYS = "gene-keys"
    HUMAN_DESIGN = "human-design"
    NUMEROLOGY = "numerology"
    PANCHANGA = "panchanga"
    VEDIC_CLOCK = "vedic-clock"
    VIMSHOTTARI = "vimshottari"
    
    # Extended Engines (5)
    TAROT = "tarot"
    I_CHING = "i-ching"
    ENNEAGRAM = "enneagram"
    SIGIL_FORGE = "sigil-forge"
    SACRED_GEOMETRY = "sacred-geometry"


@dataclass
class EngineMetadata:
    """Metadata for each Selemene engine."""
    name: str
    kosha_layer: str
    description: str
    requires_birth_data: bool = True
    requires_birth_time: bool = False
    requires_location: bool = False
    api_path: str = ""
    kernel_refs: List[str] = field(default_factory=list)
    symbol: str = "⚙️"


# Engine → Metadata mapping
ENGINE_REGISTRY: Dict[Engine, EngineMetadata] = {
    Engine.BIOFIELD: EngineMetadata(
        name="Biofield",
        kosha_layer="pranamaya",
        description="Chakra voltage readings, bioelectric field analysis",
        requires_birth_data=True,
        api_path="/api/v1/engines/biofield/calculate",
        kernel_refs=["VEDIC-LEXICON §3", "PANCHA-KOSHA"],
        symbol="🔋"
    ),
    Engine.BIORHYTHM: EngineMetadata(
        name="Biorhythm",
        kosha_layer="pranamaya",
        description="Physical/emotional/intellectual cycle tracking",
        requires_birth_data=True,
        api_path="/api/v1/engines/biorhythm/calculate",
        kernel_refs=["LHA.md §Karmic Vector"],
        symbol="📊"
    ),
    Engine.GENE_KEYS: EngineMetadata(
        name="Gene Keys",
        kosha_layer="manomaya",
        description="Shadow → Gift → Siddhi transformation mapping",
        requires_birth_data=True,
        requires_birth_time=True,
        requires_location=True,
        api_path="/api/v1/engines/gene-keys/calculate",
        kernel_refs=["BHA.md §Vikara"],
        symbol="🧬"
    ),
    Engine.HUMAN_DESIGN: EngineMetadata(
        name="Human Design",
        kosha_layer="vijnanamaya",
        description="Type, strategy, authority, profile",
        requires_birth_data=True,
        requires_birth_time=True,
        requires_location=True,
        api_path="/api/v1/engines/human-design/calculate",
        kernel_refs=["USER.md"],
        symbol="🎯"
    ),
    Engine.NUMEROLOGY: EngineMetadata(
        name="Numerology",
        kosha_layer="manomaya",
        description="Life path, expression, soul urge numbers",
        requires_birth_data=True,
        api_path="/api/v1/engines/numerology/calculate",
        kernel_refs=["aboutme/02_NUMERICAL"],
        symbol="🔢"
    ),
    Engine.PANCHANGA: EngineMetadata(
        name="Panchanga",
        kosha_layer="pranamaya",
        description="Tithi, nakshatra, yoga, karana, vara",
        requires_birth_data=True,
        requires_location=True,
        api_path="/api/v1/engines/panchanga/calculate",
        kernel_refs=["VEDIC-LEXICON §14"],
        symbol="📅"
    ),
    Engine.VEDIC_CLOCK: EngineMetadata(
        name="Vedic Clock",
        kosha_layer="pranamaya",
        description="TCM organ clock, dosha timing",
        requires_birth_data=False,  # Uses current time only
        api_path="/api/v1/engines/vedic-clock/calculate",
        kernel_refs=["KHA.md §Doshas"],
        symbol="🕐"
    ),
    Engine.VIMSHOTTARI: EngineMetadata(
        name="Vimshottari Dasha",
        kosha_layer="vijnanamaya",
        description="Mahadasha/Antardasha/Pratyantar periods",
        requires_birth_data=True,
        requires_birth_time=True,
        requires_location=True,
        api_path="/api/v1/engines/vimshottari/calculate",
        kernel_refs=["LHA.md §Dasha"],
        symbol="🌙"
    ),
    # Extended engines
    Engine.TAROT: EngineMetadata(
        name="Tarot",
        kosha_layer="vijnanamaya",
        description="Archetypal guidance through major/minor arcana",
        requires_birth_data=False,
        api_path="/api/v1/engines/tarot/draw",
        kernel_refs=["decision-support workflow"],
        symbol="🃏"
    ),
    Engine.I_CHING: EngineMetadata(
        name="I Ching",
        kosha_layer="vijnanamaya",
        description="Hexagram consultation for decision support",
        requires_birth_data=False,
        api_path="/api/v1/engines/i-ching/cast",
        kernel_refs=["decision-support workflow"],
        symbol="☯️"
    ),
    Engine.ENNEAGRAM: EngineMetadata(
        name="Enneagram",
        kosha_layer="manomaya",
        description="9-type personality mapping with wings and instincts",
        requires_birth_data=False,
        api_path="/api/v1/engines/enneagram/calculate",
        kernel_refs=["self-inquiry workflow"],
        symbol="🔯"
    ),
    Engine.SIGIL_FORGE: EngineMetadata(
        name="Sigil Forge",
        kosha_layer="anandamaya",
        description="Intent visualization and sigil generation",
        requires_birth_data=False,
        api_path="/api/v1/engines/sigil-forge/create",
        kernel_refs=["creative-expression workflow"],
        symbol="✨"
    ),
    Engine.SACRED_GEOMETRY: EngineMetadata(
        name="Sacred Geometry",
        kosha_layer="anandamaya",
        description="Geometric pattern generation for meditation",
        requires_birth_data=False,
        api_path="/api/v1/engines/sacred-geometry/generate",
        kernel_refs=["creative-expression workflow"],
        symbol="🔺"
    ),
}


@dataclass
class EngineState:
    """Current state of a Selemene engine."""
    engine: Engine
    status: str  # idle, calling, success, error, timeout
    last_called: Optional[datetime] = None
    last_result: Optional[Dict[str, Any]] = None
    call_count: int = 0
    error_count: int = 0
    avg_latency_ms: float = 0.0
    
    @property
    def metadata(self) -> EngineMetadata:
        return ENGINE_REGISTRY[self.engine]
    
    def to_dict(self) -> dict:
        return {
            "engine": self.engine.value,
            "status": self.status,
            "last_called": self.last_called.isoformat() if self.last_called else None,
            "call_count": self.call_count,
            "error_count": self.error_count,
            "avg_latency_ms": self.avg_latency_ms,
        }


class EngineTracker:
    """
    Tracks state of all 13 Selemene engines.
    
    Usage:
        tracker = EngineTracker()
        tracker.record_call(Engine.PANCHANGA, success=True, latency_ms=150)
        state = tracker.get_state(Engine.PANCHANGA)
    """
    
    def __init__(self):
        self._states: Dict[Engine, EngineState] = {
            engine: EngineState(engine=engine, status="idle")
            for engine in Engine
        }
    
    def record_call(
        self,
        engine: Engine,
        success: bool,
        latency_ms: float,
        result: Optional[Dict[str, Any]] = None
    ):
        """Record an engine API call."""
        state = self._states[engine]
        state.call_count += 1
        state.last_called = datetime.utcnow()
        
        if success:
            state.status = "success"
            state.last_result = result
        else:
            state.status = "error"
            state.error_count += 1
        
        # Rolling average latency
        if state.call_count == 1:
            state.avg_latency_ms = latency_ms
        else:
            state.avg_latency_ms = (
                state.avg_latency_ms * (state.call_count - 1) + latency_ms
            ) / state.call_count
    
    def mark_calling(self, engine: Engine):
        """Mark an engine as currently being called."""
        self._states[engine].status = "calling"
    
    def mark_timeout(self, engine: Engine):
        """Mark an engine call as timed out."""
        state = self._states[engine]
        state.status = "timeout"
        state.error_count += 1
    
    def get_state(self, engine: Engine) -> EngineState:
        """Get current state of an engine."""
        return self._states[engine]
    
    def get_all_states(self) -> List[EngineState]:
        """Get states of all engines."""
        return list(self._states.values())
    
    def get_active_engines(self) -> List[EngineState]:
        """Get engines that have been called at least once."""
        return [s for s in self._states.values() if s.call_count > 0]
    
    def get_by_kosha(self, kosha: str) -> List[EngineState]:
        """Get engines aligned with a specific kosha layer."""
        return [
            s for s in self._states.values()
            if s.metadata.kosha_layer == kosha
        ]
    
    def to_summary(self) -> dict:
        """Generate summary statistics."""
        active = self.get_active_engines()
        total_calls = sum(s.call_count for s in active)
        total_errors = sum(s.error_count for s in active)
        
        return {
            "total_engines": len(Engine),
            "active_engines": len(active),
            "total_calls": total_calls,
            "total_errors": total_errors,
            "error_rate": total_errors / total_calls if total_calls > 0 else 0,
            "engines_by_status": {
                status: len([s for s in self._states.values() if s.status == status])
                for status in ["idle", "calling", "success", "error", "timeout"]
            },
            "engines_by_kosha": {
                kosha: len(self.get_by_kosha(kosha))
                for kosha in ["annamaya", "pranamaya", "manomaya", "vijnanamaya", "anandamaya"]
            }
        }


# Global tracker instance
_tracker: Optional[EngineTracker] = None


def get_engine_tracker() -> EngineTracker:
    """Get or create the global engine tracker."""
    global _tracker
    if _tracker is None:
        _tracker = EngineTracker()
    return _tracker


def get_engine_metadata(engine: Engine) -> EngineMetadata:
    """Get metadata for an engine."""
    return ENGINE_REGISTRY[engine]


def list_engines_by_kosha(kosha: str) -> List[Engine]:
    """List all engines aligned with a kosha layer."""
    return [
        engine for engine, meta in ENGINE_REGISTRY.items()
        if meta.kosha_layer == kosha
    ]


def format_engine_status(state: EngineState, compact: bool = False) -> str:
    """Format engine state for display."""
    meta = state.metadata
    status_icons = {
        "idle": "⚪",
        "calling": "🔄",
        "success": "✅",
        "error": "❌",
        "timeout": "⏱️"
    }
    icon = status_icons.get(state.status, "❓")
    
    if compact:
        return f"{meta.symbol} {icon}"
    
    lines = [
        f"{meta.symbol} {meta.name} [{state.status.upper()}]",
        f"   Kosha: {meta.kosha_layer.capitalize()}",
        f"   Calls: {state.call_count} (errors: {state.error_count})",
    ]
    
    if state.last_called:
        lines.append(f"   Last: {state.last_called.strftime('%H:%M:%S')}")
    
    if state.avg_latency_ms > 0:
        lines.append(f"   Latency: {state.avg_latency_ms:.0f}ms avg")
    
    return "\n".join(lines)


def format_engine_dashboard() -> str:
    """Format all engines as a dashboard view."""
    tracker = get_engine_tracker()
    summary = tracker.to_summary()
    
    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║                    SELEMENE ENGINE DASHBOARD                     ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  Active: {summary['active_engines']}/{summary['total_engines']}  │  "
        f"Calls: {summary['total_calls']}  │  "
        f"Errors: {summary['total_errors']}  │  "
        f"Rate: {summary['error_rate']:.1%}    ║",
        "╠══════════════════════════════════════════════════════════════════╣",
    ]
    
    # Group by kosha
    kosha_order = ["pranamaya", "manomaya", "vijnanamaya", "anandamaya"]
    
    for kosha in kosha_order:
        engines = tracker.get_by_kosha(kosha)
        if not engines:
            continue
        
        kosha_label = kosha.upper()
        engine_str = " ".join(format_engine_status(e, compact=True) for e in engines)
        lines.append(f"║  {kosha_label:12} │ {engine_str:50} ║")
    
    lines.append("╚══════════════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)


# Convenience exports
__all__ = [
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
