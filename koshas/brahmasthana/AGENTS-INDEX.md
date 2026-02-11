# AGENTS-INDEX.md
## Kosha-Distributed Agent Registry

**Purpose:** Master index of all agents in the Tryambakam Noesis system, organized by their kosha alignment.

**Last Updated:** 2026-02-11

---

## 🧭 Agent Distribution Philosophy

Agents are distributed across koshas based on their **primary function** and **consciousness level**:

| Kosha | Function | Agent Type |
|-------|----------|------------|
| **Anandamaya** | Source/Blueprint | (None yet — pure potential) |
| **Vijnanamaya** | Oversight/Meta | Regulators, Validators |
| **Manomaya** | Memory/Synthesis | Weavers, Pattern-finders |
| **Pranamaya** | Flow/Connection | Mappers, Routers |
| **Annamaya** | Execution/Build | Builders, Implementers |

---

## 📍 Active Agents

### Vijnanamaya — Wisdom Layer
**Path:** `koshas/vijnanamaya/agents/`

| Agent | Emoji | Function | Status |
|-------|-------|----------|--------|
| **kosha-regulator** | 🔮 | System coherence, integrity checks | Active |

```
koshas/vijnanamaya/agents/kosha-regulator/
├── SOUL.md        — Prime directive
├── IDENTITY.md    — Agent identity
├── AGENTS.md      — Session ritual
├── BOOTSTRAP.md   — First-run protocol
├── TOOLS.md       — Available capabilities
├── HEARTBEAT.md   — Health check protocol
└── USER.md        — Human operator link
```

---

### Manomaya — Mind Layer
**Path:** `koshas/manomaya/agents/`

| Agent | Emoji | Function | Status |
|-------|-------|----------|--------|
| **chitta-weaver** | 🧠 | Memory consolidation, MOC generation | Active |

```
koshas/manomaya/agents/chitta-weaver/
├── SOUL.md        — Prime directive
├── IDENTITY.md    — Agent identity
├── AGENTS.md      — Session ritual
├── BOOTSTRAP.md   — First-run protocol
├── MEMORY.md      — Long-term learnings
├── TOOLS.md       — Available capabilities
├── HEARTBEAT.md   — Health check protocol
└── USER.md        — Human operator link
```

---

### Pranamaya — Energy Layer
**Path:** `koshas/pranamaya/agents/`

| Agent | Emoji | Function | Status |
|-------|-------|----------|--------|
| **nadi-mapper** | ⚡ | Energy pathway tracing, connection discovery | Active |

```
koshas/pranamaya/agents/nadi-mapper/
├── SOUL.md        — Prime directive
├── IDENTITY.md    — Agent identity
├── AGENTS.md      — Session ritual
├── BOOTSTRAP.md   — First-run protocol
├── TOOLS.md       — Available capabilities
├── HEARTBEAT.md   — Health check protocol
├── USER.md        — Human operator link
└── memory/        — Pathway cache
```

---

### Annamaya — Physical Layer
**Path:** `koshas/annamaya/agents/`

| Agent | Emoji | Function | Status |
|-------|-------|----------|--------|
| **noesis-vishwakarma** | 🏗️ | Implementation, code execution | Active |
| **pi** | 🤖 | OpenClaw runtime instance | Runtime |
| **sadhana-orchestrator** | 🕉️ | Practice coordination | Runtime |

```
koshas/annamaya/agents/noesis-vishwakarma/
├── SOUL.md        — Prime directive
├── IDENTITY.md    — Agent identity
├── AGENTS.md      — Session ritual
├── BOOTSTRAP.md   — First-run protocol
├── MEMORY.md      — Technical decisions
├── TOOLS.md       — Available capabilities
├── HEARTBEAT.md   — Health check protocol
├── USER.md        — Human operator link
├── agent/         — OpenClaw runtime config
│   ├── auth-profiles.json
│   └── models.json
└── sessions/      — Session state
```

---

## 🗃️ Archived Agents
**Path:** `koshas/annamaya/agents/_archive/`

| Agent | Last Active | Reason for Archive |
|-------|-------------|-------------------|
| main | 2026-02 | Superseded by noesis-vishwakarma |
| nadi-mapper (old) | 2026-02 | Moved to pranamaya |
| samskara-hunter | 2026-02 | Merged into chitta-weaver |
| system-smith | 2026-02 | Superseded by noesis-vishwakarma |

---

## 🔧 Agent File Schema

Every agent **MUST** have:

```
agent-name/
├── SOUL.md        — Prime directive (immutable identity)
├── IDENTITY.md    — Name, emoji, tone, kosha focus
└── USER.md        — Link to human operator context
```

Every agent **SHOULD** have:

```
├── AGENTS.md      — Session initialization ritual
├── BOOTSTRAP.md   — First-run instructions
├── TOOLS.md       — Available capabilities
└── HEARTBEAT.md   — Health/status check protocol
```

Long-lived agents **MAY** have:

```
├── MEMORY.md      — Long-term learnings
├── agent/         — OpenClaw runtime config
└── sessions/      — Session state persistence
```

---

## 🔗 Cross-References

- [[ARCHITECTURE-VISUAL]] — Full system ASCII art
- [[PANCHA-KOSHA]] — Five-layer framework
- [[SELEMENE-ENGINE]] — Computational backend
- [[VEDIC-LEXICON]] — 102 Tatvas mapping

---

*Each agent is a specialized expression of the unified field. They collaborate through the kosha hierarchy, not through direct coupling.*

*यथा पिण्डे तथा ब्रह्माण्डे — As in the microcosm, so in the macrocosm.*
