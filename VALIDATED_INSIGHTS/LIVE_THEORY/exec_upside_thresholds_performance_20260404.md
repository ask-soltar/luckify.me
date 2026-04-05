---
title: Exec & Upside Score Thresholds and Performance
status: LIVE_THEORY
confidence: 1
date_created: 2026-04-04
last_updated: 2026-04-04
---

## Theory Statement
Higher Upside scores (and Exec scores) should correlate with better performance (higher vs_avg, higher win rates) across all playing conditions (Calm, Moderate, Tough). Upside > Exec suggests growth potential; players with high Upside should outperform in most conditions.

## Origin
User intuition + numerology/divination logic (Upside = growth/expansion energy → better performance).

## Reasoning
- **Upside:** Represents growth, expansion, potential → should translate to better results
- **Exec:** Represents execution/manifestation → should also correlate with performance
- **Threshold hypothesis:** Players bucketed by Upside (0-25, 25-50, 50-75, 75-100) should show performance ladder (higher bucket = better performance)
- **Prediction:** Top Upside bucket should outperform baseline by +0.3 to +0.7 vs_avg

## Test Plan

### Data Source
Golf Historics v3 - ANALYSIS (8)
All years, S + NS tournament types, Calm/Moderate/Tough conditions

### Variables
- **Exec:** Executive/manifestation score (0-100 scale)
- **Upside:** Growth/potential score (0-100 scale)
- **vs_avg:** Score vs venue field average (performance metric)
- **Conditions:** Calm, Moderate, Tough
- **Colors:** All 8 colors

### Analysis Approach

**Level 1: Upside Bucket Thresholds**
```
Upside buckets: 0-25, 25-50, 50-75, 75-100
For each bucket:
  Mean vs_avg, n, win rate (beat_field)
  Trend: Does higher bucket = better performance?
```

**Level 2: Exec Bucket Thresholds**
```
Same as Upside, but for Exec score
```

**Level 3: Upside × Condition (Does effect hold across conditions?)**
```
For each Upside bucket × Condition:
  Mean vs_avg, n, win rate
  Expect: Top bucket wins in Calm AND Moderate AND Tough
```

**Level 4: Color × Upside Interaction (Which colors amplify high Upside?)**
```
For each color:
  High Upside (75-100) vs baseline
  Which colors benefit most from high Upside?
```

**Level 5: Correlation Analysis (How strong is the relationship?)**
```
Correlation: Upside vs vs_avg (Pearson r)
Correlation: Exec vs vs_avg
Stratified by condition
```

**Levels 6-8 (Deep):**
- Round progression (Upside effect by round)
- Time trend (Upside effect stable over years?)
- Synergy (Upside × Exec combined)

### Passing Thresholds
| Gate | Threshold |
|------|-----------|
| **Statistical Significance** | p < 0.05 (stricter; expecting strong effect) |
| **Sample Size** | n ≥ 100 per bucket |
| **Effect Size** | Cohen's d ≥ 0.3 OR vs_avg diff ≥ +0.15 |
| **Trend Consistency** | Higher bucket > lower bucket in ≥2 conditions |
| **Correlation** | Pearson r ≥ 0.10 (positive direction) |

## Execution

### Script
`test_exec_upside_thresholds.py` (to be written)

### Expected Output
- Level 1 CSV: Upside bucket performance
- Level 2 CSV: Exec bucket performance
- Level 3 CSV: Upside × Condition breakdown
- Level 4 CSV: Color × Upside interaction
- Level 5 CSV: Correlation analysis
- Level 6-8 CSVs: (if deep analysis)
- Report: Is performance ladder real? How strong?

### Expected Time
1.5-2 hours (comprehensive 8-angle analysis)

## Key Questions to Answer

1. Does higher Upside consistently outperform lower Upside?
2. Is there a performance ladder (0-25 < 25-50 < 50-75 < 75-100)?
3. Does the effect hold across all conditions (Calm, Moderate, Tough)?
4. Which colors benefit most from high Upside?
5. How strong is the correlation between Upside score and performance?
6. Does Exec follow the same pattern as Upside?

## Next Steps
- [ ] User approves test plan
- [ ] Choose: Quick (3-level) or Deep (8-angle) analysis?
- [ ] Claude writes script
- [ ] Test runs
- [ ] Results reviewed
- [ ] Decision: VALIDATED / PARTIALLY_BACKED / REJECTED

