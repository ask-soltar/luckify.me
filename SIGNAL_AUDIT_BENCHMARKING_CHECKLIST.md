# Signal Audit: Revalidate Against New Benchmarking Standards
**Date:** 2026-04-05
**Status:** CHECKLIST FOR EXECUTION
**Standard:** See BENCHMARKING_STANDARDS.md

---

## Overview

New benchmarking standard introduced: **vs_avg < -2** (beat field by 2+ strokes) as primary threshold.

This affects all past signals. Each must be revalidated or marked as "deprecated."

---

## Signals to Audit

### From VALIDATED_SIGNALS.json (6 Signals)

**Status:** REVALIDATED ✓ (completed in Tier 3C test)

- [x] orange_fullmoon_calm → 39.0% beat by 2+ ✓ VALID
- [x] orange_newmoon_calm → 35.5% beat by 2+ ✓ VALID
- [x] orange_newmoon → 35.5% beat by 2+ ✓ VALID
- [x] orange_calm → 29.4% beat by 2+ ✓ VALID
- [x] orange_waxing_calm → 30.0% beat by 2+ ✓ VALID
- [x] libra_horoscope (FADE) → 32.1% lose by 2+ ✓ VALID

**Action:** Replace VALIDATED_SIGNALS.json with v2 (new benchmarks)

---

### From VALIDATED_INSIGHTS/VALIDATED/ (1 Signal)

**Status:** PENDING REVALIDATION

| Signal | Current Metric | Needs Retest? | Action |
|---|---|---|---|
| Exec × Color × Element/Round | Unknown (not checked) | YES | Rerun analysis with vs_avg < -2 |

---

### From Memory: Personal Year 7 Tournament Signal

**Current status:** +32.5% excess in top-10 finishers

**Current metric:** Chi-square on placement distribution (non-vs_avg metric)

**Question:** Is this compatible with new benchmarking standard?

**Action needed:**
1. Define what this signal actually measures (placement vs vs_avg?)
2. If placement-based, keep separate framework (not golf round performance)
3. If vs_avg-based, revalidate with vs_avg < -2

---

## Revalidation Process

### For Each Signal:

**Step 1: Identify metric**
```
What is this signal measuring?
- vs_avg (golf round performance)?
- Tournament placement (meta-outcome)?
- Something else?
```

**Step 2: Check compatibility**
```
Can this signal use vs_avg < -2 threshold?
- YES: Proceed to Step 3
- NO: Create separate "non-round-metric" framework
- UNKNOWN: Research first
```

**Step 3: Run analysis**
```
Test against new benchmark:
- Threshold: vs_avg < -2 (or appropriate equivalent)
- Calculate: beat_field_pct, n, p-value, effect size
- Check all 4 gates (n ≥ 50, beat% > 25%, p < 0.05, effect ≥ 0.15)
```

**Step 4: Document**
```
Update signal file with:
- New metric
- New threshold
- New results (beat%, n, p, effect)
- Status: REVALIDATED or DEPRECATED
```

---

## Signals by Category

### Category A: Golf Round Performance (vs_avg-based)

**Use standard:** vs_avg < -2

**Signals in this category:**
- orange_fullmoon_calm ✓ (revalidated)
- orange_newmoon_calm ✓ (revalidated)
- orange_newmoon ✓ (revalidated)
- orange_calm ✓ (revalidated)
- orange_waxing_calm ✓ (revalidated)
- libra_horoscope ✓ (revalidated)
- exec_color_element_round (pending)

---

### Category B: Tournament Placement (meta-outcome)

**Use standard:** TBD (need separate framework)

**Signals in this category:**
- personal_year_7_tournament (pending classification)

**Why separate:** Tournament placement is determined by 4 rounds of golf. Signal is about statistical tendency (chi-square on final results), not individual round performance.

**Possible thresholds:**
- % of tournament finishers hitting signal
- Excess rate vs population baseline
- Top-10 placement rate

---

### Category C: Other (Divination, Numerology, etc.)

**Status:** None yet defined

**Future work:** Define benchmarks for non-performance signals (e.g., numerology, astrology, etc.)

---

## Immediate Actions (Today)

### Priority 1: Lock In Core Signals
- [ ] Replace VALIDATED_SIGNALS.json with v2 (new benchmarks) ✓
- [ ] Update BENCHMARKING_STANDARDS.md (lock in universal metrics) ✓
- [ ] Deploy updated signals with screener

### Priority 2: Audit Other Validated Signals
- [ ] Revalidate exec_color_element_round signals (need data pull)
- [ ] Classify personal_year_7_tournament (vs_avg-based or placement-based?)
- [ ] If vs_avg: revalidate with < -2 threshold

### Priority 3: Update Documentation
- [ ] Update TIER2_DEPLOYMENT_GUIDE.md to reference new thresholds
- [ ] Update screener Kelly sizing for new beat% values
- [ ] Create signal migration guide (old vs new metrics)

---

## Results of Revalidation

### Completed (6 signals)

| Signal | Beat % (Old) | Beat % (New) | Status | Confidence |
|---|---|---|---|---|
| orange_fullmoon_calm | 78.0% | 39.0% | VALID | HIGH (n=82) |
| orange_newmoon_calm | 64.5% | 35.5% | VALID | MODERATE (n=76) |
| orange_newmoon | 64.5% | 35.5% | VALID | MODERATE (n=76) |
| orange_calm | 56.8% | 29.4% | VALID | VERY HIGH (n=1372) |
| orange_waxing_calm | 56.3% | 30.0% | VALID | HIGH (n=781) |
| libra_horoscope | 45.7% | 32.1% (FADE) | VALID | HIGH (n=683) |

**All 6 signals remain valid under new benchmark.**

---

## Pending (To Be Investigated)

### Exec × Color × Element/Round Signals
**File:** `/VALIDATED_INSIGHTS/VALIDATED/exec_color_element_round_signals_20260405.md`

**Known:**
- 7 combos with varying effects
- Effect sizes: +0.876 to -0.707 vs_avg
- 68.8% replication rate

**To revalidate:**
1. Pull 2025/2026 data for each combo
2. Test using vs_avg < -2 threshold
3. Calculate beat_field_pct for each
4. Check if passes 4 gates
5. Update file with results

---

### Personal Year 7 Tournament Signal
**File:** `personal_year_tournament_signal.md` (in memory)

**Known:**
- +32.5% excess in top-10 finishers (2022-2024)
- Chi-square p < 0.05
- 94 total finishers in Year 7

**To investigate:**
1. Does this measure vs_avg or placement?
2. If vs_avg: Can we retest with < -2 threshold?
3. If placement: Create separate benchmarking framework
4. Either way: Revalidate on 2025-2026 data

---

## Summary

**Locked signals:** 6 (orange_calm family + libra_horoscope)
**Signals needing audit:** 2 (exec signals, personal year signal)
**Total signals:** 8

**Next step:** Audit pending signals, then all 8 are production-ready.

