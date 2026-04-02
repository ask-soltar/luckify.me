"""Push 2-ball matchup lookup to sheets"""
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

CREDS_FILE = "luckifyme-f6c83489cd24.json"
SHEET_ID = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
ss = client.open_by_key(SHEET_ID)

df = pd.read_csv('matchup_edge_lookup.csv')
df = df.fillna('')

try:
    ws = ss.worksheet('MATCHUP_EDGE_LOOKUP')
    ws.clear()
    print("Cleared existing MATCHUP_EDGE_LOOKUP sheet")
except:
    ws = ss.add_worksheet(
        title='MATCHUP_EDGE_LOOKUP',
        rows=len(df) + 100,
        cols=len(df.columns) + 5
    )
    print("Created new MATCHUP_EDGE_LOOKUP sheet")

data = [df.columns.tolist()] + df.values.tolist()
ws.update(values=data, range_name='A1', value_input_option="USER_ENTERED")

print(f"Pushed {len(df)} rows to MATCHUP_EDGE_LOOKUP")
