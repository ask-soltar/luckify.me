# 3-Ball ROI Audit Guide

## Overview
This document explains exactly how scores, edges, filters, and ROI are calculated for 3-ball matchup validation.

---

## 1. Score Calculation Formula

For each player, we calculate:
```
SCORE = (EXEC_ROI + UPSIDE_ROI) / 2
```

### Example: Player A (Yellow color, Exec=25, Upside=25.0)

**Step 1: Bucket the scores**
- Exec=25 → Bucket "25-50" (25 ≤ x < 50)
- Upside=25.0 → Bucket "25-50" (25 ≤ x < 50)

**Step 2: Look up ROI from tables**
- File: `color_exec_bucket_roi_v2.csv`
  - Filter: condition="Moderate", round_type="Open", color="Yellow", exec_bucket="25-50"
  - Result: EXEC_ROI = -8.12%

- File: `color_upside_bucket_roi_v2.csv`
  - Filter: condition="Moderate", round_type="Open", color="Yellow", upside_bucket="25-50"
  - Result: UPSIDE_ROI = -19.75%

**Step 3: Average the ROIs**
```
SCORE_A = (-8.12 + -19.75) / 2 = -13.94%
```

---

## 2. Edge Calculation

Once all 3 players are scored:
```
1. Rank players by score (highest to lowest)
2. EDGE = BEST_SCORE - SECOND_BEST_SCORE
```

### Example: Haotong Li vs Zecheng Dou vs Jordan Smith
- Player A (Haotong Li): score = -13.94%
- Player B (Zecheng Dou): score = -13.94%
- Player C (Jordan Smith): score = +0.78%

Ranking: C (0.78%) > A (-13.94%) = B (-13.94%)

```
EDGE = 0.78 - (-13.94) = 14.71%
```

**Prediction: BET on Player C (best score)**

---

## 3. Filtering Rules

We test multiple filter thresholds:

| Filter | Rule | Meaning |
|--------|------|---------|
| 0% | EDGE > 0% | Pick if best player beats second |
| 0.5% | EDGE > 0.5% | Pick if edge at least 0.5% |
| 1% | EDGE > 1% | Pick if edge at least 1% |
| 2% | EDGE > 2% | Pick if edge at least 2% |
| 5% | EDGE > 5% | Pick if edge at least 5% |
| 8% | EDGE > 8% | Pick if edge at least 8% |

**For each matchup, we calculate whether it qualifies for EACH threshold.**

In the audit spreadsheet:
- `filter_0pct` = TRUE if edge > 0%
- `filter_0.5pct` = TRUE if edge > 0.5%
- `filter_1pct` = TRUE if edge > 1%
- etc.

---

## 4. Outcome Recording

For each matchup, we record:

```
ACTUAL_WINNER = Who actually won in the tournament
RESULT_TYPE = {WIN, LOSS, 2WAY_PUSH_WIN, 2WAY_PUSH_LOSS, 3WAY_PUSH}
WIN_INDICATOR = 1 if (WIN or 2WAY_PUSH_WIN), else 0
```

---

## 5. P&L Calculation (Moneyline-based)

For each matchup with known odds (ML A, ML B, ML C):

```
IF RESULT = WIN:
  Profit = ML_Factor * 100

IF RESULT = LOSS:
  Profit = -100

IF RESULT = 2WAY_PUSH_WIN (predicted player in tie):
  Profit = (ML_Factor * 100) / 2

IF RESULT = 2WAY_PUSH_LOSS (predicted player not in tie):
  Profit = -100

IF RESULT = 3WAY_PUSH:
  Profit = 0
```

Where ML_Factor is converted from moneyline odds:
```
IF ML >= 0:
  ML_Factor = ML / 100        (e.g., +150 → 1.5)
ELSE:
  ML_Factor = 100 / abs(ML)   (e.g., -150 → 0.667)
```

**Example:**
- Prediction: Player C
- Actual result: C won
- Moneyline for C: -120
- ML_Factor = 100 / 120 = 0.833
- Profit = 0.833 * 100 = $83.30

---

## 6. ROI Calculation at Each Filter Level

For a given filter threshold:

```
MATCHUPS_QUALIFYING = count(filter = TRUE)
GRADED_MATCHUPS = count(filter = TRUE AND result ≠ SKIP/UNKNOWN)
TOTAL_WINS = count(win_indicator = 1)
WIN_RATE = TOTAL_WINS / GRADED_MATCHUPS * 100%

TOTAL_P&L = sum(pl) for all graded matchups
AVERAGE_BET = TOTAL_P&L / GRADED_MATCHUPS
ROI = (AVERAGE_BET / 100) * 100
```

---

## 7. Audit Results Summary

From `3ball_roi_audit.csv`:

| Filter | Matchups | Graded | Wins | Win % | Total P&L | ROI |
|--------|----------|--------|------|-------|-----------|-----|
| 0% | 423 | 423 | 182 | 43.0% | $3,297 | 7.8% |
| **0.5%** | 394 | 394 | 172 | 43.7% | **$3,991** | **10.1%** |
| 1% | 330 | 330 | 135 | 40.9% | $467 | 1.4% |
| 2% | 289 | 289 | 109 | 37.7% | -$585 | -2.0% |
| 5% | 162 | 162 | 51 | 31.5% | -$2,457 | -15.2% |
| 8% | 67 | 67 | 17 | 25.4% | -$2,671 | -39.9% |

**Optimal: Edge > 0.5% gives 10.1% ROI**

---

## 8. Verification Checklist

To audit this work, verify:

- [ ] Score formula: (exec_roi + upside_roi) / 2 ✓
- [ ] Exec/Upside buckets use 25-point ranges (0-25, 25-50, 50-75, 75-100) ✓
- [ ] ROI lookup uses correct (condition, round_type, color, bucket) combination ✓
- [ ] Edge = best_score - second_best_score ✓
- [ ] Filter thresholds are applied correctly (edge > X%) ✓
- [ ] P&L uses moneyline conversion for odds ✓
- [ ] Win rate and ROI calculations match audit spreadsheet ✓

---

## 9. Known Issues

1. **Edge signal is inverted**: Higher edges correlate with LOWER win rates
2. **ROI tables may not be predictive**: Training data (ANALYSIS v3) may not predict live outcomes
3. **3-ball model doesn't generalize**: Same methodology works better in 2-ball
4. **Optimal filter is counterintuitive**: Lower thresholds (0.5%) perform better than higher ones (5%, 8%)

---

## Files Referenced

- `3ball_roi_audit.csv` - Full audit data for all 423 matchups
- `matchup3b_scored_3ball.csv` - Scored 3-balls with colors, exec, upside, edges
- `matchup3b_scored_3ball_with_pl.csv` - P&L results with moneyline odds
- `color_exec_bucket_roi_v2.csv` - Exec ROI lookup table
- `color_upside_bucket_roi_v2.csv` - Upside ROI lookup table
