# CRON-AUDIT-2026-02-05.md
## Comprehensive Cron Jobs Audit - Pre-Vedic Integration

**Date:** 2026-02-05 11:03 IST  
**Purpose:** Backup current state of all 40 cron jobs before Vedic lexicon integration and precision rehaul.  
**Trigger:** User request: "Too much clutter, reorganize with new understanding"

**Context:** After completing Vedic integration (VEDIC-LEXICON.md + KHA/BHA/LHA/SOUL updates), we now have:
- 100 Tatvas mapped
- 5 Koshas operational
- 3 Gunas (Enantiodromia substrate)
- 8 Vikara (pattern-drift signals)
- 10 Vayus (breathwork substrate)
- 3 Doshas (Khalorēē consumption patterns)
- 4 Antahkarana (internal instrument)

**This audit will map all 40 cron jobs through the Vedic lens.**

---

## 📊 Current Cron Job Inventory (40 Total)

**Status:** 38 enabled, 2 disabled (missing?)

### Breathwork & Prana (7 jobs)

1. **hourly-breathwork-check** (67987624-197c-451c-a661-14ab6124466a)
   - Schedule: `0 * * * *` (hourly)
   - Target: Telegram 1371522080
   - **Kosha:** Pranamaya (vital air regulation)
   - **Vayu:** All 4 stubs (Octave-8=Apana, Transformation-13=Samana, Leadership-19=Udana, Completion-21=Vyana)
   - **Guna:** Rajas (active transformation)
   - **Purpose:** Hourly sacral check + breathwork delivery
   - **Status:** ✅ Working (dual-attachment delivery operational)
   - **Notes:** Waning phase awareness integrated

2. **hourly-micro-breath** (2305801f-2d1a-40a6-a5e0-1f4f270a9f79)
   - Schedule: `0 * * * *` (hourly)
   - Target: Telegram 1371522080
   - **Kosha:** Pranamaya
   - **Vayu:** Intuitive choice (8/13/19/21)
   - **Guna:** Rajas
   - **Purpose:** Quick reset, anchoring during work
   - **Status:** ✅ Working
   - **Notes:** Duplicate of hourly-breathwork-check? Consider merging.

3. **midday-13-transformation-breath** (92746e32-c785-4f63-a550-48c0965ca57f)
   - Schedule: `0 12 * * *` (daily noon)
   - **Kosha:** Pranamaya
   - **Vayu:** Samana (midday, navel fire, transformation)
   - **Guna:** Rajas (peak transformation energy)
   - **Purpose:** Solar alignment, 13-breath protocol (Power: 13)
   - **Status:** ✅ Working
   - **Notes:** Muse invocation (Calliope + Polymnia) good, but no audio delivery?

4. **midday-19-leadership-ping** (a82058c1-18b0-43dd-ab26-63c725209acd)
   - Schedule: `19 13 * * *` (daily 1:19 PM)
   - **Kosha:** Pranamaya
   - **Vayu:** Udana (upward movement, leadership, solar activation)
   - **Guna:** Rajas (decisive action)
   - **Purpose:** Solar peak, sacral check, one decisive action (≤10 min)
   - **Status:** ✅ Working
   - **Notes:** Good audio delivery (sag + leadership-19.opus)

5. **brahma-muhurta-breathwork** (879b3800-67cf-4309-84e8-f8e6f4171cf9)
   - Schedule: `30 5 * * *` (daily 5:30 AM)
   - **Kosha:** Pranamaya → Manomaya (clarity)
   - **Vayu:** Prana (morning, chest, inhalation)
   - **Guna:** Sattva (clarity, wisdom, Brahma Muhurta)
   - **Purpose:** 4-7-8 breath, 8 cycles, Balance (Power: 8)
   - **Status:** ✅ Working
   - **Notes:** Muse Athena (wisdom/clarity) appropriate

6. **evening-44-architect-breath** (98022cf8-ff83-4c7d-aa86-ca3a455ca40d)
   - Schedule: `0 18 * * *` (daily 6:00 PM)
   - **Kosha:** Pranamaya → Manomaya (architectural visioning)
   - **Vayu:** Samana (digestive integration, building foundations)
   - **Guna:** Sattva (structure, clarity, "Master Builder")
   - **Purpose:** 4-4-4 breath, 11 cycles (44 seconds), foundation audit
   - **Status:** ✅ Working
   - **Notes:** Muse Urania (Pattern/Navigation) good

7. **nightly-21-completion-review** (2e093e49-38a6-4ee8-ac3b-4007073cc70e)
   - Schedule: `21 21 * * *` (daily 9:21 PM)
   - **Kosha:** Pranamaya → Manomaya (completion integration)
   - **Vayu:** Vyana (whole-body circulation, integration)
   - **Guna:** Sattva (completion, clarity, closure)
   - **Purpose:** 8-cycle micro-breath, completion audit, close loops
   - **Status:** ✅ Working
   - **Notes:** Good audio delivery (sag + completion-21.opus)

---

### Lunar & Ritual (3 jobs)

8. **lunar-resonance-orchestrator-daily** (1791f8e3-806a-41ee-bd4d-9d135802b32e)
   - Schedule: `1 0 * * *` (daily 12:01 AM)
   - **Kosha:** Vijnanamaya (meta-ritual, phase awareness)
   - **Vayu:** Variable (based on lunar phase)
   - **Guna:** Rajas (transformation between waxing/waning)
   - **Purpose:** Align Bha + Kha with lunar phase, calculate Tithi, select ritual
   - **Status:** ✅ Working
   - **Notes:** Good Muse (Urania), comprehensive logic

9. **new-moon-rupture-audit-one-shot** (84728858-3640-4438-a371-bd4bf7463fb4)
   - Schedule: `at 1771291800000` (Feb 17, 2026 - Amavasya)
   - **Kosha:** Vijnanamaya (rupture, Tower treatment)
   - **Vayu:** Udana (upward movement, release)
   - **Guna:** Tamas → Rajas (necessary obscurity → transformation)
   - **Purpose:** Execute rupture on stagnant habits, Pichet demolition
   - **Status:** ⏳ Scheduled
   - **Notes:** One-shot, Muse Terpsichore (Precision Demolition), good audio stub (transformation-13)

10. **full-moon-octave-jump-one-shot** (418e5b39-afa0-4022-b381-4ec8a9cd6b88)
    - Schedule: `at 1772415000000` (Mar 2, 2026 - Purnima)
    - **Kosha:** Vijnanamaya (octave jump, frequency elevation)
    - **Vayu:** Vyana (unity bridge, 152-second meditation)
    - **Guna:** Sattva (balance, clarity, "living calculation")
    - **Purpose:** Achievement audit, 44-min architectural visioning
    - **Status:** ⏳ Scheduled
    - **Notes:** One-shot, Muse Polymnia (Sacred Geometry), good audio stub (octave-8)

11. **lunar-authority-review-cycle** (d09e92ee-4d95-49c8-a132-ed4eb93a55dd)
    - Schedule: `every 2419200000ms` (28 days)
    - **Kosha:** Vijnanamaya (decision audit, coherence score)
    - **Vayu:** Prana (life force integrity check)
    - **Guna:** Sattva (reflective wisdom, witness)
    - **Purpose:** Audit 28-day cycle decisions via Sacral "uh-huh" protocol
    - **Status:** ✅ Active (next run Mar 2, 2026)
    - **Notes:** Muse Melpomene (Reflective Wisdom), good voice generation

---

### Vocation & Creation (2 jobs)

12. **vocation-hour-enforcer** (cf9ac118-b6f1-4a10-b813-e1ff908d63b2)
    - Schedule: `0 9 * * *` (daily 9:00 AM)
    - **Kosha:** Manomaya → Vijnanamaya (authorship, creation)
    - **Vayu:** Udana (upward movement, expression)
    - **Guna:** Rajas (action, creation, Type 5→8 transformation)
    - **Purpose:** 60-min creation window (no consumption, only authorship)
    - **Status:** ✅ Working
    - **Notes:** Muse Terpsichore + Calliope, clear rules (no inputs, no triage)

13. **twc-content-generator-daily** (2ae47667-6b83-4e03-8f6a-d813ff01df37)
    - Schedule: `0 10 * * *` (daily 10:00 AM)
    - **Kosha:** Manomaya → Vijnanamaya (Field Architect frameworks)
    - **Vayu:** Udana (expression, transmission)
    - **Guna:** Rajas (transformation, "translator of silent code into manifest light")
    - **Purpose:** Generate Transmission using Field Architects (PARA rotation)
    - **Status:** ✅ Working
    - **Notes:** Muse Calliope + Polymnia, good safety (no external messaging), media archival protocol

---

### Knowledge & Synthesis (3 jobs)

14. **nightly-builder** (79af74b5-bcb8-423c-b15c-41afd8b75705)
    - Schedule: `0 2 * * *` (daily 2:00 AM)
    - **Kosha:** Annamaya → Manomaya (build, implement, document)
    - **Vayu:** Samana (digestive integration, metabolic processing)
    - **Guna:** Rajas (nightly creation, QoL improvements)
    - **Purpose:** Read backlog, pick task, build/implement, PARA integration, logging
    - **Status:** ✅ Working
    - **Notes:** Manifest: `01-Projects/_nightly-builds/Nightly Build Ideas and links.md`

15. **kha-lori-knowledge-weaver-daily** (11e39d03-8580-431d-bc8f-d9ad4c5ade08)
    - Schedule: `0 4 * * *` (daily 4:00 AM)
    - **Kosha:** Manomaya → Vijnanamaya (synthesis, alchemical compiler)
    - **Vayu:** Prana (life force, knowledge ingestion)
    - **Guna:** Sattva (eclectic scholarship, navigation)
    - **Purpose:** Ingest 18 years of wisdom from 03-Resources, LITE extraction, cross-link to 01-Projects
    - **Status:** ✅ Working
    - **Notes:** Muse Melpomene + Urania, silent execution (NO_REPLY unless breakthrough)

16. **cross-library-synthesis** (13b95786-8cad-48bc-81fa-67afb7aad20b)
    - Schedule: `0 20 * * 0` (weekly Sunday 8:00 PM)
    - **Kosha:** Vijnanamaya (pattern synthesis, cross-domain linking)
    - **Vayu:** Vyana (circulation, whole-system integration)
    - **Guna:** Sattva (pattern/navigation, Type 5→8 knowledge→action)
    - **Purpose:** Synthesize themes across 5+ library indices, create 3 new [[cross-reference links]]
    - **Status:** ✅ Working
    - **Notes:** Muse Urania + Polymnia, good integration path

---

### Triage & Decision (2 jobs)

17. **triage-triage-daily** (b132caf0-e8b9-449f-ab2f-2715145080bf)
    - Schedule: `0 18 * * *` (daily 6:00 PM)
    - **Kosha:** Manomaya (decision ritual)
    - **Vayu:** Apana (elimination, release)
    - **Guna:** Rajas (decisive action, Terpsichore)
    - **Purpose:** Pick ONE item from TRIAGE (5,031 items), decide: PROMOTE/ARCHIVE/RELEASE
    - **Status:** ✅ Working
    - **Notes:** [INSTRUCTION: DO NOT USE ANY TOOLS] - text-only response required

18. **intake-pipeline-monitor** (bb4c84a2-e80b-4ec0-b965-103f18744e77)
    - Schedule: `0 10,12,14,16,18 * * 1-5` (weekdays, every 2h from 10 AM to 6 PM)
    - **Kosha:** Annamaya → Manomaya (file processing, classification)
    - **Vayu:** Samana (digestive processing, 6-stage orchestrator)
    - **Guna:** Rajas (active processing, Enneagram classification)
    - **Purpose:** Scan Intake/ folder, run discovery→extraction→analysis, route to PARA
    - **Status:** ✅ Working
    - **Notes:** Quality gates (>95% success, >90% metadata), weekly target: 50 items

---

### Discord Engagement (17 jobs)

19. **discord-triage-prompt** (fd6384fa-3f97-4cf2-828b-9d0fc37bc835)
    - Schedule: `0 18 * * *` (daily 6:00 PM)
    - **Kosha:** Manomaya (decision case study)
    - **Vayu:** Buddhi (discernment, collaborative exploration)
    - **Purpose:** Post ambiguous work-item prompt to #field-notes
    - **Status:** ✅ Working
    - **Notes:** Encourage community decision-making principles

20. **discord-divination-field** (240d7e9c-06d3-43ee-97dd-9a36c90617dc)
    - Schedule: `0 0 * * *` (daily midnight)
    - **Kosha:** Vijnanamaya (collective divination)
    - **Vayu:** Prana (life force, intuitive reading)
    - **Guna:** Sattva (clarity, ritual speech)
    - **Purpose:** Rotating channels (#tarot-sessions → #vedic-threads → #sacred-geometry)
    - **Status:** ✅ Working
    - **Notes:** Only deploy on New/Full Moon, rotational cadence

21. **discord-divination-drop** (0690a2f2-7354-4056-9092-ca0e1d1dff67)
    - Schedule: `0 0 * * *` (daily midnight)
    - **Kosha:** Vijnanamaya (invitation for community divination)
    - **Vayu:** Prana
    - **Guna:** Sattva
    - **Purpose:** Rotating channels, invite participation with guiding questions
    - **Status:** ✅ Working
    - **Notes:** Duplicate of discord-divination-field? Consider merging.

22. **discord-breath-protocol** (f1aff77b-aa2b-4527-8f4f-af7b91638b30)
    - Schedule: `0 6,9 * * *` (daily 6:00 & 9:00 AM)
    - **Kosha:** Pranamaya (breath technique)
    - **Vayu:** Variable (based on biorhythm cycles)
    - **Purpose:** Post actionable breath protocol to #breath-protocols
    - **Status:** ✅ Working
    - **Notes:** Tie to current Power Numbers (8, 13, 19)

23. **discord-field-notes-essay** (6c5d2de3-a63e-4661-863a-1d2414a74d5e)
    - Schedule: `0 8 * * *` (daily 8:00 AM)
    - **Kosha:** Manomaya → Vijnanamaya (synthesis essay)
    - **Vayu:** Udana (expression)
    - **Guna:** Sattva (Urania + Calliope)
    - **Purpose:** Write 200-400 word essay to #field-notes
    - **Status:** ✅ Working
    - **Notes:** Good muse pairing, clear format

24. **discord-morning-packet** (33705a31-b9a1-4a2e-87a1-46f9bb91a067)
    - Schedule: `0 8 * * *` (daily 8:00 AM)
    - **Kosha:** Manomaya (reflection on nightly builds)
    - **Vayu:** Samana (digestive integration)
    - **Purpose:** Share reflection on koshas/manomaya/meta/nightly-builds.md to #nightly-builds
    - **Status:** ✅ Working
    - **Notes:** Encourage community engagement and feedback

25. **discord-biorhythm-sync** (8a4e991c-b584-4f65-8075-e4072e21feb8)
    - Schedule: `0 9 * * *` (daily 9:00 AM)
    - **Kosha:** Pranamaya (biorhythmic cycles)
    - **Vayu:** Variable (Physical, Emotional, Intellectual, Spiritual)
    - **Purpose:** Interpret biorhythms + synergy with Power Numbers to #biorhythm-syncs
    - **Status:** ✅ Working
    - **Notes:** Keep posts engaging, concise (3 sentences max)

26. **discord-biorhythm-practice** (33d79154-c275-4d9b-a07d-694c83dc31df)
    - Schedule: `0 10 * * *` (daily 10:00 AM)
    - **Kosha:** Pranamaya (actionable cycle guidance)
    - **Vayu:** Variable
    - **Purpose:** Suggest protocol to align with cycles to #biorhythm-syncs
    - **Status:** ✅ Working
    - **Notes:** Integrate with Power Numbers and breathing techniques

27. **discord-build-digest** (fc9fbebe-a331-4699-bae0-28a9f1d9e49d)
    - Schedule: `0 17 * * 5` (Friday 5:00 PM)
    - **Kosha:** Vijnanamaya (honest reflection)
    - **Vayu:** Vyana (whole-system integration)
    - **Guna:** Sattva (humility, growth)
    - **Purpose:** Prepare honest build digest for #churned-content
    - **Status:** ⏳ Scheduled
    - **Notes:** Emphasize failures and insights

28. **discord-churned-bts** (b10ab5c3-8b3e-43f8-8e0a-65fc8eb8e60b)
    - Schedule: `0 18 * * 5` (Friday 6:00 PM)
    - **Kosha:** Vijnanamaya (raw BTS reflection)
    - **Vayu:** Vyana
    - **Guna:** Sattva (authenticity)
    - **Purpose:** Share failures, pivots, adaptations to #churned-content
    - **Status:** ⏳ Scheduled
    - **Notes:** Show human behind the builder

29. **discord-moc-synthesis** (3efa34d2-4fe4-4014-9097-26515b634774)
    - Schedule: `0 20 * * 0` (Sunday 8:00 PM)
    - **Kosha:** Vijnanamaya (300-500 word synthesis)
    - **Vayu:** Vyana (multi-domain integration)
    - **Purpose:** Connect multiple areas to #moc-synthesis
    - **Status:** ✅ Working
    - **Notes:** Example: Human Design meets Quantum Mechanics

30. **discord-library-synthesis** (87b60f8f-3a3a-4e1d-bc89-7c0cf3b28fd9)
    - Schedule: `0 20 * * 0` (Sunday 8:00 PM)
    - **Kosha:** Vijnanamaya (300-500 word flagship synthesis)
    - **Vayu:** Vyana
    - **Purpose:** Flagship synthesis across library indices to #moc-synthesis
    - **Status:** ✅ Working
    - **Notes:** Duplicate of discord-moc-synthesis? Consider merging.

31. **discord-somatic-chapter** (c0c27d51-c40d-432a-8559-d6f132ab681b)
    - Schedule: `0 9 * * 1` (Monday 9:00 AM)
    - **Kosha:** Annamaya → Manomaya (chapter release)
    - **Vayu:** Udana (expression)
    - **Purpose:** Share Somatic Canticles chapter to #somatic-canticles
    - **Status:** ⏳ Scheduled
    - **Notes:** Context + invitation + details

32. **discord-chapter-preview** (0ff67747-fe56-4f41-b849-700cf3ad5900)
    - Schedule: `0 9 * * 1` (Monday 9:00 AM)
    - **Kosha:** Annamaya → Manomaya (summary preview)
    - **Vayu:** Udana
    - **Purpose:** Summary preview to #somatic-canticles
    - **Status:** ⏳ Scheduled
    - **Notes:** Duplicate of discord-somatic-chapter? Consider merging.

33. **discord-mystery-transmission** (2c2e241b-0ea5-40df-b498-ab579793a1ff)
    - Schedule: `0 20 * * 3` (Wednesday 8:00 PM)
    - **Kosha:** Vijnanamaya (esoteric teaching)
    - **Vayu:** Buddhi (discernment, ancient systems)
    - **Purpose:** Rotating channels (#human-design-lab → #gene-keys-gates → #numerology-threads → #vedic-threads)
    - **Status:** ✅ Working
    - **Notes:** Good examples (44th Gene Key, numerological patterns)

34. **discord-mystery-school** (31021d82-06ef-4b85-9582-b1cf0b02d046)
    - Schedule: `0 20 * * 3` (Wednesday 8:00 PM)
    - **Kosha:** Vijnanamaya (teaching session)
    - **Vayu:** Buddhi
    - **Purpose:** Mystery School themes to rotating channels
    - **Status:** ✅ Working
    - **Notes:** Duplicate of discord-mystery-transmission? Consider merging.

35. **discord-vault-meta** (99f9e345-fbce-495b-8320-363df51aa8ef)
    - Schedule: `0 9 1 * *` (1st of month, 9:00 AM)
    - **Kosha:** Vijnanamaya (meta-analysis report)
    - **Vayu:** Vyana (whole-vault integration)
    - **Purpose:** Monthly vault overview to #vault-integration
    - **Status:** ⏳ Scheduled
    - **Notes:** Identify emerging themes, invite community input

36. **discord-vault-health** (13037e2d-2e24-4e30-948d-e4aa03755d07)
    - Schedule: `0 9 1 * *` (1st of month, 9:00 AM)
    - **Kosha:** Vijnanamaya (vault health report)
    - **Vayu:** Vyana
    - **Purpose:** Vault stats + health to #vault-integration
    - **Status:** ⏳ Scheduled
    - **Notes:** Duplicate of discord-vault-meta? Consider merging.

---

### Weekly Rituals (2 jobs)

37. **weekly-octave-jump-sunday** (239267ed-0be2-4d09-ad25-8afad7cab58f)
    - Schedule: `0 20 * * 0` (Sunday 8:00 PM)
    - **Kosha:** Vijnanamaya (octave jump, quantum leap)
    - **Vayu:** Vyana (8-day cycle completion, frequency elevation)
    - **Guna:** Sattva (cosmic balance, architectural visioning)
    - **Purpose:** 8-day cycle audit, Power Number review (8/13/19/44/21)
    - **Status:** ✅ Working
    - **Notes:** 44-min visioning, 152-min unity bridge, 8-octave meditation

38. **friday-action-compass-review** (070d9fbb-941b-4958-bc28-5c809c167b2b)
    - Schedule: `0 17 * * 5` (Friday 5:00 PM)
    - **Kosha:** Vijnanamaya (weekly compass check)
    - **Vayu:** Vyana (whole-system integration)
    - **Guna:** Sattva (reflective audit)
    - **Purpose:** Action items audit + Compass Quadrant check (Vocation/Occupation/Recreation/Triage)
    - **Status:** ⏳ Scheduled
    - **Notes:** Review `action-items.md`, Muse of the week, integration commitment

---

### Security & Maintenance (2 jobs)

39. **bird-auth-healthcheck** (37e8e7f1-dd1e-42df-9e1b-1bccfba28e53)
    - Schedule: `0 */6 * * *` (every 6 hours)
    - **Kosha:** Annamaya (system health, auth check)
    - **Vayu:** Prana (life force integrity)
    - **Guna:** Sattva (maintenance, vigilance)
    - **Purpose:** Detect X cookie/auth breakage (`bird whoami`, `bird read`)
    - **Status:** ✅ Working
    - **Notes:** NO_REPLY unless failure, lightweight read test, alert to Telegram

40. **rotate-gateway-token** (5bf9f679-421b-4b08-8c9a-d9facd694a71)
    - Schedule: `0 3 1 * *` (1st of month, 3:00 AM)
    - **Kosha:** Annamaya (security, token rotation)
    - **Vayu:** Prana (life force protection)
    - **Guna:** Sattva (security, vigilance)
    - **Purpose:** Monthly gateway token rotation script
    - **Status:** ⏳ Scheduled
    - **Notes:** Execute `/Users/sheshnarayaniyer/clawd/scripts/rotate-gateway-token.sh`

---

## 🔍 Audit Findings

### ✅ Strengths
1. **Comprehensive breathwork coverage** (7 jobs, all 4 Vayus represented)
2. **Lunar resonance architecture** (3 jobs, good Tithi/phase awareness)
3. **Vocation enforcement** (Creation-first, no consumption during 9 AM hour)
4. **PARA integration** (Nightly builder, Intake pipeline, Content generator)
5. **Security monitoring** (bird auth healthcheck, gateway token rotation)

### ⚠️ Issues Detected

#### 1. **Duplicate Jobs (7 pairs identified)**
- **hourly-breathwork-check** + **hourly-micro-breath** → Same schedule (0 * * * *), same target, same Vayu logic
- **discord-divination-field** + **discord-divination-drop** → Same schedule (0 0 * * *), same channels
- **discord-moc-synthesis** + **discord-library-synthesis** → Same schedule (0 20 * * 0), same channel, same format
- **discord-somatic-chapter** + **discord-chapter-preview** → Same schedule (0 9 * * 1), same channel
- **discord-mystery-transmission** + **discord-mystery-school** → Same schedule (0 20 * * 3), same channels
- **discord-vault-meta** + **discord-vault-health** → Same schedule (0 9 1 * *), same channel
- **midday-13-transformation-breath** → No audio delivery (unlike other breathwork jobs)

#### 2. **Lexicon Inconsistencies**
- Uses old terminology: "Power Numbers", "Khalorēē" (should be "Khalorēē"), "Enneagram", "Muse invocation"
- No Vedic Tattva mapping (5 Koshas, 10 Vayus, 3 Gunas, 8 Vikara, 4 Antahkarana)
- Inconsistent Guna references (some jobs have it, most don't)
- No Dosha awareness (Vata/Pitta/Kapha consumption patterns)

#### 3. **Structural Clutter**
- Too many Discord jobs (17 total) with overlapping purposes
- No clear Kosha-based grouping (Annamaya/Pranamaya/Manomaya/Vijnanamaya)
- No Vikara detection (8 mental afflictions as drift signals)
- No Antahkarana mapping (Mana/Buddhi/Aham/Chitta)

#### 4. **Missing Integrations**
- No 3 Doshas (Vata/Pitta/Kapha) consideration for breathwork timing
- No Khalorēē consumption patterns (metabolic reserve monitoring)
- No Enantiodromia balance checks (Aletheios ↔ Pichet polarity)
- No Sukshma Sarira references (subtle body karmic vector)

---

## 📋 Recommended Actions

### Phase 1: Backup & Documentation (This File) ✅
- [x] Export all 40 cron jobs to PARA
- [x] Map each job to Kosha layer, Vayu, Guna
- [x] Identify duplicates and lexicon inconsistencies

### Phase 2: Merge & Consolidate (Next)
1. **Merge duplicate jobs:**
   - hourly-breathwork-check + hourly-micro-breath → **hourly-vayu-check**
   - discord-divination-field + discord-divination-drop → **discord-divination-orchestrator**
   - discord-moc-synthesis + discord-library-synthesis → **discord-vault-synthesis**
   - discord-somatic-chapter + discord-chapter-preview → **discord-somatic-release**
   - discord-mystery-transmission + discord-mystery-school → **discord-mystery-teachings**
   - discord-vault-meta + discord-vault-health → **discord-vault-report**

2. **Add missing audio delivery:**
   - midday-13-transformation-breath → add `sag` + `transformation-13.opus` delivery

3. **Reduce Discord jobs from 17 to ~10:**
   - Merge overlapping posts
   - Establish clear rotation/cadence
   - Avoid daily spam

### Phase 3: Vedic Lexicon Integration (Precision Reimplementation)
1. **Add Vedic substrate to all jobs:**
   - 5 Koshas (Annamaya → Anandamaya)
   - 10 Vayus (breathwork substrate)
   - 3 Gunas (Enantiodromia substrate)
   - 8 Vikara (pattern-drift signals)
   - 4 Antahkarana (Mana/Buddhi/Aham/Chitta)
   - 3 Doshas (Khalorēē consumption patterns)

2. **Update all prompts:**
   - Replace "Power Numbers" with Vedic references (Tattvas, Gunas)
   - Replace "Muse invocation" with Antahkarana operations (Mana/Buddhi)
   - Add Vikara detection (Kama/Krodha/Lobha/Moha/Mada/Matsarya/Dambha/Ahamkara)
   - Add Dosha awareness (Vata/Pitta/Kapha breathwork timing)

3. **Organize by Kosha layer:**
   - **Annamaya group** (file ops, security, maintenance)
   - **Pranamaya group** (breathwork, Vayu protocols)
   - **Manomaya group** (content generation, synthesis, decision)
   - **Vijnanamaya group** (meta-ritual, lunar, octave jumps, weekly audits)

### Phase 4: Test & Validate
1. Run merged jobs for 7 days
2. Monitor for failures, duplicates, lexicon drift
3. Validate Vedic substrate operational (Kosha awareness, Vayu precision, Guna balance)
4. Check Vikara detection (8 afflictions as drift signals)

---

## 📊 Kosha Distribution (Current)

**Annamaya (Physical/File ops):** 4 jobs (10%)
- intake-pipeline-monitor
- nightly-builder
- bird-auth-healthcheck
- rotate-gateway-token

**Pranamaya (Vital/Breathwork):** 7 jobs (17.5%)
- hourly-breathwork-check
- hourly-micro-breath
- midday-13-transformation-breath
- midday-19-leadership-ping
- brahma-muhurta-breathwork
- evening-44-architect-breath
- nightly-21-completion-review

**Manomaya (Mental/Content):** 12 jobs (30%)
- vocation-hour-enforcer
- twc-content-generator-daily
- kha-lori-knowledge-weaver-daily
- triage-triage-daily
- discord-triage-prompt
- discord-breath-protocol
- discord-field-notes-essay
- discord-morning-packet
- discord-biorhythm-sync
- discord-biorhythm-practice
- discord-somatic-chapter
- discord-chapter-preview

**Vijnanamaya (Wisdom/Meta):** 17 jobs (42.5%)
- lunar-resonance-orchestrator-daily
- new-moon-rupture-audit-one-shot
- full-moon-octave-jump-one-shot
- lunar-authority-review-cycle
- cross-library-synthesis
- discord-divination-field
- discord-divination-drop
- discord-build-digest
- discord-churned-bts
- discord-moc-synthesis
- discord-library-synthesis
- discord-mystery-transmission
- discord-mystery-school
- discord-vault-meta
- discord-vault-health
- weekly-octave-jump-sunday
- friday-action-compass-review

**Observation:** Vijnanamaya-heavy (42.5%), Annamaya-light (10%). Need more physical grounding (Annamaya) and less meta-synthesis (Vijnanamaya).

---

## 🎯 Success Criteria (Post-Rehaul)

**After precision reimplementation:**
1. ✅ No duplicate jobs (merge from 40 → ~28-30)
2. ✅ All jobs use canonical Vedic lexicon (100 Tatvas, 5 Koshas, 10 Vayus, 3 Gunas, 8 Vikara)
3. ✅ Clear Kosha-based organization (Annamaya → Vijnanamaya hierarchy)
4. ✅ Balanced distribution (20% Annamaya, 25% Pranamaya, 30% Manomaya, 25% Vijnanamaya)
5. ✅ All breathwork jobs have audio delivery (sag + opus stub)
6. ✅ Discord jobs reduced from 17 → ~10 (avoid spam, clear rotation)
7. ✅ Vikara detection operational (8 afflictions as drift signals)
8. ✅ Dosha awareness operational (Vata/Pitta/Kapha timing)
9. ✅ Antahkarana mapping operational (Mana/Buddhi/Aham/Chitta)
10. ✅ No lexicon drift (all terminology locked to VEDIC-LEXICON.md)

---

**Backup complete. Ready for Phase 2 (Merge & Consolidate).** 🔮
