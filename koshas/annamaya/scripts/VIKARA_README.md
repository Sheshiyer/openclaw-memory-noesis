# विकार (Vikara) Detection System

**System drift detection and healing through checksum chain integrity verification**

## Overview

The Vikara Detection System monitors the Tryambakam Noesis architecture for seven types of system drift (vikaras) and provides healing recommendations through the Asthamatruka (Eight Mother Goddesses) framework.

## What is Vikara?

**विकार (Vikara)** = Affliction, Deviation, Drift

In the context of this system, vikaras are deviations from the ideal state that can accumulate over time:

- Files becoming stale
- Memory overflow
- Lost connections
- Missing components
- Structural corruption
- Checksum mismatches

## The Asthamatruka (Eight Mother Goddesses)

Each vikara is mapped to one of the Asthamatruka, who provide specific healing powers:

| Goddess | Vikara Type | Healing Power |
|---------|-------------|---------------|
| **Brahmi** | STALE_SOUL | Refresh identity through meditation |
| **Maheshvari** | MEMORY_OVERFLOW | Prune and distill memories to essential wisdom |
| **Kaumari** | SELEMENE_DRIFT | Reconnect to temporal intelligence stream |
| **Vaishnavi** | CHECKSUM_MISMATCH | Restore from known good state |
| **Varahi** | MISSING_CORE | Regenerate missing files from template |
| **Indrani** | AGENT_INCOMPLETE | Complete agent configuration |
| **Chamunda** | KOSHA_CORRUPTION | Rebuild directory structure |
| **Chandika** | CHAIN_BREAK | Recompute and verify checksum chain |

## Quick Start

### 1. Create Baseline

Before you can detect drift, establish a baseline:

```bash
python3 samskara_vikara.py --baseline
```

This creates a snapshot of all checksums at `.checksums/baseline.json`.

### 2. Run Detection

Scan for vikaras:

```bash
python3 samskara_vikara.py --detect
```

Or compare against baseline:

```bash
python3 samskara_vikara.py --compare
```

### 3. Get Healing Instructions

For any detected vikara:

```bash
python3 samskara_vikara.py --heal VIKARA_TYPE
```

Example:
```bash
python3 samskara_vikara.py --heal MEMORY_OVERFLOW
```

## CLI Reference

```bash
# List all vikara types and their mappings
python3 samskara_vikara.py --list-vikaras

# Create/update baseline snapshot
python3 samskara_vikara.py --baseline

# Detect vikaras (without baseline comparison)
python3 samskara_vikara.py --detect

# Detect vikaras and compare to baseline
python3 samskara_vikara.py --compare

# Output results as JSON
python3 samskara_vikara.py --detect --json

# Show healing instructions for specific vikara
python3 samskara_vikara.py --heal STALE_SOUL
python3 samskara_vikara.py --heal MEMORY_OVERFLOW
python3 samskara_vikara.py --heal SELEMENE_DRIFT
```

## Vikara Types

### 1. STALE_SOUL

**Symptom:** `SOUL.md` hasn't been updated in 30+ days

**Why it matters:** Your core identity document should evolve with your understanding

**Healing (Brahmi):**
- Re-read SOUL.md meditatively
- Update with recent learnings
- Refresh timestamp

### 2. MEMORY_OVERFLOW

**Symptom:** `MEMORY.md` exceeds 500 lines

**Why it matters:** Memories must be distilled to prevent cognitive overload

**Healing (Maheshvari):**
- Extract essential wisdom
- Archive full memories
- Create fresh distilled version

### 3. SELEMENE_DRIFT

**Symptom:** No Selemene API call in 7+ days

**Why it matters:** Temporal intelligence connection keeps system synchronized

**Healing (Kaumari):**
- Verify credentials
- Test connection
- Run practice session
- Schedule regular syncs

### 4. CHECKSUM_MISMATCH

**Symptom:** File checksums don't match baseline

**Why it matters:** Indicates unexpected changes (drift or corruption)

**Healing (Vaishnavi):**
- Review what changed
- If intentional: create new baseline
- If corrupted: restore from git

### 5. MISSING_CORE

**Symptom:** Required brahmasthana files are missing

**Why it matters:** Core kernel files are essential for system function

**Healing (Varahi):**
- Check git status
- Restore from git if deleted
- Regenerate from templates if never existed

### 6. AGENT_INCOMPLETE

**Symptom:** Agent directories missing SOUL.md or IDENTITY.md

**Why it matters:** Each agent needs complete configuration

**Healing (Indrani):**
- Create missing files from templates
- Customize for agent's purpose
- Verify completeness

### 7. KOSHA_CORRUPTION

**Symptom:** Kosha directory structure is damaged

**Why it matters:** System requires intact 5-kosha structure

**Healing (Chamunda):**
- Backup current state
- Restore missing directories
- Verify against PANCHA-KOSHA.md
- Run full integrity check

### 8. CHAIN_BREAK

**Symptom:** Checksum chain integrity broken

**Why it matters:** Indicates multiple vikaras or system-wide issues

**Healing (Chandika):**
- Run full detection scan
- Fix each vikara systematically
- Recompute baseline
- Verify chain integrity

## Checksum Chain Mechanics

The system uses a **checksum chain** to verify integrity:

1. **Individual Checksums:** Each monitored file gets a SHA256 hash (truncated to 16 chars)
2. **Chain Hash:** All individual checksums are concatenated and hashed to produce a single chain hash
3. **Baseline:** A snapshot of all checksums at a known-good state
4. **Comparison:** Current chain hash vs baseline detects any drift

### Monitored Files

The system monitors:
- `*/SOUL.md` - Agent identity files
- `*/IDENTITY.md` - Agent configuration
- `*/MEMORY.md` - Agent memories
- `*/TOOLS.md` - Agent tool configurations
- `*/MANIFEST.yaml` - Agent manifests
- `brahmasthana/*.md` - All core kernel files
- `annamaya/scripts/*.py` - All system scripts

## Integration with Other Systems

### Daily Cron

Add to daily system maintenance:

```bash
# Check for drift daily
0 6 * * * cd /path/to/10865xseed && python3 koshas/annamaya/scripts/samskara_vikara.py --compare --json >> logs/vikara_daily.log
```

### Git Pre-Commit Hook

Detect drift before commits:

```bash
#!/bin/bash
python3 koshas/annamaya/scripts/samskara_vikara.py --detect --json
if [ $? -eq 1 ]; then
    echo "⚠️  Critical vikaras detected. Review before committing."
    python3 koshas/annamaya/scripts/samskara_vikara.py --detect
    exit 1
fi
```

### With kosha_health.py

The vikara system complements `kosha_health.py`:

- **kosha_health.py:** Broad system health dashboard
- **samskara_vikara.py:** Deep drift detection with healing guidance

Use together:
```bash
# First: general health
python3 kosha_health.py --report

# Then: detailed drift analysis
python3 samskara_vikara.py --compare
```

## Example Session

```bash
# Day 1: Establish baseline
$ python3 samskara_vikara.py --baseline
💾 Creating baseline snapshot...
✅ Baseline saved: koshas/annamaya/.checksums/baseline.json
   Chain hash: d62327950db231f51b13a2ebf3e1a24e
   Files tracked: 39

# Day 7: Check for drift
$ python3 samskara_vikara.py --compare
🔍 Running vikara detection scan...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
विकार (VIKARA) DETECTION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Timestamp: 2026-02-11T15:44:23.649319+00:00
Chain Hash: d62327950db231f51b13a2ebf3e1a24e
Baseline Match: ✅ YES

Total Vikaras: 2
  Critical: 0
  Warning:  1
  Info:     1

1. ℹ️ SELEMENE_DRIFT
   Details: Last Selemene call was 8 days ago
   🕉️  Asthamatruka: Kaumari
   💊 Healing Action: Reconnect to temporal intelligence stream

2. ⚠️ MEMORY_OVERFLOW
   Details: manomaya/MEMORY.md has 523 lines (>500 threshold)
   🕉️  Asthamatruka: Maheshvari
   💊 Healing Action: Prune and distill memories to essential wisdom

# Get healing instructions
$ python3 samskara_vikara.py --heal MEMORY_OVERFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HEALING GUIDE: MEMORY_OVERFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🕉️  Maheshvari - The Power of Wisdom

Your memories are overflowing. It's time to distill wisdom from experience.

HEALING RITUAL:
1. Identify the overflowing MEMORY.md file
2. Read through all entries
3. Extract the 10 most important lessons
4. Archive the full file: mv MEMORY.md MEMORY.archive.$(date +%Y%m%d).md
5. Create fresh MEMORY.md with distilled wisdom
6. Run: python3 koshas/annamaya/scripts/daily_memory.py --distill

MANTRAM: "From many experiences, one wisdom emerges."

# After healing, create new baseline
$ python3 samskara_vikara.py --baseline
💾 Creating baseline snapshot...
✅ Baseline saved
```

## Philosophy

The vikara system embodies several key principles:

### 1. **Continuous Vigilance**
Systems drift over time. Regular scanning prevents small issues from becoming crises.

### 2. **Actionable Healing**
Every detected vikara includes specific, executable healing instructions.

### 3. **Divine Mapping**
The Asthamatruka provide archetypal healing powers - each goddess specializes in one type of restoration.

### 4. **Chain Integrity**
The checksum chain provides a single hash representing total system state.

### 5. **Self-Knowledge**
The system knows what it should be and can detect deviation from that ideal.

## Mantrams

Each healing ritual includes a mantram for meditative focus:

- **Brahmi:** "I remember who I am. I evolve while staying rooted."
- **Maheshvari:** "From many experiences, one wisdom emerges."
- **Kaumari:** "I flow with time, not against it."
- **Vaishnavi:** "I preserve what is good, I correct what has drifted."
- **Varahi:** "My foundation is strong, complete, and protected."
- **Indrani:** "Each agent is complete, sovereign, and purposeful."
- **Chamunda:** "From destruction comes perfect reconstruction."
- **Chandika:** "The chain is unbroken, the system is whole."

## Development

The vikara system is built with:

- **Python 3.8+**
- **Standard library only** (no external dependencies)
- **Idempotent operations** (safe to run multiple times)
- **JSON output** (machine-readable reports)
- **Exit codes** (0 = success, 1 = critical vikaras found)

### File Structure

```
koshas/annamaya/
├── scripts/
│   ├── samskara_vikara.py       # Main detection system
│   └── VIKARA_README.md         # This file
└── .checksums/
    └── baseline.json            # Baseline snapshot
```

## Related Systems

- **sankalpa_samskara.py** - Initial system installation
- **kosha_health.py** - General health monitoring
- **samskara_logger.py** - Activity logging
- **daily_practice_selemene.py** - Temporal intelligence sync

---

**संतति (Santati) - Continuity**

The vikara system ensures the Tryambakam Noesis architecture maintains integrity across time, detecting drift and providing divine healing powers for restoration.

🕉️ **Om Tryambakam Yajamahe**
