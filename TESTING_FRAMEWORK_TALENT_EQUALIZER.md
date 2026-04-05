# Testing Framework: Orange Talent Equalizer Theory

## Core Finding to Validate
**Orange constrains elite players (lose to own par by +0.32) while liberating weak players (lose to own par by +0.09, but beat field by +0.96)**

---

## TIER 1: Core Pattern Validation

### Test 1A: Cross-Validation on 2025/2026 Out-of-Sample Data
**Does the pattern hold on recent data?**
- Filter: 2025/2026 only
- Metric: Does elite still underperform vs own par more than weak?
- Expected: Same direction, possibly different magnitude
- Pass threshold: p<0.05, effect size > 0.15 strokes

### Test 1B: Skill Tier Granularity
**Is the pattern consistent across more granular skill tiers?**
- Instead of quartiles (4 tiers), test deciles (10 tiers)
- Graph: vs_own_par by skill tier (should show increasing underperformance as skill increases)
- Pass: Monotonic increase in underperformance from weakest to elite

### Test 1C: Symmetry Check
**Does the same pattern appear when we compare field performance?**
- Do weak players overperform vs field more than elite underperform?
- Expected: Weak beat field by 0.96, elite lose by 0.59 (symmetry in opposite directions)
- Pass: The gap (1.55 strokes) is significant and stable

---

## TIER 2: Dimension-Specific Tests

### Test 2A: Does Pattern Vary by Condition?
**Does Orange's equalizer effect strengthen/weaken based on weather?**

```
For each condition (Calm, Moderate, Tough):
  - Repeat Test 1A for just that condition
  - Hypothesis: Effect strongest in Calm, weakest in Tough
  - Why: Tough noise might amplify variance, masking the talent equalizer
```

### Test 2B: Does Pattern Vary by Round Type?
**Is the equalizer stronger in specific round types?**

```
For each round type (Open, Closing, Survival, Positioning):
  - Elite vs weak underperformance gap
  - Hypothesis: Closing rounds show biggest effect (less room for luck)
```

### Test 2C: Does Pattern Vary by Moon Phase?
**Does the equalizer interact with moon phases?**

```
For each moon phase (New Moon, Full Moon, Waxing, Waning):
  - Elite vs weak performance gap
  - Cross-tabulate: Orange × Moon × Skill Tier
  - Hypothesis: New Moon amplifies the equalizer (clarity enforces baseline)
```

### Test 2D: Does Pattern Vary by Element (Year)?
**Different years (2022=Water through 2026=Fire) show different effects?**

```
By element year:
  - 2022 Water, 2023 Fire, etc.
  - Does the equalizer effect remain stable or change with element?
```

---

## TIER 3: Comparative Color Tests

### Test 3A: Is Orange Unique?
**Does Red, Green, Blue show the same talent equalizer pattern?**

```
For each color:
  - Calculate vs_own_par by skill tier
  - Compare Elite vs Weak underperformance
  - Hypothesis: Other colors DON'T show this pattern
                (Orange is unique as a "normalizer")
```

### Test 3B: Ranking Colors by Equalizer Strength
**Which colors constrain elite most? Liberate weak most?**

```
Matrix:
  Color      | Elite Underperformance | Weak Overperformance (vs field) | Net Equalizer Effect
  Orange     |                        |                                 |
  Red        |                        |                                 |
  Green      |                        |                                 |
  Blue       |                        |                                 |
  Yellow     |                        |                                 |
  Purple     |                        |                                 |
```

---

## TIER 4: Predictive Validation Tests

### Test 4A: Can We Predict Which Elite Will Underperform?
**Build a model: Does adj_his_par predict underperformance in Orange?**

```
Linear regression: vs_own_par ~ adj_his_par (Orange only)
  - Slope: How much does each additional stroke of skill = underperformance?
  - R-squared: How much of the variance does skill level explain?
  - Expected: Strong negative slope (higher skill = more underperformance)
```

### Test 4B: Kelly Sizing for Elite Fade
**If we fade elite Orange players, what's the edge?**

```
For Elite Top 25% Orange players:
  - Calculate: % that beat vs_avg (field)
  - Current: 43.5% beat field
  - Baseline (no Orange): ~50%
  - Edge: 6.5 percentage points
  - Kelly calculation: Can we size a fade position?
```

### Test 4C: Kelly Sizing for Weak Boost
**If we bet weak Orange players, what's the edge?**

```
For Weakest 25% Orange players:
  - Calculate: % that beat vs_avg (field)
  - Current: 65.2% beat field
  - Baseline (no Orange): ~50%
  - Edge: 15.2 percentage points (larger!)
  - Kelly calculation: Size position
```

---

## TIER 5: Robustness Tests

### Test 5A: Sample Size Stability
**Does the effect hold across different sample sizes?**

```
- Test on 2022 only (smallest sample)
- Test on 2022-2024 (medium)
- Test on 2022-2026 (full)
- Expected: Consistent direction, possibly larger p-value in smaller samples
```

### Test 5B: Tournament Type
**Does the effect vary by PGA Tour vs LIV vs DP World Tour?**

```
By tour (if data available):
  - Does Orange equalizer apply universally?
  - Hypothesis: PGA Tour (strongest field) shows biggest effect
               because elite have more to lose vs weak
```

### Test 5C: Outlier Sensitivity
**Is the effect driven by a few extreme cases or broadly consistent?**

```
- Identify top 5 elite outliers (most underperform in Orange)
- Remove them and re-run Test 1A
- Expected: Effect should remain significant
```

---

## TIER 6: Mechanistic Validation

### Test 6A: Does vs_own_par Correlate with vs_avg?
**When elite underperform vs own par, do they also underperform vs field?**

```
Correlation: vs_own_par ↔ vs_avg (Orange only, by skill tier)
  - Expected: Positive correlation (when they lose to own par, also lose to field)
```

### Test 6B: What's Driving the Underperformance?
**Is it lower scores or higher field average?**

```
Decompose for Elite Top 25% Orange:
  - Average off_par (absolute performance)
  - Average field strength (vs_avg)
  - Which changed most from non-Orange?
```

---

## Proposed Execution Order

**Week 1: Tier 1 (Foundation)**
- Test 1A: Out-of-sample validation (CRITICAL)
- Test 1B: Skill tier granularity
- Test 1C: Symmetry check

**Week 2: Tier 2 (Dimensions)**
- Test 2A-D: Condition, round type, moon, element
- Prioritize: 2A (Condition) first, then 2C (Moon)

**Week 3: Tier 3 (Comparison)**
- Test 3A: Is Orange unique?
- Test 3B: Color ranking

**Week 4: Tier 4 (Prediction)**
- Test 4A: Regression model
- Test 4B-C: Kelly sizing for actual bets

**Follow-up: Tier 5-6 (Robustness & Mechanistic)**

---

## Success Criteria

**Theory is VALIDATED if:**
1. Test 1A passes (2025/2026 out-of-sample holds)
2. Test 3A shows Orange is unique (other colors don't show this)
3. Test 4B & 4C show +EV edge > 5% for at least one direction

**Theory is PARTIALLY VALIDATED if:**
- Tests 1A-1C pass but dimension tests (2A-D) show it only works in Calm/New Moon
- (Narrows the edge but confirms the pattern in specific contexts)

**Theory is REJECTED if:**
- Test 1A fails on out-of-sample data
- Test 3A shows all colors do this (not unique to Orange)

---

## Output Format

For each test, produce:
1. **CSV**: Raw results by skill tier
2. **Summary**: One-paragraph interpretation
3. **Statistical significance**: p-value and effect size
4. **Betting implication**: If applicable, edge calculation

---

## Questions Before Running

1. **Should we test on specific tournaments only?** (e.g., majors vs regular events)
2. **Should we control for field strength?** (e.g., test only in events with elite-heavy fields)
3. **Do you want to validate on player-level data?** (i.e., does PLAYER X consistently underperform in Orange, or is it a field-level phenomenon?)
4. **Should we backtest Kelly sizing?** (i.e., if we sized bets this way in 2022, what would 2024-2026 results show?)

---

**Ready to run any subset of these tests. Which tier(s) should we prioritize?**
