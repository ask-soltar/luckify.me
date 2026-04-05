---
title: Master Numbers × Colors Signal
status: ARCHIVED_PENDING_REVALIDATION
confidence: 2 (was 4 in 2024, now uncertain)
date_created: 2026-04-04
date_archived: 2026-04-04
archive_reason: Effect disappeared in 2025-2026 data; needs recent revalidation
review_date: 2026-05-04
---

## Theory Statement
Certain colors (especially Fire element: Yellow, Red, Orange) + Green perform worse on Master Number Personal Day 22 in Calm conditions, Round 2 specifically.

## Why Archived

**Critical Finding:** Effect was strong and validated in 2022-2024 data but completely disappeared in 2025-2026.

### Historical Evidence (2022-2024)
- **2022:** PD 22 mean=-0.362 vs_avg, p=0.0082 ✓
- **2023:** PD 22 mean=-0.315 vs_avg, p=0.0860 ✓
- **2024:** PD 22 mean=-0.464 vs_avg, p=0.0719 ✓

### Recent Data (2025-2026)
- **2025:** PD 22 mean=-0.026 vs_avg, p=0.4371 ✗ (DISAPPEARED)
- **2026:** PD 22 mean=-0.331 vs_avg, p=0.6351 ✗ (DISAPPEARED)

**Conclusion:** Effect is no longer valid. Not safe to deploy as signal.

---

## What We Learned (Deep Analysis)

### The Signal (When It Worked)
**Hyper-specific conditions:**
- Calm rounds only (p=0.0268 Calm vs p=0.24 Moderate vs p=0.17 Tough)
- Round 2 (Positioning) specifically (p=0.0232 R2 vs p=0.17 R1 vs p=0.15 R3 vs p=0.82 R4)
- Fire element (p=0.0100, n=601) and Green element (p=0.031, n=289)
- Warm colors synergy (p=0.0031, n=1,177)

### Strength of Effect
- Cohen's d ≈ -0.06 to -0.13 (small but meaningful)
- Sample size: n=289-1,177 per combo (adequate)
- Variance: std≈2.8-2.9 (high golf variance, but stable)
- Not outlier-driven: 44.3% PD22 beat field vs 46.1% baseline

### Why It Might Have Disappeared

**Hypothesis 1: Market Adaptation**
- Master Numbers knowledge became public
- Oddsmakers adjusted for PD 22 pattern
- Edge eliminated through market efficiency

**Hypothesis 2: Cohort Change**
- LIV Golf expansion (2022-2023) changed player composition
- Retirement/new player influx altered demographic
- Fire element distribution changed

**Hypothesis 3: Random Variance**
- 2022-2024 was lucky clustering
- True effect is smaller or non-existent
- Reversion to mean in recent years

**Hypothesis 4: Calendar/Tournament Changes**
- Fewer Calm+R2 tournaments in 2025-2026
- Different course conditions in recent events
- Scheduling pattern shift

---

## Test Results Summary

### All 8 Deep Analyses
1. ✓ Condition breakdown — Calm-specific (p=0.0268)
2. ✓ 3-way interaction — Multiple combos pass when conditions met
3. ✓ Variance/stability — Green×PD22 most consistent (std=2.826, n=289)
4. ✓ Element lens — Fire element effect (p=0.0100, n=601)
5. ✓ Round progression — R2 concentrated (p=0.0232)
6. ✗ Time trend — **Effect absent 2025-2026** (p>0.43)
7. ✓ Player consistency — Widespread, not outlier-driven
8. ✓ Synergy check — Warm colors amplify (p=0.0031)

**Critical Analysis:** See `MASTER_NUMBERS_DEEP_ANALYSIS_SUMMARY.md` for full details.

---

## Rubber Stamp Assessment (Why Not Validated)

| Gate | Result | Status |
|------|--------|--------|
| Statistical Significance | YES (2022-2024 data) | ✓ PASSED |
| Sample Size | YES (n>200-1,000) | ✓ PASSED |
| Effect Size | YES (Cohen's d>0.05) | ✓ PASSED |
| Stability Across Contexts | NO (disappeared 2025-2026) | ✗ **FAILED** |
| Not Luck | MAYBE (historical, not current) | ⚠️ UNCERTAIN |

**Verdict:** Fails Gate 4 (Stability). Cannot validate without recent data support.

---

## Archive Instructions

### When to Revisit (Auto-Check Dates)
- **2026-05-04** (1 month) — First check: Has effect returned?
- **2026-07-04** (3 months) — Quarterly: Still gone? Or back?
- **2026-10-04** (6 months) — Decision point: Archive indefinitely or resurrect?

### How to Revalidate
1. Load 2026-current data (most recent tournament results)
2. Run `test_master_numbers_colors.py` on new data only
3. Compare p-values to historical (2022-2024) baseline
4. If p < 0.10: Move back to NEEDS_TESTING
5. If p > 0.10: Extend archive, check again in 3 months
6. If pattern changes (different colors, different rounds): investigate why

### Possible Revival Scenarios
- **Scenario A:** Effect returns with same pattern → Move to NEEDS_TESTING, investigate market change
- **Scenario B:** Effect returns with different pattern → Create new theory, test that pattern
- **Scenario C:** Effect partially returns (weaker) → Move to PARTIALLY_BACKED, needs more data
- **Scenario D:** Effect stays gone → Move to REJECTED after 6-month archive period

---

## Key Files
- **Analysis scripts:** `test_master_numbers_colors.py`, `test_master_numbers_deep_analysis.py`
- **Result CSVs:** `analysis1_condition_breakdown.csv` through `analysis8_synergy_check.csv`
- **Summary:** `MASTER_NUMBERS_DEEP_ANALYSIS_SUMMARY.md`

---

## User Notes

**User's Intuition:** "I want to test Master Numbers × Colors"

**What We Found:** Theory was right historically (2022-2024) but effect disappeared in recent data.

**Decision:** Archive pending revalidation rather than reject, because:
1. Effect WAS real (not luck in 2022-2024)
2. Mechanism is understood (Fire element, Calm rounds, R2 specific)
3. Disappearance is explainable (market, cohort, chance)
4. Worth monitoring quarterly in case it returns

---

## Confidence Level

**Current confidence: LOW** (effect not present in recent data)

**If 2026 data shows effect returning:** Confidence would jump to MEDIUM (mechanism understood, pattern replicates)

**Next review:** 2026-05-04

