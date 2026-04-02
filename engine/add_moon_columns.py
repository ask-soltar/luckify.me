#!/usr/bin/env python3
"""
Add moon columns from Golf_Analytics to ANALYSIS_v2.

Joins moon data by player_id + event_id + round_num.
Saves merged data locally as CSV for manual inspection, then updates sheet.
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

MOON_COLUMNS = [
    "Moon R1", "Moon R2", "Moon R3", "Moon R4",
    "Wu Xing Element", "Chinese Zodiac", "Destiny Card", "Horoscope",
    "MoonWest R1 (8C)", "MoonWest R2 (8C)", "MoonWest R3 (8C)", "MoonWest R4 (8C)",
    "Life Path", "Tithi"
]


def main():
    print("Authenticating ...")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    # Load Golf_Analytics with moon data
    print(f"Loading {GOLF_SHEET} ...")
    golf_raw = ss.worksheet(GOLF_SHEET).get_all_values()
    golf_df = pd.DataFrame(golf_raw[1:], columns=golf_raw[0])
    print(f"  {len(golf_df)} rows loaded")

    # Load ANALYSIS_v2
    print(f"Loading {ANALYSIS_SHEET} ...")
    analysis_raw = ss.worksheet(ANALYSIS_SHEET).get_all_values()
    analysis_df = pd.DataFrame(analysis_raw[1:], columns=analysis_raw[0])
    print(f"  {len(analysis_df)} rows loaded")

    # Clean key columns for merging
    golf_df["player_id"] = golf_df["player_id"].astype(str).str.strip()
    golf_df["event_id"] = golf_df["event_id"].astype(str).str.strip()
    golf_df["round_num"] = pd.to_numeric(golf_df["round_num"], errors="coerce")

    analysis_df["player_id"] = analysis_df["player_id"].astype(str).str.strip()
    analysis_df["event_id"] = analysis_df["event_id"].astype(str).str.strip()
    analysis_df["round_num"] = pd.to_numeric(analysis_df["round_num"], errors="coerce")

    # Extract only moon columns from Golf_Analytics
    moon_data = golf_df[["player_id", "event_id", "round_num"] + MOON_COLUMNS].copy()

    print(f"\nMerging moon columns ...")

    # Merge on player_id, event_id, round_num
    analysis_merged = analysis_df.merge(
        moon_data,
        on=["player_id", "event_id", "round_num"],
        how="left"
    )

    matched = analysis_merged[MOON_COLUMNS[0]].notna().sum()
    print(f"  Matched {matched} / {len(analysis_merged)} rows with moon data")

    # Save merged data locally
    output_file = os.path.join(BASE_DIR, "analysis_v2_with_moons.csv")
    analysis_merged.to_csv(output_file, index=False)
    print(f"  Saved merged data to {output_file}")

    print(f"\n*** MANUAL STEP REQUIRED ***")
    print(f"The merged data has been saved to CSV.")
    print(f"To add to sheet, copy columns X onwards (moon columns) from CSV")
    print(f"And paste into ANALYSIS_v2 starting at column X row 2.")
    print(f"\nAlternatively, rebuild ANALYSIS_v2 from scratch using build_analysis_v2.py")
    print(f"with moon columns added to the build process.")


if __name__ == "__main__":
    main()
