# Tier 1 Validation Results: Orange Talent Equalizer Theory
**Date:** 2026-04-05
**Status:** OUT-OF-SAMPLE VALIDATION COMPLETE — Theory Rejected

---

## Executive Summary

The Orange "talent equalizer" pattern identified in 2022-2024 data **does not replicate** in 2025/2026 out-of-sample data. Tests 1A and 1B both failed validation thresholds.

---

## Test 1A: Quartile Analysis Results

**Sample:** 2,009 Orange + Stroke Play rounds (1,592 in 2025, 417 in 2026)

### Performance by Skill Tier

| Tier | n | adj_his_par Range | Mean vs_own_par | Beat Own % | Interpretation |
|---|---|---|---|---|---|
| Weakest 25% | 506 | -3.10 to -1.48 | +0.329 | 48.8% | Baseline underperformance |
| Weak 50% | 506 | -1.48 to -1.11 | -0.053 | 47.8% | Slightly beat own average |
| Elite 75% | 500 | -1.10 to -0.73 | +0.238 | 48.6% | Underperform own average |
| **Elite Top 25%** | 497 | -0.72 to +2.13 | **+0.282** | 47.9% | **Highest underperformance** |

### Pass/Fail Criteria

| Criterion | Expected | Actual | Pass? |
|---|---|---|---|
| Monotonic increase (weakest → elite) | Yes | NO — reversed | ✗ FAIL |
| Effect size (elite vs weak) | >0.15 strokes | -0.047 strokes | ✗ FAIL |
| Statistical significance | p < 0.05 | p = 0.8175 | ✗ FAIL |

**Verdict:** TEST 1A **FAILED** — Pattern does not hold

---

## Test 1B: Decile Analysis Results

Tested 10 skill tiers (deciles 1–10). **No monotonic trend** observed. Pattern is noisy:

- **Worst decile:** D10 (elite top 10%): +0.762 strokes underperformance
- **Best decile:** D9 (elite top 20%): -0.164 strokes (beats own average)
- **Regression (adj_his_par → vs_own_par):** R² = 0.0008, p = 0.214 (not significant)

**Verdict:** TEST 1B **FAILED** — No clean gradient across skill tiers

---

## Condition Breakdown

### Calm Conditions (n=1,285)
- Weakest: +0.456
- Elite Top 25%: +0.703
- Effect size: +0.247 (p = 0.3727, not significant)

### Moderate Conditions (n=668)
- Weakest: -0.162
- Elite Top 25%: +0.353
- Effect size: +0.515 (p = 0.1221, not significant)

### Tough Conditions (n=56, low power)
- Weakest: -0.389
- Elite Top 25%: +1.249
- Effect size: +1.639 (p = 0.1457, not significant due to low n)

**Note:** Even in Calm (expected peak), effect size is 0.247 with p > 0.05.

---

## Key Statistics

| Metric | Value |
|---|---|
| Total Orange rounds (2025/2026) | 2,010 |
| vs_own_par available | 2,009 |
| Year 2025 | 1,592 rounds |
| Year 2026 | 417 rounds |
| Regression slope (adj_his_par) | +0.154 (weak) |
| Regression R² | 0.0008 (explains 0.08% of variance) |
| Regression p-value | 0.214 (not significant) |

---

## Interpretation

The 2022-2024 finding that "Orange constrains elite players while liberating weak players" was either:

1. **Year/meta-specific:** 2025-2026 tournament dynamics differ from 2022-2024
2. **Statistical artifact:** Pattern emerged from data-dredging; doesn't generalize
3. **Context-dependent:** Effect only applies to subset of tournaments/conditions (but not robust enough to model)
4. **Reversed trend:** Orange dynamics have fundamentally changed

**The testing framework is working correctly.** Out-of-sample validation caught a signal that looked strong historically but fails forward-looking replication.

---

## Next Steps (Resume Tomorrow)

### Option A: Investigate Why Pattern Broke
- Analyze 2022-2024 vs 2025-2026 separately
- Check for tournament meta changes, field composition shifts
- Test for interaction effects (Orange × specific conditions/years)

### Option B: Accept Rejection, Move Forward
- Archive talent equalizer theory in REJECTED folder
- Focus validation on remaining archetypal signals (Moon phases, Condition combos)
- Use Tier 2-6 tests to stress-test other patterns

### Recommendation
**Option B** — The framework proved its value by catching this. Focus on signals that already passed 2025/2026 validation (orange_newmoon_calm, orange_newmoon, orange_calm from VALIDATED_SIGNALS.json). Those held; talent equalizer didn't.

---

## Files Generated
- `test_1a_1b_orange_talent_equalizer_2025_2026.py` — Full test script (reusable)
- This file: Results summary

## Resume Point
Morning work should pivot to:
1. Archive talent equalizer theory (VALIDATED_INSIGHTS/REJECTED/)
2. Run Tier 2 tests on signals that already validated (condition, round type, moon interactions)
3. Build depth on validated signals rather than chasing dead patterns
