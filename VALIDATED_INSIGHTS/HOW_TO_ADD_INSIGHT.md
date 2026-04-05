# How to Add an Insight — Complete Workflow

**Purpose:** Step-by-step guide for submitting and validating new theories
**Audience:** User (provides theories) + Claude (structures and manages workflow)
**Last Updated:** 2026-04-04

---

## 🚀 Quick Start (3 Steps)

1. **Tell Claude the theory** — Describe what you've intuited/channeled
2. **Claude structures it** — Creates file in LIVE_THEORY/, fills template
3. **You review** — Approve or revise; then decide: test next? or keep exploring?

---

## 📝 STAGE 1: LIVE THEORY (You Provide Theory)

### What to do:
Submit theory in conversation. Include:
- **Theory name** (concise label, e.g., "Purple × Closing Bonus")
- **Origin** (intuited? channeled? observed pattern?)
- **Clear statement** (what exactly does this claim?)
- **Why you believe it** (intuitive reasoning, experience, pattern noticed)
- **Rough prediction** (what would prove/disprove it?)

### Example:
> "I've intuited that **Purple players close stronger**. When I think about Purple's traits (grounding, emotional resilience, introspection), it makes sense they'd perform better in the pressure of a closing round. I'd want to test if Purple players have higher vs_avg in Closing rounds vs. other players."

### What Claude does:
1. Creates `purple_players_close_stronger_20260404.md` in `/LIVE_THEORY/`
2. Fills LIVE_THEORY_TEMPLATE with your theory
3. Adds file to INDEX.md
4. Shares back: "Theory filed. Ready to design a test?"

### File location:
```
/VALIDATED_INSIGHTS/LIVE_THEORY/purple_players_close_stronger_20260404.md
```

### Template (Claude fills this):
```markdown
---
title: Purple Players Close Stronger
status: LIVE_THEORY
confidence: 1
date_created: 2026-04-04
last_updated: 2026-04-04
---

## Theory Statement
Purple players perform better (higher vs_avg) in Closing rounds compared to non-Purple players.

## Origin
User intuition + color rhythm theory (Purple traits: grounding, emotional resilience, introspection).

## Reasoning
Closing rounds are high-pressure. Purple's emotional stability → better composure → better execution.

## Test Plan
(To be designed)

## Results
(Pending test)
```

---

## 📋 STAGE 2: NEEDS_TESTING (Claude Designs Test)

### What happens:
After theory is in LIVE_THEORY, you decide: test now or explore more?

If **test now:**
1. Claude designs test:
   - Which data to use? (all years? recent? specific condition?)
   - What metric? (vs_avg, win rate, off_par?)
   - Sample size needed? (how many rounds?)
   - Significance threshold? (p-value, effect size)
2. Claude writes test script (or links existing analysis)
3. File moves to `/NEEDS_TESTING/` with test plan attached

### Example test plan:
```
Test: Do Purple players outperform in Closing rounds?

Data:
  - ANALYSIS v3 sheet, all years (2022-2026)
  - Filter: round_type = "Closing"
  - Compare: Purple vs. all other players

Metric:
  - vs_avg (score vs. venue field average)
  - win_rate (beat_field)

Sample:
  - Target: n ≥ 100 rounds per group
  - Expected: ~200-300 Closing rounds available

Test Method:
  - T-test (means differ?)
  - Z-test (win rates differ?)
  - Effect size (Cohen's d)

Passing threshold:
  - p < 0.10 (exploratory)
  - n ≥ 50 per group
  - Effect size ≥ 0.2 (small)
  - Result direction matches theory (positive for Purple)

Script:
  /Scripts/test_purple_closing_signal.py (Claude to write)
```

### What you do:
- Approve test plan or ask for changes
- When ready: say "run the test"
- Claude runs script, shares results

### File location:
```
/VALIDATED_INSIGHTS/NEEDS_TESTING/purple_players_close_stronger_20260404.md
```

---

## 📊 STAGE 3: TEST RESULTS (Claude Runs Analysis)

### What happens:
Claude runs test script, documents results:

**If positive** (supports theory):
- Move to `/PARTIALLY_BACKED/` or `/VALIDATED/` (depending on strength)
- Include full test results in file
- If strong enough: fill RUBBER_STAMP_CHECKLIST

**If negative** (contradicts theory):
- Move to `/REJECTED/` or `/PARTIALLY_BACKED/` (if mixed)
- Document why it failed
- Keep for learning + future reference

**If inconclusive** (marginal/unclear):
- Stay in `/PARTIALLY_BACKED/`
- Flag: "needs more data" or "needs different approach"
- Design next test

### Example result file (positive):

```markdown
---
title: Purple Players Close Stronger
status: VALIDATED
confidence: 4
date_tested: 2026-04-15
sample_size: 247
---

## Test Results

**Metric:** vs_avg (Closing rounds only)

| Group | n | mean vs_avg | std |
|-------|---|---|---|
| Purple | 68 | +0.127 | 0.89 |
| Others | 179 | -0.044 | 0.95 |
| Difference | | +0.171 | — |

**Statistical Tests:**
- t-test: t=1.82, p=0.070 ✓ (marginally significant)
- Cohen's d: 0.184 (small effect, but positive)
- 95% CI: [+0.008, +0.334]

**Win Rate:**
- Purple: 52.9% (36/68)
- Others: 48.0% (86/179)
- Difference: +4.9pp

**Stability Check:**
- 2022-2024: +0.140 vs_avg, 52.1% WR ✓
- 2025-2026: +0.156 vs_avg, 53.7% WR ✓
- Stable across time periods

## Rubber Stamp Checklist
[See attached RUBBER_STAMP_CHECKLIST]
✓ Statistical significance: p=0.070 (acceptable for exploratory)
✓ Sample size: n=247 total (✓ ≥100)
✓ Effect size: Cohen's d=0.184 (✓ small, positive)
✓ Stability: Consistent across 2022-2026
✓ Not luck: Repeatable across years

## Verdict
**VALIDATED** — Theory supported. Ready for application (e.g., use as signal modifier, player profiling).
```

---

## ✅ STAGE 4: APPROVAL (Moving to VALIDATED)

### Requirements to move file to `/VALIDATED/`:
All items in RUBBER_STAMP_CHECKLIST must pass:

1. ✓ **Statistical Significance** — p < context-appropriate threshold
2. ✓ **Sample Size** — n ≥ minimum for confidence
3. ✓ **Effect Size** — Effect is practically meaningful
4. ✓ **Stability** — Holds across multiple conditions
5. ✓ **Not Luck** — Signal is repeatable

### What you decide:
- Review results
- Agree/disagree with verdict
- If disagree: ask Claude to investigate further
- Once approved: insight is VALIDATED and ready for use

### What Claude does:
- Move file to `/VALIDATED/`
- Update INDEX.md (add to VALIDATED table)
- Link to any active signals that use this insight

---

## 🔄 STAGE 5: APPLICATION (Using Validated Insights)

### Where do insights get applied?
- **Signal Development** — Modify signals based on validated insights (e.g., adjust Purple weight in Closing combo)
- **Player Profiling** — Build player attributes using insights (e.g., "Purple players strong in Closing")
- **Analysis Stratification** — Bucket analysis by insight (test if signal differs by player color)
- **Betting Framework** — Layer insights into odds evaluation

### How it links:
```
VALIDATED_INSIGHTS/VALIDATED/
  └── purple_players_close_stronger_20260404.md
           ↓
FINAL_BETTING_SIGNALS.md
  └── "Closing round: boost Purple players by 1.5× Kelly multiplier"
           ↓
matchup_screener_v3.py
  └── score += purple_closing_boost if player.color == "Purple" and round_type == "Closing"
```

---

## 📋 QUICK CHECKLIST: Submitting a New Theory

- [ ] I have a clear theory (not vague)
- [ ] I can state it in one sentence
- [ ] I've thought about how to test it
- [ ] I know what data to use (ANALYSIS sheet? Golf_Analytics? specific years?)
- [ ] I'm ready to hear if it's wrong (and learn from it)

**If all ✓, tell Claude the theory.**

---

## 🚫 Common Mistakes (and How to Avoid Them)

### ❌ "Purple players are lucky"
**Why vague:** "Lucky" isn't measurable. Lucky at what? In what conditions?
**Fix:** "Purple players have higher vs_avg in Closing rounds"

### ❌ "All Red players perform worse"
**Why too broad:** Might be true only in certain conditions (Tough rounds? specific tournaments?)
**Fix:** "Red players underperform in Tough conditions" (more testable)

### ❌ "Master 22s win more often"
**Why incomplete:** Need context. "More often than whom? In what conditions?"
**Fix:** "Personal Day 22 players beat field more often in Calm + Closing rounds vs. other days"

### ❌ "I feel like Element signals work"
**Why not testable:** "Feel" is intuition, not theory
**Fix:** "Metal element players outperform Fire players in closing rounds (based on elemental opposition theory)"

---

## 📞 Questions?

**Q: How long does a test take?**
A: Depends on complexity. Simple (Purple in Closing) → 30 min. Complex (4D color × element × condition) → 2-4 hours.

**Q: What if my theory fails?**
A: Goes to REJECTED or PARTIALLY_BACKED. You learn why. Helps build better theories.

**Q: Can I test multiple theories at once?**
A: Yes. Have Claude queue them up. We run them in priority order.

**Q: What if I change my mind about a theory?**
A: Move it to REJECTED with note "User retraction" or "Intuition revised". No shame — part of exploration.

**Q: Can a VALIDATED insight be disproven later?**
A: Yes. If new data shows it's wrong, move it to REJECTED with updated evidence. Insights evolve as data grows.

---

## 📂 File Naming Convention

```
[theory_name_keywords]_[YYYYMMDD].md

Examples:
  - purple_players_close_stronger_20260404.md
  - element_opposition_metal_vs_fire_20260404.md
  - master_22_personal_day_signal_20260404.md
  - calm_closing_element_synergy_20260404.md
```

---

**Ready to add your first insight?**

Just describe it in conversation, and Claude will structure it.

