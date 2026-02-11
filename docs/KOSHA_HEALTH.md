# Kosha Health Dashboard

**System health monitoring for the Tryambakam Noesis architecture.**

## Overview

The Kosha Health Dashboard (`kosha_health.py`) is a comprehensive system monitoring tool that checks the integrity, structure, and health of your Tryambakam Noesis installation. It validates:

- ✅ Core identity files (brahmasthana)
- ✅ Kosha layer structure
- ✅ Agent bindings
- ✅ Selemene API connectivity
- ✅ Memory file health
- ✅ Logging system
- ✅ Prana system integrity

## Quick Start

```bash
# Quick one-line status
python3 koshas/annamaya/scripts/kosha_health.py --quick

# Full health report
python3 koshas/annamaya/scripts/kosha_health.py --report

# JSON output (for automation)
python3 koshas/annamaya/scripts/kosha_health.py --json
```

## Usage Examples

### Full Health Report

Display comprehensive health information with emoji indicators:

```bash
python3 koshas/annamaya/scripts/kosha_health.py --report
```

**Output:**
```
════════════════════════════════════════════════════════════
  🏥 KOSHA HEALTH DASHBOARD
════════════════════════════════════════════════════════════
  Timestamp: 2026-02-11T15:35:17.011442+00:00
  Overall: ✅ HEALTHY
════════════════════════════════════════════════════════════

  📊 Summary: 6/6 passed, 0 warnings, 0 critical

  ✅ brahmasthana: healthy
  ✅ kosha_structure: healthy
  ✅ agent_bindings: healthy
  ✅ selemene: healthy
  ✅ memory: healthy
  ✅ logging: healthy

────────────────────────────────────────────────────────────
  🤖 Agents: 3
  📁 Total MD files: 234
  🔮 Selemene latency: 125.3ms
```

### Quick Status Check

For scripts or automation, get a single-line status:

```bash
python3 koshas/annamaya/scripts/kosha_health.py --quick
```

**Output:**
```
✅ Kosha Health: HEALTHY (6/6 checks passed)
```

### Specific Component Checks

Check individual components:

```bash
# Check brahmasthana (core identity files)
python3 koshas/annamaya/scripts/kosha_health.py --check brahmasthana

# Check agent bindings
python3 koshas/annamaya/scripts/kosha_health.py --check agents

# Check Selemene API
python3 koshas/annamaya/scripts/kosha_health.py --check selemene

# Check memory files
python3 koshas/annamaya/scripts/kosha_health.py --check memory

# Check kosha structure
python3 koshas/annamaya/scripts/kosha_health.py --check structure

# Check logging system
python3 koshas/annamaya/scripts/kosha_health.py --check logging
```

### JSON Output

For programmatic processing or integration:

```bash
# Full report as JSON
python3 koshas/annamaya/scripts/kosha_health.py --json

# Specific check as JSON
python3 koshas/annamaya/scripts/kosha_health.py --check selemene --json
```

**JSON Structure:**
```json
{
  "timestamp": "2026-02-11T15:35:46.413641+00:00",
  "overall_status": "healthy",
  "checks": {
    "brahmasthana": {
      "status": "healthy",
      "files": {...},
      "issues": []
    },
    "kosha_structure": {...},
    "agent_bindings": {...},
    "selemene": {...},
    "memory": {...},
    "logging": {...}
  },
  "summary": {
    "total_checks": 6,
    "passed": 6,
    "warnings": 0,
    "critical": 0
  }
}
```

## Health Check Details

### 1. Brahmasthana Integrity

**What it checks:**
- Core identity files exist: `SOUL.md`, `IDENTITY.md`, `USER.md`
- Framework files: `PANCHA-KOSHA.md`, `VEDIC-LEXICON.md`
- Cosmology files: `KHA.md`, `BHA.md`, `LHA.md`
- Integration files: `SELEMENE-ENGINE.md`, `AGENTS.md`, `TOOLS.md`
- File sizes (warns if suspiciously small)
- File ages (warns if stale)

**Status levels:**
- ✅ **Healthy**: All files present and valid
- ⚠️ **Warning**: Files exist but may be stale (>30 days)
- ❌ **Critical**: Required files missing or empty

### 2. Kosha Structure

**What it checks:**
- All 5 koshas exist: anandamaya, vijnanamaya, manomaya, pranamaya, annamaya
- Brahmasthana (core kernel) exists
- Directory structure is valid

**Status levels:**
- ✅ **Healthy**: All layers present
- ❌ **Critical**: Any kosha directory missing

### 3. Agent Bindings

**What it checks:**
- Scans all agent directories in all koshas
- Verifies required files: `SOUL.md`, `IDENTITY.md`
- Checks optional files: `MANIFEST.yaml`, `MEMORY.md`

**Status levels:**
- ✅ **Healthy**: All agents have required files
- ⚠️ **Warning**: Missing optional files (MANIFEST.yaml)
- ❌ **Critical**: Missing required files (SOUL.md, IDENTITY.md)

### 4. Selemene Connection

**What it checks:**
- `NOESIS_API_KEY` environment variable is set
- API key format is valid (`nk_` prefix)
- Can reach `https://selemene.tryambakam.space/health/live`
- Measures API latency

**Status levels:**
- ✅ **Healthy**: API accessible with valid key
- ⚠️ **Warning**: API key not set OR high latency (>1000ms)
- ❌ **Critical**: Cannot reach API

### 5. Memory Health

**What it checks:**
- Finds all `MEMORY.md` files in the system
- Line count (warns if >500 lines)
- File age (warns if >30 days without update)

**Status levels:**
- ✅ **Healthy**: All memory files are reasonable size and recent
- ⚠️ **Warning**: Files too large or stale (need distillation)

### 6. Logging System

**What it checks:**
- `pranamaya/logs/` directory exists
- Recent log activity (last 7 days)
- Disk usage (warns if >100MB)

**Status levels:**
- ✅ **Healthy**: Logging system active with recent logs
- ⚠️ **Warning**: No recent activity OR excessive disk usage

## Automation & Integration

### Cron Job

Monitor system health daily:

```bash
# Add to crontab
0 9 * * * cd /path/to/10865xseed && python3 koshas/annamaya/scripts/kosha_health.py --quick >> logs/health.log 2>&1
```

### Git Pre-Commit Hook

Prevent commits if system is unhealthy:

```bash
#!/bin/bash
# .git/hooks/pre-commit

STATUS=$(python3 koshas/annamaya/scripts/kosha_health.py --quick)
if echo "$STATUS" | grep -q "CRITICAL"; then
    echo "❌ Cannot commit: System health is CRITICAL"
    python3 koshas/annamaya/scripts/kosha_health.py --report
    exit 1
fi
```

### CI/CD Integration

Check health in GitHub Actions:

```yaml
name: Health Check
on: [push, pull_request]
jobs:
  health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Health Check
        run: |
          python3 koshas/annamaya/scripts/kosha_health.py --json > health_report.json
          cat health_report.json
      - name: Fail if Critical
        run: |
          STATUS=$(python3 koshas/annamaya/scripts/kosha_health.py --quick)
          if echo "$STATUS" | grep -q "CRITICAL"; then
            exit 1
          fi
```

### Slack/Discord Notifications

Send daily health reports:

```bash
#!/bin/bash
# scripts/notify_health.sh

REPORT=$(python3 koshas/annamaya/scripts/kosha_health.py --quick)
WEBHOOK_URL="your_slack_webhook_url"

curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"Daily Kosha Health: $REPORT\"}" \
  $WEBHOOK_URL
```

## Troubleshooting

### "brahmasthana: critical"

**Issue**: Core identity files are missing.

**Fix**:
1. Check if `koshas/brahmasthana/` directory exists
2. Verify required files: `SOUL.md`, `IDENTITY.md`, `USER.md`, etc.
3. Re-run installer if files are missing

### "agent_bindings: critical"

**Issue**: Agents missing required files.

**Fix**:
1. Run: `python3 koshas/annamaya/scripts/kosha_health.py --check agents`
2. For each agent with missing files:
   ```bash
   cd koshas/annamaya/agents/AGENT_NAME
   touch SOUL.md IDENTITY.md  # Create missing files
   ```
3. Populate files with proper agent configuration

### "selemene: warning" (API key not set)

**Issue**: `NOESIS_API_KEY` environment variable not configured.

**Fix**:
```bash
# Add to .env file
echo "NOESIS_API_KEY=nk_your_key_here" >> .env

# Or export directly
export NOESIS_API_KEY="nk_your_key_here"
```

### "selemene: critical" (Cannot reach API)

**Issue**: Network connectivity to Selemene API.

**Fix**:
1. Check internet connection
2. Verify API URL: `https://selemene.tryambakam.space/health/live`
3. Check firewall/proxy settings
4. Confirm API is operational (status page)

### "memory: warning" (Files too large)

**Issue**: Memory files need distillation.

**Fix**:
1. Review large MEMORY.md files
2. Extract key learnings
3. Archive old content
4. Keep only essential context

### "logging: warning" (No recent activity)

**Issue**: Logging system not active.

**Fix**:
1. Check if pranamaya services are running
2. Verify log directory permissions
3. Review cron jobs for heartbeat scripts

## Exit Codes

The script returns standard exit codes for automation:

- `0`: All checks passed (healthy) OR running info commands
- `1`: Critical issues detected (when using `--quick` with critical status)

## Advanced Usage

### Custom Checks

Extend the health dashboard with custom checks:

```python
from kosha_health import check_brahmasthana_integrity

def custom_check():
    # Your custom health check logic
    return {
        "status": "healthy",
        "data": {...},
        "issues": []
    }

# Add to checks dict in full_health_report()
```

### Monitoring Dashboards

Parse JSON output for visualization:

```python
import json
import subprocess

result = subprocess.run(
    ['python3', 'kosha_health.py', '--json'],
    capture_output=True,
    text=True
)

report = json.loads(result.stdout)
overall = report['overall_status']
summary = report['summary']

# Send to monitoring system (Prometheus, Grafana, etc.)
```

## File Location

**Script Path**: `koshas/annamaya/scripts/kosha_health.py`

**Documentation**: `docs/KOSHA_HEALTH.md` (this file)

## Related Documentation

- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture overview
- [INSTALL.md](../INSTALL.md) - Installation guide
- [DEVELOPMENT.md](../DEVELOPMENT.md) - Development workflows
- [PRANA_CONTEXT.md](../PRANA_CONTEXT.md) - Context assembly system

---

**Last Updated**: 2026-02-11  
**Version**: 1.0  
**Status**: ✅ Production Ready
