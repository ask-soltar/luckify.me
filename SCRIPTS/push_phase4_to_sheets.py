"""
Push corrected Phase 4 tournament placement lookup to Google Sheets
"""

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
df = pd.read_csv('tournament_placement_lookup.csv')
df = df.fillna('')

# Try to get existing worksheet, create if doesn't exist
try:
    ws = ss.worksheet('TOURNAMENT_PLACEMENT')
    ws.clear()
    print("Cleared existing TOURNAMENT_PLACEMENT sheet")
except:
    ws = ss.add_worksheet(
        title='TOURNAMENT_PLACEMENT',
        rows=len(df) + 100,
        cols=len(df.columns) + 5
    )
    print("Created new TOURNAMENT_PLACEMENT sheet")

# Push data
data = [df.columns.tolist()] + df.values.tolist()
ws.update('A1', data, value_input_option="USER_ENTERED")

print(f"Pushed {len(df)} rows to TOURNAMENT_PLACEMENT sheet")
print(f"Columns: {', '.join(df.columns)}")
