import csv

matchup_file = "Golf Historics v3 - 2BMatchup (7).csv"

# Column indices for main LP SCore section
main_lp_score_idx = 52      # LP SCore (main)
main_lp_pick_idx = 53       # LP Pick (main)
main_wl_idx = 54            # W/L [LP] (main)

# Column indices for Same LP/PY/Tithi sections
same_lp_idx = 39            # Same LP indicator
same_lp_pick_idx = 40       # LP Pick (for Same LP section)
same_lp_wl_idx = 41         # W/L (for Same LP section)

same_py_idx = 42            # Same PY indicator
same_py_pick_idx = 43       # PY Pick (for Same PY section)
same_py_wl_idx = 44         # W/L (for Same PY section)

same_tithi_idx = 45         # Same Tithi indicator
same_tithi_pick_idx = 46    # Tithi Pick (for Same Tithi section)
same_tithi_wl_idx = 47      # W/L (for Same Tithi section)
horo_a_idx = 11        # Horoscope [A]
horo_b_idx = 12        # Horoscope [B]
zodiac_a_idx = 17      # Zodiac [A]
zodiac_b_idx = 18      # Zodiac [B]
tithi_a_idx = 19       # Tithi type [A]
tithi_b_idx = 20       # Tithi type [B]

# Load data
filters = {
    'same_lp': [],
    'same_py': [],
    'same_tithi': [],
    'same_horoscope': [],
    'same_zodiac': []
}

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        if not row or len(row) < max(main_lp_score_idx + 1, zodiac_b_idx + 1):
            continue

        try:
            # Get main LP Score (used by all)
            lp_score_str = row[main_lp_score_idx].strip() if main_lp_score_idx < len(row) else ''
            if not lp_score_str or lp_score_str in ['', '#REF!']:
                continue
            lp_score = float(lp_score_str)

            # Same LP check (uses cols 40, 41)
            same_lp = row[same_lp_idx].strip() if same_lp_idx < len(row) else ''
            if same_lp.upper() == 'TRUE':
                lp_pick = row[same_lp_pick_idx].strip() if same_lp_pick_idx < len(row) else ''
                if lp_pick:
                    wl = row[same_lp_wl_idx].strip() if same_lp_wl_idx < len(row) else ''
                    is_win = None
                    if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                        is_win = True
                    elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                        is_win = False
                    if is_win is not None:
                        filters['same_lp'].append({'lp_score': lp_score, 'result': is_win})

            # Same PY check (uses cols 43, 44)
            same_py = row[same_py_idx].strip() if same_py_idx < len(row) else ''
            if same_py.upper() == 'TRUE':
                py_pick = row[same_py_pick_idx].strip() if same_py_pick_idx < len(row) else ''
                if py_pick:
                    wl = row[same_py_wl_idx].strip() if same_py_wl_idx < len(row) else ''
                    is_win = None
                    if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                        is_win = True
                    elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                        is_win = False
                    if is_win is not None:
                        filters['same_py'].append({'lp_score': lp_score, 'result': is_win})

            # Same Tithi check (uses cols 46, 47)
            same_tithi = row[same_tithi_idx].strip() if same_tithi_idx < len(row) else ''
            if same_tithi.upper() == 'TRUE':
                tithi_pick = row[same_tithi_pick_idx].strip() if same_tithi_pick_idx < len(row) else ''
                if tithi_pick:
                    wl = row[same_tithi_wl_idx].strip() if same_tithi_wl_idx < len(row) else ''
                    is_win = None
                    if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                        is_win = True
                    elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                        is_win = False
                    if is_win is not None:
                        filters['same_tithi'].append({'lp_score': lp_score, 'result': is_win})

            # Same Horoscope check
            horo_a = row[horo_a_idx].strip() if horo_a_idx < len(row) else ''
            horo_b = row[horo_b_idx].strip() if horo_b_idx < len(row) else ''
            if horo_a and horo_b and horo_a == horo_b:
                # Use main LP section pick/WL for horoscope
                lp_pick = row[main_lp_pick_idx].strip() if main_lp_pick_idx < len(row) else ''
                if lp_pick:
                    wl = row[main_wl_idx].strip() if main_wl_idx < len(row) else ''
                    is_win = None
                    if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                        is_win = True
                    elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                        is_win = False
                    if is_win is not None:
                        filters['same_horoscope'].append({'lp_score': lp_score, 'result': is_win})

            # Same Zodiac check
            zodiac_a = row[zodiac_a_idx].strip() if zodiac_a_idx < len(row) else ''
            zodiac_b = row[zodiac_b_idx].strip() if zodiac_b_idx < len(row) else ''
            if zodiac_a and zodiac_b and zodiac_a == zodiac_b:
                # Use main LP section pick/WL for zodiac
                lp_pick = row[main_lp_pick_idx].strip() if main_lp_pick_idx < len(row) else ''
                if lp_pick:
                    wl = row[main_wl_idx].strip() if main_wl_idx < len(row) else ''
                    is_win = None
                    if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                        is_win = True
                    elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                        is_win = False
                    if is_win is not None:
                        filters['same_zodiac'].append({'lp_score': lp_score, 'result': is_win})

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
print("\n" + "=" * 120)
print("LP SCORE THRESHOLD ANALYSIS: MULTIPLE FILTERS")
print("=" * 120)

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
print("\n" + "=" * 120)
print("DETAILED THRESHOLD ANALYSIS BY FILTER")
print("=" * 120)

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

        if wr >= 55:
            status = "STRONG"
        elif wr >= 50:
            status = "Okay"
        else:
            status = "WEAK"

        print(f"T{threshold:+3d}        {wr:>6.1f}%        {len(filtered):>6d}       {status:<20}")

print("\n" + "=" * 120)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 120)

top_filter = max(results, key=lambda x: x['edge'])
print(f"\nBEST SIGNAL: {top_filter['name']}")
print(f"  - Baseline: {top_filter['baseline_wr']:.1f}% ({top_filter['total_picks']} picks)")
print(f"  - With T{top_filter['best_threshold']:+d} filter: {top_filter['best_wr']:.1f}% ({top_filter['best_picks']} picks)")
print(f"  - Edge: +{top_filter['edge']:.1f} pp")

print(f"\nRANKING (by edge improvement):")
for i, r in enumerate(sorted(results, key=lambda x: x['edge'], reverse=True), 1):
    print(f"  {i}. {r['name']:<20} +{r['edge']:.1f}pp edge (T{r['best_threshold']:+d}, {r['best_wr']:.1f}% WR)")
