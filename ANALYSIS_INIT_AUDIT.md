# ANALYSIS v3 Init Script Audit

## Potential Issues Found

### 1. INIT_ANALYSIS_V3_SHEET() May Not Be Getting Called
- Menu item exists: "🔨 Init ANALYSIS v3 Sheet" → calls `INIT_ANALYSIS_V3_SHEET()`
- But user reports no headers appearing
- **Possible causes:**
  - User didn't click the menu item
  - Error in INIT silently failing (no error handling)
  - Script permissions issue

### 2. Populate Functions Clear Headers on First Run
- `POPULATE_ANALYSIS_V3_CHUNKED()` checks if `analysisLastRow > ANALYSIS_V3.START_ROW`
- If ANALYSIS only has headers (lastRow = 1), it won't delete (1 > 2 is FALSE) ✓ Good
- But if headers exist and data is added, subsequent runs will clear rows 2+ correctly ✓ Good

### 3. Auto-Populate Trigger May Already Be Active
- If user previously ran "▶▶ Start Auto-Populate", trigger still exists
- Even if INIT fails, trigger could still auto-populate
- **Check:** Extensions → Apps Script → Triggers (look for `POPULATE_ANALYSIS_V3_CHUNKED`)

### 4. Sheet Name Mismatch (Unlikely)
- ANALYSIS.SHEET = "ANALYSIS" ✓
- ANALYSIS_V3.SHEET = "ANALYSIS" ✓
- Both point to same sheet, so no name conflict

---

## Debug Checklist

**Step 1: Clear Everything**
```
1. Go to Google Sheets
2. Delete ANALYSIS sheet completely
3. Delete ANALYSIS_v2 sheet if it exists
4. Extensions → Apps Script → Triggers → Remove any existing POPULATE_ANALYSIS_V3_CHUNKED triggers
```

**Step 2: Check Logs for Errors**
```
1. Extensions → Apps Script
2. Click "Execution Logs" (or View → Logs)
3. Check for any error messages when you run functions
```

**Step 3: Manually Run INIT**
```
1. Menu → 📊 ANALYSIS v3 → "🔨 Init ANALYSIS v3 Sheet"
2. Wait 5 seconds
3. Check if ANALYSIS sheet appears with headers (row 1)
4. Check logs for "✓ Created ANALYSIS v3 sheet with 36 columns (A-AJ)"
```

**Step 4: If No Headers After INIT**
- There's an error in the function (likely `insertSheet()` call)
- Manual workaround: Create sheet manually in Google Sheets, then paste headers

**Step 5: Manually Run Populate**
```
1. Menu → 📊 ANALYSIS v3 → "▶ Populate (Single Batch)"
2. Wait for it to complete
3. Check logs for progress messages
```

---

## Recommended Fix

If INIT fails, the issue is likely with `ss.insertSheet(ANALYSIS.SHEET)`.

**Safe approach:**
1. Manually create "ANALYSIS" sheet in Google Sheets
2. Add header row manually (or I can provide a fix to the script)
3. Then use Populate functions

Or I can add error handling to INIT to show what's failing.

---

## Next Step

**Run the debug checklist and report:**
- Do you see ANALYSIS sheet after running INIT?
- What do the logs show?
- Are there any error messages?

