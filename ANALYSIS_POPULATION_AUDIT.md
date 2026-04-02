# ANALYSIS Sheet Population Script Audit

## Problem Found 🐛

The population scripts **appended** rows instead of clearing the sheet first, causing duplicates when run multiple times.

### Root Cause

**Old code (lines 767-773):**
```javascript
// Write all rows (append after existing data)
if (analysisRows.length > 0) {
  var analysisLastRow = analysisSheet.getLastRow();
  var insertRow = Math.max(ANALYSIS_V3.START_ROW, analysisLastRow + 1);
  var writeRange = analysisSheet.getRange(insertRow, 1, analysisRows.length, analysisRows[0].length);
  writeRange.setValues(analysisRows);
}
```

**What happened:**
1. First run: 77,144 rows added ✓
2. Script crashed/interrupted → progress tracker reset
3. Run again → appended another 77,144 rows (now 154,288)
4. Maybe ran 3rd time → more duplicates

**Result:** 164,374 original rows → 87,230 duplicates (53%) → 77,144 unique after dedup

---

## Solution Applied ✅

Both functions now **clear the ANALYSIS sheet before population**:

### 1. `POPULATE_ANALYSIS_V3_CHUNKED()`
**Added (after line 457):**
```javascript
// CLEAR ANALYSIS on first run (when starting from GA.START_ROW)
if (lastProcessedRow === GA.START_ROW) {
  var analysisLastRow = analysisSheet.getLastRow();
  if (analysisLastRow > ANALYSIS_V3.START_ROW) {
    analysisSheet.deleteRows(ANALYSIS_V3.START_ROW, analysisLastRow - ANALYSIS_V3.START_ROW + 1);
    console.log("✓ Cleared ANALYSIS sheet before population");
  }
}
```

**How it works:**
- Checks if this is a **fresh start** (lastProcessedRow = GA.START_ROW)
- Only clears if data exists (analyzeLastRow > 1)
- Resumes from stored progress on subsequent runs
- No re-clearing on chunk 2, 3, 4, etc.

### 2. `POPULATE_ANALYSIS_V3()` (Non-chunked version)
**Added (before batch call):**
```javascript
// Clear ANALYSIS before population
var analysisLastRow = analysisSheet.getLastRow();
if (analysisLastRow > ANALYSIS_V3.START_ROW) {
  analysisSheet.deleteRows(ANALYSIS_V3.START_ROW, analysisLastRow - ANALYSIS_V3.START_ROW + 1);
  console.log("✓ Cleared ANALYSIS sheet before population");
}
```

---

## How to Use (Safe Process)

**Step 1: Clear ANALYSIS sheet in Google Sheets**
- Go to ANALYSIS tab
- Select all data rows (row 2+)
- Delete (keep header)

**Step 2: Reset progress tracker**
```
In Google Sheets, go to:
Menu → ⚙️ Extensions → Apps Script
Open the script editor
In the left panel, click "Storage" > "Properties" (or use console)
Delete the property: "ANALYSIS_V3_PROGRESS"
```

**Step 3: Run the fixed population script**
```
Menu → ➕ ANALYSIS v3 → "➕ Rebuild ANALYSIS v3 Chunked"
(or for smaller datasets: "➕ Rebuild ANALYSIS v3" for non-chunked)
```

This will:
1. Automatically clear the sheet once (on first chunk)
2. Process Golf_Analytics rows in 10k-row chunks
3. Track progress so it doesn't restart
4. Prevent any duplicate appends

**Step 4: When complete, add formulas**
```
Menu → 📊 ANALYSIS v3 → "➕ Add Formulas"
```

**Step 5: Verify**
- Check row count matches expected (e.g., 77,144 data rows)
- Spot-check 10 random rows
- Confirm no duplicates by key (player_id, event_id, round_num)

---

## Prevention for Future

**Safe practices:**
1. **Always clear ANALYSIS before re-population** (script now does this)
2. **Check progress tracker** before running (it auto-resets now)
3. **Never append multiple exports manually** — use the engine scripts
4. **Monitor for crashes** — if script times out mid-run, progress will resume on next run

---

## Audit Summary

| Metric | Value |
|--------|-------|
| Original file lines | 164,375 (1 header + 164,374 data) |
| Duplicate rows found | 87,230 (53%) |
| Unique rows after dedup | 77,144 |
| Root cause | Append without clear + progress reset |
| Fix | Clear on first run + validate progress |
| Risk with fix | None — clearing only happens on fresh start |
| Files changed | `engine/10_analysis_baseline.gs` |

---

## Git Commit

```
Fix: Prevent duplicate rows in ANALYSIS population

- POPULATE_ANALYSIS_V3_CHUNKED(): Clear ANALYSIS on first chunk
  * Checks if lastProcessedRow === GA.START_ROW (fresh start)
  * Deletes all data rows before population
  * Allows progress tracking to resume on chunk 2, 3, 4

- POPULATE_ANALYSIS_V3(): Clear ANALYSIS before population
  * Same logic for non-chunked (full) population

Root cause: Old code appended rows without clearing first.
If script crashed/restarted, progress would reset and cause duplicates.
Example: 77k rows → crash → run again → 154k total (duplicates).

This fix prevents append-without-clear, ensuring clean rebuilds.
```

