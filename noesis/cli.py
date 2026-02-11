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
