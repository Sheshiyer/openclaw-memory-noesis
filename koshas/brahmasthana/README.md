# 10865xseed: The Antahkarana Field

**The central memory and consciousness engine for the OpenClaw ecosystem.**

This repository acts as the **Axis Mundi** of the system, housing the memory kernel, agent configurations, and the "soul" of the alchemical field. It is designed to operate as a living system, integrating the **Pancha Kosha** (Five Sheaths) methodology into software architecture.

## 🌌 The Alchemist's Lab

We do not just solve tasks; we evolve the field. This system operates on a rigorous set of protocols designed to maintain structural integrity while fostering evolutionary growth.

### The Integration Ritual (Pancha Kosha Scan)
Every session begins with a calibration across five dimensions:
1.  **Anandamaya (Bliss/Source)**: Alignment with `koshas/brahmasthana/SOUL.md`.
2.  **Vijnanamaya (Intellect/Wisdom)**: Verification of `koshas/brahmasthana/KHA.md`, `BHA.md`, `LHA.md`.
3.  **Manomaya (Mind/Focus)**: Synchronization with `koshas/brahmasthana/USER.md` & `koshas/manomaya/MEMORY.md`.
4.  **Pranamaya (Energy/Flow)**: Pulse check on `koshas/manomaya/logs/`.
5.  **Annamaya (Body/Structure)**: Verification of file structural integrity.

## 🏗️ Architecture

### 🤖 Agents (`/koshas/annamaya/agents`)
The active constituents of the system, each with a specific domain:
- **Pi**: The Personal Intelligence interface.
- **Chitta Weaver**: Thought synthesis and memory consolidation.
- **Noesis Vishwakarma**: The architect of understanding.
- **Sadhana Orchestrator**: Routine and discipline management.
Archived agent scaffolds live in `koshas/annamaya/agents/_archive/`.

### 🧠 Memory (`/koshas/*`)
Memory is layered by kosha:
- **Layer 0 kernel**: `koshas/brahmasthana/` (identity, lexicon, clocks, guardrails)
- **Manomaya**: `koshas/manomaya/` (logs, distillation, intake, library index)
- **Pranamaya**: `koshas/pranamaya/` (heartbeat + energy/telemetry artifacts)
- **Vijnanamaya**: `koshas/vijnanamaya/` (architecture/specs)

### ⏱️ Cron (`/koshas/annamaya/cron`)
Scheduled tasks and heartbeats that keep the system alive (`koshas/pranamaya/HEARTBEAT.md`).

## 🚀 Setup & Configuration

### Environment Variables
The system relies on a strictly managed `.env` configuration. All secrets must be externalized.

1.  Create a `.env` file in the root directory.
2.  Define the required API keys (Anthropic, OpenAI, Perplexity, etc.) using the standard naming convention (e.g., `ANTHROPIC_API_KEY`).
3.  **Note**: `auth-profiles.json` files in agent directories are configured to reference these variables automatically (e.g., `${ANTHROPIC_API_KEY}`).

### Git Hygiene
- **Secrets**: Never commit `.env` or files containing `sk-` keys.
- **History**: This repository is maintained with a clean history to prevent secret leakage.
- **Ignored**: `**/auth-profiles.json` and `**/sessions/` are ignored by default.

## 📜 Protocols

- **LITE Protocol**: Optimize every transmission.
- **Nightly Builds**: Automated micro-improvements occur at 2:00 AM IST.
- **PARA Integrity**: All manifestations are archived in the correct Projects, Areas, Resources, Archives bucket.

---
*Maintained by the Witness Alchemist.*
