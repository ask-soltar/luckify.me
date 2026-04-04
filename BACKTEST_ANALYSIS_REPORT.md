# Color × Personal Day Backtest Report

## Executive Summary

Backtest of 20 Color × Personal Day combos using train/test split (2022-2024 train, 2025-2026 test via holdout).

**Key Finding:** None of the 20 tested combos show strong predictive edge. The hypothesis that specific Color + Personal Day combinations reliably beat field average is NOT supported by the data.

### Overall Statistics
- **Valid combos tested:** 15 of 20 (5 had insufficient data)
- **Combos with >50% win rate:** 3 (Green × Day 11, Blue × Day 22, Brown × Day 7)
- **Mean test win rate:** 44.8% (vs 50% baseline) → -5.2% edge
- **Mean variance (train→test):** 12.2% (high divergence suggests overfitting or noise)

---

## Detailed Results

### Positive Signals (Test WR > 50%)

#### 1. Green × Day 11 (Direction Switcher) ✓
- **Training:** 38.4% (n=151)
- **Testing:** 52.7% (n=93)
- **Variance:** 14.3% (significant divergence)
- **Edge:** +2.7% vs 50% baseline
- **Kelly Sizing:** 5.4%
- **Interpretation:** Train shows weak signal (below 50%), test flips to 52.7%. Large variance suggests instability. The divergence is suspicious—could indicate overfitting on the 80/20 holdout or true signal that didn't appear in training subset.
- **Recommendation:** Proceed with caution. Test with higher bar (60%+ win rate) before deployment.

#### 2. Blue × Day 22 (Candidate) ✓
- **Training:** 42.9% (n=296)
- **Testing:** 55.3% (n=132)
- **Variance:** 12.4% (significant divergence)
- **Edge:** +5.3% vs 50% baseline
- **Kelly Sizing:** 10.6%
- **Interpretation:** Similar to Green × Day 11. Training shows weak signal, test improves to 55.3%. Variance of 12.4% is high; this suggests the test set may not be representative of the true distribution, or there's a real temporal shift.
- **Recommendation:** Requires further validation. Sample size is reasonable (n=132), but the large variance is concerning.

#### 3. Brown × Day 7 (Candidate) ✓
- **Training:** 40.0% (n=5)
- **Testing:** 100.0% (n=1)
- **Variance:** 60.0% (extreme divergence)
- **Edge:** +50.0% vs 50% baseline
- **Kelly Sizing:** 100.0%
- **Interpretation:** Training sample is tiny (n=5). Test result is n=1 with 100% win rate. This is not statistically meaningful and should be ignored.
- **Recommendation:** REJECT. Ignore. Insufficient sample size.

---

### Neutral/Weak Signals (Test WR 40-50%)

#### 4. Purple × Day 7 (Candidate)
- **Training:** 47.1% (n=605)
- **Testing:** 49.2% (n=319)
- **Variance:** 2.1% (stable)
- **Edge:** -0.8% vs 50% baseline
- **Interpretation:** Very stable across train/test (variance only 2.1%). Consistent but slightly below 50% threshold. Not a signal.

#### 5. Yellow × Day 22 (Consistent Winner)
- **Training:** 41.8% (n=552)
- **Testing:** 47.1% (n=255)
- **Variance:** 5.2%
- **Edge:** -2.9% vs 50% baseline
- **Interpretation:** Improves from train to test but remains below 50%. Original hypothesis labeled this "Consistent Winner" but data contradicts it.

#### 6. Purple × Day 3 (Consistent Winner)
- **Training:** 43.2% (n=630)
- **Testing:** 44.9% (n=312)
- **Variance:** 1.7% (very stable)
- **Edge:** -5.1% vs 50% baseline
- **Interpretation:** Extremely stable (only 1.7% variance). Consistently ~44.9%, which is below baseline. Not a signal.

#### 7. Blue × Day 5 (Candidate)
- **Training:** 45.6% (n=965)
- **Testing:** 49.1% (n=397)
- **Variance:** 3.5% (stable)
- **Edge:** -0.9% vs 50% baseline
- **Interpretation:** Large sample sizes, stable across split. Very close to 50% but not quite there. Marginal.

#### 8. Yellow × Day 11 (Candidate)
- **Training:** 46.7% (n=497)
- **Testing:** 47.6% (n=250)
- **Variance:** 0.9% (extremely stable)
- **Edge:** -2.4% vs 50% baseline
- **Interpretation:** Highly stable. Consistently ~47.6%, below baseline.

---

### Negative Signals (Test WR < 40% or High Variance)

#### 9. Red × Day 4 (Weak/Avoid) ✗
- **Training:** 42.4% (n=92)
- **Testing:** 28.3% (n=46)
- **Variance:** 14.1% (significant divergence)
- **Edge:** -21.7% vs 50% baseline
- **Interpretation:** Test performance is terrible at 28.3%. This is the weakest signal. Original hypothesis labeled it "Weak/Avoid"—data confirms it should be avoided.
- **Recommendation:** STRONG AVOID. This combo actively loses money.

#### 10. Orange × Day 1 (Direction Switcher)
- **Training:** 44.9% (n=792)
- **Testing:** 37.7% (n=212)
- **Variance:** 7.2%
- **Edge:** -12.3% vs 50% baseline
- **Interpretation:** Large sample (n=792) shows training at 44.9%, test drops to 37.7%. Weak.

#### 11. Orange × Day 33 (Direction Switcher)
- **Training:** 43.7% (n=174)
- **Testing:** 39.1% (n=46)
- **Variance:** 4.5%
- **Edge:** -10.9% vs 50% baseline
- **Interpretation:** Small test sample (n=46) at 39.1%. Below baseline.

#### 12. Red × Day 8 (Consistent Winner)
- **Training:** 41.4% (n=133)
- **Testing:** 40.9% (n=66)
- **Variance:** 0.4% (extremely stable)
- **Edge:** -9.1% vs 50% baseline
- **Interpretation:** Very stable but consistently below 50%. Original hypothesis labeled it "Consistent Winner"—data contradicts.

#### 13. Green × Day 2 (Consistent Winner)
- **Training:** 44.4% (n=403)
- **Testing:** 41.1% (n=202)
- **Variance:** 3.3%
- **Edge:** -8.9% vs 50% baseline
- **Interpretation:** Stable but below baseline.

#### 14. Purple × Day 11 (Weak/Avoid)
- **Training:** 43.3% (n=180)
- **Testing:** 39.6% (n=91)
- **Variance:** 3.8%
- **Edge:** -10.4% vs 50% baseline
- **Interpretation:** Below baseline, confirms "Weak/Avoid" label.

#### 15. Pink × Day 8 (Candidate)
- **Training:** 50.0% (n=38)
- **Testing:** 0.0% (n=2)
- **Variance:** 50.0% (extreme divergence)
- **Edge:** -50.0% vs 50% baseline
- **Interpretation:** Training shows 50%, test shows 0% (n=2 insufficient). Extreme variance. Reject as noise.

---

### No Data (5 combos)
- Pink × Day 15
- Orange × Day 10
- Green × Day 20
- Red × Day 15
- Brown × Day 14

These combos do not exist in the dataset or have zero rounds.

---

## Statistical Validation

### Confidence Intervals
All combos tested use **Wilson score 95% CI** (more accurate for extreme proportions than normal approximation).

Example: Green × Day 11
- Test WR: 52.7%
- CI: [42.6% - 62.5%]
- Confidence: We are 95% confident the true win rate is between 42.6% and 62.5%

The wide CI reflects the finite sample size (n=93 for test). Narrower samples (n=46) have wider CI bands.

### Variance Analysis
- **Low variance (<5%):** Signal is stable across train/test (Purple × Day 7, Yellow × Day 11)
- **Medium variance (5-10%):** Some divergence (Yellow × Day 22, Orange × Day 33)
- **High variance (>10%):** Large divergence, possible overfitting or temporal shift (Green × Day 11, Blue × Day 22, Red × Day 4)

High variance signals are unreliable for deployment.

---

## Key Findings

### 1. Hypothesis Was Incorrect
The original hypothesis that certain Color × Personal Day combos beat field average on specific conditions is NOT supported by the data:
- 15 valid combos tested
- Only 3 showed >50% win rate
- 2 of those 3 have extreme variance (>12%) suggesting noise
- Mean win rate across all: 44.8% (vs 50% baseline)

### 2. No Consistency Between Training and Testing
High variance across train/test splits suggests:
- Either the signal is overfitting to a specific time window (2022-2024)
- Or the signal is too weak to reliably predict 2025-2026 outcomes
- Or temporal changes in the game/players have shifted the distribution

### 3. Color Alone May Not Be Predictive
Unlike the 4D Element analysis (which found strong signals like Calm × Closing × Purple × Fire at +4.6%), Color × Personal Day combos show baseline performance.

This suggests:
- Color might need to be combined with additional dimensions (condition, round type, moon phase)
- Personal Day may be too granular or too weak as a primary signal
- The interaction between Color and Personal Day may not be as strong as originally theorized

---

## Recommendations

### For Deployment
1. **DO NOT deploy any of these 20 combos in isolation**
   - Mean edge is -5.2%
   - Only 3/15 valid combos beat 50%, and 2 of those are suspicious (high variance)

2. **Do NOT use Green × Day 11 or Blue × Day 22 for live betting**
   - Variance >12% indicates unreliable signals
   - Would recommend 60%+ win rate minimum before deployment
   - These may improve with larger sample sizes (wait for 2026-2027 data)

3. **STRONG AVOID: Red × Day 4**
   - Test WR: 28.3% (far below baseline)
   - Active loss-maker

### For Further Research
1. **Reconsider the framework**
   - Personal Day alone may be too weak
   - Try Personal Day + Color + Condition (e.g., Green × Day 11 × Calm)
   - Revisit the original 4D Element analysis (which showed stronger signals)

2. **Temporal analysis**
   - High variance suggests the signal may be time-dependent
   - Analyze by year to see if the signal changes (2022 vs 2023 vs 2024 vs 2025-2026)
   - If signal deteriorates over time, it may reflect changing player pool or course conditions

3. **Larger sample sizes**
   - Green × Day 11 (n=93 test) and Blue × Day 22 (n=132 test) could improve with more data
   - Consider waiting until 2027 when you have 2+ years of 2025-2026 data

4. **Ensemble approach**
   - Individual Color × Personal Day combos are weak
   - Consider combining multiple weak signals (e.g., vote-based ensemble)
   - Merge with other divination signals (Wu Xing, Zodiac, Moon phase) to boost

---

## Technical Notes

### Data & Methodology
- **Data source:** Golf Historics v3 - ANALYSIS (7).csv (77,155 rounds)
- **Standard filters:** Condition ∈ {Calm, Moderate, Tough} × Round Type ∈ {Open, Positioning, Closing, Survival} × Tournament Type ∈ {S, NS}
- **Train/test split:** 2022-2024 for training, 2025-2026 for testing
- **Fallback:** For combos with no 2025-2026 data, used 80/20 holdout split from all available years
- **Win rate:** Percentage of rounds where player beat field average (vs_avg > 0)
- **Confidence interval:** Wilson score 95% CI (accurate for all proportions, especially extremes)
- **Kelly criterion:** f = 2p - 1, only displayed if win rate >51%

### Files Generated
- `backtest_summary.txt` — This summary
- `backtest_detailed.csv` — Full results with all metrics

---

## Conclusion

The backtest does **not validate** the Color × Personal Day hypothesis. The expected edges (55.6%, 80%, etc.) were not observed. Instead:
- Mean win rate: 44.8% (baseline is 50%)
- Only 3/15 valid combos beat 50%
- High variance indicates unreliable signals

**Recommendation:** Do not use these combos for live betting. Consider revisiting the 4D Element analysis (which did show strong signals) or exploring alternative divination dimensions.
