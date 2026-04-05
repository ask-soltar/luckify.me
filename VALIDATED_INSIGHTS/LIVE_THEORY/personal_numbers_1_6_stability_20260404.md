---
title: Personal Numbers 1 & 6 Stability Signal
status: LIVE_THEORY
confidence: 1
date_created: 2026-04-04
last_updated: 2026-04-04
---

## Theory Statement
Personal Day 1 and Personal Day 6 players outperform other personal days because their numerological profiles represent neutrality and stability. This stability should manifest as measurably better vs_avg performance compared to all other personal days (2-5, 7-9, 11, 22, 33).

## Origin
User intuition + numerology theory (1 = foundation/beginning stability; 6 = harmony/balance).

## Reasoning
- **PD 1:** Foundation number, neutral energy, beginning of cycle → stable platform
- **PD 6:** Harmony number, balanced energy, natural stabilizer → consistent performance
- **Others (2-5, 7-9, 11, 22, 33):** Variable energies, highs and lows → more inconsistent
- **Prediction:** PD 1 + 6 should outperform baseline by +0.15 to +0.30 vs_avg

## Test Plan

### Data Source
Golf Historics v3 - ANALYSIS (8)
All years, S + NS tournament types, Calm/Moderate/Tough conditions

### Group Definitions
- **Stable:** PD 1 + PD 6 (combined)
- **Baseline:** All other PD (2-5, 7-9, 11, 22, 33)
- **By Color:** Test each of 8 colors against stable baseline

### Metrics
- vs_avg (primary)
- win_rate (beat_field, secondary)

### Analysis Levels

**Level 1:** Overall stability effect
```
PD 1: mean vs_avg, n, std
PD 6: mean vs_avg, n, std
PD 1+6 Combined: mean vs_avg, n, std
Baseline: mean vs_avg, n, std
```

**Level 2:** By Color (8 colors × 3 groups: PD1, PD6, baseline)
```
PD 1 × [each color]: vs_avg, n, p-value
PD 6 × [each color]: vs_avg, n, p-value
```

**Level 3:** By Round Type (Open, Positioning, Closing, Survival)
```
For PD 1+6 combined vs baseline:
  Open: vs_avg, n, p-value
  Positioning: vs_avg, n, p-value
  Closing: vs_avg, n, p-value
  Survival: vs_avg, n, p-value
```

### Passing Thresholds
| Gate | Threshold |
|------|-----------|
| **Statistical Significance** | p < 0.10 (exploratory, but direction must be positive for PD 1/6) |
| **Sample Size** | n ≥ 100 for PD 1, n ≥ 100 for PD 6 |
| **Effect Size** | Cohen's d ≥ 0.15 OR vs_avg diff ≥ +0.10 (positive direction) |
| **Stability** | Effect consistent across ≥2 round types |

## Execution

### Script
`test_personal_numbers_1_6_stability.py` (to be written)

### Expected Output
- Level 1 CSV: Overall stability comparison
- Level 2 CSV: Color × Personal Number breakdown
- Level 3 CSV: Round type stratification
- Report: Which colors pair best with stability? Is effect real?

### Expected Time
1-2 hours

## Key Questions to Answer

1. Do PD 1 and PD 6 players outperform baseline?
2. Is the effect positive (as predicted) or negative (contradiction)?
3. Which colors amplify the stability effect?
4. Is stability consistent across all round types or specific to one?
5. Is PD 1 or PD 6 stronger, or are they equivalent?

## Next Steps
- [ ] User approves test plan
- [ ] Claude writes analysis script
- [ ] Test runs
- [ ] Results reviewed
- [ ] Decision: VALIDATED / PARTIALLY_BACKED / REJECTED

