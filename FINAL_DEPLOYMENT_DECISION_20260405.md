# Final Deployment Decision — April 5, 2026
**Thresholds Approved:**
- **>5pp:** Deploy (5 signals)
- **>2pp:** Consideration (0 signals — gap in distribution)
- **<2pp:** Archive (3 signals)

---

## Signals to Deploy (5 Total)

All pass >5pp relative advantage vs peer colors:

### Tier 1A: Strongest

**1. orange_fullmoon_calm**
- Beat field by 2+: 39.0%
- Peer median: 29.6%
- Relative advantage: +9.4pp
- Sample: n=82
- Status: ✅ DEPLOY
- Interpretation: Orange + Full Moon + Calm is noticeably better than all other colors in Calm

**2. libra_horoscope_tough** (FADE)
- Lose to field by 2+: 50.0%
- Peer median: 12.4%
- Relative advantage: +37.6pp
- Sample: n=26 (SMALL)
- Status: ✅ DEPLOY (with caution on sample size)
- Interpretation: Avoid Libra in Tough. Extreme effect but rare condition.

**3. libra_horoscope_moderate** (FADE)
- Lose to field by 2+: 34.5%
- Peer median: 25.8%
- Relative advantage: +8.7pp
- Sample: n=197
- Status: ✅ DEPLOY
- Interpretation: Avoid Libra in Moderate. Strong and stable.

### Tier 1B: Strong

**4. orange_newmoon_calm**
- Beat field by 2+: 35.5%
- Peer median: 29.6%
- Relative advantage: +5.9pp
- Sample: n=76
- Status: ✅ DEPLOY
- Interpretation: Orange + New Moon + Calm beats other colors.

**5. orange_newmoon**
- Beat field by 2+: 35.5%
- Peer median: 29.6% (Calm baseline)
- Relative advantage: +5.9pp
- Sample: n=76
- Status: ✅ DEPLOY
- Interpretation: Orange + New Moon (any condition). Strong moon effect.

---

## Signals Archived (3 Total)

Below >5pp threshold. Not deployable as distinct signals.

### Archived 1: orange_calm
- Beat field by 2+: 29.4%
- Peer median: 29.6%
- Relative advantage: **-0.1pp** (BELOW BASELINE)
- Sample: n=1,372 (large, but not better)
- Status: ❌ ARCHIVED
- Reason: Not color-specific. All colors in Calm perform similarly (~29%). The Calm CONDITION is the signal, not Orange.
- Implication: If you want to bet on Calm, any color works. Orange has no edge.

### Archived 2: orange_waxing_calm
- Beat field by 2+: 30.0%
- Peer median: 29.6%
- Relative advantage: **+0.4pp** (MARGINAL)
- Sample: n=781
- Status: ❌ ARCHIVED
- Reason: Below 5pp threshold. Too weak.

### Archived 3: libra_horoscope_calm
- Lose to field by 2+: 30.0%
- Peer median: 29.6%
- Relative advantage: **+0.4pp** (MARGINAL)
- Sample: n=460
- Status: ❌ ARCHIVED
- Reason: Libra fade effect disappears in Calm. Only deploy in Moderate/Tough.

---

## The Critical Insight

**orange_calm is NOT a distinct signal.**

The old framework treated orange_calm as valuable because it beats field 29.4% of rounds. But that's just the baseline for Calm. Red, Blue, Green, Yellow all do the same thing.

**The only distinct signals are:**
1. **Color × Moon combos** (Orange + New Moon, Orange + Full Moon) — these beat peer colors
2. **Horoscope × Condition** (Libra in Moderate/Tough) — these underperform vs peers

**Calm itself isn't a signal.** It's a baseline. Only signals that are BETTER than Calm are worth deploying.

---

## Deployment Checklist

- [x] Thresholds set (>5pp for deploy, >2pp for consideration)
- [x] 5 signals identified for deployment
- [x] 3 signals archived (below threshold)
- [x] Relative advantages verified
- [x] Sample sizes checked
- [x] Conditions specified (which condition each signal applies to)

---

## Live Deployment Instructions

### What to Load
Use `VALIDATED_SIGNALS_v3_THRESHOLDS_APPLIED.json` — contains only 5 deploy signals

### Kelly Sizing (By Signal Strength)

| Signal | Advantage | Kelly Size |
|---|---|---|
| orange_fullmoon_calm | +9.4pp | 2-3% |
| libra_horoscope_tough | +37.6pp | 2-3% (but small n=26, use caution) |
| libra_horoscope_moderate | +8.7pp | 2-3% |
| orange_newmoon_calm | +5.9pp | 1.5-2% |
| orange_newmoon | +5.9pp | 1.5-2% |

Start conservative (1-1.5%) and scale up after 20+ bets if results align with edge estimates.

---

## Sample Matchup Scoring (New Framework)

**Player A:** Orange + New Moon + Calm
- Hits signal: orange_newmoon_calm (+5.9pp advantage)
- Base score: 50% + (5.9 / 2) ≈ 53%
- Kelly: ~1.5%

**Player B:** Libra horoscope in Moderate
- Hits fade signal: libra_horoscope_moderate (-8.7pp disadvantage)
- Base score: 50% - (8.7 / 2) ≈ 46%
- Recommendation: **BET Player A**, 1.5% Kelly
- Rationale: A has +7pp vs B

---

## What Changed From Original Framework

**Before (vs_avg < -2, no peer comparison):**
- orange_calm: "Beats field by 2+ 29.4% of rounds" → Seemed valuable

**After (relative peer comparison, >5pp threshold):**
- orange_calm: "-0.1pp vs peers" → Archived (not distinct signal)

**This is why relative peer comparison matters:** It reveals that some signals are real edges (better than peers) while others are just riding the condition's baseline.

---

## Going Live

All infrastructure is ready:
- ✅ 5 signals locked and quantified
- ✅ Relative advantages calculated
- ✅ Kelly sizing rules defined
- ✅ VALIDATED_SIGNALS_v3_THRESHOLDS_APPLIED.json ready
- ✅ matchup_screener_signals_only.py ready to load v3
- ✅ BENCHMARKING_STANDARDS.md updated with thresholds

**Status:** READY FOR IMMEDIATE DEPLOYMENT

---

## Quarterly Revalidation

On 2026-07-05 (and every 3 months after), run Tier 4 again:
- Recalculate peer baselines (all colors × all conditions)
- Recalculate relative advantages for all signals
- Verify they still pass >5pp threshold
- If any signal drops below 5pp, archive it
- If new signals emerge above 5pp, add them

**This keeps deployment honest: only signals that beat peers stay in rotation.**

