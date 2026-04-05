# Color × Personal Day Combo Analysis — Executive Summary

**Analysis Date:** April 4, 2026
**Dataset:** 61,300 golf rounds (79.5% of 77,155 total records)
**Filters:** Calm/Moderate/Tough conditions, Open/Positioning/Closing/Survival round types, S/NS tournament types only

---

## Bottom Line

Personal Day **does NOT** meaningfully stabilize Color signals. While Color × Personal Day combos identify directions (beat/miss field average) with moderate consistency, **variance is extremely high (σ=2.9 avg)**, making individual combo predictions unreliable.

**Recommendation:** Use Color × Personal Day as a **conditioner** (secondary layer) to boost other signals, NOT as a primary standalone pick.

---

## Key Findings

### 1. By Color (Best to Worst)

| Color | Avg Beat % | Avg Std Dev | Interpretation |
|-------|-----------|------------|-----------------|
| Pink | 60.12% | 2.90 | Best direction signal, still erratic |
| Green | 54.97% | 2.94 | Solid baseline, unpredictable magnitude |
| Orange | 54.73% | 2.89 | Solid baseline, unpredictable magnitude |
| Purple | 54.56% | 2.94 | Near-baseline, unreliable |
| Red | 54.03% | 3.08 | Variable, high noise |
| Yellow | 53.98% | 2.93 | Variable, high noise |
| Blue | 53.32% | 2.98 | Below baseline, weak |
| Brown | 53.18% | 2.50 | Low sample size (91 rounds), below baseline |

**Insight:** Pink color is the only one consistently above 60% beat rate. All others cluster 53-55%, barely above 50% random threshold.

---

### 2. By Personal Day (Best to Worst)

| Personal Day | Avg Beat % | Avg Std Dev | Rounds | Interpretation |
|-------------|-----------|------------|--------|-----------------|
| **4** | **57.65%** | 2.89 | 4,603 | **STRONGEST** (consistent best) |
| **9** | **57.47%** | 3.00 | 6,798 | **STRONG** (consistent, high sample) |
| **3** | **56.50%** | 2.90 | 6,752 | **STRONG** (consistent, high sample) |
| **33** | **56.24%** | 2.62 | 1,450 | Modest sample size |
| **8** | **55.87%** | 3.02 | 6,826 | Moderate, high variance |
| **6** | **55.63%** | 2.74 | 5,351 | Moderate, stable std dev |
| **1** | **55.51%** | 3.28 | 6,765 | Moderate, high variance |
| **2** | **54.71%** | 2.99 | 4,822 | Slight advantage |
| **7** | **54.00%** | 2.91 | 6,837 | Baseline |
| **5** | **53.93%** | 2.90 | 6,905 | Baseline |
| **22** | **51.03%** | 2.92 | 2,191 | **WEAK** (below baseline) |
| **11** | **49.79%** | 2.57 | 2,000 | **WEAKEST** (below 50%, poor predictor) |

**Insight:** Personal Days 3, 4, 9 are consistent winners. Days 11 and 22 are consistent underperformers.

---

## Top Combos for Deployment

### Tier 1: STRONG SIGNALS (>62% beat rate, small samples)
- Brown × Day 6: 83% (6 rounds)
- Brown × Day 9: 78% (7 rounds)
- Pink × Day 33: 75% (8 rounds)

**Caveat:** Sample sizes are small (6-8 rounds). Expand with confidence only if validated on new data.

### Tier 2: MODERATE SIGNALS (58-62% beat rate)
- Brown × Day 4: 73% (8 rounds)
- Pink × Day 11: 70% (10 rounds)
- Pink × Day 2: 70% (23 rounds)
- Pink × Day 3: 68% (44 rounds)
- Pink × Day 7: 67% (52 rounds)
- Red × Day 4: 62% (138 rounds) ✓ Higher sample
- Red × Day 8: 59% (199 rounds) ✓ Higher sample

**Recommendation:** Tier 2 combos with 100+ rounds (Red × Day 4/8, Purple × Day 11) are more reliable.

---

## Combos to AVOID

### Red Flags (>5% underperformance vs 50%)
- **Red × Day 7:** 47% (89 rounds) — Direct weakness signal
- **Pink × Day 6:** 46% (26 rounds) — Unexpected pink underperformance
- **Brown × Day 2:** 40% (5 rounds) — Small sample, poor
- **Brown × Day 11:** 0% (1 round) — Avoid entirely

### Weak Baseline (51-52%, barely profitable)
- **Blue × Day 6:** 51% (535 rounds) — Large sample, no edge
- **Blue × Day 11:** 51% (203 rounds) — No edge
- **Red × Day 22/33:** 51-52% (21-38 rounds) — No edge

---

## Variance Analysis: Why Predictions Fail

### High Erratic Distribution (93 of 96 combos)

| Stability | Count | Meaning |
|-----------|-------|---------|
| Rock Solid (σ < 0.5) | 1 | Nearly impossible to achieve |
| Consistent (σ < 0.8) | 0 | None found |
| Moderate (σ < 1.2) | 0 | None found |
| Volatile (σ < 1.6) | 2 | Rare; Brown × Day 6, Brown × Day 5 |
| Erratic (σ ≥ 1.6) | 93 | **Dominant pattern** |

**Why:** Personal Day acts as a direction indicator (beat/miss field avg) but not a magnitude predictor. Rounds that beat field avg do so by -0.5 to -3.0 strokes; rounds that miss do so by +0.2 to +4.3 strokes. This large spread (±2.9 std dev) makes sizing/confidence intervals unreliable.

---

## How to Use in Betting Framework

### Option A: Conditioner (RECOMMENDED)
1. Identify primary signal (e.g., Color × Condition = Green × Calm = +5.9% edge)
2. Check player's Personal Day from the Tier 2 list (Days 3, 4, 9)
3. If match: Apply 1.1x Kelly multiplier (boost confidence)
4. If mismatch (e.g., Day 11): Apply 0.9x Kelly multiplier (reduce confidence)

### Option B: Standalone (NOT RECOMMENDED)
- Combos with >60% beat rate and 100+ samples only (Red × Day 4, Red × Day 8, Purple × Day 11)
- Use as weak secondary signal, never primary
- Require 1.2x Kelly minimum to justify

### Option C: Filtering (SAFER)
- Exclude players on Personal Days 11, 22 (consistent underperformers)
- Boost confidence for Days 3, 4, 9

---

## Quality Assessment

| Question | Answer |
|----------|--------|
| Is Personal Day a strong standalone signal? | **No** (53-58% typical, high variance) |
| Does Personal Day improve Color stability? | **No** (still erratic, σ~2.9) |
| Can we predict magnitude (not just direction)? | **No** (std dev too high) |
| Is this useful as a conditioner? | **Maybe** (Days 3,4,9 show +4% advantage vs Days 11,22) |
| Sample size sufficient? | **Partially** (96 combos, but 50 combos <20 rounds) |

**Conclusion:** Personal Day is a **weak secondary signal**, useful only as a confidence modifier in a larger framework.

---

## Next Steps

1. **Cross-validation:** Test Color × Personal Day on 2024-2025 tournaments (out-of-sample)
2. **Interaction effects:** Analyze Color × Personal Day × Round Type (e.g., Pink × Day 2 × Closing)
3. **Ensemble:** Combine with Color × Condition + Moon Phase for richer model
4. **Sample expansion:** Monitor as 2025-2026 season progresses; some combos (Brown × Day 6) need more rounds to stabilize

---

## Files Generated

| File | Purpose |
|------|---------|
| `color_personalday_combos_corrected.csv` | Full 96-combo ranked table with all metrics |
| `color_personalday_pivot.csv` | Color × Day pivot table (heat map format) |
| `COLOR_PERSONALDAY_ANALYSIS_CORRECTED.md` | Detailed technical analysis |
| `COLOR_PERSONALDAY_EXECUTIVE_SUMMARY.md` | This document |

---

## Quick Reference: Top Picks

**USE THESE (>60% beat rate):**
- Brown × Day 6 (83%)
- Brown × Day 9 (78%)
- Pink × Day 33 (75%)
- Brown × Day 4 (73%)
- Pink × Day 11 (70%)

**AVOID THESE (<48% beat rate or 0%):**
- Red × Day 7 (47%)
- Pink × Day 6 (46%)
- Brown × Day 11 (0%)

**NEUTRAL (51-52%, no edge):**
- Blue × Day 6, Blue × Day 11
- Red × Days 22, 33

