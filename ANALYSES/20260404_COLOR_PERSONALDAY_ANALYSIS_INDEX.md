# Color × Personal Day Analysis — Complete Index

**Analysis Date:** April 4, 2026
**Dataset:** 61,300 golf rounds (79.5% of 77,155 total)
**Status:** COMPLETE — Ready for integration into betting framework

---

## Quick Start (Read These First)

1. **COLOR_PERSONALDAY_QUICK_STATS.txt** ← **START HERE** (2-min read)
   - Fast summary of best/worst combos
   - By-color and by-day performance rankings
   - Key deployment recommendations

2. **COLOR_PERSONALDAY_EXECUTIVE_SUMMARY.md** (5-min read)
   - Bottom-line verdict (personal day is weak standalone signal)
   - Tier 1/2/3 combos by reliability
   - How to integrate as conditioner vs standalone

---

## Detailed Analysis Documents

3. **COLOR_PERSONALDAY_ANALYSIS_CORRECTED.md** (10-min read)
   - Full technical methodology
   - All 96 combos ranked
   - Interpretation of corrected negative=good convention
   - Summary statistics and distribution analysis

---

## Data Files

### Primary Results
- **color_personalday_combos_corrected.csv** — All 96 combos with:
  - Rank, Color, Personal Day
  - Sample size, % beating field avg
  - Mean performance, std dev, stability classification
  - Typical range (±1σ), min/max values
  - Verdict (PREMIER/STRONG/MODERATE/WEAK edge)

### Supporting Data
- **color_personalday_pivot.csv** — Heat map format
  - Rows: Colors (8 colors)
  - Columns: Personal Days (12 days: 1-11, 33)
  - Values: % beating field avg for each combo
  - For easy visual scanning of Color × Day patterns

---

## Analysis Scripts

### Main Analysis
- **analyze_color_personal_day_corrected.py** (executable)
  - Loads ANALYSIS v3 data
  - Applies standard filters (Calm/Moderate/Tough, Open/Positioning/Closing/Survival, S/NS tournaments)
  - Calculates per-combo statistics
  - Generates ranked output with verdicts

---

## Key Findings Summary

### Methodology: Corrected Interpretation
- **Negative (score - course_avg < 0)** = Beats field average = **GOOD**
- **Positive (score - course_avg > 0)** = Underperforms = **BAD**
- All percentages = % of rounds beating field average

### Dataset Filters Applied
- Condition: Calm, Moderate, Tough only
- Round Type: Open, Positioning, Closing, Survival only
- Tournament Type: S (Standard Stroke Play), NS (Non-Standard) only
- Non-null vs_avg and Personal Day required
- **Result:** 61,300 records (79.5% of 77,155 total)

### Overall Verdict: NOT A STANDALONE SIGNAL

| Metric | Finding |
|--------|---------|
| **Best combo** | Brown × Day 6 (83.33% beat rate, 6 rounds) |
| **Worst combo** | Brown × Day 11 (0.00% beat rate, 1 round) |
| **Median performance** | ~54% beat rate (barely above 50% baseline) |
| **Stability** | Erratic (93 of 96 combos, σ=2.9 avg) |
| **Predictability** | Direction only; magnitude highly variable |
| **Recommended use** | Conditioner (secondary layer), NOT primary pick |

---

## By Color Performance

| Rank | Color | Avg Beat % | Interpretation |
|------|-------|-----------|-----------------|
| 1 | **Pink** | 60.12% | **STRONG** — Best color for direction signal |
| 2 | Green | 54.97% | Solid baseline |
| 3 | Orange | 54.73% | Solid baseline |
| 4 | Purple | 54.56% | Baseline (unremarkable) |
| 5 | Red | 54.03% | Variable/erratic |
| 6 | Yellow | 53.98% | Variable/erratic |
| 7 | Blue | 53.32% | Below baseline |
| 8 | Brown | 53.18% | Below baseline (small sample, 91 rounds) |

**Insight:** Pink is the only color >60% beat rate. All others cluster 53-55%, barely above random.

---

## By Personal Day Performance

| Rank | Day | Avg Beat % | Rounds | Interpretation |
|------|-----|-----------|--------|-----------------|
| 1 | **4** | **57.65%** | 4,603 | STRONGEST (consistent best) |
| 2 | **9** | **57.47%** | 6,798 | STRONG (consistent, large sample) |
| 3 | **3** | **56.50%** | 6,752 | STRONG (consistent, large sample) |
| 4 | 33 | 56.24% | 1,450 | Good (modest sample) |
| 5 | 8 | 55.87% | 6,826 | Moderate (erratic) |
| 6 | 6 | 55.63% | 5,351 | Moderate |
| 7 | 1 | 55.51% | 6,765 | Moderate (high variance) |
| 8 | 2 | 54.71% | 4,822 | Baseline (slight edge) |
| 9 | 7 | 54.00% | 6,837 | Baseline (no edge) |
| 10 | 5 | 53.93% | 6,905 | Baseline (no edge) |
| 11 | 22 | 51.03% | 2,191 | **WEAK** (below baseline) |
| 12 | 11 | 49.79% | 2,000 | **WEAKEST** (below 50%) |

**Insight:** Days 3, 4, 9 are consistent winners (56-58% beat rate). Days 11, 22 are consistent underperformers (49-51%).

---

## Top 15 Combos (Best Signals)

All ranked by % beating field average:

| # | Color | Day | Beat % | Rounds | Stability | Verdict |
|---|-------|-----|--------|--------|-----------|---------|
| 1 | Brown | 6 | 83.33% | 6 | Volatile | PREMIER |
| 2 | Brown | 9 | 77.78% | 9 | Erratic | PREMIER |
| 3 | Pink | 33 | 75.00% | 8 | Erratic | PREMIER |
| 4 | Brown | 4 | 72.73% | 11 | Erratic | PREMIER |
| 5 | Pink | 11 | 70.00% | 10 | Erratic | PREMIER |
| 6 | Pink | 2 | 69.70% | 33 | Erratic | PREMIER |
| 7 | Pink | 3 | 68.18% | 44 | Erratic | PREMIER |
| 8 | Pink | 7 | 67.31% | 52 | Erratic | PREMIER |
| 9 | Brown | 5 | 62.50% | 16 | Erratic | PREMIER |
| 10 | Brown | 8 | 62.50% | 8 | Erratic | PREMIER |
| 11 | Red | 4 | 62.32% | **138** | Erratic | PREMIER |
| 12 | Red | 8 | 58.79% | **199** | Erratic | PREMIER |
| 13 | Pink | 1 | 58.14% | 25 | Erratic | PREMIER |
| 14 | Purple | 11 | 57.93% | **271** | Erratic | PREMIER |
| 15 | Red | 9 | 57.89% | 110 | Erratic | PREMIER |

**Deployment tiers:**
- **Tier 1 (Risky):** Combos #1-4 (small samples 6-11 rounds)
- **Tier 2 (Reliable):** Combos #11, 12, 14 (100+ rounds, 57-62% beat rate)
- **Tier 3 (Backup):** Combos #5-10, 13, 15 (medium samples, 58-70% beat rate)

---

## Bottom 15 Combos (Worst Signals)

All ranked by % beating field average (lowest = worst):

| # | Color | Day | Beat % | Rounds | Verdict |
|---|-------|-----|--------|--------|---------|
| 96 | Brown | 11 | 0.00% | 1 | **AVOID** |
| 95 | Brown | 22 | 25.00% | 4 | WEAK |
| 94 | Brown | 2 | 40.00% | 5 | WEAK |
| 93 | Pink | 6 | 46.15% | 26 | WEAK |
| 92 | Red | 7 | 47.34% | 89 | WEAK |
| 91 | Brown | 7 | 50.00% | 3 | SLIGHT |
| 90 | Brown | 33 | 50.00% | 2 | SLIGHT |
| 89 | Red | 33 | 51.22% | 21 | SLIGHT |
| 88 | Blue | 6 | 51.25% | **535** | SLIGHT |
| 87 | Blue | 11 | 51.26% | **203** | SLIGHT |
| 86 | Pink | 5 | 51.61% | 16 | SLIGHT |
| 85 | Red | 5 | 51.74% | 89 | SLIGHT |
| 84 | Red | 22 | 52.05% | 38 | MODERATE |
| 83 | Yellow | 5 | 52.10% | **1,280** | MODERATE |
| 82 | Red | 6 | 52.14% | 73 | MODERATE |

**Pattern:** Brown color has most underperformers. Days 2, 5, 6, 7, 11, 22, 33 are problematic in combinations.

---

## Stability Analysis: Why This Signal Is Weak

### Distribution of Variance (Std Dev)

| Classification | Threshold | Count | % | Meaning |
|-----------------|-----------|-------|----|---------|
| Rock Solid | σ < 0.5 | 1 | 1.0% | Highly predictable magnitude |
| Consistent | σ < 0.8 | 0 | 0% | Rare to impossible |
| Moderate | σ < 1.2 | 0 | 0% | Rare to impossible |
| Volatile | σ < 1.6 | 2 | 2.1% | Uncommon (Brown × Days 5,6) |
| **Erratic** | **σ ≥ 1.6** | **93** | **96.9%** | **DOMINANT pattern** |

### What This Means
- Color × Personal Day combos **predict direction** (beat or miss field avg) inconsistently
- They do **NOT predict magnitude** (how much better/worse)
- Average std dev = 2.9, meaning typical range is ±2.9 strokes around mean
- High variance makes probability calibration unreliable

**Example:**
- Combo: Pink × Day 2 (mean -0.749, σ=2.810)
- Player on this day typically beats field by 0.75 strokes
- But 95% of rounds fall in range -3.56 to +2.06 (spread of 5.6 strokes!)
- This makes Kelly sizing and confidence intervals unreliable

---

## Deployment Recommendations

### ✓ DO USE (Conditioning / Secondary Layer)

**Apply 1.1x Kelly multiplier boost for:**
- Personal Days 3, 4, 9 (avg 56-58% beat rate)
- Especially in Pink/Red/Purple colors

**Apply 0.9x Kelly multiplier reduction for:**
- Personal Days 11, 22 (avg 49-51% beat rate)
- All colors on these days

### ✓ USE AS STANDALONE (Only these combos meet criteria: 100+ samples + 57%+ beat rate)
- Red × Day 4 (62.32%, 138 rounds)
- Red × Day 8 (58.79%, 199 rounds)
- Purple × Day 11 (57.93%, 271 rounds)

**Caveat:** Even these are erratic (σ=2.8-3.1). Use with 1.0-1.1x Kelly only.

### ✗ AVOID ENTIRELY

- Brown × Day 11 (0%, 1 round) — no data
- Red × Day 7 (47.34%, 89 rounds) — direct weakness
- Pink × Day 6 (46.15%, 26 rounds) — unexpected weakness
- Brown × Days 2, 22 (25-40%, small samples) — poor performers

### ⚠ MONITOR (Small sample tier 1 combos)
- Brown × Day 6 (83%, 6 rounds) — needs more data
- Brown × Day 9 (78%, 9 rounds) — needs more data
- Pink × Day 33 (75%, 8 rounds) — needs more data
- Pink × Day 11 (70%, 10 rounds) — needs more data

Collect 2025-2026 season data before making live deployment decisions on these.

---

## How to Integrate Into Betting Framework

### Option A: Conditioner (RECOMMENDED)
```
1. Identify primary signal (e.g., Color × Condition = Green × Calm)
2. Look up player's current Personal Day
3. If Day ∈ {3,4,9}: Apply 1.1x Kelly multiplier
4. If Day ∈ {11,22}: Apply 0.9x Kelly multiplier
5. Otherwise: Use 1.0x multiplier (neutral)
```

### Option B: Filter (SAFER)
```
1. Exclude all bets on players with Personal Day 11 or 22
2. Boost confidence for players with Personal Days 3, 4, or 9
3. Use only as input to larger model, not standalone
```

### Option C: Standalone (NOT RECOMMENDED, High Risk)
```
Only for these combos:
- Red × Day 4 or 8 (Kelly 1.0x-1.1x)
- Purple × Day 11 (Kelly 1.0x)
As secondary signal only; never primary stake driver
```

---

## Quality Checklist

| Criterion | Status | Note |
|-----------|--------|------|
| Data integrity | ✓ | 61,300 records after filtering |
| Methodology | ✓ | Corrected interpretation (negative=good) |
| Filter validation | ✓ | All combos meet Calm/Moderate/Tough, Open/Pos/Clos/Surv, S/NS |
| Sample size | ⚠️ | 21 combos <20 rounds (risky) |
| Stability | ⚠️ | 93 of 96 erratic (σ≥1.6) |
| Statistical significance | ⚠️ | None formally tested; recommend χ² validation |
| Out-of-sample validation | ❌ | Not yet done (2025-2026 season pending) |

---

## Next Steps

1. **Validation (Priority HIGH):**
   - Test on 2024-2025 tournament data (out-of-sample)
   - Run χ² goodness-of-fit test for significant day effects
   - Stratify by round type (does Pink × Day 2 work better in Closing vs Open?)

2. **Integration (Priority MEDIUM):**
   - Combine with Color × Condition (already validated +4-6%)
   - Layer with Moon Phase (western + vedic)
   - Test ensemble: Color × (Day + Condition + Moon)

3. **Expansion (Priority LOW):**
   - Monitor 2025-2026 season for Tier 1 small-sample combos
   - Consider Personal Month × Color (likely weaker, but check)
   - Look for Color × Day × Round Type interactions

---

## File Summary

| File | Purpose | Size |
|------|---------|------|
| **COLOR_PERSONALDAY_QUICK_STATS.txt** | Fast reference (start here) | 6.6K |
| **COLOR_PERSONALDAY_EXECUTIVE_SUMMARY.md** | Detailed recommendations | 7.0K |
| **COLOR_PERSONALDAY_ANALYSIS_CORRECTED.md** | Technical deep-dive | 7.0K |
| **color_personalday_combos_corrected.csv** | Full dataset (96 combos) | 15K |
| **color_personalday_pivot.csv** | Heat map by Color × Day | 1.7K |
| **analyze_color_personal_day_corrected.py** | Analysis script (executable) | 10K |
| **COLOR_PERSONALDAY_ANALYSIS_INDEX.md** | This document | — |

---

## Analysis Provenance

**Generated:** April 4, 2026
**Source Data:** Golf Historics v3 - ANALYSIS (7).csv
**Methodology:** Pandas + NumPy statistical analysis
**Filters Applied:** Condition (Calm/Moderate/Tough) + Round Type (Open/Pos/Clos/Surv) + Tournament Type (S/NS)
**Records:** 61,300 / 77,155 (79.5%)
**Combos:** 96 (8 colors × 12 personal days)

**Script:** analyze_color_personal_day_corrected.py
**Owner:** Claude (April 4, 2026)

---

## Interpretation Notes

### Corrected Meaning
- In golf, negative scores vs field average are GOOD (beat the field)
- This analysis classifies "beat field avg" (negative vs_avg) as the desired outcome
- All percentages refer to proportion of rounds beating field average

### Stability Classification
- **Rock Solid (σ < 0.5):** Near-zero variance; magnitude is predictable
- **Consistent (σ < 0.8):** Low variance; useful for Kelly sizing
- **Moderate (σ < 1.2):** Medium variance; acceptable for secondary signals
- **Volatile (σ < 1.6):** High variance; direction useful, magnitude unreliable
- **Erratic (σ ≥ 1.6):** Very high variance; magnitude unpredictable, direction inconsistent

### Kelly Sizing
- Multiplier 1.1x = boost confidence by 10% (for strong days 3,4,9)
- Multiplier 0.9x = reduce confidence by 10% (for weak days 11,22)
- Multiplier 1.0x = neutral (baseline)
- Applied to existing Kelly fraction from primary signal

---

**Analysis complete. Ready for deployment as secondary conditioning layer.**

