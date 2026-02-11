#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Track
from rich.markdown import Markdown
from rich.layout import Layout
from rich import print as rprint

# Import the Prana System
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from prana import PranaSystem

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_step(step_num, total_steps, title):
    console.print(f"\n[bold cyan]Step {step_num}/{total_steps}[/bold cyan]: [bold white]{title}[/bold white]")
    console.print("─" * 40, style="dim")

def onboarding_wizard():
    clear_screen()
    
    # --- STEP 1: WELCOME ---
    console.print(Panel.fit(
        "[bold magenta]OPENCLAW FRAMEWORK[/bold magenta]\n"
        "[dim]Personal Agentic Infrastructure & Prana Installation[/dim]",
        border_style="magenta"
    ))
    time.sleep(1)
    
    config = {}
    total_steps = 15
    
    # --- STEP 2: IDENTITY ---
    print_step(2, total_steps, "Identity Verification")
    config['user_name'] = Prompt.ask("Who enters the circle?", default=os.getenv("USER", "User"))
    
    # --- STEP 3: ARCHETYPE ---
    print_step(3, total_steps, "Archetype Selection")
    archetypes = ["Alchemist", "Engineer", "Writer", "Scholar", "None"]
    config['archetype'] = Prompt.ask("What is your function?", choices=archetypes, default="Alchemist")
    
    # --- STEP 4: PLATFORM ---
    print_step(4, total_steps, "Manifestation Layer")
    platforms = ["Claude Code", "Cursor", "Windsurf", "Terminal (CLI)", "Custom"]
    config['platform'] = Prompt.ask("Where shall we manifest?", choices=platforms, default="Claude Code")
    
    # --- STEP 5: ROOT PATH ---
    print_step(5, total_steps, "Source Verification")
    default_root = os.getcwd()
    config['root_path'] = Prompt.ask("Is this the Source (Root Path)?", default=default_root)
    
    # --- STEP 6: PRANA STREAMS ---
    print_step(6, total_steps, "Prana Streams")
    console.print("[dim]Select which knowledge streams to imbibe into the agent.[/dim]")
    streams = []
    if Confirm.ask("Ingest Identity (Soul/User/Identity)?", default=True): streams.append("identity")
    if Confirm.ask("Ingest Cosmology (Kha/Bha/Lha)?", default=True): streams.append("cosmology")
    if Confirm.ask("Ingest Operational Protocols?", default=True): streams.append("operational")
    config['streams'] = streams
    
    # --- STEP 7: AGENT NAME ---
    print_step(7, total_steps, "Vessel Naming")
    config['agent_name'] = Prompt.ask("Name your agentic vessel", default="OpenClaw")
    
    # --- STEP 8: MISSION ---
    print_step(8, total_steps, "Teleology (Mission)")
    config['mission'] = Prompt.ask("Define the primary goal", default="To evolve the field and execute tasks autonomously.")
    
    # --- STEP 9: VOICE ---
    print_step(9, total_steps, "Tone of Transmission")
    config['voice'] = Prompt.ask("Select voice style", choices=["Formal", "Casual", "Mystic", "Concise"], default="Mystic")
    
    # --- STEP 10: MEMORY ---
    print_step(10, total_steps, "Persistence Mode")
    config['memory_mode'] = Prompt.ask("Memory persistence strategy", choices=["Markdown (Flat File)", "Vector DB", "None"], default="Markdown (Flat File)")
    
    # --- STEP 11: HOOKS ---
    print_step(11, total_steps, "Autonomic Reflexes")
    config['enable_hooks'] = Confirm.ask("Enable event-driven hooks (git, startup, exit)?", default=True)
    
    # --- STEP 12: GUARDRAILS ---
    print_step(12, total_steps, "Safety Protocols")
    config['guardrails'] = Confirm.ask("Enable safety guardrails (confirmation before execution)?", default=True)
    
    # --- STEP 13: TOOLS ---
    print_step(13, total_steps, "External Agency")
    config['enable_tools'] = Confirm.ask("Grant access to system tools (File I/O, Shell)?", default=True)
    
    # --- STEP 14: REVIEW ---
    print_step(14, total_steps, "Ritual Confirmation")
    console.print(Panel(
        f"[bold]User:[/bold] {config['user_name']}\n"
        f"[bold]Agent:[/bold] {config['agent_name']} ({config['archetype']})\n"
        f"[bold]Platform:[/bold] {config['platform']}\n"
        f"[bold]Streams:[/bold] {', '.join(config['streams'])}\n"
        f"[bold]Mission:[/bold] {config['mission']}",
        title="Configuration Manifest",
        border_style="green"
    ))
    if not Confirm.ask("Proceed with Prana Prathistaapana (Installation)?"):
        console.print("[red]Aborted.[/red]")
        sys.exit(0)
        
    # --- STEP 15: INSTALLATION ---
    print_step(15, total_steps, "Prana Prathistaapana")
    
    # 1. Initialize System
    with console.status("[bold green]Initializing OpenClaw System...[/bold green]") as status:
        time.sleep(1)
        # Create directories
        base_dir = Path.home() / ".openclaw"
        base_dir.mkdir(exist_ok=True)
        (base_dir / "hooks").mkdir(exist_ok=True)
        (base_dir / "memory").mkdir(exist_ok=True)
        (base_dir / "config").mkdir(exist_ok=True)
        
        # Save Config
        with open(base_dir / "config" / "settings.json", "w") as f:
            import json
            json.dump(config, f, indent=2)
            
    console.print("✅ [green]Structure Created at ~/.openclaw[/green]")
    
    # 2. Invoke Prana
    with console.status("[bold blue]Gathering Prana from Root...[/bold blue]") as status:
        prana_system = PranaSystem(config['root_path'])
        # Only gather selected streams (mocking filter for now, PranaSystem gathers all by default but we can select later)
        prana_content = prana_system.gather_prana()
        
        # Manifest
        if config['platform'] == "Claude Code":
            target = Path.home() / ".claude" / "openclaw_context.md"
            target.parent.mkdir(exist_ok=True)
            prana_system.manifest(str(target), platform="claude")
            console.print(f"✅ [green]Prana injected into {target}[/green]")
            
        elif config['platform'] == "Cursor":
            target = Path(config['root_path']) / ".cursorrules"
            prana_system.manifest(str(target), platform="cursor")
            console.print(f"✅ [green]Prana manifest as {target}[/green]")
            
        else:
            target = base_dir / "CONTEXT.md"
            prana_system.manifest(str(target), platform="generic")
            console.print(f"✅ [green]Prana stored at {target}[/green]")
            
    # Final Message
    console.print("\n[bold magenta]✨ PRANA PRATHISTAAPANA COMPLETE ✨[/bold magenta]")
    console.print(f"The vessel [bold]{config['agent_name']}[/bold] is now ensouled with your knowledge.")
    console.print("Run 'openclaw' (hypothetically) to begin.")

if __name__ == "__main__":
    try:
        onboarding_wizard()
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted.[/red]")
