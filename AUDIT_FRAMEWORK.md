# Audit Framework

**Core Principle:** Complete transparency, verifiability, and honesty in every step.
No hidden assumptions. Every calculation auditable. Every decision logged.

This is not just QA — it's game theory applied to data work.
We want the incentives aligned such that the truth is always easier than covering it up.

---

## Why This Matters (Game Theory)

In a system with hidden data or unverified transformations, bad actors (or honest mistakes) can persist undetected. The cost to find and fix them later is exponential.

**Our design:**
- Every row is traceable to its source.
- Every calculated column is formula-transparent.
- Every decision (what to keep, what to exclude, what to weight) is logged with reasoning.
- Disagreements are resolved in writing, not silently overwritten.
- A newcomer can read the audit trail and understand exactly why the data is the way it is.

This makes it **harder to cheat, easier to catch errors, and impossible to hide uncertainty.**

---

## Audit Layers

### Layer 1: Import Audit (data entry)
**Owner:** Human + checklist (DATA_INTAKE_CHECKLIST.md)
**Timing:** Before IMPORTED status
**Gate:** No data enters Golf_Analytics without passing this.

**Checks:**
- ✓ Source data is actual (receipt, link, screenshot provided)
- ✓ Column mapping is explicit (not guessed)
- ✓ Sample rows spot-checked (5+ rows vs original source)
- ✓ No duplicates introduced
- ✓ Withdrawn players handled correctly
- ✓ Totals reconcile (R1+R2+R3+R4 = Total)
- ✓ Scores are numeric, par-relative values sensible

**Artifact:** Completed DATA_INTAKE_CHECKLIST entry

---

### Layer 2: Formula Audit (engine computation)
**Owner:** Engine code (Google Apps Script)
**Timing:** During overnight run (or on-demand)
**Gate:** Engine version increments when scoring logic changes.

**What the engine writes to Golf_Analytics:**
- Columns R–U: Round colors (R1 Rhythm, etc.)
- Columns V–AG: Exec/Upside/Peak scores × 4 rounds
- Column AH: Best Upside round label

**Verification:**
- ✓ All formulas in `00_config.gs` are canonical and immutable during a run
- ✓ RUN_LOGS sheet records every execution (version, rows, duration, errors)
- ✓ `TEST_SINGLE_ROW` in menu allows re-running one row to verify output
- ✓ If engine changes, ENGINE_VERSION increments (golf_v1.0 → golf_v1.1)
- ✓ All historical runs are versioned, so you can replay any row with any past version

**Artifact:** RUN_LOGS sheet + ENGINE_SETTINGS sheet

---

### Layer 3: Data Derivation Audit (human-added columns)
**Owner:** Analyst (human)
**Timing:** As columns are added (Course Avg, vs Avg, Round Type, etc.)
**Gate:** Every new derived column has a documented formula or rule.

**Columns needing audit trail:**
- AI–AL (Course Avg R1–R4): How is field average computed? Rows included? Withdrawn excluded?
- AM–AP (vs Avg): Score − Course Avg (simple subtraction). ✓
- AU–AX (Round Type): Manually assigned? Rule-based? Document the rule.
- Moon columns: Source (10-cat lunar calendar). Document the algorithm.
- Wu Xing / Zodiac / Destiny Card / Horoscope / MoonWest / Life Path / Tithi: Source algorithm documented in PLAYERS sheet + divination engine notes.

**For each column, record:**
```
Column: [Name] ([Letter] - [Number])
Purpose: [Why do we compute this?]
Formula/Rule: [Exact logic]
Source: [Where does the input come from?]
Verification: [How do you check it's correct?]
Owner: [Who maintains this column?]
Last updated: [YYYY-MM-DD]
```

**Artifact:** COLUMN_AUDIT_TRAIL.md (to be created as new columns are added)

---

### Layer 4: Combo Analysis Audit (statistical findings)
**Owner:** Python scripts (root directory)
**Timing:** After ANALYSIS sheet is populated and locked
**Gate:** Before any signal is claimed "validated," it must pass replication test.

**Checks:**
- ✓ Sample size is adequate (n ≥ 30 for statistical claim, ideally n ≥ 100)
- ✓ Calculation is reproducible (code runs, same result every time)
- ✓ Edge cases handled (withdrawn rounds excluded? gaps = 0 or removed?)
- ✓ Confounds identified (is the signal real or just correlated with something else?)
- ✓ Out-of-sample validation attempted (does signal hold on new data?)
- ✓ Confidence interval or p-value reported (not just point estimate)
- ✓ Opposite hypothesis tested (what would disprove this?)

**When you run a combo analysis (e.g., `combo_analysis_4d_element.py`):**
1. Save output CSV with timestamp
2. Log the run: date, script, parameters, sample size, top signal found
3. Annotate findings with reasoning (why does this signal make sense?)
4. Flag limitations (small sample? many confounds? needs more data?)
5. **Do not promote to "validated" until replicated on new data**

**Artifact:** COMBO_ANALYSIS_LOG.md (to be created)

---

### Layer 5: Betting Signal Audit (real-world test)
**Owner:** Betting execution + outcomes tracking
**Timing:** Ongoing; every bet logged
**Gate:** No signal is deployed for live betting until Layer 4 passes.

**Tracking:**
- Signal name + definition (exact combo condition)
- Bet size (Kelly calculation based on edge + variance)
- Live win rate vs model prediction
- Drawdown tracking (largest losing streak)
- P&L attribution (which signals profitable? which losing?)

**Decision rule:**
- If live p&L < model confidence interval: pause, re-audit, find why.
- If discrepancy found: update Layer 3 or Layer 4 (formula or sample)
- If no error found but sample still small: accumulate more data before high confidence

**Artifact:** BETTING_LOG.md + P&L dashboard

---

## Standard Audit Checklist (Use for Any Change)

Before committing a change to any layer:

```
[ ] Why am I making this change? (write it down)
[ ] What data / code does it affect?
[ ] Have I documented the old behavior vs new?
[ ] Can someone else understand this change from the git diff + work log?
[ ] Have I tested it on a small sample first (1 row, 1 event, 5 results)?
[ ] Are there edge cases I haven't considered? (withdrawn players, zeros, NaNs?)
[ ] If this is a calculation, have I hand-checked 2–3 rows?
[ ] If this touches the engine, have I incremented ENGINE_VERSION?
[ ] Have I updated CLAUDE.md work log with "what, why, next step"?
[ ] Is there any state that's now hidden? (if yes, make it explicit)
```

---

## Rules for Living in This Framework

1. **All data is traceable.** Dedupe_Key exists so you can follow any row back to its source.
2. **All formulas are explicit.** No hidden logic in Google Sheets. If it's a formula, it's visible and auditable.
3. **All decisions are logged.** Why did you exclude this row? Why that weight? Write it in the work log.
4. **All versions are preserved.** Old ENGINE_SETTINGS entries are never deleted. RUN_LOGS is append-only. Git history is immutable.
5. **Disagreements are not resolved by deleting.** If Alice thinks a signal is real and Bob disagrees, document both positions. Test both. Don't silently overwrite one.
6. **Null is not a value.** Empty cells should be intentional (row withdrawn, data not yet collected) and labeled, not ambiguous.
7. **No hardcoded thresholds without reasoning.** When you pick a threshold (e.g., "Calm ≥ 2 rounds before betting"), explain why in a comment.
8. **Every production change is a commit + work log entry.** Not just "I changed it." Say what, why, how to revert.

---

## Sample Audit Trail (Example)

**Change:** Add "R1 GAP" column to Golf_Analytics

**Work Log Entry:**
```
### 2026-03-25 — Add R1 GAP column (BM)
**Status:** Done
**What:** Added COL_GAP_R1 = 65 (BM) to Golf_Analytics.
**Why:** Observed that players with positive R1 gaps (score much better than field avg)
         have higher R2–R4 variance. Hypothesis: calibration effect or regression to mean.
         Need to quantify this.
**How:** GAP_R1 = R1 score − Course Avg R1. Added manually via formula in Golf_Analytics.
**Validation:** Hand-checked Ramey row: R1 = 71, Course Avg R1 = 69.39, GAP = 1.61 ✓
**Next step:** Analyze GAP distribution; look for correlation with subsequent rounds.
**Reversibility:** Delete column BM to revert. Previous data unaffected.
```

**Audit Trail (to add to COLUMN_AUDIT_TRAIL.md):**
```
Column: R1 GAP (BM - 65)
Purpose: Quantify how much player outperformed field in R1
Formula: =D2 − AI2 (R1 score − Course Avg R1)
Source: Golf_Analytics D + AI
Verification: Manual spot-check on 3 rows vs. source spreadsheet
Owner: [Your name]
Last updated: 2026-03-25
Limitations: Does not account for course difficulty within season. TBD: adjust for par.
```

---

## Checklist: Before Publishing a Signal

If you claim a signal is "validated," it must pass ALL of this:

- [ ] **Data clean:** Imported via DATA_INTAKE_CHECKLIST, no duplicates, no gaps
- [ ] **Formula audited:** All derived columns (vs Avg, Round Type, etc.) documented with rules
- [ ] **Sample size:** n ≥ 30, ideally n ≥ 100 (more for rare conditions)
- [ ] **Reproducible:** Code runs, same result every time; no manual steps hidden
- [ ] **Out-of-sample test:** Signal tested on new tournament not in training set
- [ ] **Opposite hypothesis tested:** Asked "what would disprove this?" and looked for it
- [ ] **Confounds identified:** List other factors that could explain the signal (not just assert it's real)
- [ ] **Confidence interval:** Not just "45.9% win rate" but "45.9% ± 3.2% (95% CI, n=117)"
- [ ] **Limited scope:** Signal clearly states when it applies (e.g., "Closing rounds only, Calm or Moderate")
- [ ] **Documented decay:** If live testing shows degradation, note how fast and why hypothesized
- [ ] **In writing:** A sentence per point above, in FINAL_BETTING_SIGNALS.md or similar

Only then is it safe to deploy.

---

## See Also

- [DATA_INTAKE_CHECKLIST.md](DATA_INTAKE_CHECKLIST.md) — Layer 1 (import audit)
- [CLAUDE.md](CLAUDE.md) — Main reference; links here
- [FINAL_BETTING_SIGNALS.md](FINAL_BETTING_SIGNALS.md) — Layer 5 (signal audit)
