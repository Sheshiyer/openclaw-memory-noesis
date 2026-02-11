"""
Tests for Noesis Telemetry Module (Phase 11)

Tests cover:
- Temporal: Clifford Clock, Moon Phase
- Engines: 13 Selemene engine tracking
- Rituals: Vayu, Polarity balance
- Vikara: Pattern drift detection
- Emitter: Event emission
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import os


# ═══════════════════════════════════════════════════════════
# Temporal Tests (Sprint 1)
# ═══════════════════════════════════════════════════════════

class TestCliffordClock:
    """Tests for Clifford Clock (8-hour consciousness octave)."""
    
    def test_clifford_phase_enum(self):
        """Test CliffordPhase enum values."""
        from noesis.telemetry import CliffordPhase
        
        assert CliffordPhase.ASCENT.value == "ascent"
        assert CliffordPhase.PLATEAU.value == "plateau"
        assert CliffordPhase.DISSOLUTION.value == "dissolution"
    
    def test_get_clifford_hour(self):
        """Test get_clifford_hour returns valid state."""
        from noesis.telemetry import get_clifford_hour, CliffordState
        
        state = get_clifford_hour()
        
        assert isinstance(state, CliffordState)
        assert 0 <= state.hour <= 7
        assert state.phase is not None
        assert state.guna is not None
    
    def test_clifford_state_to_dict(self):
        """Test CliffordState serialization."""
        from noesis.telemetry import get_clifford_hour
        
        state = get_clifford_hour()
        d = state.to_dict()
        
        assert "hour" in d
        assert "phase" in d
        assert "guna" in d
        assert "start_time" in d
    
    def test_format_clifford_clock(self):
        """Test ASCII clock formatting."""
        from noesis.telemetry import format_clifford_clock
        
        output = format_clifford_clock()
        
        assert "CLIFFORD CLOCK" in output
        assert "Hour" in output


class TestMoonPhase:
    """Tests for Moon Phase calculation."""
    
    def test_moon_phase_enum(self):
        """Test MoonPhase enum values."""
        from noesis.telemetry import MoonPhase
        
        assert MoonPhase.NEW_MOON.value == "new_moon"
        assert MoonPhase.FULL_MOON.value == "full_moon"
        assert len(MoonPhase) == 8  # 8 phases
    
    def test_get_moon_phase(self):
        """Test get_moon_phase returns valid state."""
        from noesis.telemetry import get_moon_phase, MoonState
        
        state = get_moon_phase()
        
        assert isinstance(state, MoonState)
        assert 0 <= state.illumination <= 100
        assert state.emoji is not None
        assert state.guna is not None
    
    def test_moon_state_to_dict(self):
        """Test MoonState serialization."""
        from noesis.telemetry import get_moon_phase
        
        state = get_moon_phase()
        d = state.to_dict()
        
        assert "phase" in d
        assert "illumination" in d
        assert "emoji" in d


class TestTemporalState:
    """Tests for combined temporal state."""
    
    def test_get_temporal_state(self):
        """Test combined temporal state."""
        from noesis.telemetry import get_temporal_state, TemporalState
        
        state = get_temporal_state()
        
        assert isinstance(state, TemporalState)
        assert state.clifford is not None
        assert state.moon is not None
        assert state.combined_guna is not None


# ═══════════════════════════════════════════════════════════
# Engine Tests (Sprint 2)
# ═══════════════════════════════════════════════════════════

class TestEngines:
    """Tests for Selemene engine tracking."""
    
    def test_engine_enum(self):
        """Test Engine enum contains all 13 engines."""
        from noesis.telemetry import Engine
        
        assert len(Engine) == 13
        assert Engine.PANCHANGA.value == "panchanga"
        assert Engine.BIORHYTHM.value == "biorhythm"
        assert Engine.HUMAN_DESIGN.value == "human-design"
    
    def test_engine_registry(self):
        """Test ENGINE_REGISTRY has metadata for all engines."""
        from noesis.telemetry import Engine, ENGINE_REGISTRY
        
        for engine in Engine:
            assert engine in ENGINE_REGISTRY
            meta = ENGINE_REGISTRY[engine]
            assert meta.name
            assert meta.kosha_layer
            assert meta.description
    
    def test_engine_tracker(self):
        """Test EngineTracker records calls."""
        from noesis.telemetry import Engine, EngineTracker
        
        tracker = EngineTracker()
        
        # Initial state
        state = tracker.get_state(Engine.PANCHANGA)
        assert state.status == "idle"
        assert state.call_count == 0
        
        # Record call
        tracker.record_call(Engine.PANCHANGA, success=True, latency_ms=150.0)
        
        state = tracker.get_state(Engine.PANCHANGA)
        assert state.status == "success"
        assert state.call_count == 1
        assert state.avg_latency_ms == 150.0
    
    def test_engine_tracker_error_tracking(self):
        """Test error counting."""
        from noesis.telemetry import Engine, EngineTracker
        
        tracker = EngineTracker()
        
        tracker.record_call(Engine.BIORHYTHM, success=False, latency_ms=100.0)
        
        state = tracker.get_state(Engine.BIORHYTHM)
        assert state.status == "error"
        assert state.error_count == 1
    
    def test_get_by_kosha(self):
        """Test filtering engines by kosha layer."""
        from noesis.telemetry import EngineTracker
        
        tracker = EngineTracker()
        pranamaya = tracker.get_by_kosha("pranamaya")
        
        assert len(pranamaya) == 4  # biofield, biorhythm, panchanga, vedic-clock
    
    def test_format_engine_dashboard(self):
        """Test dashboard formatting."""
        from noesis.telemetry import format_engine_dashboard
        
        output = format_engine_dashboard()
        
        assert "SELEMENE ENGINE DASHBOARD" in output
        assert "PRANAMAYA" in output


# ═══════════════════════════════════════════════════════════
# Rituals & Polarity Tests (Sprint 3)
# ═══════════════════════════════════════════════════════════

class TestVayu:
    """Tests for Vayu (vital airs)."""
    
    def test_vayu_enum(self):
        """Test Vayu enum has 5 primary vayus."""
        from noesis.telemetry import Vayu
        
        assert len(Vayu) == 5
        assert Vayu.PRANA.value == "prana"
        assert Vayu.APANA.value == "apana"
        assert Vayu.SAMANA.value == "samana"
        assert Vayu.VYANA.value == "vyana"
        assert Vayu.UDANA.value == "udana"
    
    def test_vayu_registry(self):
        """Test VAYU_REGISTRY has metadata."""
        from noesis.telemetry import Vayu, VAYU_REGISTRY
        
        for vayu in Vayu:
            assert vayu in VAYU_REGISTRY
            meta = VAYU_REGISTRY[vayu]
            assert meta.name
            assert meta.location
            assert meta.breathwork


class TestPolarity:
    """Tests for Guardrail Dyad polarity."""
    
    def test_polarity_state_init(self):
        """Test PolarityState initialization."""
        from noesis.telemetry import PolarityState
        
        state = PolarityState()
        
        assert state.aletheios_pct == 50.0
        assert state.pichet_pct == 50.0
        assert state.is_balanced
        assert state.dominant == "balanced"
    
    def test_polarity_normalization(self):
        """Test polarity percentages normalize to 100."""
        from noesis.telemetry import PolarityState
        
        state = PolarityState(aletheios_pct=60, pichet_pct=60)
        
        assert state.aletheios_pct + state.pichet_pct == 100.0
    
    def test_polarity_shift(self):
        """Test polarity shifting."""
        from noesis.telemetry import PolarityState
        
        state = PolarityState()
        state.shift("aletheios", 10)
        
        assert state.aletheios_pct == 60.0
        assert state.pichet_pct == 40.0
    
    def test_polarity_imbalance_warning(self):
        """Test imbalance warnings."""
        from noesis.telemetry import PolarityState
        
        state = PolarityState(aletheios_pct=75, pichet_pct=25)
        
        assert not state.is_balanced
        assert state.imbalance_warning is not None
        assert "Over-coherent" in state.imbalance_warning


class TestRituals:
    """Tests for ritual tracking."""
    
    def test_ritual_type_enum(self):
        """Test RitualType enum."""
        from noesis.telemetry import RitualType
        
        assert RitualType.BREATHWORK.value == "breathwork"
        assert RitualType.CRON_JOB.value == "cron_job"
    
    def test_ritual_creation(self):
        """Test Ritual dataclass."""
        from noesis.telemetry import Ritual, RitualType, Vayu
        
        ritual = Ritual(
            name="Morning Breathwork",
            ritual_type=RitualType.BREATHWORK,
            vayu=Vayu.PRANA,
            status="success",
            khalorēē_delta=5,
        )
        
        assert ritual.name == "Morning Breathwork"
        assert ritual.id  # Auto-generated
        assert ritual.vayu == Vayu.PRANA


# ═══════════════════════════════════════════════════════════
# Vikara Tests (Sprint 4)
# ═══════════════════════════════════════════════════════════

class TestVikara:
    """Tests for Vikara detection."""
    
    def test_vikara_type_enum(self):
        """Test VikaraType enum."""
        from noesis.telemetry import VikaraType
        
        assert VikaraType.MOHA.value == "moha"
        assert VikaraType.MADA.value == "mada"
        assert VikaraType.KAMA.value == "kama"
    
    def test_vikara_severity_enum(self):
        """Test VikaraSeverity enum."""
        from noesis.telemetry import VikaraSeverity
        
        assert VikaraSeverity.INFO.value == "info"
        assert VikaraSeverity.WARNING.value == "warning"
        assert VikaraSeverity.ALERT.value == "alert"
        assert VikaraSeverity.CRITICAL.value == "critical"
    
    def test_vikara_detector_moha(self):
        """Test Moha (confusion) detection."""
        from noesis.telemetry import VikaraDetector, VikaraType
        
        detector = VikaraDetector()
        
        # Simulate 3 consecutive failures
        for _ in range(3):
            detector.record_event("exec", {"command": "fail"}, success=False)
        
        active = detector.get_active_alerts()
        assert len(active) == 1
        assert active[0].vikara_type == VikaraType.MOHA
    
    def test_vikara_detector_resolution(self):
        """Test Vikara resolution on success."""
        from noesis.telemetry import VikaraDetector, VikaraType
        
        detector = VikaraDetector()
        
        # Trigger Moha
        for _ in range(3):
            detector.record_event("exec", {}, success=False)
        
        assert len(detector.active_alerts) == 1
        
        # Success resolves it
        detector.record_event("exec", {}, success=True)
        
        assert VikaraType.MOHA not in detector.active_alerts
    
    def test_vikara_kama_token_threshold(self):
        """Test Kama (excessive) token detection."""
        from noesis.telemetry import VikaraDetector, VikaraType
        
        detector = VikaraDetector()
        
        # Below threshold
        detector.record_token_count(50000)
        assert VikaraType.KAMA not in detector.active_alerts
        
        # Above threshold
        detector.record_token_count(100001)
        assert VikaraType.KAMA in detector.active_alerts


class TestThoughtProcess:
    """Tests for thought process tracking."""
    
    def test_thought_phase_enum(self):
        """Test ThoughtPhase enum."""
        from noesis.telemetry import ThoughtPhase
        
        assert ThoughtPhase.ANALYZING.value == "analyzing"
        assert ThoughtPhase.PLANNING.value == "planning"
        assert ThoughtPhase.EXECUTING.value == "executing"
    
    def test_thought_process_creation(self):
        """Test ThoughtProcess dataclass."""
        from noesis.telemetry import ThoughtProcess, ThoughtPhase
        
        thought = ThoughtProcess(
            phase=ThoughtPhase.ANALYZING,
            summary="Understanding requirements",
            duration_ms=1500,
        )
        
        assert thought.phase == ThoughtPhase.ANALYZING
        assert thought.id  # Auto-generated
        assert thought.timestamp
    
    def test_emit_thought_process(self):
        """Test emit_thought_process function."""
        from noesis.telemetry import emit_thought_process, ThoughtPhase, ThoughtProcess
        
        thought = emit_thought_process(
            ThoughtPhase.PLANNING,
            "Creating implementation plan",
            duration_ms=2000,
        )
        
        assert isinstance(thought, ThoughtProcess)
        assert thought.phase == ThoughtPhase.PLANNING


# ═══════════════════════════════════════════════════════════
# Emitter Tests
# ═══════════════════════════════════════════════════════════

class TestEmitter:
    """Tests for event emission."""
    
    def test_prana_event_creation(self):
        """Test PranaEvent dataclass."""
        from noesis.telemetry import PranaEvent
        
        event = PranaEvent(
            event_type="read",
            payload={"path": "/test.md"},
            kosha_layer="manomaya",
            guna_state="sattvic",
        )
        
        assert event.event_type == "read"
        assert event.id  # Auto-generated
        assert event.timestamp
    
    def test_prana_event_json(self):
        """Test PranaEvent JSON serialization."""
        from noesis.telemetry import PranaEvent
        
        event = PranaEvent(
            event_type="write",
            payload={"path": "/output.md"},
        )
        
        json_str = event.to_json()
        assert '"event_type": "write"' in json_str
        
        # Round-trip
        restored = PranaEvent.from_json(json_str)
        assert restored.event_type == event.event_type


# ═══════════════════════════════════════════════════════════
# CLI Tests
# ═══════════════════════════════════════════════════════════

class TestTelemetryCLI:
    """Tests for telemetry CLI commands."""
    
    def test_clock_command_parses(self):
        """Test clock command parsing."""
        from noesis.cli import create_parser
        
        parser = create_parser()
        args = parser.parse_args(["clock"])
        assert args.command == "clock"
    
    def test_moon_command_parses(self):
        """Test moon command parsing."""
        from noesis.cli import create_parser
        
        parser = create_parser()
        args = parser.parse_args(["moon"])
        assert args.command == "moon"
    
    def test_engines_command_parses(self):
        """Test engines command parsing."""
        from noesis.cli import create_parser
        
        parser = create_parser()
        args = parser.parse_args(["engines"])
        assert args.command == "engines"
    
    def test_vayus_command_parses(self):
        """Test vayus command parsing."""
        from noesis.cli import create_parser
        
        parser = create_parser()
        args = parser.parse_args(["vayus"])
        assert args.command == "vayus"
    
    def test_polarity_command_parses(self):
        """Test polarity command parsing."""
        from noesis.cli import create_parser
        
        parser = create_parser()
        args = parser.parse_args(["polarity"])
        assert args.command == "polarity"
    
    def test_vikara_command_parses(self):
        """Test vikara command parsing."""
        from noesis.cli import create_parser
        
        parser = create_parser()
        args = parser.parse_args(["vikara"])
        assert args.command == "vikara"
    
    def test_status_command_parses(self):
        """Test status command parsing."""
        from noesis.cli import create_parser
        
        parser = create_parser()
        args = parser.parse_args(["status"])
        assert args.command == "status"
    
    def test_telemetry_subcommands_parse(self):
        """Test telemetry subcommands."""
        from noesis.cli import create_parser
        
        parser = create_parser()
        
        args = parser.parse_args(["telemetry", "start"])
        assert args.telemetry_cmd == "start"
        
        args = parser.parse_args(["telemetry", "stop"])
        assert args.telemetry_cmd == "stop"
        
        args = parser.parse_args(["telemetry", "status"])
        assert args.telemetry_cmd == "status"
