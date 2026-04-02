#!/usr/bin/env python3
"""
Add 'moon' column to ANALYSIS_v2 sheet.

Uses the pre-computed moon column from analysis_v2_with_moon.csv
(moon = Moon R{round_num} selected by round number).
"""

import os
import sys
import time
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE     = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID       = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES         = ["https://www.googleapis.com/auth/spreadsheets"]
ANALYSIS_SHEET = "ANALYSIS_v2"


def main():
    print("Authenticating ...")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    # Load pre-computed moon data from CSV
    csv_path = os.path.join(BASE_DIR, "analysis_v2_with_moon.csv")
    print(f"Loading moon column from {csv_path} ...")

    if not os.path.exists(csv_path):
        print("ERROR: CSV not found. Run add_moon_to_analysis.py first.")
        sys.exit(1)

    df = pd.read_csv(csv_path)

    # Create moon column (round-specific)
    def get_moon(row):
        round_num = row["round_num"]
        if pd.isna(round_num):
            return ""
        round_num = int(round_num)
        if round_num == 1:
            return str(row.get("Moon R1", "")).strip()
        elif round_num == 2:
            return str(row.get("Moon R2", "")).strip()
        elif round_num == 3:
            return str(row.get("Moon R3", "")).strip()
        elif round_num == 4:
            return str(row.get("Moon R4", "")).strip()
        return ""

    df["moon"] = df.apply(get_moon, axis=1)

    matched = (df["moon"] != "").sum()
    print(f"  Computed moon column for {matched} / {len(df)} rows")

    # Open sheet and expand columns if needed
    print(f"Opening {ANALYSIS_SHEET} ...")
    ws = ss.worksheet(ANALYSIS_SHEET)

    current_cols = ws.col_count
    if current_cols < 24:
        ws.add_cols(24 - current_cols)
        print(f"  Expanded to 24 columns")
        time.sleep(0.5)

    # Update header
    print(f"Adding 'moon' header to column X (col 24) ...")
    ws.update(range_name="X1", values=[["moon"]], value_input_option="USER_ENTERED")
    time.sleep(0.5)

    # Update moon data in batches
    print(f"Adding moon values to rows 2-{len(df)+1} ...")
    batch_size = 500

    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:min(i+batch_size, len(df))]["moon"].values
        batch_data = [[val] for val in batch]

        start_row = 2 + i
        end_row = start_row + len(batch) - 1

        range_str = f"X{start_row}:X{end_row}"
        ws.update(range_name=range_str, values=batch_data, value_input_option="USER_ENTERED")

        print(f"  Rows {start_row}--{end_row} [OK]")

        if i + batch_size < len(df):
            time.sleep(1.0)

    print(f"\nDone! Added 'moon' column to {ANALYSIS_SHEET}")
    print(f"Total rows with moon data: {matched}")
    print(f"\nColumn X now contains round-specific moon phases:")
    print(f"  Round 1 -> Moon R1")
    print(f"  Round 2 -> Moon R2")
    print(f"  Round 3 -> Moon R3")
    print(f"  Round 4 -> Moon R4")


if __name__ == "__main__":
    main()
