import csv
import statistics

matchup_file = "Golf Historics v3 - 2BMatchup (8).csv"

# Column indices
lp_score_idx = 52       # BA - LP SCore
py_score_idx = 57       # BF - Py Score
wl_combined_idx = 62    # BK - PY & LP W/L

# Load data
data = []

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        if not row or len(row) < wl_combined_idx + 1:
            continue

        try:
            # Get scores
            lp_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
            py_str = row[py_score_idx].strip() if py_score_idx < len(row) else ''

            if not lp_str or lp_str in ['', '#REF!'] or not py_str or py_str in ['', '#REF!']:
                continue

            lp_score = float(lp_str)
            py_score = float(py_str)

            # Get W/L result
            wl = row[wl_combined_idx].strip() if wl_combined_idx < len(row) else ''
            is_win = None
            if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                is_win = True
            elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                is_win = False

            if is_win is None:
                continue

            data.append({
                'lp': lp_score,
                'py': py_score,
                'result': is_win
            })

        except (ValueError, IndexError):
            continue

print(f"\n" + "=" * 120)
print(f"WEIGHTING OPTIMIZATION: Life Path vs Personal Year")
print(f"=" * 120)
print(f"\nTotal picks with both scores + W/L: {len(data)}\n")

if not data:
    print("ERROR: No data found!")
    exit(1)

# Test different weightings
weightings = [
    (1.0, 0.0, "100% LP / 0% PY"),
    (0.9, 0.1, "90% LP / 10% PY"),
    (0.8, 0.2, "80% LP / 20% PY"),
    (0.7, 0.3, "70% LP / 30% PY"),
    (0.6, 0.4, "60% LP / 40% PY"),
    (0.5, 0.5, "50% LP / 50% PY (Current)"),
    (0.4, 0.6, "40% LP / 60% PY"),
    (0.3, 0.7, "30% LP / 70% PY"),
    (0.2, 0.8, "20% LP / 80% PY"),
    (0.1, 0.9, "10% LP / 90% PY"),
    (0.0, 1.0, "0% LP / 100% PY"),
]

results_by_weight = []

for lp_weight, py_weight, label in weightings:
    # Calculate weighted scores
    weighted_data = []
    for d in data:
        weighted_score = (d['lp'] * lp_weight) + (d['py'] * py_weight)
        weighted_data.append({
            'score': weighted_score,
            'result': d['result']
        })

    # Test thresholds
    thresholds = list(range(-2, 9))
    best_threshold = None
    best_wr = 0
    best_picks = 0

    for threshold in thresholds:
        filtered = [d for d in weighted_data if d['score'] > threshold]
        if len(filtered) >= 5:
            wins = sum(1 for d in filtered if d['result'])
            wr = (wins / len(filtered) * 100)
            if wr > best_wr:
                best_wr = wr
                best_threshold = threshold
                best_picks = len(filtered)

    # Baseline
    baseline_wins = sum(1 for d in weighted_data if d['result'])
    baseline_wr = (baseline_wins / len(weighted_data) * 100)

    edge = best_wr - baseline_wr

    results_by_weight.append({
        'label': label,
        'lp_weight': lp_weight,
        'py_weight': py_weight,
        'baseline_wr': baseline_wr,
        'best_threshold': best_threshold,
        'best_wr': best_wr,
        'best_picks': best_picks,
        'edge': edge
    })

# Sort by edge improvement
results_by_weight.sort(key=lambda x: x['edge'], reverse=True)

# Summary table
print(f"{'Weighting':<25} {'Baseline':<12} {'Best T':<8} {'Best WR':<10} {'Picks':<8} {'Edge':<10}")
print("-" * 90)

for r in results_by_weight:
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    edge_str = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    print(f"{r['label']:<25} {r['baseline_wr']:>10.1f}% {t_str:<8} {r['best_wr']:<9.1f}% {r['best_picks']:<8} {edge_str:<10}")

print("\n" + "=" * 120)
print("RECOMMENDATION")
print("=" * 120)

best = results_by_weight[0]
print(f"\nBEST WEIGHTING: {best['label']}")
print(f"  Baseline WR: {best['baseline_wr']:.1f}%")
print(f"  Best threshold: T{best['best_threshold']:+d}")
print(f"  Best WR: {best['best_wr']:.1f}% ({best['best_picks']} picks)")
print(f"  Edge improvement: +{best['edge']:.1f} pp")

current = [r for r in results_by_weight if '50%' in r['label']][0]
print(f"\nCURRENT (50/50): {current['baseline_wr']:.1f}% baseline -- {current['best_wr']:.1f}% at T{current['best_threshold']:+d} (+{current['edge']:.1f} pp)")

improvement = best['best_wr'] - current['best_wr']
if improvement > 0:
    print(f"\nOPTIMAL IS {improvement:.1f}pp BETTER than current 50/50 blend")
else:
    print(f"\nOPTIMAL is {abs(improvement):.1f}pp worse than current 50/50 blend")

# Detailed analysis for top 3
print("\n" + "=" * 120)
print("TOP 3 WEIGHTINGS - DETAILED THRESHOLD ANALYSIS")
print("=" * 120)

for idx, r in enumerate(results_by_weight[:3], 1):
    print(f"\n{idx}. {r['label']}")
    print("-" * 90)

    weighted_data = []
    for d in data:
        weighted_score = (d['lp'] * r['lp_weight']) + (d['py'] * r['py_weight'])
        weighted_data.append({
            'score': weighted_score,
            'result': d['result']
        })

    print(f"{'Threshold':<12} {'Win Rate':<12} {'Picks':<10} {'Status':<20}")
    print("-" * 60)

    thresholds = list(range(-2, 9))
    for threshold in thresholds:
        filtered = [d for d in weighted_data if d['score'] > threshold]
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
