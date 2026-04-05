import csv
import statistics

matchup_file = "Golf Historics v3 - 2BMatchup (7).csv"

matchup_data = []

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    lp_score_idx = 52      # LP SCore
    lp_pick_idx = 53       # LP Pick
    wl_lp_idx = 54         # W/L [LP]
    element_a_idx = 9      # Element [A]
    element_b_idx = 10     # Element [B]

    print(f"Columns:")
    print(f"  {lp_score_idx}: {header[lp_score_idx]}")
    print(f"  {lp_pick_idx}: {header[lp_pick_idx]}")
    print(f"  {wl_lp_idx}: {header[wl_lp_idx]}")
    print(f"  {element_a_idx}: {header[element_a_idx]}")
    print(f"  {element_b_idx}: {header[element_b_idx]}\n")

    for row in reader:
        if not row or len(row) < max(wl_lp_idx + 1, element_b_idx + 1):
            continue

        try:
            # Check elements match
            elem_a = row[element_a_idx].strip() if element_a_idx < len(row) else ''
            elem_b = row[element_b_idx].strip() if element_b_idx < len(row) else ''

            if not elem_a or not elem_b or elem_a != elem_b:
                continue

            # Get LP Score
            lp_score_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
            if not lp_score_str or lp_score_str in ['', '#REF!']:
                continue

            lp_score = float(lp_score_str)

            # Get LP Pick
            lp_pick = row[lp_pick_idx].strip() if lp_pick_idx < len(row) else ''
            if not lp_pick:
                continue

            # Get W/L result
            wl = row[wl_lp_idx].strip() if wl_lp_idx < len(row) else ''

            # Determine if win or loss
            is_win = None
            if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                is_win = True
            elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                is_win = False

            if is_win is None:
                continue

            matchup_data.append({
                'lp_score': lp_score,
                'element': elem_a,
                'pick': lp_pick,
                'result': is_win
            })

        except (ValueError, IndexError):
            continue

print(f"Total same-element picks: {len(matchup_data)}\n")

if not matchup_data:
    print("ERROR: No same-element data found!")
    exit(1)

# ============================================================
# ANALYSIS 1: Distribution
# ============================================================
print("=" * 100)
print("LP SCORE THRESHOLD ANALYSIS - SAME ELEMENT MATCHUPS ONLY")
print("=" * 100)

lp_scores = [d['lp_score'] for d in matchup_data]
wins = [d for d in matchup_data if d['result']]
losses = [d for d in matchup_data if not d['result']]

print(f"\nOverall Stats:")
print(f"  Total picks: {len(matchup_data)}")
print(f"  Wins: {len(wins)} ({len(wins)/len(matchup_data)*100:.1f}%)")
print(f"  Losses: {len(losses)} ({len(losses)/len(matchup_data)*100:.1f}%)")
print(f"  Overall win rate: {len(wins)/len(matchup_data)*100:.1f}%")

print(f"\nLP Score Statistics:")
print(f"  Min: {min(lp_scores):.2f}")
print(f"  Max: {max(lp_scores):.2f}")
print(f"  Mean: {statistics.mean(lp_scores):.2f}")
print(f"  Median: {statistics.median(lp_scores):.2f}")
print(f"  Stdev: {statistics.stdev(lp_scores):.2f}")

# ============================================================
# ANALYSIS 2: By Element
# ============================================================
print("\n" + "=" * 100)
print("PERFORMANCE BY ELEMENT")
print("=" * 100)

by_element = {}
for data in matchup_data:
    elem = data['element']
    if elem not in by_element:
        by_element[elem] = {'total': 0, 'wins': 0}
    by_element[elem]['total'] += 1
    if data['result']:
        by_element[elem]['wins'] += 1

print(f"\n{'Element':<15} {'Picks':<10} {'Wins':<10} {'Win Rate':<12}")
print("-" * 50)

for elem in sorted(by_element.keys()):
    total = by_element[elem]['total']
    wins = by_element[elem]['wins']
    wr = (wins / total * 100) if total > 0 else 0
    print(f"{elem:<15} {total:<10} {wins:<10} {wr:<11.1f}%")

# ============================================================
# ANALYSIS 3: Threshold Analysis
# ============================================================
print("\n" + "=" * 100)
print("THRESHOLD FILTERING")
print("=" * 100)

thresholds = list(range(-10, 12))
threshold_results = []

for threshold in sorted(thresholds):
    filtered = [d for d in matchup_data if d['lp_score'] > threshold]

    if not filtered:
        continue

    wins_above = sum(1 for d in filtered if d['result'])
    losses_above = sum(1 for d in filtered if not d['result'])
    win_rate = (wins_above / len(filtered) * 100) if filtered else 0

    threshold_results.append({
        'threshold': threshold,
        'picks': len(filtered),
        'wins': wins_above,
        'losses': losses_above,
        'win_rate': win_rate
    })

print(f"\n{'Threshold':<12} {'Picks':<10} {'Wins':<10} {'Losses':<10} {'Win Rate':<12}")
print("-" * 65)

for result in sorted(threshold_results, key=lambda x: x['threshold']):
    print(f"{result['threshold']:>10.0f} {result['picks']:<10} {result['wins']:<10} {result['losses']:<10} {result['win_rate']:<11.1f}%")

# Find best thresholds
by_winrate = sorted(threshold_results, key=lambda x: x['win_rate'], reverse=True)

print(f"\nTOP 10 THRESHOLDS BY WIN RATE:")
for i, result in enumerate(by_winrate[:10], 1):
    print(f"  {i:2d}. Threshold {result['threshold']:>3.0f}: {result['win_rate']:>5.1f}% WR ({result['picks']:3d} picks, {result['wins']:2d}W-{result['losses']:2d}L)")

# ============================================================
# ANALYSIS 4: Comparison to All Matchups
# ============================================================
print("\n" + "=" * 100)
print("COMPARISON: Same Element vs All Matchups")
print("=" * 100)

same_element_wins = sum(1 for d in matchup_data if d['result'])
same_element_total = len(matchup_data)
all_same_wr = (same_element_wins / same_element_total * 100) if same_element_total else 0
print(f"\nSame Element WR: {all_same_wr:.1f}% ({same_element_wins}W-{same_element_total - same_element_wins}L, {same_element_total} picks)")
print(f"All Matchups WR: 49.5% (422W-431L, 853 picks)")
print(f"Difference: {all_same_wr - 49.5:.1f} pp")

if all_same_wr > 49.5:
    print(f"\nFINDING: Same-element matchups OUTPERFORM by {all_same_wr - 49.5:.1f} pp")
else:
    print(f"\nFINDING: Same-element matchups UNDERPERFORM by {49.5 - all_same_wr:.1f} pp")
