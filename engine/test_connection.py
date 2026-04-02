import gspread
from google.oauth2.service_account import Credentials
import os

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID   = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES     = ["https://www.googleapis.com/auth/spreadsheets"]

creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
ss     = client.open_by_key(SHEET_ID)

print("Connected! Sheets found:")
for ws in ss.worksheets():
    print(f"  - {ws.title}")
