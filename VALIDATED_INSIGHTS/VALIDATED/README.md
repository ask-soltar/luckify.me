# VALIDATED — Approved Insights

**Status:** 🟢 Passes all rubber stamp gates; ready for use
**Purpose:** Archive approved insights used in signals, analysis, player profiling
**Owner:** Claude (maintains list) + User (decides applications)

---

## What Goes Here

Theories that:
- ✅ Pass all 5 rubber stamp gates
- ✅ Are repeatable and real (not luck)
- ✅ Have meaningful practical effect
- ✅ Have adequate sample size
- ✅ Are statistically significant
- ✅ Stable across conditions

These are **approved for use in:**
- Betting signals (as modifiers or primary signals)
- Player profiling (as attributes)
- Analysis stratification (as filters)
- Betting framework decisions

---

## Template (What Each File Contains)

```markdown
---
title: [Theory Name]
status: VALIDATED
confidence: 4
date_validated: YYYY-MM-DD
test_script: /Scripts/test_[name].py
---

## Theory Statement
One clear sentence.

## Key Finding
The headline result in plain language.

## Statistical Summary

| Gate | Result | Threshold | Status |
|------|--------|-----------|--------|
| Statistical Significance | p=X | p < Y | ✓ |
| Sample Size | n=X | n ≥ Y | ✓ |
| Effect Size | d=X or WR=+Xpp | ≥ threshold | ✓ |
| Stability | Holds in [contexts] | ≥ [contexts] | ✓ |
| Not Luck | Test/Train ratio | ≥ 70% | ✓ |

## RUBBER STAMP CHECKLIST
[Full checklist from testing; all gates marked ✓]

## How to Use This Insight

### In signals:
[Example: "Boost Purple players by 1.5× Kelly multiplier in Closing rounds"]

### In player profiling:
[Example: "Add 'Purple closing strength' attribute to player models"]

### In analysis:
[Example: "Stratify combo analysis by color in Closing rounds"]

## Data Snapshots
[Show actual results from test: means, sample sizes, p-values]

## Out-of-Sample Validation
[Show how test set performed vs. training set]

## Notes
Any caveats, context-specificity, or important details.

## Related Insights
Links to other validated insights that work with this one.
```

---

## Current Validated Insights

**None yet. First theories will populate this section as they pass validation.**

---

## Applications

Once an insight is VALIDATED, it can be:

1. **Added to FINAL_BETTING_SIGNALS.md**
   - Example: "Purple × Closing = +1.5× Kelly boost"

2. **Built into player profiling**
   - Example: Player attribute = "closing strength" (if Purple)

3. **Used to stratify analysis**
   - Example: "Separate combo analysis by color in Closing rounds"

4. **Layered into scoring models**
   - Example: Adjust Upside/Exec scoring for color in condition

---

## Maintenance

**Claude maintains:**
- Accurate test script references
- Links to supporting analyses
- Updated confidence assessments if new contradicting data arrives

**User decides:**
- Whether to use this in signals
- Whether to combine with other insights
- Whether to deprioritize if conflicting signals emerge

---

## Moving Back Out

A VALIDATED insight can be:

**Demoted to PARTIALLY_BACKED** if:
- New data shows weaker effect than original test
- Contradicting evidence in new tournament subset
- Stability degrades over time

**Moved to REJECTED** if:
- Strong contradicting evidence arrives
- Original test is found to be wrong
- User intuition shifts decisively against it

When this happens, file moves to REJECTED with explanation.

---

## Quick Links

- [How to Add an Insight](../HOW_TO_ADD_INSIGHT.md) — Full workflow
- [Rubber Stamp Checklist](../RUBBER_STAMP_CHECKLIST.md) — What "passing" means
- [INDEX.md](../INDEX.md) — Central registry
- [FINAL_BETTING_SIGNALS.md](../../FINAL_BETTING_SIGNALS.md) — Where signals are deployed

