# NEEDS_TESTING — Ready to Validate

**Status:** 🟡 Test plan designed; test not yet run
**Purpose:** Queue theories awaiting analysis
**Owner:** Claude (manages test queue) + User (provides priorities)

---

## What Goes Here

Theories that are:
- **Clear and defined** (moved from LIVE_THEORY after refinement)
- **Test plan attached** (Claude has designed the analysis)
- **Script ready** (Python script exists or will be written before test runs)
- **Ready to run** (waiting for user to say "go")

---

## How Theories Get Here

1. Theory in LIVE_THEORY
2. You say "let's test this"
3. Claude designs test plan → file moves here with plan attached
4. You approve test plan or request changes
5. Once approved → test runs

---

## Template (What Each File Contains)

```markdown
---
title: [Theory Name]
status: NEEDS_TESTING
confidence: 2
date_designed: YYYY-MM-DD
test_script: /Scripts/test_[name].py
---

## Theory Statement
One clear sentence.

## Test Plan

### Data Source
Which data to use (ANALYSIS v3, Golf_Analytics, specific years)

### Metric
What to measure (vs_avg, win_rate, off_par, etc.)

### Sample Definitions
How to split groups (Purple vs. Others, etc.)

### Passing Thresholds
- p-value: [threshold]
- sample size: [minimum]
- effect size: [minimum]
- other gates: [as applicable]

## Execution

### To run this test:
1. Claude runs: `python /Scripts/test_[name].py`
2. Results saved to: `/Scripts/test_[name]_RESULTS.csv`
3. Analysis saved to: `/VALIDATED_INSIGHTS/test_[name]_REPORT.md`

### Expected time: [duration]

## Next Steps
- [ ] User approves test plan
- [ ] Claude runs test
- [ ] Results reviewed
- [ ] Move to PARTIALLY_BACKED or VALIDATED
```

---

## Current Queue

None yet. Theories move here as you decide to test them.

---

## What Happens Next

When test runs:

- **Passes all gates** → Move to VALIDATED
- **Passes most gates** → Move to PARTIALLY_BACKED (needs more work)
- **Fails key gates** → Move to REJECTED (with analysis why)
- **Inconclusive** → Stay here with note "needs different approach"

---

## Quick Links

- [How to Add an Insight](../HOW_TO_ADD_INSIGHT.md) — Full workflow
- [Rubber Stamp Checklist](../RUBBER_STAMP_CHECKLIST.md) — What "passing" means
- [INDEX.md](../INDEX.md) — Central registry

