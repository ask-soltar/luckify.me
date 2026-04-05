import csv

matchup_file = "Golf Historics v3 - 2BMatchup (6).csv"

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    ba_idx = None  # LP Score
    bb_idx = None  # Picks
    bc_idx = None  # W/L

    for i, col_name in enumerate(header):
        if 'LP S' in col_name or 'LP Score' in col_name:
            ba_idx = i
        elif col_name.strip() == 'BB' or 'pick' in col_name.lower():
            bb_idx = i
        elif col_name.strip() == 'W/L':
            bc_idx = i

    print(f"Column indices:")
    print(f"  BA (LP Score): {ba_idx}")
    print(f"  BB (Picks): {bb_idx}")
    print(f"  BC (W/L): {bc_idx}\n")

    # Count data completeness patterns
    bb_only = 0
    ba_bb_only = 0
    ba_bc_only = 0
    all_three = 0
    none = 0

    for row in reader:
        has_ba = ba_idx < len(row) and row[ba_idx].strip() and row[ba_idx].strip() not in ['', '0', '#REF!']
        has_bb = bb_idx < len(row) and row[bb_idx].strip() and row[bb_idx].strip() not in ['', '0']
        has_bc = bc_idx < len(row) and row[bc_idx].strip() and row[bc_idx].strip() not in ['', '0']

        if has_bb and not has_ba and not has_bc:
            bb_only += 1
        elif has_ba and has_bb and not has_bc:
            ba_bb_only += 1
        elif has_ba and has_bc and not has_bb:
            ba_bc_only += 1
        elif has_ba and has_bb and has_bc:
            all_three += 1
        elif not has_ba and not has_bb and not has_bc:
            none += 1

    total = bb_only + ba_bb_only + ba_bc_only + all_three + none

    print(f"Data Completeness Breakdown:")
    print(f"  All 3 (BA + BB + BC): {all_three} rows ({all_three/total*100:.1f}%)")
    print(f"  BA + BB only (no W/L): {ba_bb_only} rows ({ba_bb_only/total*100:.1f}%)")
    print(f"  BB only (no score/result): {bb_only} rows ({bb_only/total*100:.1f}%)")
    print(f"  BA + BC only (no picks): {ba_bc_only} rows ({ba_bc_only/total*100:.1f}%)")
    print(f"  None: {none} rows ({none/total*100:.1f}%)")
    print(f"  Total rows: {total}")

    print(f"\nSummary:")
    print(f"  Picks with W/L results (for analysis): {all_three}")
    print(f"  Picks scored but waiting for W/L: {ba_bb_only}")
    print(f"  Need to analyze: {all_three} rows (remaining {ba_bb_only} picks awaiting results)")
