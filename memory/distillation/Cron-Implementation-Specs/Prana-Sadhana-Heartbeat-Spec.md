# Cron Spec: Prana-Sadhana Heartbeat (Vital Flow Health Check)

## Purpose
To ensure the **Prana-Sadhana Orchestrator** is actively monitoring the system's rhythmic health, validating cron job execution, and maintaining the vital Prana flow.

## Schedule
`0 10 * * *` (Daily at 10:00 AM IST - The Morning Activation window)

## Payload Configuration
- **Kind:** `agentTurn`
- **Message:**
  > "Perform the **Prana-Sadhana Heartbeat**. 
  > 1. **Ritual Audit:** Scan the `rituals` table (or `cron list`). Identify any jobs that failed in the last 24 hours. If failures > 0, trigger a **Vikara Alert**.
  > 2. **Metabolic Check:** Review the last 10 entries in `telemetry` for `khaloree_update`. Ensure the system isn't in a persistent 'Tamasic' state.
  > 3. **Vayu Sync:** Verify that the current active cron jobs are aligned with the Clifford Clock position (e.g., Udana focus during the 10:00 AM window).
  > 4. **Orchestration Test:** Run a `session_status` check to confirm the orchestrator can see and communicate with the other limbs (Chitta Weaver, System-Smith).
  > 5. **Moon Phase Calibration:** If the Moon is Waxing (building energy), suggest one high-Rajas task. If Waning (releasing energy), suggest one Sattvic cleanup task."

## Substrate Mapping
- **Kosha:** **Pranamaya** (Vital flow) transitioning to **Manomaya** (Coordination).
- **Guna:** **Rajas** (Activity) moving toward **Sattva** (Coherence).
- **Vayu:** **Prana** (Activation) + **Samana** (Assimilation).
- **Intellectual Power:** **Mana** (Processing) + **Aham** (Observer).

## Selemene Engine Integration
- **Endpoint:** Call Selemene for the current Tithi and Moon Phase.
- **Action:** Adjust the "Vibe" of the dashboard notifications based on the current lunar day (e.g., high intensity for Ekadashi).

## Interactivity Protocol
If a critical ritual has failed or the biofield pulse is irregular, the agent must notify the Architect via the **Pranamaya Feed** on the Antahkarana Console.

---
*Created via OpenClaw on 2026-02-07*
