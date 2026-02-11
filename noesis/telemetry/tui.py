"""
Prana Stream - Terminal UI
प्राण दर्शन — The visualization of vital flow

Rich-based live dashboard for real-time telemetry monitoring.
Falls back gracefully if Rich is not installed.
"""

import os
import sys
import stat
import select
import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from collections import deque

from .schema import get_fifo_path, PranaEvent
from .query import get_recent_events, get_current_khaloree, get_event_stats

# Try to import Rich
try:
    from rich.console import Console
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.text import Text
    from rich.progress import Progress, BarColumn, TextColumn
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


# Event type icons
EVENT_ICONS = {
    "read": "📖",
    "write": "✍️",
    "exec": "⚡",
    "think": "🧠",
    "vikara": "⚠️",
    "khalorēē": "💫",
    "session.start": "🚀",
    "session.end": "🏁",
}

# Guna colors/icons
GUNA_DISPLAY = {
    "sattvic": ("🟢", "green"),
    "rajasic": ("🟠", "yellow"),
    "tamasic": ("🔴", "red"),
}

# Kosha colors
KOSHA_COLORS = {
    "annamaya": "bright_white",
    "pranamaya": "bright_yellow",
    "manomaya": "bright_cyan",
    "vijnanamaya": "bright_magenta",
    "anandamaya": "bright_green",
}


class PranaTUI:
    """Rich-based TUI for Prana Stream monitoring."""
    
    def __init__(self, max_events: int = 20):
        if not HAS_RICH:
            raise ImportError(
                "Rich is required for the TUI. Install with: pip install rich"
            )
        
        self.console = Console()
        self.max_events = max_events
        self.events: deque = deque(maxlen=max_events)
        self.running = False
        self.paused = False
        self.khaloree = 100
        self.stats: Dict[str, Any] = {}
        
        # Load recent events
        self._load_recent_events()
    
    def _load_recent_events(self) -> None:
        """Load recent events from database."""
        try:
            recent = get_recent_events(limit=self.max_events)
            for event in reversed(recent):  # Oldest first
                self.events.append(event)
            self.khaloree = get_current_khaloree()
            self.stats = get_event_stats(since="1 hour ago")
        except Exception:
            pass
    
    def _build_header(self) -> Panel:
        """Build the header panel."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        status = "⏸️ PAUSED" if self.paused else "▶️ LIVE"
        
        header_text = Text()
        header_text.append("🕉️ PRANA STREAM ", style="bold magenta")
        header_text.append(f"│ {status} ", style="bold green" if not self.paused else "bold yellow")
        header_text.append(f"│ {now}", style="dim")
        
        return Panel(header_text, box=box.ROUNDED)
    
    def _build_khaloree_gauge(self) -> Panel:
        """Build the khalorēē gauge panel."""
        # Create progress bar
        filled = int(self.khaloree / 5)  # 20 chars total
        empty = 20 - filled
        
        if self.khaloree >= 70:
            color = "green"
        elif self.khaloree >= 40:
            color = "yellow"
        else:
            color = "red"
        
        bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
        
        text = Text()
        text.append("KHALORĒĒ  ", style="bold")
        text.append_text(Text.from_markup(bar))
        text.append(f"  {self.khaloree}/100", style="bold " + color)
        
        return Panel(text, title="💫 Metabolic Reserve", box=box.ROUNDED)
    
    def _build_guna_indicator(self) -> Panel:
        """Build the guna state indicator."""
        # Determine dominant guna from recent events
        guna_counts = {"sattvic": 0, "rajasic": 0, "tamasic": 0}
        for event in self.events:
            if event.guna_state in guna_counts:
                guna_counts[event.guna_state] += 1
        
        dominant = max(guna_counts, key=guna_counts.get) if self.events else "sattvic"
        icon, color = GUNA_DISPLAY.get(dominant, ("⚪", "white"))
        
        text = Text()
        text.append(f"{icon} ", style="bold")
        text.append(dominant.upper(), style=f"bold {color}")
        text.append(f"\n\n🟢 {guna_counts['sattvic']}  ", style="green")
        text.append(f"🟠 {guna_counts['rajasic']}  ", style="yellow")
        text.append(f"🔴 {guna_counts['tamasic']}", style="red")
        
        return Panel(text, title="🎭 Guna State", box=box.ROUNDED)
    
    def _build_events_table(self) -> Panel:
        """Build the events table."""
        table = Table(
            box=box.SIMPLE,
            expand=True,
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("Time", width=8)
        table.add_column("", width=2)  # Guna icon
        table.add_column("Type", width=12)
        table.add_column("Kosha", width=12)
        table.add_column("Agent", width=16)
        table.add_column("Details", ratio=1)
        
        for event in list(self.events)[-15:]:  # Show last 15
            # Time
            ts = event.timestamp[11:19] if len(event.timestamp) > 19 else event.timestamp[:8]
            
            # Guna icon
            guna_icon, guna_color = GUNA_DISPLAY.get(event.guna_state, ("⚪", "white"))
            
            # Event type with icon
            type_icon = EVENT_ICONS.get(event.event_type, "•")
            event_type = f"{type_icon} {event.event_type}"
            
            # Kosha with color
            kosha_color = KOSHA_COLORS.get(event.kosha_layer, "white")
            
            # Agent
            agent = event.agent_id or "system"
            if len(agent) > 16:
                agent = agent[:14] + "…"
            
            # Details from payload
            details = ""
            if isinstance(event.payload, dict):
                if "path" in event.payload:
                    details = event.payload["path"].split("/")[-1]
                elif "command" in event.payload:
                    cmd = event.payload["command"]
                    details = cmd[:30] + "…" if len(cmd) > 30 else cmd
                elif "topic" in event.payload:
                    details = event.payload["topic"]
                elif "type" in event.payload:
                    details = event.payload["type"]
                elif "reason" in event.payload:
                    details = event.payload["reason"]
            
            table.add_row(
                Text(ts, style="dim"),
                Text(guna_icon),
                Text(event_type),
                Text(event.kosha_layer, style=kosha_color),
                Text(agent, style="cyan"),
                Text(details, style="dim")
            )
        
        return Panel(table, title="📜 Event Stream", box=box.ROUNDED)
    
    def _build_stats_panel(self) -> Panel:
        """Build the statistics panel."""
        text = Text()
        
        if self.stats:
            text.append(f"Events (1h): {self.stats.get('total_events', 0)}\n", style="bold")
            
            by_type = self.stats.get('by_type', {})
            if by_type:
                text.append("\nBy Type:\n", style="bold dim")
                for t, count in list(by_type.items())[:5]:
                    icon = EVENT_ICONS.get(t, "•")
                    text.append(f"  {icon} {t}: {count}\n", style="dim")
            
            by_kosha = self.stats.get('by_kosha', {})
            if by_kosha:
                text.append("\nBy Kosha:\n", style="bold dim")
                for k, count in by_kosha.items():
                    if k:
                        color = KOSHA_COLORS.get(k, "white")
                        text.append(f"  {k}: ", style=color)
                        text.append(f"{count}\n", style="dim")
        else:
            text.append("No stats available", style="dim")
        
        return Panel(text, title="📊 Statistics", box=box.ROUNDED)
    
    def _build_layout(self) -> Layout:
        """Build the full layout."""
        layout = Layout()
        
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        layout["body"].split_row(
            Layout(name="main", ratio=3),
            Layout(name="sidebar", ratio=1)
        )
        
        layout["sidebar"].split(
            Layout(name="khaloree", size=5),
            Layout(name="guna", size=8),
            Layout(name="stats")
        )
        
        # Populate
        layout["header"].update(self._build_header())
        layout["main"].update(self._build_events_table())
        layout["khaloree"].update(self._build_khaloree_gauge())
        layout["guna"].update(self._build_guna_indicator())
        layout["stats"].update(self._build_stats_panel())
        
        footer_text = Text()
        footer_text.append(" q", style="bold")
        footer_text.append("=quit  ", style="dim")
        footer_text.append("p", style="bold")
        footer_text.append("=pause  ", style="dim")
        footer_text.append("r", style="bold")
        footer_text.append("=refresh  ", style="dim")
        footer_text.append("c", style="bold")
        footer_text.append("=clear", style="dim")
        layout["footer"].update(Panel(footer_text, box=box.ROUNDED))
        
        return layout
    
    def _read_fifo_events(self) -> List[PranaEvent]:
        """Read any pending events from FIFO (non-blocking)."""
        events = []
        fifo_path = get_fifo_path()
        
        if not fifo_path.exists():
            return events
        
        try:
            if not stat.S_ISFIFO(fifo_path.stat().st_mode):
                return events
        except Exception:
            return events
        
        try:
            fd = os.open(str(fifo_path), os.O_RDONLY | os.O_NONBLOCK)
            try:
                readable, _, _ = select.select([fd], [], [], 0)
                if readable:
                    data = os.read(fd, 8192)
                    if data:
                        for line in data.decode('utf-8').strip().split('\n'):
                            if line:
                                try:
                                    events.append(PranaEvent.from_json(line))
                                except Exception:
                                    pass
            finally:
                os.close(fd)
        except Exception:
            pass
        
        return events
    
    def run(self) -> None:
        """Run the TUI."""
        self.running = True
        
        with Live(self._build_layout(), console=self.console, refresh_per_second=2) as live:
            last_stats_refresh = time.time()
            
            while self.running:
                try:
                    # Check for new events from FIFO
                    if not self.paused:
                        new_events = self._read_fifo_events()
                        for event in new_events:
                            self.events.append(event)
                            if event.khalorēē_delta:
                                self.khaloree = max(0, min(100, self.khaloree + event.khalorēē_delta))
                    
                    # Refresh stats periodically
                    if time.time() - last_stats_refresh > 30:
                        try:
                            self.stats = get_event_stats(since="1 hour ago")
                            self.khaloree = get_current_khaloree()
                        except Exception:
                            pass
                        last_stats_refresh = time.time()
                    
                    # Update display
                    live.update(self._build_layout())
                    
                    # Brief sleep
                    time.sleep(0.5)
                
                except KeyboardInterrupt:
                    self.running = False
                    break


def run_tui() -> None:
    """Run the Prana TUI."""
    if not HAS_RICH:
        print("Rich library required. Install with: pip install rich")
        print("\nFallback: Showing recent events as plain text...\n")
        
        # Fallback to plain text
        try:
            events = get_recent_events(limit=20)
            khaloree = get_current_khaloree()
            
            print(f"KHALORĒĒ: {khaloree}/100")
            print("-" * 60)
            
            for event in reversed(events):
                ts = event.timestamp[11:19] if len(event.timestamp) > 19 else event.timestamp
                guna_icon = {"sattvic": "🟢", "rajasic": "🟠", "tamasic": "🔴"}.get(event.guna_state, "⚪")
                type_icon = EVENT_ICONS.get(event.event_type, "•")
                print(f"[{ts}] {guna_icon} {type_icon} {event.event_type:12} │ {event.kosha_layer:12}")
        except Exception as e:
            print(f"Error: {e}")
        
        return
    
    tui = PranaTUI()
    tui.run()


if __name__ == "__main__":
    run_tui()
