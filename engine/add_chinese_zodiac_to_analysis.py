#!/usr/bin/env python3
"""
Add Chinese Zodiac column to ANALYSIS_v2.

Sources Chinese Zodiac from Golf_Analytics column 56.
Matches by player_name + event_name + year.
"""

import os
import sys
import time
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
ANALYSIS_SHEET = "ANALYSIS_v2"
GOLF_SHEET = "Golf_Analytics"


def main():
    print("Authenticating ...")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    # Load ANALYSIS_v2
    print(f"Loading {ANALYSIS_SHEET} ...")
    analysis_raw = ss.worksheet(ANALYSIS_SHEET).get_all_values()
    analysis_df = pd.DataFrame(analysis_raw[1:], columns=analysis_raw[0])
    print(f"  {len(analysis_df)} rows")

    # Load Golf_Analytics
    print(f"Loading {GOLF_SHEET} ...")
    golf_raw = ss.worksheet(GOLF_SHEET).get_all_values()
    golf_df = pd.DataFrame(golf_raw[1:], columns=golf_raw[0])
    print(f"  {len(golf_df)} rows")

    # Clean keys
    analysis_df["player_name"] = analysis_df["player_name"].astype(str).str.strip()
    analysis_df["event_name"] = analysis_df["event_name"].astype(str).str.strip()
    analysis_df["year"] = pd.to_numeric(analysis_df["year"], errors="coerce")

    golf_df["Player"] = golf_df["Player"].astype(str).str.strip()
    golf_df["Venue"] = golf_df["Venue"].astype(str).str.strip()
    golf_df["Year"] = pd.to_numeric(golf_df["Year"], errors="coerce")

    # Extract Chinese Zodiac
    zodiac_data = golf_df[["Player", "Venue", "Year", "Chinese Zodiac"]].copy()
    zodiac_data.columns = ["player_name", "event_name", "year", "chinese_zodiac"]

    print(f"\nMerging Chinese Zodiac by player + event + year ...")

    # Merge
    analysis_merged = analysis_df.merge(
        zodiac_data,
        on=["player_name", "event_name", "year"],
        how="left"
    )

    matched = analysis_merged["chinese_zodiac"].notna().sum()
    print(f"  Matched {matched} / {len(analysis_merged)} rows")

    # Save to CSV for inspection
    csv_path = os.path.join(BASE_DIR, "analysis_v2_with_chinese_zodiac.csv")
    analysis_merged.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")

    # Push to sheet
    print(f"\nAdding 'chinese_zodiac' column to {ANALYSIS_SHEET} ...")
    ws = ss.worksheet(ANALYSIS_SHEET)

    current_cols = ws.col_count
    if current_cols < 29:
        ws.add_cols(29 - current_cols)
        print(f"  Expanded to 29 columns")
        time.sleep(0.5)

    # Update header (Column AC = column 29)
    ws.update(range_name="AC1", values=[["chinese_zodiac"]], value_input_option="USER_ENTERED")
    time.sleep(0.5)

    # Update data in batches
    batch_size = 500
    for i in range(0, len(analysis_merged), batch_size):
        batch = analysis_merged.iloc[i:min(i+batch_size, len(analysis_merged))]["chinese_zodiac"].values
        batch_data = [[val if pd.notna(val) else ""] for val in batch]

        start_row = 2 + i
        end_row = start_row + len(batch) - 1

        range_str = f"AC{start_row}:AC{end_row}"
        ws.update(range_name=range_str, values=batch_data, value_input_option="USER_ENTERED")

        print(f"  Rows {start_row}--{end_row} [OK]")

        if i + batch_size < len(analysis_merged):
            time.sleep(1.0)

    print(f"\nDone! Added 'chinese_zodiac' column to {ANALYSIS_SHEET}")
    print(f"Total rows with chinese_zodiac data: {matched}")


if __name__ == "__main__":
    main()
