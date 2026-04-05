# /DATA/ — Index of Reference Data Files

Golf tournament data exports, analysis sheets, and lookup tables.

---

## 🔴 PRIMARY DATA FILE

**`Golf Historics v3 - ANALYSIS (7).csv`**
- **Rows:** 62,215 golf rounds (filtered to valid conditions + tournament types)
- **Columns:** 37 (player, event, scores, colors, conditions, moon, numerology, etc.)
- **Years:** 2022–2026
- **What it is:** Main analysis dataset. Use this for all signal testing.
- **Updated:** 2026-04-04 (after Color × Personal Day analysis)

---

## Analysis Exports

### Main Analysis Sheet Exports
- `ANALYSIS_v3_export.csv` — Full ANALYSIS sheet export (all 34 columns)
- `ANALYSIS_v3_RESCORED.csv` — Rescored with updated K values
- `ANALYSIS_v3_CLEAN.csv` — Cleaned duplicate-removed version
- `ANALYSIS_v3_CLEAN_NO_FORMULA_COLS.csv` — Formulas removed (data only)

---

## 2-Ball & 3-Ball Scoring Data

- `2ball_golf_historics_scoring.csv` — 2-ball matchup scores
- `2ball_scored_*.csv` (v1, v2, 35_65, 35_65_with_tough) — Various scoring iterations
- `3ball_roi_audit.csv` — 3-ball ROI audit

---

## Element & Combo Data

- `analysis_v2_with_*.csv` — Analysis with added dimensions:
  - `*_element.csv` — Wu Xing element
  - `*_moon.csv` — Moon phase
  - `*_horoscope.csv` — Western horoscope
  - `*_life_path.csv` — Numerology life path
  - `*_moonwest.csv` — Western moon (8-cat)
  - `*_chinese_zodiac.csv` — Chinese zodiac

---

## JSON Reference Data

- `combo_analysis_summary.json` — 4D Element combo metrics (from most recent analysis)
- `personal_year_analysis.json` — Personal Year distribution analysis
- `player_personal_year_weighted_analysis.json` — Player × personal year weighted scores

---

## How to Use

**For all analyses:**
```python
import pandas as pd
df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (7).csv')
```

**With standard filters:**
```python
# Apply recommended filters
df = df[df['condition'].isin(['Calm', 'Moderate', 'Tough'])]
df = df[df['round_type'].isin(['Open', 'Positioning', 'Closing', 'Survival'])]
df = df[df['tournament_type'].isin(['S', 'NS'])]
# Result: ~62k rows (79.5% of original)
```

**For DuckDB (recommended for speed):**
```sql
SELECT * FROM 'DATA/Golf Historics v3 - ANALYSIS (7).csv'
WHERE condition IN ('Calm', 'Moderate', 'Tough')
  AND round_type IN ('Open', 'Positioning', 'Closing', 'Survival')
  AND tournament_type IN ('S', 'NS')
LIMIT 100;
```

---

## Column Reference

**For column definitions, see:** `GOLF_ANALYTICS_DATA_DICTIONARY.md` (root)

**Quick reference:**
- Columns A–F: player, event, year, round details
- Columns G–I: scores (score, par, course_avg)
- Columns J–O: performance metrics (vs_avg, condition, round_type, color, exec, upside)
- Columns P–Z: divination (moon, element, zodiac, life_path, tithi, gap, tour, best_round)
- Columns AA–AH: calculated metrics (player_hist_par, off_par, buckets, adj_his_par, tournament_type)

---

## Data Integrity Notes

⚠️ **Known issues:**
- Some old versions have duplicate rows (use CLEAN version if issues occur)
- Personal Day numbers (numerology) only exist for certain date ranges (2025-2026 may have gaps)
- Tough conditions are underrepresented (only ~2.3k of 62k rows)

✓ **Validated:**
- No missing values in core columns (score, course_avg, condition)
- All player names match PLAYERS sheet
- All event names match EVENTS sheet
- Condition values are exactly: Calm, Moderate, Tough

---

## Managing Data Files

**Best practices:**
1. Don't modify CSVs in place (create copies for analysis)
2. Use CLEAN versions if you encounter duplicates
3. Always apply standard filters before analysis (condition, round_type, tournament_type)
4. Reference `Golf Historics v3 - ANALYSIS (7).csv` as the canonical source

**Adding new data:**
When new tournaments are analyzed:
1. Export from ANALYSIS sheet as new CSV
2. Name: `Golf Historics v3 - ANALYSIS (8).csv`
3. Update this index
4. Update scripts to reference new file

---

**Last updated:** 2026-04-04
**File count:** 122 total CSVs + JSONs
