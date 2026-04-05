# PARTIALLY_BACKED — Mixed or Weak Results

**Status:** 🟠 Some tests pass; results inconclusive or weak; needs more work
**Purpose:** Archive promising but incomplete theories
**Owner:** Claude (tracks status) + User (decides if worth revisiting)

---

## What Goes Here

Theories where test results show:
- **Positive direction but weak effect** — Pattern is real but small
- **Some gates pass, some fail** — Marginally meets threshold
- **Inconclusive results** — Depends on how you measure it
- **Stable but narrow** — Works in specific context only (e.g., only in Closing rounds)
- **Need more data** — Signal is real but requires larger sample to confirm

---

## What This DOESN'T Mean

🚫 **NOT rejected:** The theory isn't disproven. Pattern exists.
🚫 **NOT invalid:** Just not strong enough for primary signals yet.
🚫 **NOT abandoned:** Can be revisited when more data arrives.

---

## Template (What Each File Contains)

```markdown
---
title: [Theory Name]
status: PARTIALLY_BACKED
confidence: 3
date_tested: YYYY-MM-DD
sample_size: [n]
---

## Theory Statement
One clear sentence.

## Test Results

### Metrics
| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| p-value | [result] | [threshold] | [✓/✗] |
| sample size | [n] | [minimum] | [✓/✗] |
| effect size | [d or diff] | [threshold] | [✓/✗] |
| stability | [holds in X conditions] | [≥2 conditions] | [✓/✗] |
| not luck | [train/test split] | [✓/✗] | [✓/✗] |

### Summary
What passed, what didn't, and why.

## Why Not Fully Validated?
Explain what's missing (small sample, weak effect, single context, etc.)

## What's Needed to Reach Validated?
- [ ] [More data from X years/condition]
- [ ] [Different measurement approach]
- [ ] [Combine with another signal to strengthen]
- [ ] [Retest in broader context]

## Notes
Anything else interesting or surprising.

## Possible Next Steps
1. Collect more data → retest
2. Modify hypothesis → test revised version
3. Shelve for later → return when domain knowledge expands
4. Move to REJECTED → evidence against theory emerging
```

---

## Examples (Will Be Added As Tests Complete)

Currently: Empty. Tests move here as they show mixed results.

---

## When to Revisit

A PARTIALLY_BACKED theory might become VALIDATED if:
- **More years of data arrive** (sample size grows)
- **Better measurement method** develops (new analysis technique)
- **Supporting evidence accumulates** (other signals strengthen it)
- **Refinement helps** (narrowing scope makes it stronger)

---

## When to Abandon

Move to REJECTED if:
- **Contradicting evidence** accumulates over time
- **Related signal disproven** (e.g., element opposition doesn't hold)
- **User intuition changes** (you no longer believe it)
- **Becomes lower priority** than other work

---

## Quick Links

- [How to Add an Insight](../HOW_TO_ADD_INSIGHT.md) — Full workflow
- [Rubber Stamp Checklist](../RUBBER_STAMP_CHECKLIST.md) — What "passing" means
- [INDEX.md](../INDEX.md) — Central registry

