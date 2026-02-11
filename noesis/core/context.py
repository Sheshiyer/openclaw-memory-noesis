"""
Context - Context Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generates context at different tiers for injection into AI models.
"""

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from noesis.config import Config


TIERS = {
    "lite": {
        "files": ["SOUL.md", "IDENTITY.md"],
        "description": "Minimal identity (~3KB)",
    },
    "core": {
        "files": ["SOUL.md", "IDENTITY.md", "PANCHA-KOSHA.md", "USER.md"],
        "description": "Core consciousness (~49KB)",
    },
    "standard": {
        "files": [
            "SOUL.md", "IDENTITY.md", "PANCHA-KOSHA.md", "USER.md",
            "KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md",
        ],
        "description": "Full kernel (~60KB)",
    },
    "full": {
        "files": [
            "SOUL.md", "IDENTITY.md", "PANCHA-KOSHA.md", "USER.md",
            "KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md",
            "SELEMENE-ENGINE.md", "ARCHITECTURE-VISUAL.md",
        ],
        "description": "Complete system (~155KB)",
    },
}


def compress_content(content: str) -> str:
    """
    Pratyahara compression - remove redundant whitespace and comments.
    """
    lines = content.splitlines()
    compressed = []
    in_code_block = False
    
    for line in lines:
        # Track code blocks (don't compress them)
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            compressed.append(line)
            continue
        
        if in_code_block:
            compressed.append(line)
            continue
        
        # Skip empty lines and HTML comments
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        
        # Keep the line
        compressed.append(line)
    
    return "\n".join(compressed)


def generate_context(config: "Config", tier: str, compress: bool = False) -> str:
    """Generate context for the specified tier."""
    tier_config = TIERS.get(tier, TIERS["core"])
    files = tier_config["files"]
    
    parts = [
        f"<!-- NOESIS CONTEXT INJECTION :: tier={tier} -->",
        "",
    ]
    
    for filename in files:
        filepath = config.brahmasthana / filename
        if filepath.exists():
            content = filepath.read_text()
            
            if compress:
                content = compress_content(content)
            
            parts.append(f"<!-- FILE: {filename} -->")
            parts.append(content)
            parts.append("")
    
    context = "\n".join(parts)
    
    if compress:
        context = compress_content(context)
    
    return context


def run_context_generation(
    config: "Config",
    tier: str = "core",
    compress: bool = False,
    output: Optional[str] = None,
) -> int:
    """
    Generate context for the specified tier.
    
    Returns:
        0 on success, 1 on error
    """
    if tier not in TIERS:
        print(f"Unknown tier: {tier}", file=sys.stderr)
        print(f"Available: {', '.join(TIERS.keys())}", file=sys.stderr)
        return 1
    
    context = generate_context(config, tier, compress)
    
    if output:
        output_path = Path(output)
        output_path.write_text(context)
        
        # Print summary to stderr
        tier_config = TIERS[tier]
        print(f"Generated {tier} context ({tier_config['description']})", file=sys.stderr)
        print(f"Output: {output_path} ({len(context):,} bytes)", file=sys.stderr)
    else:
        # Output to stdout
        print(context)
    
    return 0
