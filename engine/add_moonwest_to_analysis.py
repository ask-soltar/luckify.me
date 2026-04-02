#!/usr/bin/env python3
"""
Add Western Moon (8 phases) column to ANALYSIS_v2.

Sources MoonWest R1-R4 from Golf_Analytics (columns 58-61).
Matches by player_name + event_name + year, then selects correct round phase.
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
    analysis_df["round_num"] = pd.to_numeric(analysis_df["round_num"], errors="coerce")

    golf_df["Player"] = golf_df["Player"].astype(str).str.strip()
    golf_df["Venue"] = golf_df["Venue"].astype(str).str.strip()
    golf_df["Year"] = pd.to_numeric(golf_df["Year"], errors="coerce")

    # Extract MoonWest columns (R1-R4)
    moonwest_data = golf_df[["Player", "Venue", "Year", "MoonWest R1 (8C)", "MoonWest R2 (8C)", "MoonWest R3 (8C)", "MoonWest R4 (8C)"]].copy()
    moonwest_data.columns = ["player_name", "event_name", "year", "moonwest_r1", "moonwest_r2", "moonwest_r3", "moonwest_r4"]

    print(f"\nMerging Western Moon by player + event + year ...")

    # Merge
    analysis_merged = analysis_df.merge(
        moonwest_data,
        on=["player_name", "event_name", "year"],
        how="left"
    )

    # For each row, select correct MoonWest based on round_num
    def get_moonwest(row):
        if pd.isna(row['round_num']):
            return None
        round_num = int(row['round_num'])
        if round_num == 1:
            return row['moonwest_r1']
        elif round_num == 2:
            return row['moonwest_r2']
        elif round_num == 3:
            return row['moonwest_r3']
        elif round_num == 4:
            return row['moonwest_r4']
        return None

    analysis_merged['moonwest'] = analysis_merged.apply(get_moonwest, axis=1)

    matched = analysis_merged["moonwest"].notna().sum()
    print(f"  Matched {matched} / {len(analysis_merged)} rows")

    # Save to CSV for inspection
    csv_path = os.path.join(BASE_DIR, "analysis_v2_with_moonwest.csv")
    analysis_merged.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")

    # Push to sheet
    print(f"\nAdding 'moonwest' column to {ANALYSIS_SHEET} ...")
    ws = ss.worksheet(ANALYSIS_SHEET)

    current_cols = ws.col_count
    if current_cols < 28:
        ws.add_cols(28 - current_cols)
        print(f"  Expanded to 28 columns")
        time.sleep(0.5)

    # Update header (Column AB = column 28)
    ws.update(range_name="AB1", values=[["moonwest"]], value_input_option="USER_ENTERED")
    time.sleep(0.5)

    # Update data in batches
    batch_size = 500
    for i in range(0, len(analysis_merged), batch_size):
        batch = analysis_merged.iloc[i:min(i+batch_size, len(analysis_merged))]["moonwest"].values
        batch_data = [[val if pd.notna(val) else ""] for val in batch]

        start_row = 2 + i
        end_row = start_row + len(batch) - 1

        range_str = f"AB{start_row}:AB{end_row}"
        ws.update(range_name=range_str, values=batch_data, value_input_option="USER_ENTERED")

        print(f"  Rows {start_row}--{end_row} [OK]")

        if i + batch_size < len(analysis_merged):
            time.sleep(1.0)

    print(f"\nDone! Added 'moonwest' column to {ANALYSIS_SHEET}")
    print(f"Total rows with moonwest data: {matched}")
    print(f"\nColumn AB now contains Western Moon phases (8 phases)")


if __name__ == "__main__":
    main()
