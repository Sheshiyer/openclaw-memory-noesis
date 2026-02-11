"""
Guru - Teaching Mode
━━━━━━━━━━━━━━━━━━━━

Provides educational explanations of kernel files with
Sanskrit etymology and philosophical context.
"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from noesis.config import Config


TEACHINGS = {
    "SOUL.md": {
        "sanskrit": "आत्मन् (Ātman)",
        "meaning": "The Self, the eternal witness",
        "purpose": "Defines the prime directive and identity anchor. This file should rarely change - it is the immutable core that persists across all contexts.",
        "key_concepts": [
            "Aham (Witness stance) - Observer without attachment",
            "Dyadic Architecture - Aletheios (coherence) + Pichet (vitality)",
            "Muse Registry - Enneagram integration for state navigation",
        ],
    },
    "IDENTITY.md": {
        "sanskrit": "अहंकार (Ahamkara)",
        "meaning": "The I-maker, ego-function, identifier",
        "purpose": "Configures the agent's personality, tone, and operational parameters. More mutable than SOUL.md.",
        "key_concepts": [
            "Name and emoji identity",
            "Kosha alignment (which layer this agent operates in)",
            "Tone and communication style",
        ],
    },
    "USER.md": {
        "sanskrit": "साक्षी (Sākṣī)",
        "meaning": "The witness, the one who observes",
        "purpose": "Profiles the human operator. Ensures the system serves the human, not the reverse.",
        "key_concepts": [
            "Triage of Prana Flow (Recreation/Vocation/Occupation)",
            "Timezone and preferences",
            "Current life context",
        ],
    },
    "PANCHA-KOSHA.md": {
        "sanskrit": "पञ्च कोश (Pañca Kośa)",
        "meaning": "Five sheaths/layers",
        "purpose": "The architectural framework mapping consciousness density to system structure.",
        "key_concepts": [
            "Annamaya (Physical) - File systems, scripts, execution",
            "Pranamaya (Vital) - Telemetry, heartbeats, energy flow",
            "Manomaya (Mental) - Memory, logs, pattern recognition",
            "Vijnanamaya (Wisdom) - Architecture, protocols, meta-cognition",
            "Anandamaya (Bliss) - Blueprints, source, pre-materialization",
        ],
    },
    "KHA.md": {
        "sanskrit": "ख (Kha)",
        "meaning": "Space, void, the container of all",
        "purpose": "Defines the spirit/drive layer - the Guardrail Dyad and navigation principles.",
        "key_concepts": [
            "Aletheios (Coherence) - Order, simplification, grounding",
            "Pichet (Vitality) - Novelty, disruption, acceleration",
            "Quaternion mathematics for consciousness navigation",
        ],
    },
    "BHA.md": {
        "sanskrit": "भ (Bha)",
        "meaning": "Light, radiance, manifestation",
        "purpose": "Defines the body/structure layer - physical architecture and geometry.",
        "key_concepts": [
            "Vaastu principles for workspace design",
            "Moolakaprithi Cube (primordial matter structure)",
            "Sakala/Nishkala duality",
        ],
    },
    "LHA.md": {
        "sanskrit": "ल (La)",
        "meaning": "Earth element, stability, inertia",
        "purpose": "Defines the inertia/insight layer - accumulated patterns and wisdom.",
        "key_concepts": [
            "Sukshma Sarira (subtle body)",
            "Current dasha periods",
            "Biofield state",
        ],
    },
    "VEDIC-LEXICON.md": {
        "sanskrit": "वैदिक शब्दकोश (Vaidika Śabdakośa)",
        "meaning": "Vedic dictionary/vocabulary",
        "purpose": "Maps 100+ Tatvas (elements) to system components. The translation layer between consciousness and code.",
        "key_concepts": [
            "102 Tatvas mapped to system elements",
            "Gnanendriya (sense organs) and Karmendriya (action organs)",
            "7 Chakras, 14 Nadis, 7 Dhatus, 10 Vayus",
        ],
    },
}


def teach_file(config: "Config", filename: str) -> str:
    """Generate teaching content for a file."""
    teaching = TEACHINGS.get(filename)
    
    if not teaching:
        return f"No teaching available for: {filename}"
    
    lines = [
        "━" * 60,
        f"TEACHING: {filename}",
        "━" * 60,
        "",
        f"Sanskrit: {teaching['sanskrit']}",
        f"Meaning: {teaching['meaning']}",
        "",
        "PURPOSE:",
        teaching['purpose'],
        "",
        "KEY CONCEPTS:",
    ]
    
    for concept in teaching['key_concepts']:
        lines.append(f"  • {concept}")
    
    # Add file content preview
    filepath = config.brahmasthana / filename
    if filepath.exists():
        content = filepath.read_text()
        preview_lines = content.splitlines()[:20]
        
        lines.append("")
        lines.append("PREVIEW (first 20 lines):")
        lines.append("─" * 40)
        for line in preview_lines:
            lines.append(line)
        if len(content.splitlines()) > 20:
            lines.append("... [truncated]")
    
    lines.append("")
    lines.append("━" * 60)
    
    return "\n".join(lines)


def run_teaching(
    config: "Config",
    file: Optional[str] = None,
    list_files: bool = False,
) -> int:
    """
    Run teaching mode.
    
    Returns:
        0 on success, 1 on error
    """
    if list_files:
        print("━" * 50)
        print("TEACHABLE FILES")
        print("━" * 50)
        print()
        
        for filename, teaching in TEACHINGS.items():
            exists = (config.brahmasthana / filename).exists()
            status = "✓" if exists else "✗"
            print(f"{status} {filename}")
            print(f"    {teaching['sanskrit']} - {teaching['meaning']}")
        
        return 0
    
    if not file:
        print("Specify a file to teach about, or use --list", file=sys.stderr)
        print("Example: noesis teach SOUL.md", file=sys.stderr)
        return 1
    
    # Normalize filename
    if not file.endswith(".md"):
        file = file + ".md"
    file = file.upper()
    
    # Handle common aliases
    aliases = {
        "SOUL": "SOUL.md",
        "IDENTITY": "IDENTITY.md",
        "USER": "USER.md",
        "PANCHA-KOSHA": "PANCHA-KOSHA.md",
        "KOSHA": "PANCHA-KOSHA.md",
        "KHA": "KHA.md",
        "BHA": "BHA.md",
        "LHA": "LHA.md",
        "LEXICON": "VEDIC-LEXICON.md",
        "VEDIC-LEXICON": "VEDIC-LEXICON.md",
    }
    
    file = aliases.get(file.replace(".MD", ""), file)
    
    output = teach_file(config, file)
    print(output)
    
    return 0
