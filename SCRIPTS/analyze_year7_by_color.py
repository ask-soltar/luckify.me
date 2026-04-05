import csv
from collections import defaultdict

# Read ANALYSIS sheet
analysis_file = "Golf Historics v3 - ANALYSIS (6).csv"
year7_by_color = defaultdict(list)

with open(analysis_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    player_name_idx = header.index('player_name')
    personal_year_idx = header.index('Personal Year')
    color_idx = header.index('color')
    score_idx = header.index('score')
    off_par_idx = header.index('off_par')
    round_num_idx = header.index('round_num')
    condition_idx = header.index('condition')

    for row in reader:
        if not row or row[player_name_idx].strip() == '':
            continue

        try:
            personal_year = row[personal_year_idx].strip() if personal_year_idx < len(row) else ''
            if not personal_year or personal_year == '' or not personal_year.isdigit():
                continue

            # Only process Year 7
            if int(personal_year) != 7:
                continue

            color = row[color_idx].strip() if color_idx < len(row) else ''
            if not color or color == '':
                continue

            score = float(row[score_idx]) if row[score_idx] else None
            if score is None:
                continue

            off_par = float(row[off_par_idx]) if off_par_idx < len(row) and row[off_par_idx] else None
            round_num = row[round_num_idx].strip() if round_num_idx < len(row) else ''
            condition = row[condition_idx].strip() if condition_idx < len(row) else ''

            year7_by_color[color].append({
                'player': row[player_name_idx],
                'score': score,
                'off_par': off_par,
                'round_num': round_num,
                'condition': condition
            })
        except (ValueError, IndexError):
            continue

# Analyze Year 7 performance by color
print("\n" + "="*100)
print("PERSONAL YEAR 7: PERFORMANCE BY COLOR")
print("="*100)

color_stats = {}
for color in sorted(year7_by_color.keys()):
    rounds = year7_by_color[color]

    if len(rounds) > 0:
        valid_off_par = [r['off_par'] for r in rounds if r['off_par'] is not None]
        avg_off_par = sum(valid_off_par) / len(valid_off_par) if len(valid_off_par) > 0 else None

        # Win rate: off_par < 0 means beating par
        beats_par = sum(1 for r in rounds if r['off_par'] is not None and r['off_par'] < 0)
        win_rate = (beats_par / len(rounds) * 100) if len(rounds) > 0 else 0

        color_stats[color] = {
            'count': len(rounds),
            'avg_off_par': avg_off_par,
            'win_rate': win_rate,
            'beats_par': beats_par
        }

# Print overall summary
print(f"\nTotal Year 7 Rounds: {sum(s['count'] for s in color_stats.values())}")
print(f"Total Unique Colors: {len(color_stats)}")

print(f"\n{'Color':<15} {'Rounds':<10} {'Avg Off-Par':<15} {'Win Rate':<15} {'Beats Par':<10}")
print("-" * 70)

# Sort by win rate
for color in sorted(color_stats.keys(), key=lambda x: color_stats[x]['win_rate'], reverse=True):
    stats = color_stats[color]
    print(f"{color:<15} {stats['count']:<10} {stats['avg_off_par']:<15.3f} {stats['win_rate']:<14.1f}% {stats['beats_par']:<10}")

# Highlight top performers
print("\n" + "="*100)
print("YEAR 7 COLOR RANKINGS")
print("="*100)

# By win rate
print("\nBest Colors (by Win Rate):")
top_colors_wr = sorted(color_stats.items(), key=lambda x: x[1]['win_rate'], reverse=True)
for i, (color, stats) in enumerate(top_colors_wr[:5], 1):
    print(f"  {i}. {color:<12} {stats['win_rate']:5.1f}% win rate ({stats['count']} rounds)")

# By off-par
print("\nBest Colors (by Off-Par):")
top_colors_op = sorted(color_stats.items(), key=lambda x: x[1]['avg_off_par'] if x[1]['avg_off_par'] else 0)
for i, (color, stats) in enumerate(top_colors_op[:5], 1):
    print(f"  {i}. {color:<12} {stats['avg_off_par']:7.3f} off-par ({stats['count']} rounds)")

# By volume
print("\nMost Common Colors (by Volume):")
top_colors_vol = sorted(color_stats.items(), key=lambda x: x[1]['count'], reverse=True)
for i, (color, stats) in enumerate(top_colors_vol[:5], 1):
    print(f"  {i}. {color:<12} {stats['count']:4d} rounds ({stats['win_rate']:5.1f}% WR)")

# Round-specific analysis
print("\n" + "="*100)
print("YEAR 7 COLOR PERFORMANCE BY ROUND TYPE")
print("="*100)

year7_by_color_round = defaultdict(lambda: defaultdict(list))
for color in year7_by_color.keys():
    for round_data in year7_by_color[color]:
        round_num = round_data['round_num']
        year7_by_color_round[color][round_num].append(round_data)

for color in sorted(year7_by_color.keys()):
    print(f"\n{color.upper()}:")
    for round_num in sorted(year7_by_color_round[color].keys()):
        rounds = year7_by_color_round[color][round_num]
        valid_off_par = [r['off_par'] for r in rounds if r['off_par'] is not None]
        avg_off_par = sum(valid_off_par) / len(valid_off_par) if len(valid_off_par) > 0 else None
        beats_par = sum(1 for r in rounds if r['off_par'] is not None and r['off_par'] < 0)
        win_rate = (beats_par / len(rounds) * 100) if len(rounds) > 0 else 0

        print(f"  Round {round_num}: {len(rounds):3d} rounds | {avg_off_par:7.3f} off-par | {win_rate:5.1f}% WR")

# Condition-specific analysis
print("\n" + "="*100)
print("YEAR 7 COLOR PERFORMANCE BY CONDITION")
print("="*100)

year7_by_color_cond = defaultdict(lambda: defaultdict(list))
for color in year7_by_color.keys():
    for round_data in year7_by_color[color]:
        condition = round_data['condition']
        year7_by_color_cond[color][condition].append(round_data)

for color in sorted(year7_by_color.keys()):
    print(f"\n{color.upper()}:")
    for condition in sorted(year7_by_color_cond[color].keys()):
        rounds = year7_by_color_cond[color][condition]
        valid_off_par = [r['off_par'] for r in rounds if r['off_par'] is not None]
        avg_off_par = sum(valid_off_par) / len(valid_off_par) if len(valid_off_par) > 0 else None
        beats_par = sum(1 for r in rounds if r['off_par'] is not None and r['off_par'] < 0)
        win_rate = (beats_par / len(rounds) * 100) if len(rounds) > 0 else 0

        print(f"  {condition:12} {len(rounds):3d} rounds | {avg_off_par:7.3f} off-par | {win_rate:5.1f}% WR")

# Find Year 7 + Color combos that beat baseline
print("\n" + "="*100)
print("YEAR 7 + COLOR COMBINATIONS (Above 50% Win Rate)")
print("="*100)

all_combos = []
for color in sorted(color_stats.keys()):
    stats = color_stats[color]
    if stats['win_rate'] >= 50.0:
        all_combos.append((color, stats))

if all_combos:
    print(f"\nStrong Signals (50%+ win rate):")
    for color, stats in sorted(all_combos, key=lambda x: x[1]['win_rate'], reverse=True):
        print(f"  Year 7 + {color:<12} {stats['win_rate']:5.1f}% WR | {stats['avg_off_par']:7.3f} off-par | {stats['count']} rounds")
else:
    print("\nNo colors reach 50%+ win rate for Year 7 alone")
    print("Best Year 7 color:")
    best = max(color_stats.items(), key=lambda x: x[1]['win_rate'])
    stats = best[1]
    print(f"  Year 7 + {best[0]:<12} {stats['win_rate']:5.1f}% WR | {stats['avg_off_par']:7.3f} off-par | {stats['count']} rounds")
