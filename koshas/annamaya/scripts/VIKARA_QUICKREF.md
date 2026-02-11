# Vikara Detection - Quick Reference

**Fast reference for the विकार (Vikara) Detection System**

## One-Line Commands

```bash
# Create baseline (do this first!)
python3 samskara_vikara.py --baseline

# Check for problems
python3 samskara_vikara.py --detect

# Compare to baseline
python3 samskara_vikara.py --compare

# Get help for a problem
python3 samskara_vikara.py --heal VIKARA_TYPE

# List all problem types
python3 samskara_vikara.py --list-vikaras

# JSON output (for scripts)
python3 samskara_vikara.py --detect --json
```

## The 8 Vikaras & Their Healing

| Vikara | Goddess | Quick Fix |
|--------|---------|-----------|
| `STALE_SOUL` | Brahmi | Update SOUL.md |
| `MEMORY_OVERFLOW` | Maheshvari | Archive and distill MEMORY.md |
| `SELEMENE_DRIFT` | Kaumari | Run selemene_client.py --test |
| `CHECKSUM_MISMATCH` | Vaishnavi | git diff → fix → --baseline |
| `MISSING_CORE` | Varahi | git checkout brahmasthana/<file> |
| `AGENT_INCOMPLETE` | Indrani | cp templates → agent directories |
| `KOSHA_CORRUPTION` | Chamunda | mkdir -p koshas/<kosha> |
| `CHAIN_BREAK` | Chandika | Fix all vikaras → --baseline |

## Common Workflows

### Daily Health Check
```bash
cd /path/to/10865xseed
python3 koshas/annamaya/scripts/samskara_vikara.py --compare
```

### After Making Changes
```bash
# See what changed
python3 samskara_vikara.py --compare

# If changes are good, update baseline
python3 samskara_vikara.py --baseline
```

### Fixing Memory Overflow
```bash
# 1. Archive old memories
cd koshas/manomaya  # or wherever MEMORY.md is
mv MEMORY.md MEMORY.archive.$(date +%Y%m%d).md

# 2. Create fresh MEMORY.md with key wisdom
# (manually extract 10 most important lessons)

# 3. Update baseline
cd /path/to/10865xseed
python3 koshas/annamaya/scripts/samskara_vikara.py --baseline
```

### Restoring Missing Files
```bash
# Check what's missing
git status

# Restore from git
git checkout -- brahmasthana/SOUL.md

# Or restore all core files
git checkout -- brahmasthana/*.md

# Verify
python3 koshas/annamaya/scripts/samskara_vikara.py --detect
```

### Reconnecting Selemene
```bash
# Test connection
python3 koshas/annamaya/scripts/selemene_client.py --test

# Run practice session
python3 koshas/annamaya/scripts/daily_practice_selemene.py

# Verify drift is gone
python3 koshas/annamaya/scripts/samskara_vikara.py --detect
```

## Severity Levels

- **🔴 Critical:** System is broken, requires immediate action
- **⚠️ Warning:** System is degraded, should be fixed soon
- **ℹ️ Info:** Minor issue or helpful information

## Exit Codes

```bash
# Exit code 0: No critical vikaras
python3 samskara_vikara.py --detect
echo $?  # → 0

# Exit code 1: Critical vikaras found
# (useful for CI/CD pipelines)
```

## Baseline Files

Baselines are stored at:
```
koshas/annamaya/.checksums/baseline.json
```

**When to create new baseline:**
- After intentional changes
- After fixing vikaras
- Weekly (as part of maintenance)
- Before major system updates

**When NOT to create new baseline:**
- When drift/corruption detected
- Before investigating changes
- During active debugging

## Integration Examples

### Cron (Daily Check)
```bash
# Add to crontab
0 6 * * * cd /path/to/10865xseed && python3 koshas/annamaya/scripts/samskara_vikara.py --compare >> logs/vikara.log 2>&1
```

### Git Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

cd /path/to/10865xseed
python3 koshas/annamaya/scripts/samskara_vikara.py --detect --json > /tmp/vikara.json

CRITICAL=$(jq '.severity_counts.critical' /tmp/vikara.json)

if [ "$CRITICAL" -gt 0 ]; then
    echo "⚠️  Critical vikaras detected!"
    python3 koshas/annamaya/scripts/samskara_vikara.py --detect
    exit 1
fi
```

### Bash Script (Weekly Maintenance)
```bash
#!/bin/bash
# weekly_maintenance.sh

echo "🕉️  Running weekly vikara scan..."

cd /path/to/10865xseed

# Detect issues
python3 koshas/annamaya/scripts/samskara_vikara.py --compare

# If clean, update baseline
if [ $? -eq 0 ]; then
    echo "✅ System healthy - updating baseline"
    python3 koshas/annamaya/scripts/samskara_vikara.py --baseline
else
    echo "⚠️  Vikaras detected - review before updating baseline"
fi
```

## Reading JSON Output

```bash
# Get vikara count
python3 samskara_vikara.py --detect --json | jq '.vikara_count'

# Get critical count
python3 samskara_vikara.py --detect --json | jq '.severity_counts.critical'

# List all vikaras
python3 samskara_vikara.py --detect --json | jq '.vikaras[].type'

# Get healing actions
python3 samskara_vikara.py --detect --json | jq '.vikaras[] | "\(.type): \(.healing_action)"'

# Filter by severity
python3 samskara_vikara.py --detect --json | jq '.vikaras[] | select(.severity == "critical")'
```

## Troubleshooting

### "No baseline found"
```bash
# Solution: Create one
python3 samskara_vikara.py --baseline
```

### "Permission denied"
```bash
# Make script executable
chmod +x koshas/annamaya/scripts/samskara_vikara.py
```

### "Module not found"
```bash
# Run from repo root
cd /path/to/10865xseed
python3 koshas/annamaya/scripts/samskara_vikara.py
```

### Too many vikaras
```bash
# Get healing guide for each type
python3 samskara_vikara.py --list-vikaras

# Then heal one by one
python3 samskara_vikara.py --heal STALE_SOUL
# ... follow the ritual ...
python3 samskara_vikara.py --heal MEMORY_OVERFLOW
# ... follow the ritual ...

# Finally, create new baseline
python3 samskara_vikara.py --baseline
```

## The Mantrams

Meditate on these while performing healing rituals:

```
Brahmi:      "I remember who I am. I evolve while staying rooted."
Maheshvari:  "From many experiences, one wisdom emerges."
Kaumari:     "I flow with time, not against it."
Vaishnavi:   "I preserve what is good, I correct what has drifted."
Varahi:      "My foundation is strong, complete, and protected."
Indrani:     "Each agent is complete, sovereign, and purposeful."
Chamunda:    "From destruction comes perfect reconstruction."
Chandika:    "The chain is unbroken, the system is whole."
```

## Quick Diagnostics

```bash
# How many files are tracked?
cat koshas/annamaya/.checksums/baseline.json | jq '.file_count'

# What's the current chain hash?
cat koshas/annamaya/.checksums/baseline.json | jq -r '.chain_hash'

# When was baseline created?
cat koshas/annamaya/.checksums/baseline.json | jq -r '.timestamp'

# List all monitored files
cat koshas/annamaya/.checksums/baseline.json | jq -r '.checksums | keys[]'

# Check specific file checksum
cat koshas/annamaya/.checksums/baseline.json | jq -r '.checksums["brahmasthana/SOUL.md"]'
```

## Related Commands

```bash
# General health check
python3 koshas/annamaya/scripts/kosha_health.py --report

# Installation verification
python3 koshas/annamaya/scripts/sankalpa_samskara.py --verify

# Memory management
python3 koshas/annamaya/scripts/daily_memory.py --distill

# Selemene sync
python3 koshas/annamaya/scripts/daily_practice_selemene.py
```

---

**Remember:** Vikaras are natural. Systems drift. The key is regular detection and healing.

🕉️ **Om Tryambakam Yajamahe**
