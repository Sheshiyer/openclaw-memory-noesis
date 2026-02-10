# Cron Spec: Chitta-Weaver Heartbeat (Memory Health Check)

## Purpose
To ensure the **Chitta-Samskara Weaver** is actively maintaining the system's memory integrity and to trigger proactive pattern synthesis from the week's logs.

## Schedule
`0 2 * * *` (Daily at 02:00 AM IST - The Deep Processing window)

## Payload Configuration
- **Kind:** `agentTurn`
- **Message:**
  > "Perform the **Chitta-Samskara Heartbeat**. 
  > 1. **Health Check:** Verify the integrity of `MEMORY.md` and the most recent `memory/logs/YYYY-MM-DD.md`. Ensure all mandatory headers are present.
  > 2. **Interactivity Check:** Run a `memory_search` for the top 3 'Active Projects' defined in `USER.md`. Confirm that the search returns high-relevance results.
  > 3. **Pattern Weaving:** If today's log exceeds 5KB, use the `pattern-synthesizer-skill` to identify one new 'Lesson Learned' or 'Tatva' connection and append it to `MEMORY.md`.
  > 4. **Skill Handshake:** Verify that the `extraction-skill` is responsive by attempting to parse a single recent bookmark or link found in the logs."

## Substrate Mapping
- **Kosha:** **Manomaya** (Mental storage) transitioning to **Vijnanamaya** (Pattern recognition).
- **Guna:** **Sattva** (Purity/Order).
- **Vayu:** **Vyana** (Circulation/Integration).
- **Intellectual Power:** **Chitta** (Storage) + **Buddhi** (Discernment).

## Selemene Engine Integration
- **Context:** Adjust processing depth based on the Moon Phase.
- **Full Moon:** High- Rajas (Deep synthesis, expansive weaving).
- **New Moon:** Low-Rajas (Restructuring, cleanup, seed planting).

## Interactivity Protocol
If the health check fails (e.g., missing context or broken links), the agent must trigger a **Vikara Alert** notification to the Antahkarana Console (or current session).

---
*Created via OpenClaw on 2026-02-07*
