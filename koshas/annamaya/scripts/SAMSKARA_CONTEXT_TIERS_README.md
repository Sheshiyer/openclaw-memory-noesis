# Samskara Context Tiers - Quick Reference

## Overview

`samskara_context_tiers.py` provides tiered context loading for different model context windows and Pratyahara (withdrawal) compression for minimal context.

## Context Tiers

| Tier | Size | Tokens | Files | Use Case |
|------|------|--------|-------|----------|
| **lite** | ~3KB | ~847 | SOUL.md, IDENTITY.md | Minimal identity for small models |
| **core** | ~49KB | ~12,555 | + PANCHA-KOSHA.md, USER.md | Core framework for standard models |
| **standard** | ~118KB | ~30,312 | + KHA.md, BHA.md, LHA.md, VEDIC-LEXICON.md | Extended knowledge for large models |
| **full** | ~155KB | ~39,728 | + SELEMENE-ENGINE.md, ARCHITECTURE-VISUAL.md | Complete system for premium models |

## Usage Examples

### Check Tier Size (Fast)
```bash
python3 koshas/annamaya/scripts/samskara_context_tiers.py --tier core --estimate
# Output: 📊 Tier 'core': ~49KB (50,223 bytes, ~12,555 tokens)
```

### Get Detailed Statistics
```bash
python3 koshas/annamaya/scripts/samskara_context_tiers.py --tier standard --stats
# Outputs JSON with file-by-file breakdown
```

### Load Full Context
```bash
python3 koshas/annamaya/scripts/samskara_context_tiers.py --tier core
# Outputs concatenated content of all tier files
```

### Apply Pratyahara Compression
```bash
# Compress to ~4000 tokens (default)
python3 koshas/annamaya/scripts/samskara_context_tiers.py --tier full --compress

# Compress to specific token target
python3 koshas/annamaya/scripts/samskara_context_tiers.py --tier standard --compress --target-tokens 2000
```

## Pratyahara Compression

**प्रत्याहार (Pratyahara)** = Withdrawal of senses, focusing on essence

The compression algorithm extracts:
1. **Headers** - Structural outline
2. **Prime Directives** - Lines with MUST, NEVER, ALWAYS, REQUIRED, CRITICAL
3. **Current State** - Lines with temporal markers (current, active, 2024, dasha)
4. **Definitions** - Sanskrit terms and key concept explanations

### Compression Example
```bash
# Full tier: ~39,728 tokens → Compressed: ~1,545 tokens (26x reduction)
python3 koshas/annamaya/scripts/samskara_context_tiers.py --tier full --compress --target-tokens 3000
```

## Integration Examples

### Python API Usage
```python
from pathlib import Path
import sys
sys.path.append('koshas/annamaya/scripts')

from samskara_context_tiers import (
    load_tier_context,
    pratyahara_compress,
    get_tier_stats,
    BRAHMASTHANA
)

# Load tier
context = load_tier_context("core", BRAHMASTHANA)

# Apply compression
compressed = pratyahara_compress(context, target_tokens=4000)

# Get statistics
stats = get_tier_stats("standard", BRAHMASTHANA)
print(f"Total: {stats['total_kb']}KB, {stats['estimated_tokens']} tokens")
```

### As System Prompt Builder
```python
def build_system_prompt(model_context_window: int):
    """Select appropriate tier based on model capacity."""
    
    if model_context_window < 16000:
        tier = "lite"
    elif model_context_window < 64000:
        tier = "core"
    elif model_context_window < 128000:
        tier = "standard"
    else:
        tier = "full"
    
    context = load_tier_context(tier, BRAHMASTHANA)
    
    # Compress if still too large
    if estimate_tokens(context) > model_context_window * 0.3:
        context = pratyahara_compress(context, target_tokens=int(model_context_window * 0.25))
    
    return context
```

### For Agent Spawning
```bash
# Load lite context for quick agent initialization
CONTEXT=$(python3 koshas/annamaya/scripts/samskara_context_tiers.py --tier lite)

# Pass to agent via environment or stdin
echo "$CONTEXT" | your_agent_command

# Or compressed for extreme size constraints
COMPRESSED=$(python3 koshas/annamaya/scripts/samskara_context_tiers.py --tier core --compress --target-tokens 2000)
```

## CLI Options

```
--tier {lite,core,standard,full}   Context tier to load (default: core)
--compress                          Apply Pratyahara compression
--estimate                          Show size estimate without loading
--stats                             Show detailed JSON statistics
--target-tokens N                   Compression target (default: 4000)
--brahmasthana PATH                 Override brahmasthana path
```

## File Location

**Script:** `koshas/annamaya/scripts/samskara_context_tiers.py`
**Context Files:** `koshas/brahmasthana/*.md`

## Notes

- Compression is lossy but preserves essential structure and directives
- Token estimation is approximate (~4 chars per token)
- Missing files are reported but don't cause failure
- Script auto-detects brahmasthana path relative to its location
