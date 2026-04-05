# Color & Personal Day +2/-2 Threshold Analysis

**Analysis Date:** 2026-04-04
**Data Source:** Golf Historics v3 - ANALYSIS (7).csv
**Records Analyzed:** 61,301 (after filtering)
**Raw Input:** 77,155 records

---

## Executive Summary

This analysis examines how **Color** (BaZi Rhythm) and **Personal Day** (numerology) influence player scoring performance, specifically looking at:
- **Metric:** score (col G) - course_avg (col I) = performance vs field average
- **Thresholds:** +2/-2 bins to identify bias toward outperformance or underperformance
- **Filters:** Calm/Moderate/Tough conditions, Open/Positioning/Closing/Survival rounds, S/NS tournament types only

### Key Findings at a Glance

**Colors - Positive Bias:**
- **Blue, Yellow, Red** lead in positive skew (~46-46.3% in positive range, mean near -0.08 to -0.19)
- **Red** has strongest "strong positive" bias: 23.68% in +2 to +6+ range
- **Pink, Brown** show strong negative bias (60.4% and 59.2% in negative range)

**Personal Days - Positive Bias:**
- **Days 5, 6, 7** dominate positive skew (46.8-47.04% in positive range, mean -0.15 to -0.17)
- **Day 22** strongest negative bias (55.32% in negative range, mean -0.269)
- **Day 3** also weak (55.07% negative, mean -0.249)

---

## Filtering Logic

**Applied filters:**
```
Condition:        Calm OR Moderate OR Tough (all 3)
Round Type:       Open OR Positioning OR Closing OR Survival
Tournament Type:  S (Standard Stroke Play) OR NS (Non-Standard Stroke Play)
                  [Excluded T/P/M: Team, Points, Match play — not comparable]
Removed:          Null Color or null Personal Day
```

**Result:** 61,301 valid records (79.5% of raw 77,155)

---

## Overall Distribution

**Metric (score - course_avg):**
| Bin | Count | % |
|-----|-------|-----|
| -6 to -4 | 5,580 | 9.10% |
| -4 to -2 | 11,283 | 18.41% |
| -2 to 0 | 16,409 | 26.77% |
| **0 to 2** | **14,646** | **23.89%** |
| **2 to 4** | **8,296** | **13.53%** |
| **4 to 6** | **3,507** | **5.72%** |
| **6+** | **1,580** | **2.58%** |

**Positive range (0+):** 45.72% of all rounds
**Negative range (<0):** 54.28% of all rounds
**Mean:** -0.199
**Median:** -0.252
**Std Dev:** 3.233

---

## Color Analysis

**8 colors present.** Ranked by volume and impact:

### Colors by Frequency
1. **Yellow** — 22,252 (36.3%)
2. **Blue** — 11,807 (19.3%)
3. **Orange** — 9,308 (15.2%)
4. **Purple** — 8,370 (13.7%)
5. **Green** — 7,390 (12.1%)
6. **Red** — 1,698 (2.8%)
7. **Pink** — 385 (0.6%)
8. **Brown** — 91 (0.1%)

### Colors with Strongest Positive Bias (Score > 0)

| Color | Positive % | Mean | n | +2 to +6+ % |
|-------|------------|------|---|------------|
| **Blue** | 46.35% | -0.150 | 11,807 | 22.25% |
| **Yellow** | 46.05% | -0.188 | 22,252 | 21.78% |
| **Red** | 45.53% | -0.082 | 1,698 | **23.68%** ← Best strong positive |
| **Orange** | 45.32% | -0.245 | 9,308 | 21.41% |
| **Purple** | 45.24% | -0.242 | 8,370 | 21.58% |

**Interpretation:**
- **Red** shows best quality upside: 23.68% of Red rounds score 2+ above average (highest concentration in strong positive range)
- **Blue, Yellow** have volume (11.8k, 22.2k) with solid positive bias, making them reliable signals
- **Blue** has best mean (-0.150, closest to neutral)

### Colors with Strongest Negative Bias (Score < 0)

| Color | Negative % | Mean | n | -6 to -2 % |
|-------|------------|------|---|------------|
| **Brown** | 60.44% | -0.261 | 91 | 29.67% |
| **Pink** | 59.22% | -0.296 | 385 | **31.43%** ← Worst strong negative |
| **Green** | 54.83% | -0.226 | 7,390 | 27.86% |
| **Purple** | 54.77% | -0.242 | 8,370 | 28.04% |
| **Orange** | 54.67% | -0.245 | 9,308 | 27.69% |

**Interpretation:**
- **Pink, Brown** are clear penalty colors: >59% of rounds below average, with heavy concentration in -6 to -2 range (30%+)
- **Green, Purple, Orange** show moderate penalty (~27-28% in strong negative range)
- **Brown** (only 91 samples) and **Pink** (385 samples) may be high-variance; recommend filtering to sufficient sample size before deployment

---

## Personal Day Analysis

**12 unique Personal Days identified:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33

*Note: Days 10, 12-21, 23-32 are absent from this dataset. Distribution is imbalanced.*

### Days with Strongest Positive Bias (Score > 0)

| Day | Positive % | Mean | n | +2 to +6+ % |
|-----|------------|------|---|------------|
| **Day 6** | **47.04%** | -0.159 | 5,351 | 22.61% |
| **Day 5** | **46.80%** | -0.148 | 6,905 | **22.60%** |
| **Day 7** | 46.18% | -0.173 | 6,837 | 22.30% |
| **Day 9** | 45.82% | -0.159 | 6,798 | 21.65% |
| **Day 11** | 45.70% | -0.186 | 2,000 | 21.40% |

**Interpretation:**
- **Days 5, 6, 7** are premium: >46.8% in positive range, concentrated at edges (Days 5 & 6 have 22.6% in +2 to +6+ range)
- **Day 5** has best mean (-0.148, highest overall)
- **Days 5-7** form a cohesive signal: "mid-week days" (numerologically associated with challenge/opportunity) perform well
- Volume is solid for Days 5, 7 (6.9k, 6.8k); Day 6 at 5.4k

### Days with Strongest Negative Bias (Score < 0)

| Day | Negative % | Mean | n | -6 to -2 % |
|-----|------------|------|---|------------|
| **Day 22** | **55.32%** | -0.269 | 2,191 | **29.08%** ← Worst |
| **Day 33** | **55.11%** | -0.224 | 1,450 | 25.73% |
| **Day 3** | **55.07%** | -0.249 | 6,752 | 28.44% |
| **Day 1** | 54.81% | -0.213 | 6,766 | 27.69% |
| **Day 2** | 54.76% | -0.271 | 4,822 | 28.19% |

**Interpretation:**
- **Day 22** is a clear penalty day: 55.32% negative, mean -0.269, heaviest concentration in -6 to -2 (29.08%)
- **Days 1-3** show moderate penalty (55% negative), likely associated with "reset cycle" (new month/week effects)
- **Day 33** (only 1,450 samples, ~2.4%) is an outlier; recommend verifying data integrity (Day 33 in month? Calculation artifact?)

---

## Combined Insights: Color × Personal Day

### High-Signal Combos (Preliminary)

**Strong Positive Signals (recommend further testing):**
1. **Blue × Day 5-6-7** — Blue has +46.35% positive, Days 5-7 have +47% positive → multiplicative effect likely
2. **Red × Day 5-6-7** — Red has strongest upside quality (+23.68% in +2 to +6+), Days 5-7 are premium
3. **Yellow × Day 5-6** — Yellow has highest volume (22.2k) + Days 5-6 best performers

**Strong Negative Signals (recommend avoidance):**
1. **Pink × Day 22** — Pink (59.22% negative) × Day 22 (55.32% negative) = compound underperformance risk
2. **Pink × Days 1-3** — Pink underperforms; Days 1-3 also weak
3. **Brown × Day 22** — Brown (60.44% negative) × Day 22 (55.32% negative) = highest penalty combo

### Statistical Caution
- **Pink (385 samples), Brown (91 samples)** have low n; require validation on larger dataset before betting
- **Days 10, 12-21, 23-32** are absent (likely data artifact or rarity); treat as missing not negative
- **Day 33** may be data error (is 33rd day of month in rare cases?); verify before using

---

## Raw Data Files Generated

1. **`analysis_color_personalday_filtered.csv`**
   - Summary statistics table (mean, median, std dev, record counts)

2. **`frequency_by_color.csv`**
   - Full frequency distribution by color (8 rows)
   - Columns: color, count, %_of_population, mean_metric, bin counts, bin %, derived bias metrics

3. **`frequency_by_personalday.csv`**
   - Full frequency distribution by personal day (12 rows)
   - Same column structure as color file

---

## Methodology Notes

**Metric Calculation:**
- `metric = score (col G) - course_avg (col I)`
- This is **score relative to field average**, not relative to par
- Positive metric = better than field; negative = worse than field

**Binning Strategy:**
- Bins: -6 to -4, -4 to -2, -2 to 0, 0 to 2, 2 to 4, 4 to 6, 6+
- "Positive range" = 0 to 2 + 2 to 4 + 4 to 6 + 6+ (all ≥0)
- "Strong positive" = 2 to 4 + 4 to 6 + 6+ (performance >+2 above average)
- "Strong negative" = -6 to -4 + -4 to -2 (performance <-2 below average)

**Why DuckDB + Pandas:**
- DuckDB for efficient SQL-based filtering on 77k rows
- Pandas for group-by aggregation and export

---

## Next Steps (Recommendations)

1. **Validate Color × Personal Day combos** — Run `analyze_color_personalday_combos.py` to get 2D cross-tab with sample sizes and significance tests

2. **Exclude low-n colors** — Consider filtering Pink/Brown to high-volume data only (n>500) if using in live betting

3. **Investigate Day 33** — Check if this is a genuine numerological calculation or data artifact; may need to treat as missing

4. **Test signal strength** — Use chi-squared test or logistic regression to quantify:
   - Does Color × Day predict >0 outcome better than random?
   - How much does each factor contribute?

5. **Season-by-Season analysis** — Repeat by year or tournament type to check signal stability across time

---

**Analysis completed:** 2026-04-04 using DuckDB + Pandas
**Script:** `analyze_color_personalday_thresholds.py` (reusable for future data refreshes)
