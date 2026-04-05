import csv
import statistics

matchup_file = "Golf Historics v3 - 2BMatchup (7).csv"

# Core columns for LP analysis
lp_score_idx = 52       # BA - LP SCore
lp_pick_idx = 53        # BB - LP Pick
wl_idx = 54             # BC - W/L [LP]

# Filter indicator columns
same_ele_idx = 36       # Same Ele
same_lp_a_idx = 22      # W - LP [A]
same_lp_b_idx = 23      # X - LP [B]
same_py_idx = 42        # Same PY
same_tithi_idx = 45     # Same Tithi

# Load data for each filter
filters = {
    'same_ele': [],
    'same_lp': [],
    'same_py': [],
    'same_tithi': []
}

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        if not row or len(row) < max(wl_idx + 1, same_tithi_idx + 1):
            continue

        try:
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
            wl = row[wl_idx].strip() if wl_idx < len(row) else ''
            is_win = None
            if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                is_win = True
            elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                is_win = False

            if is_win is None:
                continue

            base_data = {'lp_score': lp_score, 'result': is_win}

            # Check filters
            if row[same_ele_idx].strip().upper() == 'TRUE':
                filters['same_ele'].append(base_data)

            # Same LP: Check if LP [A] == LP [B]
            lp_a = row[same_lp_a_idx].strip() if same_lp_a_idx < len(row) else ''
            lp_b = row[same_lp_b_idx].strip() if same_lp_b_idx < len(row) else ''
            if lp_a and lp_b and lp_a == lp_b:
                filters['same_lp'].append(base_data)

            if row[same_py_idx].strip().upper() == 'TRUE':
                filters['same_py'].append(base_data)

            if row[same_tithi_idx].strip().upper() == 'TRUE':
                filters['same_tithi'].append(base_data)

        except (ValueError, IndexError):
            continue

# Analysis function
def analyze_filter(name, data):
    if not data:
        return None

    wins = sum(1 for d in data if d['result'])
    wr = (wins / len(data) * 100)

    thresholds = list(range(-2, 9))
    best_threshold = None
    best_wr = 0
    best_picks = 0

    for threshold in thresholds:
        filtered = [d for d in data if d['lp_score'] > threshold]
        if len(filtered) >= 5:
            wins_f = sum(1 for d in filtered if d['result'])
            wr_f = (wins_f / len(filtered) * 100)
            if wr_f > best_wr:
                best_wr = wr_f
                best_threshold = threshold
                best_picks = len(filtered)

    return {
        'name': name,
        'total_picks': len(data),
        'baseline_wr': wr,
        'best_threshold': best_threshold,
        'best_wr': best_wr,
        'best_picks': best_picks,
        'edge': (best_wr - wr) if best_wr > 0 else 0,
        'data': data
    }

# Run analysis
print("\n" + "=" * 100)
print("LP SCORE ANALYSIS: FILTER COMPARISON (BA, BB, BC Only)")
print("=" * 100)

results = []
for filter_name, filter_data in filters.items():
    result = analyze_filter(filter_name.replace('_', ' ').title(), filter_data)
    if result:
        results.append(result)

# Summary table
print(f"\n{'Filter':<20} {'Total':<10} {'Baseline':<12} {'Best T':<8} {'Best WR':<10} {'Picks':<8} {'Edge':<10}")
print("-" * 90)

for r in sorted(results, key=lambda x: x['edge'], reverse=True):
    edge = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    print(f"{r['name']:<20} {r['total_picks']:<10} {r['baseline_wr']:<11.1f}% {t_str:<8} {r['best_wr']:<9.1f}% {r['best_picks']:<8} {edge:<10}")

# Detailed breakdown for each filter
print("\n" + "=" * 100)
print("DETAILED THRESHOLD ANALYSIS BY FILTER")
print("=" * 100)

for r in sorted(results, key=lambda x: x['edge'], reverse=True):
    print(f"\n{r['name'].upper()}")
    print("-" * 90)
    print(f"Total picks: {r['total_picks']} | Baseline WR: {r['baseline_wr']:.1f}%\n")

    thresholds = list(range(-2, 9))
    print(f"{'Threshold':<12} {'Win Rate':<12} {'Picks':<10} {'Status':<20}")
    print("-" * 60)

    for threshold in thresholds:
        filtered = [d for d in r['data'] if d['lp_score'] > threshold]
        if not filtered:
            continue

        wins = sum(1 for d in filtered if d['result'])
        wr = (wins / len(filtered) * 100)

        if wr >= 60:
            status = "STRONG"
        elif wr >= 55:
            status = "Very Good"
        elif wr >= 50:
            status = "Good"
        else:
            status = "WEAK"

        print(f"T{threshold:+3d}        {wr:>6.1f}%        {len(filtered):>6d}       {status:<20}")

print("\n" + "=" * 100)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 100)

for r in sorted(results, key=lambda x: x['edge'], reverse=True):
    print(f"\n{r['name'].upper()}")
    print(f"  Baseline: {r['baseline_wr']:.1f}% ({r['total_picks']} picks)")
    if r['best_threshold'] is not None:
        print(f"  Best filter: T{r['best_threshold']:+d} -> {r['best_wr']:.1f}% ({r['best_picks']} picks)")
        print(f"  Edge: +{r['edge']:.1f} pp")
    else:
        print(f"  No effective filtering found")

print("\n" + "=" * 100)
print("RANKING BY EDGE IMPROVEMENT")
print("=" * 100)
for i, r in enumerate(sorted(results, key=lambda x: x['edge'], reverse=True), 1):
    if r['best_threshold'] is not None:
        print(f"  {i}. {r['name']:<20} +{r['edge']:.1f}pp (T{r['best_threshold']:+d}, {r['best_wr']:.1f}% WR, {r['best_picks']} picks)")
    else:
        print(f"  {i}. {r['name']:<20} {r['baseline_wr']:.1f}% baseline ({r['total_picks']} picks)")
