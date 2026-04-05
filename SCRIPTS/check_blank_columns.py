import csv

matchup_file = 'Golf Historics v3 - 2BMatchup (6).csv'

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    print('Checking blank header columns (53-59) for pick data:\n')

    for col_idx in range(53, 60):
        non_empty = 0
        non_zero = 0
        sample_vals = []

        # Count values in this column
        for row in reader:
            if col_idx < len(row):
                val = row[col_idx].strip()
                if val:
                    non_empty += 1
                    if val != '0':
                        non_zero += 1
                        if len(sample_vals) < 3:
                            sample_vals.append(val)

        print(f'Col {col_idx}: {non_empty} non-empty, {non_zero} non-zero')
        if sample_vals:
            print(f'         Sample: {sample_vals}\n')
        else:
            print()

print("\nW/L columns (47, 49):")
with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for col_idx in [47, 49]:
        non_empty = 0
        sample_vals = []

        for row in reader:
            if col_idx < len(row):
                val = row[col_idx].strip()
                if val:
                    non_empty += 1
                    if len(sample_vals) < 3:
                        sample_vals.append(val)

        print(f'Col {col_idx} (W/L): {non_empty} non-empty')
        if sample_vals:
            print(f'       Sample: {sample_vals}\n')
