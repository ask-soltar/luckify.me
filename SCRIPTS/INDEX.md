# /SCRIPTS/ — Index of Python Analysis Scripts

Reusable Python scripts for golf analysis, backtesting, and signal validation.

---

## ✅ Active/Recommended Scripts

### Production Screener
- **`matchup_screener_v3.py`** — Main 2-ball/3-ball matchup screener with Kelly sizing

### Combo Analysis (4D Element)
- **`combo_analysis_4d_element.py`** — Analyze Color × Condition × RoundType × Element (core signal finding)
- **`combo_analysis_4d_element_recursive.py`** — Recursive dimensionality reduction

### Signal Validation
- **`backtest_color_personal_day.py`** — Train/test backtest framework
- **`k_optimization_statistical_analysis.py`** — K-value optimization for shrinkage

### Data Exploration
- **`analyze_all_dimensions.py`** — Full N-dimensional factor analysis
- **`player_scoring_system_v2.py`** — Player scoring + shrinkage calculations

---

## 🔍 By Analysis Type

### Signal Development
- `combo_analysis_4d_element.py` — PRIMARY (validated +4.6% signals)
- `combo_analysis_4d_element_recursive.py`
- `analyze_alternatives_impact.py` — Test alternative weighting schemes
- `analyze_master_numbers_matchups.py` — Master number validation

### Backtesting & Validation
- `backtest_color_personal_day.py` — Train/test split validation
- `phase_5_par_outcomes_optimized.py` — Par outcome modeling
- `k_optimization_statistical_analysis.py` — Cross-validation for parameters
- `k_optimization_loocv.py` — Leave-one-out cross-validation

### Numerology Signals
- `analyze_tournament_winners_personal_year.py` — Personal Year analysis
- `analyze_personal_year_threshold_comprehensive.py`
- `analyze_western_moons.py` — Western moon phase analysis
- `analyze_tithi_zodiac_testing.py` — Vedic calendar signals

### Element & Bucketing
- `analyze_by_element.py` — Wu Xing element breakdowns
- `analyze_collapsed_dimensions_v1.py` — Aggregate element/condition/round combos
- `analyze_data_completeness.py` — Data quality checks

### Other Analyses
- `player_scoring_system_v2.py` — Player skill shrinkage modeling
- `aggregate_and_test_top40_models.py` — Ensemble model testing

---

## 📋 All Scripts (168 total)

Full alphabetical list available via `ls -1 /SCRIPTS/` or `ls /SCRIPTS/ | wc -l`

**High-value scripts:** ~15 (marked above)
**Experimental/archived:** ~153 (may be useful as reference, test at your risk)

---

## How to Run

**Basic:**
```bash
cd /d/Projects/luckify-me
python SCRIPTS/combo_analysis_4d_element.py
```

**With arguments:**
```bash
python SCRIPTS/matchup_screener_v3.py --player "Scottie Scheffler" --rounds 50
```

**Check dependencies:**
Most scripts use:
- `pandas` — data manipulation
- `duckdb` — SQL queries
- `numpy` — math operations
- `scipy` — statistics

---

## Maintenance Notes

**Old/experimental scripts:**
Many scripts were written for earlier signal hypotheses (Color only, Element only, etc.). Not all are maintained.

**Before using a script:**
1. Check if `.py` is mentioned in `/ANALYSES/` index (currently active)
2. Scan first 10 lines for comments explaining what it does
3. Check if it references outdated column names (see GOLF_ANALYTICS_DATA_DICTIONARY.md)
4. Test on small sample first (don't process entire dataset blindly)

**To mark script as obsolete:**
Add `# DEPRECATED` to top of file, move to ARCHIVE/, update this index.

---

## Recommended Workflow

**For new analysis:**
1. Copy `combo_analysis_4d_element.py` (proven template)
2. Modify the dimensions you're testing (e.g., Color → Moon)
3. Run on `/DATA/Golf Historics v3 - ANALYSIS (7).csv`
4. Save output to `/ANALYSES/YYYYMMDD_[topic]_results.csv`
5. Document findings in `/ANALYSES/YYYYMMDD_[topic]_findings.md`

---

**Last updated:** 2026-04-04
