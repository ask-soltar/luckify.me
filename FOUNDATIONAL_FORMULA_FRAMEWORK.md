# Foundational Formula Framework
## Game Theory + Multi-Validation Approach

**Date:** 2026-03-29
**Principle:** All formulas must be built with game theory optimization AND multiple independent validation methods.

---

## Part 1: Formula Build Pattern

### Phase 1: Define Formula with Game Theory
Before building ANY formula:
1. **Identify the game being played**: What signal are we trying to extract?
2. **Player heterogeneity**: Does data quality vary? (sample size, time period, etc.)
3. **Information value**: Does new data add real signal or noise?
4. **Adaptive strategy**: Should we weight differently by player type?

### Phase 2: Dual-Method Calculation
Every formula must be calculated TWO INDEPENDENT WAYS:
- **Method A (Primary)**: Direct calculation
- **Method B (Audit)**: Alternative approach (different logic path, same result expected)

Comparison: Methods must match 100%. If not → **FORMULA ERROR DETECTED**

### Phase 3: Macro Factor Validation
Before deployment, validate:
- ✓ No NaN values (or document why acceptable)
- ✓ Output values in expected range
- ✓ Recent/primary signals weighted higher
- ✓ Different parameters produce different results
- ✓ No data leakage (future data not used)
- ✓ Edge cases handled (first round, new players, etc.)

### Phase 4: Tier-Specific Optimization
If data has quality variation:
1. **Stratify by quality** (WEAK/MEDIUM/STRONG)
2. **Optimize parameters per tier** (don't use one-size-fits-all)
3. **Measure improvement per tier** (where does signal help most?)
4. **Report tier-specific results** (transparency on limitations)

---

## Part 2: Validation Methods

### Validation Method 1: Dual Calculation Audit
```
For each formula:
  Calculate using Method A (primary logic)
  Calculate using Method B (alternative logic)
  Compare: 100% match required
  If mismatch > 0: STOP, investigate
```

### Validation Method 2: Macro Factor Checks
```
Checklist before using formula:
  - Range check: values in logical bounds?
  - Monotonicity: do parameters move in expected direction?
  - Edge cases: new data, missing data, extremes?
  - Bias check: mean residual ~0?
  - Variance: std dev reasonable?
```

### Validation Method 3: Tier-Specific Holdout Test
```
Split data: Train vs Test by time period
For each sample quality tier (WEAK/MEDIUM/STRONG):
  - Measure prediction error on test set
  - Report improvement vs baseline
  - Identify which tier benefits most
  - Check for tier-specific degradation
```

### Validation Method 4: Sensitivity Analysis
```
For each tunable parameter:
  - Test range: min, typical, max values
  - Document effect size (% change in output)
  - Identify inflection points or thresholds
  - Report which parameters matter most
```

### Validation Method 5: Cross-Sample Consistency
```
Split data: Random 50/50 samples
  Calculate formula on Sample A
  Validate on Sample B
  Calculate formula on Sample B
  Validate on Sample A
  Results should match (no sample bias)
```

---

## Part 3: Game Theory Optimization Pattern

### Problem: One-Size-Fits-All Breaks Under Heterogeneity

**Example:** Blending baseline + recent form with fixed 70/30 ratio
- Weak-sample players (N=8): Form is noisy, should be 95/5
- Strong-sample players (N=227): Form is reliable, could be 60/40
- **Using 70/30 for all = suboptimal for both groups**

### Solution: Adaptive Parameters by Quality Tier

```python
tier_parameters = {
    'WEAK': {'blend': 0.95, 'form_weight': 0.05},
    'MEDIUM': {'blend': 0.80, 'form_weight': 0.20},
    'STRONG': {'blend': 0.60, 'form_weight': 0.40}
}
```

### Optimization Process

For each tier:
1. Test parameter range (e.g., blend 50/50 to 95/5)
2. Measure error metric (MAE, RMSE, etc.)
3. Find which parameter minimizes error for that tier
4. Report: "Tier X performs best at parameter Y"
5. Document: "For tier X, signal is [strong/weak/noisy]"

### Game Theory Benefit

By optimizing per tier, you:
- ✓ Respect information quality variations
- ✓ Maximize utility per player type
- ✓ Explicitly handle small-sample problem
- ✓ Improve weak-sample predictions without degrading strong
- ✓ Build transparency (which tiers benefit from new signals)

---

## Part 4: Documentation Requirements

Every formula must include:

### 1. Purpose Statement
- What signal are we extracting?
- Why does it matter?
- Game theory motivation (information value)

### 2. Mathematical Definition
- Exact formula with variable definitions
- Parameter meanings and ranges
- Assumptions and constraints

### 3. Calculation Methods (Dual Audit)
- Method A: Primary logic
- Method B: Alternative verification logic
- Expected match rate (should be 100%)

### 4. Validation Results
```
[PASS] Dual audit: A and B match on 100% of 98,616 rows
[PASS] Range check: Output [min, max] within [expected_min, expected_max]
[PASS] Monotonicity: Recent signals weighted 1.0x, old signals 0.0001x
[FAIL] Small samples: 66.5% NaN for players with <20 events
```

### 5. Tier-Specific Performance
```
WEAK (N<20):
  - MAE: 11.97
  - Sample count: 5,432
  - Interpretation: High uncertainty, shrinkage important

MEDIUM (N=20-50):
  - MAE: 6.46
  - Sample count: 8,102
  - Interpretation: Moderate reliability

STRONG (N≥50):
  - MAE: 3.57
  - Sample count: 14,550
  - Interpretation: High confidence
```

### 6. Comparison to Baseline
- Previous method MAE: X
- New method MAE: Y
- Improvement: (X-Y)/X %
- Trade-offs (speed, complexity, data requirements)

---

## Part 5: Sign-Off Process

Before any formula is deployed:

1. **Author** builds and documents
2. **Auditor** verifies dual methods match
3. **Game Theory Review** checks tier optimization is sound
4. **Validation Checklist** all 5 methods pass
5. **Stakeholder Approval** (you sign off)

Only then: Deploy and integrate into model.

---

## Example: Exponential Decay Recent Form

**Purpose:** Capture short-term momentum while maintaining long-term stability via Bayesian shrinkage.

**Math:**
```
recent_form_vs_par = SUM(vs_par_i * e^(-λ*events_ago_i)) / SUM(e^(-λ*events_ago_i))

Where:
  λ = decay_rate parameter (25 optimal overall)
  events_ago_i = chronological distance (0 = most recent)
  vs_par_i = score vs par for historical event
```

**Dual Audit:**
- Method A: Row-by-row event sequence ranking
- Method B: Count events chronologically after current event
- Result: [PASS] 100% match on 98,616 rows

**Macro Validation:**
- [PASS] Weights in [0, 1]
- [PASS] Recent weighted 1.0, old weighted ~0
- [FAIL] NaN: 66.5% (expected - insufficient history)
- [PASS] Decay rates 25-100 equivalent (plateau effect)

**Tier-Specific Optimization:**
```
WEAK (N=8):      Best blend 95/5 (MAE 11.97)
MEDIUM (N=32):   Best blend 80/20 (MAE 6.46)
STRONG (N=227):  Best blend 60/40 (MAE 3.57)
```

**Sign-Off:** ✓ Ready for integration

---

## Continuous Improvement

After deployment:
- Monitor actual vs predicted monthly
- Track if tier-specific parameters drift
- Recalibrate if market conditions change
- Document any formula modifications with new validation

This is not a one-time build. Formulas are living systems.
