import csv

matchup_file = "Golf Historics v3 - 2BMatchup (5).csv"

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    print(f"Header row length: {len(header)}")
    print(f"\nSearching for column BB...")

    # Find BB column
    bb_idx = None
    for i, col_name in enumerate(header):
        if i == 53:  # BB is the 54th column (0-indexed = 53)
            print(f"Column {i} (BB): '{col_name}'")
            bb_idx = i
            break

    if bb_idx is None:
        # Try to find by name
        for i, col_name in enumerate(header):
            print(f"Column {i}: '{col_name}'")
            if 'pick' in col_name.lower() and 'filter' in col_name.lower():
                bb_idx = i
                print(f"  ^ Found match at index {i}")

    print(f"\nBB Index: {bb_idx}")

    # Count picks in BB
    bb_count = 0
    bb_empty = 0
    total_rows = 0

    for row_num, row in enumerate(reader, start=2):
        total_rows += 1

        if bb_idx < len(row):
            bb_value = row[bb_idx].strip()
            if bb_value and bb_value != '':
                bb_count += 1
            else:
                bb_empty += 1

    print(f"\nResults for Column BB:")
    print(f"  Total data rows: {total_rows}")
    print(f"  Non-empty picks in BB: {bb_count}")
    print(f"  Empty/blank in BB: {bb_empty}")
    print(f"  Percentage with picks: {bb_count/total_rows*100:.1f}%")
