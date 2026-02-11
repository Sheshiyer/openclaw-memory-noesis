"""
Noesis CLI - Unified Command Line Interface
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commands:
    noesis init              Initialize (Sankalpa)
    noesis install           Full installation (Samskara)
    noesis health            System health check
    noesis drift             Detect pattern drift (Vikara)
    noesis context           Generate context for tier
    noesis teach             Teaching mode (Guru)
    noesis agents            List available agents
    noesis clock             Show Clifford Clock (8-hour octave)
    noesis moon              Show moon phase (Selemene)
    noesis telemetry         Prana Stream telemetry
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from noesis import __version__
from noesis.config import load_config, resolve_paths


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize the system (Sankalpa phase)."""
    from noesis.core.sankalpa import run_sankalpa
    
    config = load_config()
    config = resolve_paths(config)
    
    return run_sankalpa(config, verbose=args.verbose)


def cmd_install(args: argparse.Namespace) -> int:
    """Full installation (Samskara phase)."""
    from noesis.core.samskara import run_samskara
    
    config = load_config()
    config = resolve_paths(config)
    
    return run_samskara(
        config,
        agent=args.agent,
        tier=args.tier,
        verbose=args.verbose,
    )


def cmd_health(args: argparse.Namespace) -> int:
    """Run system health checks."""
    from noesis.core.health import run_health_check
    
    config = load_config()
    config = resolve_paths(config)
    
    return run_health_check(
        config,
        check=args.check,
        json_output=args.json,
        quick=args.quick,
    )


def cmd_drift(args: argparse.Namespace) -> int:
    """Detect pattern drift (Vikara)."""
    from noesis.core.vikara import run_drift_detection
    
    config = load_config()
    config = resolve_paths(config)
    
    return run_drift_detection(
        config,
        baseline=args.baseline,
        json_output=args.json,
    )


def cmd_context(args: argparse.Namespace) -> int:
    """Generate context for specified tier."""
    from noesis.core.context import run_context_generation
    
    config = load_config()
    config = resolve_paths(config)
    
    return run_context_generation(
        config,
        tier=args.tier,
        compress=args.compress,
        output=args.output,
    )


def cmd_teach(args: argparse.Namespace) -> int:
    """Teaching mode (Guru)."""
    from noesis.core.guru import run_teaching
    
    config = load_config()
    config = resolve_paths(config)
    
    return run_teaching(
        config,
        file=args.file,
        list_files=args.list,
    )


def cmd_agents(args: argparse.Namespace) -> int:
    """List available agents."""
    from noesis.core.agents import list_agents
    
    config = load_config()
    config = resolve_paths(config)
    
    return list_agents(config, verbose=args.verbose)


# ═══════════════════════════════════════════════════════════
# Temporal Commands (Clifford Clock & Moon)
# ═══════════════════════════════════════════════════════════

def cmd_clock(args: argparse.Namespace) -> int:
    """Show Clifford Clock state."""
    from noesis.telemetry import get_clifford_hour, format_clifford_clock
    import json as json_module
    
    state = get_clifford_hour()
    
    if args.json:
        print(json_module.dumps(state.to_dict(), indent=2))
    else:
        print(format_clifford_clock(state, ascii_art=not args.minimal))
    
    return 0


def cmd_moon(args: argparse.Namespace) -> int:
    """Show moon phase."""
    from noesis.telemetry import get_moon_phase, format_moon_phase
    import json as json_module
    
    state = get_moon_phase()
    
    if args.json:
        print(json_module.dumps(state.to_dict(), indent=2))
    else:
        print(format_moon_phase(state))
    
    return 0


def cmd_temporal(args: argparse.Namespace) -> int:
    """Show combined temporal state."""
    from noesis.telemetry import get_temporal_state, format_clifford_clock, format_moon_phase
    import json as json_module
    
    state = get_temporal_state()
    
    if args.json:
        print(json_module.dumps(state.to_dict(), indent=2))
    else:
        print(format_clifford_clock(state.clifford, ascii_art=True))
        print("\n")
        print(format_moon_phase(state.moon))
        print(f"\n🎭 Combined Guna: {state.combined_guna.value}")
    
    return 0


# ═══════════════════════════════════════════════════════════
# Telemetry Commands (Prana Stream)
# ═══════════════════════════════════════════════════════════

def cmd_telemetry_start(args: argparse.Namespace) -> int:
    """Start the Prana daemon."""
    from noesis.telemetry import start_daemon
    
    start_daemon(foreground=args.foreground)
    return 0


def cmd_telemetry_stop(args: argparse.Namespace) -> int:
    """Stop the Prana daemon."""
    from noesis.telemetry import stop_daemon
    
    stopped = stop_daemon()
    return 0 if stopped else 1


def cmd_telemetry_status(args: argparse.Namespace) -> int:
    """Show Prana daemon status."""
    from noesis.telemetry import daemon_status
    import json as json_module
    
    status = daemon_status()
    
    if args.json:
        print(json_module.dumps(status, indent=2))
    else:
        running = "🟢 running" if status["running"] else "🔴 stopped"
        print(f"Prana Daemon: {running}")
        if status["pid"]:
            print(f"PID: {status['pid']}")
        print(f"FIFO: {status['fifo_path']} ({'exists' if status['fifo_exists'] else 'missing'})")
    
    return 0


def cmd_telemetry_watch(args: argparse.Namespace) -> int:
    """Launch the Prana TUI dashboard."""
    from noesis.telemetry.tui import run_tui
    
    run_tui()
    return 0


def cmd_telemetry_query(args: argparse.Namespace) -> int:
    """Query telemetry events."""
    from noesis.telemetry import get_recent_events, get_session_events, search_events
    import json as json_module
    
    if args.session:
        events = get_session_events(args.session)
    elif args.search:
        events = search_events(args.search, since=args.since, limit=args.last)
    else:
        events = get_recent_events(
            limit=args.last,
            event_type=args.type,
            agent_id=args.agent,
            kosha_layer=args.kosha,
        )
    
    if args.json:
        print(json_module.dumps([e.to_dict() for e in events], indent=2))
    else:
        # Simple table output
        print(f"{'Time':8} {'Type':12} {'Kosha':12} {'Agent':16} {'Guna':8}")
        print("-" * 60)
        for e in events:
            ts = e.timestamp[11:19] if len(e.timestamp) > 19 else e.timestamp[:8]
            agent = (e.agent_id or "system")[:16]
            print(f"{ts:8} {e.event_type:12} {e.kosha_layer:12} {agent:16} {e.guna_state:8}")
    
    return 0


def cmd_telemetry_export(args: argparse.Namespace) -> int:
    """Export telemetry data."""
    from noesis.telemetry import export_events
    
    output = export_events(
        format=args.format,
        limit=args.last,
        since=args.since,
    )
    
    if args.output:
        Path(args.output).write_text(output)
        print(f"Exported to {args.output}")
    else:
        print(output)
    
    return 0


def cmd_telemetry_stats(args: argparse.Namespace) -> int:
    """Show telemetry statistics."""
    from noesis.telemetry import get_event_stats, get_current_khaloree
    import json as json_module
    
    stats = get_event_stats(since=args.since)
    
    if args.json:
        print(json_module.dumps(stats, indent=2))
    else:
        print(f"📊 Prana Stream Statistics")
        print(f"{'═' * 40}")
        print(f"Total Events: {stats['total_events']}")
        print(f"Khalorēē Balance: {stats['current_khaloree']}/100")
        print(f"Khalorēē Delta: {stats['khaloree_delta']:+d}")
        print()
        
        if stats['by_type']:
            print("By Type:")
            for t, count in stats['by_type'].items():
                print(f"  {t}: {count}")
        
        if stats['by_kosha']:
            print("\nBy Kosha:")
            for k, count in stats['by_kosha'].items():
                if k:
                    print(f"  {k}: {count}")
        
        if stats['by_guna']:
            print("\nBy Guna:")
            for g, count in stats['by_guna'].items():
                if g:
                    icon = {"sattvic": "🟢", "rajasic": "🟠", "tamasic": "🔴"}.get(g, "⚪")
                    print(f"  {icon} {g}: {count}")
    
    return 0


# ═══════════════════════════════════════════════════════════
# Engine commands (Selemene)
# ═══════════════════════════════════════════════════════════

def cmd_engines(args: argparse.Namespace) -> int:
    """Show Selemene engine dashboard."""
    from noesis.telemetry import (
        Engine, get_engine_tracker, get_engine_metadata,
        format_engine_dashboard, format_engine_status
    )
    import json as json_module
    
    tracker = get_engine_tracker()
    
    if args.json:
        summary = tracker.to_summary()
        states = {e.value: tracker.get_state(e).to_dict() for e in Engine}
        print(json_module.dumps({"summary": summary, "engines": states}, indent=2))
        return 0
    
    # Filter by kosha if requested
    if args.kosha:
        engines = tracker.get_by_kosha(args.kosha)
        if not engines:
            print(f"No engines aligned with {args.kosha}")
            return 1
        
        print(f"⚙️ Engines aligned with {args.kosha.upper()}")
        print("=" * 50)
        for state in engines:
            if args.verbose:
                print(format_engine_status(state))
                print()
            else:
                meta = state.metadata
                icon = meta.symbol
                status = {"idle": "⚪", "calling": "🔄", "success": "✅", "error": "❌", "timeout": "⏱️"}.get(state.status, "❓")
                print(f"  {icon} {meta.name:20} {status} {state.call_count} calls")
        return 0
    
    # Full dashboard
    print(format_engine_dashboard())
    
    if args.verbose:
        print()
        for engine in Engine:
            state = tracker.get_state(engine)
            print(format_engine_status(state))
            print()
    
    return 0


def cmd_engine_detail(args: argparse.Namespace) -> int:
    """Show details for a single engine."""
    from noesis.telemetry import (
        Engine, get_engine_tracker, get_engine_metadata, format_engine_status
    )
    import json as json_module
    
    # Find engine by name
    try:
        engine = Engine(args.name)
    except ValueError:
        # Try partial match
        matches = [e for e in Engine if args.name.lower() in e.value.lower()]
        if len(matches) == 1:
            engine = matches[0]
        elif len(matches) > 1:
            print(f"Ambiguous engine name '{args.name}'. Matches: {', '.join(e.value for e in matches)}")
            return 1
        else:
            print(f"Unknown engine '{args.name}'. Available: {', '.join(e.value for e in Engine)}")
            return 1
    
    tracker = get_engine_tracker()
    state = tracker.get_state(engine)
    meta = state.metadata
    
    if args.json:
        data = {
            **state.to_dict(),
            "metadata": {
                "name": meta.name,
                "kosha_layer": meta.kosha_layer,
                "description": meta.description,
                "requires_birth_data": meta.requires_birth_data,
                "requires_birth_time": meta.requires_birth_time,
                "requires_location": meta.requires_location,
                "api_path": meta.api_path,
                "kernel_refs": meta.kernel_refs,
            }
        }
        print(json_module.dumps(data, indent=2))
        return 0
    
    # Detailed output
    print(f"{meta.symbol} {meta.name}")
    print("=" * 50)
    print(f"  Engine ID: {engine.value}")
    print(f"  Kosha Layer: {meta.kosha_layer.capitalize()}")
    print(f"  Description: {meta.description}")
    print()
    print(f"  Status: {state.status.upper()}")
    print(f"  Calls: {state.call_count} (errors: {state.error_count})")
    if state.last_called:
        print(f"  Last Called: {state.last_called.strftime('%Y-%m-%d %H:%M:%S')}")
    if state.avg_latency_ms > 0:
        print(f"  Avg Latency: {state.avg_latency_ms:.0f}ms")
    print()
    print("  Requirements:")
    print(f"    Birth Data: {'✓' if meta.requires_birth_data else '✗'}")
    print(f"    Birth Time: {'✓' if meta.requires_birth_time else '✗'}")
    print(f"    Location: {'✓' if meta.requires_location else '✗'}")
    print()
    print(f"  API Path: {meta.api_path}")
    if meta.kernel_refs:
        print(f"  Kernel Refs: {', '.join(meta.kernel_refs)}")
    
    return 0


# ═══════════════════════════════════════════════════════════
# Ritual & Polarity commands
# ═══════════════════════════════════════════════════════════

def cmd_rituals(args: argparse.Namespace) -> int:
    """Show ritual/cron history."""
    from noesis.telemetry import (
        get_ritual_tracker, format_ritual_list, Vayu, RitualType
    )
    import json as json_module
    
    tracker = get_ritual_tracker()
    
    # Filter rituals
    if args.vayu:
        try:
            vayu = Vayu(args.vayu)
            rituals = tracker.get_by_vayu(vayu)
        except ValueError:
            print(f"Unknown vayu: {args.vayu}. Options: {', '.join(v.value for v in Vayu)}")
            return 1
    elif args.type:
        try:
            rtype = RitualType(args.type)
            rituals = tracker.get_by_type(rtype)
        except ValueError:
            print(f"Unknown type: {args.type}. Options: {', '.join(t.value for t in RitualType)}")
            return 1
    elif args.today:
        rituals = tracker.get_today()
    else:
        rituals = tracker.get_recent(args.limit)
    
    if args.json:
        data = {
            "summary": tracker.to_summary(),
            "rituals": [r.to_dict() for r in rituals]
        }
        print(json_module.dumps(data, indent=2))
        return 0
    
    # Summary first
    summary = tracker.to_summary()
    print(f"📿 Ritual Tracker")
    print(f"{'═' * 50}")
    print(f"  Today: {summary['today_success']}✅ {summary['today_failed']}❌ │ Khalorēē: {summary['total_khalorēē_delta']:+d}")
    print()
    
    # Ritual list
    print(format_ritual_list(rituals, args.limit))
    
    return 0


def cmd_vayus(args: argparse.Namespace) -> int:
    """Show the 5 Vayus (vital airs)."""
    from noesis.telemetry import Vayu, VAYU_REGISTRY, format_vayu_list
    import json as json_module
    
    if args.json:
        data = {
            v.value: {
                "name": m.name,
                "location": m.location,
                "function": m.function,
                "breathwork": m.breathwork,
                "kosha_effect": m.kosha_effect,
            }
            for v, m in VAYU_REGISTRY.items()
        }
        print(json_module.dumps(data, indent=2))
        return 0
    
    print(format_vayu_list())
    
    # If specific vayu requested
    if args.name:
        try:
            vayu = Vayu(args.name)
            meta = VAYU_REGISTRY[vayu]
            print()
            print(f"{meta.symbol} {meta.name} Details")
            print(f"{'─' * 40}")
            print(f"  Location: {meta.location}")
            print(f"  Function: {meta.function}")
            print(f"  Breathwork: {meta.breathwork}")
            print(f"  Kosha Effect: {meta.kosha_effect}")
        except ValueError:
            print(f"\nUnknown vayu: {args.name}")
            return 1
    
    return 0


def cmd_polarity(args: argparse.Namespace) -> int:
    """Show Guardrail Dyad balance."""
    from noesis.telemetry import get_polarity, shift_polarity, format_polarity_gauge
    import json as json_module
    
    # Handle shift command
    if args.shift:
        if args.shift not in ("aletheios", "pichet"):
            print(f"Invalid shift target: {args.shift}. Use 'aletheios' or 'pichet'")
            return 1
        amount = args.amount if hasattr(args, 'amount') and args.amount else 5.0
        shift_polarity(args.shift, amount, args.reason or "manual adjustment")
        print(f"✓ Shifted polarity toward {args.shift} by {amount}%")
    
    state = get_polarity()
    
    if args.json:
        print(json_module.dumps(state.to_dict(), indent=2))
        return 0
    
    print(format_polarity_gauge(state))
    
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="noesis",
        description="Tryambakam Noesis - Consciousness architecture kernel for AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  noesis init                    # Initialize system
  noesis install --agent chitta-weaver
  noesis health --quick
  noesis context --tier core
  noesis teach SOUL.md
        """,
    )
    
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"noesis {__version__}",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # init
    init_parser = subparsers.add_parser("init", help="Initialize (Sankalpa)")
    init_parser.set_defaults(func=cmd_init)
    
    # install
    install_parser = subparsers.add_parser("install", help="Full installation (Samskara)")
    install_parser.add_argument("--agent", "-a", help="Agent to bind to")
    install_parser.add_argument(
        "--tier", "-t",
        choices=["lite", "core", "standard", "full"],
        default="core",
        help="Context tier (default: core)",
    )
    install_parser.set_defaults(func=cmd_install)
    
    # health
    health_parser = subparsers.add_parser("health", help="System health check")
    health_parser.add_argument("--check", "-c", help="Run specific check only")
    health_parser.add_argument("--json", action="store_true", help="Output as JSON")
    health_parser.add_argument("--quick", "-q", action="store_true", help="Quick check")
    health_parser.set_defaults(func=cmd_health)
    
    # drift
    drift_parser = subparsers.add_parser("drift", help="Detect pattern drift (Vikara)")
    drift_parser.add_argument("--baseline", "-b", action="store_true", help="Create baseline")
    drift_parser.add_argument("--json", action="store_true", help="Output as JSON")
    drift_parser.set_defaults(func=cmd_drift)
    
    # context
    context_parser = subparsers.add_parser("context", help="Generate context")
    context_parser.add_argument(
        "--tier", "-t",
        choices=["lite", "core", "standard", "full"],
        default="core",
        help="Context tier (default: core)",
    )
    context_parser.add_argument("--compress", action="store_true", help="Compress output")
    context_parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    context_parser.set_defaults(func=cmd_context)
    
    # teach
    teach_parser = subparsers.add_parser("teach", help="Teaching mode (Guru)")
    teach_parser.add_argument("file", nargs="?", help="File to teach about")
    teach_parser.add_argument("--list", "-l", action="store_true", help="List teachable files")
    teach_parser.set_defaults(func=cmd_teach)
    
    # agents
    agents_parser = subparsers.add_parser("agents", help="List available agents")
    agents_parser.set_defaults(func=cmd_agents)
    
    # ═══════════════════════════════════════════════════════════
    # Temporal commands (Clifford Clock & Moon)
    # ═══════════════════════════════════════════════════════════
    
    # clock
    clock_parser = subparsers.add_parser("clock", help="Show Clifford Clock (8-hour octave)")
    clock_parser.add_argument("--json", action="store_true", help="Output as JSON")
    clock_parser.add_argument("--minimal", "-m", action="store_true", help="Minimal output (no ASCII)")
    clock_parser.set_defaults(func=cmd_clock)
    
    # moon
    moon_parser = subparsers.add_parser("moon", help="Show moon phase (Selemene)")
    moon_parser.add_argument("--json", action="store_true", help="Output as JSON")
    moon_parser.set_defaults(func=cmd_moon)
    
    # temporal (combined)
    temporal_parser = subparsers.add_parser("temporal", help="Show combined temporal state")
    temporal_parser.add_argument("--json", action="store_true", help="Output as JSON")
    temporal_parser.set_defaults(func=cmd_temporal)
    
    # ═══════════════════════════════════════════════════════════
    # Telemetry subcommands
    # ═══════════════════════════════════════════════════════════
    
    telemetry_parser = subparsers.add_parser(
        "telemetry", 
        help="Prana Stream telemetry",
        aliases=["tele", "prana"],
    )
    telemetry_sub = telemetry_parser.add_subparsers(dest="telemetry_cmd", help="Telemetry commands")
    
    # telemetry start
    tele_start = telemetry_sub.add_parser("start", help="Start Prana daemon")
    tele_start.add_argument("--foreground", "-f", action="store_true", help="Run in foreground")
    tele_start.set_defaults(func=cmd_telemetry_start)
    
    # telemetry stop
    tele_stop = telemetry_sub.add_parser("stop", help="Stop Prana daemon")
    tele_stop.set_defaults(func=cmd_telemetry_stop)
    
    # telemetry status
    tele_status = telemetry_sub.add_parser("status", help="Show daemon status")
    tele_status.add_argument("--json", action="store_true", help="Output as JSON")
    tele_status.set_defaults(func=cmd_telemetry_status)
    
    # telemetry watch
    tele_watch = telemetry_sub.add_parser("watch", help="Live TUI dashboard")
    tele_watch.set_defaults(func=cmd_telemetry_watch)
    
    # telemetry query
    tele_query = telemetry_sub.add_parser("query", help="Query events")
    tele_query.add_argument("--last", "-n", type=int, default=50, help="Number of events")
    tele_query.add_argument("--session", "-s", help="Filter by session ID")
    tele_query.add_argument("--type", "-t", help="Filter by event type")
    tele_query.add_argument("--agent", "-a", help="Filter by agent")
    tele_query.add_argument("--kosha", "-k", help="Filter by kosha layer")
    tele_query.add_argument("--since", help="Time filter (e.g., '1 hour ago')")
    tele_query.add_argument("--search", help="Search in payload")
    tele_query.add_argument("--json", action="store_true", help="Output as JSON")
    tele_query.set_defaults(func=cmd_telemetry_query)
    
    # telemetry export
    tele_export = telemetry_sub.add_parser("export", help="Export events")
    tele_export.add_argument("--format", "-f", choices=["json", "csv"], default="json")
    tele_export.add_argument("--last", "-n", type=int, default=1000, help="Number of events")
    tele_export.add_argument("--since", help="Time filter")
    tele_export.add_argument("--output", "-o", help="Output file")
    tele_export.set_defaults(func=cmd_telemetry_export)
    
    # telemetry stats
    tele_stats = telemetry_sub.add_parser("stats", help="Show statistics")
    tele_stats.add_argument("--since", default="1 hour ago", help="Time range")
    tele_stats.add_argument("--json", action="store_true", help="Output as JSON")
    tele_stats.set_defaults(func=cmd_telemetry_stats)
    
    # ═══════════════════════════════════════════════════════════
    # Engine commands (Selemene)
    # ═══════════════════════════════════════════════════════════
    
    # engines (main command)
    engines_parser = subparsers.add_parser("engines", help="Selemene engine status")
    engines_parser.add_argument("--json", action="store_true", help="Output as JSON")
    engines_parser.add_argument("--kosha", "-k", help="Filter by kosha layer")
    engines_parser.add_argument("--verbose", "-v", action="store_true", help="Show full details")
    engines_parser.set_defaults(func=cmd_engines)
    
    # engine (info on single engine)
    engine_parser = subparsers.add_parser("engine", help="Single engine details")
    engine_parser.add_argument("name", help="Engine name (e.g., panchanga, biorhythm)")
    engine_parser.add_argument("--json", action="store_true", help="Output as JSON")
    engine_parser.set_defaults(func=cmd_engine_detail)
    
    # ═══════════════════════════════════════════════════════════
    # Ritual & Polarity commands
    # ═══════════════════════════════════════════════════════════
    
    # rituals
    rituals_parser = subparsers.add_parser("rituals", help="Ritual/cron history")
    rituals_parser.add_argument("--limit", "-n", type=int, default=20, help="Number to show")
    rituals_parser.add_argument("--today", action="store_true", help="Show today only")
    rituals_parser.add_argument("--vayu", "-v", help="Filter by vayu (prana, apana, etc.)")
    rituals_parser.add_argument("--type", "-t", help="Filter by type (breathwork, cron_job, etc.)")
    rituals_parser.add_argument("--json", action="store_true", help="Output as JSON")
    rituals_parser.set_defaults(func=cmd_rituals)
    
    # vayus
    vayus_parser = subparsers.add_parser("vayus", help="Show the 5 Vayus (vital airs)")
    vayus_parser.add_argument("name", nargs="?", help="Specific vayu to show details")
    vayus_parser.add_argument("--json", action="store_true", help="Output as JSON")
    vayus_parser.set_defaults(func=cmd_vayus)
    
    # polarity
    polarity_parser = subparsers.add_parser("polarity", help="Guardrail Dyad balance")
    polarity_parser.add_argument("--shift", help="Shift toward: aletheios or pichet")
    polarity_parser.add_argument("--amount", type=float, default=5.0, help="Shift amount (default: 5)")
    polarity_parser.add_argument("--reason", help="Reason for shift")
    polarity_parser.add_argument("--json", action="store_true", help="Output as JSON")
    polarity_parser.set_defaults(func=cmd_polarity)
    
    return parser


def main(argv: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Handle telemetry subcommands
    if args.command in ("telemetry", "tele", "prana"):
        if not hasattr(args, 'telemetry_cmd') or not args.telemetry_cmd:
            # Show telemetry help
            parser.parse_args([args.command, "--help"])
            return 0
    
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
    except Exception as e:
        if args.verbose:
            raise
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
