import csv

matchup_file = "Golf Historics v3 - 2BMatchup (8).csv"

# Column indices
lp_a_idx = 22           # LP [A]
lp_b_idx = 23           # LP [B]
py_a_idx = 24           # PY [A]
py_b_idx = 25           # PY [B]
lp_score_idx = 52       # BA - LP SCore
lp_pick_idx = 53        # BB - LP Pick
wl_idx = 54             # BC - W/L [LP]

# Load data for all years
lp_data = {i: [] for i in range(1, 10)}
py_data = {i: [] for i in range(1, 10)}

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

            # Assign to LP years
            if lp_a and 1 <= lp_a <= 9:
                lp_data[lp_a].append(base_data)
            if lp_b and 1 <= lp_b <= 9:
                lp_data[lp_b].append(base_data)

            # Assign to PY years
            if py_a and 1 <= py_a <= 9:
                py_data[py_a].append(base_data)
            if py_b and 1 <= py_b <= 9:
                py_data[py_b].append(base_data)

        except (ValueError, IndexError):
            continue

# Analysis function
def analyze_year(year_num, data):
    if not data or len(data) < 5:
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
        'year': year_num,
        'total_picks': len(data),
        'baseline_wr': wr,
        'best_threshold': best_threshold,
        'best_wr': best_wr,
        'best_picks': best_picks,
        'edge': (best_wr - wr) if best_wr > 0 else 0
    }

# Run analysis
print("\n" + "=" * 120)
print("LIFE PATH ANALYSIS - ALL YEARS (1-9)")
print("=" * 120)

lp_results = []
for year in range(1, 10):
    result = analyze_year(year, lp_data[year])
    if result:
        lp_results.append(result)

# Sort by edge
lp_results.sort(key=lambda x: x['edge'], reverse=True)

print(f"\n{'Year':<8} {'Picks':<10} {'Baseline':<12} {'Best T':<8} {'Best WR':<10} {'Edge':<10}")
print("-" * 90)

for r in lp_results:
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    edge_str = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    print(f"{r['year']:<8} {r['total_picks']:<10} {r['baseline_wr']:>10.1f}% {t_str:<8} {r['best_wr']:<9.1f}% {edge_str:<10}")

print("\n" + "=" * 120)
print("PERSONAL YEAR ANALYSIS - ALL YEARS (1-9)")
print("=" * 120)

py_results = []
for year in range(1, 10):
    result = analyze_year(year, py_data[year])
    if result:
        py_results.append(result)

# Sort by edge
py_results.sort(key=lambda x: x['edge'], reverse=True)

print(f"\n{'Year':<8} {'Picks':<10} {'Baseline':<12} {'Best T':<8} {'Best WR':<10} {'Edge':<10}")
print("-" * 90)

for r in py_results:
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    edge_str = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    print(f"{r['year']:<8} {r['total_picks']:<10} {r['baseline_wr']:>10.1f}% {t_str:<8} {r['best_wr']:<9.1f}% {edge_str:<10}")

# Ranking summary
print("\n" + "=" * 120)
print("RANKING SUMMARY")
print("=" * 120)

print("\nLIFE PATH - RANKED BY EDGE:")
for i, r in enumerate(lp_results[:5], 1):
    print(f"  {i}. LP{r['year']}: +{r['edge']:.1f}pp ({r['baseline_wr']:.1f}% -> {r['best_wr']:.1f}% at T{r['best_threshold']:+d}, {r['best_picks']} picks)")

print("\nPERSONAL YEAR - RANKED BY EDGE:")
for i, r in enumerate(py_results[:5], 1):
    print(f"  {i}. PY{r['year']}: +{r['edge']:.1f}pp ({r['baseline_wr']:.1f}% -> {r['best_wr']:.1f}% at T{r['best_threshold']:+d}, {r['best_picks']} picks)")

print("\nLIFE PATH - RANKED BY BASELINE WR:")
lp_by_baseline = sorted(lp_results, key=lambda x: x['baseline_wr'], reverse=True)
for i, r in enumerate(lp_by_baseline[:5], 1):
    print(f"  {i}. LP{r['year']}: {r['baseline_wr']:.1f}% ({r['total_picks']} picks)")

print("\nPERSONAL YEAR - RANKED BY BASELINE WR:")
py_by_baseline = sorted(py_results, key=lambda x: x['baseline_wr'], reverse=True)
for i, r in enumerate(py_by_baseline[:5], 1):
    print(f"  {i}. PY{r['year']}: {r['baseline_wr']:.1f}% ({r['total_picks']} picks)")
