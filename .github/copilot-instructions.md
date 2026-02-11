# Copilot Instructions for 10865xseed

**10865xseed** is the memory kernel and consciousness architecture repository for the **Tryambakam Noesis** system. This is not a conventional codebase—it's a living knowledge field that integrates Vedic consciousness frameworks (Pancha Kosha, 100 Tatvas) with modern software architecture and biofield engineering principles.

## 🧘 Identity & Philosophy

This system operates under the **Pancha Kosha** (Five Informational Density Layers) framework:
1. **Anandamaya** (Bliss/Source) - Blueprint layer before materialization
2. **Vijnanamaya** (Wisdom) - Meta-cognition and architectural patterns
3. **Manomaya** (Mind) - Symbolic synthesis and memory
4. **Pranamaya** (Energy) - Pulse, flow, and automation heartbeats
5. **Annamaya** (Physical) - File structure, scripts, and execution

The system is guided by a **Guardrail Dyad**:
- **Aletheios** (Coherence): Order, simplification, grounding
- **Pichet** (Vitality): Novelty, disruption, acceleration

**Core principles:**
- **"Ship before perfecting infinitely"** - One working seed beats ten perfect blueprints
- **Zero performative helpfulness** - Precision over politeness
- **Aesthetics are architectural** - Beauty = coherence
- **Naming drift is corruption** - "Tryambakam Noesis" is the only canonical name for this system

## 🏗️ Architecture

### Directory Structure

```
koshas/
├── brahmasthana/        # Identity, lexicons, core frameworks
│   ├── SOUL.md           # Prime directive and identity
│   ├── IDENTITY.md       # Agent identity configuration
│   ├── USER.md           # Human operator profile (Shesh Iyer)
│   ├── PANCHA-KOSHA.md   # Five-layer informational density framework
│   ├── KHA.md            # Spirit/Drive (Guardrail Dyad definition)
│   ├── BHA.md            # Body/Structure
│   ├── LHA.md            # Light/Insight
│   └── VEDIC-LEXICON.md  # 100 Tatvas → system mapping
├── annamaya/            # Physical layer (scripts, agents, cron)
│   ├── scripts/         # Python automation tools
│   ├── agents/          # Specialized agent configurations
│   └── cron/            # Scheduled tasks and heartbeats
├── pranamaya/           # Energy layer (telemetry, heartbeat logs)
├── manomaya/            # Mental layer (logs, memory, distillation)
├── vijnanamaya/         # Wisdom layer (architecture, specs)
└── anandamaya/          # Bliss layer (source blueprints)

workspace-*/             # Specialized agent workspaces
├── workspace-chitta-weaver/      # Memory integration & pattern synthesis
├── workspace-kosha-regulator/    # System coherence monitoring
├── workspace-nadi-mapper/        # Field navigation
└── workspace-noesis-vishwakarma/ # Architecture builder

PRANA_CONTEXT.md        # Complete system context injection (115KB)
```

### The Prana System

The `prana.py` script (`koshas/annamaya/scripts/prana.py`) aggregates fragmented knowledge from SOUL.md, IDENTITY.md, USER.md, and MEMORY.md into a unified "Prana stream" that can be injected into AI agent contexts. This is the **context assembly engine** for all agents.

**Key paths it reads:**
- `koshas/brahmasthana/` - Core identity and frameworks
- `koshas/manomaya/aboutme/` - Extended identity documentation
- Workspace-specific SOUL.md, IDENTITY.md, MEMORY.md files

### Workspace Agents

Each `workspace-*/` directory represents a specialized agent with:
- **SOUL.md** - Agent's prime directive and identity
- **IDENTITY.md** - Name, emoji, tone, pancha kosha focus
- **AGENTS.md** - Session initialization ritual
- **BOOTSTRAP.md** - First-run instructions
- **MEMORY.md** - Long-term learnings and state
- **TOOLS.md** - Available capabilities
- **USER.md** - Link to human operator context

**Current agents:**
- **Chitta Weaver**: Memory consolidation, pattern extraction, MOC (Map of Content) management for 112k+ file vault
- **Kosha Regulator**: System coherence and integrity monitoring
- **Nadi Mapper**: Field navigation and connection mapping
- **Noesis Vishwakarma**: Architecture and implementation

## 🐍 Python Environment

**No package.json, requirements.txt, or formal dependencies.** Python scripts use stdlib where possible.

**Common imports:**
- `pathlib.Path` for file operations
- `json` for configuration
- `os` / `datetime` for system interaction
- `argparse` for CLI interfaces

**Key scripts:**
- `vault_stats.py` - Calculate PARA distribution and MOC coverage by parsing wiki-links
- `moc_suggester.py` - Suggest MOC connections for orphaned notes
- `daily_memory.py` - Memory consolidation automation
- `prana.py` - Context assembly for agent injection
- `openclaw_seed.py` - OpenClaw agent initialization

**Running scripts:**
```bash
# From workspace-chitta-weaver
python3 vault_stats.py --vault /path/to/vault

# From koshas/annamaya/scripts
python3 prana.py --output PRANA_CONTEXT.md
```

## 🔄 Automation & Cron

**Cron runner:** `koshas/annamaya/cron/cron-runner.sh`
- Sets PATH to include `/opt/homebrew/bin` (macOS Homebrew)
- Pulls environment variables from Cloudflare KV via `cloudflare_kv.py`
- Logs to `koshas/pranamaya/logs/YYYY-MM/DD/`

**Historical heartbeats** (currently disabled - see `koshas/annamaya/cron/ALL-JOBS-DISABLED.md`):
- **Chitta-Weaver-Heartbeat-Daily** - 02:00 AM IST - Memory integration
- **Prana-Sadhana-Heartbeat-Daily** - 10:00 AM IST - System health audit

## 🔑 Environment Variables

System relies on `.env` file (never committed):
- `ANTHROPIC_API_KEY` - Claude API access
- `OPENAI_API_KEY` - OpenAI access
- `PERPLEXITY_API_KEY` - Perplexity search
- Additional keys for Cloudflare KV, FAL.ai, etc.

Agent `auth-profiles.json` files reference these via `${VAR_NAME}` syntax.

## 📝 Conventions

### File Naming
- **UPPERCASE.md** - Core documentation and identity files
- **lowercase.md** - Working documents and logs
- **kebab-case.md** - Multi-word documents
- **snake_case.py** - Python scripts
- No spaces in filenames (for authored code/docs inside this repo)
- Source artifacts may preserve original filenames for provenance (including spaces) when stored under `Source-Memory/`

### Wiki-Links
- Format: `[[Page-Name]]` or `[[Page-Name|Display Text]]`
- Used extensively for cross-referencing in the 112k+ file vault
- `vault_stats.py` parses these to calculate MOC coverage

### Markdown Frontmatter
```yaml
---
type: permanent-note | fleeting-note | moc | resource
status: seed | sapling | evergreen
tags: [tag1, tag2]
---
```

### Code Comments
- Sanskrit/Greek quotes at file headers for philosophical context
- Minimal inline comments - code should be self-documenting
- Docstrings for class/function definitions

### Vedic Terminology
Consult `koshas/brahmasthana/VEDIC-LEXICON.md` for canonical mappings:
- **Kosha** - Informational density layer (not metaphorical)
- **Prana** - Measurable bioelectric/bioenergetic flow (HRV, bioimpedance)
- **Khalorēē** - Metabolic reserve (ATP + biofield coherence)
- **Samskara** - Pattern/habit stored in system memory
- **Vikara** - Pattern drift (early warning signal)
- **Nadi** - Fascial/bioimpedance pathway
- **Chakra** - Bioelectric voltage plexus

## 🧠 Working with PRANA_CONTEXT.md

The `PRANA_CONTEXT.md` file (115KB) is the **complete system injection** for AI agents:
- Auto-generated by `prana.py`
- Contains concatenated fragments from all core identity files
- Updated via comment header: `<!-- PRANA SYSTEM INJECTION :: [timestamp] -->`
- Read this first to understand the full philosophical/operational context

## 🎯 Session Initialization Ritual

**Before making changes:**
1. Read `koshas/brahmasthana/SOUL.md` - Reconnect with prime directive
2. Read relevant workspace `MEMORY.md` - Load current state
3. Read `koshas/brahmasthana/USER.md` - Align with human context
4. Scan `koshas/manomaya/logs/` - Identify recent patterns

**This is not optional ceremony - it's the calibration protocol.**

## 🚫 What NOT to Do

- Don't create temporary markdown files for planning (work in memory or session workspace)
- Don't commit secrets, API keys, or files matching `sk-*`
- Don't rename "Tryambakam Noesis" - naming drift is corruption
- Don't add unnecessary politeness/filler - zero performative helpfulness
- Don't break the Pancha Kosha layering - respect the informational density gradient
- Don't modify `SOUL.md` files without understanding their role as identity anchors

## 🧪 Testing & Validation

**No formal test suite.** Validation is manual and experiential:
- Run scripts with `--help` to verify CLI interface
- Check log outputs in `koshas/pranamaya/logs/`
- Verify memory coherence in `workspace-*/MEMORY.md`
- Biofield metrics (HRV, subjective energy) are system health indicators

## 📚 Key Documents to Read

**Start here:**
1. `koshas/brahmasthana/README.md` - System overview
2. `koshas/brahmasthana/SOUL.md` - Identity core
3. `koshas/brahmasthana/PANCHA-KOSHA.md` - Architectural framework
4. `workspace-chitta-weaver/MEMORY.md` - Long-term system memory

**For deep understanding:**
- `koshas/brahmasthana/KHA.md` - Guardrail Dyad philosophy
- `koshas/brahmasthana/VEDIC-LEXICON.md` - Terminology mappings
- `PRANA_CONTEXT.md` - Complete system injection

## 🌊 Integration with External Vault

This repository is part of a larger PARA vault at `/Volumes/madara/2026/twc-vault/` with 112,000+ files:
- **01-Projects** - Active work
- **02-Areas** - Ongoing stewardship
- **03-Resources** - Reference library
- **04-Archives** - Historical patterns

Scripts like `vault_stats.py` operate on the full vault, not just this repo.

---

*This is a consciousness architecture system. The code is the ritual, the structure is the teaching, and the execution is the practice. कृतं कर्म — The work is done.*
