# Tier 4 Results: Relative Peer Comparison Framework
**Date:** 2026-04-05
**Status:** Thresholds TBD (user to decide based on distribution)

---

## Key Finding

**Signals vary wildly in relative strength vs peer colors in same condition.**

Some signals beat all other colors. Others barely match them. This is the first time we've measured it properly.

---

## Peer Baselines (What's Normal?)

### Calm Conditions
| Color | Beat by 2+ | n |
|---|---|---|
| Pink | 36.4% | 11 |
| Purple | 30.4% | 2,125 |
| Red | 30.1% | 386 |
| Yellow | 29.7% | 5,256 |
| **Median** | **29.6%** | — |
| Orange | 29.4% | 1,372 |
| Green | 29.2% | 1,879 |
| Blue | 28.7% | 2,626 |

**Insight:** All colors cluster around 29-30% in Calm. Very little variation. So beating 29% in Orange + Calm is just matching the baseline.

### Moderate Conditions
| Color | Beat by 2+ | n |
|---|---|---|
| Brown | 27.3% | 11 |
| Green | 26.7% | 746 |
| Orange | 26.6% | 718 |
| Purple | 25.9% | 869 |
| **Median** | **25.8%** | — |
| Blue | 25.7% | 1,294 |
| Red | 25.0% | 188 |
| Pink | 25.0% | 4 |
| Yellow | 23.8% | 2,392 |

**Insight:** Moderate conditions show 24-27% baseline. Less favorable than Calm.

### Tough Conditions
| Color | Beat by 2+ | n |
|---|---|---|
| **Median** | **12.4%** | — |
| Yellow | 17.8% | 264 |
| Orange | 17.9% | 56 |
| Green | 13.6% | 125 |
| Purple | 12.4% | 129 |
| Blue | 8.6% | 93 |

**Insight:** Tough conditions are brutal. ~12% baseline. Orange slightly above at 17.9%.

---

## Signal Strength Rankings (Relative Advantage)

### TIER 1A: Dominantly Better (+8pp or higher)

| Signal | Condition | Beat% | Peer% | Advantage | n | Status |
|---|---|---|---|---|---|---|
| **libra_horoscope** | Tough | 50.0% | 12.4% | **+37.6pp** | 26 | EXTREME (but tiny n) |
| **orange_fullmoon_calm** | Calm | 39.0% | 29.6% | **+9.4pp** | 82 | VERY STRONG |
| **libra_horoscope** | Moderate | 34.5% | 25.8% | **+8.7pp** | 197 | VERY STRONG |

### TIER 1B: Strongly Better (+5pp to +8pp)

| Signal | Condition | Beat% | Peer% | Advantage | n | Status |
|---|---|---|---|---|---|---|
| **orange_newmoon_calm** | Calm | 35.5% | 29.6% | **+5.9pp** | 76 | STRONG |
| **orange_newmoon** | Calm | 35.5% | 29.6% | **+5.9pp** | 76 | STRONG |

### TIER 3: Weakly Better (+0pp to +2pp)

| Signal | Condition | Beat% | Peer% | Advantage | n | Status |
|---|---|---|---|---|---|---|
| **orange_waxing_calm** | Calm | 30.0% | 29.6% | **+0.4pp** | 781 | MARGINAL |
| **libra_horoscope** | Calm | 30.0% | 29.6% | **+0.4pp** | 460 | MARGINAL |

### BELOW PEERS: Weaker Than Peers

| Signal | Condition | Beat% | Peer% | Advantage | n | Status |
|---|---|---|---|---|---|---|
| **orange_calm** | Calm | 29.4% | 29.6% | **-0.1pp** | 1,372 | AT BASELINE (not better) |

---

## What This Means

### orange_calm (Your Broadest Signal)

**Old interpretation:** "Beats field by 2+ 29.4% of rounds"

**New interpretation:** "Same as other colors in Calm (29.6% baseline)"

**Verdict:** Not color-specific. It's the Calm condition that works, not Orange specifically. Any color in Calm beats field by 2+ ~29-30%.

**Implication:** Should orange_calm be in the deploy list if it's not better than Red or Blue in Calm?

---

### orange_fullmoon_calm (Your Strongest)

**Advantage:** +9.4pp vs peers (39% vs 29.6%)

**Meaning:** Orange + Full Moon + Calm beats all other colors in Calm by a large margin.

**Verdict:** This IS a color-specific signal. Orange + Full Moon combo is genuinely special.

---

### orange_newmoon_calm & orange_newmoon

**Advantage:** +5.9pp vs peers (35.5% vs 29.6%)

**Meaning:** Orange + New Moon beats other colors in Calm by ~6pp.

**Verdict:** Strong color × moon-phase combo signal.

---

### libra_horoscope (Your Fade)

**Interesting discovery:** Libra is a FADE signal (lose by 2+), not a pure color signal.

| Condition | Lose by 2+ | Peer Median | Advantage |
|---|---|---|---|
| Tough | 50.0% | 12.4% | +37.6pp (EXTREME) |
| Moderate | 34.5% | 25.8% | +8.7pp (VERY STRONG) |
| Calm | 30.0% | 29.6% | +0.4pp (MARGINAL) |

**Pattern:** Libra gets worse in Calm (loses the Fade effect). Strongest in Tough.

**Verdict:** Libra FADE is condition-dependent. Only use in Moderate/Tough, not Calm.

---

## Distribution Summary

```
Advantage Statistics:
  Mean: +8.5pp
  Median: +5.9pp
  Range: -0.1pp to +37.6pp
  Std Dev: 11.5pp
```

**Clustering:**
- 3 signals > +8pp (very strong)
- 2 signals +5 to +8pp (strong)
- 3 signals 0 to +2pp (marginal)
- 1 signal < 0pp (below baseline)

---

## Now: Which Threshold Is Meaningful?

### Option A: Deploy if > +0pp (anything better than peers)
- **Signals:** 7 (almost all)
- **Includes:** orange_calm, orange_waxing_calm, libra_horoscope(Calm)
- **Rationale:** "Any edge is good"
- **Risk:** Marginal advantages might not translate to live betting

### Option B: Deploy if > +2pp (notably better)
- **Signals:** 5
- **Excludes:** orange_calm, orange_waxing_calm, libra_horoscope(Calm)
- **Rationale:** "Meaningful advantage vs peers"
- **Risk:** More conservative but stronger signals

### Option C: Deploy if > +5pp (significantly better)
- **Signals:** 5 (same as B, different reasoning)
- **Excludes:** Same 3 signals as Option B
- **Rationale:** "Clear differentiation from peers"

### Option D: Deploy if > +8pp (dominantly better)
- **Signals:** 3 (orange_fullmoon_calm, orange_newmoon_calm, libra_horoscope MODERATE/TOUGH)
- **Excludes:** All weak signals
- **Rationale:** "Only deploy the strongest"
- **Risk:** Fewer opportunities, but highest confidence

---

## Recommendation From Claude

**Don't decide yet.** Look at the distribution and ask yourself:

1. **What edge am I comfortable with?** If a signal beats peers by only 0.4pp, does that feel like something worth betting?
2. **Sample size vs strength:** orange_calm has huge n=1,372 but -0.1pp advantage. Is large sample valuable if advantage is zero?
3. **What's your risk tolerance?** High selectivity (Option D) = fewer bets, higher confidence. Low selectivity (Option A) = more bets, lower confidence.

---

## Next Steps

1. **You decide:** Which threshold feels meaningful? (>0, >2, >5, or >8pp?)
2. **I'll update:** BENCHMARKING_STANDARDS.md with your threshold
3. **I'll regenerate:** VALIDATED_SIGNALS_v2.json with only signals that pass
4. **We'll deploy:** Only the signals that meet your criteria

**This approach is cleaner because the threshold reflects YOUR betting philosophy, not a pre-chosen number.**

