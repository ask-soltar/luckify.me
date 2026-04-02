# Google Sheets Integration Setup

## Quick Reference for Pushing Data

### Authentication Method
- **Type:** Service Account (NOT OAuth)
- **Credentials File:** `luckifyme-f6c83489cd24.json`
- **Location:** `D:\Projects\luckify-me\`
- **Library:** `gspread` + `google-auth-oauthlib`
- **Why this works:** Pre-authenticated, no browser popups needed

### Target Sheet
- **Name:** Golf Historics v3
- **Sheet ID:** `1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok`
- **Tab names:** ANALYSIS_v2, RESIDUAL_TABLE, PLAYER_VOLATILITY, etc.

### Python Template (Copy-Paste Ready)

```python
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Setup
CREDS_FILE = "luckifyme-f6c83489cd24.json"
SHEET_ID = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Authenticate
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
ss = client.open_by_key(SHEET_ID)

# Load data
df = pd.read_csv('your_file.csv')
df = df.fillna('')  # IMPORTANT: Replace NaN before pushing

# Push to sheet
ws = ss.worksheet('SHEET_NAME')  # Change tab name here
data = [df.columns.tolist()] + df.values.tolist()
ws.update('A1', data, value_input_option="USER_ENTERED")

print("Done!")
```

### Installation
```bash
pip install gspread google-auth-oauthlib
```

### Gotchas & Fixes

**Issue:** `ValueError: Out of range float values are not JSON compliant`
- **Cause:** NaN or infinity values in DataFrame
- **Fix:** `df = df.fillna('')` before pushing

**Issue:** `gspread.exceptions.APIError: [400]: Requested writing within range...`
- **Cause:** Range size mismatch in batch update
- **Fix:** Push all at once instead of batches (see template above)

**Issue:** `KeyError: 'Column name'`
- **Cause:** Column name mismatch
- **Fix:** Check column names: `df.columns.tolist()`

### Common Workflows

#### Workflow 1: Replace existing sheet with new data
```python
ws = ss.worksheet('SHEET_NAME')
ws.clear()
# ... then push data as above
```

#### Workflow 2: Create new sheet if doesn't exist
```python
try:
    ws = ss.worksheet('NEW_SHEET')
    ws.clear()
except:
    ws = ss.add_worksheet(title='NEW_SHEET', rows=len(df)+100, cols=len(df.columns)+5)
# ... then push data
```

#### Workflow 3: Append to existing data (without clearing)
```python
ws = ss.worksheet('SHEET_NAME')
existing_rows = len([r for r in ws.col_values(1) if r])  # Count non-empty rows
start_row = existing_rows + 1
ws.update(f'A{start_row}', data, value_input_option="USER_ENTERED")
```

### List All Sheets
```python
for ws in ss.worksheets():
    print(ws.title)
```

### Get Sheet Stats
```python
ws = ss.worksheet('SHEET_NAME')
print(f"Rows: {ws.row_count}, Cols: {ws.col_count}")
```

---

## Current Sheets (as of 2026-03-29)

| Sheet Name | Rows | Purpose |
|-----------|------|---------|
| ANALYSIS_v2 | 98,616 | Main player analysis table |
| RESIDUAL_TABLE | 67,860 | Model residuals for calibration |
| PLAYER_VOLATILITY | 1,232 | Player uncertainty metrics |
| Golf_Analytics | ~50k | Legacy/intermediate data |

---

## For Future Sessions / Other AIs

If you need to push data to this sheet:

1. **Check if credentials file exists:** `D:\Projects\luckify-me\luckifyme-f6c83489cd24.json`
2. **Install gspread:** `pip install gspread google-auth-oauthlib`
3. **Use the template above**
4. **Remember to:** `df.fillna('')` before pushing

If authentication fails, check:
- Credentials file exists and is not corrupted
- Sheet ID is correct
- Service account has access to the sheet (share with service account email if needed)
