#!/usr/bin/env python3
"""
Add gap column to ANALYSIS_v2.

Gap = exec_bucket - upside_bucket
Positive gap: player executing above upside potential
Negative gap: player has untapped upside
"""

import os
import sys
import time
import gspread
from google.oauth2.service_account import Credentials

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE     = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID       = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES         = ["https://www.googleapis.com/auth/spreadsheets"]
ANALYSIS_SHEET = "ANALYSIS_v2"


def main():
    print("Authenticating …")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    print(f"Opening {ANALYSIS_SHEET} …")
    ws = ss.worksheet(ANALYSIS_SHEET)

    # Get sheet dimensions
    print("Reading sheet dimensions …")
    all_values = ws.get_all_values()
    total_rows = len(all_values)
    print(f"  Total rows (including header): {total_rows}")

    if total_rows < 2:
        print("ERROR: Sheet has no data rows")
        sys.exit(1)

    # Expand sheet to have enough columns (need column V for gap, which is col 21)
    print("Expanding sheet columns …")
    current_cols = ws.col_count
    if current_cols < 22:
        ws.add_cols(22 - current_cols)
        print(f"  Added columns (now {current_cols + (22 - current_cols)} total)")
        time.sleep(0.5)

    # Update header (row 1)
    print("Updating header row …")
    ws.update(range_name="V1", values=[["gap"]], value_input_option="USER_ENTERED")
    time.sleep(0.5)

    # Add formulas for all data rows
    print(f"Adding gap formulas to rows 2–{total_rows} …")

    formulas = []
    for row_num in range(2, total_rows + 1):
        # gap = exec_bucket - upside_bucket = M - N
        gap_formula = f"=M{row_num}-N{row_num}"
        formulas.append([gap_formula])

    # Write in batches
    batch_size = 500
    for i in range(0, len(formulas), batch_size):
        batch = formulas[i : i + batch_size]
        start_row = 2 + i
        end_row = start_row + len(batch) - 1
        range_str = f"V{start_row}:V{end_row}"

        ws.update(range_name=range_str, values=batch, value_input_option="USER_ENTERED")
        print(f"  Rows {start_row}–{end_row} ✓")

        if i + batch_size < len(formulas):
            time.sleep(1.0)

    print(f"\nDone! Added gap column to {total_rows - 1} data rows.")
    print("Gap = exec_bucket - upside_bucket")
    print("  Positive: executing above upside potential")
    print("  Negative: has untapped upside")


if __name__ == "__main__":
    main()
