import csv
import statistics

matchup_file = "Golf Historics v3 - 2BMatchup (8).csv"

# Column indices
lp_a_idx = 22           # LP [A]
lp_b_idx = 23           # LP [B]
py_a_idx = 24           # PY [A]
py_b_idx = 25           # PY [B]
lp_score_idx = 52       # BA - LP SCore
lp_pick_idx = 53        # BB - LP Pick
wl_idx = 54             # BC - W/L [LP]

# Target years
target_years = [1, 6, 7]

# Load data by filter
filters = {
    'lp_1_6_7': [],
    'py_1_6_7': [],
    'lp_1': [],
    'lp_6': [],
    'lp_7': [],
    'py_1': [],
    'py_6': [],
    'py_7': []
}

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        if not row or len(row) < wl_idx + 1:
            continue

        try:
            # Get LP and PY values
            try:
                lp_a = int(row[lp_a_idx].strip()) if lp_a_idx < len(row) and row[lp_a_idx].strip().isdigit() else None
                lp_b = int(row[lp_b_idx].strip()) if lp_b_idx < len(row) and row[lp_b_idx].strip().isdigit() else None
                py_a = int(row[py_a_idx].strip()) if py_a_idx < len(row) and row[py_a_idx].strip().isdigit() else None
                py_b = int(row[py_b_idx].strip()) if py_b_idx < len(row) and row[py_b_idx].strip().isdigit() else None
            except:
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
            wl = row[wl_idx].strip() if wl_idx < len(row) else ''
            is_win = None
            if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                is_win = True
            elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                is_win = False

            if is_win is None:
                continue

            base_data = {'lp_score': lp_score, 'result': is_win}

            # Filter by LP 1, 6, 7
            if (lp_a in target_years) or (lp_b in target_years):
                filters['lp_1_6_7'].append(base_data)

                if lp_a in [1] or lp_b in [1]:
                    filters['lp_1'].append(base_data)
                if lp_a in [6] or lp_b in [6]:
                    filters['lp_6'].append(base_data)
                if lp_a in [7] or lp_b in [7]:
                    filters['lp_7'].append(base_data)

            # Filter by PY 1, 6, 7
            if (py_a in target_years) or (py_b in target_years):
                filters['py_1_6_7'].append(base_data)

                if py_a in [1] or py_b in [1]:
                    filters['py_1'].append(base_data)
                if py_a in [6] or py_b in [6]:
                    filters['py_6'].append(base_data)
                if py_a in [7] or py_b in [7]:
                    filters['py_7'].append(base_data)

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
print("\n" + "=" * 110)
print("LP SCORE ANALYSIS: Life Path & Personal Year Years 1, 6, 7 Only")
print("=" * 110)

results = []

# LP analysis
print("\nLIFE PATH ANALYSIS (Years 1, 6, 7):")
print("-" * 110)

lp_combined = analyze_filter('LP 1, 6, 7 Combined', filters['lp_1_6_7'])
if lp_combined:
    results.append(lp_combined)
    print(f"LP 1, 6, 7 Combined: {lp_combined['total_picks']} picks, {lp_combined['baseline_wr']:.1f}% baseline")
    print(f"  Best: T{lp_combined['best_threshold']:+d} -> {lp_combined['best_wr']:.1f}% (+{lp_combined['edge']:.1f} pp)\n")

for year in [1, 6, 7]:
    result = analyze_filter(f'LP {year}', filters[f'lp_{year}'])
    if result:
        results.append(result)
        print(f"LP {year}: {result['total_picks']} picks, {result['baseline_wr']:.1f}% baseline")
        if result['best_threshold'] is not None:
            print(f"  Best: T{result['best_threshold']:+d} -> {result['best_wr']:.1f}% (+{result['edge']:.1f} pp)")
        print()

# PY analysis
print("\nPERSONAL YEAR ANALYSIS (Years 1, 6, 7):")
print("-" * 110)

py_combined = analyze_filter('PY 1, 6, 7 Combined', filters['py_1_6_7'])
if py_combined:
    results.append(py_combined)
    print(f"PY 1, 6, 7 Combined: {py_combined['total_picks']} picks, {py_combined['baseline_wr']:.1f}% baseline")
    print(f"  Best: T{py_combined['best_threshold']:+d} -> {py_combined['best_wr']:.1f}% (+{py_combined['edge']:.1f} pp)\n")

for year in [1, 6, 7]:
    result = analyze_filter(f'PY {year}', filters[f'py_{year}'])
    if result:
        results.append(result)
        print(f"PY {year}: {result['total_picks']} picks, {result['baseline_wr']:.1f}% baseline")
        if result['best_threshold'] is not None:
            print(f"  Best: T{result['best_threshold']:+d} -> {result['best_wr']:.1f}% (+{result['edge']:.1f} pp)")
        print()

# Detailed breakdown for top performers
print("\n" + "=" * 110)
print("DETAILED THRESHOLD ANALYSIS - TOP PERFORMERS")
print("=" * 110)

for r in sorted(results, key=lambda x: x['edge'] if x['edge'] else 0, reverse=True)[:6]:
    if not r:
        continue

    print(f"\n{r['name'].upper()}")
    print(f"Total: {r['total_picks']} picks | Baseline: {r['baseline_wr']:.1f}%")
    print("-" * 90)
    print(f"{'Threshold':<12} {'Win Rate':<12} {'Picks':<10} {'Status':<20}")
    print("-" * 60)

    thresholds = list(range(-2, 9))
    for threshold in thresholds:
        filtered = [d for d in r['data'] if d['lp_score'] > threshold]
        if not filtered or len(filtered) < 5:
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

print("\n" + "=" * 110)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 110)

print("\nBEST SIGNALS:")
for i, r in enumerate(sorted(results, key=lambda x: x['edge'] if x['edge'] else 0, reverse=True)[:5], 1):
    if r and r['best_threshold'] is not None:
        print(f"  {i}. {r['name']:<25} {r['baseline_wr']:>6.1f}% -> {r['best_wr']:<6.1f}% at T{r['best_threshold']:+d} (+{r['edge']:.1f}pp, {r['best_picks']} picks)")
