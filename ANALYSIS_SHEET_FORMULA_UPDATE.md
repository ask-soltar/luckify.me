# ANALYSIS Sheet Formula Update Guide

## Setup Process

1. **Clear ANALYSIS sheet** — Delete all rows (keep header)
2. **Push clean data** — Paste `Golf Historics v3 - ANALYSIS_CLEAN_NO_FORMULA_COLS.csv` (77,145 rows)
3. **Add formula columns** — Insert AI and AJ columns with formulas below

---

## Column AI — Birthday (Lookup from PLAYERS)

**Column Header:** `Birthday`

**Formula (paste in cell AI2, then fill down to row 77,146):**

```
=IFERROR(XLOOKUP(A2,PLAYERS!A:A,PLAYERS!C:C,""),"")
```

**What it does:**
- Looks up player_id in column A
- Finds matching player in PLAYERS sheet
- Returns birthday from PLAYERS column C
- Returns "" if not found

**Verification:**
- Should populate dates like `14/07/1993`
- Check 5+ rows match PLAYERS sheet

---

## Column AJ — Personal Year (Numerology Calculation)

**Column Header:** `Personal Year`

**Formula (paste in cell AJ2, then fill down to row 77,146):**

```
=IF(
  OR(AI2="",E2=""),
  "",
  LET(
    b,AI2,
    y,E2,
    mRed,MOD(MONTH(b)-1,9)+1,
    dRed,MOD(DAY(b)-1,9)+1,
    yRed,MOD(SUMPRODUCT(MID(y&"",SEQUENCE(LEN(y&"")),1)*1)-1,9)+1,
    total,mRed+dRed+yRed,
    IF(MOD(total,9)=0,9,MOD(total,9))
  )
)
```

**What it does:**
- Uses birthday (AI) and year (E) columns
- Reduces month, day, year to single digits (numerology reduction)
- Sums them and applies 9-cycle reduction
- Returns Personal Year number (1-9)

**Verification:**
- Should return numbers 1-9
- Check 5+ rows: month digits + day digits + year digits = personal year

---

## Step-by-Step Push Instructions

### Step 1: Clear ANALYSIS Sheet
1. Open Google Sheet → ANALYSIS tab
2. Select all data rows (row 2 onwards)
3. Delete all rows
4. Header row should remain intact

### Step 2: Push Clean CSV
1. Download: `Golf Historics v3 - ANALYSIS_CLEAN_NO_FORMULA_COLS.csv`
2. Open in Excel or Google Sheets desktop app
3. Select all data (Ctrl+A)
4. Copy
5. Go to Google Sheets ANALYSIS tab
6. Click cell A2
7. Paste (Ctrl+V)
8. Wait for 77,145 rows to import
9. Verify row count: should see row 77,146 as last data row

### Step 3: Add Birthday Formula (Column AI)
1. Click cell AI1
2. Type header: `Birthday`
3. Press Enter → now in AI2
4. Paste formula:
```
=IFERROR(XLOOKUP(A2,PLAYERS!A:A,PLAYERS!C:C,""),"")
```
5. Press Ctrl+Shift+End to fill down to last row
6. Or: Select AI2, then Ctrl+C, select AI2:AI77146, Ctrl+V

### Step 4: Add Personal Year Formula (Column AJ)
1. Click cell AJ1
2. Type header: `Personal Year`
3. Press Enter → now in AJ2
4. Paste formula (the long IF/LET one above)
5. Fill down to row 77,146
6. Or: Select AJ2, then Ctrl+C, select AJ2:AJ77146, Ctrl+V

### Step 5: Verify & Spot Check
1. Scroll to a few random rows
2. Spot check 5+ rows:
   - AI column has dates (from PLAYERS)
   - AJ column has numbers 1-9
3. Check Google Sheets row count matches: 77,146 (header + 77,145 data)

### Step 6: Done
- ANALYSIS sheet is now updated with clean data + formulas
- No duplicates
- Birthday and Personal Year auto-calculate

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| XLOOKUP returns error | Check PLAYERS sheet exists and has player_id in col A, birthday in col C |
| Personal Year returns error | Verify AI (Birthday) is filled, E (year) is not blank |
| Personal Year returns 0 | Should return 1-9; check formula has `IF(MOD(total,9)=0,9,MOD(total,9))` |
| Paste is slow | Normal for 77K rows; can take 2-5 minutes |
| Some rows have blank Birthday | Check PLAYERS sheet has complete data for all player_ids |

---

## Formula Logic Reference

### AI (Birthday XLOOKUP)
```
XLOOKUP(A2, PLAYERS!A:A, PLAYERS!C:C, "")
  ↓
lookup_value: A2 (player_id from ANALYSIS)
search_array: PLAYERS!A:A (player_ids in PLAYERS)
return_array: PLAYERS!C:C (birthdays in PLAYERS)
if_not_found: "" (empty string)
```

### AJ (Personal Year Numerology)
```
mRed = (Month - 1) mod 9 + 1       [reduces month to 1-9]
dRed = (Day - 1) mod 9 + 1         [reduces day to 1-9]
yRed = (sum of year digits - 1) mod 9 + 1  [reduces year to 1-9]
total = mRed + dRed + yRed
result = IF(total mod 9 = 0, 9, total mod 9)  [final reduction to 1-9]
```

Example: Birth 14/07/1993, Year 2024
```
mRed = (7-1) mod 9 + 1 = 6+1 = 7
dRed = (14-1) mod 9 + 1 = (13 mod 9) + 1 = 4+1 = 5
yRed: year=2024 → digits 2+0+2+4=8 → (8-1) mod 9 + 1 = 7+1 = 8
total = 7+5+8 = 20 → 20 mod 9 = 2 → Personal Year = 2
```

---

## After Push Complete

1. Save a clean version: **Keep `Golf Historics v3 - ANALYSIS_CLEAN.csv`** as backup
2. Update memory with new sheet state
3. If formulas need tweaking later, edit them in this document + Google Sheets

