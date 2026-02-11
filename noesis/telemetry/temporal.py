"""
Noesis Temporal - Clifford Clock & Moon Phase
कालचक्र — The wheel of time that governs consciousness octaves

The Clifford Clock divides the 24-hour day into three 8-hour octaves:
- Ascent (04:00-12:00): Creation, expansion, rajasic energy
- Plateau (12:00-20:00): Sustenance, maintenance, sattvic balance
- Dissolution (20:00-04:00): Rest, integration, tamasic restoration

Each octave contains 8 hours (0-7), mapping to Clifford algebra periodicity.
"""

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple
from enum import Enum
import math


class CliffordPhase(Enum):
    """The three phases of the consciousness octave."""
    ASCENT = "ascent"           # 04:00-12:00 - Creation/Expansion
    PLATEAU = "plateau"         # 12:00-20:00 - Sustenance/Balance  
    DISSOLUTION = "dissolution" # 20:00-04:00 - Rest/Integration


class Guna(Enum):
    """The three gunas mapped to Clifford phases."""
    SATTVIC = "sattvic"     # Balance, clarity, plateau
    RAJASIC = "rajasic"     # Activity, creation, ascent
    TAMASIC = "tamasic"     # Rest, inertia, dissolution


# Phase boundaries in UTC hours
PHASE_BOUNDARIES = {
    CliffordPhase.ASCENT: (4, 12),       # 04:00-12:00
    CliffordPhase.PLATEAU: (12, 20),     # 12:00-20:00
    CliffordPhase.DISSOLUTION: (20, 4),  # 20:00-04:00 (wraps)
}

# Phase to Guna mapping
PHASE_GUNA = {
    CliffordPhase.ASCENT: Guna.RAJASIC,
    CliffordPhase.PLATEAU: Guna.SATTVIC,
    CliffordPhase.DISSOLUTION: Guna.TAMASIC,
}

# Phase colors for TUI
PHASE_COLORS = {
    CliffordPhase.ASCENT: "yellow",
    CliffordPhase.PLATEAU: "green",
    CliffordPhase.DISSOLUTION: "magenta",
}

# Phase emojis
PHASE_EMOJI = {
    CliffordPhase.ASCENT: "🌅",
    CliffordPhase.PLATEAU: "☀️",
    CliffordPhase.DISSOLUTION: "🌙",
}


@dataclass
class CliffordState:
    """Current state of the Clifford Clock."""
    hour: int                    # 0-7 within current octave
    phase: CliffordPhase         # Current phase
    guna: Guna                   # Associated guna
    utc_hour: int                # Actual UTC hour (0-23)
    octave_progress: float       # 0.0-1.0 progress through octave
    next_phase: CliffordPhase    # Upcoming phase
    next_phase_in: timedelta     # Time until next phase
    timestamp: datetime          # When this was calculated
    
    def to_dict(self) -> dict:
        return {
            "hour": self.hour,
            "phase": self.phase.value,
            "guna": self.guna.value,
            "utc_hour": self.utc_hour,
            "octave_progress": round(self.octave_progress, 3),
            "next_phase": self.next_phase.value,
            "next_phase_in_minutes": int(self.next_phase_in.total_seconds() / 60),
            "timestamp": self.timestamp.isoformat(),
        }


def get_clifford_hour(dt: Optional[datetime] = None) -> CliffordState:
    """
    Calculate the current Clifford Clock state.
    
    The 24-hour day is divided into three 8-hour octaves:
    - Ascent: 04:00-12:00 UTC (hours 0-7)
    - Plateau: 12:00-20:00 UTC (hours 0-7)
    - Dissolution: 20:00-04:00 UTC (hours 0-7)
    
    Args:
        dt: Optional datetime (defaults to now UTC)
    
    Returns:
        CliffordState with current hour, phase, and timing info
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    utc_hour = dt.hour
    utc_minute = dt.minute
    
    # Determine current phase and calculate octave hour
    if 4 <= utc_hour < 12:
        phase = CliffordPhase.ASCENT
        phase_start = 4
        next_phase = CliffordPhase.PLATEAU
        next_phase_hour = 12
    elif 12 <= utc_hour < 20:
        phase = CliffordPhase.PLATEAU
        phase_start = 12
        next_phase = CliffordPhase.DISSOLUTION
        next_phase_hour = 20
    else:
        phase = CliffordPhase.DISSOLUTION
        phase_start = 20 if utc_hour >= 20 else -4  # Handle wrap
        next_phase = CliffordPhase.ASCENT
        next_phase_hour = 4 if utc_hour >= 20 else 4
    
    # Calculate hour within octave (0-7)
    if phase == CliffordPhase.DISSOLUTION:
        if utc_hour >= 20:
            hour = utc_hour - 20
        else:
            hour = utc_hour + 4  # 0-3 maps to 4-7
    else:
        hour = utc_hour - phase_start
    
    # Calculate octave progress (0.0 to 1.0)
    minutes_into_octave = hour * 60 + utc_minute
    octave_progress = minutes_into_octave / 480  # 8 hours = 480 minutes
    
    # Calculate time until next phase
    if phase == CliffordPhase.DISSOLUTION and utc_hour < 4:
        # After midnight, next phase is at 04:00 same day
        next_dt = dt.replace(hour=4, minute=0, second=0, microsecond=0)
    elif phase == CliffordPhase.DISSOLUTION:
        # Before midnight, next phase is at 04:00 next day
        next_dt = (dt + timedelta(days=1)).replace(hour=4, minute=0, second=0, microsecond=0)
    else:
        next_dt = dt.replace(hour=next_phase_hour, minute=0, second=0, microsecond=0)
    
    next_phase_in = next_dt - dt
    
    return CliffordState(
        hour=hour,
        phase=phase,
        guna=PHASE_GUNA[phase],
        utc_hour=utc_hour,
        octave_progress=octave_progress,
        next_phase=next_phase,
        next_phase_in=next_phase_in,
        timestamp=dt,
    )


def format_clifford_clock(state: CliffordState, ascii_art: bool = True) -> str:
    """
    Format Clifford Clock state for display.
    
    Args:
        state: CliffordState to format
        ascii_art: Include ASCII visualization
    
    Returns:
        Formatted string for CLI/TUI display
    """
    emoji = PHASE_EMOJI[state.phase]
    guna_emoji = {"sattvic": "🟢", "rajasic": "🟠", "tamasic": "🔴"}[state.guna.value]
    
    lines = [
        f"{emoji} Clifford Clock",
        f"━━━━━━━━━━━━━━━━━━━━",
        f"Phase: {state.phase.value.capitalize()} ({state.guna.value})",
        f"Hour:  {state.hour}/7 in octave",
        f"UTC:   {state.utc_hour:02d}:{state.timestamp.minute:02d}",
    ]
    
    if ascii_art:
        # Create octave progress bar
        filled = int(state.octave_progress * 20)
        bar = "█" * filled + "░" * (20 - filled)
        lines.append(f"\n[{bar}] {state.octave_progress*100:.0f}%")
        
        # Phase indicator
        phase_positions = {"ascent": 0, "plateau": 1, "dissolution": 2}
        pos = phase_positions[state.phase.value]
        indicator = "  " * pos + "▼"
        lines.append(f"\n{indicator}")
        lines.append("┌────────┬────────┬────────┐")
        lines.append("│ ASCENT │PLATEAU │DISSOLVE│")
        lines.append("│  🌅    │   ☀️   │   🌙   │")
        lines.append("└────────┴────────┴────────┘")
    
    # Next phase
    mins = int(state.next_phase_in.total_seconds() / 60)
    hours = mins // 60
    mins = mins % 60
    lines.append(f"\n→ {state.next_phase.value.capitalize()} in {hours}h {mins}m")
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# Moon Phase (Selemene Integration)
# ═══════════════════════════════════════════════════════════

class MoonPhase(Enum):
    """The 8 lunar phases."""
    NEW_MOON = "new_moon"
    WAXING_CRESCENT = "waxing_crescent"
    FIRST_QUARTER = "first_quarter"
    WAXING_GIBBOUS = "waxing_gibbous"
    FULL_MOON = "full_moon"
    WANING_GIBBOUS = "waning_gibbous"
    LAST_QUARTER = "last_quarter"
    WANING_CRESCENT = "waning_crescent"


MOON_EMOJI = {
    MoonPhase.NEW_MOON: "🌑",
    MoonPhase.WAXING_CRESCENT: "🌒",
    MoonPhase.FIRST_QUARTER: "🌓",
    MoonPhase.WAXING_GIBBOUS: "🌔",
    MoonPhase.FULL_MOON: "🌕",
    MoonPhase.WANING_GIBBOUS: "🌖",
    MoonPhase.LAST_QUARTER: "🌗",
    MoonPhase.WANING_CRESCENT: "🌘",
}

# Moon phase to Guna mapping (Full Moon = peak Sattva)
MOON_GUNA = {
    MoonPhase.NEW_MOON: Guna.TAMASIC,
    MoonPhase.WAXING_CRESCENT: Guna.RAJASIC,
    MoonPhase.FIRST_QUARTER: Guna.RAJASIC,
    MoonPhase.WAXING_GIBBOUS: Guna.SATTVIC,
    MoonPhase.FULL_MOON: Guna.SATTVIC,
    MoonPhase.WANING_GIBBOUS: Guna.SATTVIC,
    MoonPhase.LAST_QUARTER: Guna.TAMASIC,
    MoonPhase.WANING_CRESCENT: Guna.TAMASIC,
}


@dataclass
class MoonState:
    """Current moon phase state."""
    phase: MoonPhase
    illumination: float          # 0.0-1.0
    age_days: float              # Days since new moon
    guna: Guna                   # Associated guna influence
    emoji: str
    timestamp: datetime
    
    def to_dict(self) -> dict:
        return {
            "phase": self.phase.value,
            "illumination": round(self.illumination, 3),
            "age_days": round(self.age_days, 2),
            "guna": self.guna.value,
            "emoji": self.emoji,
            "timestamp": self.timestamp.isoformat(),
        }


def get_moon_phase(dt: Optional[datetime] = None) -> MoonState:
    """
    Calculate current moon phase using astronomical approximation.
    
    Uses the synodic month (29.53 days) and a known new moon reference
    to calculate the current phase. For production, integrate with
    Selemene Engine #5 for precise ephemeris data.
    
    Args:
        dt: Optional datetime (defaults to now UTC)
    
    Returns:
        MoonState with phase, illumination, and guna
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Reference new moon: January 6, 2000 18:14 UTC
    reference_new_moon = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    synodic_month = 29.53058867  # days
    
    # Calculate days since reference
    days_since_ref = (dt - reference_new_moon).total_seconds() / 86400
    
    # Calculate moon age (days into current cycle)
    age_days = days_since_ref % synodic_month
    
    # Calculate phase (0-7)
    phase_index = int((age_days / synodic_month) * 8) % 8
    phases = list(MoonPhase)
    phase = phases[phase_index]
    
    # Calculate illumination (simplified sinusoidal model)
    # 0 at new moon, 1 at full moon
    illumination = (1 - math.cos(2 * math.pi * age_days / synodic_month)) / 2
    
    return MoonState(
        phase=phase,
        illumination=illumination,
        age_days=age_days,
        guna=MOON_GUNA[phase],
        emoji=MOON_EMOJI[phase],
        timestamp=dt,
    )


def format_moon_phase(state: MoonState) -> str:
    """Format moon phase for display."""
    guna_emoji = {"sattvic": "🟢", "rajasic": "🟠", "tamasic": "🔴"}[state.guna.value]
    
    lines = [
        f"{state.emoji} Moon Phase",
        f"━━━━━━━━━━━━━━━━━━━━",
        f"Phase: {state.phase.value.replace('_', ' ').title()}",
        f"Illumination: {state.illumination*100:.0f}%",
        f"Age: {state.age_days:.1f} days",
        f"Guna: {guna_emoji} {state.guna.value}",
    ]
    
    # Illumination bar
    filled = int(state.illumination * 20)
    bar = "●" * filled + "○" * (20 - filled)
    lines.append(f"\n[{bar}]")
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# Combined Temporal State
# ═══════════════════════════════════════════════════════════

@dataclass
class TemporalState:
    """Combined Clifford Clock and Moon state."""
    clifford: CliffordState
    moon: MoonState
    combined_guna: Guna  # Weighted combination
    
    def to_dict(self) -> dict:
        return {
            "clifford": self.clifford.to_dict(),
            "moon": self.moon.to_dict(),
            "combined_guna": self.combined_guna.value,
        }


def get_temporal_state(dt: Optional[datetime] = None) -> TemporalState:
    """Get combined temporal state (Clifford + Moon)."""
    clifford = get_clifford_hour(dt)
    moon = get_moon_phase(dt)
    
    # Weight: 70% Clifford (immediate), 30% Moon (ambient)
    # Simple heuristic: if both agree, use that guna
    # If they differ, use Clifford (more immediate influence)
    if clifford.guna == moon.guna:
        combined = clifford.guna
    else:
        combined = clifford.guna  # Clifford dominates
    
    return TemporalState(
        clifford=clifford,
        moon=moon,
        combined_guna=combined,
    )


if __name__ == "__main__":
    # Test the temporal functions
    print("Current Clifford State:")
    print("=" * 40)
    state = get_clifford_hour()
    print(format_clifford_clock(state))
    
    print("\n\nCurrent Moon State:")
    print("=" * 40)
    moon = get_moon_phase()
    print(format_moon_phase(moon))
    
    print("\n\nCombined Temporal State:")
    print("=" * 40)
    temporal = get_temporal_state()
    print(f"Combined Guna: {temporal.combined_guna.value}")
