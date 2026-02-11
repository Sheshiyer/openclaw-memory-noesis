# TOOLS.md - The Regulator's Instruments

## Primary Ritual Tool
- `vault_stats.py` → Located at `/Volumes/madara/2026/twc-vault/vault_stats.py`.
- **Usage:** `python3 /Volumes/madara/2026/twc-vault/vault_stats.py --vault /Volumes/madara/2026/twc-vault`
- **Purpose:** Analyzes PARA distribution and MOC coverage.

## Environmental Configuration
- **Vault Root:** `/Volumes/madara/2026/twc-vault`
- **Target Density:**
  - Projects (01): 15-20%
  - Areas (02): 20-30%
  - Resources (03): 30-40%
  - Archives (04): 10-20%
- **MOC Coverage Goal:** > 90%

## Cleanup Procedures
- **Stale Check:** Files not modified in > 90 days in `03-Resources` are candidates for archival.
- **Orphan Check:** Markdown files with no inbound links (excluding MOCs themselves).
