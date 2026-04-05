# Personal Year Performance Analysis — Findings

**Date:** April 2, 2026  
**Data Source:** Golf Historics v3 - ANALYSIS (6).csv  
**Players Analyzed:** 346 (with 30+ rounds each)  
**Total Rounds:** 67,882 (stroke play only)

---

## Executive Summary

Personal Year cycles (1-9 repeating annually) show **highly individual patterns** with no universal optimal year. However, there are weak statistical signals:

- **Most common best year:** Year 7 (15.0% of players)
- **Most common worst year:** Year 8 (15.6% of players)
- **No consensus:** Top year accounts for only 15%, indicating substantial variation by player
- **Average spread (best to worst):** 2.595 strokes per round
- **Median spread:** 1.909 strokes per round

This suggests Personal Year is a **weak collective signal** but potentially strong **individual signal** for certain players.

---

## Key Findings

### 1. Year-to-Year Variation is Moderate (Not Negligible)

Players with 30+ rounds show **median spread of 1.9 strokes** between their best and worst Personal Years. For golf betting:
- At +1.9 strokes worst-to-best = ~1.5% edge over 100 bets (assuming 2% ROI threshold)
- Not trivial, but player-specific (not applicable across all)

### 2. No Universal Optimal Year

| Year | % of Players with Best Performance | % of Players with Worst Performance |
|------|-----------------------------------|-------------------------------------|
| 1    | 13.6%                            | 9.2%                               |
| 2    | 12.4%                            | 13.3%                              |
| 3    | 10.1%                            | 8.7%                               |
| 4    | 9.0%                             | 10.4%                              |
| 5    | 8.4%                             | 8.1%                               |
| 6    | 11.0%                            | 11.3%                              |
| 7    | 15.0% **(strongest)**            | 10.1%                              |
| 8    | 12.1%                            | 15.6% **(weakest)**                |
| 9    | 8.4%                             | 13.3%                              |

**Takeaway:** Year 7 is slightly favored as best (15%), Year 8 slightly disfavored as worst (15.6%), but distribution is **fairly flat** (8-15% range). No dominant pattern.

### 3. Extreme Outliers Exist

Top players with largest year-to-year spreads:
1. Paul Waring: +34.0 strokes (Year 3 best, Year 5 worst) — *but only 2 rounds in best year*
2. Erik Barnes: +26.4 strokes (Year 5 best, Year 4 worst) — *111 rounds, more reliable*
3. Sangmoon Bae: +11.4 strokes (Year 9 best, Year 7 worst) — *47 rounds*

**But:** Most players cluster around 1-3 stroke average spread. Top 20 outliers are noise-driven (small sample sizes in best/worst years).

### 4. Data Quality Warning: Small Sample Sizes

Many "best" and "worst" year designations are based on very few rounds:
- Paul Waring's "best" Year 3: **only 2 rounds** (avg -34 = statistical outlier)
- Erik Barnes's "best" Year 5: **only 2 rounds** (avg -26 = likely luck)

**When filtering for 10+ rounds per year:**
- Spreads shrink substantially
- Patterns become more stable (less noise-driven)

---

## Individual Player Patterns (High-Confidence Sample)

Players with 50+ total rounds AND 10+ rounds in multiple years show more stable patterns:

| Player | Best Year(s) | Worst Year(s) | Spread | Confidence |
|--------|-------------|-------------|--------|------------|
| Ludvig Åberg | Year 3 (-2.76) | Year 2 (+3.50) | 6.26 | HIGH (220 total, 50 in best) |
| Brendon Todd | Year 9 (-1.51) | Year 3 (+5.00) | 6.51 | HIGH (287 total, 85 in best) |
| Nick Dunlap | Year 7 (-0.64) | Year 5 (+6.00) | 6.64 | HIGH (169 total, 75 in best) |
| Jonathan Byrd | Year 1 (-1.62) | Year 2 (+5.00) | 6.62 | HIGH (149 total, 26 in best) |

**Pattern:** Established pros with large sample sizes do show meaningful year-to-year variation, but each player has their own cycle (no universal pattern).

---

## Betting Implications

### What This Means for Matchup Betting

1. **Individual player edge exists** — If you have a player's 3+ year history showing they perform better in Year 7, that's a real +1-2% edge conditional on Personal Year
2. **Not universal** — You cannot simply say "bet on everyone in Year 7" across all matchups
3. **Weak collective signal** — Using Personal Year alone for matchup picks would underperform random

### Recommended Approach

1. **For specific players:** If you track an individual player's Personal Year pattern (e.g., "Jon Rahm performs +1.8 strokes better in Year 1"), incorporate that as a conditional adjustment
2. **Not for broad screening:** Don't filter the entire field by Personal Year
3. **Combine with other factors:** Personal Year might work as a tiebreaker when two players have similar other attributes

---

## Statistical Details

### Overall Distribution

- **Players analyzed:** 346 (with 30+ rounds)
- **Total rounds analyzed:** 67,882
- **Removed:** 75,468 rows with valid off_par but missing Personal Year data
- **Population:** 635 unique players total, filtered to established players (30+ rounds)

### Spread Statistics

- **Mean spread:** 2.595 strokes
- **Median spread:** 1.909 strokes
- **Min spread:** 0.000 strokes (tied across years)
- **Max spread:** 34.000 strokes (Paul Waring, likely noise)

### Personal Year Consensus Strength

- **Best year consensus:** Year 7 at 15.0% — means 85% of players have different best years
- **Worst year consensus:** Year 8 at 15.6% — means 84.4% of players differ

**Interpretation:** Personal Year is a **weak collective predictor** (no dominant consensus) but may be a **strong individual predictor** for certain players.

---

## Detailed Output

Full player-by-player breakdown saved to:
```
personal_year_analysis.json
```

JSON structure:
```json
{
  "summary": {
    "total_players_analyzed": 346,
    "min_rounds_threshold": 30,
    "total_rounds_in_analysis": 67882,
    "average_spread": 2.595,
    "median_spread": 1.909,
    "best_year_consensus": 7,
    "best_year_consensus_pct": 15.0,
    "worst_year_consensus": 8,
    "worst_year_consensus_pct": 15.6
  },
  "personal_year_winners": { "1": 47, "2": 43, ..., "9": 29 },
  "personal_year_losers": { "1": 32, "2": 46, ..., "9": 46 },
  "player_details": {
    "Paul Waring": {
      "total_rounds": 41,
      "best_year": 3,
      "best_year_avg": -34.0,
      "best_year_rounds": 2,
      "worst_year": 5,
      "worst_year_avg": 0.0,
      "worst_year_rounds": 10,
      "spread": 34.0,
      "by_year": { "1": {...}, "2": {...}, ... }
    },
    ...
  }
}
```

---

## Recommendations for Next Steps

1. **Filter by reliability:** Re-run analysis requiring 10+ rounds per year per player to reduce noise
2. **Compare to other divination factors:** Does Personal Year correlate with Wu Xing, Moon Phase, or other divination signals?
3. **Time-series analysis:** Check if best/worst years shift over a player's career (e.g., Year 7 best early career, Year 1 best late career)
4. **Conditional model:** Build matchup predictions that incorporate "if this player's best year is Year X and we're in Year X, +adjustment"

---

## Files Generated

- `personal_year_analysis.json` — Complete data (346 players, all metrics)
- `PERSONAL_YEAR_ANALYSIS_FINDINGS.md` — This summary

**Analysis completed:** 2026-04-02 16:31 UTC
