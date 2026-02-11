# OpenClaw Seed

Local scaffolding + installer utilities for this vault.

## Install

```bash
cd /Volumes/madara/2026/twc-vault/_System/10865xseed/koshas/annamaya/scripts
./install_openclaw_seed.sh
```

## TUI

```bash
openclaw-seed
```

## Commands

```bash
openclaw-seed install
openclaw-seed prana --root . --platform claude
openclaw-seed scaffold-agent my-new-agent --root . --template-agent pi
openclaw-seed doctor --root .
```

## Notes

- `install` runs the Rich-based onboarding wizard in [setup_openclaw.py](file:///Volumes/madara/2026/twc-vault/_System/10865xseed/koshas/annamaya/scripts/setup_openclaw.py).
- `prana` uses [PranaSystem](file:///Volumes/madara/2026/twc-vault/_System/10865xseed/koshas/annamaya/scripts/prana.py) to generate a context file.
- `scaffold-agent` copies an existing `models.json` as a baseline into `koshas/annamaya/agents/<agent>/agent/models.json`.
