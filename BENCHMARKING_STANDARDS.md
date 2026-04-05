# Benchmarking Standards — Universal Metrics Framework
**Established:** 2026-04-05
**Status:** LOCKED (all future analysis must comply)
**Owner:** User + Claude (enforce consistency)

---

## Core Principle

**Every signal must specify:**
1. What metric is being measured
2. What threshold defines "success"
3. What baseline is being compared against
4. Why that threshold is meaningful

This prevents inconsistency (e.g., sometimes using vs_avg < 0, sometimes vs_avg < -2).

---

## Universal Metrics for Golf Signals

### Primary Metric: vs_avg (Score vs Field Average)

**Definition:** `vs_avg = player_score - course_field_average`

**Sign Convention:**
- **Negative = Good** (beat field average)
- **Positive = Bad** (lost to field average)

**Thresholds (Ranked by Confidence):**

| Threshold | Meaning | When to Use | Confidence |
|---|---|---|---|
| **vs_avg < -2** | Beat field by 2+ strokes (meaningful outlier) | Primary signal definition | HIGHEST |
| **vs_avg < -1** | Beat field by 1+ stroke (modest outperformance) | Secondary signal / context | HIGH |
| **vs_avg < 0** | Beat field by any amount (marginal) | Baseline for comparison | MEDIUM |
| **vs_avg > +2** | Lose to field by 2+ strokes (meaningful underperformance) | FADE signals (opposite direction) | HIGHEST |

**Standard to use:** `vs_avg < -2` for BET signals, `vs_avg > +2` for FADE signals

**Why:** Asymmetrical distribution in Calm shows beating field by 2+ is ~29% (vs baseline 50% for any amount). This is meaningful, not marginal.

---

### Secondary Metric: Beat Field % (Win Rate)

**Definition:** Percentage of rounds where signal condition is met

**Calculation for BET signals:**
```
beat_field_pct = 100 * (count where vs_avg < -2) / (total rounds)
```

**Calculation for FADE signals (opposite):**
```
lose_field_pct = 100 * (count where vs_avg > +2) / (total rounds)
```

**Baseline:** 50% (random chance)

**Threshold for signal validity:** > 25% (meaningful edge over baseline)

---

### Tertiary Metric: Sample Size (n)

**Minimum thresholds:**
- **n ≥ 50** — Basic signal (exploratory)
- **n ≥ 100** — Moderate confidence
- **n ≥ 300** — High confidence
- **n ≥ 1000** — Very high confidence

**For rare conditions (moon phases, specific combos):**
- Can accept n ≥ 50 if effect size is large (>35% beat rate)

---

### Quaternary Metric: Statistical Significance (p-value)

**Standard:** p < 0.05 (95% confidence)

**Relaxed standard (rare conditions only):** p < 0.10 (90% confidence)

**How to calculate:**
- For proportion (beat % vs 50% baseline): Use proportion z-test
- For mean effect (vs_avg values): Use t-test vs 0

---

### Quinary Metric: Effect Size

**Definition:** How much better/worse than baseline

**For proportion signals:** `effect = beat_field_pct - 50`
- Example: 35% beat rate = +35 percentage points vs 50% baseline

**For vs_avg signals:** `effect = mean_vs_avg`
- Example: mean vs_avg = -0.34 strokes (negative = better)

**Threshold for meaningful effect:** ≥ ±0.15 strokes or ±7.5 percentage points

---

## Benchmarking Framework (How to Apply)

### Step 1: Define the Signal
**Input:**
- Condition: e.g., "Orange + Calm"
- Metric: e.g., vs_avg
- Threshold: e.g., < -2

### Step 2: Run Analysis
**Calculate:**
1. Sample size (n)
2. Beat field % (how many rounds met threshold)
3. Mean vs_avg (average performance)
4. Statistical significance (p-value)
5. Effect size (magnitude)

### Step 3: Check Against Benchmarks

**Pass if:**
- [x] n ≥ 50 (or ≥ 100 for high confidence)
- [x] beat_field_pct > 25% (meaningful vs baseline)
- [x] p < 0.05 (statistically significant)
- [x] effect_size ≥ 0.15 (practically meaningful)

**If ANY fail:** Signal is weak, needs investigation or rejection

### Step 4: Document
**Record in VALIDATED_SIGNALS.json:**
```json
{
  "id": "signal_name",
  "metric": "vs_avg",
  "threshold": "< -2",
  "effect": -0.34,
  "beat_field_pct": 29.4,
  "n": 1372,
  "p_value": 0.000001,
  "effect_size": "+29.4pp",
  "baseline": "50% (random)"
}
```

---

## Specific Standards by Signal Type

### BET Signals (Player Outperforms Field)

**Metric:** vs_avg
**Threshold:** < -2 (beat field by 2+ strokes)
**Success criterion:** beat_field_pct > 25%
**Baseline:** 50% (random chance of beating field)

**Example (VALID):**
- orange_calm: 29.4% beat by 2+ (vs 50% baseline) → +21.3pp edge ✓

**Example (INVALID):**
- random_color: 18.0% beat by 2+ (vs 50% baseline) → -32pp (below baseline) ✗

### FADE Signals (Player Underperforms Field)

**Metric:** vs_avg
**Threshold:** > +2 (lose field by 2+ strokes)
**Success criterion:** lose_field_pct > 25%
**Baseline:** 50% (random chance of losing to field)

**Example (VALID):**
- libra_horoscope: 32.1% lose by 2+ (vs 50% baseline) → +32.1pp edge ✓

### Conditioning Signals (Condition Effects)

**Metric:** vs_avg < -2 (same as BET)
**How to test:** For each condition, calculate beat_field_pct

**Example:**
- Calm condition: 29% of all rounds beat field by 2+
- Moderate condition: 22% of all rounds beat field by 2+
- Tough condition: 18% of all rounds beat field by 2+

---

## Backward Compatibility: Past Signals

**All previously validated signals must be re-benchmarked against this standard.**

For each signal in VALIDATED_SIGNALS.json:
1. Recalculate using vs_avg < -2 threshold
2. Report new beat_field_pct
3. Check if still passes all 4 gates
4. Mark as "REVALIDATED_20260405" or "DEPRECATED_INCOMPATIBLE"

---

## Documentation Template (For All Future Signals)

Every signal must include:

```markdown
## Signal: [Name]

**Metric:** vs_avg
**Threshold:** < -2 (beat field by 2+ strokes)
**Condition:** [e.g., Orange + Calm]

**Validation Data:**
- Sample size: 1,372 rounds
- Beat field by 2+: 404 rounds (29.4%)
- Baseline: 50%
- Edge: +29.4 percentage points
- p-value: < 0.000001 (highly significant)

**Passes benchmarks?**
- [x] n ≥ 50 ✓
- [x] beat_field_pct > 25% ✓
- [x] p < 0.05 ✓
- [x] effect_size ≥ 7.5pp ✓

**Status:** VALIDATED
**Confidence:** HIGH (n=1,372)
**Recommendation:** Deploy with standard Kelly sizing
```

---

## Enforcement Rules

**For Claude (when analyzing signals):**
1. Always state threshold upfront
2. Always compare against 50% baseline (or stated baseline)
3. Always report n, beat%, p-value, effect size
4. Always check all 4 gates before declaring "valid"
5. Flag any signal using non-standard threshold

**For User (when requesting analysis):**
1. Specify desired threshold if different from vs_avg < -2
2. If requesting past signal re-analysis, ask for full benchmarking
3. If creating new signal type, request benchmark definition first

---

## Lock-In (What We're Committing To)

**Going forward, ALL signals must use:**

1. **vs_avg < -2** as primary threshold (vs_avg > +2 for FADE)
2. **Beat field % > 25%** as success criterion
3. **p < 0.05** as statistical significance bar
4. **n ≥ 50** as minimum (n ≥ 100 preferred)
5. **50% baseline** for win rate comparisons

**If a signal needs different thresholds (e.g., vs_avg < -1):**
- Must be explicitly justified and documented
- Cannot use in primary deployment without justification
- Marked as "experimental" until re-validated

---

## Review & Adjustment Schedule

**Quarterly review:** Every Jan 5, Apr 5, Jul 5, Oct 5

- Revalidate all signals against benchmarks
- If any signal drops below thresholds, flag for investigation
- If new data reveals better thresholds, update framework

**Next review:** 2026-07-05

---

## Summary

| Item | Standard | Reference |
|---|---|---|
| Primary Metric | vs_avg | Score - field avg |
| Primary Threshold | < -2 (BET) / > +2 (FADE) | Meaningful outliers |
| Success Rate | > 25% | vs 50% baseline |
| Statistical Bar | p < 0.05 | 95% confidence |
| Sample Size | n ≥ 50 (n ≥ 100 preferred) | Adequate power |
| Effect Size | ≥ 0.15 strokes or ±7.5pp | Practically meaningful |

**This is the single source of truth. All future analysis references this.**

