---
title: Master Numbers × Colors Signal
status: LIVE_THEORY
confidence: 1
date_created: 2026-04-04
last_updated: 2026-04-04
---

## Theory Statement
Certain colors perform distinctly better or worse on Master Number Personal Days (11, 22, 33) compared to non-master days.

## Origin
User intuition + numerology + color rhythm theory (Master Numbers are amplified, should interact with color archetypal energies).

## Reasoning
Master Numbers (11, 22, 33) represent heightened numerological power. Should amplify color effects:
- Some colors thrive under Master amplification
- Some colors struggle under Master amplification
- Effect should be measurable in vs_avg performance

## Test Plan

### Data Source
Golf Historics v3 - ANALYSIS (8)
All years

### Filters Applied
- **Tournament type:** S (Standard Stroke Play) + NS (Non-Standard Stroke Play) only
- **Course condition:** Calm, Moderate, Tough (must be one of these three)
- **Round types included:** Open, Positioning, Closing, Survival

### Group Definitions
- **Master Number days:** PD 11, PD 22, PD 33 (separate)
- **Baseline:** All other personal days (PD 1-9, excluding master numbers)
- **Colors:** All 8 colors (Pink, Orange, Blue, Yellow, Green, Purple, Red, Brown)

### Metrics
- **vs_avg** (score vs. venue field average)
- **Sample size** (n per group)
- **Variance** (std dev per group)
- **Count by round type** (Open, Positioning, Closing, Survival)

### Analysis Structure

**Level 1: Master Numbers Overall**
```
PD 11 vs Baseline: mean vs_avg, n, std
PD 22 vs Baseline: mean vs_avg, n, std
PD 33 vs Baseline: mean vs_avg, n, std
```

**Level 2: By Color (8 × 3 = 24 combinations)**
```
Pink × PD 11: vs_avg, n, std
Pink × PD 22: vs_avg, n, std
Pink × PD 33: vs_avg, n, std
[... repeat for Orange, Blue, Yellow, Green, Purple, Red, Brown]
```

**Level 3: By Round Type**
```
For each round type (Open, Positioning, Closing, Survival):
  PD 11 vs Baseline: vs_avg, n, std
  PD 22 vs Baseline: vs_avg, n, std
  PD 33 vs Baseline: vs_avg, n, std
  [For strongest color × master combos: break down by color]
```

### Statistical Tests

**For each group comparison (e.g., Pink × PD 22 vs Baseline):**
- **t-test:** Do means differ significantly?
- **p-value:** Probability effect is random chance
- **Cohen's d:** Magnitude of effect (small/medium/large)
- **95% CI:** Confidence interval on difference

### Passing Thresholds (Flexible, noting sample size/variance)

| Gate | Threshold | Notes |
|------|-----------|-------|
| **Statistical Significance** | p < 0.10 | Exploratory; master numbers are specialized |
| **Sample Size** | n ≥ 30 per group | Flag if n < 50; note as "small sample" |
| **Effect Size** | Cohen's d ≥ 0.2 OR vs_avg diff ≥ ±0.10 | Small but meaningful |
| **Variance** | Report std dev; note if σ > 1.0 | High variance = less confident in effect |
| **Round Type Stability** | Effect appears in ≥2 round types | Shows it's not context-dependent |

**Special note on sample size/variance:**
- If n < 30 in any group: Flag as "exploratory only"
- If std > 1.0: Flag as "high variance; effect may be unreliable"
- If both: Mark as "interesting pattern, needs validation with more data"

## Execution

### Script to Write
`test_master_numbers_colors.py` — Reads ANALYSIS (8), tests all combinations

### Expected Output
- Master numbers overall summary (PD 11, 22, 33 vs baseline)
- Color × Master breakdown (24 combinations with stats)
- Round type stratification (Open, Positioning, Closing, Survival)
- CSV export: All test results with p-values, effect sizes, sample sizes, variances
- Report: Which combos pass gates? Which are interesting but underpowered?

### Expected Time
1-2 hours (includes writing script, running analysis, documenting results)

## Key Questions to Answer

1. Do Master Numbers (11, 22, 33) show different performance baseline than other days?
2. Which colors (if any) amplify under Master Number days?
3. Which colors (if any) struggle under Master Number days?
4. Is the effect consistent across round types?
5. Are sample sizes adequate for confidence, or do we need more data?

## Next Steps
- [ ] User approves test plan (this file)
- [ ] Claude writes `test_master_numbers_colors.py`
- [ ] Claude runs test on ANALYSIS (8)
- [ ] Results reviewed
- [ ] File moves to NEEDS_TESTING → analysis runs → VALIDATED/PARTIALLY_BACKED/REJECTED

