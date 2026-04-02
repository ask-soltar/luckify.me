#!/usr/bin/env python3
"""
Add moon columns to ANALYSIS_v2 by matching:
- player_id (col A)
- event_id (col C)
- round_num (col F)

Uses round_num to select Moon R1-R4 from Golf_Analytics.
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
GOLF_SHEET     = "Golf_Analytics"

MOON_COLUMNS = ["Moon R1", "Moon R2", "Moon R3", "Moon R4"]


def main():
    print("Authenticating ...")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    # Load both sheets
    print(f"Loading {ANALYSIS_SHEET} ...")
    analysis_raw = ss.worksheet(ANALYSIS_SHEET).get_all_values()
    analysis_df = pd.DataFrame(analysis_raw[1:], columns=analysis_raw[0])
    print(f"  {len(analysis_df)} rows")

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

    # Extract moon columns from Golf_Analytics
    if "Moon R1" in golf_df.columns:
        moon_data = golf_df[["Player", "Venue", "Year"] + MOON_COLUMNS].copy()
        moon_data.columns = ["player_name", "event_name", "year"] + MOON_COLUMNS
        print(f"\nMerging moon data by player_name + event_name + year ...")

        # Merge
        analysis_merged = analysis_df.merge(
            moon_data,
            on=["player_name", "event_name", "year"],
            how="left"
        )

        matched = analysis_merged["Moon R1"].notna().sum()
        print(f"  Matched {matched} / {len(analysis_merged)} rows")

        # Create single "moon" column by round_num
        def get_moon(row):
            round_num = row["round_num"]
            if pd.isna(round_num):
                return ""
            round_num = int(round_num)
            if round_num == 1:
                return row.get("Moon R1", "")
            elif round_num == 2:
                return row.get("Moon R2", "")
            elif round_num == 3:
                return row.get("Moon R3", "")
            elif round_num == 4:
                return row.get("Moon R4", "")
            return ""

        analysis_merged["moon"] = analysis_merged.apply(get_moon, axis=1)

        # Save as CSV for review
        csv_path = os.path.join(BASE_DIR, "analysis_v2_with_moon.csv")
        analysis_merged.to_csv(csv_path, index=False)
        print(f"\nSaved merged data to {csv_path}")
        print(f"Total rows with moon data: {analysis_merged['moon'].notna().sum()}")

        print(f"\n*** NEXT STEP ***")
        print(f"1. Review the CSV: {csv_path}")
        print(f"2. To add 'moon' column to sheet, copy it from the CSV")
        print(f"3. Or run: combo_analysis_4d_moon.py with the CSV as input")

    else:
        print("\nMoon columns not found in Golf_Analytics")
        print("Available columns:", list(golf_df.columns[:30]))


if __name__ == "__main__":
    main()
