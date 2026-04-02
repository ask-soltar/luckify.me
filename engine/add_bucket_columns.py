#!/usr/bin/env python3
"""
Add exec_bucket and upside_bucket helper columns to ANALYSIS_v2.

Columns T (exec_bucket) and U (upside_bucket) with formulas:
  exec_bucket   = INT(M / 25) * 25
  upside_bucket = INT(N / 25) * 25

Adds headers and populates formulas for all data rows.
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

BUCKET_SIZE = 25


def main():
    print("Authenticating …")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    print(f"Opening {ANALYSIS_SHEET} …")
    ws = ss.worksheet(ANALYSIS_SHEET)

    # Get all values to find row count
    print("Reading sheet dimensions …")
    all_values = ws.get_all_values()
    total_rows = len(all_values)
    print(f"  Total rows (including header): {total_rows}")

    if total_rows < 2:
        print("ERROR: Sheet has no data rows")
        sys.exit(1)

    # Expand sheet to have enough columns (need at least 21 for T, U)
    print("Expanding sheet columns …")
    current_cols = ws.col_count
    if current_cols < 21:
        ws.add_cols(21 - current_cols)
        print(f"  Added columns (now {current_cols + (21 - current_cols)} total)")
        time.sleep(0.5)

    # Update header (row 1)
    print("Updating header row …")
    ws.update(range_name="T1:U1", values=[["exec_bucket", "upside_bucket"]], value_input_option="USER_ENTERED")
    time.sleep(0.5)

    # Add formulas for all data rows
    print(f"Adding bucket formulas to rows 2–{total_rows} …")

    # Build formula list
    formulas = []
    for row_num in range(2, total_rows + 1):
        exec_formula = f"=INT(M{row_num}/25)*25"
        upside_formula = f"=INT(N{row_num}/25)*25"
        formulas.append([exec_formula, upside_formula])

    # Write in batches
    batch_size = 500
    for i in range(0, len(formulas), batch_size):
        batch = formulas[i : i + batch_size]
        start_row = 2 + i
        end_row = start_row + len(batch) - 1
        range_str = f"T{start_row}:U{end_row}"

        ws.update(range_name=range_str, values=batch, value_input_option="USER_ENTERED")
        print(f"  Rows {start_row}–{end_row} ✓")

        if i + batch_size < len(formulas):
            time.sleep(1.0)

    print(f"\nDone! Added exec_bucket and upside_bucket to {total_rows - 1} data rows.")
    print(f"Bucket size: {BUCKET_SIZE}")


if __name__ == "__main__":
    main()
