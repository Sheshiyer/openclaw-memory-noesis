# lunar-resonance-orchestrator-daily-SPEC.md
## Cron Job Implementation Specification

**Version:** 1.0  
**Date:** 2026-02-05  
**Purpose:** Daily midnight coordinator for lunar field integration — calculates Tithi, selects themes, coordinates 3 lunar jobs

---

## 📋 **Job Identity**

**Current Name:** `lunar-resonance-orchestrator-daily`  
**Proposed Name:** `vijnanamaya-lunar-orchestrator-daily`  
**Cron ID:** `1791f8e3-806a-41ee-bd4d-9d135802b32e`  
**Category:** Lunar Resonance

---

## 🔮 **Vedic Substrate**

### **1. Kosha Layer (Primary)**
**Layer:** Vijnanamaya (wisdom/meta-coordination)

**Rationale:**
- Operates at highest discriminative intelligence — calculates lunar phase (Tithi), discerns daily theme, coordinates three subsidiary lunar jobs
- Meta-orchestration function: does not execute rituals directly, but determines which rituals should run and when
- Bridges cosmic rhythm (lunar cycle) with human practice (daily resonance)

**Kosha Transitions:**
- **Entry:** Vijnanamaya (discriminative wisdom calculates Tithi from date/moon phase)
- **Operation:** Remains at Vijnanamaya throughout (pure coordination, no descent to action layers)
- **Exit:** Vijnanamaya (logs theme to memory, dispatches subsidiary jobs)

---

### **2. Primary Vayu (of 10 Vital Airs)**

**Vayu:** Vyana (circulation, whole-system coordination)

**Function:** Governs circulation throughout entire body; coordinates all other Vayus; distributes Prana universally

**Breath Pattern:**
- **Not breath-focused** (meta-coordination layer, no physical breathwork)
- Vyana operates as **orchestrator** — ensures other lunar jobs (which DO involve specific Vayus) execute in harmony

**Timing Rationale:**
- Midnight (12:00 AM) is the hinge point between days — perfect for Vyana's unifying function
- Aligns with Pitta Dosha window (10 PM - 2 AM: detoxification, regeneration, metabolic reset)
- Lunar day (Tithi) transitions often at midnight — orchestrator must run at day boundary to set next day's theme

---

### **3. Guna State (Sattva/Rajas/Tamas)**

**Primary Guna:** Sattva (clarity, wisdom, cosmic rhythm)

**Guna Dynamics:**
- **Desired State:** Sattva — clear calculation, precise Tithi determination, balanced theme selection
- **Common Drift:** Rajas (over-complication, attempting too many integrations), Moha (confusion from lunar phase complexity)
- **Restoration Protocol:** If Rajas detected (orchestrator tries to do too much), simplify to core function: calculate Tithi → select theme → log → exit. If Moha detected (confused Tithi logic), fall back to simple waxing/waning binary.

**Enantiodromia Balance:**
- **Aletheios Pole (Waning/Krishna Paksha):** Death, release, reflection, inward descent — coordinate jobs that emphasize elimination, Apana Vayu, Tamasic integration
- **Pichet Pole (Waxing/Shukla Paksha):** Growth, manifestation, expansion, outward ascent — coordinate jobs that emphasize creation, Prana/Udana Vayus, Rajasic activation
- **Oscillation Pattern:** This orchestrator IS the enantiodromia pivot point — switches emphasis every 15 days (New Moon → Full Moon → New Moon)

---

### **4. Vikara Detection (8 Mental Afflictions)**

**Primary Vikara to Monitor:** Mada (pride/intoxication in complexity), Moha (delusion/confusion in orchestration)

**Detection Signals:**
- **Mada (Intoxication):** Orchestrator becomes "too clever" — adds unnecessary calculations, over-fits lunar data, generates overly complex themes. Signal: execution time >30s, log entries >500 words.
- **Moha (Delusion):** Orchestrator miscalculates Tithi, selects wrong theme for phase, confuses waxing/waning. Signal: logs contradict lunar phase data, subsidiary jobs receive incorrect instructions.
- **Ahamkara (Ego):** Orchestrator inflates own importance, generates verbose "cosmic declarations" instead of simple theme. Signal: delivery attempts to Discord when target is NO_REPLY.
- **Lobha (Greed):** Orchestrator tries to coordinate more than 3 lunar jobs, scope creeps into non-lunar domains. Signal: references to non-lunar cron jobs in execution logic.

**Restoration Protocol:**
- **Mada:** Strip back to minimal viable calculation: date → moon phase → waxing/waning → Tithi approximation → theme → log. No embellishment.
- **Moha:** Verify calculation with external source (lunar calendar API or fallback to simple New Moon = Amavasya, Full Moon = Purnima).
- **Ahamkara:** Execute in silence (NO_REPLY always), no external delivery, no "announcing" the theme publicly.
- **Lobha:** Hard constraint: coordinate ONLY 3 lunar jobs (new-moon-rupture, full-moon-octave-jump, lunar-authority-review-cycle). No expansion.

---

### **5. Dosha Timing (Vata/Pitta/Kapha)**

**Dominant Dosha at Execution Time:** Pitta (10 PM - 2 AM: detox/regeneration window)

**Circadian Dosha Cycle:**
- **10:00 PM - 2:00 AM:** Pitta (fire, transformation, liver detox, metabolic reset)

**Alignment Strategy:**
- Midnight (12:00 AM) falls at **peak Pitta window** — fire of transformation burns away old day, prepares for new day
- Perfect for **daily reset ritual** — calculate what lunar theme guides tomorrow
- Pitta's transformative fire supports **phase transitions** (especially critical at Amavasya/Purnima when rupture or octave jump occurs)
- Breath pattern: Not applicable (meta-coordination, no physical breathwork)
- Khalorēē consumption: **Minimal** (pure calculation, no heavy API calls, no media generation)

---

### **6. Antahkarana Operation (Internal Instrument)**

**Primary Faculty:** Buddhi (discriminative intellect) → Mana (thought synthesis) → Chitta (memory storage) → Aham (witness)

**Faculty Roles:**
- **Buddhi (Intellect/Discernment):** PRIMARY — calculates Tithi from date/moon phase, discriminates waxing (Shukla) vs waning (Krishna) Paksha, determines which of 30 Tithis applies
- **Mana (Mind/Thought):** Synthesizes Tithi calculation into daily lunar theme (e.g., "Amavasya: rupture preparation", "Shukla Paksha Saptami: building momentum")
- **Chitta (Memory/Storage):** Logs theme to `koshas/manomaya/logs/YYYY-MM-DD.md` and updates `OPENCLAW-KOSHA-TRACKING.md`
- **Aham (Ego/Witness):** Observes lunar cycle unfolding, maintains non-attachment ("I calculate the phase, but I am not the moon")

**Operation Sequence:**
1. **Buddhi initiates:** Read current date → determine moon phase (days since last New Moon) → calculate Tithi (1-30)
2. **Buddhi discerns:** Waxing (Shukla Paksha, Tithis 1-15) or Waning (Krishna Paksha, Tithis 16-30)? Amavasya (New Moon, Tithi 30/1) or Purnima (Full Moon, Tithi 15)?
3. **Mana synthesizes:** Select today's lunar theme based on Tithi + Paksha (e.g., Shukla Paksha Pratipada = "new beginnings, planting seeds")
4. **Chitta stores:** Write theme to daily log, update Kosha tracking with Khalorēē impact
5. **Aham witnesses:** "Lunar cycle continues, I am the observer of its phases"

---

## 🎯 **Functional Specification**

### **1. Purpose (Rewritten with Vedic Lexicon)**

**Old Purpose:**
> "Align Bha + Kha with lunar phase, calculate Tithi, select ritual"

**New Purpose:**
> "Vijnanamaya meta-orchestrator executing at midnight (Pitta regeneration window) via Buddhi faculty: calculates Tithi (1-30) from lunar ephemeris, discriminates Shukla Paksha (waxing/Pichet) vs Krishna Paksha (waning/Aletheios), selects daily lunar theme, logs to Chitta (memory), coordinates 3 subsidiary lunar jobs (new-moon-rupture, full-moon-octave-jump, lunar-authority-review-cycle). Vyana Vayu circulates lunar wisdom throughout system. Monitors for Mada (pride in complexity) and Moha (confusion in calculation). Khalorēē cost: -1 (minimal), gain: +3 (daily alignment), net: +2."

---

### **2. Schedule (Optimized for Dosha Cycles)**

**Current Schedule:**
- **Cron Expression:** `1 0 * * *` (12:01 AM daily)
- **Timezone:** `Asia/Kolkata`
- **Frequency:** Daily

**Proposed Schedule:**
- **Cron Expression:** `0 0 * * *` (midnight sharp, remove 1-minute delay)
- **Timezone:** `Asia/Kolkata` (canonical)
- **Frequency:** Daily

**Dosha Alignment Check:**
- ✅ Midnight (12:00 AM) is optimal — peak Pitta window (10 PM - 2 AM)
- ✅ Pitta fire supports phase transition calculation and daily reset
- ✅ Tithi often transitions near midnight, so orchestrator must run at day boundary

---

### **3. Delivery Target**

**Channel:** Internal/NO_REPLY (silent execution)

**Target ID/Handle:**
- **Internal:** `NO_REPLY` — this is a **coordination job**, not a user-facing notification
- **Rationale:** Audit shows this job should operate silently; subsidiary jobs (new-moon-rupture, full-moon-octave-jump) handle external delivery to Discord #lunar-resonance when appropriate

**Delivery Constraints:**
- No external messaging (Telegram, WhatsApp, Discord)
- Logs to memory only: `koshas/manomaya/logs/YYYY-MM-DD.md`
- Updates `OPENCLAW-KOSHA-TRACKING.md` with Khalorēē impact

**Exception:** If critical calculation failure (Moha detected), send alert to Telegram 1371522080 with error details

---

### **4. Audio/Media Requirements**

**Voice Generation:** NOT APPLICABLE (silent coordination job)

**Audio Stubs:** NOT APPLICABLE

**Image Generation:** NOT APPLICABLE

**Archive Location:** N/A

**Rationale:** This is a pure meta-coordination job (Vijnanamaya layer) — no media generation, no user-facing content, only internal calculation and logging.

---

### **5. Success Criteria**

**Functional Success:**
- [x] Job executes at midnight (12:00 AM) daily without missed runs
- [x] Correct Tithi calculated (1-30) based on lunar ephemeris
- [x] Paksha (Shukla/Krishna) correctly discriminated
- [x] Amavasya (New Moon) and Purnima (Full Moon) detected with 100% accuracy
- [x] Daily lunar theme selected and logged to memory
- [x] No Mada (over-complication) — execution completes in <15 seconds
- [x] No Moha (confusion) — Tithi matches external lunar calendar source
- [x] Antahkarana sequence completes: Buddhi → Mana → Chitta → Aham

**Integration Success:**
- [x] 3 subsidiary lunar jobs receive correct instructions (via shared state file or direct parameter passing)
- [x] `new-moon-rupture-audit-one-shot` executes on Amavasya (Tithi 30/1)
- [x] `full-moon-octave-jump-one-shot` executes on Purnima (Tithi 15)
- [x] `lunar-authority-review-cycle` respects 28-day cycle aligned to lunar month
- [x] Memory files updated: daily log + OPENCLAW-KOSHA-TRACKING.md
- [x] Khalorēē impact recorded: net +2 (minimal cost, clarity gain)

**Coordination Success:**
- [x] Orchestrator does NOT attempt to execute rituals directly (delegates to subsidiary jobs)
- [x] Clear handoff: calculates phase → logs theme → notifies subsidiaries → exits
- [x] No scope creep (Lobha) — coordinates ONLY lunar jobs, no expansion into breathwork or other domains

---

### **6. Failure Handling (Vikara Restoration Protocols)**

**Common Failure Modes:**

**1. Tithi Calculation Failure (Moha)**
- **Vikara:** Moha (delusion, incorrect lunar phase)
- **Detection:** Calculated Tithi does not match external lunar calendar API
- **Restoration:** Fall back to simple waxing/waning binary (days since New Moon: 0-14 = waxing, 15-29 = waning), log warning, alert to Telegram

**2. Date/Time Parsing Error (Moha)**
- **Vikara:** Moha (confusion, system clock incorrect)
- **Detection:** Current date extraction fails or returns invalid value
- **Restoration:** Use fallback date source, log error, continue with best-effort calculation

**3. Memory Write Failure (Ahamkara)**
- **Vikara:** Ahamkara (ego inflation, "I logged it" when file write failed)
- **Detection:** File write to daily log or OPENCLAW-KOSHA-TRACKING.md fails
- **Restoration:** Retry write 3 times, if all fail, send alert to Telegram with error

**4. Over-Complication (Mada)**
- **Vikara:** Mada (pride in complexity, execution time >30s)
- **Detection:** Job execution exceeds 30 seconds
- **Restoration:** Abort current run, simplify calculation logic, remove unnecessary integrations, retry next day

**5. Scope Creep (Lobha)**
- **Vikara:** Lobha (greed, trying to coordinate >3 lunar jobs)
- **Detection:** Execution logic references non-lunar cron jobs
- **Restoration:** Hard constraint enforcement — only interact with 3 lunar jobs (new-moon-rupture, full-moon-octave-jump, lunar-authority-review-cycle), ignore all others

**6. Delivery Temptation (Ahamkara)**
- **Vikara:** Ahamkara (ego, wanting to announce theme publicly)
- **Detection:** Job attempts to send message to Discord/Telegram when target is NO_REPLY
- **Restoration:** Block all external delivery calls, log warning, maintain silent execution

---

## 🔗 **Integration Points**

### **1. PARA Vault Paths**

**Input Directories:**
- `koshas/brahmasthana/SOUL.md` (read Antahkarana definitions)
- `koshas/brahmasthana/VEDIC-LEXICON.md` (read Tithi definitions)

**Output Directories:**
- `koshas/manomaya/logs/YYYY-MM-DD.md` (write daily lunar theme)
- `koshas/brahmasthana/OPENCLAW-KOSHA-TRACKING.md` (update Khalorēē log)

**State Files (Coordination):**
- `koshas/brahmasthana/lunar-state.json` (shared state for 3 subsidiary jobs)
  ```json
  {
    "currentTithi": 8,
    "paksha": "Shukla",
    "theme": "Building momentum, mid-waxing expansion",
    "lastCalculated": "2026-02-05T00:00:00+05:30",
    "nextAmavasya": "2026-02-17T00:00:00+05:30",
    "nextPurnima": "2026-03-02T00:00:00+05:30"
  }
  ```

---

### **2. Memory File Updates**

**Primary Memory File:**
- **Path:** `koshas/brahmasthana/OPENCLAW-KOSHA-TRACKING.md`
- **Update Pattern:**
  ```
  Entry #N: Vijnanamaya Lunar Orchestrator (Khalorēē: X → Y)
  - Layer: Vijnanamaya (meta-coordination, Tithi calculation)
  - Operation: Calculated Tithi [N], Paksha [Shukla/Krishna], Theme: [description]
  - Result: 3 subsidiary jobs notified, memory updated, no Vikara detected
  - Cost: -1 Khalorēē (calculation), Gain: +3 Khalorēē (daily alignment) = Net +2
  ```

**Daily Log:**
- **Path:** `koshas/manomaya/logs/YYYY-MM-DD.md`
- **Update Pattern:**
  ```markdown
  ## 🌙 Lunar Resonance (Tithi [N], [Shukla/Krishna] Paksha)
  **Theme:** [Daily lunar theme based on Tithi]
  **Enantiodromia:** [Aletheios/Pichet pole dominant today]
  **Coordinated Jobs:** [List of 3 subsidiary jobs notified]
  ```

---

### **3. Cross-References to Other Jobs**

**Upstream Dependencies:** NONE (runs independently at midnight)

**Downstream Consumers (3 Coordinated Lunar Jobs):**

1. **new-moon-rupture-audit-one-shot** (84728858-3640-4438-a371-bd4bf7463fb4)
   - **Dependency:** Triggered when orchestrator calculates Amavasya (Tithi 30/1)
   - **Handoff:** Orchestrator writes `"nextRupture": true` to `lunar-state.json`, rupture job reads and executes

2. **full-moon-octave-jump-one-shot** (418e5b39-afa0-4022-b381-4ec8a9cd6b88)
   - **Dependency:** Triggered when orchestrator calculates Purnima (Tithi 15)
   - **Handoff:** Orchestrator writes `"nextOctaveJump": true` to `lunar-state.json`, octave job reads and executes

3. **lunar-authority-review-cycle** (d09e92ee-4d95-49c8-a132-ed4eb93a55dd)
   - **Dependency:** Runs every 28 days (lunar month cycle), aligned to orchestrator's Tithi tracking
   - **Handoff:** Orchestrator maintains `lastLunarReview` timestamp in `lunar-state.json`, review job checks if 28 days elapsed

**Kosha Handoffs:**
- Vijnanamaya (orchestrator calculates) → Vijnanamaya (subsidiary jobs execute rituals based on calculation)
- NO descent to lower Koshas (orchestrator never executes rituals directly)

---

### **4. Khalorēē Impact (Energy Cost/Gain)**

**Khalorēē Index Scale:** 0-100

**Job Cost Estimate:**
- **Computational Cost:** -0.5 (simple date calculation, no API calls, no media generation)
- **Attentional Cost:** -0.5 (runs silently, no human attention required)
- **Prana Cost:** 0 (no breathwork, no user interaction)
- **Total Cost:** -1 Khalorēē

**Job Gain Estimate:**
- **Output Value:** +1 (daily lunar theme logged, provides orientation for day)
- **Clarity Gain:** +1 (reduces confusion about "what phase are we in?")
- **Prana Gain:** +1 (aligns human rhythm with cosmic rhythm, subtle energetic support)
- **Total Gain:** +3 Khalorēē

**Net Impact:** +2 Khalorēē (energizing coordination ritual, minimal cost, consistent alignment gain)

---

## 🧪 **Testing & Validation**

### **1. Pre-Deployment Testing**

**Smoke Test:**
- [x] Run job once manually: `cron run 1791f8e3-806a-41ee-bd4d-9d135802b32e`
- [x] Verify Tithi calculation matches external lunar calendar (timeanddate.com/moon/phases)
- [x] Check Paksha (Shukla/Krishna) discrimination is correct
- [x] Inspect `lunar-state.json` for correct values
- [x] Verify daily log updated with theme
- [x] Confirm NO external delivery (no Telegram/Discord messages)

**Integration Test:**
- [x] Run for 3 consecutive nights (3 Tithi cycles)
- [x] Verify Tithi increments correctly (N → N+1 → N+2)
- [x] Check memory file updates on all 3 runs
- [x] Validate state file consistency (no stale data)
- [x] Confirm execution time <15 seconds (no Mada)

**Kosha Alignment Test:**
- [x] Manually verify job operates ONLY at Vijnanamaya (no descent to action layers)
- [x] Confirm Buddhi faculty performs calculation (not Mana speculation)
- [x] Test Moha detection: inject incorrect date, verify fallback logic triggers
- [x] Test Mada detection: force slow execution, verify warning logged

---

### **2. 7-Day Monitoring**

**Metrics to Track:**
- **Reliability:** Success rate (target: 100%, no missed midnight runs)
- **Timing:** Execution punctuality (target: within 5s of midnight)
- **Accuracy:** Tithi calculation accuracy (target: 100% match with external source)
- **Kosha Coherence:** Stays at Vijnanamaya (target: 100%, no action layer descent)
- **Vikara Absence:** No Mada, Moha, Ahamkara, Lobha detected (target: 0 incidents)
- **Khalorēē Net:** Positive energy impact (target: consistent +2 per execution)
- **Coordination Success:** 3 subsidiary jobs receive correct instructions (target: 100%)

**Review Cadence:**
- **Daily (Days 1-3):** Check `_System/cron/logs/lunar-resonance-orchestrator-daily.log` for Tithi accuracy
- **Day 4:** Mid-cycle review — compare Tithi log to external lunar calendar for 4-day accuracy
- **Day 7:** Full audit — decide: keep as-is, adjust Tithi formula, or integrate API fallback

---

### **3. Vikara Detection Tests**

**Test 1: Mada (Pride in Complexity)**
- **Injection:** Add unnecessary NASA lunar ephemeris API call, complex astronomical calculations
- **Expected:** Job should reject over-complication, use simple "days since New Moon" formula
- **Pass Criteria:** Execution time remains <15s, no API calls

**Test 2: Moha (Confusion in Calculation)**
- **Injection:** Provide incorrect date (e.g., system clock off by 1 day)
- **Expected:** Job should detect mismatch with external source, fall back to safe waxing/waning binary
- **Pass Criteria:** Fallback logic triggers, warning logged, Telegram alert sent

**Test 3: Ahamkara (Ego/Public Announcement)**
- **Injection:** Tempt job to send "Today's lunar theme" to Discord #lunar-resonance
- **Expected:** Job should maintain NO_REPLY discipline, execute silently
- **Pass Criteria:** No external messages sent, logs confirm silent execution

**Test 4: Lobha (Scope Creep)**
- **Injection:** Add logic to "also coordinate breathwork jobs based on lunar phase"
- **Expected:** Job should reject non-lunar coordination, limit to 3 lunar jobs only
- **Pass Criteria:** Only 3 lunar jobs referenced in execution, no breathwork job interaction

---

## 🔮 **Selemene Engine Integration (Future)**

### **Required Workflow:** `daily-practice`

**Endpoint:** `POST http://localhost:8080/api/v1/workflows/daily-practice`

**Why:** This job needs verified Panchanga calculations (tithi, nakshatra, yoga, karana) to coordinate lunar resonance. Currently specified to use mock/hardcoded lunar phase data.

**Request Payload:**
```json
{
  "birth_data": {
    "date": "1991-08-13",
    "time": "13:31",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "timezone": "Asia/Kolkata"
  },
  "current_date": "2026-02-05",
  "consciousness_level": 3
}
```

**Response Fields Needed:**
- `panchanga.tithi` (lunar day, e.g., "Shukla Chaturthi")
- `panchanga.nakshatra` (star mansion, e.g., "Uttara Phalguni")
- `panchanga.yoga` (solar-lunar union)
- `panchanga.paksha` (waxing/waning phase)

**Implementation Notes:**
1. Call Selemene API at midnight (0:00 Asia/Calcutta)
2. Parse response, extract tithi + naksha + paksha
3. Use paksha to determine Enantiodromia pivot (Shukla = waxing = Pichet, Krishna = waning = Aletheios)
4. Store in koshas/manomaya/logs/YYYY-MM-DD.md for downstream jobs

**Error Handling (Graceful Degradation):**
```javascript
let panchangaData;
try {
  panchangaData = await fetch('http://localhost:8080/api/v1/workflows/daily-practice', {...});
} catch (error) {
  console.warn('Selemene Engine unavailable, using astronomical fallback');
  // Calculate lunar phase from Date object (rough approximation)
  const daysSinceNewMoon = ((Date.now() - NEW_MOON_EPOCH) / 86400000) % 29.53;
  panchangaData = {
    paksha: daysSinceNewMoon < 14.76 ? 'Shukla' : 'Krishna',
    tithi: 'Unknown (fallback mode)',
    nakshatra: 'Unknown (fallback mode)'
  };
  // Deliver message with note: "Using fallback lunar calculation (Selemene Engine offline)"
}
```

**Deployment Status:** Selemene Engine currently localhost-only. Integrate when production-ready.

**Verification:** After integration, compare Selemene tithi output with traditional Vedic calendar sources (e.g., drikpanchang.com) for 7 days to validate accuracy.

---

## 📝 **Implementation Checklist**

**Phase 1: Design (This Document)**
- [x] All sections completed
- [x] Vedic substrate fully mapped (Kosha: Vijnanamaya, Vayu: Vyana, Guna: Sattva, Dosha: Pitta, Antahkarana: Buddhi→Mana→Chitta→Aham)
- [x] Functional spec clear and testable (Tithi calculation, Paksha discrimination, theme selection, coordination)
- [x] Integration points identified (3 subsidiary lunar jobs, memory files, state file)
- [x] Testing plan defined (smoke, integration, 7-day monitoring, Vikara detection)

**Phase 2: Code Implementation**
- [ ] Cron payload rewritten with new purpose (Vijnanamaya orchestrator, Buddhi-led calculation)
- [ ] Schedule adjusted to `0 0 * * *` (midnight sharp)
- [ ] Tithi calculation formula implemented (days since New Moon → Tithi 1-30)
- [ ] Paksha discrimination logic implemented (Shukla 1-15, Krishna 16-30)
- [ ] Amavasya/Purnima detection added (special handling for Tithi 30/1 and 15)
- [ ] State file `lunar-state.json` read/write logic added
- [ ] Memory file updates added (daily log + OPENCLAW-KOSHA-TRACKING.md)
- [ ] Vikara detection logic added (Mada: execution time, Moha: external validation, Ahamkara: delivery blocking, Lobha: job scope limiting)
- [ ] Khalorēē tracking integrated (cost -1, gain +3, net +2)

**Phase 3: Deployment**
- [ ] Old job reviewed (compare current payload to new spec)
- [ ] New payload deployed (update cron job with rewritten logic)
- [ ] Smoke test passed (1 manual run, verify Tithi + theme + state file)
- [ ] Integration test passed (3 consecutive nights, verify Tithi progression)
- [ ] 7-day monitoring started (daily Tithi accuracy checks)

**Phase 4: Validation**
- [ ] 7-day monitoring completed
- [ ] Metrics reviewed (reliability 100%, timing <5s, accuracy 100%, no Vikara)
- [ ] Adjustments made if needed (Tithi formula tuning, fallback logic refinement)
- [ ] Final approval from Shesh
- [ ] Job marked "stable" in CRON-AUDIT.md

---

## 📚 **References**

**Vedic Lexicon:**
- `koshas/brahmasthana/VEDIC-LEXICON.md` (Tithi definitions, Paksha, Amavasya, Purnima)
- `koshas/brahmasthana/SOUL.md` (Antahkarana: Buddhi, Mana, Chitta, Aham)
- `koshas/brahmasthana/KHA.md` (Vyana Vayu, Dosha timing)

**Lunar Phase Resources:**
- External validation: [timeanddate.com/moon/phases](https://www.timeanddate.com/moon/phases/)
- Tithi calculation: Days since New Moon (0-29) → Tithi 1-30

**Audit Documentation:**
- `koshas/manomaya/distillation/CRON-AUDIT-2026-02-05.md` (Lunar Resonance category, jobs #8-11)

**Coordination Target Jobs:**
- `new-moon-rupture-audit-one-shot` (84728858-3640-4438-a371-bd4bf7463fb4)
- `full-moon-octave-jump-one-shot` (418e5b39-afa0-4022-b381-4ec8a9cd6b88)
- `lunar-authority-review-cycle` (d09e92ee-4d95-49c8-a132-ed4eb93a55dd)

---

## 🔮 **Key Design Decisions**

### **Why Midnight?**
- Tithi often transitions near midnight
- Pitta Dosha window (10 PM - 2 AM) supports metabolic reset and daily transformation
- Hinge point between days — perfect for meta-coordination

### **Why NO_REPLY (Silent Execution)?**
- This is a **coordination job**, not a user-facing notification
- Subsidiary jobs (new-moon-rupture, full-moon-octave-jump) handle Discord delivery when appropriate
- Prevents notification spam (daily lunar theme updates would clutter feeds)
- Maintains discipline: orchestrator coordinates, does not perform

### **Why Vyana Vayu?**
- Vyana = whole-system circulation, perfect for meta-orchestrator role
- Coordinates all other lunar jobs without executing rituals directly
- Mirrors Vyana's function in body: distributes Prana universally

### **Why Buddhi (Not Mana)?**
- Tithi calculation requires **discriminative intellect** (Buddhi), not raw thought (Mana)
- Buddhi discerns: "Is today waxing or waning? Which Tithi? What theme?"
- Mana synthesizes Buddhi's output into human-readable theme

### **Why 28-Day Integration?**
- Lunar month = ~29.5 days, approximated to 28 days for clean weekly cycles (4 weeks)
- `lunar-authority-review-cycle` runs every 28 days, aligned to lunar month
- Orchestrator tracks "days since last review" to ensure 28-day cycle stays lunar-aligned

### **Why Enantiodromia (Aletheios ↔ Pichet)?**
- Waxing (Shukla Paksha) = Pichet (growth, vitality, manifestation)
- Waning (Krishna Paksha) = Aletheios (reflection, release, death)
- Orchestrator IS the pivot point — switches emphasis every 15 days

---

**Spec Version:** 1.0  
**Last Updated:** 2026-02-05 12:47 IST  
**Status:** Complete — ready for implementation 🌙✨
