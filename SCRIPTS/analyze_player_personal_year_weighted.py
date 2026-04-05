import csv
from collections import defaultdict
import json

# Read ANALYSIS sheet
analysis_file = "Golf Historics v3 - ANALYSIS (6).csv"
player_data = defaultdict(lambda: {year: [] for year in range(1, 10)})

with open(analysis_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    player_name_idx = header.index('player_name')
    score_idx = header.index('score')
    personal_year_idx = header.index('Personal Year')
    off_par_idx = header.index('off_par')

    for row in reader:
        if not row or row[player_name_idx].strip() == '':
            continue

        player_name = row[player_name_idx].strip()

        # Only process complete rounds (score must be numeric)
        try:
            score = float(row[score_idx]) if row[score_idx] else None
            if score is None:
                continue

            personal_year = row[personal_year_idx].strip() if personal_year_idx < len(row) else ''
            if not personal_year or personal_year == '' or not personal_year.isdigit():
                continue

            py_num = int(personal_year)
            off_par = float(row[off_par_idx]) if off_par_idx < len(row) and row[off_par_idx] else None

            player_data[player_name][py_num].append({
                'score': score,
                'off_par': off_par
            })
        except (ValueError, IndexError):
            continue

# Analyze each player with weighting
player_summaries = {}
best_year_weighted = defaultdict(lambda: {'weighted_count': 0, 'unweighted_count': 0, 'players': []})
worst_year_weighted = defaultdict(lambda: {'weighted_count': 0, 'unweighted_count': 0, 'players': []})

print("\n" + "="*100)
print("WEIGHTED PERSONAL YEAR ANALYSIS (By Years Available)")
print("="*100)

for player_name in sorted(player_data.keys()):
    py_stats = {}
    total_rounds = 0

    # Calculate stats for each Personal Year
    for py_num in range(1, 10):
        rounds = player_data[player_name][py_num]
        if len(rounds) > 0:
            total_rounds += len(rounds)
            avg_off_par = sum(r['off_par'] for r in rounds if r['off_par'] is not None) / len(rounds)
            py_stats[py_num] = {
                'count': len(rounds),
                'avg_off_par': avg_off_par
            }
        else:
            py_stats[py_num] = {
                'count': 0,
                'avg_off_par': None
            }

    # Only include players with meaningful data (30+ rounds)
    if total_rounds >= 30:
        # Find best and worst years for this player
        valid_years = {py: stats for py, stats in py_stats.items() if stats['count'] > 0}
        num_valid_years = len(valid_years)

        if num_valid_years > 0:
            best_year = min(valid_years.items(), key=lambda x: x[1]['avg_off_par'])
            worst_year = max(valid_years.items(), key=lambda x: x[1]['avg_off_par'])

            # Weight = 1 / num_valid_years (so players with all 9 years count 1/9 each,
            # players with 3 years count 1/3 each)
            year_weight = 1.0 / num_valid_years

            player_summary = {
                'total_rounds': total_rounds,
                'num_years_played': num_valid_years,
                'year_weight': year_weight,
                'best_year': best_year[0],
                'best_avg_off_par': best_year[1]['avg_off_par'],
                'best_count': best_year[1]['count'],
                'worst_year': worst_year[0],
                'worst_avg_off_par': worst_year[1]['avg_off_par'],
                'worst_count': worst_year[1]['count'],
                'all_years': py_stats
            }

            player_summaries[player_name] = player_summary

            # Track weighted best/worst
            best_year_weighted[best_year[0]]['weighted_count'] += year_weight
            best_year_weighted[best_year[0]]['unweighted_count'] += 1
            best_year_weighted[best_year[0]]['players'].append({
                'player': player_name,
                'years_data': num_valid_years,
                'weight': year_weight,
                'off_par': best_year[1]['avg_off_par']
            })

            worst_year_weighted[worst_year[0]]['weighted_count'] += year_weight
            worst_year_weighted[worst_year[0]]['unweighted_count'] += 1
            worst_year_weighted[worst_year[0]]['players'].append({
                'player': player_name,
                'years_data': num_valid_years,
                'weight': year_weight,
                'off_par': worst_year[1]['avg_off_par']
            })

# Print detailed breakdown
print(f"\nAnalyzed {len(player_summaries)} players with 30+ rounds\n")

print("Distribution of Years Available per Player:")
years_dist = defaultdict(int)
for summary in player_summaries.values():
    years_dist[summary['num_years_played']] += 1

for num_years in sorted(years_dist.keys()):
    count = years_dist[num_years]
    pct = count / len(player_summaries) * 100
    print(f"  {num_years} years: {count:3d} players ({pct:5.1f}%)")

# Summary comparison
print("\n" + "="*100)
print("WEIGHTED vs UNWEIGHTED BEST YEAR COMPARISON")
print("="*100)

print(f"\n{'Year':<5} {'Unweighted':<20} {'Unweighted %':<15} {'Weighted':<20} {'Weighted %':<15}")
print("-" * 80)

total_unweighted = sum(v['unweighted_count'] for v in best_year_weighted.values())
total_weighted = sum(v['weighted_count'] for v in best_year_weighted.values())

for py_num in range(1, 10):
    unw_count = best_year_weighted[py_num]['unweighted_count']
    unw_pct = (unw_count / total_unweighted * 100) if total_unweighted > 0 else 0
    w_count = best_year_weighted[py_num]['weighted_count']
    w_pct = (w_count / total_weighted * 100) if total_weighted > 0 else 0

    print(f"{py_num:<5} {unw_count:<20} {unw_pct:<14.1f}% {w_count:<20.2f} {w_pct:<14.1f}%")

print("\n" + "="*100)
print("WEIGHTED vs UNWEIGHTED WORST YEAR COMPARISON")
print("="*100)

print(f"\n{'Year':<5} {'Unweighted':<20} {'Unweighted %':<15} {'Weighted':<20} {'Weighted %':<15}")
print("-" * 80)

total_unweighted_worst = sum(v['unweighted_count'] for v in worst_year_weighted.values())
total_weighted_worst = sum(v['weighted_count'] for v in worst_year_weighted.values())

for py_num in range(1, 10):
    unw_count = worst_year_weighted[py_num]['unweighted_count']
    unw_pct = (unw_count / total_unweighted_worst * 100) if total_unweighted_worst > 0 else 0
    w_count = worst_year_weighted[py_num]['weighted_count']
    w_pct = (w_count / total_weighted_worst * 100) if total_weighted_worst > 0 else 0

    print(f"{py_num:<5} {unw_count:<20} {unw_pct:<14.1f}% {w_count:<20.2f} {w_pct:<14.1f}%")

# Find biggest changes from weighting
print("\n" + "="*100)
print("IMPACT OF WEIGHTING (Biggest Changes)")
print("="*100)

print("\nBEST YEAR:")
best_changes = []
for py_num in range(1, 10):
    unw_pct = (best_year_weighted[py_num]['unweighted_count'] / total_unweighted * 100) if total_unweighted > 0 else 0
    w_pct = (best_year_weighted[py_num]['weighted_count'] / total_weighted * 100) if total_weighted > 0 else 0
    change = w_pct - unw_pct
    best_changes.append((py_num, change, unw_pct, w_pct))

for py_num, change, unw_pct, w_pct in sorted(best_changes, key=lambda x: abs(x[1]), reverse=True):
    direction = "UP" if change > 0 else "DN"
    print(f"  Year {py_num}: {unw_pct:5.1f}% -> {w_pct:5.1f}% ({direction} {abs(change):5.1f} pp)")

print("\nWORST YEAR:")
worst_changes = []
for py_num in range(1, 10):
    unw_pct = (worst_year_weighted[py_num]['unweighted_count'] / total_unweighted_worst * 100) if total_unweighted_worst > 0 else 0
    w_pct = (worst_year_weighted[py_num]['weighted_count'] / total_weighted_worst * 100) if total_weighted_worst > 0 else 0
    change = w_pct - unw_pct
    worst_changes.append((py_num, change, unw_pct, w_pct))

for py_num, change, unw_pct, w_pct in sorted(worst_changes, key=lambda x: abs(x[1]), reverse=True):
    direction = "UP" if change > 0 else "DN"
    print(f"  Year {py_num}: {unw_pct:5.1f}% -> {w_pct:5.1f}% ({direction} {abs(change):5.1f} pp)")

# Save results
results = {
    'methodology': 'Players weighted by 1/num_years_played (so someone with 3 years counts as 0.33, someone with 9 years counts as 0.11)',
    'players_analyzed': len(player_summaries),
    'best_year_unweighted': {str(k): v['unweighted_count'] for k, v in best_year_weighted.items()},
    'best_year_weighted': {str(k): round(v['weighted_count'], 2) for k, v in best_year_weighted.items()},
    'worst_year_unweighted': {str(k): v['unweighted_count'] for k, v in worst_year_weighted.items()},
    'worst_year_weighted': {str(k): round(v['weighted_count'], 2) for k, v in worst_year_weighted.items()},
    'years_distribution': dict(years_dist),
    'player_summaries': player_summaries,
}

with open('player_personal_year_weighted_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*100)
print(f"Results saved to: player_personal_year_weighted_analysis.json")
print("="*100)
