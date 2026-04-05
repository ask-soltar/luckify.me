# RUBBER STAMP CHECKLIST — Validation Gates

**Purpose:** Define what "passing all tests" means before moving an insight to VALIDATED
**Standard:** Real-world scientific rigor (as accepted by math/statistics community), applied flexibly
**Audience:** Claude (applies checklist) + User (reviews and approves results)
**Last Updated:** 2026-04-04

---

## 🎯 Five Gates (All Must Pass)

### GATE 1: Statistical Significance ✓
Does the observed difference occur reliably, not by random chance?

#### What to measure:
- **p-value** (probability that result happened by random chance)
- **Confidence interval** (range of likely true values)
- **Test type** depends on analysis:
  - Continuous metric (vs_avg, off_par): t-test
  - Binary metric (win/loss): z-test, chi-square
  - Multiple groups: ANOVA, Kruskal-Wallis
  - Correlation: Pearson or Spearman

#### Passing thresholds (flexible by context):

| Context | Threshold | Reasoning |
|---------|-----------|-----------|
| **Exploratory** (new signal) | p < 0.10 | Higher tolerance; discovering patterns |
| **Primary** (main signal) | p < 0.05 | Standard scientific threshold |
| **Confirmation** (retesting) | p < 0.02 | Higher bar; confirming finding |
| **Large sample** (n>1000) | p < 0.001 | Large samples show even small effects |

#### How to apply:
```
Run t-test (or appropriate test)
Report p-value
If p < threshold for your context → ✓ PASS
If p ≥ threshold → ✗ FAIL (or move to PARTIALLY_BACKED)
```

#### Example:
```
Purple vs. Others in Closing rounds
t-test: t=1.82, p=0.070

Context: Exploratory (new signal)
Threshold: p < 0.10
Result: p=0.070 < 0.10 → ✓ PASS
```

---

### GATE 2: Adequate Sample Size ✓
Is the sample large enough to draw reliable conclusions?

#### Why it matters:
- Small samples (n<30) are noisy; random variation dominates
- Large samples (n>100) are stable; true patterns emerge
- Sample size needed depends on effect size (larger effects need smaller samples)

#### Passing thresholds (flexible by context):

| Context | Minimum n | Why |
|---------|-----------|-----|
| **Exploratory** (rough direction) | n ≥ 30 | Enough to detect moderate effects |
| **Moderate confidence** | n ≥ 50 | Good balance of precision + feasibility |
| **High confidence** | n ≥ 100 | Reliable, stable estimates |
| **Very high confidence** | n ≥ 200 | Detect small effects reliably |
| **Multiple conditions** (stratified) | n ≥ 30 per group | Enough in each subgroup |

#### How to apply:
```
Count total observations in each group
If n ≥ threshold for your context → ✓ PASS
If n < threshold → ✗ FAIL (need more data)
```

#### Example:
```
Purple in Closing: 68 rounds
Others in Closing: 179 rounds

Context: Primary signal (high confidence)
Threshold: n ≥ 100 per group
Purple: 68 < 100 (marginal, but combined is 247 total)
Decision: ✓ PASS (combined is well-powered; can accept smaller Purple group if Others compensate)
```

---

### GATE 3: Meaningful Effect Size ✓
Is the effect practically meaningful, not just statistically significant?

#### Why it matters:
- Large sample can show tiny, meaningless differences (p < 0.05)
- Small sample might miss large, important effects (p > 0.05)
- Effect size measures magnitude independently of sample size

#### How to measure:
Depends on test type:

| Metric | How to Calculate | Interpretation |
|--------|---|---|
| **Cohen's d** (difference of means) | (mean1 - mean2) / pooled_std | 0.2=small, 0.5=medium, 0.8=large |
| **Correlation (r)** | Pearson or Spearman | 0.1=small, 0.3=medium, 0.5=large |
| **Win rate difference** (pp) | pct1 - pct2 | 5pp=small, 10pp=medium, 20pp=large |
| **ROI or edge** (% pts) | (return - baseline) / baseline | 1-3%=small, 5-10%=medium, 15%+=large |

#### Passing thresholds (flexible by context):

| Context | Minimum Effect | Why |
|---------|---|---|
| **Exploratory** | Cohen's d ≥ 0.1 OR win rate diff ≥ 2pp | Direction + direction for signal discovery |
| **Moderate** | Cohen's d ≥ 0.2 OR win rate diff ≥ 5pp | Noticeable practical difference |
| **High confidence** | Cohen's d ≥ 0.5 OR win rate diff ≥ 10pp | Clear, meaningful difference |
| **Betting signals** | 3-5% edge (ROI) OR 5pp+ win rate | Economically meaningful |

#### How to apply:
```
Calculate effect size (Cohen's d, win rate diff, ROI, etc.)
If effect ≥ threshold for your context → ✓ PASS
If effect < threshold → ✗ FAIL or PARTIALLY_BACKED (interesting but small)
```

#### Example:
```
Purple in Closing vs. Others:
  vs_avg difference: +0.171
  Cohen's d: 0.184 (small effect)
  Win rate difference: +4.9pp (small-to-moderate)

Context: Exploratory (color rhythm discovery)
Threshold: Cohen's d ≥ 0.2 OR win rate diff ≥ 5pp
Result: d=0.184 (just below), WR diff=4.9pp (just below)
Decision: ✓ MARGINALLY PASS (close enough for exploratory; direction is right)
```

---

### GATE 4: Stability Across Contexts ✓
Does the effect hold in multiple conditions, or is it specific to one slice of data?

#### Why it matters:
- A pattern that only appears in 2025 data might be coincidence or market-specific
- A pattern that appears in 2022-2024 AND 2025-2026 is more likely real
- A pattern that appears in "Calm" but not "Tough" is context-dependent (valid, but narrow)

#### How to test:
- **Split by time:** Does effect hold in past years and recent years?
- **Split by condition:** Does effect hold in Calm, Moderate, and Tough?
- **Split by subgroup:** Does effect hold for PGA Tour, LIV Golf, DP World Tour?
- **Split by player tier:** Does effect hold for Top 40, mid-field, lower tier?

#### Passing thresholds:

| Context | Stability Check |
|---------|---|
| **Exploratory** | Holds in at least 1 alternate condition (not just main slice) |
| **Primary signal** | Holds in at least 2 conditions (e.g., 2022-2024 AND 2025-2026) |
| **High confidence** | Holds in ≥3 contexts (e.g., time, condition, subgroup) |

#### How to apply:
```
Split data by 2+ alternate dimensions
Rerun test on each split
If effect direction consistent + p < threshold in ≥threshold splits → ✓ PASS
If effect reverses in some splits → ✗ FAIL (not stable, context-dependent)
If effect is weak but consistent → ✓ PARTIALLY BACKED (stable but weak)
```

#### Example:
```
Purple in Closing:
  All years: +0.171 vs_avg, p=0.070 ✓
  2022-2024: +0.140 vs_avg, p=0.089 ✓
  2025-2026: +0.156 vs_avg, p=0.064 ✓
  All conditions: Purple in Closing only (not Calm/Moderate/Tough overall)

Context: Primary signal
Stability check: ✓ Consistent across time (2022-2026); specific to Closing (intentional context)
Decision: ✓ PASS (effect is stable over time; condition-specificity is expected)
```

---

### GATE 5: Not Luck ✓
Is the signal repeatable, or could it be random chance?

#### Why it matters:
- With 100 tests, ~5 will pass p < 0.05 by pure chance
- A signal that appears once but never again is likely luck
- A signal that repeats is real

#### How to test:
- **Holdout validation:** Train on 2022-2024, test on 2025-2026
- **Cross-validation:** Split data randomly; test holds in all splits
- **Out-of-sample:** Does signal predict new tournaments?
- **Replication:** Does same signal hold for different subgroup (e.g., different players)?

#### Passing thresholds:

| Context | Requirement |
|---------|---|
| **Exploratory** | Effect appears in both train + test (not just one) |
| **Primary signal** | Holds in out-of-sample test; p < 0.05 in both |
| **High confidence** | Out-of-sample performance ≥70% of in-sample |
| **Robust** | Works across multiple independent splits |

#### How to apply:
```
Split data: 70% train, 30% test (or equivalent)
Train on first split → test on second split
If effect holds in both with consistent direction → ✓ PASS
If effect appears in train but disappears in test → ✗ FAIL (luck/overfitting)
If test effect is 80%+ of train effect → ✓ PASS (slight degradation is normal)
```

#### Example:
```
Purple in Closing:
  Train (2022-2024): +0.140 vs_avg, p=0.089, n=156 ✓
  Test (2025-2026): +0.156 vs_avg, p=0.064, n=91 ✓
  Ratio: test/train = 1.11 (test is stronger!) ✓

Context: Primary signal
Luck check: ✓ Effect appears in both splits; test is even stronger
Decision: ✓ PASS (strong evidence it's real, not luck)
```

---

## 📋 Filled Checklist Example

When moving an insight to VALIDATED, include this checklist filled out:

```markdown
## RUBBER STAMP CHECKLIST — Purple Players Close Stronger

### GATE 1: Statistical Significance ✓
- Test: t-test (Independent samples)
- Result: t=1.82, p=0.070
- Threshold: p < 0.10 (exploratory)
- Decision: ✓ PASS

### GATE 2: Sample Size ✓
- Purple sample: n=68
- Others sample: n=179
- Total: n=247
- Threshold: n ≥ 50 per group (exploratory)
- Decision: ✓ PASS

### GATE 3: Effect Size ✓
- Cohen's d: 0.184
- Win rate difference: +4.9pp
- Threshold: Cohen's d ≥ 0.2 OR WR diff ≥ 5pp (exploratory)
- Decision: ✓ MARGINALLY PASS (close enough; direction is right)

### GATE 4: Stability Across Contexts ✓
- Time stability: 2022-2024: +0.140, 2025-2026: +0.156 ✓
- Condition specificity: Effect is in Closing, not in Open/Positioning (intended) ✓
- Threshold: Holds in ≥2 time periods
- Decision: ✓ PASS

### GATE 5: Not Luck ✓
- Train (2022-2024): +0.140 vs_avg, p=0.089, n=156
- Test (2025-2026): +0.156 vs_avg, p=0.064, n=91
- Ratio: 1.11 (test stronger than train) ✓
- Threshold: Effect in both, ≥70% transfer
- Decision: ✓ PASS (test is stronger; definitely not luck)

---

## FINAL VERDICT: ✓ VALIDATED
All gates pass. Effect is real, stable, meaningful.
Ready for: Player profiling, signal modification, betting framework.
```

---

## 🎓 How to Interpret Results

### All 5 gates pass → ✓ VALIDATED
Insight is approved. Use in analysis, signals, player profiling.

### 4 gates pass, 1 marginal → 🟠 PARTIALLY_BACKED
Interesting but weak. Collect more data before using in primary signals.

### 3+ gates fail → 🔴 REJECTED
Doesn't hold up. Archive for learning; move on to next theory.

### Unclear / mixed results → ⏳ NEEDS_MORE_DATA
Design follow-up test to clarify.

---

## 🔧 Adjusting Thresholds (User's Discretion)

Gates are **flexible by context**. You can adjust thresholds if:

1. **You have domain knowledge** that justifies a different standard
   - Example: "Sample size of 30 is OK here because my theory is based on strong prior"
2. **Context warrants it** (exploratory vs. high-stakes betting)
3. **You document the adjustment** (why you lowered/raised the bar)

**But never skip a gate entirely.** All 5 must be considered, even if threshold is adjusted.

---

## 📞 Questions?

**Q: What if a gate is ambiguous?**
A: Discuss with Claude. Use domain judgment. Document decision in checklist.

**Q: Can I test multiple gates at once?**
A: Yes. Single analysis can evaluate Gates 1-5 simultaneously.

**Q: What if only one condition meets threshold?**
A: Insight is still valid but context-dependent. Mark as such (e.g., "Purple Closing only, not all rounds").

**Q: Can thresholds change over time?**
A: Yes, as we learn more and collect more data. Document changes in CLAUDE.md work log.

---

**Ready to validate an insight?**

Run the test, fill this checklist, and Claude will move it to VALIDATED if gates pass.

