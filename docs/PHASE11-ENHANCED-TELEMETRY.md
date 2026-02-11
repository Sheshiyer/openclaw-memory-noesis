# Phase 11: Enhanced Telemetry (Antahkarana Protocol)

**Generated:** 2026-02-11  
**Source:** Architecture docs from `/01-Projects/tryambakam-noesis/architecture/`  
**Planner:** task-master-planner skill

---

## 🎯 Objective

Implement remaining telemetry features from architecture specs:
- Clifford Clock (8-hour consciousness octave)
- 13 Engine States with load tracking
- Ritual/Cron Tracking with Vayu mapping
- Polarity Balance (Aletheios ↔ Pichet)
- Thought Process emissions (>5s reasoning)

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 35 |
| Total Hours | ~200 |
| Sprints | 5 |
| Duration | 5 weeks |

### New CLI Commands
```bash
noesis clock      # Clifford hour + phase
noesis moon       # Selemene moon phase
noesis engines    # 13 engine states
noesis rituals    # Cron job tracking
noesis polarity   # Aletheios/Pichet balance
noesis status     # Unified dashboard
```

### New Emitters
```python
emit_thought_process(summary, depth_level, duration_ms)
emit_engine_state(engine_num, load, active)
emit_ritual(job_id, name, status, vayu)
emit_polarity(aletheios_pct, pichet_pct)
```

---

## 🗓️ Sprint Breakdown

### Sprint 1: Clifford Clock & Temporal Awareness (Week 1)
| ID | Task | Hours |
|----|------|-------|
| P11-S1-01 | Add Clifford Clock schema to SQLite | 4 |
| P11-S1-02 | Implement `get_clifford_hour()` function | 6 |
| P11-S1-03 | Add `noesis clock` CLI command | 4 |
| P11-S1-04 | Integrate Clifford hour into telemetry events | 4 |
| P11-S1-05 | Add Selemene moon phase integration | 8 |
| P11-S1-06 | Add `noesis moon` CLI command | 4 |
| P11-S1-07 | Update TUI header with Clifford Clock | 6 |

**Sprint Hours:** 36

---

### Sprint 2: 13 Engine States & Load Tracking (Week 2)
| ID | Task | Hours |
|----|------|-------|
| P11-S2-01 | Add engine_states table to SQLite schema | 4 |
| P11-S2-02 | Create Engine enum and metadata | 6 |
| P11-S2-03 | Implement `emit_engine_state()` function | 6 |
| P11-S2-04 | Add `noesis engines` CLI command | 6 |
| P11-S2-05 | Add engine panel to TUI dashboard | 8 |
| P11-S2-06 | Auto-detect engine usage from event types | 8 |

**Sprint Hours:** 38

---

### Sprint 3: Ritual/Cron Tracking & Polarity Balance (Week 3)
| ID | Task | Hours |
|----|------|-------|
| P11-S3-01 | Add rituals table to SQLite schema | 4 |
| P11-S3-02 | Create Vayu enum (5 types) | 4 |
| P11-S3-03 | Implement `emit_ritual()` function | 6 |
| P11-S3-04 | Add `noesis rituals` CLI command | 6 |
| P11-S3-05 | Add polarity tracking to session_metrics | 4 |
| P11-S3-06 | Implement `emit_polarity()` function | 6 |
| P11-S3-07 | Add `noesis polarity` CLI command | 4 |
| P11-S3-08 | Add polarity indicator to TUI | 6 |

**Sprint Hours:** 40

---

### Sprint 4: Thought Process & Vikara Enhancements (Week 4)
| ID | Task | Hours |
|----|------|-------|
| P11-S4-01 | Implement `emit_thought_process()` for long reasoning | 6 |
| P11-S4-02 | Add thinking indicator to TUI stream | 6 |
| P11-S4-03 | Enhance Vikara detection with protocol checks | 8 |
| P11-S4-04 | Add Vikara jitter effect to TUI | 6 |
| P11-S4-05 | Implement Khalorēē scoring rules from protocol | 6 |
| P11-S4-06 | Add `noesis status` unified dashboard command | 8 |

**Sprint Hours:** 40

---

### Sprint 5: Integration, Testing & Documentation (Week 5)
| ID | Task | Hours |
|----|------|-------|
| P11-S5-01 | Create integration tests for all new emitters | 8 |
| P11-S5-02 | Add end-to-end TUI test scenarios | 6 |
| P11-S5-03 | Write TELEMETRY.md documentation | 8 |
| P11-S5-04 | Update README with Phase 11 features | 4 |
| P11-S5-05 | Create ASCII art diagram of telemetry architecture | 4 |
| P11-S5-06 | Performance benchmark telemetry overhead | 6 |
| P11-S5-07 | Final integration and release (v0.2.0) | 4 |

**Sprint Hours:** 40

---

## 🏗️ Schema Additions

### clifford_state
```sql
CREATE TABLE clifford_state (
    id INTEGER PRIMARY KEY,
    timestamp TEXT NOT NULL,
    hour INTEGER NOT NULL,        -- 0-7
    phase TEXT NOT NULL,          -- ascent|plateau|dissolution
    octave_start TEXT NOT NULL,   -- UTC timestamp of current octave
    session_id TEXT
);
```

### engine_states
```sql
CREATE TABLE engine_states (
    engine_number INTEGER PRIMARY KEY,  -- 1-13
    name TEXT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    current_load INTEGER DEFAULT 0,     -- 0-100
    last_active TEXT,
    kosha_layer TEXT,
    color TEXT
);
```

### rituals
```sql
CREATE TABLE rituals (
    job_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    schedule TEXT NOT NULL,        -- cron expression
    last_run TEXT,
    status TEXT DEFAULT 'pending', -- pending|success|failed
    vayu TEXT,                     -- prana|apana|samana|udana|vyana
    duration_ms INTEGER
);
```

### session_metrics (additions)
```sql
ALTER TABLE sessions ADD COLUMN aletheios_pct INTEGER DEFAULT 50;
ALTER TABLE sessions ADD COLUMN pichet_pct INTEGER DEFAULT 50;
ALTER TABLE sessions ADD COLUMN clifford_hour INTEGER;
```

---

## 🎨 TUI Enhancements

### Header Bar
```
┌─────────────────────── PRANA STREAM ───────────────────────┐
│ 🕰️ Hour 3/7 (Ascent) │ 🌙 Waxing Gibbous │ Session: abc123 │
├────────────────────────────────────────────────────────────┤
```

### Engine Panel
```
┌─────── 13 ENGINES ────────┐
│ 01 Personal OS    [████░░] │
│ 03 Chitta        [██████] │
│ 05 Selemene      [███░░░] │
│ 12 Unified Field [░░░░░░] │
└───────────────────────────┘
```

### Polarity Gauge
```
┌────── POLARITY ──────┐
│ ☯️ Aletheios ←───→ Pichet │
│   [████████░░░░░░░░]    │
│      62%  ←→  38%       │
└───────────────────────┘
```

---

## ⚠️ Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Selemene API rate limits | Cache moon phase for 1 hour |
| Clifford timezone handling | Store all times in UTC, convert at display |
| Engine state complexity | Start with manual emit, add auto-detect later |
| Polarity subjectivity | Define clear rules for Aletheios/Pichet shifts |

---

## ✅ Success Criteria

1. `noesis clock` shows current Clifford hour with ASCII visualization
2. `noesis engines` displays all 13 engine states with load bars
3. `noesis status` provides single-view system dashboard
4. TUI watch shows live updates for clock, engines, polarity
5. Vikara auto-detected for Moha (3 failures), Mada, Kama (>100k tokens)
6. Khalorēē scoring follows protocol (+10 archive, -5 synthesis, +2 protocol)
7. Version 0.2.0 released with all features documented

---

*Generated via task-master-planner skill from Antahkarana architecture specs*
