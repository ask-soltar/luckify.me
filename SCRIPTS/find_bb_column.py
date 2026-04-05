import csv

matchup_file = "Golf Historics v3 - 2BMatchup (6).csv"

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    print(f"Total columns: {len(header)}\n")
    print("Looking for BB-related columns:\n")

    for i, col_name in enumerate(header):
        if 'pick' in col_name.lower() or 'bb' in col_name.lower() or i == 48 or i == 53:
            print(f"  Col {i} ({chr(65 + (i % 26)) if i < 26 else chr(65 + (i // 26) - 1) + chr(65 + (i % 26))}): '{col_name}'")

    print("\nFirst 5 data rows, relevant columns:")
    reader = csv.reader(open(matchup_file, 'r', encoding='utf-8'))
    header = next(reader)

    for row_num, row in enumerate(reader, 1):
        if row_num > 5:
            break
        print(f"\nRow {row_num}:")
        print(f"  Col 48 (BB expected): '{row[48] if 48 < len(row) else 'N/A'}'")
        print(f"  Col 53 (alternative): '{row[53] if 53 < len(row) else 'N/A'}'")
        print(f"  Col 52 (LP Score): '{row[52] if 52 < len(row) else 'N/A'}'")
        print(f"  Col 49 (W/L): '{row[49] if 49 < len(row) else 'N/A'}'")
