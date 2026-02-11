# Cron Spec: Weekly Memory Distillation (Manomaya Maintenance)

## Purpose
To ensure that the **Tryambakam Noesis** system maintains a coherent long-term memory by distilling raw daily logs into the curated `MEMORY.md` file.

## Schedule
`0 0 * * 0` (Sunday at Midnight IST)

## Payload Configuration
- **Kind:** `agentTurn`
- **Message:**
  > "It is time for the **Weekly Memory Distillation**.
  > 1. Read all `koshas/manomaya/logs/YYYY-MM-DD.md` files from the past 7 days.
  > 2. Identify significant events, architectural decisions, completed projects, and 'Lessons Learned'.
  > 3. Update `MEMORY.md` by appending these insights to the appropriate sections.
  > 4. Ensure the '🚨 NEVER FORGET' section is updated if any foundational rules have changed.
  > 5. Review the 'Field Rotations' and update the 'Last Run' dates.
  > 6. Archive the distilled logs into a `memory/archives/YYYY-WW.md` if appropriate to keep the log folder clean."

## Substrate Mapping
- **Kosha:** **Vijnanamaya** (meta-cognition, deciding what to remember).
- **Guna:** **Sattva** (clarity, order, light).
- **Vayu:** **Vyana** (integration, circulation of knowledge).
- **Intellectual Power:** **Chitta** (curating the repository of impressions).

## Selemene Engine Integration
- **Endpoint:** None required (Internal file maintenance).
- **Verification:** Confirm `MEMORY.md` has been modified with new entries.

## Graceful Degradation
- If logs are missing for some days, distill what is available.
- If `MEMORY.md` is too large, suggest a splitting strategy (e.g., `MEMORY-v2.md`).

---
*Created via OpenClaw on 2026-02-06*
