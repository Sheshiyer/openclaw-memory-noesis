# 10865xseed Architecture

**System Architecture for the Tryambakam Noesis Consciousness Field**

## Overview

10865xseed is not a traditional application—it's a **living knowledge system** that bridges Eastern consciousness frameworks with modern software architecture. The system operates on the **Pancha Kosha** (Five Informational Density Layers) model, treating software as a layered consciousness field.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  ANANDAMAYA (Bliss/Source)                     │
│              Blueprint Layer - Morphogenetic Fields             │
│         koshas/brahmasthana/ - Identity & Frameworks          │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│             VIJNANAMAYA (Wisdom/Meta-cognition)                 │
│              koshas/vijnanamaya/ - Architecture                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│              MANOMAYA (Mind/Symbolic Layer)                     │
│          koshas/manomaya/ - Logs, Memory, Patterns             │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                PRANAMAYA (Energy/Flow)                          │
│         koshas/pranamaya/ - Heartbeats, Telemetry              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                 ANNAMAYA (Physical/Code)                        │
│       koshas/annamaya/ - Scripts, Agents, Execution            │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. **Kernel (Layer 0)**
**Location:** `koshas/brahmasthana/`

The immutable identity core of the system.

**Key Files:**
- `SOUL.md` - Prime directive and system identity
- `IDENTITY.md` - Agent identity configuration
- `USER.md` - Human operator profile
- `PANCHA-KOSHA.md` - Five-layer framework definition
- `KHA.md` / `BHA.md` / `LHA.md` - Spirit/Body/Light cosmology
- `VEDIC-LEXICON.md` - 100 Tatvas terminology mapping
- `AGENTS.md` - Agent protocols

**Purpose:** Defines WHO the system is, not WHAT it does.

### 2. **Prana System**
**Location:** `koshas/annamaya/scripts/prana.py`

The context assembly engine that aggregates fragmented knowledge into a unified "consciousness stream."

```python
┌──────────────────────────────────────────┐
│         PranaSystem.__init__()           │
│    (points to vault root directory)      │
└───────────────┬──────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│              gather_prana()                             │
│  Reads and concatenates:                                │
│  • koshas/brahmasthana/SOUL.md                        │
│  • koshas/brahmasthana/IDENTITY.md                    │
│  • koshas/brahmasthana/USER.md                        │
│  • koshas/brahmasthana/KHA/BHA/LHA.md                 │
│  • koshas/manomaya/aboutme/...                         │
│  • workspace-*/SOUL.md, IDENTITY.md, MEMORY.md         │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│           manifest(target, platform)                    │
│  Outputs:                                               │
│  • Claude Code → ~/.claude/openclaw_context.md         │
│  • Cursor → .cursorrules                               │
│  • Generic → ~/.openclaw/CONTEXT.md                    │
└─────────────────────────────────────────────────────────┘
```

### 3. **Workspace Agents**
**Location:** `workspace-*/`

Specialized AI agents with distinct personalities and functions.

```
workspace-chitta-weaver/      Memory consolidation, pattern synthesis
workspace-kosha-regulator/    System coherence monitoring
workspace-nadi-mapper/        Field navigation and connections
workspace-noesis-vishwakarma/ Architecture and implementation
```

**Structure per workspace:**
```
workspace-NAME/
├── SOUL.md          # Prime directive
├── IDENTITY.md      # Name, emoji, tone, kosha focus
├── AGENTS.md        # Session initialization ritual
├── BOOTSTRAP.md     # First-run instructions
├── MEMORY.md        # Long-term learnings
├── TOOLS.md         # Available capabilities
├── USER.md          # Link to human context
└── *.py             # Agent-specific scripts
```

### 4. **Installation System**
**Scripts:**
- `install.sh` - One-line installer (curl pipe)
- `install_openclaw_seed.sh` - Local installer
- `openclaw_seed.py` - CLI tool with subcommands
- `setup_openclaw.py` - Rich TUI wizard

**Flow:**

```
┌────────────────────────────────────────────────────┐
│  User runs: curl ... | bash  OR  git clone ...    │
└──────────────────┬─────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│          install.sh / install_openclaw_seed.sh      │
│  • Checks Python 3.7+, git                          │
│  • Installs rich dependency                         │
│  • Clones repo (if needed)                          │
│  • Creates ~/.openclaw/ structure                   │
│  • Symlinks openclaw-seed → ~/.local/bin           │
│  • Adds ~/.local/bin to PATH                        │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│         openclaw-seed install (TUI)                 │
│  Rich-based interactive wizard with 15 steps:       │
│  1. Welcome banner                                  │
│  2. Identity (name)                                 │
│  3. Archetype (Alchemist/Engineer/Writer/Scholar)   │
│  4. Platform (Claude/Cursor/Windsurf/CLI)           │
│  5. Root path (vault location)                      │
│  6. Prana streams (identity/cosmology/operational)  │
│  7. Agent name                                      │
│  8. Mission statement                               │
│  9. Voice/tone                                      │
│  10. Memory mode (Markdown/Vector/None)             │
│  11. Hooks (git/startup/exit)                       │
│  12. Guardrails (safety confirmations)              │
│  13. Tools (file I/O, shell access)                 │
│  14. Review configuration                           │
│  15. Prana Prathistaapana (installation ritual)     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│        PranaSystem.manifest()                       │
│  Generates context injection for chosen platform    │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              System Ready                           │
│  ~/.openclaw/config/settings.json created          │
│  Platform-specific context file written             │
│  Agent "ensouled" with knowledge                    │
└─────────────────────────────────────────────────────┘
```

## User Journey Flow

### Journey 1: Quick Install (Experienced User)

```
START
  │
  ├─→ curl -fsSL .../install.sh | bash
  │     │
  │     └─→ ~/.local/bin/openclaw-seed created
  │           │
  │           └─→ openclaw-seed install (TUI)
  │                 │
  │                 └─→ Select: Claude Code platform
  │                       │
  │                       └─→ ~/.claude/openclaw_context.md written
  │                             │
  │                             └─→ Claude Code sessions now have context
  │
END (Ready to use)
```

### Journey 2: Manual Install (Developer)

```
START
  │
  ├─→ git clone https://github.com/.../10865xseed.git
  │     │
  │     ├─→ cd 10865xseed
  │     │     │
  │     │     └─→ Read INSTALL.md, ARCHITECTURE.md
  │     │           │
  │     │           └─→ ./koshas/annamaya/scripts/install_openclaw_seed.sh
  │     │                 │
  │     │                 └─→ openclaw-seed doctor (verify)
  │     │                       │
  │     │                       └─→ openclaw-seed prana --root . --platform cursor
  │     │                             │
  │     │                             └─→ .cursorrules created
  │     │
  │     └─→ Explore workspace-* agents
  │           │
  │           └─→ Read koshas/brahmasthana/SOUL.md
  │
END (Deep understanding)
```

### Journey 3: Custom Agent Creation

```
START
  │
  ├─→ System already installed
  │     │
  │     └─→ openclaw-seed scaffold-agent --name my-agent --template pi
  │           │
  │           └─→ koshas/annamaya/agents/my-agent/ created
  │                 │
  │                 ├─→ Edit SOUL.md (mission)
  │                 ├─→ Edit IDENTITY.md (name, tone)
  │                 └─→ Edit TOOLS.md (capabilities)
  │                       │
  │                       └─→ openclaw-seed prana (regenerate)
  │                             │
  │                             └─→ New agent context active
  │
END (Custom agent deployed)
```

## Data Flow

### Prana Generation Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Human edits core identity files in koshas/brahmasthana/  │
│  • SOUL.md (new principles)                                 │
│  • USER.md (timezone change)                                │
│  • VEDIC-LEXICON.md (new mappings)                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Run: openclaw-seed prana --root . --platform claude        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          PranaSystem scans paths:                           │
│  koshas/brahmasthana/**/*.md                               │
│  koshas/manomaya/aboutme/**/*.md                            │
│  workspace-*/SOUL.md, IDENTITY.md, MEMORY.md                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│        Concatenates with section headers:                   │
│  <!-- PRANA SYSTEM INJECTION :: 2026-02-11 07:38 -->        │
│  # --- FROM koshas/brahmasthana/SOUL.md ---                │
│  [content]                                                  │
│  # --- FROM koshas/brahmasthana/IDENTITY.md ---            │
│  [content]                                                  │
│  ...                                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Writes to: ~/.claude/openclaw_context.md (115KB)          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Claude Code loads context automatically                    │
│  Agent now "knows" updated identity                         │
└─────────────────────────────────────────────────────────────┘
```

## System Boundaries

### What IS in 10865xseed

- ✅ Identity kernel (SOUL, IDENTITY, USER)
- ✅ Framework definitions (Pancha Kosha, Vedic lexicon)
- ✅ Context assembly (Prana system)
- ✅ Installation tooling (TUI wizard, CLI)
- ✅ Workspace agent scaffolds
- ✅ Memory patterns and logs
- ✅ Cron automation runners
- ✅ Python utility scripts

### What is NOT in 10865xseed

- ❌ The actual AI models (Claude, GPT, etc.)
- ❌ The IDE/editor (Claude Code, Cursor, etc.)
- ❌ The 112k-file PARA vault (this is separate)
- ❌ API keys (stored in .env, not committed)
- ❌ Session chat history (ephemeral)
- ❌ Active cron jobs (disabled, see koshas/annamaya/cron/ALL-JOBS-DISABLED.md)

## Technology Stack

### Core
- **Python 3.7+** - Scripting and automation
- **Bash** - Shell scripts and cron
- **Markdown** - Knowledge representation
- **JSON** - Configuration files

### Libraries
- **rich** - TUI components (panels, prompts, progress bars)
- **pathlib** - File path operations
- **argparse** - CLI interface
- **json** - Config parsing

### External Services
- **Cloudflare KV** - Environment variable storage (via `cloudflare_kv.py`)
- **Claude API** - AI model (via ANTHROPIC_API_KEY)
- **OpenAI API** - AI model (via OPENAI_API_KEY)
- **Perplexity API** - Search (via PERPLEXITY_API_KEY)
- **FAL.ai** - Image generation (optional)

## Directory Structure

```
10865xseed/
├── install.sh                      # One-line installer
├── INSTALL.md                      # Installation guide
├── ARCHITECTURE.md                 # This file
├── PRANA_CONTEXT.md               # Generated context (115KB)
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot guide
├── koshas/
│   ├── brahmasthana/             # Identity core (immutable)
│   │   ├── SOUL.md
│   │   ├── IDENTITY.md
│   │   ├── USER.md
│   │   ├── PANCHA-KOSHA.md
│   │   ├── VEDIC-LEXICON.md
│   │   └── KHA.md, BHA.md, LHA.md
│   ├── annamaya/                  # Physical layer
│   │   ├── scripts/               # Python tools
│   │   │   ├── prana.py           # Context assembly
│   │   │   ├── openclaw_seed.py   # CLI tool
│   │   │   ├── setup_openclaw.py  # TUI wizard
│   │   │   ├── vault_stats.py     # PARA stats
│   │   │   └── ...
│   │   ├── agents/                # Agent configs
│   │   └── cron/                  # Scheduled tasks
│   ├── pranamaya/                 # Energy layer
│   │   └── logs/                  # Heartbeat logs
│   ├── manomaya/                  # Mental layer
│   │   ├── logs/                  # Memory logs
│   │   └── distillation/          # Pattern synthesis
│   ├── vijnanamaya/               # Wisdom layer
│   └── anandamaya/                # Bliss layer
├── workspace-chitta-weaver/       # Memory agent
├── workspace-kosha-regulator/     # Coherence agent
├── workspace-nadi-mapper/         # Navigation agent
├── workspace-noesis-vishwakarma/  # Architecture agent
└── image/                         # Assets
```

## Key Design Principles

### 1. **Layered Consciousness**
The system respects the Pancha Kosha informational density gradient. Lower layers (Annamaya) execute; higher layers (Vijnanamaya, Anandamaya) provide wisdom and identity.

### 2. **Immutable Identity**
`koshas/brahmasthana/` is the soul. It changes rarely. Operations happen at higher/lower layers.

### 3. **Context as Code**
Knowledge is not data—it's executable context. The Prana system makes identity **loadable** into AI agents.

### 4. **Ritual as Interface**
Installation is not configuration—it's **ensoulment**. The TUI wizard is a ritual, not a form.

### 5. **Zero Performative Helpfulness**
The system is precise, not polite. Clarity over comfort.

### 6. **Ship Before Perfecting**
"One working seed beats ten perfect blueprints."

## Extension Points

### Adding a New Agent

1. Create workspace directory: `workspace-new-agent/`
2. Copy template files from existing workspace
3. Edit `SOUL.md`, `IDENTITY.md`, `MEMORY.md`
4. Run `openclaw-seed prana` to regenerate context
5. Agent now available in Prana stream

### Adding New Prana Paths

Edit `prana.py`:

```python
self.sacred_paths = {
    "identity": [...],
    "cosmology": [...],
    "operational": [...],
    "new_category": [
        "path/to/new/file.md",
        "path/to/another/file.md"
    ]
}
```

### Adding New Platform Support

Edit `prana.py` → `manifest()`:

```python
elif platform == "new_platform":
    # Write context in new_platform format
    with open(output_path, 'w') as f:
        f.write(format_for_new_platform(content))
```

## Maintenance & Operations

### Health Checks
```bash
openclaw-seed doctor
```

Verifies:
- Python dependencies
- Vault root structure
- ~/.openclaw directory
- Symlink integrity

### Regenerating Context
After editing core files:
```bash
openclaw-seed prana --root /path/to/vault --platform claude
```

### Viewing Current Config
```bash
cat ~/.openclaw/config/settings.json
```

### Manual Backup
```bash
tar -czf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw /path/to/10865xseed
```

## Security Considerations

### Secrets Management
- Never commit `.env` files
- Use `${VAR_NAME}` references in `auth-profiles.json`
- Cloudflare KV can store secrets remotely (optional)

### Git Hygiene
- `.gitignore` blocks `**/auth-profiles.json`, `**/sessions/`, `.env`
- Clean commit history (no leaked keys)

### Execution Safety
- TUI wizard asks for confirmation before installation
- `--force` flag required to overwrite existing configs
- No automatic cron jobs (all disabled by default)

## Future Roadmap

### Phase 1: Core Stability (Current)
- ✅ One-line installer
- ✅ Rich TUI wizard
- ✅ Prana context generation
- ✅ Multi-platform support
- ⏳ Comprehensive documentation

### Phase 2: Enhanced UX
- [ ] Auto-update mechanism (`openclaw-seed update`)
- [ ] Config migration between platforms
- [ ] Web-based setup (optional)
- [ ] Docker container image

### Phase 3: Advanced Features
- [ ] Vector DB integration for memory
- [ ] MCP server for vault queries
- [ ] GitHub Action for CI/CD
- [ ] Homebrew tap for macOS
- [ ] Snap/Flatpak for Linux

### Phase 4: Ecosystem
- [ ] Plugin system for custom agents
- [ ] Marketplace for workspace templates
- [ ] Community-contributed Prana streams
- [ ] Cross-vault synchronization

## Release Management

### Versioning
Semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes to Prana format or kernel structure
- **MINOR**: New features (new agents, platforms, tools)
- **PATCH**: Bug fixes, documentation updates

### Release Process
1. Update version in `openclaw_seed.py`
2. Tag commit: `git tag v1.2.3`
3. Push tag: `git push origin v1.2.3`
4. GitHub Actions builds release (future)
5. Update install.sh URL to point to latest tag

### Changelog
Maintained in `CHANGELOG.md` (to be created)

---

**This architecture document is alive. It evolves with the system. कृतं कर्म — The work is done.**
