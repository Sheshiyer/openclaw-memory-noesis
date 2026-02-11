# Quick Reference Guide

## Health Monitoring

### Quick Status Check
```bash
python3 koshas/annamaya/scripts/kosha_health.py --quick
```

### Full Health Report
```bash
python3 koshas/annamaya/scripts/kosha_health.py --report
```

### Check Specific Component
```bash
# Brahmasthana (core files)
python3 koshas/annamaya/scripts/kosha_health.py --check brahmasthana

# Agent bindings
python3 koshas/annamaya/scripts/kosha_health.py --check agents

# Selemene API
python3 koshas/annamaya/scripts/kosha_health.py --check selemene

# Memory health
python3 koshas/annamaya/scripts/kosha_health.py --check memory

# Kosha structure
python3 koshas/annamaya/scripts/kosha_health.py --check structure

# Logging system
python3 koshas/annamaya/scripts/kosha_health.py --check logging
```

### JSON Output (for automation)
```bash
python3 koshas/annamaya/scripts/kosha_health.py --json
```

## Status Indicators

- ✅ **Healthy** - Everything working as expected
- ⚠️ **Warning** - Non-critical issues, review recommended
- ❌ **Critical** - Requires immediate attention

## Common Commands

### Prana Context Generation
```bash
python3 koshas/annamaya/scripts/prana.py
```

### Vault Statistics
```bash
python3 koshas/annamaya/scripts/vault_stats.py
```

### Daily Practice (Selemene)
```bash
python3 koshas/annamaya/scripts/daily_practice_selemene.py
```

## Quick Fixes

### Missing Agent Files
```bash
cd koshas/annamaya/agents/AGENT_NAME
touch SOUL.md IDENTITY.md MANIFEST.yaml
# Then populate with proper content
```

### Set Selemene API Key
```bash
echo "NOESIS_API_KEY=nk_your_key_here" >> .env
```

### Make Scripts Executable
```bash
chmod +x koshas/annamaya/scripts/*.py
```

## Directory Structure

```
10865xseed/
├── koshas/
│   ├── brahmasthana/      # Core identity (SOUL, IDENTITY, USER)
│   ├── annamaya/          # Scripts & agents
│   ├── pranamaya/         # Logs & telemetry
│   ├── manomaya/          # Memory & patterns
│   ├── vijnanamaya/       # Architecture
│   └── anandamaya/        # Bliss layer
├── docs/                  # Documentation
└── install.sh             # Installer
```

## File Paths

- **Health Check**: `koshas/annamaya/scripts/kosha_health.py`
- **Prana System**: `koshas/annamaya/scripts/prana.py`
- **Core Identity**: `koshas/brahmasthana/SOUL.md`
- **User Config**: `koshas/brahmasthana/USER.md`
- **Environment**: `.env` (not committed)

## Documentation

- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture
- [INSTALL.md](../INSTALL.md) - Installation guide
- [DEVELOPMENT.md](../DEVELOPMENT.md) - Development workflows
- [KOSHA_HEALTH.md](KOSHA_HEALTH.md) - Health monitoring guide
- [PRANA_CONTEXT.md](../PRANA_CONTEXT.md) - Context assembly

---

**Quick Help**: `python3 koshas/annamaya/scripts/kosha_health.py --help`
