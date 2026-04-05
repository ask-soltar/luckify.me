import csv

matchup_file = "Golf Historics v3 - 2BMatchup (7).csv"

lp_score_idx = 52
lp_pick_idx = 53
wl_lp_idx = 54
same_lp_idx = 39

lp_data = []
rows_checked = 0
rows_with_lp_score = 0
rows_with_lp_pick = 0
rows_with_wl = 0
rows_with_same_lp_true = 0
rows_with_all = 0

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row_num, row in enumerate(reader, 1):
        if not row or len(row) < max(wl_lp_idx + 1, same_lp_idx + 1):
            continue

        rows_checked += 1

        # Check LP Score
        lp_score_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
        if lp_score_str and lp_score_str not in ['', '#REF!']:
            rows_with_lp_score += 1
            try:
                lp_score = float(lp_score_str)
            except:
                continue
        else:
            continue

        # Check LP Pick
        lp_pick = row[lp_pick_idx].strip() if lp_pick_idx < len(row) else ''
        if lp_pick:
            rows_with_lp_pick += 1
        else:
            continue

        # Check W/L
        wl = row[wl_lp_idx].strip() if wl_lp_idx < len(row) else ''
        is_win = None
        if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
            is_win = True
        elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
            is_win = False

        if is_win is not None:
            rows_with_wl += 1
        else:
            continue

        rows_with_all += 1

        # Check Same LP
        same_lp = row[same_lp_idx].strip() if same_lp_idx < len(row) else ''
        if same_lp.upper() == 'TRUE':
            rows_with_same_lp_true += 1
            lp_data.append({
                'lp_score': lp_score,
                'result': is_win
            })

print(f"Data flow audit:")
print(f"  Total rows with data: {rows_checked}")
print(f"  With LP Score: {rows_with_lp_score}")
print(f"  With LP Pick: {rows_with_lp_pick}")
print(f"  With W/L result: {rows_with_wl}")
print(f"  With all 3: {rows_with_all}")
print(f"  With Same LP = TRUE: {rows_with_same_lp_true}")
print(f"\nSame LP filtered picks: {len(lp_data)}")

if lp_data:
    wins = sum(1 for d in lp_data if d['result'])
    wr = (wins / len(lp_data) * 100)
    print(f"Baseline WR: {wr:.1f}% ({wins}W-{len(lp_data)-wins}L)")
