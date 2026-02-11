#!/usr/bin/env python3
"""
Context Tiers & Pratyahara Compression
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Provides tiered context loading for different model context windows
and Pratyahara (withdrawal) compression for minimal context.

प्रत्याहार (Pratyahara) = Withdrawal of senses
The fifth limb of yoga - withdrawing from sensory overload to focus on essence.

CONTEXT TIERS:
- lite: ~8KB - Minimal identity (SOUL + IDENTITY)
- core: ~25KB - Core framework (+ PANCHA-KOSHA + USER)
- standard: ~85KB - Extended knowledge (+ KHA + BHA + LHA + VEDIC-LEXICON)
- full: ~115KB - Complete system (+ SELEMENE + ARCHITECTURE-VISUAL)

Usage:
    python3 samskara_context_tiers.py --tier core
    python3 samskara_context_tiers.py --tier full --compress
    python3 samskara_context_tiers.py --tier standard --estimate
"""

import re
import argparse
from pathlib import Path
from typing import List, Dict

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

KOSHAS_ROOT = Path(__file__).parent.parent.parent  # Up from scripts → annamaya → koshas
BRAHMASTHANA = KOSHAS_ROOT / "brahmasthana"

# Context Tier Definitions
SANKALPA_LITE = ["SOUL.md", "IDENTITY.md"]  # ~8KB - Minimal identity
SANKALPA_CORE = SANKALPA_LITE + ["PANCHA-KOSHA.md", "USER.md"]  # ~25KB - Core framework
SAMSKARA_STANDARD = ["KHA.md", "BHA.md", "LHA.md", "VEDIC-LEXICON.md"]  # ~60KB - Extended
SAMSKARA_FULL = SANKALPA_CORE + SAMSKARA_STANDARD + ["SELEMENE-ENGINE.md", "ARCHITECTURE-VISUAL.md"]  # ~100KB

TIER_MAP = {
    "lite": SANKALPA_LITE,
    "core": SANKALPA_CORE,
    "standard": SANKALPA_CORE + SAMSKARA_STANDARD,
    "full": SAMSKARA_FULL,
}

# Token estimation (rough: ~4 chars per token)
CHARS_PER_TOKEN = 4

# ═══════════════════════════════════════════════════════════════════════════════
# TIER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def get_tier_files(tier: str) -> List[str]:
    """
    Get list of files for a context tier.
    
    Args:
        tier: One of "lite", "core", "standard", "full"
        
    Returns:
        List of markdown file names for the tier
    """
    if tier not in TIER_MAP:
        raise ValueError(f"Unknown tier '{tier}'. Must be one of: {list(TIER_MAP.keys())}")
    
    return TIER_MAP[tier]


def estimate_tier_size(tier: str, brahmasthana_path: Path = BRAHMASTHANA) -> int:
    """
    Estimate total bytes for a tier.
    
    Args:
        tier: One of "lite", "core", "standard", "full"
        brahmasthana_path: Path to brahmasthana directory
        
    Returns:
        Total size in bytes
    """
    files = get_tier_files(tier)
    total_size = 0
    
    for filename in files:
        filepath = brahmasthana_path / filename
        if filepath.exists():
            total_size += filepath.stat().st_size
        else:
            print(f"⚠️  Warning: {filename} not found in {brahmasthana_path}", file=sys.stderr)
    
    return total_size


def load_tier_context(tier: str, brahmasthana_path: Path = BRAHMASTHANA) -> str:
    """
    Load and concatenate all files for a tier.
    
    Args:
        tier: One of "lite", "core", "standard", "full"
        brahmasthana_path: Path to brahmasthana directory
        
    Returns:
        Concatenated content of all files in the tier
    """
    files = get_tier_files(tier)
    contexts = []
    
    for filename in files:
        filepath = brahmasthana_path / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Add file separator for clarity
                contexts.append(f"{'═' * 80}")
                contexts.append(f"FILE: {filename}")
                contexts.append(f"{'═' * 80}")
                contexts.append(content)
                contexts.append("")  # Blank line separator
        else:
            contexts.append(f"⚠️  ERROR: {filename} not found\n")
    
    return "\n".join(contexts)


# ═══════════════════════════════════════════════════════════════════════════════
# PRATYAHARA COMPRESSION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_prime_directives(content: str) -> List[str]:
    """
    Extract lines containing prime directives.
    
    Looks for imperatives: MUST, NEVER, ALWAYS, REQUIRED, CRITICAL, etc.
    
    Args:
        content: Full text content
        
    Returns:
        List of lines with prime directives
    """
    prime_keywords = [
        'MUST', 'NEVER', 'ALWAYS', 'REQUIRED', 'CRITICAL', 
        'MANDATORY', 'FORBIDDEN', 'ESSENTIAL', 'PROHIBITED',
        'SHALL', 'SHALL NOT', 'CANNOT'
    ]
    
    directives = []
    lines = content.split('\n')
    
    for line in lines:
        line_upper = line.upper()
        if any(keyword in line_upper for keyword in prime_keywords):
            directives.append(line.strip())
    
    return directives


def extract_current_state(content: str) -> List[str]:
    """
    Extract lines about current state/dasha/active items.
    
    Looks for temporal markers: current, active, now, today, 2024, 2025, etc.
    
    Args:
        content: Full text content
        
    Returns:
        List of lines about current state
    """
    state_keywords = [
        'current', 'active', 'now', 'today', 'present',
        'dasha', 'ongoing', 'in progress', '2024', '2025', '2026'
    ]
    
    state_lines = []
    lines = content.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in state_keywords):
            state_lines.append(line.strip())
    
    return state_lines


def extract_headers(content: str) -> List[str]:
    """
    Extract all markdown headers.
    
    Args:
        content: Full text content
        
    Returns:
        List of header lines
    """
    headers = []
    lines = content.split('\n')
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            headers.append(stripped)
    
    return headers


def extract_definitions(content: str) -> List[str]:
    """
    Extract Sanskrit definitions and key term explanations.
    
    Looks for patterns like:
    - सङ्कल्प (Sankalpa) = Definition
    - **Term** - Explanation
    
    Args:
        content: Full text content
        
    Returns:
        List of definition lines
    """
    definitions = []
    lines = content.split('\n')
    
    # Pattern for Sanskrit definitions: word (transliteration) = definition
    sanskrit_pattern = re.compile(r'^[^\w]*[\u0900-\u097F]+.*?=', re.UNICODE)
    # Pattern for bold definitions: **term** or **term**:
    bold_pattern = re.compile(r'^\s*\*\*[^*]+\*\*\s*[-:]')
    
    for line in lines:
        if sanskrit_pattern.search(line) or bold_pattern.search(line):
            definitions.append(line.strip())
    
    return definitions


def pratyahara_compress(full_context: str, target_tokens: int = 4000) -> str:
    """
    प्रत्याहार (Pratyahara) = Withdrawal of senses
    
    Compress context by extracting only essential patterns:
    1. Keep all headers (## lines)
    2. Keep prime directives (lines with "MUST", "NEVER", "ALWAYS")
    3. Keep current state (lines with dates, "current", "active")
    4. Keep Sanskrit definitions and key terms
    5. Remove examples, verbose explanations
    6. Truncate to target token estimate (~4 chars/token)
    
    Args:
        full_context: Complete context to compress
        target_tokens: Target token count (default 4000)
        
    Returns:
        Compressed context string
    """
    target_chars = target_tokens * CHARS_PER_TOKEN
    
    # Extract essential components
    headers = extract_headers(full_context)
    directives = extract_prime_directives(full_context)
    state = extract_current_state(full_context)
    definitions = extract_definitions(full_context)
    
    # Build compressed context
    compressed_parts = []
    
    compressed_parts.append("=" * 80)
    compressed_parts.append("PRATYAHARA COMPRESSED CONTEXT")
    compressed_parts.append(f"Target: ~{target_tokens} tokens ({target_chars} chars)")
    compressed_parts.append("=" * 80)
    compressed_parts.append("")
    
    # Add headers (structure)
    if headers:
        compressed_parts.append("## STRUCTURE")
        compressed_parts.extend(headers[:50])  # Limit headers
        compressed_parts.append("")
    
    # Add definitions (knowledge)
    if definitions:
        compressed_parts.append("## KEY DEFINITIONS")
        compressed_parts.extend(definitions[:30])  # Limit definitions
        compressed_parts.append("")
    
    # Add directives (rules)
    if directives:
        compressed_parts.append("## PRIME DIRECTIVES")
        compressed_parts.extend(directives[:40])  # Limit directives
        compressed_parts.append("")
    
    # Add current state (context)
    if state:
        compressed_parts.append("## CURRENT STATE")
        compressed_parts.extend(state[:20])  # Limit state lines
        compressed_parts.append("")
    
    # Join and truncate to target
    compressed = "\n".join(compressed_parts)
    
    if len(compressed) > target_chars:
        compressed = compressed[:target_chars]
        # Try to end at a line break
        last_newline = compressed.rfind('\n')
        if last_newline > target_chars * 0.9:  # If we're close to target
            compressed = compressed[:last_newline]
        compressed += "\n\n[... TRUNCATED TO TARGET SIZE ...]"
    
    return compressed


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def estimate_tokens(text: str) -> int:
    """Rough token estimation: 1 token ≈ 4 characters."""
    return len(text) // CHARS_PER_TOKEN


def get_tier_stats(tier: str, brahmasthana_path: Path = BRAHMASTHANA) -> Dict[str, any]:
    """
    Get comprehensive statistics for a tier.
    
    Args:
        tier: One of "lite", "core", "standard", "full"
        brahmasthana_path: Path to brahmasthana directory
        
    Returns:
        Dictionary with stats: bytes, tokens, files, missing_files
    """
    files = get_tier_files(tier)
    total_bytes = 0
    found_files = []
    missing_files = []
    
    for filename in files:
        filepath = brahmasthana_path / filename
        if filepath.exists():
            size = filepath.stat().st_size
            total_bytes += size
            found_files.append({"name": filename, "bytes": size})
        else:
            missing_files.append(filename)
    
    return {
        "tier": tier,
        "total_bytes": total_bytes,
        "total_kb": total_bytes // 1024,
        "estimated_tokens": estimate_tokens(" " * total_bytes),  # Rough estimate
        "files_count": len(found_files),
        "found_files": found_files,
        "missing_files": missing_files,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """CLI entry point for context tier management."""
    parser = argparse.ArgumentParser(
        description="Sankalpa/Samskara Context Tier Management with Pratyahara Compression",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --tier core                    # Load core tier context
  %(prog)s --tier full --compress         # Load full tier + compress
  %(prog)s --tier standard --estimate     # Show size estimate
  %(prog)s --tier lite --stats            # Detailed statistics
        """
    )
    
    parser.add_argument(
        "--tier", 
        choices=["lite", "core", "standard", "full"], 
        default="core",
        help="Context tier to load (default: core)"
    )
    
    parser.add_argument(
        "--compress", 
        action="store_true", 
        help="Apply Pratyahara compression to reduce context size"
    )
    
    parser.add_argument(
        "--estimate", 
        action="store_true", 
        help="Show size estimate without loading content"
    )
    
    parser.add_argument(
        "--stats", 
        action="store_true", 
        help="Show detailed statistics for the tier"
    )
    
    parser.add_argument(
        "--target-tokens",
        type=int,
        default=4000,
        help="Target token count for Pratyahara compression (default: 4000)"
    )
    
    parser.add_argument(
        "--brahmasthana",
        type=Path,
        default=BRAHMASTHANA,
        help="Path to brahmasthana directory (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Validate brahmasthana path
    if not args.brahmasthana.exists():
        print(f"❌ Error: Brahmasthana path not found: {args.brahmasthana}")
        print(f"   Expected at: {BRAHMASTHANA}")
        return 1
    
    # Handle --estimate
    if args.estimate:
        size = estimate_tier_size(args.tier, args.brahmasthana)
        tokens = estimate_tokens(" " * size)
        print(f"📊 Tier '{args.tier}': ~{size // 1024}KB ({size:,} bytes, ~{tokens:,} tokens)")
        return 0
    
    # Handle --stats
    if args.stats:
        import json
        stats = get_tier_stats(args.tier, args.brahmasthana)
        print(json.dumps(stats, indent=2))
        return 0
    
    # Load context
    try:
        context = load_tier_context(args.tier, args.brahmasthana)
        
        # Apply compression if requested
        if args.compress:
            context = pratyahara_compress(context, args.target_tokens)
            print(f"🧘 Pratyahara compression applied (target: {args.target_tokens} tokens)")
            print(f"📏 Compressed size: {len(context):,} chars (~{estimate_tokens(context):,} tokens)")
            print("=" * 80)
            print()
        
        # Output context
        print(context)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error loading context: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
