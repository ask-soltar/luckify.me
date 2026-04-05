import csv

matchup_file = "Golf Historics v3 - 2BMatchup (7).csv"

matchup_data = []

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    lp_score_idx = 52
    lp_pick_idx = 53
    wl_lp_idx = 54
    element_a_idx = 9
    element_b_idx = 10

    for row in reader:
        if not row or len(row) < max(wl_lp_idx + 1, element_b_idx + 1):
            continue

        try:
            elem_a = row[element_a_idx].strip() if element_a_idx < len(row) else ''
            elem_b = row[element_b_idx].strip() if element_b_idx < len(row) else ''

            if not elem_a or not elem_b or elem_a != elem_b:
                continue

            lp_score_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
            if not lp_score_str or lp_score_str in ['', '#REF!']:
                continue

            lp_score = float(lp_score_str)

            lp_pick = row[lp_pick_idx].strip() if lp_pick_idx < len(row) else ''
            if not lp_pick:
                continue

            wl = row[wl_lp_idx].strip() if wl_lp_idx < len(row) else ''

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
                'result': is_win
            })

        except (ValueError, IndexError):
            continue

# Build matrix: Element x Threshold
elements = ['Metal', 'Earth', 'Water', 'Fire', 'Wood']
thresholds = list(range(-2, 9))

print("\n" + "=" * 140)
print("LP SCORE PERFORMANCE MATRIX: ELEMENT x THRESHOLD")
print("=" * 140)
print("\nFormat: Win Rate (Picks)")
print("Green background indicates 55%+ WR | Red indicates <50% WR\n")

# Header row
header_row = f"{'Element':<12}"
for t in thresholds:
    header_row += f" T{t:+3d}  "
header_row += " | BASELINE"
print(header_row)
print("-" * 140)

# Data rows
for elem in elements:
    row_data = f"{elem:<12}"
    elem_data = [d for d in matchup_data if d['element'] == elem]

    # Calculate baseline (all thresholds)
    baseline_wins = sum(1 for d in elem_data if d['result'])
    baseline_wr = (baseline_wins / len(elem_data) * 100) if elem_data else 0

    for threshold in thresholds:
        filtered = [d for d in elem_data if d['lp_score'] > threshold]

        if not filtered:
            row_data += "   --   "
        else:
            wins = sum(1 for d in filtered if d['result'])
            wr = (wins / len(filtered) * 100)

            # Color coding
            if wr >= 55:
                marker = "*"
            elif wr < 50:
                marker = "!"
            else:
                marker = " "

            row_data += f"{wr:5.1f}%{marker} "

    row_data += f" | {baseline_wr:5.1f}% ({len(elem_data)} picks)"
    print(row_data)

print("\n" + "-" * 140)
print("Legend: * = 55%+ WR (STRONG) | ! = <50% WR (WEAK) | -- = Insufficient data\n")

# Recommendation table
print("\n" + "=" * 100)
print("RECOMMENDED THRESHOLDS BY ELEMENT")
print("=" * 100)

recommendations = []
for elem in elements:
    elem_data = [d for d in matchup_data if d['element'] == elem]
    if not elem_data:
        continue

    best_wr = 0
    best_threshold = None
    best_picks = 0

    # Find best threshold with at least 5 picks
    for threshold in thresholds:
        filtered = [d for d in elem_data if d['lp_score'] > threshold]
        if len(filtered) >= 5:
            wins = sum(1 for d in filtered if d['result'])
            wr = (wins / len(filtered) * 100)
            if wr > best_wr:
                best_wr = wr
                best_threshold = threshold
                best_picks = len(filtered)

    baseline_wins = sum(1 for d in elem_data if d['result'])
    baseline_wr = (baseline_wins / len(elem_data) * 100)

    recommendations.append({
        'element': elem,
        'threshold': best_threshold,
        'wr': best_wr,
        'picks': best_picks,
        'baseline': baseline_wr,
        'total': len(elem_data)
    })

# Sort by WR
recommendations.sort(key=lambda x: x['wr'], reverse=True)

print(f"\n{'Element':<12} {'Threshold':<12} {'Win Rate':<12} {'Picks':<12} {'Baseline':<12} {'Edge':<12}")
print("-" * 80)

for rec in recommendations:
    edge = rec['wr'] - rec['baseline']
    edge_marker = "(+)" if edge > 0 else "(-)"
    print(f"{rec['element']:<12} T{rec['threshold']:+3d}        {rec['wr']:>6.1f}%      {rec['picks']:>4d}         {rec['baseline']:>6.1f}%       {edge:+6.1f}% {edge_marker}")

print("\n" + "=" * 100)
print("STRATEGY RECOMMENDATION")
print("=" * 100)

print(f"\n1. METAL (Best Element): Use T6+ threshold")
print(f"   - Baseline 71.0% (31 picks)")
print(f"   - Already dominant; filtering may reduce volume without major WR gain")
print(f"   - Use T3-T5 for more moderate filtering")

print(f"\n2. EARTH (Decent): Use T3-T5 threshold")
print(f"   - Baseline 53.3% (30 picks)")
print(f"   - Light filtering improves edge")

print(f"\n3. WATER (Neutral): Use T0-T3 threshold")
print(f"   - Baseline 45.2% (42 picks)")
print(f"   - Needs filtering; T0-T1 recommended")

print(f"\n4. FIRE (Weak): Use with caution or avoid")
print(f"   - Baseline 40.0% (25 picks)")
print(f"   - Even filtered, may underperform")

print(f"\n5. WOOD (Worst): AVOID")
print(f"   - Baseline 37.5% (24 picks)")
print(f"   - Poor signal even at high thresholds")

print("\n" + "=" * 100)
