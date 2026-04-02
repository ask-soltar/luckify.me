# System Testing Fixes — All Combos Now Saved

## Problem Identified
All four system testing scripts were filtering results to save only **positive ROI** combos, which made it appear that 100% of tested combos had positive ROI. This is statistically impossible and misleading for ensemble building.

**Example:** System 3 tested 882 combos but saved only 336 positive ROI combos, hiding 502 negative ROI combos (56.9%).

## Root Cause
Each script followed this pattern:
```python
df_combos = pd.DataFrame(all_combos)  # All combos tested
positive = df_combos[df_combos['roi'] > 0]  # Filter positive only
positive.to_csv('results.csv', index=False)  # Save filtered data
```

This means the CSV output showed artificial 100% positive distribution, not the actual mixed distribution.

## Solution Applied
All three system testing scripts (System 2, 3, 4) have been updated to:

1. **Save ALL combos** (positive, negative, zero ROI) to `system*_ALL_combos.csv`
2. **Track actual distributions** (positive %, negative %, zero %)
3. **Report statistics on complete dataset**, not just positive subset
4. **Keep positive-only backup** in `system*_positive_only.csv` for reference

## Updated Scripts
- `system2_exec_upside_gap_testing.py` ✓
- `system3_moon_lifepath_testing.py` ✓
- `system4_tithi_zodiac_testing.py` ✓

## What Each System Tests

### System 1: Round Type × Color × Element (COMPLETED)
- Baseline: Rhythm (color) × 5 Wu Xing elements
- Results: `combo_scoring_rce_all_combos.csv` (427 combos)
  - Positive: 160 (37.5%)
  - Negative: 236 (55.3%)
  - Zero: 31 (7.2%)

### System 2: Round Type × Exec × Upside × Gap
- Baseline: Execution quality × Upside potential × GAP score
- Buckets: Exec/Upside (0-25, 25-50, 50-75, 75-100), Gap (20+, 10-20, 0-10, -10-0, -20--10, <-20)
- New output: `system2_exec_upside_gap_ALL_combos.csv`

### System 3: Round Type × Moon × Life Path
- Baseline: Lunar phase (Tithi, 10 categories) × Numerological Life Path (1-9)
- Moon phases: Krishna Jaya, Krishna Bhadra, Krishna Nanda, Krishna Purna, Krishna Rikta, Shukla Purna, Shukla Rikta, Shukla Bhadra, Shukla Nanda, Shukla Jaya
- New output: `system3_moon_lifepath_ALL_combos.csv`

### System 4: Round Type × Tithi × Chinese Zodiac
- Baseline: Lunar day (Tithi, 1-30) × Astrological identity (Rat, Ox, Tiger, etc.)
- New output: `system4_tithi_zodiac_ALL_combos.csv`

## How to Run (Updated Scripts)

```bash
# Run individual systems
python system2_exec_upside_gap_testing.py
python system3_moon_lifepath_testing.py
python system4_tithi_zodiac_testing.py
```

Each script now:
1. Tests all combos
2. Prints complete statistics (positive%, negative%, zero%, mean ROI, median, std dev)
3. Saves **ALL** combos sorted by |ROI| (signal strength)
4. Saves positive-only for comparison
5. Prints top 25 combos (best signals)
6. Prints summary by condition (Calm/Moderate/Tough)

## Output Files Generated

For each system (e.g., System 2):
- `system2_exec_upside_gap_ALL_combos.csv` — Complete dataset (all ROI signs)
- `system2_exec_upside_gap_positive_only.csv` — Positive ROI only (for reference)

## Data Fields in ALL_combos CSVs
All results include:
- `condition`: Calm / Moderate / Tough
- `round_type`: Open / Positioning / Closing
- `[system-specific dims]`: Color, Element, Exec, Upside, Gap, Moon, Life Path, Tithi, Zodiac
- `n`: Sample size
- `edge`: (good_rate - bad_rate) × 100, where good = model_error ≤ -2.0, bad ≥ +2.0
- `roi`: edge × (n / (n + 50)) — Bayesian shrinkage ROI
- `conf`: HIGH (n≥30), EXPLORATORY (n≥15), WEAK (n<15)
- `mean_error`: Average model_error for this combo

## Next Steps

After running all three systems:
1. **Validate distributions** — Confirm positive/negative percentages are realistic (30-40% positive is healthy)
2. **Compare signal strength** — Identify which systems have strongest ROI signals
3. **Build consensus scorer** — Combine systems with inverse variance weighting
4. **Test ensemble** — Run combos that agreement across 2+ systems

---

**Status:** Scripts fixed ✓
**Next:** Run all three systems and validate results
**Owner:** User (Python environment available locally)
