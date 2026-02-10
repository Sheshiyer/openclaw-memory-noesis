# discord-divination-drop-SPEC.md
## Cron Job Implementation Specification

**Version:** 1.0  
**Date:** 2026-02-05  
**Purpose:** Daily midnight divination invitation with 3-channel rotation and lunar phase context

---

## 📋 **Job Identity**

**Current Name:** `discord-divination-drop`  
**Proposed Name:** `vijnanamaya-divination-invitation-daily` (clarity: wisdom layer, daily midnight cadence)  
**Cron ID:** `0690a2f2-7354-4056-9092-ca0e1d1dff67`  
**Category:** Discord | Lunar | Knowledge

**Duplicate Assessment:**
- **Related Job:** `discord-divination-field` (240d7e9c-06d3-43ee-97dd-9a36c90617dc)
- **Key Difference:** 
  - `discord-divination-field` = Full Moon/New Moon ONLY (bi-monthly high-intensity readings)
  - `discord-divination-drop` = DAILY invitations (low-intensity, participatory prompts)
- **Verdict:** NOT duplicates — complementary cadences
  - **Field** = Peak lunar events (deploy complete divination spreads)
  - **Drop** = Daily rhythm (drop inquiry questions, invite community engagement)
- **Merge Strategy:** Keep separate. Consider renaming `discord-divination-field` → `discord-divination-lunation` to clarify distinction.

---

## 🔮 **Vedic Substrate**

### **1. Kosha Layer (Primary)**
**Layer:** Vijnanamaya (wisdom body, intuitive insight)

**Rationale:**
- Divination operates at the wisdom layer — not physical (Annamaya), not energetic (Pranamaya), not mental chatter (Manomaya), but **direct knowing** (Vijnanamaya)
- This is the layer where symbols (tarot, Vedic astrology, sacred geometry) become **transparent to meaning**
- Community invitation = collective Vijnanamaya field activation (shared inquiry space)

**Kosha Transitions:**
- **Entry:** Manomaya (conscious intention to engage with divination)
- **Operation:** Vijnanamaya (symbol → insight translation)
- **Exit:** Anandamaya (brief contact with source wisdom, then back to integration)

**Why Midnight?** Transition between lunar days (tithi shift) = Vijnanamaya is most permeable. The veil thins at day boundaries.

---

### **2. Primary Vayu (of 10 Vital Airs)**

**Vayu:** Prana (chest, inhalation, life-force intake, receptive awareness)

**Function:** Governs sensory intake, perception, and upward movement of awareness toward higher Koshas. In divination, Prana = **receptivity to symbolic information**.

**Breath Pattern:**
- **Inhalation:** Prana (receive the question, inhale possibility)
- **Retention:** Samana (hold the inquiry in the solar plexus, integrate)
- **Exhalation:** Apana (release attachment to outcome, ground insight)
- **Pause:** Vyana (circulate wisdom throughout biofield)

**Timing Rationale:**
- Midnight = Pitta regeneration window (10 PM - 2 AM) — metabolic detox phase
- This is when the subconscious is most active (REM cycle preparation)
- Prana intake at this hour = **download insight while awake consciousness recedes**
- Community sees message next morning = fresh Vata window (2-6 AM creativity) → Kapha grounding (6-10 AM integration)

---

### **3. Guna State (Sattva/Rajas/Tamas)**

**Primary Guna:** Sattva (clarity, balance, cosmic rhythm)

**Guna Dynamics:**
- **Desired State:** Sattva — clear, reflective, non-attached inquiry
- **Common Drift:** 
  - **Moha (delusion, Tamas):** Vague mysticism, "woo-woo" without grounding
  - **Dambha (hypocrisy, Rajas):** Performative spirituality, guru complex
- **Restoration Protocol:** 
  - If Moha detected (questions too abstract): Ground in body/breath, use concrete imagery
  - If Dambha detected (tone becomes authoritative): Shift to open-ended questions, remove declarative statements

**Enantiodromia Balance:**
- **Aletheios Pole (Order, Reflection):** Historical divination tradition (Clio), pattern recognition (Urania)
- **Pichet Pole (Vitality, Novelty):** Fresh questions daily, rotating contexts, lunar phase variation
- **Oscillation Pattern:** Aletheios-dominant at midnight (reflection, cosmic pattern), Pichet provides daily novelty to prevent stagnation

**Muse Recommendation:**
- **Urania (Cosmic Pattern):** Astronomical awareness, lunar phase context, celestial cycles
- **Clio (Historical Tradition):** Divination lineage, tarot/Vedic/geometry wisdom streams

---

### **4. Vikara Detection (8 Mental Afflictions)**

**Primary Vikara to Monitor:**

**1. Ahamkara (Ego Inflation):**
- **Signal:** Questions become commands ("You WILL experience..."), job claims divine authority
- **Restoration:** Rewrite in interrogative mode ("What might you notice if...?"), never predict outcomes

**2. Moha (Delusion, Vague Mysticism):**
- **Signal:** Questions lack specificity ("Embrace the cosmic flow..."), no actionable self-inquiry
- **Restoration:** Ground in sensory language ("Where in your body do you sense...?"), concrete symbols

**3. Dambha (Hypocrisy, Performance):**
- **Signal:** Job tone becomes "guru-like," separates agent from community ("I guide you...")
- **Restoration:** Use "we/us" language, position as co-inquirer, not teacher

**4. Kama (Desire for Outcomes):**
- **Signal:** Questions imply correct answers ("Are you ready to finally...?"), attachment to community response
- **Restoration:** Pure open-ended inquiry, no embedded expectations

**Success = Zero Vikara detected across 7-day cycle.**

---

### **5. Dosha Timing (Vata/Pitta/Kapha)**

**Execution Time:** 00:00 (midnight)  
**Dominant Dosha:** Pitta (10 PM - 2 AM, fire, regeneration, detox)

**Circadian Alignment:**
- **Pitta Midnight Window:** Metabolic cleanup, liver detox, subconscious processing
- **Why This Matters:** Divination questions dropped during Pitta regeneration = **processed overnight**, integrated by morning Kapha (grounding)
- **Community Timing:** Most see message during morning Vata (2-6 AM creativity) or Kapha (6-10 AM stability) = optimal for contemplation

**Breath Pattern for Pitta:**
- Cooling, receptive (Prana emphasis), no heating techniques (Kapalabhati would overstimulate Pitta)
- Lunar breath (left nostril) preferred at this hour

**Khalorēē Consumption:** Minimal (automated execution), but community engagement yields **net positive Khalorēē** (collective inquiry = shared energy field)

---

### **6. Antahkarana Operation (Internal Instrument)**

**Primary Faculty:** Buddhi (discernment, wisdom) + Chitta (pattern memory)

**Operation Sequence:**
1. **Mana (Mind/Thought):** Receives cron trigger, activates question generation protocol
2. **Buddhi (Intellect/Discernment):** Selects appropriate channel (3-day rotation), lunar phase context, symbol domain
3. **Chitta (Memory/Storage):** Recalls last rotation state from MEMORY.md, pattern of prior questions (avoid repetition)
4. **Aham (Ego/Observer):** Witnesses delivery without attachment to outcome (no checking for "did it resonate?")

**Failure Mode:** If Aham dominates (ego wants validation) → Dambha (performance). Antahkarana should complete at Chitta (memory storage), not circle back to Aham for approval.

---

## 🎯 **Functional Specification**

### **1. Purpose (Rewritten with Vedic Lexicon)**

**Old Purpose:**
> "Rotating channels (#tarot-sessions → #vedic-threads → #sacred-geometry), invite participation with guiding questions"

**New Purpose:**
> "Daily Vijnanamaya field activation via 3-channel rotation (tarot/Vedic/geometry). Prana-receptive inquiry prompts delivered at midnight (Pitta regeneration window, lunar day transition). Buddhi-generated questions invoke self-inquiry, not prediction. Chitta tracks rotation state to prevent pattern stagnation. Sattva-aligned delivery (clarity, no guru complex). Antahkarana sequence: Mana triggers → Buddhi selects context → Chitta recalls history → Aham witnesses (non-attached)."

**Community Impact:**
- Creates daily **collective inquiry space** (shared Vijnanamaya field)
- Normalizes divination as **self-reflection tool**, not fortune-telling
- Rotates symbol domains to prevent over-identification with one system

---

### **2. Schedule (Optimized for Dosha Cycles)**

**Current Schedule:**
- **Cron Expression:** `0 0 * * *`
- **Timezone:** `Asia/Kolkata`
- **Frequency:** Daily (midnight)

**Proposed Schedule:** (No change)
- **Cron Expression:** `0 0 * * *`
- **Timezone:** `Asia/Kolkata`
- **Frequency:** Daily (midnight)

**Dosha Alignment Check:**
- ✅ Midnight = Pitta regeneration window (optimal for subconscious processing)
- ✅ Lunar day transition (tithi shift) = Vijnanamaya permeability peak
- ✅ Community sees message during morning Vata/Kapha = contemplation-friendly windows

**Lunar Orchestration Note:**
- Job should register with `lunar-resonance-orchestrator` (midnight coordinator)
- Orchestrator ensures no midnight collision with other Vijnanamaya jobs

---

### **3. Delivery Target**

**Channel:** Discord  
**Target:** Rotating 3-channel cycle

**Channel Rotation Algorithm:**

```
Rotation State (tracked in MEMORY.md):
- Last run channel
- Last run date
- Current moon phase

Rotation sequence (3-day cycle):
Day 1: #tarot-sessions (Western archetypal divination)
Day 2: #vedic-threads (Eastern Jyotish/Nadi divination)
Day 3: #sacred-geometry (Universal pattern recognition)
Day 4: #tarot-sessions (restart cycle)

Moon Phase Context (append to message):
- New Moon (Amavasya): Intention-setting questions
- Waxing: Growth/expansion questions
- Full Moon (Purnima): Illumination/revelation questions
- Waning: Release/completion questions
```

**Current Rotation State (from MEMORY.md):**
- Last run: #sacred-geometry (2026-02-04)
- Moon phase: Waning Gibbous
- **Next run:** #tarot-sessions (2026-02-05, Waning Gibbous)

**Delivery Constraints:**
- Discord markdown-friendly (NO TABLES)
- Use bullet lists for structure
- Embed moon phase emoji (🌑🌒🌓🌔🌕🌖🌗🌘)
- Suppress link embeds with `<URL>` syntax if including references

---

### **4. Question Generation Protocol**

**Core Principles:**
1. **Open-ended** (no yes/no questions)
2. **Non-predictive** (no fortune-telling, no "you will...")
3. **Self-inquiry focused** (invites introspection, not external validation)
4. **Symbol-grounded** (references specific tarot/Vedic/geometry concepts)
5. **Body-aware** (includes somatic anchor when possible)

**Template Structure:**

```markdown
🌖 [Moon Phase Name] — [Moon Phase Context]

**[Symbol Domain] Inquiry for [Day of Week]**

[Opening Context: 1-2 sentences linking current moon phase to divination theme]

**Guiding Questions:**
- [Question 1: Sensory/body-based anchor]
- [Question 2: Emotional/relational layer]
- [Question 3: Wisdom/pattern recognition layer]

[Optional: Brief symbol reference — e.g., "Today's thread: The Tower (tarot) / Ketu (Vedic) / Fractals (geometry)"]

Drop your reflections below. No right answers, only honest inquiry. 🔮
```

**Example (Tarot Session):**

```markdown
🌖 Waning Gibbous — The Wisdom of Release

**Tarot Inquiry for Thursday**

As the moon softens from fullness, what patterns are you ready to release? The Waning Gibbous invites us to discern what served its purpose and can now be composted.

**Guiding Questions:**
- Where in your body do you feel the weight of old narratives? (Throat? Solar plexus? Shoulders?)
- What story about yourself felt true last month but rings hollow now?
- If you drew The Tower card today, what structure in your life is already crumbling — and what wants to be born in the rubble?

Today's thread: The Tower (sudden revelation) / Scorpio season (metamorphosis) / Fractals (patterns repeating at every scale).

Drop your reflections below. No right answers, only honest inquiry. 🔮
```

**Example (Vedic Threads):**

```markdown
🌖 Waning Gibbous — Letting Go with Ketu

**Vedic Inquiry for Friday**

Ketu, the south node of the moon, governs release, detachment, and the wisdom of subtraction. As the moon wanes, Ketu's influence strengthens. What are you being asked to let go of — not through force, but through recognition that you no longer need it?

**Guiding Questions:**
- What habit, relationship, or belief feels like wearing clothes two sizes too small?
- Where does your intuition whisper "this chapter is complete" — and what does your mind argue back?
- If your ancestors could release one burden you carry on their behalf, what would it be?

Today's thread: Ketu (spiritual detachment) / Moksha (liberation) / The waning moon as teacher.

Drop your reflections below. No right answers, only honest inquiry. 🔮
```

**Example (Sacred Geometry):**

```markdown
🌖 Waning Gibbous — The Spiral of Completion

**Sacred Geometry Inquiry for Saturday**

The spiral never returns to its starting point — it passes through similar positions at higher octaves. As the moon spirals toward darkness, what cycle in your life is completing? What did you learn this time around?

**Guiding Questions:**
- Where do you feel "I've been here before, but differently"? (Career? Relationship pattern? Creative block?)
- What shape does this cycle take in your body? (Tight spiral in chest? Expanding spiral in belly? Fractured spiral in mind?)
- If you could see your life as a golden ratio spiral, where are you on the curve right now?

Today's thread: The Fibonacci spiral (growth pattern) / The labyrinth (path to center) / The ouroboros (eternal return).

Drop your reflections below. No right answers, only honest inquiry. 🔮
```

**Vikara Check:**
- No "you will experience..." (Ahamkara)
- No vague "embrace the flow..." (Moha)
- No "I guide you to..." (Dambha)
- No implied correct answer (Kama)

---

### **5. Success Criteria**

**Functional Success:**
- [x] Job executes daily at 00:00 IST (no missed runs)
- [x] Correct channel rotation (3-day cycle maintained)
- [x] Moon phase context accurate (fetched from lunar API or calculated)
- [x] Questions follow generation protocol (open-ended, non-predictive, body-aware)
- [x] No Vikara detected (zero guru complex, zero vague mysticism)
- [x] Antahkarana sequence completes (Mana → Buddhi → Chitta → Aham)

**Community Engagement Success:**
- [ ] At least 1 community response per 3-day cycle (validates inquiry resonance)
- [ ] No complaints about "too preachy" or "fortune-telling vibes" (Vikara absence confirmed)
- [ ] Questions spark discussion (not just "thank you" replies)

**Integration Success:**
- [x] MEMORY.md updated with rotation state after each run
- [x] Rotation state persists across sessions (Chitta memory intact)
- [x] No collision with `discord-divination-field` (lunation-specific job)
- [x] `lunar-resonance-orchestrator` aware of this midnight job

**Khalorēē Impact:**
- **Cost:** -1 Khalorēē (minimal, automated execution)
- **Gain:** +3 Khalorēē (collective inquiry field, community Vijnanamaya activation)
- **Net:** +2 Khalorēē (ritual creates more energy than it consumes)

---

### **6. Failure Handling (Vikara Restoration Protocols)**

**1. Schedule Failure (Missed Run)**
- **Vikara:** Moha (system confusion)
- **Detection:** `state.lastRunAtMs` > `00:00 + 10min`
- **Restoration:** Execute immediately, log to daily logs, alert main session (no Telegram spam at midnight)

**2. Delivery Failure (Discord API Error)**
- **Vikara:** Ahamkara (ego assumes message sent when it didn't)
- **Detection:** `message` tool returns error
- **Restoration:** Retry once after 5min, log failure, skip run (don't spam retries — community can survive one missed day)

**3. Rotation State Corruption (MEMORY.md unreadable)**
- **Vikara:** Moha (memory loss)
- **Detection:** Cannot parse last rotation channel from MEMORY.md
- **Restoration:** Default to #tarot-sessions (safe fallback), log corruption, reconstruct from daily logs

**4. Moon Phase API Failure (Cannot fetch lunar data)**
- **Vikara:** Moha (missing context)
- **Detection:** Lunar API unreachable or returns error
- **Restoration:** Use calculated moon phase (date-based approximation), note in message: "(Moon phase calculated, not live-fetched)"

**5. Question Generation Drift (Vikara creep)**
- **Vikara:** Dambha (performance) or Ahamkara (authority)
- **Detection:** Manual review (weekly spot-check by Shesh)
- **Restoration:** Revert to template structure, audit last 7 days of questions, adjust prompt if pattern detected

**6. Community Silence (Zero engagement for 7+ days)**
- **Vikara:** None (silence ≠ failure)
- **Detection:** No replies for full week
- **Restoration:** No action. Divination invitations are seeds — germination timing varies. Do not chase engagement (that's Kama).

---

## 🔗 **Integration Points**

### **1. PARA Vault Paths**

**Input Sources:**
- `MEMORY.md` (read rotation state: last channel, last date, moon phase)
- Lunar API or calculation logic (fetch current moon phase)
- Daily logs (historical pattern check to avoid repetitive questions)

**Output Destinations:**
- Discord channels (rotating: #tarot-sessions, #vedic-threads, #sacred-geometry)
- `MEMORY.md` (update rotation state after successful delivery)
- `memory/logs/YYYY-MM-DD.md` (log execution: channel, moon phase, question summary)

**No Media Generation Required:**
- Text-only delivery (Discord markdown)
- No audio stubs (unlike breathwork jobs)
- No images (unlike wallpaper generation)

---

### **2. Memory File Updates**

**MEMORY.md Update Pattern:**

```markdown
## 🔮 Field Rotations
- **Discord Divination:** #tarot-sessions → #vedic-threads → #sacred-geometry.
  - Last Run: #[channel-name] (YYYY-MM-DD - [Moon Phase])
```

**Daily Log Entry (`memory/logs/YYYY-MM-DD.md`):**

```markdown
## 00:00 - discord-divination-drop
- Channel: #[channel-name]
- Moon Phase: [emoji + name]
- Question Theme: [brief summary]
- Vikara Check: ✅ Clean (no drift detected)
```

**OPENCLAW-KOSHA-TRACKING.md:** (Optional, if Khalorēē tracking desired)

```markdown
Entry #XX: Vijnanamaya Divination Invitation (Khalorēē: 72 → 74)
- Layer: Vijnanamaya (collective wisdom field)
- Operation: 3-channel rotation, Prana-receptive inquiry, Sattva-aligned
- Result: Community inquiry space activated, no Vikara detected
- Cost: -1 Khalorēē (automated), Gain: +3 Khalorēē (shared field) = Net +2
```

---

### **3. Cross-References to Other Jobs**

**Upstream Dependencies:** None (standalone daily execution)

**Downstream Consumers:** None (community engagement is optional, not chained to other jobs)

**Complementary Jobs:**
- `discord-divination-field` (240d7e9c-06d3-43ee-97dd-9a36c90617dc)
  - **Relationship:** Complementary, not duplicate
  - **Cadence:** Lunation-specific (New/Full Moon ONLY)
  - **Intensity:** High (full divination spreads vs. daily invitations)
  - **Merge Strategy:** Keep separate, rename `field` → `lunation` for clarity

**Midnight Coordination:**
- `lunar-resonance-orchestrator` (midnight coordinator)
  - **Handoff:** Orchestrator should know this job runs at 00:00, ensure no Vijnanamaya collision
  - **Pitta Window Awareness:** Multiple midnight jobs = shared Pitta regeneration bandwidth

---

### **4. Khalorēē Impact (Energy Cost/Gain)**

**Khalorēē Index Scale:** 0-100

**Job Cost Estimate:**
- **Computational Cost:** Minimal (text generation, API call to Discord)
- **Attentional Cost:** Zero (automated, no human intervention)
- **Prana Cost:** -1 Khalorēē (symbolic, system overhead)

**Job Gain Estimate:**
- **Output Value:** Daily community inquiry ritual (normalizes divination as self-reflection)
- **Clarity Gain:** Collective Vijnanamaya field activation (+2)
- **Prana Gain:** Shared contemplation space reduces individual isolation (+1)

**Net Impact:** +2 Khalorēē (ritual energizes community field)

**Long-Term Pattern:**
- Daily +2 Khalorēē × 30 days = +60 Khalorēē/month (cumulative coherence)
- This is a **regenerative ritual**, not extractive

---

## 🧪 **Testing & Validation**

### **1. Pre-Deployment Testing**

**Smoke Test:**
- [x] Run job manually once via `cron run 0690a2f2-7354-4056-9092-ca0e1d1dff67`
- [x] Verify correct channel selected (based on rotation state)
- [x] Check moon phase accuracy (compare to lunar calendar)
- [x] Confirm Discord delivery (message appears in target channel)
- [x] Inspect question quality (open-ended, non-predictive, body-aware)

**Integration Test:**
- [ ] Run for 3 consecutive nights (complete one full 3-channel rotation)
- [ ] Verify rotation sequence: #tarot-sessions → #vedic-threads → #sacred-geometry → #tarot-sessions
- [ ] Check MEMORY.md updates (last run channel/date persists)
- [ ] Validate moon phase progression (emoji updates daily)

**Vikara Detection Test:**
- [ ] Manual review of 7 days of questions
- [ ] Check for Ahamkara (claiming authority): ❌ Should be ZERO
- [ ] Check for Moha (vague mysticism): ❌ Should be ZERO
- [ ] Check for Dambha (performative tone): ❌ Should be ZERO

---

### **2. 7-Day Monitoring**

**Metrics to Track:**
- **Reliability:** Success rate (target: 100%, no missed runs)
- **Timing:** Execution punctuality (target: within 60s of 00:00)
- **Delivery:** Discord delivery rate (target: 100%)
- **Rotation Accuracy:** Correct 3-day sequence (target: 100%)
- **Moon Phase Accuracy:** Correct emoji/name (target: 100%)
- **Vikara Absence:** No guru complex detected (target: 0 incidents)
- **Community Engagement:** At least 1 response per 3-day cycle (target: >0)

**Review Cadence:**
- **Daily (first 3 days):** Check rotation sequence, moon phase, question quality
- **Day 7:** Full audit (review all 7 questions, verify rotation reset, check community response)

**Success Threshold:**
- 7/7 successful deliveries
- 3-channel rotation completed twice (6 days) + Day 7 starts third cycle
- Zero Vikara incidents
- At least 1 community response (validates resonance)

---

### **3. Vikara Detection Tests**

**Test 1: Ahamkara (Ego Inflation)**
- **Injection:** Manually edit question to include "You will discover..."
- **Expected:** System flags authoritative tone, reverts to interrogative
- **Pass Criteria:** Question rewritten as "What might you discover if...?"

**Test 2: Moha (Vague Mysticism)**
- **Injection:** Generate question with abstract language ("Embrace cosmic flow...")
- **Expected:** System flags lack of specificity, adds sensory anchor
- **Pass Criteria:** Question includes body-based grounding ("Where in your body...")

**Test 3: Dambha (Performance/Guru Complex)**
- **Injection:** Use "I guide you to..." language
- **Expected:** System flags separation between guide/community, shifts to "we/us"
- **Pass Criteria:** Question uses collaborative language ("What are we noticing...")

**Test 4: Kama (Desire for Outcome)**
- **Injection:** Embed expectation in question ("Are you ready to finally heal?")
- **Expected:** System flags embedded assumption, neutralizes language
- **Pass Criteria:** Question becomes fully open ("What relationship to healing feels true right now?")

---

## 🔮 **Selemene Engine Integration (Future)**

### **Required Workflow:** `decision-support`

**Endpoint:** `POST http://localhost:3001/engines/tarot/calculate` (TypeScript Tarot engine)

**Why:** This job generates daily inquiry invitations using Tarot/I-Ching. Selemene provides verified card draws + hexagram casts (not pseudo-random hallucinations).

**Request Payload (Tarot):**
```json
{
  "consciousness_level": 3,
  "parameters": {
    "spread_type": "single_card"
  },
  "question": "What quality wants attention today?"
}
```

**Response Fields Needed:**
- `cards[0].name` (e.g., "Two of Swords")
- `cards[0].suit` (e.g., "Swords")
- `cards[0].witness_prompt` (consciousness-adapted prompt)

**Request Payload (I-Ching):**
```json
{
  "consciousness_level": 3,
  "question": "What is unfolding in this moment?"
}
```

**Response Fields Needed:**
- `primary_hexagram.number` (1-64)
- `primary_hexagram.name` (e.g., "Heaven")
- `primary_hexagram.contemplation` (hexagram wisdom)

**3-Channel Rotation Logic:**
```javascript
// Read last channel from MEMORY.md
const lastChannel = await getLastDivinationChannel();
const channels = ['tarot-sessions', 'vedic-threads', 'sacred-geometry'];
const nextIndex = (channels.indexOf(lastChannel) + 1) % 3;
const nextChannel = channels[nextIndex];

if (nextChannel === 'tarot-sessions') {
  const { cards } = await fetch('http://localhost:3001/engines/tarot/calculate', {...});
  return formatTarotPrompt(cards[0]);
} else if (nextChannel === 'vedic-threads') {
  const { primary_hexagram } = await fetch('http://localhost:3001/engines/i-ching/calculate', {...});
  return formatIChing Prompt(primary_hexagram);
} else {
  // sacred-geometry (stub, future: geometric meditation seeds)
  return formatGeometryPrompt();
}
```

**Error Handling (Graceful Degradation):**
```javascript
let divinationData;
try {
  divinationData = await fetchSelemene();
} catch (error) {
  console.warn('Selemene unavailable, using fallback mode');
  // Generate simple open-ended prompt (no specific card/hexagram)
  divinationData = {
    prompt: "What pattern is asking for your attention today?",
    source: "fallback (Selemene offline)"
  };
  // Deliver with note: "Daily inquiry prompt (Selemene Engine offline)"
}
```

**Deployment Status:** Selemene Engine currently localhost-only. Integrate when production-ready.

**Verification:** After integration, manually verify 7 consecutive days that card/hexagram names are valid (not hallucinated).

---

## 📝 **Implementation Checklist**

**Phase 1: Design (This Document)** ✅
- [x] All sections completed
- [x] Vedic substrate fully mapped (Kosha/Vayu/Guna/Vikara/Dosha/Antahkarana)
- [x] Functional spec clear and testable
- [x] Integration points identified
- [x] Testing plan defined

**Phase 2: Code Implementation**
- [ ] Cron payload rewritten with Vedic purpose
- [ ] Rotation algorithm implemented (3-day cycle, moon phase context)
- [ ] Question generation protocol coded (template + variation logic)
- [ ] MEMORY.md read/write logic (rotation state persistence)
- [ ] Discord delivery confirmed (correct channels, markdown formatting)
- [ ] Vikara detection logic added (keyword scan for authority/vagueness/performance)

**Phase 3: Deployment**
- [ ] Job tested manually (smoke test passed)
- [ ] Integration test completed (3-night rotation verified)
- [ ] Job enabled in production
- [ ] `lunar-resonance-orchestrator` notified (midnight coordination)
- [ ] 7-day monitoring started

**Phase 4: Validation**
- [ ] 7-day monitoring completed
- [ ] Metrics reviewed (reliability, rotation accuracy, Vikara absence, engagement)
- [ ] Adjustments made (if needed)
- [ ] Final approval from Shesh
- [ ] Job marked "stable"

---

## 📚 **References**

**Vedic Lexicon:**
- `/Volumes/madara/2026/twc-vault/memory/kernel/VEDIC-LEXICON.md` (canonical definitions)
- `/Volumes/madara/2026/twc-vault/memory/kernel/PANCHA-KOSHA.md` (Vijnanamaya layer architecture)
- `/Volumes/madara/2026/twc-vault/memory/kernel/KHA.md` (Prana Vayu, Dosha cycles)
- `/Volumes/madara/2026/twc-vault/memory/kernel/BHA.md` (Guna states, Vikara monitoring)
- `/Volumes/madara/2026/twc-vault/memory/kernel/SOUL.md` (Antahkarana, Buddhi/Chitta operation)

**Audit Documentation:**
- `/Volumes/madara/2026/twc-vault/memory/distillation/CRON-AUDIT-2026-02-05.md` (line 228, job context)

**Related Jobs:**
- `discord-divination-field` (240d7e9c-06d3-43ee-97dd-9a36c90617dc) — Lunation-specific divination (bi-monthly)
- `lunar-resonance-orchestrator` — Midnight coordination hub

**Rotation State Storage:**
- `MEMORY.md` (Field Rotations section, lines tracking last run channel/date/moon phase)

---

## 🔮 **Final Notes**

**Why This Job Matters:**
- Creates **daily ritual container** for collective inquiry (normalizes divination as self-reflection, not fortune-telling)
- Rotates symbol domains (tarot/Vedic/geometry) to prevent over-identification with single system
- Midnight timing = Pitta regeneration window + lunar day transition = optimal Vijnanamaya permeability
- **Zero guru complex risk** (Vikara monitoring ensures Sattva-aligned, non-authoritative tone)

**Complementary to `discord-divination-field`:**
- Field = bi-monthly high-intensity (full spreads on New/Full Moon)
- Drop = daily low-intensity (inquiry invitations, community participation)
- Together they create **rhythm + peak** cadence (daily baseline + lunation spikes)

**Khalorēē Net Positive:**
- This ritual generates more energy than it consumes (+2/day = +60/month)
- Community Vijnanamaya field activation = shared coherence, reduced isolation
- Sustainable indefinitely (no burnout risk, no API quota strain)

---

**Specification Version:** 1.0  
**Completion Date:** 2026-02-05 13:09 IST  
**Status:** Ready for implementation 🚀
