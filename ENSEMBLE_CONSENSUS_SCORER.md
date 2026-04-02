# Ensemble Consensus Scorer — 4-System Combiner

## Architecture

After validating each system independently, combine them into a single consensus scorer that:
1. **Matches combos** by base layer (Condition × Round Type)
2. **Calculates agreement** across all 4 systems
3. **Weights by reliability** (inverse variance of ROI)
4. **Produces ensemble ROI** with conviction level

## Base Layer (Common to All Systems)

All combos are filtered to:
- **Tournament Type:** S (Standard Stroke Play only)
- **Round Type:** Open / Positioning / Closing (exclude REMOVE/Mixed/Elimination)
- **Condition:** Calm / Moderate / Tough

Example base combination: `(Calm, Closing)`

## System Dimensions (Unique per System)

| System | Dimension 1 | Dimension 2 | Dimension 3 |
|--------|------------|------------|------------|
| 1 | Color | Element (Wu Xing) | — |
| 2 | Exec Bucket | Upside Bucket | Gap Bucket |
| 3 | Moon Phase (Tithi) | Life Path | — |
| 4 | Tithi (day) | Chinese Zodiac | — |

## Matching Algorithm

For each base combination (e.g., `Calm + Closing`), find all combos across all systems:

```
System 1:  Calm + Closing + Yellow + Fire
System 2:  Calm + Closing + 50-75 + 50-75 + 0-10
System 3:  Calm + Closing + Shukla Purna + Life Path 7
System 4:  Calm + Closing + Day 15 + Rat
```

These are **4 independent systems** testing the same base condition, so they're orthogonal (no overlap).

## Agreement Scoring

For each base combination, count how many systems show **positive ROI**:

- **HIGH AGREEMENT (4/4):** All 4 systems positive
  - Conviction: Very High
  - Ensemble ROI: Average of 4 system ROIs
  - Action: **Strongest bet** (expect 6-8%+ ROI if sampled evenly)

- **MEDIUM AGREEMENT (3/4):** 3 systems positive, 1 negative
  - Conviction: Medium-High
  - Ensemble ROI: Weighted average (high-ROI systems weighted more)
  - Action: **Moderate bet** (expect 3-5% ROI)

- **WEAK AGREEMENT (2/4):** 2 positive, 2 negative
  - Conviction: Medium
  - Ensemble ROI: Weighted average (could be positive or negative)
  - Action: **Conditional** (depends on system reliabilities)

- **STRONG DISAGREEMENT (≤1/4):** 0-1 systems positive
  - Conviction: Low
  - Ensemble ROI: Likely negative
  - Action: **Skip or short** (expect negative ROI)

## Weighting Formula

For combining ROI estimates across systems, use **inverse variance weighting**:

```
ensemble_roi = sum(roi_i / σ_i²) / sum(1 / σ_i²)

where:
  roi_i = ROI from system i
  σ_i = standard deviation of ROI within system i (measure of noise/uncertainty)
```

Higher sample size → lower σ → higher weight.

**Alternative (simpler):** Weight by sample size only:
```
ensemble_roi = sum(roi_i × n_i) / sum(n_i)
```

## Implementation Steps

1. **Load all 4 system results:**
   - System 1: `combo_scoring_rce_all_combos.csv`
   - System 2: `system2_exec_upside_gap_ALL_combos.csv`
   - System 3: `system3_moon_lifepath_ALL_combos.csv`
   - System 4: `system4_tithi_zodiac_ALL_combos.csv`

2. **Group by base (Condition × Round Type):**
   ```
   for each (condition, round_type):
     system1_combos = filter by condition, round_type
     system2_combos = filter by condition, round_type
     system3_combos = filter by condition, round_type
     system4_combos = filter by condition, round_type
   ```

3. **For each base combination, calculate metrics:**
   ```
   positive_count = sum([
     (system1_roi > 0),
     (system2_mean_roi > 0),
     (system3_mean_roi > 0),
     (system4_mean_roi > 0)
   ])

   ensemble_roi = weighted_average([
     system1_roi,
     system2_mean_roi,
     system3_mean_roi,
     system4_mean_roi
   ])

   conviction = "HIGH" if positive_count == 4
             elif positive_count == 3 "MEDIUM"
             elif positive_count >= 2 "WEAK"
             else "LOW"
   ```

4. **Output consensus table:**
   - `condition`, `round_type`, `positive_count`, `ensemble_roi`, `conviction`, `recommendation`
   - Sort by ensemble_roi (descending)
   - Filter for conviction >= "MEDIUM" (2+ systems agree)

5. **Generate betting recommendations:**
   - HIGH/MEDIUM: Bet FOR at consensus ROI
   - WEAK: Conditional (size accordingly)
   - LOW: Avoid or use for shorts

## Expected Outcome

When all 4 systems agree on a base combination (HIGH conviction), expect:
- **Ensemble ROI:** 6-8%+ (if systems are independent and each ~2-3%)
- **Confidence:** Very high (multiple independent validation)
- **Action:** Primary betting targets

When 3/4 systems agree (MEDIUM conviction), expect:
- **Ensemble ROI:** 3-5%
- **Confidence:** High
- **Action:** Secondary targets

## Example Output Table

| Condition | Round Type | Sys1 ROI | Sys2 ROI | Sys3 ROI | Sys4 ROI | Consensus | Conviction |
|-----------|-----------|----------|----------|----------|----------|-----------|------------|
| Calm | Closing | +4.6% | +3.2% | +5.1% | +2.8% | +3.9% | HIGH (4/4) |
| Calm | Opening | +1.2% | +2.5% | -1.0% | +3.8% | +1.6% | MEDIUM (3/4) |
| Moderate | Positioning | -0.5% | -1.2% | +0.8% | -2.1% | -0.8% | LOW (1/4) |

---

## What's NOT in Ensemble

**Do NOT double-count dimensions:**
- Each system tests independent dimensions
- System 1 (Color + Element) ≠ System 2 (Exec + Upside)
- No overlap = clean orthogonal combination

**Do NOT combine within-system combos:**
- System 1 best combo: `Yellow × Fire`
- System 2 best combo: `75-100 exec × 75-100 upside`
- These are NOT combined; they're independently weighted

---

## Prerequisites

All 4 systems must be run first:
- [ ] System 1: ✓ Complete (results exist)
- [ ] System 2: Run `system2_exec_upside_gap_testing.py`
- [ ] System 3: Run `system3_moon_lifepath_testing.py`
- [ ] System 4: Run `system4_tithi_zodiac_testing.py`

Then build consensus with Python script:
```
python build_ensemble_consensus.py
```

Output:
- `ensemble_consensus_scorecard.csv` — Full results by base combo
- `ensemble_high_conviction.csv` — HIGH (4/4) + MEDIUM (3/4) agreement only
- `ensemble_betting_recommendations.md` — Actionable signals ranked by conviction
