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

# Analyze each player
player_summaries = {}
global_py_stats = defaultdict(lambda: {
    'count': 0,
    'total_off_par': 0,
    'num_players': 0,
    'players_where_best': [],
    'players_where_worst': []
})

print("\n" + "="*100)
print("INDIVIDUAL PLAYER PERSONAL YEAR ANALYSIS")
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
        if len(valid_years) > 0:
            best_year = min(valid_years.items(), key=lambda x: x[1]['avg_off_par'])
            worst_year = max(valid_years.items(), key=lambda x: x[1]['avg_off_par'])

            player_summary = {
                'total_rounds': total_rounds,
                'num_years_played': len(valid_years),
                'best_year': best_year[0],
                'best_avg_off_par': best_year[1]['avg_off_par'],
                'best_count': best_year[1]['count'],
                'worst_year': worst_year[0],
                'worst_avg_off_par': worst_year[1]['avg_off_par'],
                'worst_count': worst_year[1]['count'],
                'all_years': py_stats
            }

            player_summaries[player_name] = player_summary

            # Track global stats
            for py_num, stats in py_stats.items():
                if stats['count'] > 0:
                    global_py_stats[py_num]['count'] += stats['count']
                    global_py_stats[py_num]['total_off_par'] += stats['count'] * stats['avg_off_par']
                    global_py_stats[py_num]['num_players'] += 1

            # Print individual player summary
            print(f"\n{player_name} ({total_rounds} rounds across {len(valid_years)} years)")
            print(f"  BEST YEAR:  Year {best_year[0]} ({best_year[1]['count']} rounds) — {best_year[1]['avg_off_par']:.3f} off-par")
            print(f"  WORST YEAR: Year {worst_year[0]} ({worst_year[1]['count']} rounds) — {worst_year[1]['avg_off_par']:.3f} off-par")
            print(f"  Spread: {worst_year[1]['avg_off_par'] - best_year[1]['avg_off_par']:.3f} strokes")
            print(f"  All Years Performance:")
            for py_num in sorted(valid_years.keys()):
                if py_stats[py_num]['count'] > 0:
                    print(f"    Year {py_num}: {py_stats[py_num]['count']:3d} rounds @ {py_stats[py_num]['avg_off_par']:7.3f} off-par")

# Calculate global averages
print("\n" + "="*100)
print("SUMMARY: GLOBAL PERSONAL YEAR PERFORMANCE ACROSS ALL PLAYERS")
print("="*100)

global_summary = {}
for py_num in range(1, 10):
    stats = global_py_stats[py_num]
    if stats['count'] > 0:
        avg_off_par = stats['total_off_par'] / stats['count']
        global_summary[py_num] = {
            'total_rounds': stats['count'],
            'avg_off_par': avg_off_par,
            'num_players': stats['num_players']
        }

print("\nGlobal Off-Par Average by Personal Year:")
print(f"\n{'Year':<5} {'Rounds':<10} {'Players':<10} {'Avg Off-Par':<15} {'Diff vs Baseline':<20}")
print("-" * 70)

overall_avg = sum(s['total_rounds'] * s['avg_off_par'] for s in global_summary.values()) / sum(s['total_rounds'] for s in global_summary.values())

for py_num in sorted(global_summary.keys()):
    stats = global_summary[py_num]
    diff = stats['avg_off_par'] - overall_avg
    print(f"{py_num:<5} {stats['total_rounds']:<10} {stats['num_players']:<10} {stats['avg_off_par']:<15.4f} {diff:+.4f}")

# Find players where each year is best
print("\n" + "="*100)
print("PLAYERS WHERE EACH PERSONAL YEAR IS THEIR BEST YEAR")
print("="*100)

best_year_count = defaultdict(list)
for player, summary in player_summaries.items():
    best_year_count[summary['best_year']].append({
        'player': player,
        'off_par': summary['best_avg_off_par'],
        'rounds': summary['best_count']
    })

for py_num in sorted(best_year_count.keys()):
    players = sorted(best_year_count[py_num], key=lambda x: x['off_par'])
    print(f"\nYear {py_num} is BEST for {len(players)} players:")
    for p in players[:10]:  # Top 10
        print(f"  {p['player']:25s} ({p['rounds']:3d} rounds) @ {p['off_par']:7.3f} off-par")
    if len(players) > 10:
        print(f"  ... and {len(players) - 10} more players")

# Find players where each year is worst
print("\n" + "="*100)
print("PLAYERS WHERE EACH PERSONAL YEAR IS THEIR WORST YEAR")
print("="*100)

worst_year_count = defaultdict(list)
for player, summary in player_summaries.items():
    worst_year_count[summary['worst_year']].append({
        'player': player,
        'off_par': summary['worst_avg_off_par'],
        'rounds': summary['worst_count']
    })

for py_num in sorted(worst_year_count.keys()):
    players = sorted(worst_year_count[py_num], key=lambda x: x['off_par'], reverse=True)
    print(f"\nYear {py_num} is WORST for {len(players)} players:")
    for p in players[:10]:  # Top 10 worst
        print(f"  {p['player']:25s} ({p['rounds']:3d} rounds) @ {p['off_par']:7.3f} off-par")
    if len(players) > 10:
        print(f"  ... and {len(players) - 10} more players")

# Save detailed results to JSON
results = {
    'global_summary': {str(k): v for k, v in global_summary.items()},
    'player_summaries': player_summaries,
    'best_year_distribution': {str(k): [{'player': p['player'], 'off_par': p['off_par'], 'rounds': p['rounds']} for p in v] for k, v in best_year_count.items()},
    'worst_year_distribution': {str(k): [{'player': p['player'], 'off_par': p['off_par'], 'rounds': p['rounds']} for p in v] for k, v in worst_year_count.items()},
}

with open('player_personal_year_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*100)
print(f"Analyzed {len(player_summaries)} players with 30+ rounds")
print(f"Results saved to: player_personal_year_analysis_results.json")
print("="*100)
