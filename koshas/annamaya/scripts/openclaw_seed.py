#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from openclaw_seed_helpers import copy_file, expand_path, safe_slug
from prana import PranaSystem


def _require_rich():
    try:
        from rich.console import Console
        from rich.prompt import Prompt
    except Exception as e:
        raise RuntimeError(
            "Missing dependency: rich. Install with: python3 -m pip install --user rich"
        ) from e
    return Console(), Prompt


def _default_prana_target(platform: str) -> Path:
    platform = platform.lower()
    if platform == "claude":
        return Path.home() / ".claude" / "openclaw_context.md"
    if platform == "cursor":
        return Path.cwd() / ".cursorrules"
    return Path.home() / ".openclaw" / "CONTEXT.md"


def cmd_install(_: argparse.Namespace) -> int:
    console, _ = _require_rich()
    try:
        from setup_openclaw import onboarding_wizard
    except Exception as e:
        console.print(f"[red]Failed to load setup_openclaw.py:[/red] {e}")
        return 1
    onboarding_wizard()
    return 0


def cmd_prana(args: argparse.Namespace) -> int:
    root = expand_path(args.root)
    platform = args.platform.lower()
    out_path = expand_path(args.out) if args.out else _default_prana_target(platform)

    prana_system = PranaSystem(str(root))
    prana_system.manifest(str(out_path), platform=platform)
    return 0


def _agents_dir(root: Path) -> Path:
    return root / "koshas" / "annamaya" / "agents"


def cmd_scaffold_agent(args: argparse.Namespace) -> int:
    root = expand_path(args.root)
    agent_slug = safe_slug(args.name)

    template_agent = safe_slug(args.template_agent)
    template_models = _agents_dir(root) / template_agent / "agent" / "models.json"
    if not template_models.exists():
        raise FileNotFoundError(f"Template models.json not found: {template_models}")

    out_dir = _agents_dir(root) / agent_slug / "agent"
    out_models = out_dir / "models.json"
    if out_models.exists() and not args.force:
        raise FileExistsError(f"Refusing to overwrite existing file: {out_models}")

    copy_file(template_models, out_models)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    console, _ = _require_rich()
    root = expand_path(args.root)
    ok = True

    console.print("[bold]OpenClaw Seed Doctor[/bold]")

    try:
        import rich
        console.print("✅ rich import")
    except Exception as e:
        ok = False
        console.print(f"❌ rich import: {e}")

    prana_paths_ok = (root / "koshas" / "layer0" / "kernel").exists()
    if prana_paths_ok:
        console.print(f"✅ vault root looks valid: {root}")
    else:
        ok = False
        console.print(f"❌ vault root missing expected paths: {root}")

    openclaw_dir = Path.home() / ".openclaw"
    if openclaw_dir.exists():
        console.print(f"✅ ~/.openclaw exists: {openclaw_dir}")
    else:
        console.print(f"ℹ️  ~/.openclaw not found: {openclaw_dir}")

    return 0 if ok else 1


def tui_menu() -> int:
    console, Prompt = _require_rich()

    console.print("[bold magenta]OpenClaw Seed[/bold magenta]")
    action = Prompt.ask(
        "Choose action",
        choices=["install", "prana", "scaffold-agent", "doctor", "exit"],
        default="install",
    )
    if action == "exit":
        return 0

    if action == "install":
        return cmd_install(argparse.Namespace())

    if action == "doctor":
        root = Prompt.ask("Vault root", default=str(Path.cwd()))
        return cmd_doctor(argparse.Namespace(root=root))

    if action == "prana":
        root = Prompt.ask("Vault root", default=str(Path.cwd()))
        platform = Prompt.ask("Platform", choices=["claude", "cursor", "generic"], default="claude")
        out = Prompt.ask("Output path (blank = default)", default="")
        out_value = out.strip() or None
        return cmd_prana(argparse.Namespace(root=root, platform=platform, out=out_value))

    if action == "scaffold-agent":
        root = Prompt.ask("Vault root", default=str(Path.cwd()))
        name = Prompt.ask("New agent name (folder slug)")
        template_agent = Prompt.ask("Template agent", default="pi")
        force = Prompt.ask("Overwrite if exists?", choices=["no", "yes"], default="no") == "yes"
        return cmd_scaffold_agent(
            argparse.Namespace(root=root, name=name, template_agent=template_agent, force=force)
        )

    raise RuntimeError(f"Unknown action: {action}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openclaw-seed")
    sub = parser.add_subparsers(dest="cmd", required=False)

    sub.add_parser("install")

    prana_p = sub.add_parser("prana")
    prana_p.add_argument("--root", default=".")
    prana_p.add_argument("--platform", choices=["claude", "cursor", "generic"], default="claude")
    prana_p.add_argument("--out")

    scaffold_p = sub.add_parser("scaffold-agent")
    scaffold_p.add_argument("name")
    scaffold_p.add_argument("--root", default=".")
    scaffold_p.add_argument("--template-agent", default="pi")
    scaffold_p.add_argument("--force", action="store_true")

    doctor_p = sub.add_parser("doctor")
    doctor_p.add_argument("--root", default=".")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.cmd:
        return tui_menu()

    if args.cmd == "install":
        return cmd_install(args)
    if args.cmd == "prana":
        return cmd_prana(args)
    if args.cmd == "scaffold-agent":
        return cmd_scaffold_agent(args)
    if args.cmd == "doctor":
        return cmd_doctor(args)

    raise RuntimeError(f"Unknown command: {args.cmd}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        try:
            console, _ = _require_rich()
            console.print("\n[red]Interrupted.[/red]")
        except Exception:
            print("\nInterrupted.", file=sys.stderr)
        raise SystemExit(130)
