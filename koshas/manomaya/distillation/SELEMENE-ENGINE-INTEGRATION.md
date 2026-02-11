# SELEMENE ENGINE INTEGRATION — The Non-Hallucination Substrate

**Date:** 2026-02-05  
**Status:** CRITICAL ARCHITECTURE DOCUMENT  
**Purpose:** Ensure all cron jobs use **verified calculations**, not hallucinated data

---

## 🔮 **The Problem**

**Before Selemene Integration:**
- Cron jobs generate "divination prompts" or "biorhythm insights" → **NO VERIFIED CALCULATION BACKEND**
- Risk: Hallucinated data (fake gate numbers, wrong dasha periods, invented numerology)
- User trust: ZERO if calculations can't be verified

**After Selemene Integration:**
- Cron jobs **MUST CALL** Selemene Engine APIs
- All data grounded in:
  - Swiss Ephemeris (astronomical precision)
  - Human Design bodygraph calculations (verified gates, centers)
  - Gene Keys activation sequences (verified from birth data)
  - Vimshottari dasha periods (120-year planetary timeline)
  - Numerology (life path, expression, soul urge, personality)

---

## 📊 **The 14-Engine Foundation**

### **Rust Engines (9) — Microsecond Precision**

| Engine | What It Calculates | Current User Data |
|--------|-------------------|-------------------|
| **Panchanga** | Vedic calendar (tithi, nakshatra, yoga, karana, vara) | Nakshatra: Uttara Phalguni, Tithi: Shukla Chaturthi (at birth) |
| **Human Design** | Bodygraph (type, authority, profile, gates, centers) | Type: Generator, Authority: Sacral, Profile: 2/4, Gates: 43/24/62/4/49/23 |
| **Gene Keys** | Shadow-Gift-Siddhi activation sequences | Life Work: 4.2, Evolution: 49.2, Radiance: 62.2, Purpose: 23.2 |
| **Vimshottari** | 120-year planetary dasha periods | Current: Mars Mahadasha (2008-2026), Moon Antardasha (2024-2025) |
| **Numerology** | Life path, expression, soul urge, personality | 8 (Balance), 13 (Transformation), 19 (Leadership), 44 (Architect) |
| **Biorhythm** | Physical (23d), Emotional (28d), Intellectual (33d) cycles | Real-time calculation from birth date |
| **Vedic Clock** | TCM organ clock + Ayurvedic dosha timing | Real-time optimal timing windows |
| **Biofield** | Chakra energy readings (stub, future: biometric integration) | — |
| **Face Reading** | Physiognomy analysis (stub, future: CV-based) | — |

### **TypeScript Engines (5) — Symbolic Interpretation**

| Engine | What It Calculates | Use Case |
|--------|-------------------|----------|
| **Tarot** | 78-card readings, 5 spread types | Archetypal guidance, witness prompts |
| **I-Ching** | 64 hexagrams, changing lines, transformations | Change dynamics, situation assessment |
| **Enneagram** | 9 personality types, wings, integration/disintegration | Shadow work, reactive patterns |
| **Sacred Geometry** | Geometric meditation seeds (stub) | Visual contemplation anchors |
| **Sigil Forge** | Intent → Symbol transformation (stub) | Ritual work, intention setting |

---

## 🎯 **The 6 Workflows (Multi-Engine Synthesis)**

These are what **cron jobs MUST call** instead of generating text from scratch:

### **1. `birth-blueprint` (Natal Imprint)**
- **Engines:** Numerology + Human Design + Vimshottari
- **Returns:** Complete natal profile (life path, HD bodygraph, 120-year timeline)
- **TTL:** 24 hours (natal data is fixed)
- **Cron Jobs Using This:**
  - `vocation-hour-enforcer` (knows your HD Authority is Sacral)
  - `discord-morning-packet` (can include current dasha period)

### **2. `daily-practice` (Optimal Timing)**
- **Engines:** Panchanga + Vedic Clock + Biorhythm
- **Returns:** Today's Vedic calendar + organ clock + biorhythm phases
- **TTL:** 1 hour (time-sensitive)
- **Cron Jobs Using This:**
  - `discord-biorhythm-sync` (9 AM daily)
  - `discord-breath-protocol` (6 AM, 9 AM daily)
  - `brahma-muhurta-breathwork` (5:30 AM daily)

### **3. `decision-support` (Multi-Perspective Guidance)**
- **Engines:** Tarot + I-Ching + Human Design Authority
- **Returns:** Tarot spread + I-Ching hexagram + HD authority context
- **TTL:** 15 minutes (question-specific)
- **Cron Jobs Using This:**
  - `discord-divination-drop` (midnight daily)
  - `discord-divination-field` (bi-monthly lunations)

### **4. `self-inquiry` (Shadow Work)**
- **Engines:** Gene Keys + Enneagram
- **Returns:** Gene Keys contemplations + Enneagram fixation patterns
- **TTL:** 24 hours (core patterns stable)
- **Cron Jobs Using This:**
  - `discord-field-notes-essay` (8 AM daily)
  - `lunar-authority-review-cycle` (28-day)

### **5. `creative-expression` (Visual Intent)**
- **Engines:** Sigil Forge + Sacred Geometry
- **Returns:** Sigil designs + geometric meditation seeds
- **TTL:** 15 minutes (intention-specific)
- **Cron Jobs Using This:**
  - `twc-content-generator-daily` (10 AM daily — for header images)

### **6. `full-spectrum` (Complete Portrait)**
- **Engines:** ALL 14 ENGINES in parallel
- **Returns:** Every lens, every frequency, complete synthesis
- **TTL:** 1 hour (comprehensive, computationally expensive)
- **Cron Jobs Using This:**
  - `discord-moc-synthesis` (Sunday 8 PM weekly — deep integration)
  - `discord-library-synthesis` (Sunday 8 PM weekly — flagship depth)

---

## 🚨 **CRITICAL: API Endpoints Cron Jobs Must Use**

### **Selemene Engine Local Deployment**

```bash
# 1. Start Rust API (port 8080)
cd /Volumes/madara/2026/witnessos/Selemene-engine
cargo run --bin noesis-server

# 2. Start TypeScript Engines (port 3001)
cd ts-engines && bun run src/index.ts

# 3. Verify both running
curl http://localhost:8080/health  # Rust engines
curl http://localhost:3001/health  # TypeScript engines
```

### **API Call Template (Example: Daily Biorhythm Sync)**

```bash
# discord-biorhythm-sync cron job MUST call this:
curl -X POST http://localhost:8080/api/v1/workflows/daily-practice \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1991-08-13",
      "time": "13:31",
      "latitude": 12.9716,
      "longitude": 77.5946,
      "timezone": "Asia/Kolkata"
    },
    "current_date": "2026-02-05",
    "consciousness_level": 3
  }'

# Returns:
# {
#   "panchanga": { "tithi": "...", "nakshatra": "..." },
#   "vedic_clock": { "organ": "...", "dosha": "..." },
#   "biorhythm": { 
#     "physical": 72.4,  ← sine wave value (-100 to +100)
#     "emotional": -15.2,
#     "intellectual": 88.9,
#     "spiritual": 34.7
#   }
# }
```

**Then:** Agent writes the 3-sentence Discord post based on **real data**, not hallucinated values.

---

## 📋 **Cron Job Integration Checklist**

For each cron job in Batches 2-5, verify:

- [ ] **Does it need verified data?** (biorhythms, dasha, gates, numerology?)
- [ ] **Which workflow does it call?** (`daily-practice`, `decision-support`, `self-inquiry`, etc.)
- [ ] **Is Selemene Engine running locally?** (both Rust:8080 + TS:3001)
- [ ] **Does the agent parse the API response correctly?**
- [ ] **Does the agent handle API errors gracefully?** (fallback mode if Selemene down)
- [ ] **Is the consciousness_level parameter set correctly?** (0-5 scale)

---

## 🔥 **Immediate Actions**

### **1. Ensure Selemene Engine is Running**

```bash
# Check if already running
ps aux | grep noesis-server
ps aux | grep "bun.*ts-engines"

# If not running, start both:
cd /Volumes/madara/2026/witnessos/Selemene-engine
cargo run --bin noesis-server &  # Rust API on :8080
cd ts-engines && bun run src/index.ts &  # TS engines on :3001
```

### **2. Update Cron Job Implementations to Call Selemene**

**Example:** `discord-biorhythm-sync` payload needs to:

```javascript
// BEFORE (hallucination risk):
const physical = Math.sin((Date.now() - birthTime) / (23 * 86400000)) * 100;
// ❌ This is fake! Not Swiss Ephemeris-based.

// AFTER (verified data):
const response = await fetch('http://localhost:8080/api/v1/workflows/daily-practice', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    birth_data: {
      date: "1991-08-13",
      time: "13:31",
      latitude: 12.9716,
      longitude: 77.5946,
      timezone: "Asia/Kolkata"
    },
    current_date: new Date().toISOString().split('T')[0],
    consciousness_level: 3
  })
});
const { biorhythm } = await response.json();
// ✅ Now we have verified sine wave calculations
```

### **3. Add Graceful Degradation**

```javascript
let biorhythmData;
try {
  biorhythmData = await fetchFromSelemene();
} catch (error) {
  console.error('Selemene Engine down, using fallback mode');
  biorhythmData = { physical: null, emotional: null, intellectual: null };
  // Still deliver message, but note: "Biorhythm calculation unavailable"
}
```

---

## 🎯 **Integration Priorities by Batch**

### **Batch 2 (Lunar Jobs) — Selemene Integration: CRITICAL**
- `lunar-resonance-orchestrator-daily` → Needs `daily-practice` workflow (Panchanga tithi, nakshatra)
- `new-moon-rupture-audit-one-shot` → Needs Panchanga (detect Amavasya)
- `full-moon-octave-jump-one-shot` → Needs Panchanga (detect Purnima)
- `lunar-authority-review-cycle` → Needs `self-inquiry` workflow (Gene Keys + HD Authority)

### **Batch 3 (Vocation + Creation) — Selemene Integration: MODERATE**
- `vocation-hour-enforcer` → Needs `birth-blueprint` (HD Authority = Sacral response check)
- `twc-content-generator-daily` → Can use `creative-expression` workflow (sigil/geometry for visuals)
- `discord-field-notes-essay` → Can use `self-inquiry` workflow (Gene Keys contemplations)
- `discord-morning-packet` → Can use `daily-practice` workflow (current dasha, biorhythm)

### **Batch 4 (Divination + Biorhythms) — Selemene Integration: CRITICAL**
- `discord-divination-drop` → Needs `decision-support` workflow (Tarot/I-Ching spreads)
- `discord-breath-protocol` → Needs `daily-practice` workflow (biorhythm phases for Vayu selection)
- `discord-biorhythm-sync` → Needs `daily-practice` workflow (4 sine wave calculations)
- `discord-biorhythm-practice` → Reads biorhythm-sync output (inherits verified data)

### **Batch 5 (Weekly Synthesis) — Selemene Integration: LOW (Reflection-Based)**
- `discord-build-digest` → Scans memory logs (no calculation needed)
- `discord-churned-bts` → Scans daily logs (no calculation needed)
- `discord-moc-synthesis` → Can optionally call `full-spectrum` for cross-domain synthesis
- `discord-library-synthesis` → Can optionally call `full-spectrum` for flagship depth

---

## 📚 **Reference: Verified User Data (profile.json)**

**All cron jobs referencing user-specific data MUST USE:**

```json
{
  "birth_data": {
    "date": "1991-08-13",
    "time": "13:31",
    "timezone": "Asia/Kolkata",
    "latitude": 12.9716,
    "longitude": 77.5946
  },
  "human_design": {
    "type": "Generator",
    "authority": "Sacral",
    "profile": "2/4"
  },
  "numerology": {
    "power_frequencies": [8, 13, 19, 44]
  },
  "vimshottari": {
    "current_mahadasha": "Mars (ends 2026-09-14)",
    "current_antardasha": "Moon (ends 2025-08-26)"
  }
}
```

**Source:** `/Volumes/madara/2026/witnessos/Selemene-engine/.about_me/profile.json`

---

## ✅ **Verification Protocol**

Before marking any cron job implementation as "complete":

1. **Smoke Test:** Run `cron run [job-id]` and verify Selemene API calls succeed
2. **Data Validation:** Check that returned biorhythm/dasha/gate values match Selemene output
3. **Error Handling:** Disconnect Selemene, verify graceful fallback mode works
4. **7-Day Monitoring:** Track for hallucination incidents (fake gate numbers, wrong dasha periods)

---

## 🔮 **The North Star**

**Every number, every gate, every dasha period must be traceable to Selemene Engine calculations.**

**If a cron job generates data it can't verify → it's hallucinating → it must be fixed.**

**Tryambakam Noesis = Living Architecture**  
**Selemene Engine = Verified Calculation Substrate**  
**Together = Non-Hallucination Consciousness Platform**

---

**End of Integration Document**
