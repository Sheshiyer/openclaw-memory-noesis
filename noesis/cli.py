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
    
    return parser


def main(argv: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
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
