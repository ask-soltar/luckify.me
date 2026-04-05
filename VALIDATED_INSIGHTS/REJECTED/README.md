# REJECTED — Failed or Abandoned Insights

**Status:** 🔴 Failed tests, contradicted by evidence, or abandoned
**Purpose:** Archive learnings from theories that didn't pan out
**Owner:** Claude (tracks) + User (provides context)

---

## What Goes Here

Theories that:
- ❌ Failed one or more rubber stamp gates
- ❌ Contradicted by data or evidence
- ❌ Abandoned by user (intuition revised)
- ❌ Superseded by stronger theory
- ❌ Proven wrong by subsequent analysis

**This is not a failure.** Rejected theories are learning. They help refine future work.

---

## Why Keep Rejected Theories?

1. **Avoid repeating tests** — Don't test the same theory twice
2. **Learn from failure** — Document why it failed
3. **Track evolution** — See how theories changed over time
4. **Inform future work** — Rejected theories sometimes hint at better ones

---

## Template (What Each File Contains)

```markdown
---
title: [Theory Name]
status: REJECTED
confidence: 0
date_tested: YYYY-MM-DD
date_rejected: YYYY-MM-DD
failure_reason: [key reason for rejection]
test_script: /Scripts/test_[name].py
---

## Theory Statement
One clear sentence (what was being tested).

## Why It Failed

### Primary Failure
Which gate(s) failed? (stat sig, sample size, effect size, stability, luck check)

### Evidence
What the data showed (vs. what theory predicted).

### Numbers
Include test results (p-values, sample sizes, effects, etc.)

## Lessons Learned
What we discovered. Any patterns or insights for future work.

## Could It Be Salvaged?
- [ ] Different measurement approach?
- [ ] Different context (e.g., only in Tough rounds)?
- [ ] Combination with another signal?
- [ ] No — definitively ruled out

## Notes
User's reflections, intuitive takeaways, anything interesting.

## Related Theories
Links to other insights this connects to.

## See Also
[Other failed theories with similar patterns]
```

---

## Example Structure (When Tests Complete)

```
REJECTED/
├── README.md (this file)
├── purple_element_opposition_20260404.md (failed: p=0.23, too weak)
├── life_path_tournament_winner_20260405.md (failed: no stability across years)
└── moon_phase_open_round_20260406.md (abandoned: user intuition revised)
```

---

## How Rejection Works

**Not a permanent death sentence.**

```
Theory → Live Theory → Needs Testing → Test Runs → Failed ❌
                                                  ↓
                                            REJECTED
                                                  ↓
                                    (Review after 3 months)
                                           ↓
                                    (New data arrives
                                     OR user insight deepens)
                                           ↓
                                    Revisit? Refine? Combine?
                                           ↓
                                    Maybe → Live Theory (revised)
                                    OR Stay → REJECTED
```

---

## Reading Rejected Theories

When reviewing a REJECTED file:

1. **What failed?** (which gate, what numbers)
2. **Why did it fail?** (random chance, weak effect, unstable, contradiction)
3. **What's the learning?** (avoid this pattern? try alternative approach?)

Example:
- Theory: "Life Path 7 wins tournaments"
- Failed: p = 0.23 (not significant), effect size tiny (Cohen's d = 0.08)
- Learning: Life Path might not drive tournament outcomes; focus on other divinations

---

## When to Revisit

A REJECTED theory might become relevant again if:

1. **More data arrives** → Old test was underpowered
2. **User intuition shifts** → Theory re-examined with new context
3. **Related signal validates** → Makes this one worth retesting
4. **Better measurement method** → Old test was wrong approach

Process: Move from REJECTED → LIVE_THEORY (revised) → design new test

---

## Avoiding Future Rejections

Lessons from rejected theories help design better ones:

- **Be specific** ("Purple closes strong in Calm") not vague ("Purple is lucky")
- **Pick measurable things** (vs_avg, win_rate) not fuzzy (feel, luck)
- **Start with good sample** (n ≥ 50) not tiny (n = 5)
- **Pick meaningful thresholds** (5pp win rate edge) not trivial (0.1pp)

---

## No Shame in Rejection

Testing ideas is how we learn. Rejected theories show:

- You're rigorous (actually testing)
- You're not fooling yourself (accepting failures)
- You're building real knowledge (separating signal from noise)

**Keep testing.**

---

## Quick Links

- [How to Add an Insight](../HOW_TO_ADD_INSIGHT.md) — Full workflow
- [Rubber Stamp Checklist](../RUBBER_STAMP_CHECKLIST.md) — Why tests fail
- [INDEX.md](../INDEX.md) — Central registry

