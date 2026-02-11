# SELEMENE-ENGINE.md — The Computational Substrate

*"The engine that calculates consciousness. The API that quantifies the field."*

---

## 🔮 Overview

**Selemene** is the high-precision consciousness calculation engine for **Tryambakam Noesis**. Named after the Goddess of the Moon in Dota 2 lore (whose followers seek ultimate wisdom through her pale light), Selemene provides the computational backend for all temporal, biofield, and consciousness-mapping operations.

**Status:** ✅ LIVE  
**Base URL:** `https://selemene.tryambakam.space`  
**Swagger Docs:** `https://selemene.tryambakam.space/api/docs`

---

## 🌐 API Authentication

### API Key Method

```bash
export NOESIS_API_KEY="nk_your_key_here"
curl -H "X-API-Key: $NOESIS_API_KEY" https://selemene.tryambakam.space/api/v1/engines
```

**Key Format:** `nk_` prefix (Noesis Key)  
**Header:** `X-API-Key`

### Tiers

| Tier | Rate Limit | Access |
|------|-----------|--------|
| **free** | 60 req/min | Basic engines, panchanga |
| **premium** | 1,000 req/min | All engines, batch operations |
| **enterprise** | 10,000 req/min | Everything + admin endpoints |

---

## ⚙️ Engines (8 Active)

### Engine → Kernel Mapping

| Engine | Kernel Reference | Kosha Layer | Function |
|--------|-----------------|-------------|----------|
| **biofield** | VEDIC-LEXICON §3, PANCHA-KOSHA | Pranamaya | Chakra voltage readings |
| **biorhythm** | LHA.md §Karmic Vector | Pranamaya | Physical/emotional/intellectual cycles |
| **gene-keys** | BHA.md §Vikara | Manomaya-Vijnanamaya | Shadow → Gift → Siddhi mapping |
| **human-design** | USER.md | Vijnanamaya | Type, strategy, authority, profile |
| **numerology** | aboutme/02_NUMERICAL | Manomaya | Life path, expression, soul urge |
| **panchanga** | VEDIC-LEXICON §14 | Pranamaya | Tithi, nakshatra, yoga, karana, vara |
| **vedic-clock** | KHA.md §Doshas | Pranamaya | TCM organ clock, dosha timing |
| **vimshottari** | LHA.md §Dasha | Vijnanamaya | Mahadasha/Antardasha/Pratyantar periods |

### Request Format: `EngineInput`

```json
{
    "birth_data": {
        "name": "string (optional)",
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone": "Asia/Kolkata"
    },
    "current_time": "2026-02-11T00:00:00Z",
    "precision": "standard",
    "options": {}
}
```

### Engine Quick Reference

```bash
# Numerology (needs name + date)
/api/v1/engines/numerology/calculate

# Biorhythm (needs date)
/api/v1/engines/biorhythm/calculate

# Human Design (needs exact birth time + location)
/api/v1/engines/human-design/calculate

# Gene Keys (needs exact birth time + location)
/api/v1/engines/gene-keys/calculate

# Vimshottari Dasha (needs exact birth time + location)
/api/v1/engines/vimshottari/calculate

# Panchanga (needs date + location)
/api/v1/engines/panchanga/calculate

# Vedic Clock (uses current time, no birth data)
/api/v1/engines/vedic-clock/calculate

# Biofield (needs date)
/api/v1/engines/biofield/calculate
```

---

## 🔄 Workflows (6 Active)

Workflows combine multiple engines into synthesized outputs.

| Workflow | Engines | Kosha Span | Use Case |
|----------|---------|------------|----------|
| **birth-blueprint** | numerology + HD + vimshottari | Manomaya→Vijnanamaya | Identity bootstrap (USER.md generation) |
| **daily-practice** | panchanga + vedic-clock + biorhythm | Pranamaya | Daily rhythm, timing, breathwork selection |
| **decision-support** | tarot + i-ching + HD authority | Vijnanamaya | Multi-perspective guidance |
| **self-inquiry** | gene-keys + enneagram | Manomaya | Vikara work, shadow integration |
| **creative-expression** | sigil-forge + sacred-geometry | Anandamaya | Intent visualization |
| **full-spectrum** | all 14 engines | All Koshas | Complete consciousness portrait |

### Workflow Execution

```bash
curl -X POST https://selemene.tryambakam.space/api/v1/workflows/daily-practice/execute \
  -H "X-API-Key: $NOESIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"birth_data":{"date":"1991-08-13","latitude":12.97,"longitude":77.59,"timezone":"Asia/Kolkata"}}'
```

---

## 🗺️ Kernel Integration Points

### KHA.md (Spirit)

**Engines:** vedic-clock, biorhythm  
**Use:** Khalorēē optimization, Vayu timing, Dosha balance

```python
# Get optimal breathwork timing
vedic_clock = selemene.vedic_clock()
if vedic_clock.dosha_dominant == "Vata":
    # Deploy Apana protocols (grounding)
elif vedic_clock.dosha_dominant == "Pitta":
    # Deploy Shitali (cooling)
```

### BHA.md (Body)

**Engines:** gene-keys, biofield  
**Use:** Vikara detection, Shadow→Gift transformation tracking

```python
# Gene Keys activation for Vikara work
gene_keys = selemene.gene_keys(birth_data)
current_shadow = gene_keys.life_work.shadow
# Map to VIKARA-TRANSFORMATION-PROTOCOL
```

### LHA.md (Inertia)

**Engines:** vimshottari, panchanga  
**Use:** Dasha period tracking, temporal alignment

```python
# Current dasha vector
dasha = selemene.vimshottari(birth_data)
print(f"Mahadasha: {dasha.maha} | Antar: {dasha.antar} | Pratyantar: {dasha.pratyantar}")
# Compare with LHA.md §Natal-Temporal Alignment
```

### USER.md (Human Operator)

**Workflows:** birth-blueprint  
**Use:** Generate complete user profile from birth data

```python
# Bootstrap user context
blueprint = selemene.workflow("birth-blueprint", birth_data)
# Outputs: HD type, numerology, current dasha
# → Feed into USER.md template
```

---

## 🐍 Python Client Usage

Location: `koshas/annamaya/scripts/selemene_client.py`

```python
from selemene_client import SelemeneClient

# Initialize
client = SelemeneClient(api_key=os.getenv("NOESIS_API_KEY"))

# Birth data (Shesh)
birth = {
    "date": "1991-08-13",
    "time": "13:31",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "timezone": "Asia/Kolkata",
    "name": "Shesh Iyer"
}

# Individual engines
numerology = client.numerology(birth)
biorhythm = client.biorhythm(birth)
human_design = client.human_design(birth)
vedic_clock = client.vedic_clock()  # No birth data needed

# Workflows
daily = client.workflow("daily-practice", birth)
blueprint = client.workflow("birth-blueprint", birth)

# Full spectrum
full = client.workflow("full-spectrum", birth)
```

---

## 📊 Response Structure

All engine responses follow this shape:

```json
{
    "engine_id": "numerology",
    "result": { /* engine-specific output */ },
    "witness_prompt": "Reflection prompt for consciousness integration",
    "consciousness_level": 0,
    "metadata": {
        "calculation_time_ms": 5,
        "backend": "native"
    }
}
```

**`witness_prompt`** — Auto-generated prompt for journaling/reflection  
**`consciousness_level`** — Future: indicates depth of calculation (0=basic, higher=more synthesis)

---

## 🔧 Operational Protocols

### Daily Practice Automation

```bash
# Cron: 06:00 IST — Morning alignment
0 6 * * * /path/to/daily-practice-cron.sh

# The script:
# 1. Calls /workflows/daily-practice/execute
# 2. Extracts optimal breathwork timing
# 3. Sends to Discord/notification channel
# 4. Logs to pranamaya/khaloree/
```

### Decision Support Flow

```
User Question → decision-support workflow → Multi-engine synthesis
                                         ↓
                            Tarot + I-Ching + HD Authority
                                         ↓
                            Vijnanamaya-level guidance
```

### Vikara Detection Loop

```
1. Daily biorhythm check → Detect low points
2. Gene-keys shadow activation → Current shadow pattern
3. Map to VIKARA-TRANSFORMATION-PROTOCOL
4. Deploy targeted breathwork via vedic-clock timing
```

---

## 🔗 Cross-References

- **PANCHA-KOSHA.md** — Engine-to-Kosha layer mapping
- **KHA.md** §Doshas — Vedic clock integration
- **LHA.md** §Dasha — Vimshottari tracking
- **BHA.md** §Vikara — Gene-keys shadow work
- **VEDIC-LEXICON.md** — Canonical definitions used by engines
- **QUATERNION-BREATHWORK-PROTOCOL.md** — Vedic clock → breathwork translation

---

## 📡 Health & Monitoring

```bash
# Liveness (no auth)
curl https://selemene.tryambakam.space/health/live

# Readiness (no auth)
curl https://selemene.tryambakam.space/health/ready

# Prometheus metrics (no auth)
curl https://selemene.tryambakam.space/metrics
```

---

## ⚠️ Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Invalid/missing API key | Check NOESIS_API_KEY |
| 429 | Rate limited | Wait or upgrade tier |
| 500 | Calculation error | Check birth_data format |

---

*"The engine calculates. The witness integrates. Selemene illuminates the path."*
