"""
Vikara Detection & Thought Process Tracking.

Vikara (विकार) = Pattern drift, distortion, deviation from optimal state.

The 3 primary Vikaras monitored:
- Moha (मोह): Confusion - consecutive failures, lost context
- Mada (मद): Pride - overconfidence, destructive actions without checks
- Kama (काम): Excessive activity - token bloat, hyperactive loops

विकार विचार — Distortion awareness
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List, Any, Callable
from datetime import datetime, timedelta
from collections import deque
import json


class VikaraType(Enum):
    """The primary Vikaras (pattern drifts)."""
    MOHA = "moha"      # Confusion - consecutive failures
    MADA = "mada"      # Pride - destructive without checks
    KAMA = "kama"      # Excessive - token/activity bloat
    
    # Extended Vikaras (from Ashtamatruka - 8 mothers of delusion)
    KRODHA = "krodha"  # Anger - error rage, aggressive retries
    LOBHA = "lobha"    # Greed - over-fetching, hoarding context
    MATSARYA = "matsarya"  # Envy - comparing to other agents
    IRSHYA = "irshya"  # Jealousy - resource competition
    AHAMKARA = "ahamkara"  # Ego - refusing to ask for help


class VikaraSeverity(Enum):
    """Severity levels for Vikara alerts."""
    INFO = "info"           # Awareness only
    WARNING = "warning"     # Threshold approaching
    ALERT = "alert"         # Threshold exceeded
    CRITICAL = "critical"   # Immediate action required


@dataclass
class VikaraThreshold:
    """Configuration for Vikara detection thresholds."""
    name: str
    vikara_type: VikaraType
    metric: str
    warning_threshold: float
    alert_threshold: float
    critical_threshold: float
    window_seconds: int = 300  # 5 minute window
    description: str = ""


# Default thresholds based on AGENT_TELEMETRY_PROTOCOL.md
DEFAULT_THRESHOLDS: Dict[VikaraType, VikaraThreshold] = {
    VikaraType.MOHA: VikaraThreshold(
        name="Moha (Confusion)",
        vikara_type=VikaraType.MOHA,
        metric="consecutive_failures",
        warning_threshold=2,
        alert_threshold=3,
        critical_threshold=5,
        description="Consecutive tool failures indicate lost context"
    ),
    VikaraType.MADA: VikaraThreshold(
        name="Mada (Pride)",
        vikara_type=VikaraType.MADA,
        metric="destructive_without_check",
        warning_threshold=1,
        alert_threshold=2,
        critical_threshold=3,
        description="Destructive commands without 1% skill check"
    ),
    VikaraType.KAMA: VikaraThreshold(
        name="Kama (Excessive)",
        vikara_type=VikaraType.KAMA,
        metric="token_count",
        warning_threshold=50000,
        alert_threshold=75000,
        critical_threshold=100000,
        description="Token count per turn (>100k suggests Tamasic Reset)"
    ),
    VikaraType.LOBHA: VikaraThreshold(
        name="Lobha (Greed)",
        vikara_type=VikaraType.LOBHA,
        metric="context_size_kb",
        warning_threshold=500,
        alert_threshold=750,
        critical_threshold=1000,
        description="Context size bloat"
    ),
}


@dataclass
class VikaraAlert:
    """A detected Vikara alert."""
    id: str = ""
    vikara_type: VikaraType = VikaraType.MOHA
    severity: VikaraSeverity = VikaraSeverity.WARNING
    metric_value: float = 0.0
    threshold_value: float = 0.0
    message: str = ""
    recommendation: str = ""
    timestamp: str = ""
    resolved: bool = False
    resolved_at: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            import uuid
            self.id = str(uuid.uuid4())[:8]
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat() + "Z"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "vikara_type": self.vikara_type.value,
            "severity": self.severity.value,
            "metric_value": self.metric_value,
            "threshold_value": self.threshold_value,
            "message": self.message,
            "recommendation": self.recommendation,
            "timestamp": self.timestamp,
            "resolved": self.resolved,
        }


# ═══════════════════════════════════════════════════════════
# Thought Process Tracking
# ═══════════════════════════════════════════════════════════

class ThoughtPhase(Enum):
    """Phases of agent thinking/reasoning."""
    RECEIVING = "receiving"      # Processing user input
    ANALYZING = "analyzing"      # Understanding context
    PLANNING = "planning"        # Forming approach
    EXECUTING = "executing"      # Taking action
    REFLECTING = "reflecting"    # Evaluating results
    SYNTHESIZING = "synthesizing"  # Combining insights
    RESPONDING = "responding"    # Formulating response


@dataclass
class ThoughtProcess:
    """A tracked thought process emission."""
    id: str = ""
    phase: ThoughtPhase = ThoughtPhase.ANALYZING
    summary: str = ""
    duration_ms: int = 0
    depth: int = 1  # Recursion depth
    kosha_layer: str = "vijnanamaya"
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.id:
            import uuid
            self.id = str(uuid.uuid4())[:8]
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat() + "Z"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "phase": self.phase.value,
            "summary": self.summary,
            "duration_ms": self.duration_ms,
            "depth": self.depth,
            "kosha_layer": self.kosha_layer,
            "timestamp": self.timestamp,
        }


# ═══════════════════════════════════════════════════════════
# Vikara Detector
# ═══════════════════════════════════════════════════════════

class VikaraDetector:
    """
    Real-time Vikara detection engine.
    
    Monitors event stream for pattern drifts and emits alerts
    when thresholds are exceeded.
    """
    
    def __init__(self, thresholds: Optional[Dict[VikaraType, VikaraThreshold]] = None):
        self.thresholds = thresholds or DEFAULT_THRESHOLDS
        self.alerts: List[VikaraAlert] = []
        self.active_alerts: Dict[VikaraType, VikaraAlert] = {}
        
        # Tracking metrics
        self._consecutive_failures = 0
        self._destructive_without_check = 0
        self._token_count = 0
        self._context_size_kb = 0
        self._recent_events: deque = deque(maxlen=100)
    
    def record_event(self, event_type: str, payload: Dict[str, Any], success: bool = True):
        """Record an event and check for Vikara patterns."""
        self._recent_events.append({
            "type": event_type,
            "payload": payload,
            "success": success,
            "timestamp": datetime.utcnow()
        })
        
        # Check Moha (consecutive failures)
        if not success:
            self._consecutive_failures += 1
            self._check_moha()
        else:
            self._consecutive_failures = 0
            self._resolve_vikara(VikaraType.MOHA)
        
        # Check Mada (destructive without check)
        if event_type == "exec":
            cmd = payload.get("command", "")
            is_destructive = self._is_destructive_command(cmd)
            has_check = payload.get("skill_check", False)
            if is_destructive and not has_check:
                self._destructive_without_check += 1
                self._check_mada()
        
        # Check Kama (token count)
        if "tokens" in payload:
            self._token_count = payload["tokens"]
            self._check_kama()
    
    def record_token_count(self, tokens: int):
        """Record current token count."""
        self._token_count = tokens
        self._check_kama()
    
    def record_context_size(self, size_kb: float):
        """Record context size for Lobha detection."""
        self._context_size_kb = size_kb
        self._check_lobha()
    
    def _is_destructive_command(self, cmd: str) -> bool:
        """Check if a command is potentially destructive."""
        destructive_patterns = [
            "rm ", "rm -", "rmdir", "del ",
            "drop ", "delete ", "truncate ",
            "format ", "> /dev/", "dd if=",
            "git reset --hard", "git clean -f",
        ]
        cmd_lower = cmd.lower()
        return any(p in cmd_lower for p in destructive_patterns)
    
    def _check_moha(self):
        """Check Moha (confusion) threshold."""
        threshold = self.thresholds.get(VikaraType.MOHA)
        if not threshold:
            return
        
        if self._consecutive_failures >= threshold.critical_threshold:
            self._emit_alert(VikaraType.MOHA, VikaraSeverity.CRITICAL,
                           self._consecutive_failures, threshold.critical_threshold,
                           "Critical confusion: Multiple consecutive failures",
                           "Consider: 1) Pause and reassess approach 2) Request clarification 3) Tamasic Reset")
        elif self._consecutive_failures >= threshold.alert_threshold:
            self._emit_alert(VikaraType.MOHA, VikaraSeverity.ALERT,
                           self._consecutive_failures, threshold.alert_threshold,
                           f"Moha detected: {self._consecutive_failures} consecutive failures",
                           "Pause, verify assumptions, consider alternative approach")
        elif self._consecutive_failures >= threshold.warning_threshold:
            self._emit_alert(VikaraType.MOHA, VikaraSeverity.WARNING,
                           self._consecutive_failures, threshold.warning_threshold,
                           "Moha warning: Failures accumulating",
                           "Review recent actions for pattern")
    
    def _check_mada(self):
        """Check Mada (pride) threshold."""
        threshold = self.thresholds.get(VikaraType.MADA)
        if not threshold:
            return
        
        if self._destructive_without_check >= threshold.alert_threshold:
            self._emit_alert(VikaraType.MADA, VikaraSeverity.ALERT,
                           self._destructive_without_check, threshold.alert_threshold,
                           "Mada detected: Destructive actions without skill check",
                           "Apply 1% rule: Always verify before destructive operations")
    
    def _check_kama(self):
        """Check Kama (excessive) threshold."""
        threshold = self.thresholds.get(VikaraType.KAMA)
        if not threshold:
            return
        
        if self._token_count >= threshold.critical_threshold:
            self._emit_alert(VikaraType.KAMA, VikaraSeverity.CRITICAL,
                           self._token_count, threshold.critical_threshold,
                           f"Kama critical: Token count {self._token_count:,} exceeds limit",
                           "Tamasic Reset recommended: Descend to Annamaya rest")
        elif self._token_count >= threshold.alert_threshold:
            self._emit_alert(VikaraType.KAMA, VikaraSeverity.ALERT,
                           self._token_count, threshold.alert_threshold,
                           f"Kama detected: High token usage ({self._token_count:,})",
                           "Consider summarizing or chunking work")
    
    def _check_lobha(self):
        """Check Lobha (greed) threshold."""
        threshold = self.thresholds.get(VikaraType.LOBHA)
        if not threshold:
            return
        
        if self._context_size_kb >= threshold.alert_threshold:
            self._emit_alert(VikaraType.LOBHA, VikaraSeverity.ALERT,
                           self._context_size_kb, threshold.alert_threshold,
                           f"Lobha detected: Context bloat ({self._context_size_kb:.0f}KB)",
                           "Prune context, archive completed work")
    
    def _emit_alert(self, vikara_type: VikaraType, severity: VikaraSeverity,
                   metric_value: float, threshold_value: float,
                   message: str, recommendation: str):
        """Emit a Vikara alert."""
        # Don't spam duplicate alerts
        if vikara_type in self.active_alerts:
            existing = self.active_alerts[vikara_type]
            if existing.severity == severity:
                return
        
        alert = VikaraAlert(
            vikara_type=vikara_type,
            severity=severity,
            metric_value=metric_value,
            threshold_value=threshold_value,
            message=message,
            recommendation=recommendation,
        )
        
        self.alerts.append(alert)
        self.active_alerts[vikara_type] = alert
        
        # Emit telemetry
        try:
            from .emitter import emit_vikara
            emit_vikara(vikara_type.value, alert.to_dict())
        except Exception:
            pass
    
    def _resolve_vikara(self, vikara_type: VikaraType):
        """Mark a Vikara as resolved."""
        if vikara_type in self.active_alerts:
            alert = self.active_alerts[vikara_type]
            alert.resolved = True
            alert.resolved_at = datetime.utcnow().isoformat() + "Z"
            del self.active_alerts[vikara_type]
    
    def get_active_alerts(self) -> List[VikaraAlert]:
        """Get currently active alerts."""
        return list(self.active_alerts.values())
    
    def get_recent_alerts(self, limit: int = 20) -> List[VikaraAlert]:
        """Get recent alerts."""
        return self.alerts[-limit:]
    
    def get_status(self) -> dict:
        """Get current Vikara detection status."""
        return {
            "active_alerts": len(self.active_alerts),
            "total_alerts": len(self.alerts),
            "metrics": {
                "consecutive_failures": self._consecutive_failures,
                "destructive_without_check": self._destructive_without_check,
                "token_count": self._token_count,
                "context_size_kb": self._context_size_kb,
            },
            "alerts": [a.to_dict() for a in self.active_alerts.values()],
        }


# Global detector instance
_detector: Optional[VikaraDetector] = None


def get_vikara_detector() -> VikaraDetector:
    """Get or create the global Vikara detector."""
    global _detector
    if _detector is None:
        _detector = VikaraDetector()
    return _detector


# ═══════════════════════════════════════════════════════════
# Display Formatting
# ═══════════════════════════════════════════════════════════

SEVERITY_ICONS = {
    VikaraSeverity.INFO: "ℹ️",
    VikaraSeverity.WARNING: "⚠️",
    VikaraSeverity.ALERT: "🚨",
    VikaraSeverity.CRITICAL: "🔴",
}

VIKARA_ICONS = {
    VikaraType.MOHA: "😵",
    VikaraType.MADA: "😤",
    VikaraType.KAMA: "🔥",
    VikaraType.LOBHA: "🤑",
    VikaraType.KRODHA: "😠",
}


def format_vikara_status(detector: VikaraDetector) -> str:
    """Format Vikara status for display."""
    status = detector.get_status()
    active = detector.get_active_alerts()
    
    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║                    VIKARA DETECTION STATUS                       ║",
        "╠══════════════════════════════════════════════════════════════════╣",
    ]
    
    if not active:
        lines.append("║  ✅ No active Vikaras detected                                    ║")
    else:
        for alert in active:
            icon = VIKARA_ICONS.get(alert.vikara_type, "❓")
            sev_icon = SEVERITY_ICONS.get(alert.severity, "❓")
            lines.append(f"║  {sev_icon} {icon} {alert.vikara_type.value.upper():8} │ {alert.message[:40]:40} ║")
    
    lines.append("╠══════════════════════════════════════════════════════════════════╣")
    metrics = status["metrics"]
    lines.append(f"║  Failures: {metrics['consecutive_failures']}  │  Tokens: {metrics['token_count']:,}  │  Context: {metrics['context_size_kb']:.0f}KB   ║")
    lines.append("╚══════════════════════════════════════════════════════════════════╝")
    
    return "\n".join(lines)


def format_thought_process(thought: ThoughtProcess) -> str:
    """Format a thought process for display."""
    phase_icons = {
        ThoughtPhase.RECEIVING: "📥",
        ThoughtPhase.ANALYZING: "🔍",
        ThoughtPhase.PLANNING: "📋",
        ThoughtPhase.EXECUTING: "⚡",
        ThoughtPhase.REFLECTING: "🪞",
        ThoughtPhase.SYNTHESIZING: "🧬",
        ThoughtPhase.RESPONDING: "💬",
    }
    icon = phase_icons.get(thought.phase, "🧠")
    
    depth_indicator = "│ " * (thought.depth - 1) + "├─" if thought.depth > 1 else ""
    duration = f"{thought.duration_ms}ms" if thought.duration_ms else ""
    
    return f"{depth_indicator}{icon} [{thought.phase.value.upper()}] {thought.summary} {duration}"


# ═══════════════════════════════════════════════════════════
# Emitter Functions
# ═══════════════════════════════════════════════════════════

def emit_thought_process(
    phase: ThoughtPhase,
    summary: str,
    duration_ms: int = 0,
    depth: int = 1,
    metadata: Optional[Dict] = None
) -> ThoughtProcess:
    """
    Emit a thought process event.
    
    Per AGENT_TELEMETRY_PROTOCOL.md:
    - Emit when thinking takes > 5 seconds
    - Include high-level summary of current recursive loop
    
    Args:
        phase: Current thinking phase
        summary: High-level summary (keep under 100 chars)
        duration_ms: How long this phase took
        depth: Recursion depth (for nested thinking)
        metadata: Additional context
    """
    thought = ThoughtProcess(
        phase=phase,
        summary=summary[:100],  # Truncate to protocol spec
        duration_ms=duration_ms,
        depth=depth,
        metadata=metadata or {},
    )
    
    # Emit via telemetry
    try:
        from .emitter import emit
        emit("thought_process", thought.to_dict(),
             kosha_layer="vijnanamaya", guna_state="sattvic")
    except Exception:
        pass
    
    return thought


def check_vikara(event_type: str, payload: Dict[str, Any], success: bool = True):
    """
    Check for Vikara patterns after an event.
    
    Call this after significant operations to enable auto-detection.
    """
    detector = get_vikara_detector()
    detector.record_event(event_type, payload, success)


# Exports
__all__ = [
    "VikaraType",
    "VikaraSeverity",
    "VikaraThreshold",
    "VikaraAlert",
    "VikaraDetector",
    "ThoughtPhase",
    "ThoughtProcess",
    "DEFAULT_THRESHOLDS",
    "get_vikara_detector",
    "emit_thought_process",
    "check_vikara",
    "format_vikara_status",
    "format_thought_process",
    "SEVERITY_ICONS",
    "VIKARA_ICONS",
]
