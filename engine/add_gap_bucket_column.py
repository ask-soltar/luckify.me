#!/usr/bin/env python3
"""
Add gap_bucket column to ANALYSIS_v2.

Gap_bucket = signed gap bucketed by size 10 (optimal from analysis).
Handles negative and positive gaps with direction preserved.

Bucket size 10: -50, -40, -30, -20, -10, 0, 10, 20, 30, etc.
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
BUCKET_SIZE    = 10


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

    # Expand sheet to have enough columns (need column W for gap_bucket, which is col 23)
    print("Expanding sheet columns …")
    current_cols = ws.col_count
    if current_cols < 23:
        ws.add_cols(23 - current_cols)
        print(f"  Added columns (now {current_cols + (23 - current_cols)} total)")
        time.sleep(0.5)

    # Update header (row 1)
    print("Updating header row …")
    ws.update(range_name="W1", values=[["gap_bucket"]], value_input_option="USER_ENTERED")
    time.sleep(0.5)

    # Add formulas for all data rows
    print(f"Adding gap_bucket formulas to rows 2–{total_rows} …")
    print(f"  Bucket size: {BUCKET_SIZE} (signed, direction preserved)")

    formulas = []
    for row_num in range(2, total_rows + 1):
        # gap_bucket = signed gap bucketed by 10
        # IF gap >= 0: (INT(gap/10))*10
        # IF gap < 0: -((INT(ABS(gap)/10))*10)
        gap_bucket_formula = f'=IF(V{row_num}>=0,INT(V{row_num}/{BUCKET_SIZE})*{BUCKET_SIZE},-INT(ABS(V{row_num})/{BUCKET_SIZE})*{BUCKET_SIZE})'
        formulas.append([gap_bucket_formula])

    # Write in batches
    batch_size = 500
    for i in range(0, len(formulas), batch_size):
        batch = formulas[i : i + batch_size]
        start_row = 2 + i
        end_row = start_row + len(batch) - 1
        range_str = f"W{start_row}:W{end_row}"

        ws.update(range_name=range_str, values=batch, value_input_option="USER_ENTERED")
        print(f"  Rows {start_row}--{end_row} [OK]")

        if i + batch_size < len(formulas):
            time.sleep(1.0)

    print(f"\nDone! Added gap_bucket column to {total_rows - 1} data rows.")
    print(f"Gap_bucket = signed gap with bucket size {BUCKET_SIZE}")
    print("  Positive buckets: 0, 10, 20, 30, ... (high exec relative to upside)")
    print("  Negative buckets: 0, -10, -20, -30, ... (high upside relative to exec)")


if __name__ == "__main__":
    main()
