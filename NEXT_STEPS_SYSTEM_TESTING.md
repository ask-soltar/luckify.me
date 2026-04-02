# Next Steps: Complete 4-System Ensemble Analysis

## Problem Fixed ✓
All three system testing scripts (System 2, 3, 4) were saving only positive ROI combos.
Now updated to save **all combos** (positive, negative, zero) for accurate analysis.

---

## Checklist

### Phase 1: Run All Systems (Do This First)

- [ ] **System 2** (Exec × Upside × Gap)
  ```bash
  python system2_exec_upside_gap_testing.py
  ```
  Output files:
  - `system2_exec_upside_gap_ALL_combos.csv` ← Use this
  - `system2_exec_upside_gap_positive_only.csv` (reference)

- [ ] **System 3** (Moon × Life Path)
  ```bash
  python system3_moon_lifepath_testing.py
  ```
  Output files:
  - `system3_moon_lifepath_ALL_combos.csv` ← Use this
  - `system3_moon_lifepath_positive_only.csv` (reference)

- [ ] **System 4** (Tithi × Zodiac)
  ```bash
  python system4_tithi_zodiac_testing.py
  ```
  Output files:
  - `system4_tithi_zodiac_ALL_combos.csv` ← Use this
  - `system4_tithi_zodiac_positive_only.csv` (reference)

**Expected output:** Each system prints:
- Total combos tested
- Positive ROI count + %
- Negative ROI count + %
- Zero ROI count + %
- Average ROI (all combos)
- Top 25 combos by ROI
- Summary by condition (Calm/Moderate/Tough)

**Validation:** Expect realistic distributions like:
- System 2: ~40-50% positive, ~40-50% negative (balanced)
- System 3: ~35-45% positive, ~50-60% negative (tougher signal)
- System 4: ~30-50% positive, varying by signal quality

### Phase 2: Build Consensus (After All Systems Done)

- [ ] **Run consensus builder**
  ```bash
  python build_ensemble_consensus.py
  ```
  Output files:
  - `ensemble_consensus_scorecard.csv` ← All base combos (Condition × Round Type)
  - `ensemble_high_conviction.csv` ← Only 3/4 and 4/4 agreement
  - Console output: betting recommendations

**Expected output:**
- Table of all Condition × Round Type combinations
- For each: positive_systems (0-4), system ROIs, ensemble ROI, conviction level
- Markdown formatted recommendations for betting

### Phase 3: Validation

After consensus is built, examine:

1. **High Conviction Combos (4/4 agreement):**
   - Expected ensemble ROI: 6-8%+
   - Should only appear if all 4 systems independently found the signal
   - These are **primary betting targets**

2. **Medium Conviction (3/4 agreement):**
   - Expected ensemble ROI: 3-5%
   - One system disagrees (may be noise or measurement difference)
   - These are **secondary targets** if conviction is high enough

3. **Check system agreement:**
   - Do best signals align across systems?
   - Or does each system find different winners?
   - (Orthogonal systems → different winners is healthy)

---

## What Changed

### Before (Broken)
- Saved only positive ROI combos
- CSV showed 100% positive (misleading)
- `positive.to_csv('results.csv')`

### After (Fixed)
- Saves all combos tested
- CSV shows realistic mix (30-60% positive)
- `df_combos.to_csv('results_ALL_combos.csv')`
- Still saves positive-only backup for reference

---

## File Locations

**System Test Scripts (Fixed):**
- `system2_exec_upside_gap_testing.py`
- `system3_moon_lifepath_testing.py`
- `system4_tithi_zodiac_testing.py`

**Ensemble Builder (New):**
- `build_ensemble_consensus.py`

**Documentation (New):**
- `SYSTEM_TESTING_FIXES.md` — What was wrong and how it's fixed
- `ENSEMBLE_CONSENSUS_SCORER.md` — Full architecture + math
- `NEXT_STEPS_SYSTEM_TESTING.md` ← You are here

**Expected Outputs:**
- `system2_exec_upside_gap_ALL_combos.csv`
- `system3_moon_lifepath_ALL_combos.csv`
- `system4_tithi_zodiac_ALL_combos.csv`
- `ensemble_consensus_scorecard.csv`
- `ensemble_high_conviction.csv`

---

## Success Criteria

✓ All three systems run without error
✓ Each produces realistic positive/negative/zero distribution
✓ Ensemble consensus identifies 2-5 high-conviction (4/4) signals
✓ High-conviction ensemble ROI is 5%+ (validates game theory approach)

---

## Blocking Issues

**If any system fails to run:**
1. Check that `ANALYSIS_v3_export.csv` exists
2. Verify column names match expectations
3. Check for missing/invalid data (NaN values)

**If consensus shows no high-conviction signals:**
- Systems may have different signal strengths (expected)
- May need to lower conviction threshold to 3/4 only
- May indicate signals are weaker than baseline

---

## Remember

- These are 4 **independent, orthogonal** systems
- Each tests completely different dimensions
- High ensemble ROI comes from orthogonal agreement
- Game theory approach: consensus > single system

---

## Timeline

- Phase 1 (Run 3 systems): ~5-10 minutes
- Phase 2 (Build consensus): ~30 seconds
- Phase 3 (Validation): 15-30 minutes
- **Total:** ~30-45 minutes to complete

Ready? Start with Phase 1 ✓
